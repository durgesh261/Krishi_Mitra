"""
Research Architecture: Multimodal CropNet (Vision-Transformer/CNN + Climate Telemetry Fusion)
For Multi-Spectral Crop Disease Classification, Grad-CAM Interpretability, and Yield Regression
"""

import math
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

if TORCH_AVAILABLE:

    class SpatialVisualBackbone(nn.Module):
        """
        Deep spatial feature extractor for Multi-Spectral & Drone Foliage Imagery.
        Maintains spatial dimensions before pooling to allow Grad-CAM activation mapping.
        """
        def __init__(self, in_channels=3, feature_dim=256):
            super().__init__()
            self.stem = nn.Sequential(
                nn.Conv2d(in_channels, 64, kernel_size=7, stride=2, padding=3, bias=False),
                nn.BatchNorm2d(64),
                nn.GELU(),
                nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
            )
            
            # Residual Stage 1
            self.stage1 = nn.Sequential(
                nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1, bias=False),
                nn.BatchNorm2d(128),
                nn.GELU(),
                nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1, bias=False),
                nn.BatchNorm2d(128),
                nn.GELU()
            )
            
            # Residual Stage 2 (Target Layer for Grad-CAM)
            self.stage2 = nn.Sequential(
                nn.Conv2d(128, feature_dim, kernel_size=3, stride=2, padding=1, bias=False),
                nn.BatchNorm2d(feature_dim),
                nn.GELU(),
                nn.Conv2d(feature_dim, feature_dim, kernel_size=3, stride=1, padding=1, bias=False),
                nn.BatchNorm2d(feature_dim),
                nn.GELU()
            )
            
            self.gap = nn.AdaptiveAvgPool2d((1, 1))

        def forward(self, x):
            x = self.stem(x)
            x = self.stage1(x)
            spatial_features = self.stage2(x)  # Shape: (B, feature_dim, H', W')
            pooled = self.gap(spatial_features).flatten(1)  # Shape: (B, feature_dim)
            return spatial_features, pooled

    class ClimateTelemetryEncoder(nn.Module):
        """
        Processes micro-meteorological telemetry vectors:
        [Ambient Temp, Relative Humidity, 7-day Rainfall, Soil Moisture, VPD, Solar Radiation]
        """
        def __init__(self, input_dim=6, feature_dim=128):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(input_dim, 128),
                nn.LayerNorm(128),
                nn.GELU(),
                nn.Dropout(0.15),
                nn.Linear(128, feature_dim),
                nn.LayerNorm(feature_dim),
                nn.GELU()
            )

        def forward(self, x):
            return self.net(x)

    class CrossModalAttentionGate(nn.Module):
        """
        Cross-Modal Gated Attention:
        Fuses visual spatial embeddings and meteorological telemetry embeddings.
        Learns dynamic gating weights to selectively emphasize visual disease symptoms
        conditioned on micro-climate pathogen conduciveness.
        """
        def __init__(self, visual_dim=256, climate_dim=128, fused_dim=256):
            super().__init__()
            self.proj_visual = nn.Linear(visual_dim, fused_dim)
            self.proj_climate = nn.Linear(climate_dim, fused_dim)
            
            # Gating mechanism
            self.gate = nn.Sequential(
                nn.Linear(fused_dim * 2, fused_dim),
                nn.Sigmoid()
            )
            
            self.ln = nn.LayerNorm(fused_dim)

        def forward(self, z_v, z_c):
            v_proj = self.proj_visual(z_v)
            c_proj = self.proj_climate(z_c)
            
            concat = torch.cat([v_proj, c_proj], dim=-1)
            alpha = self.gate(concat)  # Gating weights in [0, 1]
            
            # Gated residual combination
            z_fused = alpha * v_proj + (1.0 - alpha) * c_proj
            return self.ln(z_fused)

    class MultimodalCropNet(nn.Module):
        """
        Unified Multi-Task Deep Architecture:
        - Input: Multi-spectral image (B, C, H, W) + Climate telemetry (B, 6)
        - Output 1: Disease Risk Multi-Class Logits (B, num_classes)
        - Output 2: Yield Forecast Regression (B, 1)
        """
        def __init__(self, num_classes=6, in_channels=3, climate_dim=6, fused_dim=256):
            super().__init__()
            self.visual_encoder = SpatialVisualBackbone(in_channels=in_channels, feature_dim=256)
            self.climate_encoder = ClimateTelemetryEncoder(input_dim=climate_dim, feature_dim=128)
            self.fusion_gate = CrossModalAttentionGate(visual_dim=256, climate_dim=128, fused_dim=fused_dim)
            
            # Multi-Task Head 1: Disease Classification
            self.disease_classifier = nn.Sequential(
                nn.Linear(fused_dim, 128),
                nn.GELU(),
                nn.Dropout(0.2),
                nn.Linear(128, num_classes)
            )
            
            # Multi-Task Head 2: Yield Estimation (Quintals / Hectare)
            self.yield_regressor = nn.Sequential(
                nn.Linear(fused_dim, 64),
                nn.GELU(),
                nn.Linear(64, 1)
            )

        def forward(self, img, climate_vector):
            spatial_feats, pooled_visual = self.visual_encoder(img)
            climate_feats = self.climate_encoder(climate_vector)
            
            fused_repr = self.fusion_gate(pooled_visual, climate_feats)
            
            disease_logits = self.disease_classifier(fused_repr)
            yield_pred = self.yield_regressor(fused_repr)
            
            return disease_logits, yield_pred, spatial_feats

    class GradCAMExplainer:
        """
        Gradient-weighted Class Activation Mapping (Grad-CAM)
        Computes gradients of the target class score w.r.t the last convolutional feature maps.
        """
        def __init__(self, model, target_layer):
            self.model = model
            self.target_layer = target_layer
            self.gradients = None
            self.activations = None
            
            target_layer.register_forward_hook(self._save_activation)
            target_layer.register_full_backward_hook(self._save_gradient)

        def _save_activation(self, module, input, output):
            self.activations = output

        def _save_gradient(self, module, grad_input, grad_output):
            self.gradients = grad_output[0]

        def generate_cam(self, img_tensor, climate_tensor, class_idx=None):
            self.model.eval()
            self.model.zero_grad()
            
            disease_logits, _, _ = self.model(img_tensor, climate_tensor)
            
            if class_idx is None:
                class_idx = torch.argmax(disease_logits, dim=-1).item()
                
            target_score = disease_logits[0, class_idx]
            target_score.backward()
            
            # Global Average Pooling on gradients
            weights = torch.mean(self.gradients, dim=(2, 3), keepdim=True)
            cam = torch.sum(weights * self.activations, dim=1, keepdim=True)
            cam = F.relu(cam)
            
            # Upsample to image size
            cam = F.interpolate(cam, size=img_tensor.shape[2:], mode='bilinear', align_corners=False)
            cam = cam.squeeze().detach().cpu().numpy()
            
            # Normalize [0, 1]
            cam_min, cam_max = cam.min(), cam.max()
            if cam_max > cam_min:
                cam = (cam - cam_min) / (cam_max - cam_min)
            return cam, class_idx

else:
    # Lightweight fallback representation for non-PyTorch runtimes
    class MultimodalCropNet:
        def __init__(self, *args, **kwargs):
            pass
        def forward(self, *args, **kwargs):
            raise NotImplementedError("PyTorch runtime required for training script execution.")

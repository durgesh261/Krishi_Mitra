"""
Multi-Task Multimodal Training Pipeline
Optimizes joint classification (Disease) and regression (Yield) loss:
L_total = L_CrossEntropy + lambda * L_MSE
"""

import os
import sys

try:
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader
    from models.multimodal_net import MultimodalCropNet
    from dataset.dataloader import MultimodalCropDataset, generate_synthetic_benchmark_dataset
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

def run_training(epochs=5, batch_size=32, lr=1e-3, lambda_yield=0.05):
    if not TORCH_AVAILABLE:
        print("[Notice] PyTorch runtime not detected. For training benchmarks, install PyTorch.")
        return

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Initializing Multimodal Crop Training on device: {device}")

    # Generate benchmark dataset
    images, climate, disease, yields = generate_synthetic_benchmark_dataset(num_samples=800)
    
    # Split 80/20 train/val
    split = int(0.8 * len(disease))
    train_ds = MultimodalCropDataset(images[:split], climate[:split], disease[:split], yields[:split])
    val_ds = MultimodalCropDataset(images[split:], climate[split:], disease[split:], yields[split:])

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)

    # Initialize model
    model = MultimodalCropNet(num_classes=6, in_channels=3, climate_dim=6, fused_dim=256).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    ce_loss_fn = nn.CrossEntropyLoss()
    mse_loss_fn = nn.MSELoss()

    print(f"[*] Training MultimodalCropNet for {epochs} epochs...")

    for epoch in range(1, epochs + 1):
        model.train()
        total_loss, correct, total = 0.0, 0, 0

        for batch in train_loader:
            img = batch["image"].to(device)
            clim = batch["climate"].to(device)
            d_true = batch["disease_label"].to(device)
            y_true = batch["yield_label"].to(device)

            optimizer.zero_grad()
            d_logits, y_pred, _ = model(img, clim)

            loss_d = ce_loss_fn(d_logits, d_true)
            loss_y = mse_loss_fn(y_pred, y_true)
            loss = loss_d + lambda_yield * loss_y

            loss.backward()
            optimizer.step()

            total_loss += loss.item() * len(d_true)
            preds = torch.argmax(d_logits, dim=-1)
            correct += (preds == d_true).sum().item()
            total += len(d_true)

        scheduler.step()
        train_acc = (correct / total) * 100.0

        # Validation phase
        model.eval()
        val_correct, val_total, val_mse = 0, 0, 0.0
        with torch.no_grad():
            for batch in val_loader:
                img = batch["image"].to(device)
                clim = batch["climate"].to(device)
                d_true = batch["disease_label"].to(device)
                y_true = batch["yield_label"].to(device)

                d_logits, y_pred, _ = model(img, clim)
                preds = torch.argmax(d_logits, dim=-1)
                val_correct += (preds == d_true).sum().item()
                val_total += len(d_true)
                val_mse += mse_loss_fn(y_pred, y_true).item() * len(y_true)

        val_acc = (val_correct / val_total) * 100.0
        val_rmse = (val_mse / val_total) ** 0.5

        print(f"Epoch [{epoch}/{epochs}] - Train Acc: {train_acc:.1f}% | Val Acc: {val_acc:.1f}% | Val Yield RMSE: {val_rmse:.2f} q/ha")

    # Save checkpoint
    os.makedirs("research/checkpoints", exist_ok=True)
    ckpt_path = "research/checkpoints/multimodal_cropnet.pt"
    torch.save(model.state_dict(), ckpt_path)
    print(f"[OK] Model checkpoint saved to: {ckpt_path}")

if __name__ == '__main__':
    run_training()

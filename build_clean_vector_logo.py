# -*- coding: utf-8 -*-
"""
Generates an authentic, prestigious, non-AI brand logo for Krishi Mitra.
National Agricultural Emblem Design:
- Outer Crest: Forest Green (#0e3d1b) with concentric 24K Harvest Gold trim (#f59e0b)
- Top Pristine Collar with crisp motto: "★ SMART FARMING & ADVISORY ★"
- Central Circular Vignette:
  - Golden Sunrise radiating over lush rolling green fields
  - Symmetrical Golden Wheat Ears (धान-गेहूं की स्वर्णिम बालियां)
  - Vibrant Emerald Sprout / Two Leaves (नव-अंकुर)
- Bottom Institutional Ribbon:
  - "KRISHI MITRA" in bold typography
  - "कृषि मित्र • KISAN SEVA" in gold Devanagari & English
"""

def generate_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="shieldBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0e3d1b"/>
      <stop offset="50%" stop-color="#14532d"/>
      <stop offset="100%" stop-color="#0a2e14"/>
    </linearGradient>

    <linearGradient id="medallionBg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="70%" stop-color="#f8fafc"/>
      <stop offset="100%" stop-color="#ecfdf5"/>
    </linearGradient>

    <!-- Rich Gold Gradient -->
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="30%" stop-color="#f59e0b"/>
      <stop offset="70%" stop-color="#d97706"/>
      <stop offset="100%" stop-color="#92400e"/>
    </linearGradient>

    <!-- Foliage Gradients -->
    <linearGradient id="leafGradLeft" x1="100%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#15803d"/>
      <stop offset="50%" stop-color="#22c55e"/>
      <stop offset="100%" stop-color="#86efac"/>
    </linearGradient>

    <linearGradient id="leafGradRight" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#166534"/>
      <stop offset="50%" stop-color="#16a34a"/>
      <stop offset="100%" stop-color="#4ade80"/>
    </linearGradient>

    <!-- Sunrise Gradient -->
    <linearGradient id="sunriseGrad" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.25"/>
      <stop offset="50%" stop-color="#fbbf24" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#fef08a" stop-opacity="0.95"/>
    </linearGradient>

    <!-- Terraced Fields Gradients -->
    <linearGradient id="fieldGrad1" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#22c55e"/>
      <stop offset="100%" stop-color="#15803d"/>
    </linearGradient>

    <linearGradient id="fieldGrad2" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#15803d"/>
      <stop offset="100%" stop-color="#14532d"/>
    </linearGradient>

    <filter id="dropShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#000000" flood-opacity="0.22"/>
    </filter>

    <filter id="badgeShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000000" flood-opacity="0.28"/>
    </filter>
  </defs>

  <!-- 1. Outer Circular Crest -->
  <circle cx="256" cy="256" r="242" fill="url(#shieldBg)" filter="url(#dropShadow)"/>
  <circle cx="256" cy="256" r="230" fill="none" stroke="url(#goldGrad)" stroke-width="4.5"/>
  <circle cx="256" cy="256" r="222" fill="none" stroke="#4ade80" stroke-width="1.5" stroke-dasharray="4 3"/>

  <!-- 2. Inner Medallion Background -->
  <circle cx="256" cy="256" r="212" fill="url(#medallionBg)" stroke="#cbd5e1" stroke-width="1.5"/>

  <!-- 3. Top Arc Motto (Positioned cleanly at radius 192 in the upper white collar) -->
  <path id="topMottoArc" d="M 96 156 A 192 192 0 0 1 416 156" fill="none"/>
  <text font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Montserrat', sans-serif" 
        font-size="12.5" font-weight="800" fill="#14532d" letter-spacing="3.2">
    <textPath href="#topMottoArc" startOffset="50%" text-anchor="middle">
      ★  SMART FARMING &amp; ADVISORY  ★
    </textPath>
  </text>

  <!-- 4. Central Circular Agricultural Vignette (Bordered Seal) -->
  <g id="centerArtwork">
    <!-- Vignette outer gold ring -->
    <circle cx="256" cy="250" r="130" fill="none" stroke="url(#goldGrad)" stroke-width="3"/>
    <circle cx="256" cy="250" r="128.5" fill="#f8fafc"/>

    <clipPath id="vignetteClip">
      <circle cx="256" cy="250" r="127"/>
    </clipPath>

    <g clip-path="url(#vignetteClip)">
      <!-- Sky -->
      <rect x="120" y="115" width="272" height="270" fill="#f8fafc"/>

      <!-- Rising Amber Sun -->
      <circle cx="256" cy="232" r="50" fill="url(#sunriseGrad)"/>
      <!-- Radiating Sunbeams -->
      <g stroke="#f59e0b" stroke-width="2.2" stroke-linecap="round" opacity="0.85">
        <line x1="256" y1="172" x2="256" y2="158"/>
        <line x1="226" y1="182" x2="216" y2="170"/>
        <line x1="286" y1="182" x2="296" y2="170"/>
        <line x1="202" y1="205" x2="190" y2="197"/>
        <line x1="310" y1="205" x2="322" y2="197"/>
        <line x1="190" y1="232" x2="176" y2="232"/>
        <line x1="322" y1="232" x2="336" y2="232"/>
      </g>

      <!-- Rolling Green Terraced Fields -->
      <!-- Distant Hills -->
      <path d="M 120 274 Q 190 242 270 259 Q 340 274 395 246 L 395 385 L 120 385 Z" fill="#86efac" opacity="0.5"/>
      <!-- Mid Hills -->
      <path d="M 120 286 Q 210 254 310 279 Q 360 292 395 276 L 395 385 L 120 385 Z" fill="url(#fieldGrad1)"/>
      <!-- Foreground Fertile Terraces -->
      <path d="M 120 310 Q 230 280 395 312 L 395 385 L 120 385 Z" fill="url(#fieldGrad2)"/>
      <!-- Furrow lines -->
      <path d="M 135 322 Q 235 296 385 326" fill="none" stroke="#4ade80" stroke-width="2" opacity="0.75"/>
      <path d="M 150 340 Q 240 318 370 344" fill="none" stroke="#86efac" stroke-width="1.8" opacity="0.6"/>
    </g>
  </g>

  <!-- 5. Symmetrical Golden Wheat Ears (Laurel Framing) -->
  <!-- Left Wheat Stalk -->
  <g id="leftWheat" fill="url(#goldGrad)" stroke="#92400e" stroke-width="1.1">
    <path d="M 235 350 C 190 325 162 265 174 190" fill="none" stroke="#b45309" stroke-width="2.8" stroke-linecap="round"/>
    <!-- Top Awn & Grain -->
    <path d="M 174 190 C 166 182 160 188 168 196 C 175 204 182 198 174 190 Z"/>
    <line x1="166" y1="184" x2="148" y2="163" stroke="#b45309" stroke-width="1.4" stroke-linecap="round"/>
    <!-- Grain Pair 1 -->
    <path d="M 166 211 C 154 203 148 213 158 221 C 168 229 176 219 166 211 Z"/>
    <line x1="156" y1="207" x2="132" y2="195" stroke="#b45309" stroke-width="1.4" stroke-linecap="round"/>
    <path d="M 184 205 C 196 197 202 207 194 215 C 186 223 176 215 184 205 Z"/>
    <line x1="198" y1="201" x2="218" y2="189" stroke="#b45309" stroke-width="1.4" stroke-linecap="round"/>
    <!-- Grain Pair 2 -->
    <path d="M 164 237 C 150 229 144 241 154 249 C 164 257 172 247 164 237 Z"/>
    <line x1="152" y1="233" x2="128" y2="227" stroke="#b45309" stroke-width="1.4" stroke-linecap="round"/>
    <path d="M 186 231 C 200 223 206 235 198 243 C 190 251 180 241 186 231 Z"/>
    <line x1="200" y1="227" x2="224" y2="219" stroke="#b45309" stroke-width="1.4" stroke-linecap="round"/>
    <!-- Grain Pair 3 -->
    <path d="M 168 263 C 156 257 150 267 160 275 C 170 281 178 271 168 263 Z"/>
    <line x1="156" y1="261" x2="134" y2="257" stroke="#b45309" stroke-width="1.4" stroke-linecap="round"/>
    <path d="M 192 257 C 206 251 210 263 202 271 C 194 279 184 269 192 257 Z"/>
    <!-- Grain Pair 4 -->
    <path d="M 178 289 C 166 285 162 295 172 301 C 180 307 188 297 178 289 Z"/>
    <path d="M 200 283 C 214 279 218 289 210 297 C 202 305 192 295 200 283 Z"/>
  </g>

  <!-- Right Wheat Stalk (Symmetrical) -->
  <g id="rightWheat" fill="url(#goldGrad)" stroke="#92400e" stroke-width="1.1">
    <path d="M 277 350 C 322 325 350 265 338 190" fill="none" stroke="#b45309" stroke-width="2.8" stroke-linecap="round"/>
    <!-- Top Awn & Grain -->
    <path d="M 338 190 C 346 182 352 188 344 196 C 337 204 330 198 338 190 Z"/>
    <line x1="346" y1="184" x2="364" y2="163" stroke="#b45309" stroke-width="1.4" stroke-linecap="round"/>
    <!-- Grain Pair 1 -->
    <path d="M 346 211 C 358 203 364 213 354 221 C 344 229 336 219 346 211 Z"/>
    <line x1="356" y1="207" x2="380" y2="195" stroke="#b45309" stroke-width="1.4" stroke-linecap="round"/>
    <path d="M 328 205 C 316 197 310 207 318 215 C 326 223 336 215 328 205 Z"/>
    <line x1="314" y1="201" x2="294" y2="189" stroke="#b45309" stroke-width="1.4" stroke-linecap="round"/>
    <!-- Grain Pair 2 -->
    <path d="M 348 237 C 362 229 368 241 358 249 C 348 257 340 247 348 237 Z"/>
    <line x1="360" y1="233" x2="384" y2="227" stroke="#b45309" stroke-width="1.4" stroke-linecap="round"/>
    <path d="M 326 231 C 312 223 306 235 314 243 C 322 251 332 241 326 231 Z"/>
    <line x1="312" y1="227" x2="288" y2="219" stroke="#b45309" stroke-width="1.4" stroke-linecap="round"/>
    <!-- Grain Pair 3 -->
    <path d="M 344 263 C 356 257 362 267 352 275 C 342 281 334 271 344 263 Z"/>
    <line x1="356" y1="261" x2="378" y2="257" stroke="#b45309" stroke-width="1.4" stroke-linecap="round"/>
    <path d="M 320 257 C 306 251 302 263 310 271 C 318 279 328 269 320 257 Z"/>
    <!-- Grain Pair 4 -->
    <path d="M 334 289 C 346 285 350 295 340 301 C 332 307 324 297 334 289 Z"/>
    <path d="M 312 283 C 298 279 294 289 302 297 C 310 305 320 295 312 283 Z"/>
  </g>

  <!-- 6. Central Sprouting Leaf / Seedling (नव-अंकुर) -->
  <g id="centerSprout" filter="url(#badgeShadow)">
    <!-- Main Left Leaf -->
    <path d="M 256 317 C 236 270 218 213 242 165 C 258 200 268 257 256 317 Z" 
          fill="url(#leafGradLeft)" stroke="#0e3d1b" stroke-width="2"/>
    <path d="M 253 303 Q 239 233 242 165" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.7"/>

    <!-- Main Right Leaf -->
    <path d="M 256 317 C 274 275 292 223 270 180 C 254 211 248 265 256 317 Z" 
          fill="url(#leafGradRight)" stroke="#0e3d1b" stroke-width="2"/>
    <path d="M 258 303 Q 270 243 270 180" fill="none" stroke="#ffffff" stroke-width="1.8" opacity="0.65"/>

    <!-- Small Budding Leaf Center -->
    <path d="M 256 305 C 249 287 251 269 256 257 C 261 269 263 287 256 305 Z" 
          fill="#86efac" stroke="#0e3d1b" stroke-width="1.2"/>

    <!-- Seed Node Axis -->
    <circle cx="256" cy="319" r="7.5" fill="#14532d" stroke="url(#goldGrad)" stroke-width="2.5"/>
    <circle cx="256" cy="319" r="3" fill="#fef08a"/>
  </g>

  <!-- 7. Prestigious Bottom Crest Banner -->
  <g id="bottomRibbon" filter="url(#badgeShadow)">
    <!-- Base Ribbon Shield -->
    <path d="M 72 385 C 160 365 352 365 440 385 C 452 418 438 450 422 450 C 342 438 170 438 90 450 C 74 450 60 418 72 385 Z" 
          fill="url(#shieldBg)" stroke="url(#goldGrad)" stroke-width="3"/>

    <!-- Golden Accent Inlays -->
    <path d="M 84 394 C 168 376 344 376 428 394" fill="none" stroke="#fde047" stroke-width="1.6"/>
    <path d="M 98 440 C 172 428 340 428 414 440" fill="none" stroke="#f59e0b" stroke-width="1.4"/>

    <!-- Main Title: KRISHI MITRA -->
    <text x="256" y="413" text-anchor="middle" 
          font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Montserrat', sans-serif" 
          font-weight="900" font-size="24" fill="#ffffff" letter-spacing="3.5">
      KRISHI MITRA
    </text>

    <!-- Subtitle: कृषि मित्र • KISAN SEVA -->
    <text x="256" y="433" text-anchor="middle" 
          font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Nirmala UI', 'Mangal', sans-serif" 
          font-weight="700" font-size="12" fill="#fbbf24" letter-spacing="2">
      कृषि मित्र  •  KISAN SEVA
    </text>
  </g>
</svg>'''
    with open('static/logo.svg', 'w', encoding='utf-8') as f:
        f.write(svg)
    print("Written static/logo.svg successfully!")

if __name__ == '__main__':
    generate_svg()

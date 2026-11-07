import os

out_dir = "C:/Users/nanda/OneDrive/Desktop/RAVEN/assets/animations"
os.makedirs(out_dir, exist_ok=True)

# ============================================================
# DESIGN TOKENS - Consistent across all animations
# ============================================================
BG = "#0a0f0a"           # Deep comfortable dark
GRID = "#152515"         # Subtle grid lines
PRIMARY = "#00d47e"      # Softer green (less harsh than #00ff88)
PRIMARY_DIM = "#00663d"  # Dimmed for backgrounds
ACCENT = "#ffaa00"       # Amber for warnings/critical
CRITICAL = "#ff3355"     # Red for vulnerabilities
TEXT_PRIMARY = "#c8e8d0" # Readable text
TEXT_MUTED = "#6a8a72"   # Muted labels
TEXT_DIM = "#405044"     # Very subtle
BORDER = "#1a3a2a"       # Container borders
GLOW = "drop-shadow(0 0 6px #00d47e)"
GLOW_RED = "drop-shadow(0 0 8px #ff3355)"
GLOW_AMBER = "drop-shadow(0 0 6px #ffaa00)"

# ============================================================
# 1. NETWORK SCAN - Clean, spacious, aligned
# ============================================================
network_scan = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 260" width="520" height="260">
  <defs>
    <style>
      @keyframes pulse {{ 0%,100% {{ opacity: 0.4; r: 5; }} 50% {{ opacity: 1; r: 9; }} }}
      @keyframes sweep {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
      @keyframes packet {{ 0% {{ offset-distance: 0%; opacity: 1; }} 100% {{ offset-distance: 100%; opacity: 0; }} }}
      @keyframes scanline {{ 0% {{ y: 20; opacity: 0.6; }} 100% {{ y: 240; opacity: 0; }} }}
      .node {{ fill: {PRIMARY}; filter: {GLOW}; }}
      .node-active {{ animation: pulse 2s ease-in-out infinite; }}
      .scan-ring {{ stroke: {PRIMARY}; stroke-width: 1.5; fill: none; opacity: 0.35; animation: sweep 6s linear infinite; transform-origin: 260px 130px; }}
      .packet {{ fill: {PRIMARY}; filter: {GLOW}; r: 3.5; animation: packet 4s ease-in-out infinite; }}
      .scan-line {{ stroke: {PRIMARY}; stroke-width: 1.5; opacity: 0.7; animation: scanline 3s ease-out infinite; }}
      .connection {{ stroke: {PRIMARY}; stroke-width: 0.6; opacity: 0.2; stroke-dasharray: 6 6; }}
      .label {{ fill: {TEXT_PRIMARY}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 10px; text-anchor: middle; }}
      .status {{ fill: {TEXT_MUTED}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 10px; text-anchor: middle; }}
      .title {{ fill: {PRIMARY}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 11px; font-weight: 600; text-anchor: middle; }}
    </style>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#081208"/>
      <stop offset="100%" stop-color="#0a0f0a"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="520" height="260" fill="url(#bgGrad)"/>
  <g stroke="{GRID}" stroke-width="0.5" opacity="0.4">
    <line x1="0" y1="0" x2="520" y2="0" /><line x1="0" y1="65" x2="520" y2="65" />
    <line x1="0" y1="130" x2="520" y2="130" /><line x1="0" y1="195" x2="520" y2="195" />
    <line x1="0" y1="260" x2="520" y2="260" />
    <line x1="0" y1="0" x2="0" y2="260" /><line x1="130" y1="0" x2="130" y2="260" />
    <line x1="260" y1="0" x2="260" y2="260" /><line x1="390" y1="0" x2="390" y2="260" />
    <line x1="520" y1="0" x2="520" y2="260" />
  </g>

  <!-- Title bar -->
  <rect x="10" y="10" width="500" height="28" fill="{BORDER}" rx="4" opacity="0.6"/>
  <text class="title" x="260" y="29">NETWORK RECONNAISSANCE</text>

  <!-- Central scanner -->
  <g transform="translate(260,130)">
    <circle class="scan-ring" r="45" />
    <circle class="scan-ring" r="75" style="animation-delay: -2s;" />
    <circle class="scan-ring" r="105" style="animation-delay: -4s;" />
    <line class="scan-line" x1="0" y1="20" x2="0" y2="20" transform="rotate(-90)" />
    
    <!-- Central hub -->
    <circle class="node node-active" r="7" />
    <circle r="16" stroke="{PRIMARY}" stroke-width="1.5" fill="none" opacity="0.4" />
    <circle r="26" stroke="{PRIMARY}" stroke-width="0.8" fill="none" opacity="0.2" />
    <circle r="36" stroke="{PRIMARY}" stroke-width="0.5" fill="none" opacity="0.1" />
  </g>

  <!-- Host nodes in 4 quadrants - properly spaced -->
  <g>
    <!-- NW -->
    <line class="connection" x1="260" y1="130" x2="100" y2="55" />
    <circle class="node node-active" cx="100" cy="55" r="5" style="animation-delay: 0.2s;" />
    <text class="label" x="100" y="40">10.0.1.5</text>
    <text class="label" x="100" y="68" style="font-size: 8px; fill: {TEXT_DIM};">HTTP/SSH</text>

    <!-- NE -->
    <line class="connection" x1="260" y1="130" x2="420" y2="55" />
    <circle class="node node-active" cx="420" cy="55" r="5" style="animation-delay: 0.5s;" />
    <text class="label" x="420" y="40">192.168.1.10</text>
    <text class="label" x="420" y="68" style="font-size: 8px; fill: {TEXT_DIM};">RDP/SMB</text>

    <!-- SW -->
    <line class="connection" x1="260" y1="130" x2="100" y2="205" />
    <circle class="node node-active" cx="100" cy="205" r="5" style="animation-delay: 0.8s;" />
    <text class="label" x="100" y="190">172.16.0.3</text>
    <text class="label" x="100" y="218" style="font-size: 8px; fill: {TEXT_DIM};">PostgreSQL</text>

    <!-- SE -->
    <line class="connection" x1="260" y1="130" x2="420" y2="205" />
    <circle class="node node-active" cx="420" cy="205" r="5" style="animation-delay: 1.1s;" />
    <text class="label" x="420" y="190">10.10.0.7</text>
    <text class="label" x="420" y="218" style="font-size: 8px; fill: {TEXT_DIM};">LDAP/DNS</text>

    <!-- Mid-ring nodes -->
    <line class="connection" x1="260" y1="130" x2="160" y2="80" />
    <circle class="node node-active" cx="160" cy="80" r="4" style="animation-delay: 1.4s;" />
    <line class="connection" x1="260" y1="130" x2="360" y2="80" />
    <circle class="node node-active" cx="360" cy="80" r="4" style="animation-delay: 1.6s;" />
    <line class="connection" x1="260" y1="130" x2="160" y2="180" />
    <circle class="node node-active" cx="160" cy="180" r="4" style="animation-delay: 1.8s;" />
    <line class="connection" x1="260" y1="130" x2="360" y2="180" />
    <circle class="node node-active" cx="360" cy="180" r="4" style="animation-delay: 2.0s;" />
  </g>

  <!-- Data packets on curved paths -->
  <circle class="packet" offset-path="path('M 260 130 Q 180 90 100 55')" />
  <circle class="packet" style="animation-delay: -1.3s;" offset-path="path('M 260 130 Q 340 90 420 55')" />
  <circle class="packet" style="animation-delay: -2.6s;" offset-path="path('M 260 130 Q 180 170 100 205')" />

  <!-- Status bar at bottom -->
  <rect x="10" y="222" width="500" height="28" fill="{BORDER}" rx="4" opacity="0.6"/>
  <text class="status" x="260" y="239">SCANNING  \u2022  8 HOSTS ALIVE  \u2022  23 PORTS OPEN  \u2022  3 SERVICES ENUMERATED</text>
</svg>'''

# ============================================================
# 2. DATA FLOW PIPELINE - Horizontal, clean stages
# ============================================================
data_flow = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 200" width="700" height="200">
  <defs>
    <style>
      @keyframes flow {{ 0% {{ offset-distance: 0%; opacity: 1; }} 100% {{ offset-distance: 100%; opacity: 0.2; }} }}
      @keyframes process {{ 0%,100% {{ opacity: 0.6; transform: scale(1); }} 50% {{ opacity: 1; transform: scale(1.03); }} }}
      @keyframes pulse-line {{ 0%,100% {{ stroke-opacity: 0.3; }} 50% {{ stroke-opacity: 1; }} }}
      .stage {{ fill: #0d180d; stroke: {BORDER}; stroke-width: 1.5; rx: 10; }}
      .stage.active {{ animation: process 2.5s ease-in-out infinite; }}
      .pipe {{ stroke: {PRIMARY}; stroke-width: 3; fill: none; opacity: 0.25; animation: pulse-line 2s ease-in-out infinite; }}
      .packet {{ fill: {PRIMARY}; filter: {GLOW}; r: 4; animation: flow 5s linear infinite; }}
      .label {{ fill: {TEXT_PRIMARY}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 11px; font-weight: 600; text-anchor: middle; }}
      .sub-label {{ fill: {TEXT_MUTED}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 9px; text-anchor: middle; }}
      .metric {{ fill: {PRIMARY}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 10px; font-weight: 600; text-anchor: middle; }}
      .title {{ fill: {PRIMARY}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 12px; font-weight: 600; text-anchor: middle; }}
      .footer {{ fill: {TEXT_MUTED}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 9px; text-anchor: middle; }}
    </style>
    <linearGradient id="pipeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{PRIMARY}" stop-opacity="0.15"/>
      <stop offset="50%" stop-color="{PRIMARY}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{PRIMARY}" stop-opacity="0.15"/>
    </linearGradient>
    <marker id="arrow" markerWidth="10" markerHeight="8" refX="8" refY="4" orient="auto">
      <path d="M0,0 L10,4 L0,8 Z" fill="{PRIMARY}" opacity="0.6"/>
    </marker>
  </defs>

  <rect width="700" height="200" fill="{BG}"/>
  <g stroke="{GRID}" stroke-width="0.5" opacity="0.3">
    <line x1="0" y1="0" x2="700" y2="0" /><line x1="0" y1="100" x2="700" y2="100" />
    <line x1="0" y1="200" x2="700" y2="200" />
  </g>

  <!-- Title -->
  <rect x="15" y="12" width="670" height="26" fill="{BORDER}" rx="4" opacity="0.5"/>
  <text class="title" x="350" y="30">VULNERABILITY INTELLIGENCE PIPELINE</text>

  <!-- Main pipeline at y=100 (center) -->
  <g transform="translate(0, 40)">
    <!-- Stage 1: INGEST -->
    <rect class="stage active" x="25" y="30" width="130" height="90" style="animation-delay: 0s;" />
    <text class="label" x="90" y="58">INGEST</text>
    <text class="sub-label" x="90" y="74">Nmap / ZAP / httpx</text>
    <text class="metric" x="90" y="96">2,847 req/s</text>
    <circle class="packet" cx="90" cy="128" />

    <!-- Pipe 1 -->
    <line class="pipe" x1="155" y1="75" x2="190" y2="75" marker-end="url(#arrow)" />

    <!-- Stage 2: NORMALIZE -->
    <rect class="stage active" x="200" y="30" width="130" height="90" style="animation-delay: -0.5s;" />
    <text class="label" x="265" y="58">NORMALIZE</text>
    <text class="sub-label" x="265" y="74">Parse \u2192 Validate \u2192 Schema</text>
    <text class="metric" x="265" y="96">1,923 obj/s</text>
    <circle class="packet" cx="265" cy="128" style="animation-delay: -0.6s;" />

    <!-- Pipe 2 -->
    <line class="pipe" x1="330" y1="75" x2="365" y2="75" marker-end="url(#arrow)" />

    <!-- Stage 3: CORRELATE -->
    <rect class="stage active" x="375" y="30" width="150" height="90" style="animation-delay: -1s;" />
    <text class="label" x="450" y="58">CORRELATE</text>
    <text class="sub-label" x="450" y="74">CVE / KEV / EPSS / ATT\u0026CK</text>
    <text class="metric" x="450" y="96">94.2% match</text>
    <circle class="packet" cx="450" cy="128" style="animation-delay: -1.2s;" />

    <!-- Pipe 3 -->
    <line class="pipe" x1="525" y1="75" x2="560" y2="75" marker-end="url(#arrow)" />

    <!-- Stage 4: RISK SCORE -->
    <rect class="stage active" x="570" y="30" width="115" height="90" style="animation-delay: -1.5s;" />
    <text class="label" x="627" y="58">RISK SCORE</text>
    <text class="sub-label" x="627" y="74">CVSS + EPSS + KEV</text>
    <text class="metric" x="627" y="96">8.7 / 10</text>
    <circle class="packet" cx="627" cy="128" style="animation-delay: -1.8s;" />
  </g>

  <!-- Continuous packet stream on pipes -->
  <g>
    <circle class="packet" style="animation-delay: 0s;" offset-path="path('M 155 75 L 560 75')" />
    <circle class="packet" style="animation-delay: -1.25s;" offset-path="path('M 155 75 L 560 75')" />
    <circle class="packet" style="animation-delay: -2.5s;" offset-path="path('M 155 75 L 560 75')" />
    <circle class="packet" style="animation-delay: -3.75s;" offset-path="path('M 155 75 L 560 75')" />
  </g>

  <!-- Footer metrics bar -->
  <rect x="25" y="162" width="650" height="26" fill="{BORDER}" rx="6" opacity="0.5"/>
  <text class="footer" x="350" y="180">THROUGHPUT: 2,847 events/sec  \u2022  LATENCY (p99): 14ms  \u2022  ERROR RATE: 0.018%  \u2022  QUEUE: 12 pending</text>
</svg>'''

# ============================================================
# 3. NEURAL REASONING - Layered, breathing, clear
# ============================================================
neural_net = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 360" width="600" height="360">
  <defs>
    <style>
      @keyframes neuron-fire {{ 0%,100% {{ opacity: 0.35; r: 9; }} 50% {{ opacity: 1; r: 15; filter: drop-shadow(0 0 14px #00d47e); }} }}
      @keyframes synapse {{ 0% {{ stroke-opacity: 0.05; stroke-width: 0.4; }} 40% {{ stroke-opacity: 0.8; stroke-width: 2; }} 100% {{ stroke-opacity: 0.05; stroke-width: 0.4; }} }}
      @keyframes bubble-in {{ 0% {{ opacity: 0; transform: translateY(10px) scale(0.95); }} 15% {{ opacity: 1; transform: translateY(0) scale(1); }} 85% {{ opacity: 1; transform: translateY(0) scale(1); }} 100% {{ opacity: 0; transform: translateY(-10px) scale(1.05); }} }}
      .neuron {{ fill: {PRIMARY}; filter: {GLOW}; }}
      .neuron-in {{ animation: neuron-fire 3.5s ease-in-out infinite; }}
      .neuron-h1 {{ animation: neuron-fire 3.5s ease-in-out infinite; animation-delay: -0.6s; }}
      .neuron-h2 {{ animation: neuron-fire 3.5s ease-in-out infinite; animation-delay: -1.2s; }}
      .neuron-h3 {{ animation: neuron-fire 3.5s ease-in-out infinite; animation-delay: -1.8s; }}
      .neuron-out {{ animation: neuron-fire 3.5s ease-in-out infinite; animation-delay: -2.4s; }}
      .synapse {{ stroke: {PRIMARY}; stroke-width: 0.6; opacity: 0.12; animation: synapse 2.5s ease-in-out infinite; }}
      .bubble {{ fill: #0d180d; stroke: {BORDER}; stroke-width: 1.5; rx: 14; opacity: 0; animation: bubble-in 5s ease-in-out infinite; }}
      .bubble-text {{ fill: {TEXT_PRIMARY}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 10px; text-anchor: middle; }}
      .bubble-sub {{ fill: {TEXT_MUTED}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 9px; text-anchor: middle; }}
      .label {{ fill: {PRIMARY}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 11px; font-weight: 600; text-anchor: middle; }}
      .sub-label {{ fill: {TEXT_MUTED}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 9px; text-anchor: middle; }}
      .status-text {{ fill: {TEXT_PRIMARY}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 9px; text-anchor: start; }}
      .status-val {{ fill: {PRIMARY}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 9px; font-weight: 600; text-anchor: start; }}
    </style>
    <linearGradient id="neuronGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PRIMARY}"/>
      <stop offset="100%" stop-color="#004422"/>
    </linearGradient>
    <filter id="softGlow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect width="600" height="360" fill="{BG}"/>
  <g stroke="{GRID}" stroke-width="0.4" opacity="0.25">
    <line x1="0" y1="0" x2="600" y2="0" /><line x1="0" y1="120" x2="600" y2="120" />
    <line x1="0" y1="240" x2="600" y2="240" /><line x1="0" y1="360" x2="600" y2="360" />
  </g>

  <!-- Title bar -->
  <rect x="12" y="12" width="576" height="30" fill="{BORDER}" rx="5" opacity="0.5"/>
  <text class="label" x="300" y="34">REASONING ENGINE \u2014 LOCAL INFERENCE</text>

  <!-- INPUT LAYER (left) - 4 neurons, spaced -->
  <g transform="translate(50, 60)">
    <text class="label" x="0" y="-30">INPUT</text>
    <text class="sub-label" x="0" y="300">Assets \u2022 Vuln Intel \u2022 Policy \u2022 Context</text>
    <circle class="neuron neuron-in" cy="30" r="11" />
    <circle class="neuron neuron-in" cy="90" r="11" style="animation-delay: -0.4s;" />
    <circle class="neuron neuron-in" cy="150" r="11" style="animation-delay: -0.8s;" />
    <circle class="neuron neuron-in" cy="210" r="11" style="animation-delay: -1.2s;" />
    <text class="sub-label" x="30" y="33" style="font-size: 8px;">vec[4096]</text>
    <text class="sub-label" x="30" y="93" style="font-size: 8px;">vec[4096]</text>
    <text class="sub-label" x="30" y="153" style="font-size: 8px;">vec[4096]</text>
    <text class="sub-label" x="30" y="213" style="font-size: 8px;">vec[4096]</text>
  </g>

  <!-- HIDDEN LAYERS - 3 layers, properly spaced horizontally -->
  <!-- Hidden 1: 6 neurons at x=180 -->
  <g transform="translate(180, 60)">
    <circle class="neuron neuron-h1" cy="20" r="9" />
    <circle class="neuron neuron-h1" cy="70" r="9" style="animation-delay: -0.2s;" />
    <circle class="neuron neuron-h1" cy="120" r="9" style="animation-delay: -0.4s;" />
    <circle class="neuron neuron-h1" cy="170" r="9" style="animation-delay: -0.6s;" />
    <circle class="neuron neuron-h1" cy="220" r="9" style="animation-delay: -0.8s;" />
    <circle class="neuron neuron-h1" cy="270" r="9" style="animation-delay: -1.0s;" />
  </g>

  <!-- Hidden 2: 8 neurons at x=320 -->
  <g transform="translate(320, 60)">
    <circle class="neuron neuron-h2" cy="10" r="8" style="animation-delay: -0.1s;" />
    <circle class="neuron neuron-h2" cy="55" r="8" style="animation-delay: -0.3s;" />
    <circle class="neuron neuron-h2" cy="100" r="8" style="animation-delay: -0.5s;" />
    <circle class="neuron neuron-h2" cy="145" r="8" style="animation-delay: -0.7s;" />
    <circle class="neuron neuron-h2" cy="190" r="8" style="animation-delay: -0.9s;" />
    <circle class="neuron neuron-h2" cy="235" r="8" style="animation-delay: -1.1s;" />
    <circle class="neuron neuron-h2" cy="280" r="8" style="animation-delay: -1.3s;" />
    <circle class="neuron neuron-h2" cy="325" r="8" style="animation-delay: -1.5s;" />
  </g>

  <!-- Hidden 3: 5 neurons at x=460 -->
  <g transform="translate(460, 60)">
    <circle class="neuron neuron-h3" cy="30" r="9" style="animation-delay: -0.2s;" />
    <circle class="neuron neuron-h3" cy="90" r="9" style="animation-delay: -0.5s;" />
    <circle class="neuron neuron-h3" cy="150" r="9" style="animation-delay: -0.8s;" />
    <circle class="neuron neuron-h3" cy="210" r="9" style="animation-delay: -1.1s;" />
    <circle class="neuron neuron-h3" cy="270" r="9" style="animation-delay: -1.4s;" />
  </g>

  <!-- OUTPUT LAYER (right) - 3 neurons -->
  <g transform="translate(550, 60)">
    <text class="label" x="-10" y="-30">OUTPUT</text>
    <text class="sub-label" x="-10" y="300">Action \u2022 Target \u2022 Risk</text>
    <circle class="neuron neuron-out" cy="50" r="11" />
    <circle class="neuron neuron-out" cy="150" r="11" style="animation-delay: -0.4s;" />
    <circle class="neuron neuron-out" cy="250" r="11" style="animation-delay: -0.8s;" />
    <text class="sub-label" x="30" y="53" style="font-size: 8px;">Action</text>
    <text class="sub-label" x="30" y="153" style="font-size: 8px;">Target</text>
    <text class="sub-label" x="30" y="253" style="font-size: 8px;">Risk</text>
  </g>

  <!-- SYNAPSES - Clean, subset connections for visual clarity -->
  <g class="synapses" stroke="{PRIMARY}" stroke-width="0.5" opacity="0.1">
    <!-- Input to Hidden1 (full connection sample) -->
    <line x1="61" y1="90" x2="171" y2="80" class="synapse" style="animation-delay: 0s;" />
    <line x1="61" y1="90" x2="171" y2="130" class="synapse" style="animation-delay: -0.1s;" />
    <line x1="61" y1="150" x2="171" y2="80" class="synapse" style="animation-delay: -0.05s;" />
    <line x1="61" y1="150" x2="171" y2="130" class="synapse" style="animation-delay: -0.15s;" />
    <line x1="61" y1="150" x2="171" y2="180" class="synapse" style="animation-delay: -0.25s;" />
    <line x1="61" y1="210" x2="171" y2="180" class="synapse" style="animation-delay: -0.2s;" />
    <line x1="61" y1="210" x2="171" y2="230" class="synapse" style="animation-delay: -0.3s;" />
    <line x1="61" y1="210" x2="171" y2="280" class="synapse" style="animation-delay: -0.4s;" />
    <!-- Hidden1 to Hidden2 -->
    <line x1="189" y1="20" x2="311" y2="10" class="synapse" style="animation-delay: -0.3s;" />
    <line x1="189" y1="70" x2="311" y2="55" class="synapse" style="animation-delay: -0.35s;" />
    <line x1="189" y1="120" x2="311" y2="100" class="synapse" style="animation-delay: -0.4s;" />
    <line x1="189" y1="170" x2="311" y2="145" class="synapse" style="animation-delay: -0.45s;" />
    <line x1="189" y1="220" x2="311" y2="190" class="synapse" style="animation-delay: -0.5s;" />
    <line x1="189" y1="270" x2="311" y2="235" class="synapse" style="animation-delay: -0.55s;" />
    <!-- Hidden2 to Hidden3 -->
    <line x1="328" y1="10" x2="451" y2="30" class="synapse" style="animation-delay: -0.5s;" />
    <line x1="328" y1="55" x2="451" y2="90" class="synapse" style="animation-delay: -0.55s;" />
    <line x1="328" y1="100" x2="451" y2="150" class="synapse" style="animation-delay: -0.6s;" />
    <line x1="328" y1="145" x2="451" y2="210" class="synapse" style="animation-delay: -0.65s;" />
    <line x1="328" y1="190" x2="451" y2="270" class="synapse" style="animation-delay: -0.7s;" />
    <!-- Hidden3 to Output -->
    <line x1="469" y1="30" x2="541" y2="50" class="synapse" style="animation-delay: -0.7s;" />
    <line x1="469" y1="90" x2="541" y2="150" class="synapse" style="animation-delay: -0.75s;" />
    <line x1="469" y1="150" x2="541" y2="250" class="synapse" style="animation-delay: -0.8s;" />
  </g>

  <!-- Layer Labels -->
  <text class="label" x="180" y="30" style="fill: {TEXT_MUTED}; font-size: 9px;">HIDDEN 1 (6)</text>
  <text class="label" x="320" y="30" style="fill: {TEXT_MUTED}; font-size: 9px;">HIDDEN 2 (8)</text>
  <text class="label" x="460" y="30" style="fill: {TEXT_MUTED}; font-size: 9px;">HIDDEN 3 (5)</text>

  <!-- THOUGHT BUBBLES - Properly positioned, non-overlapping -->
  <g>
    <!-- Bubble 1: Analysis -->
    <rect class="bubble" x="180" y="10" width="280" height="48" style="animation-delay: 0s;" />
    <text class="bubble-text" x="320" y="30">ANALYZING: web.app.corp:443 \u2192 TLS 1.3 \u2192 Cert Valid \u2192 CN=*.corp</text>
    <text class="bubble-sub" x="320" y="46">CONFIDENCE: 96% \u2022 LATENCY: 187ms</text>

    <!-- Bubble 2: Correlation -->
    <rect class="bubble" x="180" y="140" width="280" height="48" style="animation-delay: -1.7s;" />
    <text class="bubble-text" x="320" y="160">CORRELATING: CVE-2023-48795 \u2192 SSH Service Match \u2192 OpenSSH 9.2p1</text>
    <text class="bubble-sub" x="320" y="176">EPSS: 0.91 \u2022 KEV: LISTED \u2022 CVSS: 9.1</text>

    <!-- Bubble 3: Proposal -->
    <rect class="bubble" x="180" y="270" width="280" height="48" style="animation-delay: -3.4s;" />
    <text class="bubble-text" x="320" y="290">PROPOSING: ZAP Active Scan \u2192 L2 Controlled \u2192 Target: api.internal</text>
    <text class="bubble-sub" x="320" y="306">RISK: 8.4/10 \u2022 POLICY: APPROVED \u2022 QUEUED</text>
  </g>

  <!-- STATUS PANEL (top-left) -->
  <rect x="12" y="52" width="160" height="140" fill="{BORDER}" rx="6" opacity="0.6"/>
  <text class="status-text" x="20" y="74">MODEL</text>
  <text class="status-val" x="20" y="90">llama3.1:8b</text>
  <text class="status-text" x="20" y="108">CONTEXT</text>
  <text class="status-val" x="20" y="124">4096 / 4096</text>
  <text class="status-text" x="20" y="142">TEMPERATURE</text>
  <text class="status-val" x="20" y="158">0.10</text>
  <text class="status-text" x="20" y="176">INFERENCE</text>
  <text class="status-val" x="20" y="192">234 ms</text>

  <!-- QUEUE PANEL (bottom-left) -->
  <rect x="12" y="204" width="160" height="100" fill="{BORDER}" rx="6" opacity="0.6"/>
  <text class="status-text" x="20" y="226">PROPOSAL QUEUE</text>
  <text class="status-val" x="20" y="244">PENDING: 3</text>
  <text class="status-val" x="20" y="260">APPROVED: 1</text>
  <text class="status-val" x="20" y="276">BLOCKED: 0</text>
  <text class="status-text" x="20" y="294">POLICY LEVEL: L2</text>
</svg>'''

# ============================================================
# 4. ATTACK GRAPH - Structured, layered, clear hierarchy
# ============================================================
attack_graph = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 380" width="600" height="380">
  <defs>
    <style>
      @keyframes pulse-node {{ 0%,100% {{ opacity: 0.5; r: 7; }} 50% {{ opacity: 1; r: 11; filter: drop-shadow(0 0 10px #ff3355); }} }}
      @keyframes pulse-critical {{ 0%,100% {{ opacity: 0.4; r: 10; }} 50% {{ opacity: 1; r: 16; filter: drop-shadow(0 0 14px #ff3355); }} }}
      @keyframes edge-flow {{ 0% {{ stroke-dashoffset: 16; opacity: 0.25; }} 100% {{ stroke-dashoffset: 0; opacity: 0.9; }} }}
      @keyframes path-glow {{ 0%,100% {{ stroke-width: 2; opacity: 0.4; }} 50% {{ stroke-width: 4; opacity: 1; filter: drop-shadow(0 0 8px #ff3355); }} }}
      @keyframes alert {{ 0%,100% {{ opacity: 0.5; }} 50% {{ opacity: 1; transform: scale(1.15); }} }}
      .node-asset {{ fill: {PRIMARY}; filter: {GLOW}; }}
      .node-vuln {{ fill: {CRITICAL}; filter: {GLOW_RED}; }}
      .node-exploit {{ fill: {ACCENT}; filter: {GLOW_AMBER}; }}
      .node-critical {{ animation: pulse-critical 2s ease-in-out infinite; }}
      .node-normal {{ animation: pulse-node 2.5s ease-in-out infinite; }}
      .edge {{ stroke: {CRITICAL}; stroke-width: 1.5; fill: none; stroke-dasharray: 10 6; animation: edge-flow 1.8s linear infinite; }}
      .edge-evi {{ stroke: {PRIMARY}; stroke-width: 1; fill: none; opacity: 0.35; stroke-dasharray: 6 6; }}
      .path-crit {{ stroke: {CRITICAL}; stroke-width: 3; fill: none; animation: path-glow 2s ease-in-out infinite; }}
      .alert {{ fill: {CRITICAL}; filter: {GLOW_RED}; animation: alert 1.2s ease-in-out infinite; }}
      .label {{ fill: {TEXT_PRIMARY}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 9px; text-anchor: middle; }}
      .label-sm {{ fill: {TEXT_MUTED}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 8px; text-anchor: middle; }}
      .sev {{ fill: {CRITICAL}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 8px; font-weight: 600; text-anchor: middle; }}
      .panel-title {{ fill: {PRIMARY}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 10px; font-weight: 600; text-anchor: middle; }}
      .panel-val {{ fill: {CRITICAL}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 20px; font-weight: 700; text-anchor: middle; }}
      .panel-sub {{ fill: {TEXT_MUTED}; font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 8px; text-anchor: middle; }}
    </style>
    <marker id="arrow-atk" markerWidth="10" markerHeight="7" refX="8" refY="3.5" orient="auto">
      <path d="M0,0 L10,3.5 L0,7 Z" fill="{CRITICAL}"/>
    </marker>
    <marker id="arrow-evi" markerWidth="8" markerHeight="5" refX="6" refY="2.5" orient="auto">
      <path d="M0,0 L8,2.5 L0,5 Z" fill="{PRIMARY}" opacity="0.6"/>
    </marker>
  </defs>

  <rect width="600" height="380" fill="{BG}"/>
  <g stroke="{GRID}" stroke-width="0.4" opacity="0.2">
    <line x1="0" y1="0" x2="600" y2="0" /><line x1="0" y1="95" x2="600" y2="95" />
    <line x1="0" y1="190" x2="600" y2="190" /><line x1="0" y1="285" x2="600" y2="285" />
    <line x1="0" y1="380" x2="600" y2="380" />
  </g>

  <!-- Title -->
  <rect x="12" y="10" width="576" height="28" fill="{BORDER}" rx="4" opacity="0.5"/>
  <text class="panel-title" x="300" y="30">ATTACK GRAPH \u2014 EVIDENCE-BACKED PATHS</text>

  <!-- LAYER 1: ASSETS (top row, y=65) -->
  <g>
    <text class="label" x="90" y="30" style="fill: {TEXT_DIM}; font-size: 8px;">ASSETS</text>
    <circle class="node-asset node-critical" cx="90" cy="65" r="11" />
    <text class="label" x="90" y="85">web.app.corp</text>
    <text class="label-sm" x="90" y="97">HTTPS / REST API</text>

    <circle class="node-asset node-critical" cx="210" cy="65" r="11" style="animation-delay: -0.4s;" />
    <text class="label" x="210" y="85">api.internal</text>
    <text class="label-sm" x="210" y="97">GraphQL / REST</text>

    <circle class="node-asset node-normal" cx="330" cy="65" r="10" style="animation-delay: -0.8s;" />
    <text class="label" x="330" y="85">db.cluster</text>
    <text class="label-sm" x="330" y="97">PostgreSQL 15</text>

    <circle class="node-asset node-normal" cx="450" cy="65" r="10" style="animation-delay: -1.2s;" />
    <text class="label" x="450" y="85">ldap.srv</text>
    <text class="label-sm" x="450" y="97">LDAPS / Kerberos</text>

    <circle class="node-asset node-normal" cx="530" cy="65" r="10" style="animation-delay: -1.6s;" />
    <text class="label" x="530" y="85">file.srv</text>
    <text class="label-sm" x="530" y="97">SMB 3.1.1</text>
  </g>

  <!-- LAYER 2: VULNERABILITIES (middle row, y=155) -->
  <g>
    <text class="label" x="90" y="120" style="fill: {TEXT_DIM}; font-size: 8px;">VULNERABILITIES</text>
    <circle class="node-vuln node-critical" cx="90" cy="155" r="14" />
    <circle class="alert" cx="90" cy="155" r="20" style="animation-delay: -0.3s;" />
    <text class="label" x="90" y="135">CVE-2023-48795</text>
    <text class="sev" x="90" y="175">CVSS 9.1 \u2022 EPSS 0.91 \u2022 KEV</text>

    <circle class="node-vuln node-critical" cx="210" cy="155" r="13" style="animation-delay: -0.5s;" />
    <circle class="alert" cx="210" cy="155" r="19" style="animation-delay: -0.7s;" />
    <text class="label" x="210" y="135">CVE-2023-34362</text>
    <text class="sev" x="210" y="175">CVSS 8.8 \u2022 EPSS 0.87 \u2022 KEV</text>

    <circle class="node-vuln node-normal" cx="330" cy="155" r="12" style="animation-delay: -0.9s;" />
    <text class="label" x="330" y="135">CVE-2023-25690</text>
    <text class="sev" x="330" y="175">CVSS 7.5 \u2022 EPSS 0.42</text>

    <circle class="node-vuln node-normal" cx="450" cy="155" r="11" style="animation-delay: -1.3s;" />
    <text class="label" x="450" y="135">CVE-2023-38408</text>
    <text class="sev" x="450" y="175">CVSS 6.8 \u2022 EPSS 0.15</text>
  </g>

  <!-- LAYER 3: EXPLOIT PATHS (bottom row, y=275) -->
  <g>
    <text class="label" x="210" y="240" style="fill: {TEXT_DIM}; font-size: 8px;">EXPLOITATION PATHS</text>
    <circle class="node-exploit node-critical" cx="210" cy="275" r="14" />
    <circle class="alert" cx="210" cy="275" r="21" style="animation-delay: -0.4s;" />
    <text class="label" x="210" y="255">RCE: Deserialization</text>
    <text class="sev" x="210" y="295">EPSS 0.94 \u2022 Remote Code Exec</text>

    <circle class="node-exploit node-normal" cx="350" cy="275" r="12" style="animation-delay: -0.8s;" />
    <text class="label" x="350" y="255">PrivEsc: CVE-2023-2640</text>
    <text class="sev" x="350" y="295">EPSS 0.71 \u2022 Local Root</text>

    <circle class="node-exploit node-normal" cx="470" cy="275" r="11" style="animation-delay: -1.2s;" />
    <text class="label" x="470" y="255">Cred Access: LSASS</text>
    <text class="sev" x="470" y="295">EPSS 0.58 \u2022 Mimikatz</text>
  </g>

  <!-- EDGES: Asset -> Vuln (vertical, clean) -->
  <g>
    <path class="edge" d="M 90 76 L 90 141" marker-end="url(#arrow-atk)" />
    <path class="edge" d="M 210 76 L 210 141" marker-end="url(#arrow-atk)" />
    <path class="edge" d="M 330 75 L 330 141" marker-end="url(#arrow-atk)" />
    <path class="edge" d="M 450 75 L 450 141" marker-end="url(#arrow-atk)" />
  </g>

  <!-- EDGES: Vuln -> Exploit (diagonal, critical path highlighted) -->
  <g>
    <!-- Critical path: web.app -> CVE-2023-48795 -> RCE -->
    <path class="path-crit" d="M 90 169 L 150 261" marker-end="url(#arrow-atk)" />
    <path class="path-crit" d="M 210 169 L 210 261" marker-end="url(#arrow-atk)" />
    <path class="edge" d="M 270 155 L 330 261" marker-end="url(#arrow-atk)" />
    <path class="edge" d="M 450 166 L 470 261" marker-end="url(#arrow-atk)" />

    <!-- Lateral movement (evidence-backed, green) -->
    <path class="edge-evi" d="M 210 289 L 350 261" marker-end="url(#arrow-evi)" />
    <path class="edge-evi" d="M 90 169 L 90 261" marker-end="url(#arrow-evi)" />
  </g>

  <!-- CRITICAL PATH HIGHLIGHT (thick line through full chain) -->
  <path class="path-crit" d="M 90 76 L 90 141 L 150 261 L 210 289 L 350 261" 
        fill="none" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity="0.3" />

  <!-- LEGEND PANEL (top-right) -->
  <g transform="translate(410, 10)">
    <rect width="180" height="100" fill="{BORDER}" rx="6" opacity="0.7"/>
    <circle class="node-asset" cx="20" cy="20" r="6" />
    <text class="label" x="100" y="24" style="font-size: 9px;">Asset</text>
    <circle class="node-vuln" cx="20" cy="45" r="6" />
    <text class="label" x="100" y="49" style="font-size: 9px;">Vulnerability</text>
    <circle class="node-exploit" cx="20" cy="70" r="6" />
    <text class="label" x="100" y="74" style="font-size: 9px;">Exploit Path</text>
    <line x1="15" y1="86" x2="165" y2="86" stroke="{GRID}" />
    <path class="path-crit" d="M 15 86 L 165 86" stroke-width="2" />
    <text class="sev" x="90" y="82" style="font-size: 8px;">CRITICAL PATH</text>
  </g>

  <!-- RISK SCORE PANEL (bottom-right) -->
  <g transform="translate(380, 260)">
    <rect width="200" height="110" fill="{BORDER}" rx="8" opacity="0.8"/>
    <text class="panel-title" x="100" y="28">ATTACK PATH RISK</text>
    <text class="panel-val" x="100" y="60">9.4</text>
    <text class="panel-sub" x="100" y="78">CRITICAL</text>
    <text class="panel-sub" x="100" y="90">3 hops \u2022 Evidence-backed</text>
    <text class="panel-sub" x="100" y="100">Lateral: 2 paths</text>
  </g>

  <!-- MITRE ATT&CK TAGS (bottom-left) -->
  <g transform="translate(12, 300)">
    <rect width="350" height="70" fill="{BORDER}" rx="6" opacity="0.6"/>
    <text class="panel-title" x="175" y="18" style="font-size: 9px;">MITRE ATT\u0026CK TECHNIQUES</text>
    <g style="font-family: 'JetBrains Mono', monospace; font-size: 8px;">
      <text x="20" y="38" fill="{TEXT_MUTED}">T1190</text><text x="65" y="38" fill="{PRIMARY}">Exploit Public-Facing App</text>
      <text x="20" y="52" fill="{TEXT_MUTED}">T1068</text><text x="65" y="52" fill="{PRIMARY}">Exploitation for PrivEsc</text>
      <text x="20" y="66" fill="{TEXT_MUTED}">T1003</text><text x="65" y="66" fill="{PRIMARY}">OS Credential Dumping</text>
      <text x="220" y="38" fill="{TEXT_MUTED}">T1021</text><text x="280" y="38" fill="{PRIMARY}">Remote Services</text>
      <text x="220" y="52" fill="{TEXT_MUTED}">T1505</text><text x="280" y="52" fill="{PRIMARY}">Server Software Component</text>
      <text x="220" y="66" fill="{TEXT_MUTED}">T1567</text><text x="280" y="66" fill="{PRIMARY}">Exfiltration Over Web</text>
    </g>
  </g>
</svg>'''

# Write all files
files = {
    "network-scan.svg": network_scan,
    "data-flow.svg": data_flow,
    "neural-reasoning.svg": neural_net,
    "attack-graph.svg": attack_graph,
}

for name, content in files.items():
    path = os.path.join(out_dir, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {name} ({len(content)} bytes)")

print("\nAll animations v2 created successfully!")

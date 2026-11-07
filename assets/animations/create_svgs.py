import os

out_dir = "C:/Users/nanda/OneDrive/Desktop/RAVEN/assets/animations"
os.makedirs(out_dir, exist_ok=True)

# 1. Network Scan Animation
network_scan = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200" width="400" height="200">
  <defs>
    <style>
      @keyframes pulse { 0%,100% { opacity: 0.3; r: 4; } 50% { opacity: 1; r: 8; } }
      @keyframes sweep { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
      @keyframes packet { 0% { offset-distance: 0%; opacity: 1; } 100% { offset-distance: 100%; opacity: 0; } }
      @keyframes scanline { 0% { y1: 0; y2: 0; opacity: 0.8; } 100% { y1: 200; y2: 200; opacity: 0; } }
      .node { fill: #00ff88; filter: drop-shadow(0 0 4px #00ff88); }
      .node-active { animation: pulse 1.5s ease-in-out infinite; }
      .scan-ring { stroke: #00ff88; stroke-width: 1.5; fill: none; opacity: 0.6; animation: sweep 4s linear infinite; transform-origin: 200px 100px; }
      .packet { fill: #00ff88; filter: drop-shadow(0 0 6px #00ff88); offset-path: path('M 100 100 Q 200 50 300 100'); animation: packet 3s ease-in-out infinite; }
      .scan-line { stroke: #00ff88; stroke-width: 2; opacity: 0.9; animation: scanline 2s ease-out infinite; }
      .connection { stroke: #00ff88; stroke-width: 0.8; opacity: 0.3; stroke-dasharray: 4 4; }
    </style>
  </defs>
  <g stroke="#003311" stroke-width="0.5">
    <line x1="0" y1="0" x2="400" y2="0" /><line x1="0" y1="50" x2="400" y2="50" /><line x1="0" y1="100" x2="400" y2="100" /><line x1="0" y1="150" x2="400" y2="150" /><line x1="0" y1="200" x2="400" y2="200" />
    <line x1="0" y1="0" x2="0" y2="200" /><line x1="50" y1="0" x2="50" y2="200" /><line x1="100" y1="0" x2="100" y2="200" /><line x1="150" y1="0" x2="150" y2="200" /><line x1="200" y1="0" x2="200" y2="200" />
    <line x1="250" y1="0" x2="250" y2="200" /><line x1="300" y1="0" x2="300" y2="200" /><line x1="350" y1="0" x2="350" y2="200" /><line x1="400" y1="0" x2="400" y2="200" />
  </g>
  <circle class="scan-ring" cx="200" cy="100" r="30" />
  <circle class="scan-ring" cx="200" cy="100" r="60" style="animation-delay: -1s;" />
  <circle class="scan-ring" cx="200" cy="100" r="90" style="animation-delay: -2s;" />
  <line class="scan-line" x1="200" y1="0" x2="200" y2="0" />
  <g class="nodes">
    <circle class="node node-active" cx="200" cy="100" r="6" />
    <circle cx="200" cy="100" r="14" stroke="#00ff88" stroke-width="1" fill="none" opacity="0.5" />
    <circle cx="200" cy="100" r="22" stroke="#00ff88" stroke-width="0.5" fill="none" opacity="0.3" />
    <g><line class="connection" x1="200" y1="100" x2="80" y2="30" /><circle class="node node-active" cx="80" cy="30" r="4" style="animation-delay: 0.2s;" /><text x="80" y="20" fill="#00ff88" font-size="8" text-anchor="middle" font-family="monospace">10.0.1.5</text></g>
    <g><line class="connection" x1="200" y1="100" x2="320" y2="30" /><circle class="node node-active" cx="320" cy="30" r="4" style="animation-delay: 0.4s;" /><text x="320" y="20" fill="#00ff88" font-size="8" text-anchor="middle" font-family="monospace">192.168.1.10</text></g>
    <g><line class="connection" x1="200" y1="100" x2="60" y2="170" /><circle class="node node-active" cx="60" cy="170" r="4" style="animation-delay: 0.6s;" /><text x="60" y="185" fill="#00ff88" font-size="8" text-anchor="middle" font-family="monospace">172.16.0.3</text></g>
    <g><line class="connection" x1="200" y1="100" x2="340" y2="170" /><circle class="node node-active" cx="340" cy="170" r="4" style="animation-delay: 0.8s;" /><text x="340" y="185" fill="#00ff88" font-size="8" text-anchor="middle" font-family="monospace">10.10.0.7</text></g>
    <g><line class="connection" x1="200" y1="100" x2="120" y2="50" /><circle class="node node-active" cx="120" cy="50" r="3.5" style="animation-delay: 1s;" /></g>
    <g><line class="connection" x1="200" y1="100" x2="280" y2="50" /><circle class="node node-active" cx="280" cy="50" r="3.5" style="animation-delay: 1.2s;" /></g>
    <g><line class="connection" x1="200" y1="100" x2="120" y2="150" /><circle class="node node-active" cx="120" cy="150" r="3.5" style="animation-delay: 1.4s;" /></g>
    <g><line class="connection" x1="200" y1="100" x2="280" y2="150" /><circle class="node node-active" cx="280" cy="150" r="3.5" style="animation-delay: 1.6s;" /></g>
  </g>
  <circle class="packet" r="3" />
  <circle class="packet" r="2.5" style="animation-delay: -1s; offset-path: path('M 80 30 Q 140 65 200 100');" />
  <circle class="packet" r="2.5" style="animation-delay: -2s; offset-path: path('M 320 30 Q 260 65 200 100');" />
  <text x="200" y="195" fill="#00ff88" font-size="11" text-anchor="middle" font-family="monospace" opacity="0.8">NETWORK SCAN ACTIVE \u2022 8 HOSTS DISCOVERED \u2022 3 PORTS OPEN</text>
</svg>"""

# 2. Data Flow Pipeline Animation
data_flow = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 180" width="600" height="180">
  <defs>
    <style>
      @keyframes flow { 0% { offset-distance: 0%; opacity: 1; } 100% { offset-distance: 100%; opacity: 0.3; } }
      @keyframes process { 0%,100% { opacity: 0.6; transform: scale(1); } 50% { opacity: 1; transform: scale(1.05); } }
      @keyframes data-pulse { 0%,100% { stroke-width: 2; opacity: 0.5; } 50% { stroke-width: 4; opacity: 1; } }
      .stage { fill: #0d1117; stroke: #00ff88; stroke-width: 1.5; rx: 8; }
      .stage.active { animation: process 2s ease-in-out infinite; }
      .arrow { stroke: #00ff88; stroke-width: 2; fill: none; marker-end: url(#arrowhead); animation: data-pulse 1.5s ease-in-out infinite; }
      .packet { fill: #00ff88; filter: drop-shadow(0 0 4px #00ff88); animation: flow 4s linear infinite; }
      .label { fill: #00ff88; font-family: monospace; font-size: 10px; text-anchor: middle; }
      .metric { fill: #88ffaa; font-family: monospace; font-size: 9px; text-anchor: middle; opacity: 0.8; }
    </style>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#00ff88" />
    </marker>
    <linearGradient id="pipeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00ff88" stop-opacity="0.3"/>
      <stop offset="50%" stop-color="#00ff88" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#00ff88" stop-opacity="0.3"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="600" height="180" fill="#050a05" />
  <g stroke="#002200" stroke-width="0.5" opacity="0.3">
    <line x1="0" y1="0" x2="600" y2="0" /><line x1="0" y1="60" x2="600" y2="60" /><line x1="0" y1="120" x2="600" y2="120" /><line x1="0" y1="180" x2="600" y2="180" />
  </g>

  <!-- Pipeline Stages -->
  <g>
    <!-- Stage 1: INGEST -->
    <rect class="stage active" x="20" y="40" width="100" height="100" style="animation-delay: 0s;" />
    <text class="label" x="70" y="65">INGEST</text>
    <text class="label" x="70" y="80">Nmap/ZAP</text>
    <text class="metric" x="70" y="105">2.4k req/s</text>
    <circle class="packet" r="4" offset-path="path('M 70 90 L 70 130')" />

    <!-- Arrow 1 -->
    <path class="arrow" d="M 120 90 L 150 90" />

    <!-- Stage 2: PARSE -->
    <rect class="stage active" x="160" y="40" width="100" height="100" style="animation-delay: -0.4s;" />
    <text class="label" x="210" y="65">PARSE</text>
    <text class="label" x="210" y="80">Normalize</text>
    <text class="metric" x="210" y="105">1.8k obj/s</text>
    <circle class="packet" r="4" style="animation-delay: -0.5s;" offset-path="path('M 210 90 L 210 130')" />

    <!-- Arrow 2 -->
    <path class="arrow" d="M 260 90 L 290 90" />

    <!-- Stage 3: CORRELATE -->
    <rect class="stage active" x="300" y="40" width="120" height="100" style="animation-delay: -0.8s;" />
    <text class="label" x="360" y="65">CORRELATE</text>
    <text class="label" x="360" y="80">CVE/KEV/EPSS</text>
    <text class="metric" x="360" y="105">94% match</text>
    <circle class="packet" r="4" style="animation-delay: -1s;" offset-path="path('M 360 90 L 360 130')" />

    <!-- Arrow 3 -->
    <path class="arrow" d="M 420 90 L 450 90" />

    <!-- Stage 4: SCORE -->
    <rect class="stage active" x="460" y="40" width="120" height="100" style="animation-delay: -1.2s;" />
    <text class="label" x="520" y="65">RISK SCORE</text>
    <text class="label" x="520" y="80">CVSS+EPSS+KEV</text>
    <text class="metric" x="520" y="105">8.7/10</text>
    <circle class="packet" r="4" style="animation-delay: -1.5s;" offset-path="path('M 520 90 L 520 130')" />
  </g>

  <!-- Data packets flowing through pipes -->
  <g>
    <circle class="packet" r="3" style="animation-delay: 0s;" offset-path="path('M 120 90 L 460 90')" />
    <circle class="packet" r="3" style="animation-delay: -1s;" offset-path="path('M 120 90 L 460 90')" />
    <circle class="packet" r="3" style="animation-delay: -2s;" offset-path="path('M 120 90 L 460 90')" />
    <circle class="packet" r="3" style="animation-delay: -3s;" offset-path="path('M 120 90 L 460 90')" />
  </g>

  <!-- Bottom metrics bar -->
  <rect x="20" y="150" width="560" height="20" fill="#001100" stroke="#00ff88" stroke-width="1" rx="4" opacity="0.5" />
  <text x="300" y="165" fill="#00ff88" font-family="monospace" font-size="11" text-anchor="middle">THROUGHPUT: 2,447 events/sec \u2022 LATENCY: 12ms p99 \u2022 ERROR RATE: 0.02%</text>
</svg>"""

# 3. Neural Network / LLM Reasoning Animation
neural_net = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300" width="500" height="300">
  <defs>
    <style>
      @keyframes neuron-fire { 0%,100% { opacity: 0.3; r: 8; } 50% { opacity: 1; r: 14; filter: drop-shadow(0 0 12px #00ff88); } }
      @keyframes synapse { 0% { stroke-opacity: 0; stroke-width: 0.5; } 50% { stroke-opacity: 1; stroke-width: 2.5; } 100% { stroke-opacity: 0; stroke-width: 0.5; } }
      @keyframes thought-bubble { 0% { opacity: 0; transform: scale(0.5); } 20% { opacity: 1; transform: scale(1); } 80% { opacity: 1; transform: scale(1); } 100% { opacity: 0; transform: scale(1.2); } }
      .neuron { fill: #00ff88; filter: drop-shadow(0 0 4px #00ff88); }
      .neuron-input { animation: neuron-fire 3s ease-in-out infinite; }
      .neuron-hidden { animation: neuron-fire 3s ease-in-out infinite; animation-delay: -0.5s; }
      .neuron-output { animation: neuron-fire 3s ease-in-out infinite; animation-delay: -1s; }
      .synapse { stroke: #00ff88; stroke-width: 0.8; opacity: 0.2; animation: synapse 2s ease-in-out infinite; }
      .bubble { fill: #0d1117; stroke: #00ff88; stroke-width: 1.5; rx: 12; opacity: 0; animation: thought-bubble 4s ease-in-out infinite; }
      .bubble-text { fill: #00ff88; font-family: monospace; font-size: 10px; text-anchor: middle; }
    </style>
    <linearGradient id="neuronGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#00ff88" />
      <stop offset="100%" stop-color="#004422" />
    </linearGradient>
  </defs>

  <rect width="500" height="300" fill="#030803" />

  <!-- Input Layer (4 neurons) -->
  <g id="input-layer">
    <circle class="neuron neuron-input" cx="60" cy="60" r="10" />
    <circle class="neuron neuron-input" cx="60" cy="120" r="10" style="animation-delay: -0.3s;" />
    <circle class="neuron neuron-input" cx="60" cy="180" r="10" style="animation-delay: -0.6s;" />
    <circle class="neuron neuron-input" cx="60" cy="240" r="10" style="animation-delay: -0.9s;" />
    <text x="60" y="30" fill="#00ff88" font-family="monospace" font-size="11" text-anchor="middle" opacity="0.7">INPUT LAYER</text>
    <text x="60" y="275" fill="#88ffaa" font-family="monospace" font-size="9" text-anchor="middle" opacity="0.5">Asset Data | Vuln Intel | Policy | Context</text>
  </g>

  <!-- Hidden Layers (3 layers) -->
  <g id="hidden-layers">
    <!-- Layer 1: 6 neurons -->
    <g>
      <circle class="neuron neuron-hidden" cx="180" cy="50" r="8" />
      <circle class="neuron neuron-hidden" cx="180" cy="100" r="8" style="animation-delay: -0.2s;" />
      <circle class="neuron neuron-hidden" cx="180" cy="150" r="8" style="animation-delay: -0.4s;" />
      <circle class="neuron neuron-hidden" cx="180" cy="200" r="8" style="animation-delay: -0.6s;" />
      <circle class="neuron neuron-hidden" cx="180" cy="250" r="8" style="animation-delay: -0.8s;" />
      <circle class="neuron neuron-hidden" cx="180" cy="300" r="8" style="animation-delay: -1s;" />
    </g>
    <!-- Layer 2: 8 neurons -->
    <g>
      <circle class="neuron neuron-hidden" cx="300" cy="40" r="7" style="animation-delay: -0.1s;" />
      <circle class="neuron neuron-hidden" cx="300" cy="80" r="7" style="animation-delay: -0.3s;" />
      <circle class="neuron neuron-hidden" cx="300" cy="120" r="7" style="animation-delay: -0.5s;" />
      <circle class="neuron neuron-hidden" cx="300" cy="160" r="7" style="animation-delay: -0.7s;" />
      <circle class="neuron neuron-hidden" cx="300" cy="200" r="7" style="animation-delay: -0.9s;" />
      <circle class="neuron neuron-hidden" cx="300" cy="240" r="7" style="animation-delay: -1.1s;" />
      <circle class="neuron neuron-hidden" cx="300" cy="280" r="7" style="animation-delay: -1.3s;" />
      <circle class="neuron neuron-hidden" cx="300" cy="320" r="7" style="animation-delay: -1.5s;" />
    </g>
    <!-- Layer 3: 5 neurons -->
    <g>
      <circle class="neuron neuron-hidden" cx="420" cy="70" r="8" style="animation-delay: -0.2s;" />
      <circle class="neuron neuron-hidden" cx="420" cy="130" r="8" style="animation-delay: -0.5s;" />
      <circle class="neuron neuron-hidden" cx="420" cy="190" r="8" style="animation-delay: -0.8s;" />
      <circle class="neuron neuron-hidden" cx="420" cy="250" r="8" style="animation-delay: -1.1s;" />
      <circle class="neuron neuron-hidden" cx="420" cy="310" r="8" style="animation-delay: -1.4s;" />
    </g>
    <text x="300" y="25" fill="#00ff88" font-family="monospace" font-size="11" text-anchor="middle" opacity="0.7">HIDDEN LAYERS (19 neurons)</text>
  </g>

  <!-- Output Layer (3 neurons) -->
  <g id="output-layer">
    <circle class="neuron neuron-output" cx="480" cy="80" r="10" />
    <circle class="neuron neuron-output" cx="480" cy="160" r="10" style="animation-delay: -0.4s;" />
    <circle class="neuron neuron-output" cx="480" cy="240" r="10" style="animation-delay: -0.8s;" />
    <text x="480" y="30" fill="#00ff88" font-family="monospace" font-size="11" text-anchor="middle" opacity="0.7">OUTPUT</text>
    <text x="480" cy="285" fill="#88ffaa" font-family="monospace" font-size="9" text-anchor="middle" opacity="0.5">Action | Target | Risk</text>
  </g>

  <!-- Synapses (connections) -->
  <g class="synapses" stroke="#00ff88" stroke-width="0.5" opacity="0.15">
    <!-- Input to Hidden1 -->
    <line x1="70" y1="60" x2="172" y2="50" class="synapse" style="animation-delay: 0s;" />
    <line x1="70" y1="60" x2="172" y2="100" class="synapse" style="animation-delay: -0.1s;" />
    <line x1="70" y1="60" x2="172" y2="150" class="synapse" style="animation-delay: -0.2s;" />
    <line x1="70" y1="60" x2="172" y2="200" class="synapse" style="animation-delay: -0.3s;" />
    <line x1="70" y1="60" x2="172" y2="250" class="synapse" style="animation-delay: -0.4s;" />
    <line x1="70" y1="60" x2="172" y2="300" class="synapse" style="animation-delay: -0.5s;" />
    <line x1="70" y1="120" x2="172" y2="50" class="synapse" style="animation-delay: -0.05s;" />
    <line x1="70" y1="120" x2="172" y2="100" class="synapse" style="animation-delay: -0.15s;" />
    <line x1="70" y1="120" x2="172" y2="150" class="synapse" style="animation-delay: -0.25s;" />
    <line x1="70" y1="120" x2="172" y2="200" class="synapse" style="animation-delay: -0.35s;" />
    <line x1="70" y1="120" x2="172" y2="250" class="synapse" style="animation-delay: -0.45s;" />
    <line x1="70" y1="120" x2="172" y2="300" class="synapse" style="animation-delay: -0.55s;" />
    <line x1="70" y1="180" x2="172" y2="50" class="synapse" style="animation-delay: -0.1s;" />
    <line x1="70" y1="180" x2="172" y2="100" class="synapse" style="animation-delay: -0.2s;" />
    <line x1="70" y1="180" x2="172" y2="150" class="synapse" style="animation-delay: -0.3s;" />
    <line x1="70" y1="180" x2="172" y2="200" class="synapse" style="animation-delay: -0.4s;" />
    <line x1="70" y1="180" x2="172" y2="250" class="synapse" style="animation-delay: -0.5s;" />
    <line x1="70" y1="180" x2="172" y2="300" class="synapse" style="animation-delay: -0.6s;" />
    <line x1="70" y1="240" x2="172" y2="50" class="synapse" style="animation-delay: -0.15s;" />
    <line x1="70" y1="240" x2="172" y2="100" class="synapse" style="animation-delay: -0.25s;" />
    <line x1="70" y1="240" x2="172" y2="150" class="synapse" style="animation-delay: -0.35s;" />
    <line x1="70" y1="240" x2="172" y2="200" class="synapse" style="animation-delay: -0.45s;" />
    <line x1="70" y1="240" x2="172" y2="250" class="synapse" style="animation-delay: -0.55s;" />
    <line x1="70" y1="240" x2="172" y2="300" class="synapse" style="animation-delay: -0.65s;" />
    <!-- Hidden1 to Hidden2 (sample) -->
    <line x1="188" y1="50" x2="292" y2="40" class="synapse" style="animation-delay: -0.2s;" />
    <line x1="188" y1="100" x2="292" y2="80" class="synapse" style="animation-delay: -0.3s;" />
    <line x1="188" y1="150" x2="292" y2="120" class="synapse" style="animation-delay: -0.4s;" />
    <line x1="188" y1="200" x2="292" y2="160" class="synapse" style="animation-delay: -0.5s;" />
    <line x1="188" y1="250" x2="292" y2="200" class="synapse" style="animation-delay: -0.6s;" />
    <line x1="188" y1="300" x2="292" y2="240" class="synapse" style="animation-delay: -0.7s;" />
    <!-- Hidden2 to Hidden3 (sample) -->
    <line x1="308" y1="40" x2="412" y2="70" class="synapse" style="animation-delay: -0.3s;" />
    <line x1="308" y1="80" x2="412" y2="130" class="synapse" style="animation-delay: -0.4s;" />
    <line x1="308" y1="120" x2="412" y2="190" class="synapse" style="animation-delay: -0.5s;" />
    <line x1="308" y1="160" x2="412" y2="250" class="synapse" style="animation-delay: -0.6s;" />
    <line x1="308" y1="200" x2="412" y2="310" class="synapse" style="animation-delay: -0.7s;" />
    <!-- Hidden3 to Output -->
    <line x1="428" y1="70" x2="472" y2="80" class="synapse" style="animation-delay: -0.4s;" />
    <line x1="428" y1="130" x2="472" y2="160" class="synapse" style="animation-delay: -0.5s;" />
    <line x1="428" y1="190" x2="472" y2="240" class="synapse" style="animation-delay: -0.6s;" />
  </g>

  <!-- Thought bubbles showing reasoning -->
  <g>
    <rect class="bubble" x="200" y="10" width="220" height="50" style="animation-delay: 0s;" />
    <text class="bubble-text" x="310" y="35">ANALYZING: Port 443 \u2192 TLS 1.3 \u2192 Cert Valid</text>
    <text class="bubble-text" x="310" y="50">CONFIDENCE: 94%</text>

    <rect class="bubble" x="200" y="120" width="220" height="50" style="animation-delay: -1.3s;" />
    <text class="bubble-text" x="310" y="145">CORRELATING: CVE-2023-XXXX \u2192 Service Match</text>
    <text class="bubble-text" x="310" y="160">EPSS: 0.87 | KEV: YES</text>

    <rect class="bubble" x="200" y="230" width="220" height="50" style="animation-delay: -2.6s;" />
    <text class="bubble-text" x="310" y="255">PROPOSING: ZAP Active Scan \u2192 L2 Controlled</text>
    <text class="bubble-text" x="310" y="270">RISK SCORE: 8.2/10</text>
  </g>

  <!-- Status bar -->
  <rect x="10" y="10" width="180" height="120" fill="#001100" stroke="#00ff88" stroke-width="1" rx="6" opacity="0.6" />
  <text x="20" y="30" fill="#00ff88" font-family="monospace" font-size="10">MODEL: llama3.1:8b</text>
  <text x="20" y="50" fill="#00ff88" font-family="monospace" font-size="10">CTX: 4096 tokens</text>
  <text x="20" y="70" fill="#00ff88" font-family="monospace" font-size="10">TEMP: 0.1</text>
  <text x="20" y="90" fill="#00ff88" font-family="monospace" font-size="10">INFERENCE: 234ms</text>
  <text x="20" y="110" fill="#00ff88" font-family="monospace" font-size="10">PROPOSALS: 3/queue</text>
  <text x="20" y="130" fill="#00ff88" font-family="monospace" font-size="10">POLICY: L2_ACTIVE</text>
</svg>"""

# 4. Attack Graph / Threat Map Animation
attack_graph = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300" width="500" height="300">
  <defs>
    <style>
      @keyframes node-pulse { 0%,100% { opacity: 0.5; r: 6; } 50% { opacity: 1; r: 10; filter: drop-shadow(0 0 8px #ff4444); } }
      @keyframes edge-flow { 0% { stroke-dashoffset: 20; opacity: 0.3; } 100% { stroke-dashoffset: 0; opacity: 1; } }
      @keyframes path-highlight { 0%,100% { stroke-width: 1.5; opacity: 0.4; } 50% { stroke-width: 3; opacity: 1; filter: drop-shadow(0 0 6px #ff4444); } }
      @keyframes alert-pulse { 0%,100% { opacity: 0.6; } 50% { opacity: 1; transform: scale(1.1); } }
      .node-asset { fill: #00ff88; }
      .node-vuln { fill: #ff4444; }
      .node-exploit { fill: #ffaa00; }
      .node-critical { animation: node-pulse 2s ease-in-out infinite; }
      .edge { stroke: #ff4444; stroke-width: 1.5; fill: none; stroke-dasharray: 8 4; animation: edge-flow 1.5s linear infinite; }
      .edge-evidence { stroke: #00ff88; stroke-width: 1; fill: none; opacity: 0.5; stroke-dasharray: 4 4; }
      .path-critical { stroke: #ff4444; stroke-width: 2.5; fill: none; animation: path-highlight 2s ease-in-out infinite; }
      .alert { fill: #ff4444; filter: drop-shadow(0 0 6px #ff4444); animation: alert-pulse 1s ease-in-out infinite; }
      .label { fill: #cccccc; font-family: monospace; font-size: 9px; text-anchor: middle; }
      .severity { fill: #ff4444; font-family: monospace; font-size: 8px; text-anchor: middle; }
    </style>
    <marker id="arrow" markerWidth="8" markerHeight="5" refX="7" refY="2.5" orient="auto">
      <path d="M0,0 L8,2.5 L0,5 Z" fill="#ff4444" />
    </marker>
  </defs>

  <rect width="500" height="300" fill="#0a0505" />
  <g stroke="#220000" stroke-width="0.5" opacity="0.2">
    <line x1="0" y1="0" x2="500" y2="0" /><line x1="0" y1="75" x2="500" y2="75" /><line x1="0" y1="150" x2="500" y2="150" /><line x1="0" y1="225" x2="500" y2="225" /><line x1="0" y1="300" x2="500" y2="300" />
  </g>

  <!-- Assets (green nodes) -->
  <g>
    <circle class="node-asset node-critical" cx="80" cy="60" r="10" />
    <text class="label" x="80" y="30">web.app.corp</text>
    <text class="severity" x="80" y="80">HTTP/HTTPS</text>

    <circle class="node-asset node-critical" cx="200" cy="60" r="10" style="animation-delay: -0.5s;" />
    <text class="label" x="200" y="30">api.internal</text>
    <text class="severity" x="200" y="80">REST API</text>

    <circle class="node-asset" cx="350" cy="60" r="9" style="animation-delay: -1s;" />
    <text class="label" x="350" y="30">db.cluster</text>
    <text class="severity" x="350" y="80">PostgreSQL</text>

    <circle class="node-asset" cx="420" cy="140" r="9" style="animation-delay: -1.5s;" />
    <text class="label" x="420" y="110">ldap.srv</text>
    <text class="severity" x="420" y="160">LDAP</text>

    <circle class="node-asset" cx="80" cy="220" r="9" style="animation-delay: -2s;" />
    <text class="label" x="80" y="190">file.srv</text>
    <text class="severity" x="80" y="240">SMB/NFS</text>
  </g>

  <!-- Vulnerabilities (red nodes) -->
  <g>
    <circle class="node-vuln node-critical" cx="80" cy="140" r="12" />
    <text class="label" x="80" y="115">CVE-2023-XXXX</text>
    <text class="severity" x="80" y="165">CVSS 9.8</text>
    <circle class="alert" cx="80" cy="140" r="16" style="animation-delay: -0.2s;" />

    <circle class="node-vuln node-critical" cx="200" cy="140" r="11" style="animation-delay: -0.3s;" />
    <text class="label" x="200" y="115">CVE-2023-YYYY</text>
    <text class="severity" x="200" y="165">CVSS 8.2</text>
    <circle class="alert" cx="200" cy="140" r="15" style="animation-delay: -0.5s;" />

    <circle class="node-vuln" cx="350" cy="140" r="10" style="animation-delay: -0.6s;" />
    <text class="label" x="350" y="115">CVE-2023-ZZZZ</text>
    <text class="severity" x="350" y="165">CVSS 7.1</text>
  </g>

  <!-- Exploit Paths (yellow nodes) -->
  <g>
    <circle class="node-exploit node-critical" cx="200" cy="230" r="12" />
    <text class="label" x="200" y="205">RCE via Deserialization</text>
    <text class="severity" x="200" y="255">EPSS 0.94</text>
    <circle class="alert" cx="200" cy="230" r="17" style="animation-delay: -0.4s;" />

    <circle class="node-exploit" cx="350" cy="230" r="10" style="animation-delay: -0.8s;" />
    <text class="label" x="350" y="205">PrivEsc: CVE-2023-AAAA</text>
    <text class="severity" x="350" y="255">EPSS 0.67</text>
  </g>

  <!-- Edges: Asset -> Vuln -->
  <g class="edges">
    <path class="edge" d="M 80 70 L 80 128" marker-end="url(#arrow)" />
    <path class="edge" d="M 200 70 L 200 128" marker-end="url(#arrow)" />
    <path class="edge" d="M 350 69 L 350 128" marker-end="url(#arrow)" />

    <!-- Edges: Vuln -> Exploit -->
    <path class="path-critical" d="M 80 152 L 140 218" marker-end="url(#arrow)" />
    <path class="path-critical" d="M 200 152 L 200 218" marker-end="url(#arrow)" />
    <path class="edge" d="M 260 140 L 340 218" marker-end="url(#arrow)" />
    <path class="edge" d="M 350 150 L 350 220" marker-end="url(#arrow)" />

    <!-- Lateral movement edges (evidence-backed) -->
    <path class="edge-evidence" d="M 200 242 L 350 220" marker-end="url(#arrow)" />
    <path class="edge-evidence" d="M 80 152 L 80 210" marker-end="url(#arrow)" />
  </g>

  <!-- Critical Path Highlight -->
  <g>
    <path class="path-critical" d="M 80 70 L 80 128 L 140 218 L 200 242 L 350 220" fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
  </g>

  <!-- Legend -->
  <g transform="translate(10, 10)">
    <rect width="180" height="100" fill="#001100" stroke="#ff4444" stroke-width="1" rx="6" opacity="0.8" />
    <circle class="node-asset" cx="25" cy="25" r="6" />
    <text class="label" x="80" y="29">Asset</text>
    <circle class="node-vuln" cx="25" cy="50" r="6" />
    <text class="label" x="80" y="54">Vulnerability</text>
    <circle class="node-exploit" cx="25" cy="75" r="6" />
    <text class="label" x="80" y="79">Exploit Path</text>
    <line x1="20" y1="95" x2="160" y2="95" stroke="#330000" />
    <path class="path-critical" d="M 20 95 L 160 95" stroke-width="2" />
    <text class="severity" x="90" y="92">CRITICAL PATH</text>
  </g>

  <!-- Risk Score -->
  <g transform="translate(310, 10)">
    <rect width="180" height="80" fill="#001100" stroke="#ffaa00" stroke-width="1" rx="6" opacity="0.8" />
    <text x="90" y="30" fill="#ffaa00" font-family="monospace" font-size="14" text-anchor="middle">ATTACK PATH RISK</text>
    <text x="90" y="55" fill="#ff4444" font-family="monospace" font-size="28" text-anchor="middle" font-weight="bold">9.4</text>
    <text x="90" y="75" fill="#88ffaa" font-family="monospace" font-size="10" text-anchor="middle">CRITICAL \u2022 3 hops \u2022 Evidence-backed</text>
  </g>
</svg>"""

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

print("\nAll animations created successfully!")

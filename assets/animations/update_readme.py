with open("C:/Users/nanda/OneDrive/Desktop/RAVEN/README.md", "r", encoding="utf-8") as f:
    readme = f.read()

animations_section = "\n\n---\n\n## Live Platform Animations\n\n<p align=\"center\">\n  <img src=\"assets/animations/network-scan.svg\" alt=\"Network Scan Animation\" width=\"600\"><br>\n  <em>Network Reconnaissance \u2014 Real-time host discovery, port scanning, and service enumeration with scan rings and data packets</em>\n</p>\n\n<p align=\"center\">\n  <img src=\"assets/animations/data-flow.svg\" alt=\"Data Flow Pipeline\" width=\"700\"><br>\n  <em>Vulnerability Intelligence Pipeline \u2014 Ingest \u2192 Parse \u2192 Correlate \u2192 Risk Score with live throughput metrics</em>\n</p>\n\n<p align=\"center\">\n  <img src=\"assets/animations/neural-reasoning.svg\" alt=\"Neural Reasoning\" width=\"600\"><br>\n  <em>Reasoning Engine \u2014 Multi-layer neural inference with synapse firing, thought bubbles showing structured proposals</em>\n</p>\n\n<p align=\"center\">\n  <img src=\"assets/animations/attack-graph.svg\" alt=\"Attack Graph\" width=\"600\"><br>\n  <em>Attack Graph \u2014 Evidence-backed attack paths, critical path highlighting, lateral movement visualization</em>\n</p>\n\n"

# Insert after the second --- (after Quick Overview, before Architecture)
parts = readme.split("---", 3)
if len(parts) >= 4:
    new_readme = parts[0] + "---" + parts[1] + "---" + parts[2] + animations_section + "---" + parts[3]
    with open("C:/Users/nanda/OneDrive/Desktop/RAVEN/README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)
    print("Animations section added to README.md")
else:
    print("Could not find insertion point, parts:", len(parts))

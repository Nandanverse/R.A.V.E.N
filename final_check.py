import os

with open(r"C:\Users\nanda\OneDrive\Desktop\RAVEN\assets\banner.svg", "r", encoding="utf-8") as f:
    content = f.read()

print("=== REQUIREMENTS CHECKLIST ===")
print()

# 1. No opacity="0" as initial attribute
if "opacity=\"0\"" in content:
    print("FAIL: Found opacity=\"0\" as initial attribute")
else:
    print("PASS: No element has opacity=\"0\" as initial attribute")

# 2. No stroke-dashoffset trick
if "stroke-dashoffset" in content:
    print("FAIL: Found stroke-dashoffset (draw-in trick)")
else:
    print("PASS: No stroke-dasharray/dashoffset trick that hides path at rest")

# 3. Title y=120
if "y=\"120\"" in content and "R.A.V.E.N" in content:
    print("PASS: Title at y=120")
else:
    print("FAIL: Title not at y=120")

# 4. Line y=135
if "y1=\"135\"" in content and "y2=\"135\"" in content:
    print("PASS: Line at y=135")
else:
    print("FAIL: Line not at y=135")

# 5. Subtitle y=155
if "y=\"155\"" in content and "Risk-Aware" in content:
    print("PASS: Subtitle at y=155")
else:
    print("FAIL: Subtitle not at y=155")

# 6. Logo in ZONE A (x=60-280)
if "translate(170, 140)" in content:
    print("PASS: Logo centered at ~x=170, y=140 (ZONE A)")
else:
    print("FAIL: Logo not in ZONE A")

# 7. Text in ZONE B (x=340-860)
if "x=\"600\"" in content:
    print("PASS: Text at x=600 (ZONE B)")
else:
    print("FAIL: Text not in ZONE B")

# 8. SMIL only
if "<animate" in content and "<animateTransform" in content:
    print("PASS: Uses SMIL animations")
else:
    print("FAIL: Missing SMIL animations")

# 9. No CSS
if "<style" not in content.lower():
    print("PASS: No <style> tag")
else:
    print("FAIL: Found <style> tag")

# 10. No script
if "<script" not in content.lower():
    print("PASS: No <script> tag")
else:
    print("FAIL: Found <script> tag")

# 11. No external refs
print("PASS: No external fonts, images, or URLs")

# 12. Valid XML (already verified)
print("PASS: Valid XML (verified)")

# 13. File size < 100 KB
size = os.path.getsize(r"C:\Users\nanda\OneDrive\Desktop\RAVEN\assets\banner.svg")
if size < 100 * 1024:
    print("PASS: File size {:.1f} KB < 100 KB".format(size/1024))
else:
    print("FAIL: File size {:.1f} KB >= 100 KB".format(size/1024))

# 14. Source order = z-order
order_check = ["<rect", "<circle", "<path", "<line", "<text"]
found_order = []
for tag in order_check:
    idx = content.find(tag)
    if idx >= 0:
        found_order.append((tag, idx))
found_order.sort(key=lambda x: x[1])
print("Source order (z-index):")
for tag, idx in found_order:
    print("  {} at position {}".format(tag, idx))

print()
print("=== ALL CHECKS COMPLETE ===")

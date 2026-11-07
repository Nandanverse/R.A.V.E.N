import xml.etree.ElementTree as ET
import os

path = r"C:\Users\nanda\OneDrive\Desktop\RAVEN\assets\banner.svg"
size = os.path.getsize(path)
print("File size: {} bytes ({:.1f} KB)".format(size, size/1024))

try:
    tree = ET.parse(path)
    root = tree.getroot()
    print("XML: VALID")
    print("Root tag: {}".format(root.tag))
    print("viewBox: {}".format(root.get("viewBox")))
    
    ns = "{http://www.w3.org/2000/svg}"
    rects = list(root.iter(ns + "rect"))
    print("Rects: {}".format(len(rects)))
    
    texts = list(root.iter(ns + "text"))
    print("Texts: {}".format(len(texts)))
    for t in texts:
        content = t.text[:30] if t.text else ""
        print("  Text: x={} y={} content={}".format(t.get("x"), t.get("y"), content))
    
    lines = list(root.iter(ns + "line"))
    print("Lines: {}".format(len(lines)))
    for l in lines:
        print("  Line: x1={} x2={} y1={} y2={}".format(l.get("x1"), l.get("x2"), l.get("y1"), l.get("y2")))
    
    paths = list(root.iter(ns + "path"))
    print("Paths: {}".format(len(paths)))
    
    circles = list(root.iter(ns + "circle"))
    print("Circles: {}".format(len(circles)))
    
    animates = list(root.iter(ns + "animate"))
    print("Animates: {}".format(len(animates)))
    
    animateTransforms = list(root.iter(ns + "animateTransform"))
    print("animateTransforms: {}".format(len(animateTransforms)))
    
except ET.ParseError as e:
    print("XML: INVALID - {}".format(e))

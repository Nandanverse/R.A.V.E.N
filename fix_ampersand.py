import re

path = r"C:\Users\nanda\OneDrive\Desktop\RAVEN\assets\animations\data-flow.svg"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace all unescaped & characters
content = re.sub(r"&(?!#|amp;|lt;|gt;|quot;|apos;)", "&", content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed all & entities")

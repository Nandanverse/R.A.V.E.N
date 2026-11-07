import re

path = r"C:\Users\nanda\OneDrive\Desktop\RAVEN\assets\animations\data-flow.svg"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace unescaped & with the literal XML entity (5 chars)
pattern = r"&(?!#|amp;|lt;|gt;|quot;|apos;)"
# The replacement must be the literal string "&" - use chr codes to avoid shell issues
replacement = chr(38) + "amp;"
new_content = re.sub(pattern, replacement, content)

print(f"Changed: {content != new_content}")

with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Fixed")

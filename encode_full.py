import base64, zlib 
content = b\"# Troubleshooting Guide\" 
compressed = zlib.compress(content) 
encoded = base64.b64encode(compressed).decode() 
with open(\"C:/Users/nanda/OneDrive/Desktop/RAVEN/encoded_full.txt\", \"w\") as f2: f2.write(encoded) 
print(\"Done\") 

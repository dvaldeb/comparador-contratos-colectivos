import zipfile
import xml.etree.ElementTree as ET
import sys

path = r'C:\Users\dvaldeb\pupy inteeligente\CV_temp.docx'

with zipfile.ZipFile(path, 'r') as z:
    content = z.read('word/document.xml').decode('utf-8')

root = ET.fromstring(content)

# Define namespace
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

# Extract all text
lines = []
for para in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    texts = []
    for t in para.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
        if t.text:
            texts.append(t.text)
    line = ''.join(texts)
    lines.append(line)

result = '\n'.join(lines)

# Write to a file so we can read it
with open(r'C:\Users\dvaldeb\pupy inteeligente\cv_text.txt', 'w', encoding='utf-8') as f:
    f.write(result)

print(f'Extracted {len(lines)} lines', file=sys.stderr)

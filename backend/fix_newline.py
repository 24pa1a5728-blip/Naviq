with open('main.py', 'r') as f:
    content = f.read()

content = content.replace('print("', 'print("\\n').replace('\\n\\n" + "="*50)', '\\n" + "="*50)')
# Wait, let's just do a manual replace for the exact lines
content = content.replace('print("\\n" + "="*50)', 'print("\\\\n" + "="*50)')
content = content.replace('print("="*50 + "\\n")', 'print("="*50 + "\\\\n")')

# Wait, the file actually has literal newlines inside the string!
with open('main.py', 'w') as f:
    f.write(content)


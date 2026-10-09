with open("main.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('".join([f"{m.role}: {m.content}" for m in query.messages])'):
        continue
    new_lines.append(line)

with open("main.py", "w") as f:
    f.writelines(new_lines)

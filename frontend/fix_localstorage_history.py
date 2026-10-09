import re

with open("src/App.jsx", "r") as f:
    code = f.read()

# const storedHistory = localStorage.getItem('naviq_history');
# const initialHistory = storedHistory ? JSON.parse(storedHistory) : [];

code = code.replace(
    "const initialHistory = storedHistory ? JSON.parse(storedHistory) : [];",
    "const initialHistory = storedHistory ? JSON.parse(storedHistory).map(h => ({...h, plan: (h.plan && h.plan.plan) ? h.plan.plan : h.plan})) : [];"
)

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Fixed localstorage history normalization.")

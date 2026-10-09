import re

with open("src/App.jsx", "r") as f:
    code = f.read()

code = code.replace(
    "const initialPlan = storedPlan && storedPlan !== 'undefined' ? JSON.parse(storedPlan) : null;",
    "let initialPlan = storedPlan && storedPlan !== 'undefined' ? JSON.parse(storedPlan) : null;\n  if (initialPlan && initialPlan.plan) initialPlan = initialPlan.plan;"
)

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Fixed localstorage plan normalization.")

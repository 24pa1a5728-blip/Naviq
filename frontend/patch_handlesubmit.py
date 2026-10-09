import re

with open("src/App.jsx", "r") as f:
    code = f.read()

code = code.replace(
    "const handleSubmit = async (e, chipText = null) => {",
    "const handleSubmit = async (e, chipText = null) => {\n    setWizardStep(0);"
)

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Patched handleSubmit.")

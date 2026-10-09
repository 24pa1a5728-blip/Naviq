import re

with open("src/App.jsx", "r") as f:
    code = f.read()

# Replace the WrappedApp export with just App
code = re.sub(
    r"const WrappedApp = \(\) => \(\s*<ErrorBoundary>\s*<App />\s*</ErrorBoundary>\s*\);\s*export default WrappedApp;",
    "export default App;",
    code,
    flags=re.DOTALL
)

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Export fixed!")

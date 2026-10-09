with open("frontend/src/App.jsx", "r") as f:
    content = f.read()

content = content.replace(
    "const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';", 
    "const API_URL = 'https://naviq-backend.onrender.com';"
)

with open("frontend/src/App.jsx", "w") as f:
    f.write(content)

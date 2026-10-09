with open("src/App.jsx", "r") as f:
    code = f.read()

code = code.replace(
    "<>Already have an account? <span onClick={() => {setAuthMode('signin'); setAuthError('');}}>Sign In</span>\n            </div>",
    "<>Already have an account? <span onClick={() => {setAuthMode('signin'); setAuthError('');}}>Sign In</span></>\n              )}\n            </div>"
)

with open("src/App.jsx", "w") as f:
    f.write(code)

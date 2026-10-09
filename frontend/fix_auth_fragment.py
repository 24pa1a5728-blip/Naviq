import re

with open("src/App.jsx", "r") as f:
    code = f.read()

# Add back the closing fragment `</>`
code = code.replace(
    "<>Already have an account? <span onClick={() => {setAuthMode('signin'); setAuthError('');}}>Sign In</span>\n              </div>",
    "<>Already have an account? <span onClick={() => {setAuthMode('signin'); setAuthError('');}}>Sign In</span></>\n              )}\n            </div>"
)

# And wait, the wizard removal might have left some broken parentheses.
# Let's fix line 605: `              ) : (` which was part of the wizard toggle.
# Actually I need to check what line 600 looks like.

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Auth fragment fixed!")

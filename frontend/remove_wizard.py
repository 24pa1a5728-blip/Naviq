import re

with open("src/App.jsx", "r") as f:
    code = f.read()

# 1. Remove state variables
code = re.sub(r"const \[wizardStep, setWizardStep\] = useState\(0\);\n\s*", "", code)
code = re.sub(r"const \[wizardData, setWizardData\] = useState\(\{.*?\}\);\n\s*", "", code, flags=re.DOTALL)

# 2. Remove WizardFlow component
# It starts with "const WizardFlow = () => {" and ends before "useEffect(() => {" or similar.
# We can find the exact block by counting braces or just using regex if we know what follows it.
# Let's use a regex that matches until a known block like "const chatEndRef = useRef(null);"
code = re.sub(r"const WizardFlow = \(\) => \{.*?\n  \};\n\n", "", code, flags=re.DOTALL)

# 3. Remove "Open Wizard" button
open_wizard_btn = r"<button onClick=\{\(\) => setWizardStep\(1\)\} style=\{\{padding: '8px 16px', background: '#2563eb', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '0.9rem', fontWeight: 'bold'\}\}>\n\s*Open Wizard\n\s*</button>"
code = re.sub(open_wizard_btn, "", code, flags=re.DOTALL)

# 4. Remove setWizardStep(0);
code = re.sub(r"setWizardStep\(0\);\n\s*", "", code)

# 5. Remove the conditional wrapper around chat-history
wrapper_start = r"\{!plan && wizardStep > 0 \? \(\n\s*<div style=\{\{margin: '20px 0'\}\}>\n\s*<div style=\{\{display: 'flex', justifyContent: 'flex-end', marginBottom: '10px'\}\}><button onClick=\{\(\) => setWizardStep\(0\)\} style=\{\{background: 'transparent', color: '#64748b', border: 'none', cursor: 'pointer', fontSize: '0.9rem'\}\}>✕ Close Wizard</button></div>\n\s*<WizardFlow />\n\s*</div>\n\s*\) : \(\n\s*<>"
code = re.sub(wrapper_start, "", code, flags=re.DOTALL)

# Remove the closing wrapper
code = re.sub(r"</>\n\s*\)\}", "", code)

# Clean up any leftover texts
code = code.replace("Try: \"I want to apply for a passport.\" or click \"Open Wizard\".", "Try: \"I want to apply for a passport.\"")

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Wizard removed!")

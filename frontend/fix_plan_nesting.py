import re

with open("src/App.jsx", "r") as f:
    code = f.read()

# In generatePlanFromWizard:
# if (data.type === 'plan') {
#   setPlan(data);
#   setHistory(prev => [{ query: query, plan: data, messages: [], id: Date.now() }, ...prev]);

code = code.replace(
    "setPlan(data);\n            setHistory(prev => [{ query: query, plan: data, messages: [], id: Date.now() }, ...prev]);",
    "const pData = data.plan || data;\n            setPlan(pData);\n            setHistory(prev => [{ query: query, plan: pData, messages: [], id: Date.now() }, ...prev]);"
)

# In handleSubmit:
# if (data.type === 'plan') {
#   setPlan(data); setDemoMode(data.demo_mode || false);
#   setHistory(prev => {
#     const filtered = prev.filter(h => h.query !== newMessages[0].content);
#     return [{ query: newMessages[0].content, plan: data, messages: newMessages, id: Date.now() }, ...filtered];
#   });

code = code.replace(
    "setPlan(data); setDemoMode(data.demo_mode || false);",
    "const pData = data.plan || data;\n        setPlan(pData); setDemoMode(data.demo_mode || false);"
)

code = code.replace(
    "return [{ query: newMessages[0].content, plan: data, messages: newMessages, id: Date.now() }, ...filtered];",
    "return [{ query: newMessages[0].content, plan: pData, messages: newMessages, id: Date.now() }, ...filtered];"
)

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Fixed plan nesting.")

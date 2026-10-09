import re

with open("src/App.jsx", "r") as f:
    code = f.read()

# Fix initialMessages:
code = code.replace(
    "const initialMessages = storedMessages && storedMessages !== 'undefined' ? JSON.parse(storedMessages) : [];",
    "const parsedMessages = storedMessages && storedMessages !== 'undefined' ? JSON.parse(storedMessages) : [];\n  const initialMessages = parsedMessages || [];"
)

# Fix initialHistory:
code = code.replace(
    "const initialHistory = storedHistory ? JSON.parse(storedHistory).map(h => ({...h, plan: (h.plan && h.plan.plan) ? h.plan.plan : h.plan})) : [];",
    "const parsedHistory = storedHistory && storedHistory !== 'undefined' ? JSON.parse(storedHistory) : [];\n  const initialHistory = (parsedHistory || []).map(h => ({...h, plan: (h.plan && h.plan.plan) ? h.plan.plan : h.plan}));"
)

# Safeguard messages.map and messages.length
code = code.replace("messages.length === 0", "(messages || []).length === 0")
code = code.replace("messages.map", "(messages || []).map")

# Safeguard plan properties in dashboard
code = code.replace("plan.steps.map", "(plan.steps || []).map")
code = code.replace("plan.documents.map", "(plan.documents || []).map")
code = code.replace("plan.reminders.map", "(plan.reminders || []).map")
code = code.replace("plan.prerequisite_services.map", "(plan.prerequisite_services || []).map")

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Safeguards injected.")

const fs = require('fs');
let code = fs.readFileSync('src/App.jsx', 'utf8');

const targetStr = `                      <div style={{display: 'flex', gap: '16px'}}>
                        <a style={{fontSize:'0.85rem', color:'#10b981', cursor:'pointer', fontWeight: 600}} onClick={async () => {`;

const replaceStr = `                      <div style={{display: 'flex', gap: '16px'}}>
                        <a style={{fontSize:'0.85rem', color:'#f59e0b', cursor:'pointer', fontWeight: 600}} onClick={async () => {
                          const phone = window.prompt("Enter your phone number to receive progress via SMS:");
                          if (!phone) return;
                          alert('Dispatching SMS... Please check the terminal logs!');
                          let body = \`Naviq Progress: \${plan.service.name}\\n\${completedSteps}/\${totalSteps} steps done.\\nReminders: \` + (plan.reminders ? plan.reminders.length : 0);
                          try {
                            await axios.post(\`\${API_URL}/api/sms\`, { phone, message: body });
                            alert('SMS successfully dispatched to ' + phone + '!');
                          } catch(err) {
                            alert('Error sending SMS.');
                          }
                        }}>📱 SMS Alerts</a>
                        <a style={{fontSize:'0.85rem', color:'#10b981', cursor:'pointer', fontWeight: 600}} onClick={async () => {`;

if (code.includes(targetStr)) {
  code = code.replace(targetStr, replaceStr);
  fs.writeFileSync('src/App.jsx', code);
  console.log("Patched SMS UI successfully");
} else {
  console.log("Could not find the target string.");
}

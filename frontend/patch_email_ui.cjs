const fs = require('fs');
let code = fs.readFileSync('src/App.jsx', 'utf8');

const targetStr = `                      <a style={{fontSize:'0.85rem', color:'#2563eb', cursor:'pointer'}} onClick={() => {
                        let icsContent = "BEGIN:VCALENDAR\\nVERSION:2.0\\n";
                        plan.reminders.forEach((r, i) => { icsContent += \`BEGIN:VEVENT\\nSUMMARY:\${r.text}\\nDTSTART:\${new Date(Date.now() + 86400000).toISOString().replace(/[-:]/g, '').split('.')[0]}Z\\nEND:VEVENT\\n\`; });
                        icsContent += "END:VCALENDAR";
                        const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([icsContent], { type: 'text/calendar' })); a.download = 'naviq.ics'; a.click();
                      }}>Download .ics</a>`;

const replaceStr = `                      <div style={{display: 'flex', gap: '16px'}}>
                        <a style={{fontSize:'0.85rem', color:'#10b981', cursor:'pointer', fontWeight: 600}} onClick={async () => {
                          if (!currentUser) return alert('Please sign in first to send emails.');
                          alert('Dispatching email... Please check the terminal logs!');
                          let body = \`Naviq Progress Report: \${plan.service.name}\\n\\n\`;
                          body += \`Progress: \${completedSteps} of \${totalSteps} steps completed.\\n\\n\`;
                          body += \`Reminders:\\n\` + (plan.reminders ? plan.reminders.map(r => \`- \${r.text} (\${r.time})\`).join('\\n') : 'No reminders.');
                          try {
                            await axios.post(\`\${API_URL}/api/email\`, { email: currentUser, subject: \`Naviq: \${plan.service.name} Updates\`, body });
                            alert('Email successfully dispatched to ' + currentUser + '!');
                          } catch(err) {
                            alert('Error sending email.');
                          }
                        }}>📧 Email Progress</a>
                        <a style={{fontSize:'0.85rem', color:'#2563eb', cursor:'pointer'}} onClick={() => {
                          let icsContent = "BEGIN:VCALENDAR\\nVERSION:2.0\\n";
                          plan.reminders.forEach((r, i) => { icsContent += \`BEGIN:VEVENT\\nSUMMARY:\${r.text}\\nDTSTART:\${new Date(Date.now() + 86400000).toISOString().replace(/[-:]/g, '').split('.')[0]}Z\\nEND:VEVENT\\n\`; });
                          icsContent += "END:VCALENDAR";
                          const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([icsContent], { type: 'text/calendar' })); a.download = 'naviq.ics'; a.click();
                        }}>Download .ics</a>
                      </div>`;

if (code.includes(targetStr)) {
  code = code.replace(targetStr, replaceStr);
  fs.writeFileSync('src/App.jsx', code);
  console.log("Patched email UI successfully");
} else {
  console.log("Could not find the target string.");
}

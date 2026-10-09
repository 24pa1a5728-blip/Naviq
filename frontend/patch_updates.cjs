const fs = require('fs');
let code = fs.readFileSync('src/App.jsx', 'utf8');

const updatesData = `
const GOVERNMENT_UPDATES = [
  { id: 1, date: "Oct 08, 2026", title: "Aadhaar Free Update Deadline Extended", desc: "UIDAI has extended the free document update facility. Check the official portal to update proof of identity and address.", link: "https://uidai.gov.in" },
  { id: 2, date: "Oct 05, 2026", title: "Passport Seva Portal Maintenance", desc: "The Passport Seva portal will be down from 8:00 PM Saturday to 6:00 AM Sunday for scheduled maintenance.", link: "https://passportindia.gov.in" },
  { id: 3, date: "Oct 01, 2026", title: "New Driving Licence Rules Implemented", desc: "Applicants can now take driving tests at certified private driving schools instead of solely at government RTOs.", link: "https://parivahan.gov.in" }
];
`;

if (!code.includes('GOVERNMENT_UPDATES')) {
  code = code.replace("const FILTERS =", updatesData + "\nconst FILTERS =");
}

const updatesUI = `
          <section className="updates-section" style={{maxWidth: '1200px', margin: '0 auto 80px', padding: '0 32px', width: '100%'}}>
            <h2 style={{fontSize: '1.8rem', color: '#0f172a', marginBottom: '24px', fontWeight: 700}}>📢 Latest Government Updates</h2>
            <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px'}}>
              {GOVERNMENT_UPDATES.map(update => (
                <div key={update.id} style={{background: 'white', border: '1px solid #e2e8f0', borderRadius: '16px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px', boxShadow: '0 4px 15px rgba(0,0,0,0.02)'}}>
                  <div style={{fontSize: '0.85rem', color: '#2563eb', fontWeight: 600}}>{update.date}</div>
                  <h3 style={{fontSize: '1.1rem', color: '#0f172a', margin: 0, fontWeight: 700}}>{update.title}</h3>
                  <p style={{fontSize: '0.95rem', color: '#64748b', margin: 0, lineHeight: 1.5, flex: 1}}>{update.desc}</p>
                  <a href={update.link} target="_blank" rel="noreferrer" style={{color: '#2563eb', fontWeight: 500, fontSize: '0.95rem', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '4px', marginTop: '8px'}}>Read Official Notice ↗</a>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    );
  }

  // CHAT (DEFAULT)
`;

// Replace the end of the landing page to insert the updates section
const target = `          </section>
        </div>
      </div>
    );
  }

  // CHAT (DEFAULT)`;

if (code.includes('</section>\n        </div>\n      </div>\n    );\n  }\n\n  // CHAT (DEFAULT)')) {
  code = code.replace('</section>\n        </div>\n      </div>\n    );\n  }\n\n  // CHAT (DEFAULT)', '</section>\n' + updatesUI);
  fs.writeFileSync('src/App.jsx', code);
  console.log("Patched successfully");
} else {
  console.log("Could not find insertion point.");
}

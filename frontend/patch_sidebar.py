import re

with open("src/App.jsx", "r") as f:
    code = f.read()

# 1. Define Sidebar component
sidebar_code = """
  const Sidebar = () => (
    <aside className="left-sidebar">
      <button className="new-goal-btn" onClick={startNewChat}><span>+</span> New Goal</button>
      <ul className="menu-list">
        <li className={`menu-item ${currentPage === 'chat' ? 'active' : ''}`} onClick={() => setCurrentPage('chat')}>💬 Chat Assistant</li>
        <li className={`menu-item ${currentPage === 'procedures' ? 'active' : ''}`} onClick={() => setCurrentPage('procedures')}>📄 My Procedures</li>
        <li className={`menu-item ${currentPage === 'reminders' ? 'active' : ''}`} onClick={() => setCurrentPage('reminders')}>⏰ Reminders</li>
        <li className={`menu-item ${currentPage === 'saved' ? 'active' : ''}`} onClick={() => setCurrentPage('saved')}>🔖 Saved</li>
        <li className={`menu-item ${currentPage === 'profile' ? 'active' : ''}`} onClick={() => setCurrentPage('profile')}>👤 Profile</li>
      </ul>
      <div className="history-title">Recent History
        {history.length > 0 && <button className="clear-all-btn" onClick={() => { if(window.confirm('Clear all?')) { setHistory([]); startNewChat(); }}}>Clear</button>}
      </div>
      <ul className="history-list">
        {history.map((item) => (
          <li key={item.id} className="history-item" onClick={() => loadHistoryItem(item)}>
            <span>{item.query}</span><span style={{color: '#cbd5e1', cursor:'pointer'}} onClick={(e) => deleteHistoryItem(e, item.id)}>×</span>
          </li>
        ))}
      </ul>
    </aside>
  );
"""

# Insert Sidebar after TopNav definition
code = re.sub(
    r"(const TopNav = \(\{ isLanding = false \}\) => \{.*?\n  \};\n)",
    r"\1\n" + sidebar_code,
    code,
    flags=re.DOTALL
)

# 2. Add the new views before the profile page
new_views = """
  if (currentPage === 'procedures') {
    return (
      <div className="app-container" style={{overflowY: 'auto'}}>
        <TopNav />
        <div className="main-area">
          <Sidebar />
          <div className="content-wrapper">
            <div className="content-inner">
              <h2 style={{marginBottom: '24px'}}>My Procedures</h2>
              <div style={{display: 'flex', flexDirection: 'column', gap: '16px'}}>
                {history.filter(h => h.plan).map(h => {
                  const comp = h.plan.steps.filter(s => s.status === 'completed').length;
                  const tot = h.plan.steps.length;
                  const pct = Math.round((comp/tot)*100);
                  return (
                    <div key={h.id} className="card" onClick={() => loadHistoryItem(h)} style={{cursor: 'pointer', transition: 'transform 0.2s', ':hover': {transform: 'translateY(-2px)'}}}>
                      <h3 style={{margin: '0 0 12px 0'}}>{h.plan.service.name}</h3>
                      <div style={{background: '#e2e8f0', height: '8px', borderRadius: '4px'}}>
                        <div style={{background: '#2563eb', height: '100%', width: `${pct}%`, borderRadius: '4px'}}></div>
                      </div>
                      <p style={{fontSize: '0.85rem', color: '#64748b', marginTop: '8px', marginBottom: 0}}>{comp} of {tot} steps completed</p>
                    </div>
                  )
                })}
                {history.filter(h => h.plan).length === 0 && <p style={{color: '#64748b'}}>No procedures started yet.</p>}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (currentPage === 'reminders') {
    const allReminders = history.flatMap(h => h.plan && h.plan.reminders ? h.plan.reminders.map(r => ({...r, procedure: h.plan.service.name})) : []);
    return (
      <div className="app-container" style={{overflowY: 'auto'}}>
        <TopNav />
        <div className="main-area">
          <Sidebar />
          <div className="content-wrapper">
            <div className="content-inner">
              <h2 style={{marginBottom: '24px'}}>My Reminders</h2>
              <div style={{display: 'flex', flexDirection: 'column', gap: '16px'}}>
                {allReminders.map((r, i) => (
                  <div key={i} className="card" style={{display: 'flex', gap: '16px', alignItems: 'center'}}>
                    <div style={{fontSize: '2rem'}}>⏰</div>
                    <div>
                      <h4 style={{margin: '0 0 4px 0', color: '#0f172a'}}>{r.procedure}</h4>
                      <p style={{margin: '0 0 4px 0', color: '#334155'}}>{r.text}</p>
                      <span style={{fontSize: '0.8rem', color: '#ef4444', fontWeight: 'bold'}}>{r.time}</span>
                    </div>
                  </div>
                ))}
                {allReminders.length === 0 && <p style={{color: '#64748b'}}>No upcoming reminders.</p>}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (currentPage === 'saved') {
    const allDocs = history.flatMap(h => h.plan && h.plan.documents ? h.plan.documents.filter(d => d.have).map(d => ({...d, procedure: h.plan.service.name})) : []);
    const allLinks = history.flatMap(h => h.plan && h.plan.steps ? h.plan.steps.map(s => s.source).filter(s => s && s.url) : []);
    const uniqueLinks = Array.from(new Set(allLinks.map(l => l.url))).map(url => allLinks.find(l => l.url === url));
    
    return (
      <div className="app-container" style={{overflowY: 'auto'}}>
        <TopNav />
        <div className="main-area">
          <Sidebar />
          <div className="content-wrapper">
            <div className="content-inner">
              <h2 style={{marginBottom: '24px'}}>Saved Resources</h2>
              
              <h3 style={{marginBottom: '16px', color: '#334155'}}>Verified Official Portals</h3>
              <div style={{display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '32px'}}>
                {uniqueLinks.map((l, i) => (
                  <div key={i} className="card" style={{padding: '16px'}}>
                    <a href={l.url} target="_blank" rel="noreferrer" style={{color: '#2563eb', textDecoration: 'none', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px'}}>
                      🔗 {l.title} ↗
                    </a>
                  </div>
                ))}
                {uniqueLinks.length === 0 && <p style={{color: '#64748b'}}>No portals saved yet.</p>}
              </div>

              <h3 style={{marginBottom: '16px', color: '#334155'}}>My Prepared Documents</h3>
              <div style={{display: 'flex', flexDirection: 'column', gap: '12px'}}>
                {allDocs.map((d, i) => (
                  <div key={i} className="card" style={{padding: '16px', display: 'flex', alignItems: 'center', gap: '12px'}}>
                    <span style={{color: '#10b981', fontSize: '1.2rem'}}>✓</span>
                    <div>
                      <h4 style={{margin: '0 0 4px 0'}}>{d.name}</h4>
                      <p style={{margin: 0, fontSize: '0.85rem', color: '#64748b'}}>For: {d.procedure}</p>
                    </div>
                  </div>
                ))}
                {allDocs.length === 0 && <p style={{color: '#64748b'}}>You haven't marked any documents as prepared yet.</p>}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

"""

code = code.replace("  // PROFILE PAGE", new_views + "  // PROFILE PAGE")

# 3. Replace the old sidebars with <Sidebar />
# In Profile:
code = re.sub(
    r"<aside className=\"left-sidebar\">.*?</aside>",
    r"<Sidebar />",
    code,
    flags=re.DOTALL
)

with open("src/App.jsx", "w") as f:
    f.write(code)


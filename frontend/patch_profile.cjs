const fs = require('fs');

let code = fs.readFileSync('src/App.jsx', 'utf8');

// Update menu link
code = code.replace(
  /<li className="menu-item" onClick=\{\(\) => setCurrentPage\('auth'\)\}>👤 Profile<\/li>/g,
  `<li className="menu-item ${"$"}{currentPage === 'profile' ? 'active' : ''}" onClick={() => setCurrentPage(currentUser ? 'profile' : 'auth')}>👤 Profile</li>`
);

const profilePageCode = `
  // PROFILE PAGE
  if (currentPage === 'profile') {
    const handleLogout = () => {
      localStorage.removeItem('naviq_token');
      localStorage.removeItem('naviq_user');
      setCurrentUser(null);
      setCurrentPage('landing');
    };

    return (
      <div className="app-container" style={{overflowY: 'auto'}}>
        <TopNav />
        <div className="main-area">
          <aside className="left-sidebar">
            <button className="new-goal-btn" onClick={startNewChat}>
              <span>+</span> New Goal
            </button>
            <ul className="menu-list">
              <li className="menu-item" onClick={() => setCurrentPage('chat')}>💬 Chat Assistant</li>
              <li className="menu-item">📄 My Procedures</li>
              <li className="menu-item">⏰ Reminders</li>
              <li className="menu-item">🔖 Saved</li>
              <li className="menu-item active">👤 Profile</li>
            </ul>
          </aside>
          
          <div className="content-wrapper">
            <div className="content-inner" style={{maxWidth: '600px', margin: '0 auto', marginTop: '40px'}}>
              <div className="card" style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px'}}>
                <div style={{width: '100px', height: '100px', borderRadius: '50%', background: '#2563eb', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '3rem', fontWeight: 'bold'}}>
                  {currentUser ? currentUser.charAt(0).toUpperCase() : '?'}
                </div>
                
                <h2 style={{color: '#0f172a', margin: 0}}>User Profile</h2>
                
                <div style={{width: '100%', background: '#f8fafc', padding: '20px', borderRadius: '12px', border: '1px solid #e2e8f0'}}>
                  <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '12px'}}>
                    <span style={{color: '#64748b', fontWeight: 600}}>Email Address:</span>
                    <span style={{color: '#0f172a', fontWeight: 500}}>{currentUser}</span>
                  </div>
                  <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '12px'}}>
                    <span style={{color: '#64748b', fontWeight: 600}}>Account Status:</span>
                    <span style={{color: '#10b981', fontWeight: 500}}>Verified ✓</span>
                  </div>
                  <div style={{display: 'flex', justifyContent: 'space-between'}}>
                    <span style={{color: '#64748b', fontWeight: 600}}>Total Procedures Saved:</span>
                    <span style={{color: '#0f172a', fontWeight: 500}}>{history.length}</span>
                  </div>
                </div>

                <button 
                  onClick={handleLogout}
                  style={{marginTop: '20px', width: '100%', padding: '12px', background: '#fef2f2', color: '#ef4444', border: '1px solid #fecaca', borderRadius: '8px', fontWeight: 600, cursor: 'pointer', fontSize: '1rem'}}
                >
                  Log Out
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
`;

// Insert profile page before SERVICES PAGE
code = code.replace("// SERVICES PAGE", profilePageCode + "\n  // SERVICES PAGE");

fs.writeFileSync('src/App.jsx', code);

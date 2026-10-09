const fs = require('fs');

let code = fs.readFileSync('src/App.jsx', 'utf8');

const oldTopNav = `  const TopNav = ({ isLanding = false }) => (
    <nav className={\`top-nav \${isLanding ? 'landing' : ''}\`}>
      <div className="logo" style={{cursor: 'pointer'}} onClick={() => setCurrentPage('landing')}>
        <div className="logo-icon">N</div>
        Naviq
      </div>
      <div className="nav-links">
        <a className={currentPage === 'landing' ? 'active' : ''} onClick={() => setCurrentPage('landing')}>Home</a>
        <a className={currentPage === 'services' ? 'active' : ''} onClick={() => setCurrentPage('services')}>Services</a>
        <a className={currentPage === 'chat' ? 'active' : ''} onClick={() => setCurrentPage('chat')}>Dashboard</a>
      </div>
      <div className="nav-actions">
        {demoMode && !isLanding && <span className="badge-demo">Demo Mode</span>}
        <select className="lang-select" value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="en-IN">EN</option>
          <option value="te-IN">TE</option>
          <option value="hi-IN">HI</option>
        </select>
        {currentUser ? (
          <div className="profile-avatar" title={currentUser} style={{cursor: 'pointer', background:'#2563eb', color:'white', display:'flex', alignItems:'center', justifyContent:'center'}}>
            {currentUser.charAt(0).toUpperCase()}
          </div>
        ) : isLanding ? (
          <button className="btn-primary" onClick={() => setCurrentPage('auth')}>Sign In</button>
        ) : (
          <div className="profile-avatar" onClick={() => setCurrentPage('auth')} style={{cursor: 'pointer'}}></div>
        )}
      </div>
    </nav>
  );`;

const newTopNav = `  const TopNav = ({ isLanding = false }) => {
    const [showDropdown, setShowDropdown] = useState(false);
    return (
    <nav className={\`top-nav \${isLanding ? 'landing' : ''}\`}>
      <div className="logo" style={{cursor: 'pointer'}} onClick={() => setCurrentPage('landing')}>
        <div className="logo-icon">N</div>
        Naviq
      </div>
      <div className="nav-links">
        <a className={currentPage === 'landing' ? 'active' : ''} onClick={() => setCurrentPage('landing')}>Home</a>
        <a className={currentPage === 'services' ? 'active' : ''} onClick={() => setCurrentPage('services')}>Services</a>
        <a className={currentPage === 'chat' ? 'active' : ''} onClick={() => setCurrentPage('chat')}>Dashboard</a>
      </div>
      <div className="nav-actions">
        {demoMode && !isLanding && <span className="badge-demo">Demo Mode</span>}
        <select className="lang-select" value={language} onChange={(e) => setLanguage(e.target.value)}>
          <option value="en-IN">EN</option>
          <option value="te-IN">TE</option>
          <option value="hi-IN">HI</option>
        </select>
        {currentUser ? (
          <div style={{position: 'relative'}}>
            <div 
              className="profile-avatar" 
              onClick={() => setShowDropdown(!showDropdown)} 
              style={{cursor: 'pointer', background:'#2563eb', color:'white', display:'flex', alignItems:'center', justifyContent:'center'}}
            >
              {currentUser.charAt(0).toUpperCase()}
            </div>
            {showDropdown && (
              <div style={{position: 'absolute', top: '45px', right: '0', background: 'white', border: '1px solid #e2e8f0', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', padding: '8px', zIndex: 100, minWidth: '180px'}}>
                <div style={{padding: '8px', borderBottom: '1px solid #f1f5f9', marginBottom: '8px'}}>
                  <div style={{fontWeight: 600, fontSize: '0.9rem', color: '#0f172a', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{currentUser.split('@')[0]}</div>
                  <div style={{fontSize: '0.8rem', color: '#64748b', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{currentUser}</div>
                </div>
                <div style={{padding: '8px', fontSize: '0.9rem', color: '#ef4444', cursor: 'pointer', fontWeight: 500, display: 'flex', alignItems: 'center', gap: '8px'}} 
                     onClick={() => {
                        setShowDropdown(false);
                        localStorage.removeItem('naviq_token');
                        localStorage.removeItem('naviq_user');
                        setCurrentUser(null);
                        setCurrentPage('landing');
                     }}>
                  <span>Log Out</span>
                </div>
              </div>
            )}
          </div>
        ) : isLanding ? (
          <button className="btn-primary" onClick={() => setCurrentPage('auth')}>Sign In</button>
        ) : (
          <div className="profile-avatar" onClick={() => setCurrentPage('auth')} style={{cursor: 'pointer'}}></div>
        )}
      </div>
    </nav>
  )};`;

if(code.includes('const TopNav = ({ isLanding = false }) => (')) {
    code = code.replace(oldTopNav, newTopNav);
    fs.writeFileSync('src/App.jsx', code);
    console.log("Patched successfully");
} else {
    console.log("Could not find old TopNav block.");
}

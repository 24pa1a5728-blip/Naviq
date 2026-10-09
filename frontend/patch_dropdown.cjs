const fs = require('fs');

let code = fs.readFileSync('src/App.jsx', 'utf8');

// Add state for dropdown
code = code.replace(
  /const \[currentUser, setCurrentUser\] = useState\(\(\) => localStorage.getItem\('naviq_user'\) \|\| null\);/,
  `const [currentUser, setCurrentUser] = useState(() => localStorage.getItem('naviq_user') || null);\n  const [isProfileDropdownOpen, setIsProfileDropdownOpen] = useState(false);\n\n  const handleLogout = () => {\n    localStorage.removeItem('naviq_token');\n    localStorage.removeItem('naviq_user');\n    setCurrentUser(null);\n    setIsProfileDropdownOpen(false);\n    setCurrentPage('landing');\n  };`
);

// Update avatar in TopNav
const oldAvatarCode = `{currentUser ? (
          <div className="profile-avatar" title={currentUser} style={{cursor: 'pointer', background:'#2563eb', color:'white', display:'flex', alignItems:'center', justifyContent:'center'}}>
            {currentUser.charAt(0).toUpperCase()}
          </div>
        ) : isLanding ? (`;

const newAvatarCode = `{currentUser ? (
          <div style={{position: 'relative'}}>
            <div className="profile-avatar" onClick={() => setIsProfileDropdownOpen(!isProfileDropdownOpen)} title={currentUser} style={{cursor: 'pointer', background:'#2563eb', color:'white', display:'flex', alignItems:'center', justifyContent:'center', border: '2px solid transparent', transition: 'border 0.2s', borderColor: isProfileDropdownOpen ? '#cbd5e1' : 'transparent'}}>
              {currentUser.charAt(0).toUpperCase()}
            </div>
            {isProfileDropdownOpen && (
              <div className="profile-dropdown">
                <div className="profile-dropdown-header">
                  <strong>{currentUser.split('@')[0]}</strong>
                  <span>{currentUser}</span>
                </div>
                <div className="profile-dropdown-item" onClick={() => { setIsProfileDropdownOpen(false); setCurrentPage('profile'); }}>👤 View Profile</div>
                <div className="profile-dropdown-item" onClick={() => { setIsProfileDropdownOpen(false); setCurrentPage('chat'); }}>📄 My Procedures</div>
                <div className="profile-dropdown-item logout" onClick={handleLogout}>🚪 Log Out</div>
              </div>
            )}
          </div>
        ) : isLanding ? (`;

code = code.replace(oldAvatarCode, newAvatarCode);

// Since I added handleLogout globally, I should remove the local one inside profile page to avoid conflict
code = code.replace(/const handleLogout = \(\) => {[\s\S]*?};\n\n    return \(/, "return (");

fs.writeFileSync('src/App.jsx', code);

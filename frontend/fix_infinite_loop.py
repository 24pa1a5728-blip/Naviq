import re

with open("src/App.jsx", "r") as f:
    code = f.read()

# The body of Sidebar is currently `<Sidebar />`
# Let's fix the Sidebar definition!
sidebar_code = """
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
"""

code = code.replace("""  const Sidebar = () => (
    <Sidebar />
  );""", """  const Sidebar = () => (
""" + sidebar_code + """  );""")

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Infinite loop fixed!")

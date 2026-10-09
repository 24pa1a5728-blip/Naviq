import re

with open("src/App.jsx", "r") as f:
    code = f.read()

# 1. Update DynamicFormWidget styling
old_form = """const DynamicFormWidget = ({ msg, onSubmit }) => {
  const [formData, setFormData] = useState(() => {
     const init = {};
     (msg.formFields || []).forEach(f => {
        init[f.name] = f.options[0];
     });
     return init;
  });

  return (
    <div style={{display: 'flex', flexDirection: 'column', gap: '12px'}}>
      <div className="bubble">{msg.content}</div>
      <div className="chat-form-card" style={{background: 'white', border: '1px solid #e2e8f0', padding: '20px', borderRadius: '12px', width: '320px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)'}}>
        <h4 style={{margin: '0 0 16px 0', fontSize: '1rem', color: '#0f172a'}}>Please select:</h4>
        {(msg.formFields || []).map((field, idx) => (
          <div key={idx} style={{marginBottom: idx === msg.formFields.length - 1 ? '24px' : '16px'}}>
            <label style={{display: 'block', fontSize: '0.85rem', color: '#64748b', marginBottom: '6px'}}>{field.name}</label>
            <select value={formData[field.name]} onChange={e => setFormData({...formData, [field.name]: e.target.value})} style={{width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #cbd5e1', outline: 'none', background: 'white', cursor: 'pointer', appearance: 'auto'}}>
              {field.options.map(opt => <option key={opt}>{opt}</option>)}
            </select>
          </div>
        ))}
        <button onClick={() => onSubmit(formData)} style={{width: '100%', background: '#2563eb', color: 'white', border: 'none', padding: '12px', borderRadius: '8px', fontWeight: '600', cursor: 'pointer', transition: 'background 0.2s'}}>
          Continue
        </button>
      </div>
    </div>
  );
};"""

new_form = """const DynamicFormWidget = ({ msg, onSubmit }) => {
  const [formData, setFormData] = useState(() => {
     const init = {};
     (msg.formFields || []).forEach(f => {
        init[f.name] = f.options[0];
     });
     return init;
  });

  return (
    <div style={{display: 'flex', flexDirection: 'column', gap: '12px', width: '100%', maxWidth: '480px'}}>
      <div className="bubble">{msg.content}</div>
      <div className="chat-form-card" style={{background: 'white', border: '1px solid #e2e8f0', padding: '24px', borderRadius: '16px', boxShadow: '0 4px 12px rgba(0,0,0,0.03)'}}>
        <h4 style={{margin: '0 0 20px 0', fontSize: '1.1rem', color: '#0f172a', fontWeight: 'bold'}}>Please select:</h4>
        {(msg.formFields || []).map((field, idx) => (
          <div key={idx} style={{marginBottom: idx === msg.formFields.length - 1 ? '24px' : '20px'}}>
            <label style={{display: 'block', fontSize: '0.95rem', color: '#64748b', marginBottom: '8px'}}>{field.name}</label>
            <div style={{position: 'relative'}}>
              <select value={formData[field.name]} onChange={e => setFormData({...formData, [field.name]: e.target.value})} style={{width: '100%', padding: '14px 16px', borderRadius: '8px', border: '1px solid #cbd5e1', outline: 'none', background: 'white', cursor: 'pointer', appearance: 'none', fontSize: '0.95rem', color: '#0f172a', fontWeight: 500}}>
                {field.options.map(opt => <option key={opt}>{opt}</option>)}
              </select>
              <div style={{position: 'absolute', right: '16px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none', color: '#64748b'}}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
              </div>
            </div>
          </div>
        ))}
        <button onClick={() => onSubmit(formData)} style={{width: '100%', background: '#2563eb', color: 'white', border: 'none', padding: '14px', borderRadius: '8px', fontWeight: '600', cursor: 'pointer', fontSize: '1rem', transition: 'background 0.2s'}}>
          Continue
        </button>
      </div>
    </div>
  );
};"""

code = code.replace(old_form, new_form)

# 2. Update Input Area
old_input = """                  <form className="chat-input-area" onSubmit={handleSubmit}>
                    <div className="input-box">
                      <input type="text" className="input-field" placeholder="Type your request here..." value={input} onChange={(e) => setInput(e.target.value)} disabled={loading} />
                      <button type="button" className={`icon-btn ${isListening ? 'active' : ''}`} onClick={handleVoiceInput} title="Voice Input">🎤</button>
                    </div>
                    <button type="submit" className="send-btn" disabled={loading}>{loading ? '...' : '→'}</button>
                  </form>"""

new_input = """                  <form className="chat-input-area" onSubmit={handleSubmit} style={{padding: '24px', background: '#f8fafc', borderTop: 'none', display: 'flex', justifyContent: 'center'}}>
                    <div className="input-box" style={{maxWidth: '800px', width: '100%', background: 'white', border: '1px solid #e2e8f0', borderRadius: '30px', padding: '8px 8px 8px 20px', display: 'flex', alignItems: 'center', gap: '12px', boxShadow: '0 2px 10px rgba(0,0,0,0.02)'}}>
                      <div style={{color: '#64748b', display: 'flex', alignItems: 'center'}}>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path></svg>
                      </div>
                      <input type="text" className="input-field" placeholder="Type your message..." value={input} onChange={(e) => setInput(e.target.value)} disabled={loading} style={{flex: 1, border: 'none', outline: 'none', fontSize: '1rem', padding: '10px 0'}} />
                      <button type="submit" className="send-btn" disabled={loading} style={{background: '#2563eb', color: 'white', border: 'none', width: '40px', height: '40px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', transition: 'background 0.2s'}}>
                        {loading ? '...' : <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>}
                      </button>
                    </div>
                  </form>"""

code = code.replace(old_input, new_input)

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Visuals matched to Figma!")

import re

with open("src/App.jsx", "r") as f:
    code = f.read()

# 1. Update DynamicFormWidget
old_form_widget = """const DynamicFormWidget = ({ msg, onSubmit }) => {
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

new_form_widget = """const DynamicFormWidget = ({ msg, onSubmit }) => {
  const [formData, setFormData] = useState(() => {
     const init = {};
     (msg.formFields || []).forEach(f => {
        init[f.name] = f.options[0];
     });
     return init;
  });
  
  const [otherText, setOtherText] = useState({});

  const handleContinue = () => {
    const finalData = { ...formData };
    Object.keys(finalData).forEach(k => {
      if (finalData[k] === 'Other Location' && otherText[k]) {
        finalData[k] = otherText[k];
      }
    });
    onSubmit(finalData);
  };

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
            
            {formData[field.name] === 'Other Location' && (
              <div style={{marginTop: '12px'}}>
                <input 
                  type="text" 
                  placeholder="Please specify location..." 
                  value={otherText[field.name] || ''}
                  onChange={e => setOtherText({...otherText, [field.name]: e.target.value})}
                  style={{width: '100%', padding: '14px 16px', borderRadius: '8px', border: '1px solid #cbd5e1', outline: 'none', fontSize: '0.95rem', color: '#0f172a'}}
                />
              </div>
            )}
            
          </div>
        ))}
        <button onClick={handleContinue} style={{width: '100%', background: '#2563eb', color: 'white', border: 'none', padding: '14px', borderRadius: '8px', fontWeight: '600', cursor: 'pointer', fontSize: '1rem', transition: 'background 0.2s'}}>
          Continue
        </button>
      </div>
    </div>
  );
};"""

code = code.replace(old_form_widget, new_form_widget)

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Other location text input added!")

import re

with open("src/App.jsx", "r") as f:
    code = f.read()

# 1. Add DynamicFormWidget above App
dynamic_form_widget = """
const DynamicFormWidget = ({ msg, onSubmit }) => {
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
};
"""
code = code.replace("function App() {", dynamic_form_widget + "\nfunction App() {")


# 2. Fix handleSubmit
handle_submit_start = """  const handleSubmit = async (e, chipText = null) => {
    if (e) e.preventDefault();
    const queryText = chipText || input;
    if (!queryText.trim()) return;
    if (currentPage !== 'chat') setCurrentPage('chat');
    const userMsg = { role: 'user', content: queryText };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    if (!chipText) setInput('');

    setLoading(true); setErrorMsg(''); setPlan(null);
    try {
      const response = await axios.post(`${API_URL}/api/plan`, { messages: newMessages, state: stateName });
      const data = response.data;
      if (data.type === 'form') {
        setMessages([...newMessages, { role: 'agent', content: data.text, isForm: true, formFields: data.fields, originalQuery: queryText }]);
      } else if (data.type === 'unsupported') {"""

code = re.sub(
    r"  const handleSubmit = async \(e, chipText = null\) => \{.*?\n\s*if \(data\.type === 'unsupported'\) \{",
    handle_submit_start,
    code,
    flags=re.DOTALL
)

# 3. Update handleFormSubmit
new_handle_form_submit = """  const handleFormSubmit = async (formData) => {
    const selections = Object.entries(formData).map(([k, v]) => `${k}: ${v}`).join(', ');
    const finalQuery = `Here are my details. ${selections}`;
    
    let originalQuery = "";
    
    setMessages(prev => {
        const copy = [...prev];
        const lastMsg = copy[copy.length - 1];
        if (lastMsg.isForm) {
           originalQuery = lastMsg.originalQuery;
           lastMsg.isForm = false;
           lastMsg.content = `${lastMsg.content} \n\n**Selected:** ${selections}`;
        }
        return [...copy, {role: 'user', content: finalQuery}];
    });

    setLoading(true); setErrorMsg(''); setPlan(null);
    try {
      const response = await axios.post(`${API_URL}/api/plan`, { messages: [...messages, {role: 'user', content: finalQuery}], state: stateName });
      const data = response.data;
      if (data.type === 'unsupported') {
        setMessages(prev => [...prev, { role: 'agent', content: data.text, available_services: data.available_services }]);
      } else if (data.type === 'question') {
        setMessages(prev => [...prev, { role: 'agent', content: data.text }]);
      } else if (data.type === 'plan') {
        const pData = data.plan || data;
        setPlan(pData); setDemoMode(data.demo_mode || false);
        setHistory(prev => {
          const filtered = prev.filter(h => h.query !== originalQuery);
          return [{ query: originalQuery, plan: pData, messages: messages, id: Date.now() }, ...filtered];
        });
        setMessages(prev => [...prev, { role: 'agent', content: "Here is your verified action plan. Scroll down to view the dashboard!" }]);
      }
    } catch (error) {
      setErrorMsg(error.response?.data?.detail || "Failed to connect to the AI Service.");
    } finally {
      setLoading(false);
    }
  };"""

code = re.sub(
    r"  const handleFormSubmit = async \(.*?\}\n\s*\};\n",
    new_handle_form_submit + "\n",
    code,
    flags=re.DOTALL
)

# 4. Replace the old isForm rendering with the dynamic one
old_is_form_regex = r"\{msg\.isForm \? \(\n\s*<div style=\{\{display: 'flex', flexDirection: 'column', gap: '12px'\}\}>.*?\n\s*\) : \("
new_is_form = """{msg.isForm ? (
                          <DynamicFormWidget msg={msg} onSubmit={(data) => handleFormSubmit(data)} />
                        ) : ("""

code = re.sub(old_is_form_regex, new_is_form, code, flags=re.DOTALL)

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Dynamic form UI fully injected!")

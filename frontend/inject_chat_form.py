import re

with open("src/App.jsx", "r") as f:
    code = f.read()

# 1. Add state for the form
state_injection = """  const [formApplicant, setFormApplicant] = useState('Indian Citizen');
  const [formLocation, setFormLocation] = useState('Andhra Pradesh');
"""
code = code.replace("const [input, setInput] = useState('');", "const [input, setInput] = useState('');\n" + state_injection)

# 2. Update handleSubmit to intercept the first query and show the form
handle_submit_start = """  const handleSubmit = async (e, chipText = null) => {
    if (e) e.preventDefault();
    const queryText = chipText || input;
    if (!queryText.trim()) return;
    if (currentPage !== 'chat') setCurrentPage('chat');
    const userMsg = { role: 'user', content: queryText };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    if (!chipText) setInput('');

    // INTERCEPT FIRST MESSAGE FOR THE FORM WIDGET
    if (messages.length === 0 || (messages.length === 1 && messages[0].role === 'agent')) {
       setLoading(true);
       setTimeout(() => {
           setMessages([...newMessages, {
               role: 'agent',
               content: "Great! To give you the right guidance, I need a few details.",
               isForm: true,
               originalQuery: queryText
           }]);
           setLoading(false);
       }, 500);
       return;
    }

    setLoading(true); setErrorMsg(''); setPlan(null);
"""
# Replace the original handleSubmit start
code = re.sub(
    r"  const handleSubmit = async \(e, chipText = null\) => \{.*?\n\s*setLoading\(true\); setErrorMsg\(''\); setPlan\(null\);",
    handle_submit_start,
    code,
    flags=re.DOTALL
)

# 3. Add handleFormSubmit function inside App
handle_form_submit = """
  const handleFormSubmit = async (originalQuery) => {
    const finalQuery = `${originalQuery}. Applicant Type: ${formApplicant}. Location: ${formLocation}.`;
    
    // Remove the form from UI (change it to a regular bubble, or just add the next user step)
    // Actually, we can leave the form in history but mark it completed, or just replace it with text.
    setMessages(prev => {
        const copy = [...prev];
        const lastMsg = copy[copy.length - 1];
        if (lastMsg.isForm) {
           lastMsg.isForm = false;
           lastMsg.content = `Great! To give you the right guidance, I need a few details. \\n\\n**Selected:** ${formApplicant}, ${formLocation}`;
        }
        return copy;
    });

    setLoading(true); setErrorMsg(''); setPlan(null);
    try {
      const response = await axios.post(`${API_URL}/api/plan`, { messages: [...messages, {role: 'user', content: finalQuery}], state: formLocation });
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
  };
"""

code = code.replace("  const handleAuth = async (e) => {", handle_form_submit + "\n  const handleAuth = async (e) => {")


# 4. Replace isFlowWidget rendering with isForm rendering!
# We will match from msg.isFlowWidget ? ( down to ) : (
flow_widget_regex = r"\{msg\.isFlowWidget \? \(.*?\n\s*\) : \("
new_form_widget = """{msg.isForm ? (
                          <div style={{display: 'flex', flexDirection: 'column', gap: '12px'}}>
                            <div className="bubble">Great! To give you the right guidance, I need a few details.</div>
                            <div className="chat-form-card" style={{background: 'white', border: '1px solid #e2e8f0', padding: '20px', borderRadius: '12px', width: '320px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)'}}>
                              <h4 style={{margin: '0 0 16px 0', fontSize: '1rem', color: '#0f172a'}}>Please select:</h4>
                              
                              <div style={{marginBottom: '16px'}}>
                                <label style={{display: 'block', fontSize: '0.85rem', color: '#64748b', marginBottom: '6px'}}>Applicant type</label>
                                <select value={formApplicant} onChange={e => setFormApplicant(e.target.value)} style={{width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #cbd5e1', outline: 'none', background: 'white', cursor: 'pointer', appearance: 'auto'}}>
                                  <option>Indian Citizen</option>
                                  <option>NRI</option>
                                  <option>Foreign National</option>
                                </select>
                              </div>
                              
                              <div style={{marginBottom: '24px'}}>
                                <label style={{display: 'block', fontSize: '0.85rem', color: '#64748b', marginBottom: '6px'}}>State / Location</label>
                                <select value={formLocation} onChange={e => setFormLocation(e.target.value)} style={{width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #cbd5e1', outline: 'none', background: 'white', cursor: 'pointer', appearance: 'auto'}}>
                                  <option>Andhra Pradesh</option>
                                  <option>Telangana</option>
                                  <option>Maharashtra</option>
                                  <option>Delhi</option>
                                </select>
                              </div>

                              <button onClick={() => handleFormSubmit(msg.originalQuery)} style={{width: '100%', background: '#2563eb', color: 'white', border: 'none', padding: '12px', borderRadius: '8px', fontWeight: '600', cursor: 'pointer', transition: 'background 0.2s'}}>
                                Continue
                              </button>
                            </div>
                          </div>
                        ) : ("""

code = re.sub(flow_widget_regex, new_form_widget, code, flags=re.DOTALL)


with open("src/App.jsx", "w") as f:
    f.write(code)

print("Injected form widget!")

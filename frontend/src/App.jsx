import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = 'https://naviq-backend.onrender.com';

const DB_SERVICES = [
  { id: 'passport', title: 'Apply for Passport', desc: 'New passport, renewal, documents, fees and more.', icon: '🛂', bg: 'bg-blue', category: 'Travel' },
  { id: 'pan_card', title: 'PAN Card', desc: 'Apply for new PAN card or corrections.', icon: '🪪', bg: 'bg-blue', category: 'Identity & Documents' },
  { id: 'aadhaar_update', title: 'Aadhaar Services', desc: 'Update details, download, correction and more.', icon: '🛡️', bg: 'bg-red', category: 'Identity & Documents' },
  { id: 'driving_licence', title: 'Driving License', desc: 'New license, renewal, address update.', icon: '🚗', bg: 'bg-red', category: 'Travel' },
  { id: 'voter_id', title: 'Voter ID Card', desc: 'New registration, correction and download.', icon: '🗳️', bg: 'bg-blue', category: 'Identity & Documents' },
  { id: 'ration_card', title: 'Ration Card', desc: 'Apply, add members, check status.', icon: '📜', bg: 'bg-orange', category: 'Benefits' },
  { id: 'birth_certificate', title: 'Birth Certificate', desc: 'New certificate, delayed registration, corrections.', icon: '👶', bg: 'bg-green', category: 'Identity & Documents' },
  { id: 'income_certificate', title: 'Income Certificate', desc: 'Apply for income certificate for scholarships and benefits.', icon: '💰', bg: 'bg-purple', category: 'Benefits' },
  { id: 'caste_certificate', title: 'Caste Certificate', desc: 'SC/ST/OBC certification and renewal.', icon: '🎓', bg: 'bg-yellow', category: 'Identity & Documents' },
  { id: 'residence_certificate', title: 'Residence / Nativity', desc: 'Proof of address and domicile certificate.', icon: '🏠', bg: 'bg-green', category: 'Identity & Documents' }
];


const GOVERNMENT_UPDATES = [
  { id: 1, date: "Oct 08, 2026", title: "Aadhaar Free Update Deadline Extended", desc: "UIDAI has extended the free document update facility. Check the official portal to update proof of identity and address.", link: "https://uidai.gov.in" },
  { id: 2, date: "Oct 05, 2026", title: "Passport Seva Portal Maintenance", desc: "The Passport Seva portal will be down from 8:00 PM Saturday to 6:00 AM Sunday for scheduled maintenance.", link: "https://passportindia.gov.in" },
  { id: 3, date: "Oct 01, 2026", title: "New Driving Licence Rules Implemented", desc: "Applicants can now take driving tests at certified private driving schools instead of solely at government RTOs.", link: "https://parivahan.gov.in" }
];

const FILTERS = ['All', 'Identity & Documents', 'Education', 'Business', 'Benefits', 'Travel', 'Others'];


const DynamicFormWidget = ({ msg, onSubmit }) => {
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
};

function App() {
  const [currentPage, setCurrentPage] = useState('landing');
  const [authMode, setAuthMode] = useState('signin');
  
  const [input, setInput] = useState('');
  const [formApplicant, setFormApplicant] = useState('Indian Citizen');
  const [formLocation, setFormLocation] = useState('Andhra Pradesh');

  const [messages, setMessages] = useState(() => {
    try { return JSON.parse(localStorage.getItem('naviq_messages')) || []; } catch { return []; }
  });
  const [plan, setPlan] = useState(() => {
    try { return JSON.parse(localStorage.getItem('naviq_plan')) || null; } catch { return null; }
  });
  const [history, setHistory] = useState(() => {
    try { return JSON.parse(localStorage.getItem('naviq_history')) || []; } catch { return []; }
  });
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [language, setLanguage] = useState('en-IN');
  const [stateName, setStateName] = useState('Andhra Pradesh');
  const [errorMsg, setErrorMsg] = useState('');
  const [demoMode, setDemoMode] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeFilter, setActiveFilter] = useState('All');

  const [wizardStep, setWizardStep] = useState(1);
  
  const [authEmail, setAuthEmail] = useState('');
  const [authPassword, setAuthPassword] = useState('');
  const [authConfirmPassword, setAuthConfirmPassword] = useState('');
  const [authError, setAuthError] = useState('');
  const [currentUser, setCurrentUser] = useState(() => localStorage.getItem('naviq_user') || null);

  const chatEndRef = useRef(null);
  const recognitionRef = useRef(null);

  useEffect(() => {
    localStorage.setItem('naviq_messages', JSON.stringify(messages));
    localStorage.setItem('naviq_plan', JSON.stringify(plan));
    localStorage.setItem('naviq_history', JSON.stringify(history));
  }, [messages, plan, history]);

  useEffect(() => {
    if (currentPage === 'chat') {
      chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading, currentPage]);

  const startNewChat = () => {
    setMessages([]);
    setPlan(null);
    setInput('');
    setErrorMsg('');
    localStorage.removeItem('naviq_messages');
    localStorage.removeItem('naviq_plan');
    setCurrentPage('chat');
  };

  const loadHistoryItem = (item) => {
    setMessages(item.messages || [{ role: 'user', content: item.query }]);
    setPlan(item.plan);
    setErrorMsg('');
    setCurrentPage('chat');
  };

  const deleteHistoryItem = (e, id) => {
    e.stopPropagation();
    setHistory(history.filter(h => h.id !== id));
  };

  const handleVoiceInput = () => {
    if (isListening) {
      if (recognitionRef.current) recognitionRef.current.stop();
      return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return alert("Your browser does not support Voice Recognition.");
    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;
    recognition.lang = language;
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.onstart = () => setIsListening(true);
    recognition.baseInput = input;
    recognition.onresult = (event) => {
      let transcript = '';
      for (let i = 0; i < event.results.length; ++i) transcript += event.results[i][0].transcript;
      setInput((recognition.baseInput ? recognition.baseInput + ' ' : '') + transcript);
    };
    recognition.onerror = () => setIsListening(false);
    recognition.onend = () => setIsListening(false);
    recognition.start();
  };

  const handleSubmit = async (e, chipText = null) => {
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
      } else if (data.type === 'unsupported') {
        setMessages([...newMessages, { role: 'agent', content: data.text, available_services: data.available_services }]);
      } else if (data.type === 'question') {
        setMessages([...newMessages, { role: 'agent', content: data.text }]);
      } else if (data.type === 'plan') {
        const pData = data.plan || data;
        setPlan(pData); setDemoMode(data.demo_mode || false);
        setHistory(prev => {
          const filtered = prev.filter(h => h.query !== newMessages[0].content);
          return [{ query: newMessages[0].content, plan: pData, messages: newMessages, id: Date.now() }, ...filtered];
        });
        setMessages([...newMessages, { role: 'agent', content: "Here is your verified action plan. Scroll down to view the dashboard!" }]);
      }
    } catch (error) {
      setErrorMsg(error.response?.data?.detail || "Failed to connect to the AI Service.");
    } finally {
      setLoading(false);
    }
  };


  const handleFormSubmit = async (formData) => {
    const selections = Object.entries(formData).map(([k, v]) => `${k}: ${v}`).join(', ');
    const finalQuery = `Here are my details. ${selections}`;
    
    let originalQuery = "";
    
    setMessages(prev => {
        const copy = [...prev];
        const lastMsg = copy[copy.length - 1];
        if (lastMsg.isForm) {
           originalQuery = lastMsg.originalQuery;
           lastMsg.isForm = false;
           lastMsg.content = `${lastMsg.content} 

**Selected:** ${selections}`;
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
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    setAuthError('');
    if (authMode === 'signup' && authPassword !== authConfirmPassword) return setAuthError("Passwords do not match");
    try {
      const endpoint = authMode === 'signup' ? '/api/signup' : '/api/login';
      const res = await axios.post(`${API_URL}${endpoint}`, { email: authEmail, password: authPassword });
      localStorage.setItem('naviq_token', res.data.token);
      localStorage.setItem('naviq_user', res.data.email);
      setCurrentUser(res.data.email);
      setCurrentPage('landing');
    } catch (err) {
      setAuthError(err.response?.data?.detail || "Authentication failed");
    }
  };

  const toggleStep = (id) => {
    setPlan(prev => {
      if (!prev || !prev.steps) return prev;
      const newPlan = { ...prev, steps: prev.steps.map(s => s.id === id ? { ...s, status: s.status === 'completed' ? 'pending' : 'completed' } : s) };
      
      // Sync back to history so progress is saved
      setHistory(prevHistory => prevHistory.map(h => 
        h.query === newPlan.query || h.plan?.service?.id === newPlan.service?.id 
          ? { ...h, plan: newPlan } 
          : h
      ));
      
      return newPlan;
    });
  };

  const toggleDoc = (idx) => {
    setPlan(prev => {
      if (!prev || !prev.documents) return prev;
      const newDocs = [...prev.documents];
      newDocs[idx] = { ...newDocs[idx], have: !newDocs[idx].have };
      const newPlan = { ...prev, documents: newDocs };
      
      // Sync back to history
      setHistory(prevHistory => prevHistory.map(h => 
        h.query === newPlan.query || h.plan?.service?.id === newPlan.service?.id 
          ? { ...h, plan: newPlan } 
          : h
      ));
      
      return newPlan;
    });
  };

  const isStepLocked = (step) => {
    if (!step.depends_on || step.depends_on.length === 0) return false;
    return step.depends_on.some(depId => {
      const depStep = plan.steps.find(s => s.id === depId);
      return depStep && depStep.status !== 'completed';
    });
  };

  const TopNav = ({ isLanding = false }) => {
    const [showDropdown, setShowDropdown] = useState(false);
    return (
      <nav className={`top-nav ${isLanding ? 'landing' : ''}`}>
        <div className="logo" style={{cursor: 'pointer'}} onClick={() => setCurrentPage('landing')}>
          <div className="logo-icon">N</div> Naviq
        </div>
        <div className="nav-links">
          <a className={currentPage === 'landing' ? 'active' : ''} onClick={() => setCurrentPage('landing')}>Home</a>
          <a className={currentPage === 'chat' ? 'active' : ''} onClick={() => setCurrentPage('chat')}>Dashboard</a>
        </div>
        <div className="nav-actions">
          {demoMode && !isLanding && <span className="badge-demo">Demo Mode</span>}
          <select className="lang-select" value={language} onChange={(e) => setLanguage(e.target.value)}>
            <option value="en-IN">EN</option><option value="te-IN">TE</option><option value="hi-IN">HI</option>
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
                  <div style={{padding: '8px', fontSize: '0.9rem', color: '#0f172a', cursor: 'pointer', fontWeight: 500, display: 'flex', alignItems: 'center', gap: '8px'}} 
                       onClick={() => { setShowDropdown(false); setCurrentPage('profile'); }}>
                    <span>👤 Profile</span>
                  </div>
                  <div style={{padding: '8px', fontSize: '0.9rem', color: '#ef4444', cursor: 'pointer', fontWeight: 500, display: 'flex', alignItems: 'center', gap: '8px'}} 
                       onClick={() => {
                          setShowDropdown(false);
                          localStorage.removeItem('naviq_token');
                          localStorage.removeItem('naviq_user');
                          setCurrentUser(null);
                          setCurrentPage('landing');
                       }}>
                    <span>🚪 Log Out</span>
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
    );
  };


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

  // RENDER BASED ON PAGE
  if (currentPage === 'auth') {
    return (
      <div className="app-container">
        <TopNav isLanding={true} />
        <div className="auth-page">
          <form className="auth-card" onSubmit={handleAuth}>
            <h2 className="auth-title">{authMode === 'signin' ? 'Sign In to Naviq' : 'Create an Account'}</h2>
            {authError && <div style={{color: '#ef4444', fontSize: '0.9rem', textAlign: 'center'}}>{authError}</div>}
            <input type="email" placeholder="Email address" className="auth-input" value={authEmail} onChange={e => setAuthEmail(e.target.value)} required />
            <input type="password" placeholder="Password" className="auth-input" value={authPassword} onChange={e => setAuthPassword(e.target.value)} required />
            {authMode === 'signup' && (
              <input type="password" placeholder="Confirm Password" className="auth-input" value={authConfirmPassword} onChange={e => setAuthConfirmPassword(e.target.value)} required />
            )}
            <button type="submit" className="auth-btn">{authMode === 'signin' ? 'Sign In' : 'Sign Up'}</button>
            <div className="auth-toggle">
              {authMode === 'signin' ? (
                <>Don't have an account? <span onClick={() => {setAuthMode('signup'); setAuthError('');}}>Sign Up</span></>
              ) : (
                <>Already have an account? <span onClick={() => {setAuthMode('signin'); setAuthError('');}}>Sign In</span></>
              )}
            </div>
          </form>
        </div>
      </div>
    );
  }

  if (currentPage === 'profile') {
    return (
      <div className="app-container" style={{overflowY: 'auto'}}>
        <TopNav />
        <div className="main-area">
          <Sidebar />
          
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
                    <span style={{color: '#64748b', fontWeight: 600}}>Procedures Saved:</span>
                    <span style={{color: '#0f172a', fontWeight: 500}}>{history.length}</span>
                  </div>
                </div>
                <button 
                  onClick={() => { localStorage.removeItem('naviq_token'); localStorage.removeItem('naviq_user'); setCurrentUser(null); setCurrentPage('landing'); }}
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

  if (currentPage === 'landing') {
    return (
      <div className="app-container" style={{overflowY: 'auto'}}>
        <div className="landing-page">
          <TopNav isLanding={true} />
          <main className="hero-section">
            <div className="hero-content">
              <div className="hero-pill">Your Guide to Government Services</div>
              <h1 className="hero-title">Turn your goals into step-by-step action plans.</h1>
              <p className="hero-subtitle">Naviq helps you navigate government procedures with clear steps, official sources and smart reminders.</p>
              <form onSubmit={handleSubmit} className="hero-search-bar">
                <span style={{color: '#2563eb', fontSize: '1.2rem', marginRight:'8px'}}>✨</span>
                <input type="text" placeholder="e.g. I want to apply for a passport" value={input} onChange={(e) => setInput(e.target.value)} />
                <button type="submit" className="hero-search-btn">→</button>
              </form>
              <div className="hero-suggestions">
                <span style={{color: '#64748b', fontSize: '0.9rem'}}>Try these:</span>
                <button className="suggestion-pill" onClick={() => handleSubmit(null, "Apply for Passport")}>Apply for Passport</button>
                <button className="suggestion-pill" onClick={() => handleSubmit(null, "Income Certificate")}>Get a Certificate</button>
                <button className="suggestion-pill" onClick={() => handleSubmit(null, "Apply for PAN Card")}>Apply for PAN Card</button>
                <button className="suggestion-pill" onClick={() => handleSubmit(null, "Driving Licence")}>Driving Licence</button>
              </div>
            </div>
            <div className="hero-image"><img src="/hero.jpg" alt="Illustration" /></div>
          </main>
          <section className="features-section">
            <div className="feature-card"><div className="feature-icon blue">🛡️</div><h3>Official Sources</h3><p>Verified links to government websites</p></div>
            <div className="feature-card"><div className="feature-icon blue">📋</div><h3>Step-by-Step Guidance</h3><p>Clear and organized procedures</p></div>
            <div className="feature-card"><div className="feature-icon green">☑️</div><h3>Task Tracking</h3><p>Keep track of your progress</p></div>
            <div className="feature-card"><div className="feature-icon purple">⏰</div><h3>Smart Reminders</h3><p>Never miss a deadline</p></div>
            <div className="feature-card"><div className="feature-icon blue">🗣️</div><h3>Multiple Languages</h3><p>Available in English, Hindi, Telugu</p></div>
          </section>

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

  const completedSteps = plan?.steps?.filter(s => s.status === 'completed').length || 0;
  const totalSteps = plan?.steps?.length || 1;
  const progressDeg = (completedSteps / totalSteps) * 360;
  
  return (
    <div className="app-container">
      <TopNav />
      <div className="main-area">
        <Sidebar />

        <div className="content-wrapper">
          <div className="content-inner">
            {errorMsg && <div className="error-banner">⚠️ {errorMsg}</div>}

            <div className="chat-container">
              <div className="chat-header">
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                  <div>
                    <h2>Chat with Naviq</h2>
                    <p>Tell me what you want to do. I'll guide you step by step.</p>
                  </div>
                  
                </div>
                <div style={{marginTop: '12px', display: 'flex', gap: '12px'}}>
                  <select className="state-select" value={stateName} onChange={(e) => setStateName(e.target.value)}>
                    <option value="Andhra Pradesh">Andhra Pradesh</option><option value="Telangana">Telangana</option><option value="Maharashtra">Maharashtra</option><option value="Delhi">Delhi</option>
                  </select>
                </div>
              </div>
              
              
                  <div className="chat-history">
                    {(messages || []).length === 0 ? (
                      <div className="msg-row agent">
                        <div className="avatar agent">N</div>
                        <div className="bubble">Hi! I'm Naviq. What would you like to do today? Try: "I want to apply for a passport."</div>
                      </div>
                    ) : (
                      (messages || []).map((msg, idx) => (
                        <div key={idx} className={`msg-row ${msg.role}`}>
                          {msg.role === 'agent' && <div className="avatar agent">N</div>}
                          <div style={{display:'flex', flexDirection:'column', alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start'}}>
                            {msg.isForm ? (
                          <DynamicFormWidget msg={msg} onSubmit={(data) => handleFormSubmit(data)} />
                        ) : (
                          <div className="bubble">{msg.content}</div>
                        )}
                            {msg.available_services && (
                              <div style={{marginTop:'8px', display:'flex', gap:'8px', flexWrap:'wrap'}}>
                                {msg.available_services.map(s => <button key={s} className="suggestion-pill" onClick={() => handleSubmit(null, s)}>{s}</button>)}
                              </div>
                            )}
                          </div>
                        </div>
                      ))
                    )}
                    <div ref={chatEndRef} />
                  </div>

                  <form className="chat-input-area" onSubmit={handleSubmit} style={{padding: '24px', background: '#f8fafc', borderTop: 'none', display: 'flex', justifyContent: 'center'}}>
                    <div className="input-box" style={{maxWidth: '800px', width: '100%', background: 'white', border: '1px solid #e2e8f0', borderRadius: '30px', padding: '8px 8px 8px 20px', display: 'flex', alignItems: 'center', gap: '12px', boxShadow: '0 2px 10px rgba(0,0,0,0.02)'}}>
                      <div style={{color: '#64748b', display: 'flex', alignItems: 'center'}}>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path></svg>
                      </div>
                      <input type="text" className="input-field" placeholder="Type your message..." value={input} onChange={(e) => setInput(e.target.value)} disabled={loading} style={{flex: 1, border: 'none', outline: 'none', fontSize: '1rem', padding: '10px 0'}} />
                      <button type="submit" className="send-btn" disabled={loading} style={{background: '#2563eb', color: 'white', border: 'none', width: '40px', height: '40px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', transition: 'background 0.2s'}}>
                        {loading ? '...' : <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>}
                      </button>
                    </div>
                  </form>
                
            </div>

            {plan && plan.service && (
              <div className="plan-dashboard">
                <div className="plan-header-card">
                  <div className="plan-title">
                    <h1>{plan.service.name}</h1>
                    <p>Get your procedure done with a clear, step-by-step plan.</p>
                  </div>
                  <div className="plan-actions">
                    <div className="progress-widget" style={{'--p': `${progressDeg}deg`}}>
                      <div className="circle-progress"><div className="circle-inner">{completedSteps}/{totalSteps}</div></div>
                    </div>
                  </div>
                </div>

                <div style={{gridColumn: '1 / -1'}}>
                  {plan.prerequisite_services?.length > 0 && (
                    <div className="prereq-alert">
                      <strong>⚠️ Missing Prerequisites:</strong> You need to complete these first:
                      <ul style={{marginLeft: '20px', marginTop: '5px'}}>
                        {(plan.prerequisite_services || []).map((ps, i) => <li key={i}>{ps.name} - {ps.reason}</li>)}
                      </ul>
                    </div>
                  )}
                </div>

                <div style={{display: 'flex', flexDirection: 'column', gap: '24px'}}>
                  <div className="card">
                    <div className="card-title">Overview & Steps<span style={{fontSize:'0.85rem', color:'#64748b', fontWeight:'400'}}>{completedSteps} of {totalSteps} completed</span></div>
                    <div className="timeline">
                      {(plan.steps || []).map((step, idx) => {
                        const locked = isStepLocked(step);
                        const completed = step.status === 'completed';
                        return (
                          <div key={step.id} className={`timeline-step ${completed ? 'completed' : ''} ${locked ? 'locked' : ''}`} onClick={() => !locked && toggleStep(step.id)}>
                            <div className="timeline-line"></div>
                            <div className="step-indicator">{completed ? '✓' : idx + 1}</div>
                            <div className="step-content-box">
                              <div className="step-title">{locked ? '🔒 ' : ''}{step.text}</div>
                              <div className="step-meta">
                                <span>Evidence: {step.source.title}</span>
                                <a href={step.source.url} target="_blank" rel="noreferrer" className="verify-link" onClick={e => e.stopPropagation()}>Verify ↗</a>
                              </div>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                </div>

                <div style={{display: 'flex', flexDirection: 'column', gap: '24px'}}>
                  <div className="card">
                    <div className="card-title">Required Documents</div>
                    <div>
                      {plan.documents?.map((doc, idx) => (
                        <div key={idx} className="doc-row">
                          <input type="checkbox" className="custom-checkbox" checked={doc.have} onChange={() => toggleDoc(idx)} />
                          <div className="doc-details">
                            <h4>{doc.name}</h4><p>{doc.how_to_get}</p>
                            {doc.blocked_by_service && <p style={{color: '#ef4444', marginTop:'4px'}}>⚠️ Requires {doc.blocked_by_service}</p>}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="card">
                    <div className="card-title">
                      Reminders
                      <div style={{display: 'flex', gap: '16px'}}>
                        <a style={{fontSize:'0.85rem', color:'#f59e0b', cursor:'pointer', fontWeight: 600}} onClick={async () => {
                          const phone = window.prompt("Enter your phone number to receive progress via SMS:");
                          if (!phone) return;
                          alert('Dispatching SMS... Please check the terminal logs!');
                          let body = `Naviq Progress: ${plan.service.name}\n${completedSteps}/${totalSteps} steps done.\nReminders: ` + (plan.reminders ? plan.reminders.length : 0);
                          try {
                            await axios.post(`${API_URL}/api/sms`, { phone, message: body });
                            alert('SMS successfully dispatched to ' + phone + '!');
                          } catch(err) {
                            alert('Error sending SMS.');
                          }
                        }}>📱 SMS Alerts</a>
                        <a style={{fontSize:'0.85rem', color:'#10b981', cursor:'pointer', fontWeight: 600}} onClick={async () => {
                          if (!currentUser) return alert('Please sign in first to send emails.');
                          alert('Dispatching email... Please check the terminal logs!');
                          let body = `Naviq Progress Report: ${plan.service.name}\n\n`;
                          body += `Progress: ${completedSteps} of ${totalSteps} steps completed.\n\n`;
                          body += `Reminders:\n` + (plan.reminders ? (plan.reminders || []).map(r => `- ${r.text} (${r.time})`).join('\n') : 'No reminders.');
                          try {
                            await axios.post(`${API_URL}/api/email`, { email: currentUser, subject: `Naviq: ${plan.service.name} Updates`, body });
                            alert('Email successfully dispatched to ' + currentUser + '!');
                          } catch(err) {
                            alert('Error sending email.');
                          }
                        }}>📧 Email Progress</a>
                        <a style={{fontSize:'0.85rem', color:'#2563eb', cursor:'pointer'}} onClick={() => {
                          let icsContent = "BEGIN:VCALENDAR\nVERSION:2.0\n";
                          plan.reminders.forEach((r, i) => { icsContent += `BEGIN:VEVENT\nSUMMARY:${r.text}\nDTSTART:${new Date(Date.now() + 86400000).toISOString().replace(/[-:]/g, '').split('.')[0]}Z\nEND:VEVENT\n`; });
                          icsContent += "END:VCALENDAR";
                          const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([icsContent], { type: 'text/calendar' })); a.download = 'naviq.ics'; a.click();
                        }}>Download .ics</a>
                      </div>
                    </div>
                    <div>
                      {plan.reminders?.map((r, i) => (
                        <div key={i} className="reminder-item"><div className="reminder-icon">🔔</div><div><div className="reminder-text">{r.text}</div><div className="reminder-time">{r.time}</div></div></div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}


export default App;


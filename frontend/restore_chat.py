import re

with open("src/App.jsx", "r") as f:
    code = f.read()

# I need to find the WizardFlow block I injected
# and the place where I injected it in the render logic.

old_render = """<div className="chat-container" style={{background: '#f8fafc', padding: '20px', border: 'none'}}>
              {!plan ? <WizardFlow /> : null}
            </div>"""

new_render = """<div className="chat-container">
              <div className="chat-header">
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                  <div>
                    <h2>Chat with Naviq</h2>
                    <p>Tell me what you want to do. I'll guide you step by step.</p>
                  </div>
                  <button onClick={() => setWizardStep(1)} style={{padding: '8px 16px', background: '#2563eb', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '0.9rem', fontWeight: 'bold'}}>
                    Open Wizard
                  </button>
                </div>
                <div style={{marginTop: '12px', display: 'flex', gap: '12px'}}>
                  <select className="state-select" value={stateName} onChange={(e) => setStateName(e.target.value)}>
                    <option value="Andhra Pradesh">Andhra Pradesh</option><option value="Telangana">Telangana</option><option value="Maharashtra">Maharashtra</option><option value="Delhi">Delhi</option>
                  </select>
                </div>
              </div>
              
              {!plan && wizardStep > 0 ? (
                <div style={{margin: '20px 0'}}>
                   <div style={{display: 'flex', justifyContent: 'flex-end', marginBottom: '10px'}}><button onClick={() => setWizardStep(0)} style={{background: 'transparent', color: '#64748b', border: 'none', cursor: 'pointer', fontSize: '0.9rem'}}>✕ Close Wizard</button></div>
                   <WizardFlow />
                </div>
              ) : (
                <>
                  <div className="chat-history">
                    {messages.length === 0 ? (
                      <div className="msg-row agent">
                        <div className="avatar agent">N</div>
                        <div className="bubble">Hi! I'm Naviq. What would you like to do today? Try: "I want to apply for a passport." or click "Open Wizard".</div>
                      </div>
                    ) : (
                      messages.map((msg, idx) => (
                        <div key={idx} className={`msg-row ${msg.role}`}>
                          {msg.role === 'agent' && <div className="avatar agent">N</div>}
                          <div style={{display:'flex', flexDirection:'column', alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start'}}>
                            <div className="bubble">{msg.content}</div>
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

                  <form className="chat-input-area" onSubmit={handleSubmit}>
                    <div className="input-wrapper">
                      <input type="text" placeholder="Type your request here..." value={input} onChange={(e) => setInput(e.target.value)} disabled={loading} />
                      <button type="button" className="mic-btn" onClick={startListening} title="Voice Input">🎤</button>
                      <button type="submit" disabled={loading}>{loading ? '...' : '→'}</button>
                    </div>
                  </form>
                </>
              )}
            </div>"""

if old_render in code:
    code = code.replace(old_render, new_render)
    with open("src/App.jsx", "w") as f:
        f.write(code)
    print("Chat UI successfully restored and Wizard integrated.")
else:
    print("Could not find the target string to replace.")


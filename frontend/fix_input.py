import re

with open("src/App.jsx", "r") as f:
    code = f.read()

old_input = """<div className="input-wrapper">
                      <input type="text" placeholder="Type your request here..." value={input} onChange={(e) => setInput(e.target.value)} disabled={loading} />
                      <button type="button" className="mic-btn" onClick={handleVoiceInput} title="Voice Input">🎤</button>
                      <button type="submit" disabled={loading}>{loading ? '...' : '→'}</button>
                    </div>"""

new_input = """<div className="input-box">
                      <input type="text" className="input-field" placeholder="Type your request here..." value={input} onChange={(e) => setInput(e.target.value)} disabled={loading} />
                      <button type="button" className={`icon-btn ${isListening ? 'active' : ''}`} onClick={handleVoiceInput} title="Voice Input">🎤</button>
                    </div>
                    <button type="submit" className="send-btn" disabled={loading}>{loading ? '...' : '→'}</button>"""

code = code.replace(old_input, new_input)

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Input fixed!")

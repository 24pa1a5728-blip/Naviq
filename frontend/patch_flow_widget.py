import re

# 1. Update App.jsx to render the FlowWidget and add it to the message payload
with open("src/App.jsx", "r") as f:
    app_code = f.read()

# The submit handler currently does:
# setMessages([...newMessages, { role: 'agent', content: "Here is your verified action plan. Scroll down to view the dashboard!" }]);

new_payload = """
        setMessages([...newMessages, { 
          role: 'agent', 
          isFlowWidget: true, 
          serviceName: data.service.name,
          stateName: stateName,
          totalSteps: data.steps.length
        }]);
"""
app_code = re.sub(r"setMessages\(\[\.\.\.newMessages, \{ role: 'agent', content: \"Here is your verified action plan[^\}]+\} \]\);", new_payload.strip(), app_code)


# Inject the FlowWidget rendering into the chat map
# Currently:
# <div className="bubble">{msg.content}</div>

flow_widget_ui = """
                        {msg.isFlowWidget ? (
                          <div className="flow-widget">
                            <div className="fw-header">
                              <h3>Proposed {msg.serviceName} Flow</h3>
                              <p>Illustrative interface for your existing process</p>
                            </div>
                            
                            <div className="fw-stepper">
                              <div className="fw-step active">1</div>
                              <div className="fw-line active-line"></div>
                              <div className="fw-step">2</div>
                              <div className="fw-line"></div>
                              <div className="fw-step">3</div>
                              <div className="fw-line"></div>
                              <div className="fw-step">4</div>
                              <div className="fw-line"></div>
                              <div className="fw-step">{msg.totalSteps >= 5 ? msg.totalSteps : 5}</div>
                            </div>

                            <div className="fw-content">
                              <h4>Step 1 of {msg.totalSteps} — Applicant details</h4>
                              <div style={{color: '#10b981', marginBottom: '16px'}}>
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"></circle><path d="M9 12l2 2 4-4"></path></svg>
                              </div>
                              
                              <h4>Step {msg.totalSteps} — Plan created</h4>
                              <p>Your selected application type is fresh application; applicant category: adult; region: {msg.stateName}.</p>
                              <p className="fw-disclaimer">This is a UI demonstration only; it does not verify eligibility or submit an application.</p>
                            </div>

                            <div className="fw-actions">
                              <button className="fw-btn-back">Back</button>
                              <button className="fw-btn-primary" onClick={() => { chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }}>Plan implementation</button>
                            </div>
                          </div>
                        ) : (
                          <div className="bubble">{msg.content}</div>
                        )}
"""

app_code = app_code.replace('<div className="bubble">{msg.content}</div>', flow_widget_ui.strip())

with open("src/App.jsx", "w") as f:
    f.write(app_code)


# 2. Add CSS to App.css
css_code = """

/* Flow Widget Styles */
.flow-widget {
  background: #000000;
  border: 1px solid #1f2937;
  border-radius: 12px;
  padding: 24px;
  width: 100%;
  max-width: 550px;
  color: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  box-shadow: 0 4px 20px rgba(0,0,0,0.5);
  margin-top: 8px;
}

.fw-header h3 {
  margin: 0 0 8px 0;
  font-size: 1.15rem;
  font-weight: 600;
  color: #ffffff;
}

.fw-header p {
  margin: 0 0 24px 0;
  font-size: 0.85rem;
  color: #9ca3af;
}

.fw-stepper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.fw-step {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 600;
  color: #ffffff;
}

.fw-step.active {
  background: #2563eb;
}

.fw-line {
  flex: 1;
  height: 2px;
  background: #1f2937;
  margin: 0 8px;
}
.fw-line.active-line {
  background: #2563eb;
}

.fw-content h4 {
  margin: 0 0 8px 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #ffffff;
}

.fw-content p {
  margin: 0 0 16px 0;
  font-size: 0.9rem;
  color: #d1d5db;
  line-height: 1.4;
}

.fw-disclaimer {
  font-size: 0.8rem !important;
  color: #9ca3af !important;
}

.fw-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.fw-btn-back {
  flex: 1;
  background: transparent;
  border: 1px solid #374151;
  color: #ffffff;
  padding: 10px;
  border-radius: 20px;
  font-weight: 500;
  cursor: pointer;
}

.fw-btn-primary {
  flex: 2;
  background: #f3f4f6;
  border: none;
  color: #000000;
  padding: 10px;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
}
"""

with open("src/App.css", "a") as f:
    f.write(css_code)

print("Flow Widget Injected!")

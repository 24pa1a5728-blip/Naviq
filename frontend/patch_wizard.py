import re

with open("src/App.jsx", "r") as f:
    code = f.read()

wizard_code = """
  const [wizardStep, setWizardStep] = useState(1);
  const [wizardData, setWizardData] = useState({
    service: 'Passport',
    appType: 'Fresh passport',
    applicant: 'Adult applicant',
    region: 'Andhra Pradesh'
  });

  const WizardFlow = () => {
    const handleNext = () => setWizardStep(prev => Math.min(prev + 1, 5));
    const handleBack = () => setWizardStep(prev => Math.max(prev - 1, 1));
    
    const generatePlanFromWizard = async () => {
        setLoading(true);
        setErrorMsg('');
        setPlan(null);
        try {
          const query = `I want to apply for a ${wizardData.service}. Type: ${wizardData.appType}. Category: ${wizardData.applicant}. State: ${wizardData.region}.`;
          const response = await axios.post(`${API_URL}/api/plan`, { messages: [{role: 'user', content: query}], state: wizardData.region });
          const data = response.data;
          if (data.type === 'plan') {
            setPlan(data);
            setHistory(prev => [{ query: query, plan: data, messages: [], id: Date.now() }, ...prev]);
          } else {
            setErrorMsg("Could not generate plan for these selections.");
          }
        } catch (error) {
          setErrorMsg(error.response?.data?.detail || "Failed to connect to the AI Service.");
        } finally {
          setLoading(false);
        }
    };

    return (
      <div style={{background: '#000', color: '#fff', padding: '24px', borderRadius: '12px', border: '1px solid #333', maxWidth: '800px', margin: '0 auto', fontFamily: 'sans-serif'}}>
        <h2 style={{margin: '0 0 8px 0', fontSize: '1.4rem', fontWeight: 600}}>Proposed {wizardData.service} Application Flow</h2>
        <p style={{margin: '0 0 24px 0', color: '#a3a3a3', fontSize: '0.9rem'}}>Illustrative interface for your existing process</p>
        
        {/* Progress Bar */}
        <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '32px', position: 'relative'}}>
          <div style={{position: 'absolute', top: '16px', left: '0', right: '0', height: '2px', background: '#333', zIndex: 0}}></div>
          <div style={{position: 'absolute', top: '16px', left: '0', width: `${(wizardStep-1)*25}%`, height: '2px', background: '#2563eb', zIndex: 1, transition: 'width 0.3s'}}></div>
          {[1, 2, 3, 4, 5].map(step => (
            <div key={step} style={{position: 'relative', zIndex: 2, display: 'flex', flexDirection: 'column', alignItems: 'center', width: '40px'}}>
              <div style={{width: '32px', height: '32px', borderRadius: '50%', background: wizardStep >= step ? '#2563eb' : '#000', border: wizardStep >= step ? 'none' : '2px solid #333', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 600, fontSize: '0.9rem'}}>
                {wizardStep > step ? '✓' : step}
              </div>
            </div>
          ))}
        </div>

        {/* Step Content */}
        <div style={{minHeight: '300px'}}>
          {wizardStep === 1 && (
            <div>
              <h3 style={{fontSize: '1.1rem', marginBottom: '16px'}}>Step 1 of 5 — Applicant details</h3>
              <p style={{color: '#a3a3a3', marginBottom: '24px', fontSize: '0.95rem'}}>Tell Naviq about the application you want to make.</p>
              
              <div style={{marginBottom: '20px'}}>
                <label style={{display: 'block', fontWeight: 600, marginBottom: '12px', fontSize: '0.95rem'}}>Application type</label>
                <div style={{display: 'flex', flexDirection: 'column', gap: '12px'}}>
                  <label style={{display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer'}}>
                    <input type="radio" name="appType" checked={wizardData.appType === 'Fresh passport'} onChange={() => setWizardData({...wizardData, appType: 'Fresh passport'})} style={{width: '18px', height: '18px', accentColor: '#2563eb'}} />
                    Fresh passport
                  </label>
                  <label style={{display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer'}}>
                    <input type="radio" name="appType" checked={wizardData.appType === 'Passport re-issue'} onChange={() => setWizardData({...wizardData, appType: 'Passport re-issue'})} style={{width: '18px', height: '18px', accentColor: '#2563eb'}} />
                    Passport re-issue
                  </label>
                </div>
              </div>

              <div style={{marginBottom: '24px'}}>
                <label style={{display: 'block', fontWeight: 600, marginBottom: '12px', fontSize: '0.95rem'}}>Applicant</label>
                <div style={{display: 'flex', flexDirection: 'column', gap: '12px'}}>
                  <label style={{display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer'}}>
                    <input type="radio" name="applicant" checked={wizardData.applicant === 'Adult applicant'} onChange={() => setWizardData({...wizardData, applicant: 'Adult applicant'})} style={{width: '18px', height: '18px', accentColor: '#2563eb'}} />
                    Adult applicant
                  </label>
                  <label style={{display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer'}}>
                    <input type="radio" name="applicant" checked={wizardData.applicant === 'Minor applicant'} onChange={() => setWizardData({...wizardData, applicant: 'Minor applicant'})} style={{width: '18px', height: '18px', accentColor: '#2563eb'}} />
                    Minor applicant
                  </label>
                </div>
              </div>

              <div style={{marginBottom: '20px'}}>
                <label style={{display: 'block', fontWeight: 600, marginBottom: '12px', fontSize: '0.95rem'}}>State or region</label>
                <select value={wizardData.region} onChange={e => setWizardData({...wizardData, region: e.target.value})} style={{width: '100%', padding: '12px', background: '#000', color: '#fff', border: '1px solid #333', borderRadius: '8px', fontSize: '0.95rem', outline: 'none'}}>
                  <option value="Andhra Pradesh">Andhra Pradesh</option>
                  <option value="Telangana">Telangana</option>
                  <option value="Maharashtra">Maharashtra</option>
                  <option value="Delhi">Delhi</option>
                </select>
              </div>
            </div>
          )}

          {wizardStep === 2 && (
            <div>
              <h3 style={{fontSize: '1.1rem', marginBottom: '16px'}}>Step 1 of 5 — Applicant details</h3>
              <h3 style={{fontSize: '1.1rem', marginBottom: '16px'}}>Step 2 — Confirm applicable requirements</h3>
              <p style={{color: '#a3a3a3', lineHeight: 1.6, fontSize: '0.95rem'}}>
                Naviq should use the answers from Step 1 to identify the applicable official checklist. Requirements must be verified before being displayed.
              </p>
            </div>
          )}

          {wizardStep === 3 && (
            <div>
              <h3 style={{fontSize: '1.1rem', marginBottom: '16px'}}>Step 1 of 5 — Applicant details</h3>
              <h3 style={{fontSize: '1.1rem', marginBottom: '16px'}}>Step 3 — Review documents</h3>
              <p style={{color: '#a3a3a3', lineHeight: 1.6, fontSize: '0.95rem'}}>
                Show the official document checklist relevant to the applicant's circumstances. Let the user mark what they have ready.
              </p>
            </div>
          )}

          {wizardStep === 4 && (
            <div>
              <h3 style={{fontSize: '1.1rem', marginBottom: '16px'}}>Step 1 of 5 — Applicant details</h3>
              <h3 style={{fontSize: '1.1rem', marginBottom: '16px'}}>Step 4 — Review action plan</h3>
              <p style={{color: '#a3a3a3', lineHeight: 1.6, fontSize: '0.95rem'}}>
                Display the ordered procedure, prerequisites, and official Passport Seva links for the selected application type.
              </p>
            </div>
          )}

          {wizardStep === 5 && (
            <div>
              <h3 style={{fontSize: '1.1rem', marginBottom: '16px'}}>Step 1 of 5 — Applicant details <span style={{color: '#10b981'}}>✓</span></h3>
              <h3 style={{fontSize: '1.1rem', marginBottom: '16px'}}>Step 5 — Plan created</h3>
              <p style={{color: '#e5e5e5', lineHeight: 1.6, fontSize: '0.95rem', marginBottom: '16px'}}>
                Your selected application type is {wizardData.appType.toLowerCase()}; applicant category: {wizardData.applicant.split(' ')[0].toLowerCase()}; region: {wizardData.region}.
              </p>
              <p style={{color: '#a3a3a3', lineHeight: 1.6, fontSize: '0.95rem'}}>
                This is a UI demonstration only; it does not verify eligibility or submit an application.
              </p>
            </div>
          )}
        </div>

        {/* Navigation Buttons */}
        <div style={{display: 'flex', gap: '16px', marginTop: '32px'}}>
          <button onClick={handleBack} disabled={wizardStep === 1} style={{flex: 1, padding: '14px', background: 'transparent', border: '1px solid #333', color: wizardStep === 1 ? '#555' : '#fff', borderRadius: '24px', fontWeight: 600, cursor: wizardStep === 1 ? 'not-allowed' : 'pointer'}}>
            Back
          </button>
          {wizardStep < 5 ? (
            <button onClick={handleNext} style={{flex: 1, padding: '14px', background: '#fff', border: 'none', color: '#000', borderRadius: '24px', fontWeight: 600, cursor: 'pointer'}}>
              Continue
            </button>
          ) : (
            <button onClick={generatePlanFromWizard} disabled={loading} style={{flex: 1, padding: '14px', background: '#fff', border: 'none', color: '#000', borderRadius: '24px', fontWeight: 600, cursor: 'pointer'}}>
              {loading ? 'Creating...' : 'Plan implementation'}
            </button>
          )}
        </div>
      </div>
    );
  };
"""

# Insert state vars and WizardFlow definition inside App function
# Find where other states are declared (e.g. const [activeFilter, setActiveFilter])
code = re.sub(
    r"(const \[activeFilter, setActiveFilter\] = useState\('All'\);)",
    r"\1\n" + wizard_code,
    code
)

# Now replace the chat UI with the WizardFlow when there is no plan.
# We need to find the chat container in the render block:
chat_ui_regex = r"<div className=\"chat-container\">.*?</div>\s*\{plan && plan\.service && \("

replacement = """<div className="chat-container" style={{background: '#f8fafc', padding: '20px', border: 'none'}}>
              {!plan ? <WizardFlow /> : null}
            </div>

            {plan && plan.service && ("""

code = re.sub(chat_ui_regex, replacement, code, flags=re.DOTALL)

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Wizard successfully injected.")

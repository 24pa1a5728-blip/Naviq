import re

with open("src/App.jsx", "r") as f:
    code = f.read()

error_boundary_code = """
import React from 'react';
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({ errorInfo });
    console.error("ErrorBoundary caught an error", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '20px', background: '#fee2e2', color: '#991b1b', border: '1px solid #f87171', borderRadius: '8px', margin: '20px', fontFamily: 'monospace' }}>
          <h2>Something went wrong in the UI.</h2>
          <details style={{ whiteSpace: 'pre-wrap' }}>
            <summary>Click for error details</summary>
            {this.state.error && this.state.error.toString()}
            <br />
            {this.state.errorInfo && this.state.errorInfo.componentStack}
          </details>
          <button onClick={() => { localStorage.clear(); window.location.reload(); }} style={{ marginTop: '20px', padding: '10px 20px', background: '#dc2626', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            Clear Local Data & Reload
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
"""

# Insert at the top after imports
code = code.replace("import React, { useState, useEffect, useRef } from 'react';", "import React, { useState, useEffect, useRef } from 'react';\n" + error_boundary_code)

# Wrap main export
code = code.replace("export default App;", """
const WrappedApp = () => (
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
);
export default WrappedApp;
""")

with open("src/App.jsx", "w") as f:
    f.write(code)

print("Error Boundary Injected")

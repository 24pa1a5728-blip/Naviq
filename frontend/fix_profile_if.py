import re

with open('src/App.jsx', 'r') as f:
    content = f.read()

# We need to find the bare 'return (' right after 'TopNav' definition and before the profile page content
# The profile page content has '<h2 style={{color: '#0f172a', margin: 0}}>User Profile</h2>'

# We can just look for the place where TopNav ends and insert the if statement.
search_str = """  )};

  return ("""

replace_str = """  )};

  // PROFILE PAGE
  if (currentPage === 'profile') {
    const handleLogout = () => {
      localStorage.removeItem('naviq_token');
      localStorage.removeItem('naviq_user');
      setCurrentUser(null);
      setCurrentPage('landing');
    };

    return ("""

if search_str in content:
    content = content.replace(search_str, replace_str)
    with open('src/App.jsx', 'w') as f:
        f.write(content)
    print("Fixed!")
else:
    print("Could not find the target string. Using regex...")
    # Alternative strategy:
    content = re.sub(
        r"  \)\};\n\n  return \(",
        r"  )};\n\n  // PROFILE PAGE\n  if (currentPage === 'profile') {\n    const handleLogout = () => {\n      localStorage.removeItem('naviq_token');\n      localStorage.removeItem('naviq_user');\n      setCurrentUser(null);\n      setCurrentPage('landing');\n    };\n\n    return (",
        content
    )
    with open('src/App.jsx', 'w') as f:
        f.write(content)
    print("Fallback regex run.")


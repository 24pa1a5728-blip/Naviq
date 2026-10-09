import re

with open("src/App.jsx", "r") as f:
    content = f.read()

# Remove the TopNav Services link
content = re.sub(
    r"<a className=\{currentPage === 'services' \? 'active' : ''\} onClick=\{\(\) => setCurrentPage\('services'\)\}>Services</a>\n\s*",
    "",
    content
)

# Remove the SERVICES PAGE block
# It looks like:
#   if (currentPage === 'services') {
#       ...
#   }
#   if (currentPage === 'landing') {

services_block_regex = r"  if \(currentPage === 'services'\) \{.*?\n  \}\n\n  if \(currentPage === 'landing'\) \{"
content = re.sub(services_block_regex, "  if (currentPage === 'landing') {", content, flags=re.DOTALL)

with open("src/App.jsx", "w") as f:
    f.write(content)


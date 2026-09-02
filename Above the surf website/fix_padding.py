import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

mobile_css_rules = '''
    .property-description, .contact-form, .property-overview { padding: 25px !important; }
    .page-header { padding-top: 100px !important; }
    .page-header h1 { font-size: 2rem !important; }
'''

# Append mobile rules
css = css.replace('.thumbnail-grid { grid-template-columns: repeat(2, 1fr); }', '.thumbnail-grid { grid-template-columns: repeat(2, 1fr); }' + mobile_css_rules)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Added mobile padding reductions for listing boxes.")

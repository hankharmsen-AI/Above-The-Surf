import re

with open('templates/listing.template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace inline widths with classes
html = html.replace('width: 155px; color: #94a3b8;', 'color: #94a3b8;" class="analytics-label')
html = html.replace('width: 40px; color: #fff;', 'color: #fff;" class="analytics-score')
html = html.replace('margin: 0 20px;', 'margin: 0 20px;" class="analytics-bar-container')

with open('templates/listing.template.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

new_css = '''
.analytics-label { width: 155px; }
.analytics-score { width: 40px; }
.analytics-bar-container { margin: 0 20px; }
'''

mobile_css = '''
    .analytics-label { width: 110px !important; font-size: 0.8rem !important; letter-spacing: 0px !important; }
    .analytics-bar-container { margin: 0 10px !important; }
'''

css = css.replace('.thumbnail-grid img:hover { opacity: 0.8; border-color: var(--primary); }', '.thumbnail-grid img:hover { opacity: 0.8; border-color: var(--primary); }' + new_css)

css = css.replace('.page-header h1 { font-size: 2rem !important; }', '.page-header h1 { font-size: 2rem !important; }' + mobile_css)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Added responsive classes for surf analytics.")

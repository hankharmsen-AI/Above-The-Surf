import re

with open('templates/listing.template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix overview stats to rely on CSS
html = html.replace('<div class="overview-stats" style="margin-bottom: 40px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; background: var(--bg-card); padding: 25px; border-radius: 12px; box-shadow: var(--shadow-lg);">', 
                    '<div class="overview-stats custom-stats">')

# Fix amenities list to rely on CSS
html = html.replace('<ul style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 16px; color: var(--text-muted);">',
                    '<ul class="amenities-list">')

with open('templates/listing.template.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

new_css_rules = '''
.custom-stats {
    margin-bottom: 40px; 
    display: grid; 
    grid-template-columns: repeat(3, 1fr); 
    gap: 15px; 
    background: var(--bg-card); 
    padding: 25px; 
    border-radius: 12px; 
    box-shadow: var(--shadow-lg);
}
.amenities-list {
    display: grid; 
    grid-template-columns: 1fr 1fr; 
    gap: 12px; 
    margin-top: 16px; 
    color: var(--text-muted);
}
'''

mobile_css_rules = '''
    .custom-stats { grid-template-columns: 1fr !important; padding: 15px !important; gap: 10px !important; }
    .amenities-list { grid-template-columns: 1fr !important; }
'''

# Append normal rules
css = css.replace('.overview-stats {', new_css_rules + '\n.overview-stats {')

# Append mobile rules
css = css.replace('.thumbnail-grid { grid-template-columns: repeat(2, 1fr); }', '.thumbnail-grid { grid-template-columns: repeat(2, 1fr); }' + mobile_css_rules)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Moved inline grid styles to CSS with mobile fallbacks.")

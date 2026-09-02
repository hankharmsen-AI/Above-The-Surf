import re

# 1. Update CSS to have the desired column ratio
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('.property-detail-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 40px; }', 
                  '.property-detail-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 40px; }')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Remove the inline override from listing.template.html
with open('templates/listing.template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the inline grid styling to allow the CSS media query to take over
html = html.replace('<div class="property-detail-grid" style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 40px;">', 
                    '<div class="property-detail-grid">')

with open('templates/listing.template.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Removed inline grid style to allow mobile responsive stacking.")

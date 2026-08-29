import os
import re

def parse_markdown(filepath):
    with open(filepath, 'r', encoding='latin1') as f:
        content = f.read()
    
    # Parse frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return None
    
    frontmatter, body = match.groups()
    data = {}
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            # Unescape $ if needed, though usually standard
            data[key] = val
    data['body'] = body.strip()
    return data

def build_property_card(prop, is_us_only=False):
    if is_us_only and prop.get('country') != 'United States':
        return ""
        
    return f"""                <div class="property-card" onclick="window.location.href='listings/{prop.get('slug')}/index.html';" style="cursor: pointer;">
                        <div class="property-image">
                            <img src="{prop.get('image')}" alt="{prop.get('title')}">
                            <span class="badge">{prop.get('badge')}</span>
                        </div>
                    <div class="property-details">
                        <div class="property-price">{prop.get('price')}</div>
                        <h3 class="property-title">{prop.get('title')}</h3>
                        <div class="property-location"><i class="fas fa-map-marker-alt"></i> {prop.get('location')}</div>
                        <div class="property-meta">
                            <span><i class="fas fa-bed"></i> {prop.get('beds')} Beds</span>
                            <span><i class="fas fa-bath"></i> {prop.get('baths')} Baths</span>
                            <span><i class="fas fa-expand"></i> {prop.get('size')}</span>
                        </div>
                    </div>
                </div>
"""

def main():
    props_dir = "content/properties"
    properties = []
    
    # Load all properties
    for filename in os.listdir(props_dir):
        if filename.endswith(".md"):
            prop = parse_markdown(os.path.join(props_dir, filename))
            if prop:
                properties.append(prop)
                
    # We want to preserve a specific order ideally, but for now we'll sort them
    # Let's put United States first, then others. Or sort by featured.
    # We'll just sort them so Mission Beach and Hawaii are first to match current site.
    order = ["mission-beach-estate", "kua-nalu-poipu", "poipu-beach-4br-pool", "surfsong-unit1-orchid", "sayulita-lot", "eco-home-costa-rica", "popoyo-villa"]
    properties.sort(key=lambda x: order.index(x['slug']) if x['slug'] in order else 999)

    # 1. Update properties.html
    update_file("templates/properties.template.html", "properties.html", properties)
    
    # 2. Update index.html
    update_file("templates/index.template.html", "index.html", properties)

def update_file(template_path, output_path, properties):
    if not os.path.exists(template_path):
        return
        
    with open(template_path, 'r', encoding='latin1') as f:
        html = f.read()
        
    # Generate grids
    all_grid = "".join([build_property_card(p) for p in properties])
    
    html = re.sub(r'<!-- CMS_PROPERTIES_START -->.*?<!-- CMS_PROPERTIES_END -->', 
                  f'<!-- CMS_PROPERTIES_START -->\n{all_grid}<!-- CMS_PROPERTIES_END -->', 
                  html, flags=re.DOTALL)
                  
    with open(output_path, 'w', encoding='latin1') as f:
        f.write(html)
        
    print(f"Updated {output_path}")

if __name__ == "__main__":
    main()


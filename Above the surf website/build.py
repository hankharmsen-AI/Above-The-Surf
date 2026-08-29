import os
import re

def parse_markdown(filepath):
    with open(filepath, 'r', encoding='latin1') as f:
        content = f.read()
    
    # Parse frontmatter
    match = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n(.*)', content, re.DOTALL)
    if not match:
        return None
    
    frontmatter, body = match.groups()
    data = {}
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            data[key] = val
    data['body'] = body.strip()
    return data

def build_property_card(prop, is_subdir=False):
    # Adjust paths if we are inside a destination folder (e.g. destinations/mexico.html)
    link_prefix = "../listings/" if is_subdir else "listings/"
    img_src = prop.get('image', '')
    if is_subdir and not img_src.startswith("http"):
        img_src = "../" + img_src
        
    return f"""                <div class="property-card" data-country="{prop.get('country')}" onclick="window.location.href='{link_prefix}{prop.get('slug')}/index.html';" style="cursor: pointer;">
                        <div class="property-image">
                            <img src="{img_src}" alt="{prop.get('title')}">
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

def update_file(template_path, output_path, properties_to_render, is_subdir=False):
    if not os.path.exists(template_path):
        return
        
    with open(template_path, 'r', encoding='latin1') as f:
        html = f.read()
        
    # Generate grids
    grid_html = "".join([build_property_card(p, is_subdir) for p in properties_to_render])
    
    html = re.sub(r'<!-- CMS_PROPERTIES_START -->.*?<!-- CMS_PROPERTIES_END -->', 
                  f'<!-- CMS_PROPERTIES_START -->\n{grid_html}<!-- CMS_PROPERTIES_END -->', 
                  html, flags=re.DOTALL)
                  
    with open(output_path, 'w', encoding='latin1') as f:
        f.write(html)
        
    print(f"Updated {output_path}")

def main():
    props_dir = "content/properties"
    properties = []
    
    for filename in os.listdir(props_dir):
        if filename.endswith(".md"):
            prop = parse_markdown(os.path.join(props_dir, filename))
            if prop:
                properties.append(prop)
                
    order = ["mission-beach-estate", "kua-nalu-poipu", "poipu-beach-4br-pool", "surfsong-unit1-orchid", "sayulita-lot", "eco-home-costa-rica", "popoyo-villa"]
    properties.sort(key=lambda x: order.index(x['slug']) if x['slug'] in order else 999)

    # Main pages (shows everything)
    update_file("templates/properties.template.html", "properties.html", properties)
    update_file("templates/index.template.html", "index.html", properties)
    
    # Destination pages (filtered by country)
    update_file("templates/united-states.template.html", "destinations/united-states.html", [p for p in properties if p.get('country') == 'United States'], is_subdir=True)
    update_file("templates/mexico.template.html", "destinations/mexico.html", [p for p in properties if p.get('country') == 'Mexico'], is_subdir=True)
    update_file("templates/costa-rica.template.html", "destinations/costa-rica.html", [p for p in properties if p.get('country') == 'Costa Rica'], is_subdir=True)
    update_file("templates/nicaragua.template.html", "destinations/nicaragua.html", [p for p in properties if p.get('country') == 'Nicaragua'], is_subdir=True)

    # Property Detail Pages
    for p in properties:
        slug = p.get('slug')
        if not slug: continue
        
        folder = os.path.join('listings', slug)
        os.makedirs(folder, exist_ok=True)
        
        with open('templates/listing.template.html', 'r', encoding='latin1') as f:
            template = f.read()
            
        for key in ['title', 'location', 'price', 'badge', 'beds', 'baths', 'size', 'body', 'image', 'amenities']:
            val = p.get(key, '')
            # If image is an absolute URL (like hostaway), we don't prepend ../../
            if key == 'image' and val.startswith('http'):
                # Hack to override the inline CSS if it's an absolute url
                template = template.replace(f"url('../../{{{{image}}}}')", f"url('{val}')")
            else:
                if key == 'amenities' and val:
                    items = [x.strip() for x in str(val).split(',')]
                    li_html = "".join([f'<li><i class="fas fa-check" style="color: var(--primary); margin-right: 8px;"></i> {x}</li>' for x in items])
                    template = template.replace("{{amenities}}", li_html)
                elif key == 'body' and val:
                    val_str = str(val)
                    if '<p>' not in val_str:
                        paragraphs = "".join([f'<p>{p.strip()}</p>' for p in val_str.split('\n\n') if p.strip()])
                        template = template.replace("{{body}}", paragraphs)
                    else:
                        template = template.replace("{{body}}", val_str)
                else:
                    template = template.replace(f"{{{{{key}}}}}", str(val))
                
        with open(os.path.join(folder, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(template)
            
    print("Generated property pages")

if __name__ == "__main__":
    main()



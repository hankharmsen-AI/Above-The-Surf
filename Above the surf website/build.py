import os
import re
def parse_markdown(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin1') as f:
            content = f.read()
            
    # Safely extract frontmatter and body
    parts = content.split('---')
    if len(parts) < 3:
        return {} # Fallback so it doesn't crash
        
    frontmatter = parts[1]
    body = '---'.join(parts[2:]).strip()
    
    data = {'body': body}
    
    # Very robust basic YAML parser that won't crash
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and val:
                data[key] = val
                
    return data
def build_property_card(prop, is_subdir=False):
    if not prop:
        return ""
    link_prefix = "../listings/" if is_subdir else "listings/"
    img_src = prop.get('image', '')
    if is_subdir and not img_src.startswith("http"):
        img_src = "../" + img_src
        
    return f'''                <div class="property-card" data-country="{prop.get('country', '')}" onclick="window.location.href='{link_prefix}{prop.get('slug', '')}/index.html';" style="cursor: pointer;">
                        <div class="property-image">
                            <img src="{img_src}" alt="{prop.get('title', '')}">
                            <span class="badge">{prop.get('badge', '')}</span>
                        </div>
                    <div class="property-details">
                        <div class="property-price">{prop.get('price', '')}</div>
                        <h3 class="property-title">{prop.get('title', '')}</h3>
                        <div class="property-location"><i class="fas fa-map-marker-alt"></i> {prop.get('location', '')}</div>
                        <div class="property-meta">
                            <span><i class="fas fa-bed"></i> {prop.get('beds', '')} Beds</span>
                            <span><i class="fas fa-bath"></i> {prop.get('baths', '')} Baths</span>
                            <span><i class="fas fa-expand"></i> {prop.get('size', '')}</span>
                        </div>
                    </div>
                </div>
'''
def update_file(template_path, output_path, properties_to_render, is_subdir=False):
    if not os.path.exists(template_path):
        return
        
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    grid_html = "".join([build_property_card(p, is_subdir) for p in properties_to_render if p])
    
    html = re.sub(r'<!-- CMS_PROPERTIES_START -->.*?<!-- CMS_PROPERTIES_END -->', 
                  f'<!-- CMS_PROPERTIES_START -->\n{grid_html}<!-- CMS_PROPERTIES_END -->', 
                  html, flags=re.DOTALL)
                  
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
def main():
    props_dir = 'content/properties'
    properties = []
    
    if os.path.exists(props_dir):
        for filename in os.listdir(props_dir):
            if filename.endswith('.md'):
                prop = parse_markdown(os.path.join(props_dir, filename))
                if prop and prop.get('slug'):
                    properties.append(prop)
                    
    # Generate main pages
    update_file('templates/properties.template.html', 'properties.html', properties)
    update_file('templates/index.template.html', 'index.html', properties)
    
    # Generate destination pages
    dest_dir = 'destinations'
    if os.path.exists(dest_dir):
        destinations = {
            'united-states': 'United States',
            'mexico': 'Mexico',
            'costa-rica': 'Costa Rica',
            'nicaragua': 'Nicaragua'
        }
        for slug, country in destinations.items():
            filtered = [p for p in properties if p.get('country') == country]
            template = f'templates/{slug}.template.html'
            output = f'destinations/{slug}.html'
            update_file(template, output, filtered, is_subdir=True)
            
    # Generate individual listing pages
    listing_template = 'templates/listing.template.html'
    if os.path.exists(listing_template):
        with open(listing_template, 'r', encoding='utf-8') as f:
            base_template = f.read()
            
        os.makedirs('listings', exist_ok=True)
        
        for prop in properties:
            if not prop: continue
            slug = prop.get('slug')
            if not slug: continue
            
            os.makedirs(f'listings/{slug}', exist_ok=True)
            template = base_template
            
            keys = ['title', 'location', 'price', 'badge', 'beds', 'baths', 'size', 'body', 'image', 'amenities']
            for key in keys:
                val = prop.get(key, '')
                if key == 'amenities' and val:
                    items = [x.strip() for x in str(val).split(',')]
                    li_html = "".join([f'<li><i class="fas fa-check" style="color: var(--primary); margin-right: 8px;"></i> {x}</li>' for x in items if x])
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
                    
            with open(f'listings/{slug}/index.html', 'w', encoding='utf-8') as f:
                f.write(template)
if __name__ == '__main__':
    main()

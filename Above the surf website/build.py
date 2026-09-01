import os
import re
import json

def parse_markdown(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin1') as f:
            content = f.read()
            
    parts = content.split('---')
    if len(parts) < 3:
        return {}
        
    frontmatter = parts[1]
    body = '---'.join(parts[2:]).strip()
    
    data = {'body': body}
    
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

def update_file(template_path, output_path, properties_to_render, is_subdir=False, all_properties=None):
    if not os.path.exists(template_path):
        return
        
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
    except UnicodeDecodeError:
        with open(template_path, 'r', encoding='latin1') as f:
            html = f.read()
        
    grid_html = "".join([build_property_card(p, is_subdir) for p in properties_to_render if p])
    html = re.sub(r'<!-- CMS_PROPERTIES_START -->.*?<!-- CMS_PROPERTIES_END -->', 
                  f'<!-- CMS_PROPERTIES_START -->\n{grid_html}<!-- CMS_PROPERTIES_END -->', 
                  html, flags=re.DOTALL)

    sales = [p for p in properties_to_render if p.get('badge') == 'FOR SALE']
    rentals = [p for p in properties_to_render if p.get('badge') == 'VACATION RENTAL']

    sales_html = "".join([build_property_card(p, is_subdir) for p in sales if p])
    rentals_html = "".join([build_property_card(p, is_subdir) for p in rentals if p])

    html = re.sub(r'<!-- CMS_SALES_START -->.*?<!-- CMS_SALES_END -->', 
                  f'<!-- CMS_SALES_START -->\n{sales_html}<!-- CMS_SALES_END -->', 
                  html, flags=re.DOTALL)
    html = re.sub(r'<!-- CMS_RENTALS_START -->.*?<!-- CMS_RENTALS_END -->', 
                  f'<!-- CMS_RENTALS_START -->\n{rentals_html}<!-- CMS_RENTALS_END -->', 
                  html, flags=re.DOTALL)
                  
    if '<!-- CMS_MAP_DATA -->' in html and all_properties is not None:
        map_data = []
        for p in all_properties:
            if p.get('lat') and p.get('lng'):
                link_prefix = "../listings/" if is_subdir else "listings/"
                map_data.append({
                    'title': p.get('title', ''),
                    'price': p.get('price', ''),
                    'lat': float(p.get('lat')),
                    'lng': float(p.get('lng')),
                    'badge': p.get('badge', ''),
                    'url': f"{link_prefix}{p.get('slug', '')}/index.html",
                    'image': p.get('image', '')
                })
        map_json = json.dumps(map_data)
        html = html.replace('<!-- CMS_MAP_DATA -->', map_json)
                  
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
                    
    update_file('templates/properties.template.html', 'properties.html', properties, all_properties=properties)
    update_file('templates/index.template.html', 'index.html', properties, all_properties=properties)
    update_file('templates/surf-trips.template.html', 'surf-trips.html', properties, all_properties=properties)
    
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
            update_file(template, output, filtered, is_subdir=True, all_properties=properties)
            
    listing_template = 'templates/listing.template.html'
    if os.path.exists(listing_template):
        try:
            with open(listing_template, 'r', encoding='utf-8') as f:
                base_template = f.read()
        except UnicodeDecodeError:
            with open(listing_template, 'r', encoding='latin1') as f:
                base_template = f.read()
            
        os.makedirs('listings', exist_ok=True)
        
        for prop in properties:
            if not prop: continue
            slug = prop.get('slug')
            if not slug: continue
            
            os.makedirs(f'listings/{slug}', exist_ok=True)
            template = base_template
            
            keys = ['title', 'location', 'price', 'badge', 'beds', 'baths', 'size', 'body', 'image', 'amenities', 'surf_score', 'wave_height', 'water_temp', 'consistency', 'break_type', 'crowd_level', 'quality_score', 'size_score', 'consistency_score', 'crowd_score', 'proximity_score', 'lat', 'lng']
            for key in keys:
                val = prop.get(key, '')
                
                # Special handling for out-of-10 score bars
                if key in ['proximity_score', 'quality_score', 'size_score', 'consistency_score', 'crowd_score']:
                    try:
                        score_float = float(val)
                        width_val = int(score_float * 10)
                        template = template.replace(f"{{{{{key}_width}}}}", str(width_val))
                    except ValueError:
                        template = template.replace(f"{{{{{key}_width}}}}", "0")
                        
                if key == 'image':
                    img_src = str(val)
                    if not img_src.startswith('http'):
                        img_src = '../../' + img_src.lstrip('/')
                    template = template.replace('{{image}}', img_src)
                elif key == 'amenities' and val:
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

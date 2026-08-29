import re

with open('build.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the keys array
content = content.replace("['title', 'location', 'price', 'badge', 'beds', 'baths', 'size', 'body', 'image']", 
                          "['title', 'location', 'price', 'badge', 'beds', 'baths', 'size', 'body', 'image', 'amenities']")

# Replace the else block
old_else = '''            else:
                template = template.replace(f"{{{{{key}}}}}", str(val))'''
                
new_else = '''            else:
                if key == 'amenities' and val:
                    items = [x.strip() for x in str(val).split(',')]
                    li_html = "".join([f'<li><i class="fas fa-check" style="color: var(--primary); margin-right: 8px;"></i> {x}</li>' for x in items])
                    template = template.replace("{{amenities}}", li_html)
                elif key == 'body' and val:
                    val_str = str(val)
                    if '<p>' not in val_str:
                        paragraphs = "".join([f'<p>{p.strip()}</p>' for p in val_str.split('\\n\\n') if p.strip()])
                        template = template.replace("{{body}}", paragraphs)
                    else:
                        template = template.replace("{{body}}", val_str)
                else:
                    template = template.replace(f"{{{{{key}}}}}", str(val))'''

content = content.replace(old_else, new_else)

with open('build.py', 'w', encoding='utf-8') as f:
    f.write(content)

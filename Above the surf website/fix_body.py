import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('body {', 'body { overflow-x: hidden;')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

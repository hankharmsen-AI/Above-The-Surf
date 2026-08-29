import os

properties = [
    {
        'slug': 'surfsong-unit1-orchid',
        'title': 'SurfSong Poipu - Unit 1: The Orchid',
        'price': 'From $175/night',
        'location': 'Koloa, Hawaii',
        'country': 'United States',
        'beds': 'Studio',
        'baths': '1',
        'size': 'Sleeps 2',
        'badge': 'VACATION RENTAL',
        'image': 'Pictures/IMG_0336.jpeg'
    },
    {
        'slug': 'surfsong-unit2-seashell',
        'title': 'SurfSong Poipu - Unit 2: The Seashell',
        'price': 'From $175/night',
        'location': 'Koloa, Hawaii',
        'country': 'United States',
        'beds': '1',
        'baths': '1',
        'size': 'Sleeps 2',
        'badge': 'VACATION RENTAL',
        'image': 'Pictures/IMG_0336.jpeg'
    },
    {
        'slug': 'surfsong-unit3-hawaiiana',
        'title': 'SurfSong Poipu - Unit 3: The Hawai''iana',
        'price': 'From $225/night',
        'location': 'Koloa, Hawaii',
        'country': 'United States',
        'beds': '1',
        'baths': '1',
        'size': 'Sleeps 4',
        'badge': 'VACATION RENTAL',
        'image': 'Pictures/IMG_0336.jpeg'
    },
    {
        'slug': 'surfsong-unit4-flamingo',
        'title': 'SurfSong Poipu - Unit 4: The Flamingo',
        'price': 'From $185/night',
        'location': 'Koloa, Hawaii',
        'country': 'United States',
        'beds': 'Studio',
        'baths': '1',
        'size': 'Sleeps 3',
        'badge': 'VACATION RENTAL',
        'image': 'Pictures/IMG_0336.jpeg'
    },
    {
        'slug': 'sd-oceanfront-unit1',
        'title': 'Oceanfront Unit #1 - South Mission Beach',
        'price': 'From $400/night',
        'location': 'San Diego, California',
        'country': 'United States',
        'beds': '3',
        'baths': '2',
        'size': 'Sleeps 8',
        'badge': 'VACATION RENTAL',
        'image': 'Pictures/IMG_8709.jpeg'
    },
    {
        'slug': 'sd-oceanfront-unit2',
        'title': 'Oceanfront Unit #2 - South Mission Beach',
        'price': 'From $350/night',
        'location': 'San Diego, California',
        'country': 'United States',
        'beds': '2',
        'baths': '1',
        'size': 'Sleeps 6',
        'badge': 'VACATION RENTAL',
        'image': 'Pictures/IMG_8709.jpeg'
    },
    {
        'slug': 'sd-oceanfront-unit3',
        'title': 'Oceanfront Unit #3 - South Mission Beach',
        'price': 'From $325/night',
        'location': 'San Diego, California',
        'country': 'United States',
        'beds': '2',
        'baths': '2',
        'size': 'Sleeps 6',
        'badge': 'VACATION RENTAL',
        'image': 'Pictures/IMG_8709.jpeg'
    }
]

for p in properties:
    content = f'''---
title: "{p['title']}"
slug: "{p['slug']}"
price: "{p['price']}"
location: "{p['location']}"
country: "{p['country']}"
beds: "{p['beds']}"
baths: "{p['baths']}"
size: "{p['size']}"
badge: "{p['badge']}"
image: "{p['image']}"
---

Beautiful property in {p['location']}.
'''
    with open(f"content/properties/{p['slug']}.md", 'w', encoding='utf-8') as f:
        f.write(content)


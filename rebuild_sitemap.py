import json, os, re

BASE = 'https://daohang.bot.cd'

with open('data/projects.json') as f:
    projects = json.load(f)

urls = [(f'{BASE}/', 'daily', '1.0')]

for p in ['categories/', 'collections/', 'trending/', 'daily-brief/', 'projects/', 'guides/', 'tags/', 'hubs/']:
    urls.append((f'{BASE}/{p}', 'weekly', '0.9'))

sluggy = lambda n: re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')

for p in projects:
    urls.append((f'{BASE}/projects/{sluggy(p.get("full_name", p.get("name", "")))}/', 'weekly', '0.7'))

for f in sorted(os.listdir("guides")):
    if f.endswith('.html') and f != 'index.html':
        urls.append((f'{BASE}/guides/{f.replace(".html", "")}/', 'weekly', '0.75'))

seen = set()
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for u, fr, pr in urls:
    if u not in seen:
        seen.add(u)
        xml += f'  <url><loc>{u}</loc><changefreq>{fr}</changefreq><priority>{pr}</priority></url>\n'

xml += '</urlset>'

with open('sitemap.xml', 'w') as f:
    f.write(xml)

print(f"Sitemap: {len(seen)} URLs")

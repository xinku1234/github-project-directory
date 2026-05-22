# GitHub Project Directory

A lightweight static MVP for a curated GitHub/open-source project directory.

## What is included

- Homepage with GEO-inspired positioning
- Project directory with client-side search/filter
- Structured project data: `data/projects.json`
- Guide hub and 5 answer-ready guide pages
- Resources and submit placeholder pages
- SEO basics: `robots.txt`, `sitemap.xml`, `llms.txt`, meta descriptions, OG image
- Hero image asset: `assets/hero-github-directory.png`

## Local preview

```bash
cd /home/admin/github-project-directory
python3 -m http.server 4173
# open http://127.0.0.1:4173/
```

## Next steps before public launch

1. Replace `https://example.com` in `index.html`, `robots.txt`, and `sitemap.xml` with the real domain.
2. Replace placeholder GitHub topic links with hand-reviewed real repositories.
3. Connect `submit.html` to Airtable, Notion, Formspree, or a serverless function.
4. Add category landing pages for long-tail SEO/GEO traffic.
5. Deploy to Cloudflare Pages, GitHub Pages, or Netlify.

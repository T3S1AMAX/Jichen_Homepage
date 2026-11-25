# Personal homepage (static)

This repo is a **pure static** site (no build step). You can deploy it with:
- **GitHub Pages**, or
- **Cloudflare Pages** (recommended if you want Cloudflare protection by default).

## Local preview

Any static server works.

### Option A: Python
```bash
python -m http.server 8000
# then open http://localhost:8000
```

### Option B: Node
```bash
npx serve .
```

## Update content

- Replace `assets/profile.png` with your own photo (keep the filename).
- Replace placeholder images in `assets/pubs/<paper>/` with real teaser/figures (keep filenames).
- Edit `index.html` and `pubs/*/index.html` for text.

The CV is at `cv/cv.pdf` (replace with your latest).
Before publishing a replacement, check `pdfinfo cv/cv.pdf`: its embedded Title
should be `Jichen Feng - Curriculum Vitae`, not an employer-specific application
or draft name. This metadata can appear in search results and PDF viewers.
Keep the CV searchable and keep its public URL fixed at
`https://jichen-feng.com/cv/cv.pdf` (no `?v=` parameter). `_headers` makes every
query-string variant point to that same canonical URL. For this PDF only,
`Cache-Control: no-store` and `Cloudflare-CDN-Cache-Control: no-store` ask browsers
and Cloudflare to fetch the current file instead of retaining an older copy.
These cache directives do not prevent search indexing or downloading the CV.
Existing versioned links remain usable; they are not deleted
or blocked with `noindex`.

Before publishing, run `python3 scripts/check_public_cv.py` (requires Poppler's
`pdfinfo`). This checks the PDF title, stable homepage link, canonical/cache
headers, crawl permissions, and sitemap URLs without changing the PDF.
Add new publication pages to `sitemap.xml` when publishing them.

After deployment, check the `Link` and `Cache-Control` response headers on both
`/cv/cv.pdf` and old `?v=` URLs. The public response must include the canonical
`Link` and `Cache-Control: no-store`; a successful Pages build alone is not enough.
If the custom domain overrides these headers, check its Cloudflare Cache Rules
and Browser Cache TTL, respect the origin headers for `/cv/cv.pdf`, and purge
only the affected CV URLs. In Google Search Console, inspect the unversioned
CV URL, request indexing, and submit `https://jichen-feng.com/sitemap.xml`.
Search-title/sitelink updates depend on Google's recrawling and processing;
a successful deployment does not mean the old search title has disappeared.

## Deploy with GitHub Pages (custom domain supported)

1. Push this folder to a GitHub repo.
2. GitHub repo → **Settings → Pages**:
   - Source: Deploy from branch
   - Branch: `main` / `/ (root)`
3. (Optional) Set a custom domain in the Pages settings.
4. DNS:
   - For `www`: add a CNAME record to `YOUR_USERNAME.github.io`
   - For apex/root: follow GitHub’s A-record instructions (GitHub Pages docs).

## Deploy with Cloudflare Pages (easy Cloudflare protection)

1. Add your domain to Cloudflare (so Cloudflare manages your DNS).
2. Cloudflare Dashboard → **Pages → Create a project → Connect to Git**.
3. Build settings:
   - Framework preset: **None**
   - Build command: *(empty)*
   - Output directory: `/` (or leave default; this project is already static)
4. After first deploy, Pages → **Custom Domains** → add your domain.
5. Cloudflare will automatically create the right DNS records and enable HTTPS.

## Notes

- This site uses only `index.html`, `style.css`, `script.js`, and static assets.
- Publication “abstract” and “bibtex” toggles are implemented in `script.js`.

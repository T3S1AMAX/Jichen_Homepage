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

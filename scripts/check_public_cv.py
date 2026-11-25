"""Check public CV metadata and search URL consistency before publishing.

Requires Python 3 and Poppler's pdfinfo; does not modify any files.
"""

from fnmatch import fnmatchcase
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import urljoin, urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://jichen-feng.com/"
CV_URL = urljoin(SITE, "cv/cv.pdf")


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")


class Homepage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.robots = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.links.append(urljoin(SITE, attrs["href"]))
        if tag == "meta" and attrs.get("name", "").lower() in {"robots", "googlebot"}:
            self.robots.append(attrs.get("content", "").lower())


require(shutil.which("pdfinfo"), "Install Poppler to inspect the PDF title.")
pdf_info = subprocess.check_output(
    ["pdfinfo", str(ROOT / "cv/cv.pdf")], text=True
)
require(
    re.search(r"^Title:\s+Jichen Feng - Curriculum Vitae\s*$", pdf_info, re.M),
    "The public PDF title must be 'Jichen Feng - Curriculum Vitae'.",
)

homepage = Homepage()
homepage.feed((ROOT / "index.html").read_text())
cv_links = [url for url in homepage.links if urlsplit(url).path == "/cv/cv.pdf"]
require(cv_links and all(url == CV_URL for url in cv_links),
        "Link to the stable CV URL, without query parameters or fragments.")
require(not any("noindex" in rule or "none" in rule for rule in homepage.robots),
        "The homepage must remain indexable.")

rules = {}
route = None
for line in (ROOT / "_headers").read_text().splitlines():
    if not line.strip() or line.lstrip().startswith("#"):
        continue
    if not line[0].isspace():
        route = line.strip()
        rules[route] = {}
    else:
        require(route is not None, "A header is missing its route.")
        name, value = line.strip().split(":", 1)
        rules[route][name.lower()] = value.strip()

cv_headers = rules.get("/cv/cv.pdf", {})
require(cv_headers.get("link") == f'<{CV_URL}>; rel="canonical"',
        "Declare the same canonical URL for every CV query variant.")
cache_rules = {rule.strip() for rule in cv_headers.get("cache-control", "").split(",")}
require({"no-store", "no-cache", "max-age=0", "must-revalidate"} <= cache_rules,
        "Fetch the latest PDF instead of versioning its public URL.")
require(cv_headers.get("cloudflare-cdn-cache-control") == "no-store",
        "Keep the custom-domain CDN from retaining an older PDF.")
for route, headers in rules.items():
    if any(fnmatchcase(path, route) or fnmatchcase(urljoin(SITE, path), route)
           for path in ("/", "/cv/cv.pdf")):
        directives = headers.get("x-robots-tag", "").lower()
        require("noindex" not in directives and "none" not in directives,
                f"{route} must not prevent homepage/CV indexing.")

robots = RobotFileParser()
robots.parse((ROOT / "robots.txt").read_text().splitlines())
require(all(robots.can_fetch("Googlebot", url) for url in (SITE, CV_URL)),
        "Allow Google to crawl both the homepage and CV.")
require(urljoin(SITE, "sitemap.xml") in (robots.site_maps() or []),
        "Advertise the sitemap in robots.txt.")

namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [element.text for element in ET.parse(ROOT / "sitemap.xml").findall("s:url/s:loc", namespace)]
require(SITE in urls and CV_URL in urls, "List the homepage and canonical CV in the sitemap.")
require(len(urls) == len(set(urls)), "The sitemap contains duplicate URLs.")
for url in urls:
    parsed = urlsplit(url)
    require(parsed.scheme == "https" and parsed.netloc == "jichen-feng.com"
            and not parsed.query and not parsed.fragment,
            f"Not a canonical production URL: {url}")
    target = ROOT / parsed.path.lstrip("/")
    if parsed.path.endswith("/"):
        target /= "index.html"
    require(target.is_file(), f"Missing sitemap target: {target}")

print(f"PASS: PDF title, stable CV link, canonical/cache headers, crawling, {len(urls)} sitemap URLs.")

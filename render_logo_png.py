import os
import pathlib
from playwright.sync_api import sync_playwright

def render():
    svg_path = pathlib.Path('static/logo.svg').resolve().as_uri()
    png_path = str(pathlib.Path('static/logo.png').resolve())
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 512, 'height': 512})
        page.goto(svg_path)
        page.screenshot(path=png_path, omit_background=True)
        browser.close()
    print("Rendered static/logo.png successfully via Playwright!")

if __name__ == '__main__':
    render()

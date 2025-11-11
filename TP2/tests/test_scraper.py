import pytest
from scraper.html_parser import parse_html_full

# Un HTML de prueba
SAMPLE_HTML = """
<html>
  <head>
    <title>Test Page</title>
    <meta name="description" content="A test description.">
    <meta property="og:title" content="OG Test Title">
  </head>
  <body>
    <h1>Header 1</h1>
    <h2>Header 2</h2>
    <a href="/page1">Link 1</a>
    <a href="https://example.com">Link 2</a>
    <img src="img1.png">
  </body>
</html>
"""

BASE_URL = "https://my-test-site.com"

def test_parse_html_full():
    data = parse_html_full(SAMPLE_HTML, BASE_URL)
    
    # Comprobar scraping_data
    assert data["title"] == "Test Page"
    assert data["images_count"] == 1
    
    # --- PRUEBA CLAVE (La que falla) ---
    assert len(data["links"]) == 2
    # 'urljoin' debe arreglar esto
    assert "https://my-test-site.com/page1" in data["links"] 
    assert "https://example.com" in data["links"]
    
    # Comprobar meta_tags (claves corregidas)
    assert data["meta_tags"]["description"] == "A test description."
    assert data["meta_tags"]["og:title"] == "OG Test Title"
    
    # Comprobar structure
    assert data["structure"]["h1"] == 1
    assert data["structure"]["h2"] == 1
    assert data["structure"]["h3"] == 0
        
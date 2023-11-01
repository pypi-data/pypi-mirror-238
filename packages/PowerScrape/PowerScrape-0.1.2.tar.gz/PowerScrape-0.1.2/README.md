```markdown
# PowerScrape

PowerScrape is a comprehensive and versatile Python module for web scraping. It provides powerful functionalities to extract various types of content from the web, including HTML, JSON, images, PDFs, and more. The module also includes features for handling different types of web requests, handling errors, and cloning entire websites into local files.

## Features

- Scraping HTML content from web pages
- Scraping JSON data from APIs
- Downloading images from a web page
- Rendering JavaScript-based web pages
- Extracting text from PDF files
- Extracting data points from chart images
- Making HTTP POST requests
- Handling various HTTP status codes
- Cloning entire websites into local files

## Installation

You can install PowerScrape using pip:

```bash
pip install PowerScrape
```

## Usage

```python
from PowerScrape import Scraper

# Create an instance of the Scraper class
scraper = Scraper()

# Use the various methods provided by the Scraper class to perform web scraping operations

# Example: Scrape a normal HTML page
soup = scraper.scrape_html('http://example.com')

# Example: Scrape a JSON API
data = scraper.scrape_json('http://api.example.com/data')

# Example: Scrape and download images 
scraper.scrape_images('http://example.com/gallery', 'scraped_images')

# Example: Scrape JavaScript rendered page
html = scraper.scrape_javascript('http://example.com')

# Example: Extract text from a PDF file
text = scraper.scrape_pdf('http://example.com/doc.pdf')

# Example: Extract data points from a chart image
data = scraper.scrape_graph('http://example.com/chart.png')

# Example: Make an HTTP POST request
response = scraper.http_post_request('http://example.com/post_endpoint', data={'key': 'value'})

# Example: Clone a website
scraper.clone_website('http://example.com', 'cloned_website')
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

--------------
Made by ^mind-set#0001

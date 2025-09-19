#!/usr/bin/env python3
"""
Debug version to identify the translation issue
"""

import requests
from bs4 import BeautifulSoup
import traceback

def debug_fetch_article(url):
    """Debug version of article fetching"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    try:
        print(f"Fetching: {url}")
        response = session.get(url)
        response.raise_for_status()
        print(f"Status: {response.status_code}")
        print(f"Content length: {len(response.text)}")
        return response.text
    except Exception as e:
        print(f"Error fetching: {e}")
        return None

def debug_extract_content(html_content, url):
    """Debug version of content extraction"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        print(f"Soup created successfully")
        
        # Check title
        title_tag = soup.find('title')
        if title_tag:
            print(f"Title found: {title_tag.get_text()[:100]}...")
        else:
            print("No title found")
        
        # Try to find article content with different selectors
        selectors = [
            'article',
            '.article-content', 
            '.post-content',
            '.entry-content',
            '#content',
            '.content',
            'main',
            '.blog-post',
            '.blog-content'
        ]
        
        article_content = None
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                print(f"Found content with selector: {selector}")
                article_content = element
                break
        
        if not article_content:
            print("No article content found with standard selectors")
            # Try to find any div with substantial text
            all_divs = soup.find_all('div')
            for div in all_divs:
                if div.get_text().strip() and len(div.get_text().strip()) > 200:
                    print(f"Found div with substantial content: {len(div.get_text())} characters")
                    article_content = div
                    break
        
        if article_content:
            print(f"Article content length: {len(str(article_content))}")
            print(f"Article text length: {len(article_content.get_text())}")
            print(f"First 200 chars: {article_content.get_text()[:200]}...")
            return article_content
        else:
            print("No article content found at all")
            return None
            
    except Exception as e:
        print(f"Error in extract_content: {e}")
        traceback.print_exc()
        return None

if __name__ == "__main__":
    url = "https://www.softwareshop.sk/blog/ktoru-verziu-sketchup-si-vybrat--kompletny-sprievodca-2025/"
    
    html_content = debug_fetch_article(url)
    if html_content:
        article_content = debug_extract_content(html_content, url)
        if article_content:
            print("✅ Article extraction successful!")
        else:
            print("❌ Article extraction failed!")
    else:
        print("❌ Fetching failed!")
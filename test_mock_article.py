#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test with mock HTML content that simulates a complete article
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from article_translator import ArticleTranslator
from bs4 import BeautifulSoup

def test_mock_article_translation():
    """Test with complete mock article that has the problematic patterns"""
    
    # Mock HTML that simulates a real Slovak article with problematic patterns
    mock_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ako prepojiť SketchUp s D5 Render - podrobný návod</title>
        <meta name="description" content="Zistite, ako jednoducho prepojiť SketchUp s D5 Render pre fotorealistické vizualizácie.">
        <meta property="og:image" content="https://example.com/header-image.jpg">
    </head>
    <body>
        <article>
            <h1>Ako prepojiť SketchUp s D5 Render - podrobný návod</h1>
            <img src="https://example.com/header-image.jpg" itemprop="image" fetchpriority="high" alt="Header">
            <div class="text">
                <p>SketchUp patří mezi najobľúbenejší nástroje na<strong>3D modelovanie</strong>, ale jeho vlastné možnosti vizualizácie sú obmedzené. Práve tu prichádzá do hry D5 Render, moderný nástroj na<strong>fotorealistické vykresľovanie</strong>v reálnom čase.</p>
                
                <!-- CTA blok: kontaktujte nás -->
                <div style="background-color: #e1f0ff; padding: 20px; margin: 20px 0; border-radius: 8px; text-align: center;">
                    <h3 style="margin-bottom: 10px;">Chcete pracovať rýchlejšie a získať lepšie výsledky?</h3>
                    <p style="margin-bottom: 20px;">Zistite, ako vám D5 Render môže pomôcť pri tvorbe vizualizácií alebo sa poraďte s nami.</p>
                    <a href="/sketchup-d5-render-konzultacia/" style="background-color: #007bff; padding: 12px 24px; color: #fff; text-decoration: none; border-radius: 4px; font-weight: bold;"> ➡️ Kontaktujte nás </a>
                </div>
                
                <h2>1. Inštalácia doplnku D5 Converter pre SketchUp</h2>
                <p>Aby ste mohli SketchUp a D5 Render prepojiť, potrebujete doplnok<strong>D5 Converter</strong>. Tento doplnok slúži na<strong>priame spojenie</strong>oboch programov a umožní vám rýchlejšie a efektívnejšie pracovať.</p>
                
                <h2>2. Aktivácia živého prepojenia medzi SketchUp a D5 Render</h2>
                <p>Po inštalácii doplnku otvorte oba programy súčasne. V SketchUp-e kliknite na ikonu<strong>D5 Converter</strong>, čím aktivujete funkciu<strong>LiveSync</strong>. Od tohto momentu sa každý váš krok v SketchUp-e automaticky premietne do D5 Render v<strong>reálnom čase</strong>.</p>
                
                <img src="https://example.com/content-image.jpg" alt="D5 Render interface">
                
                <h2>3. Prenos modelu do D5 Render</h2>
                <p>Ak nepotrebujete živé prepojenie, môžete využiť aj jednorazový<strong>export modelu</strong>. Pri tejto možnosti sa spolu s geometriou prenesú aj všetky nastavené materiály a textúry zo SketchUp-u priamo do D5 Render.</p>
                
                <!-- CTA blok: kurz -->
                <div style="background-color: #e1f0ff; padding: 20px; margin-top: 20px; border-radius: 8px; text-align: center;">
                    <h3 style="margin-bottom: 10px;">🎓 Chcete sa naučiť pracovať s D5 Render profesionálne?</h3>
                    <p style="margin-bottom: 20px;">Na našom kurze D5 Render vás naučíme, ako vytvářať pôsobivé vizualizácie rýchlo a efektívne.</p>
                    <a href="/d5-render-kurz/" style="background-color: #007bff; padding: 12px 24px; color: #fff; text-decoration: none; border-radius: 4px; font-weight: bold;">➡️ Prihlásiť sa na kurz</a>
                </div>
            </div>
        </article>
    </body>
    </html>
    """
    
    print("TESTING MOCK ARTICLE TRANSLATION")
    print("=" * 60)
    
    # Create ArticleTranslator instance
    translator = ArticleTranslator()
    
    # Simulate the article extraction process
    soup = BeautifulSoup(mock_html, 'html.parser')
    
    # Extract metadata like the real process does
    metadata = {
        'title': soup.find('title').get_text().strip() if soup.find('title') else '',
        'description': '',
        'cover_image': ''
    }
    
    meta_tags = soup.find_all('meta')
    for tag in meta_tags:
        if tag.get('name') == 'description':
            metadata['description'] = tag.get('content', '').strip()
        elif tag.get('property') == 'og:image':
            metadata['cover_image'] = tag.get('content', '')
    
    print(f"Original Title: {metadata['title']}")
    print(f"Original Description: {metadata['description']}")
    
    # Find article content
    article_content = soup.find('article')
    
    # Translate the HTML content using the proper pipeline
    title = metadata['title']
    content_text = article_content.get_text() if article_content else ''
    
    print("\\nTranslating HTML content...")
    translator.translate_html_content(article_content, title, content_text)
    
    # Clean the content (remove comments, header, etc.)
    print("\\nCleaning HTML content...")
    cleaned_content = translator.clean_html_content(article_content)
    
    # Get the final result
    final_html = str(cleaned_content)
    
    print("\\nFINAL TRANSLATED AND CLEANED HTML:")
    print("=" * 60)
    print(final_html[:1000] + "..." if len(final_html) > 1000 else final_html)
    
    # Verify both issues are fixed
    print("\\n" + "=" * 60)
    print("VERIFICATION RESULTS:")
    print("=" * 60)
    
    # Check spacing issues
    import re
    spacing_issues = []
    if re.search(r'[^\\s]<strong', final_html):
        spacing_issues.append("Missing space before <strong>")
    if re.search(r'</strong>[^\\s]', final_html):
        spacing_issues.append("Missing space after </strong>")
    
    if spacing_issues:
        print("❌ SPACING ISSUES:")
        for issue in spacing_issues:
            print(f"   - {issue}")
        
        # Show specific problematic patterns found
        patterns = re.findall(r'\\w<strong|</strong>\\w', final_html)
        if patterns:
            print("   - Problematic patterns found:")
            for pattern in patterns[:5]:  # Show first 5
                print(f"     * {pattern}")
    else:
        print("✅ SPACING: All <strong> tags have proper spacing")
    
    # Check HTML comments
    if re.search(r'<!--.*?-->', final_html, flags=re.DOTALL):
        print("❌ COMMENTS: HTML comments still present")
        comments = re.findall(r'<!--(.*?)-->', final_html, flags=re.DOTALL)
        for comment in comments[:3]:  # Show first 3
            print(f"   - Found: <!--{comment[:30]}...-->")
    else:
        print("✅ COMMENTS: All HTML comments removed")
    
    # Check for "CTA Block:" text that should not appear
    if "CTA Block:" in final_html or "CTA blok:" in final_html:
        print("❌ CTA TEXT: 'CTA Block:' text still appears in content")
    else:
        print("✅ CTA TEXT: No unwanted 'CTA Block:' text found")
    
    # Translate metadata
    print("\\nTranslating metadata...")
    translated_title = translator.translator.translate_text(metadata['title'])
    translated_description = translator.translator.translate_text(metadata['description'])
    
    print(f"Translated Title: {translated_title}")
    print(f"Translated Description: {translated_description}")

if __name__ == "__main__":
    test_mock_article_translation()
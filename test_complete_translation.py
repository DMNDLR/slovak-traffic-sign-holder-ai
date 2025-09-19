#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test the complete translation pipeline with sample HTML content
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from article_translator import ArticleTranslator
from bs4 import BeautifulSoup
import re

def test_complete_translation():
    """Test the complete translation with sample HTML containing problematic patterns"""
    
    article_translator = ArticleTranslator()
    
    # Sample HTML content that mimics the problematic patterns we've seen
    sample_html = """
    <div class="text">
        <article>
            <p>SketchUp patří mezi nejobľúbenejší nástroje na<strong>3D modelovanie</strong>, no jeho vlastné možnosti vizualizace sú obmedzené.</p>
            <!-- CTA blok: kontaktujte nás -->
            <div style="background-color: #e1f0ff; padding: 20px;">
                <h3>Chcete pracovať rýchlejšie?</h3>
                <p>Zisti, jak ti D5 Render môže pomôcť.</p>
                <a href="/konzultace/">Kontaktuj nás</a>
            </div>
            <h2>Instalácia doplnku D5 Converter</h2>
            <p>potrebujete doplnok<strong>D5 Converter</strong>. Tento doplnok slúži na<strong>priame spojenie</strong>oboch programů.</p>
            <h2>Aktivácia LiveSync</h2>  
            <p>aktivujete funkciu<strong>LiveSync</strong>od tohto momentu sa každý krok premietne do D5 Render v<strong>reálnom čase</strong>.</p>
            <!-- CTA blok: kurz -->
            <div style="background-color: #e1f0ff; padding: 20px;">
                <h3>Chcete sa naučiť D5 Render?</h3>
                <a href="/kurzy/d5-render/">Přihlásit se na kurz</a>
            </div>
        </article>
    </div>
    """
    
    print("TESTING COMPLETE TRANSLATION PIPELINE")
    print("=" * 60)
    print("\\nOriginal HTML:")
    print(sample_html)
    
    # Parse HTML
    soup = BeautifulSoup(sample_html, 'html.parser')
    
    # Translate text content
    print("\\n" + "=" * 60)
    print("TRANSLATING TEXT CONTENT...")
    
    # Use the proper translation pipeline
    title = "Test Article"
    content_text = soup.get_text()
    article_translator.translate_html_content(soup, title, content_text)
    
    # Clean HTML content to remove comments
    print("\\nREMOVING HTML COMMENTS...")
    soup_str = str(soup)
    soup_str = re.sub(r'<!--.*?-->', '', soup_str, flags=re.DOTALL)
    soup = BeautifulSoup(soup_str, 'html.parser')
    
    print("\\nFINAL TRANSLATED HTML:")
    print("=" * 60)
    print(str(soup))
    
    # Verify fixes
    final_html = str(soup)
    
    print("\\n" + "=" * 60)
    print("VERIFICATION RESULTS:")
    print("=" * 60)
    
    # Check for spacing issues
    spacing_issues = []
    if re.search(r'[^\\s]<strong', final_html):
        spacing_issues.append("Missing space before <strong>")
    if re.search(r'</strong>[^\\s]', final_html):
        spacing_issues.append("Missing space after </strong>")
    
    if spacing_issues:
        print("❌ SPACING ISSUES FOUND:")
        for issue in spacing_issues:
            print(f"   - {issue}")
    else:
        print("✅ SPACING: All <strong> tags have proper spacing")
    
    # Check for HTML comments
    if re.search(r'<!--.*?-->', final_html, flags=re.DOTALL):
        print("❌ COMMENTS: HTML comments still present")
    else:
        print("✅ COMMENTS: All HTML comments removed")
    
    # Check for specific patterns that were problematic
    problematic_patterns = [
        'na<strong>',
        '</strong>v',
        '</strong>V',
        '</strong>a',
        'doplnok<strong>',
        'funkciu<strong>',
        '<!-- CTA blok'
    ]
    
    pattern_issues = []
    for pattern in problematic_patterns:
        if pattern in final_html:
            pattern_issues.append(pattern)
    
    if pattern_issues:
        print("❌ SPECIFIC PATTERNS: Still found problematic patterns:")
        for pattern in pattern_issues:
            print(f"   - {pattern}")
    else:
        print("✅ SPECIFIC PATTERNS: All known problematic patterns fixed")

if __name__ == "__main__":
    test_complete_translation()
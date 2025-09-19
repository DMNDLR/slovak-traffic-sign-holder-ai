#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Slovak to Czech Article Translator
Prompts user for URL and options interactively
"""

import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from article_translator import ArticleTranslator

def safe_print(text):
    """Print text safely, handling Unicode encoding issues on Windows"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback: encode to ASCII with replacement characters
        print(text.encode('ascii', errors='replace').decode('ascii'))

def main():
    """Interactive main function"""
    print("=" * 60)
    print("SLOVAK TO CZECH ARTICLE TRANSLATOR")
    print("=" * 60)
    print()
    print("This tool translates Slovak articles to Czech while:")
    print("✅ Fixing spacing around <strong> tags")
    print("✅ Removing CTA block comments")
    print("✅ Preserving HTML structure and images")
    print("✅ Generating SEO metadata")
    print()
    
    # Get URL from user
    while True:
        url = input("Enter Slovak article URL: ").strip()
        if url:
            if not (url.startswith('http://') or url.startswith('https://')):
                url = 'https://' + url
            break
        else:
            print("❌ Please enter a valid URL")
    
    # Get output directory (optional)
    print()
    output_dir = input("Output directory (press Enter for default 'translated_articles'): ").strip()
    if not output_dir:
        output_dir = 'translated_articles'
    
    # Confirm settings
    print()
    print("=" * 60)
    print("TRANSLATION SETTINGS")
    print("=" * 60)
    print(f"📄 Source URL: {url}")
    print(f"📁 Output directory: {output_dir}")
    print()
    
    confirm = input("Start translation? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ Translation cancelled.")
        return
    
    print()
    print("=" * 60)
    print("STARTING TRANSLATION...")
    print("=" * 60)
    
    try:
        # Create translator and run
        translator = ArticleTranslator()
        result = translator.translate_article(url, output_dir)
        
        print()
        print("=" * 60)
        print("✅ TRANSLATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        
        # Show results
        safe_print(f"📁 Article folder: {result['article_folder']}")
        safe_print(f"📄 Content file: {result['html_file']}")
        safe_print(f"🔍 SEO file: {result['seo_file']}")
        
        if result.get('header_image'):
            safe_print(f"🖼️  Header image: {result['header_image']['filename']}")
        
        content_images_count = len(result.get('content_images', []))
        safe_print(f"🖼️  Content images: {content_images_count}")
        
        print()
        safe_print(f"📝 Translated title: {result['translated_metadata']['title']}")
        
        if result['translated_metadata'].get('description'):
            safe_print(f"📝 Description: {result['translated_metadata']['description'][:100]}...")
        
        print()
        print("=" * 60)
        print("📋 NEXT STEPS:")
        print("=" * 60)
        print("1. Review the translated content in the HTML file")
        print("2. Use the SEO metadata for your article title and description")
        print("3. Upload the header image as your article cover")
        print("4. Upload content images and update their references if needed")
        print()
        print("💡 TIP: Check the content.html file to verify spacing around <strong> tags is correct!")
        
        # Ask if user wants to open the folder
        print()
        open_folder = input("Open output folder in Explorer? (y/N): ").strip().lower()
        if open_folder in ['y', 'yes']:
            try:
                os.startfile(str(result['article_folder']))
            except Exception as e:
                print(f"❌ Could not open folder: {e}")
    
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ TRANSLATION FAILED")
        print("=" * 60)
        safe_print(f"Error: {str(e)}")
        print()
        print("💡 Common issues:")
        print("- Check if the URL is accessible")
        print("- Verify internet connection")
        print("- Some websites may block automated access")
        print("- Try a different article URL")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Translation cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
    
    input("\nPress Enter to exit...")
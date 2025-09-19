#!/usr/bin/env python3
"""
JSON Metadata Reader Utility
Extracts and displays metadata from translated articles for easy Shoptet import
"""

import json
import argparse
from pathlib import Path

def read_metadata(json_file):
    """Read and display metadata from JSON file"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("📄 ARTICLE METADATA")
        print("=" * 50)
        
        metadata = data.get('metadata', {})
        
        print(f"📝 Title: {metadata.get('title', 'N/A')}")
        print(f"📖 Description: {metadata.get('description', 'N/A')}")
        print(f"🏷️ Keywords: {metadata.get('keywords', 'N/A')}")
        print(f"✍️ Author: {metadata.get('author', 'N/A')}")
        print(f"🖼️ Cover Image: {metadata.get('cover_image', 'N/A')}")
        
        print("\n🖼️ IMAGES TO UPLOAD")
        print("=" * 50)
        
        images = data.get('images', [])
        if images:
            for i, img in enumerate(images, 1):
                print(f"{i}. {img['filename']}")
                print(f"   Local file: {img['local_path']}")
                print(f"   Original: {img['original_url']}")
                print()
        else:
            print("No images found")
        
        print("📊 TRANSLATION INFO")
        print("=" * 50)
        
        trans_info = data.get('translation_info', {})
        print(f"Source: {trans_info.get('source_language', 'N/A')}")
        print(f"Target: {trans_info.get('target_language', 'N/A')}")
        print(f"Generated: {data.get('generated_at', 'N/A')}")
        
        return data
        
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return None

def export_shoptet_checklist(data, output_file=None):
    """Export a Shoptet import checklist"""
    if not data:
        return
    
    metadata = data.get('metadata', {})
    images = data.get('images', [])
    
    checklist = f"""
# Shoptet Import Checklist

## 📋 Article Details
- [ ] Title: {metadata.get('title', 'N/A')}
- [ ] Description: {metadata.get('description', 'N/A')}
- [ ] Keywords: {metadata.get('keywords', 'N/A')}
- [ ] Author: {metadata.get('author', 'N/A')}

## 🖼️ Images to Upload ({len(images)} total)
"""
    
    for i, img in enumerate(images, 1):
        checklist += f"- [ ] Upload: {img['filename']}\n"
    
    checklist += f"""
## ✅ Steps
1. [ ] Create new article in Shoptet
2. [ ] Set title and SEO description
3. [ ] Upload all images to media library
4. [ ] Copy HTML content from shoptet_article_*.html file
5. [ ] Set cover image
6. [ ] Publish article

## 📁 Files
- HTML content: shoptet_article_*.html
- Images folder: images/
- This metadata: {Path(output_file or 'metadata').name}
"""
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(checklist)
        print(f"✅ Checklist saved to: {output_file}")
    else:
        print(checklist)

def main():
    parser = argparse.ArgumentParser(description='Read translated article metadata')
    parser.add_argument('json_file', help='JSON metadata file to read')
    parser.add_argument('--checklist', help='Export Shoptet import checklist to file')
    parser.add_argument('--summary', action='store_true', help='Show summary only')
    
    args = parser.parse_args()
    
    if not Path(args.json_file).exists():
        print(f"❌ File not found: {args.json_file}")
        return
    
    data = read_metadata(args.json_file)
    
    if data and args.checklist:
        export_shoptet_checklist(data, args.checklist)

if __name__ == "__main__":
    main()
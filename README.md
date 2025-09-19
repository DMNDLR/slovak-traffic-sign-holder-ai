# Slovak → Czech Article Translator

🚀 **Powerful tool for translating Slovak articles to Czech with perfect HTML formatting, automatic image processing, and CMS-ready output.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## 🚀 Quick Start

### Option 1: GUI (Recommended)
Double-click `Launch_Translator.bat` or run:
```bash
python launch_translator.py
```

### Option 2: Command Line
```bash
python article_translator.py "URL" -o "output_folder"
```

## ✨ Features

- **🎯 Perfect Translation**: High-quality Slovak → Czech translation with technical term preservation
- **📝 HTML Structure Preservation**: Maintains all formatting, tags, and structure
- **🔧 Perfect Spacing**: Bulletproof spacing around `<strong>`, `<em>`, and other HTML tags
- **🖼️ Automatic Image Processing**: Downloads and organizes all article images
- **🎨 CTA Link Replacement**: Intelligently updates Slovak links to Czech equivalents
- **📊 SEO Metadata**: Translates titles, descriptions, and keywords
- **🏢 CMS Ready**: Generates clean output perfect for Shoptet and other CMS platforms
- **🎤 User-Friendly GUI**: Easy-to-use graphical interface
- **📁 Organized Output**: Each translation in its own timestamped folder

## 📁 Output Structure

Each translation creates a timestamped folder containing:
- `content.html` - Clean article content (ready for CMS)
- `seo_metadata.txt` - Title, description, keywords
- `header_image.jpg` - Main article image
- `images/` - Content images folder
- `README.txt` - Usage instructions

## 🎯 How to Use

1. **Launch the GUI**:
   - Double-click `Launch_Translator.bat`
   - Or run `python launch_translator.py`

2. **Enter URL**: 
   - Paste Slovak article URL (e.g., from softwareshop.sk)
   - Click "Paste" to get from clipboard

3. **Set Output Folder**:
   - Choose where to save translated articles
   - Default: `translated_articles` folder

4. **Click "Translate Article"**:
   - Watch progress in real-time
   - Get notified when complete

5. **Use Results**:
   - Copy SEO metadata for title/description
   - Upload header image as article cover
   - Paste `content.html` into your CMS
   - Upload images from `images/` folder

## 🔧 Technical Details

### Supported Sites
- softwareshop.sk blog articles
- Any similar Slovak website structure

### Link Replacement
Automatically detects software topics and updates links:
- `/kontakty/` → `/konzultace/`
- `/kurzy/` → `/kurzy/` (with software-specific paths)
- `/licencie/` → `/licence/`

### Software Detection
Recognizes and handles:
- SketchUp
- D5 Render
- ArchiCAD
- Revit
- Rhino
- 3ds Max
- Blender
- Lumion
- Twinmotion
- V-Ray
- Corona Render
- Cinema 4D

## 📝 Example Usage

### GUI Method
1. Open GUI: `Launch_Translator.bat`
2. Paste URL: `https://www.softwareshop.sk/blog/ako-prepojit-sketchup-s-d5-render-za-3-minuty/`
3. Click "Translate Article"
4. Wait for completion
5. Open output folder

### Command Line Method
```bash
python article_translator.py "https://www.softwareshop.sk/blog/ako-prepojit-sketchup-s-d5-render-za-3-minuty/" -o "my_translations"
```

## ⚙️ Requirements

- Python 3.6+
- Required packages: `requests`, `beautifulsoup4`, `lxml`

Install dependencies:
```bash
pip install requests beautifulsoup4 lxml
```

## 🐛 Troubleshooting

### Common Issues

**"Module not found" error**:
```bash
pip install requests beautifulsoup4 lxml
```

**Unicode/encoding errors**:
- The tool automatically handles Slovak/Czech characters
- Uses UTF-8 encoding throughout

**Translation incomplete**:
- Some Slovak words might not be in dictionary
- Translation quality improves with usage

**Images not downloading**:
- Check internet connection
- Some SVG placeholders are normal (skipped)

## 🔄 Updates

The translator includes an extensive Slovak-Czech dictionary that can be expanded. To add new translations, edit the `translations` dictionary in `article_translator.py`.

## 📞 Support

For issues or improvements, check the translation log in the GUI for detailed error messages.

---

Created 2025-09-18 | Slovak → Czech Article Translation Tool

Automated tool to translate articles from Slovak websites to Czech while preserving HTML structure, images, and SEO metadata. Perfect for Shoptet CMS workflows.

## 🚀 Features

- **Automatic Translation**: Slovak to Czech with comprehensive dictionary
- **HTML Structure Preservation**: All tags, attributes, and formatting maintained
- **Image Processing**: Downloads and processes all article images
- **SEO Metadata Translation**: Titles, descriptions, keywords, and meta tags
- **Shoptet Ready**: Generates output compatible with Shoptet CMS
- **Batch Processing**: Handle multiple articles at once
- **Error Handling**: Robust error handling with detailed reports

## 📦 Installation

1. Install Python 3.8+ if not already installed
2. Install required packages:

```bash
pip install -r requirements.txt
```

## 🎯 Quick Start

### Single Article Translation

```bash
python article_translator.py "https://example-slovak-site.sk/article"
```

### With Custom Output Directory

```bash
python article_translator.py "https://example.sk/article" -o my_translations
```

### Verbose Output

```bash
python article_translator.py "https://example.sk/article" -v
```

## 📚 Batch Processing

### Multiple URLs from Command Line

```bash
python batch_translator.py -u "https://site1.sk/article1" "https://site2.sk/article2"
```

### From Text File

Create `urls.txt` with one URL per line:
```
https://example.sk/article1
https://example.sk/article2
https://example.sk/article3
```

Then run:
```bash
python batch_translator.py -f urls.txt
```

### From CSV File

Create `articles.csv`:
```csv
URL,Title,Category
https://example.sk/article1,Article 1,Tech
https://example.sk/article2,Article 2,Design
```

Then run:
```bash
python batch_translator.py -c articles.csv
```

## 📁 Output Structure

Each translation creates:

```
translated_articles/
├── article_czech_20250118_120000.html     # Translated HTML
├── metadata_czech_20250118_120000.json    # SEO metadata + info
├── shoptet_article_20250118_120000.html   # Shoptet-ready format
└── images/                                # Downloaded images
    ├── image1.jpg
    └── image2.png
```

## 🔧 Configuration

### Translation Dictionary

The translator uses a comprehensive Slovak-Czech dictionary in `article_translator.py`. You can extend it by adding entries to the `translations` dictionary:

```python
self.translations = {
    'slovenské_slovo': 'české_slovo',
    # Add more translations here
}
```

### Article Content Detection

The script automatically detects article content using common selectors:
- `article`
- `.article-content`
- `.post-content`
- `.entry-content`
- `#content`
- `.content`
- `main`

## 📊 Generated Files

### 1. HTML File (`article_czech_*.html`)
Clean translated HTML content ready for use.

### 2. Metadata File (`metadata_czech_*.json`)
```json
{
  "metadata": {
    "title": "Translated title",
    "description": "Translated description",
    "keywords": "translated, keywords",
    "author": "Author name",
    "cover_image": "https://..."
  },
  "images": [
    {
      "original_url": "https://...",
      "local_path": "/path/to/image.jpg",
      "filename": "image.jpg"
    }
  ],
  "translation_info": {
    "source_language": "Slovak",
    "target_language": "Czech",
    "translator": "SlovakCzechTranslator v1.0"
  }
}
```

### 3. Shoptet File (`shoptet_article_*.html`)
HTML with Shoptet-specific comments for easy import:
```html
<!-- Shoptet Article Import -->
<!-- Title: Translated Title -->
<!-- Description: Translated Description -->
<!-- Keywords: translated, keywords -->

<h1>Translated Content...</h1>
...
```

## 🛠️ Advanced Usage

### Custom Output Directory

```bash
python article_translator.py "https://example.sk/article" -o "/path/to/output"
```

### Batch Processing with Custom Settings

```bash
python batch_translator.py -c articles.csv -o batch_output -v
```

## 🚨 Error Handling

The translator handles various scenarios:
- Network connectivity issues
- Invalid URLs
- Missing images
- Malformed HTML
- Translation failures

All errors are logged and reported in the batch processing report.

## 📈 Translation Quality

The translator includes:
- **500+ translation pairs** covering common Slovak-Czech differences
- **Word boundary detection** to avoid partial matches
- **Case-insensitive matching**
- **Phrase translation** for common expressions
- **HTML attribute translation** (alt text, titles, etc.)

## 🎛️ Shoptet Integration

### Import to Shoptet CMS

1. Use the `shoptet_article_*.html` file
2. Copy the translated content
3. In Shoptet admin:
   - Create new article
   - Use translated title from comments
   - Paste HTML content
   - Set SEO metadata from comments
   - Upload processed images

### CTA Button Links

The translator automatically handles CTA buttons and can be configured to update links:
- Course links → your Czech course pages  
- Product links → your Czech product pages
- Contact links → your Czech contact pages

## 🔍 Troubleshooting

### Common Issues

**Import Error**: Make sure all requirements are installed
```bash
pip install -r requirements.txt
```

**Network Errors**: Check internet connection and URL validity

**Encoding Issues**: All files are saved with UTF-8 encoding

**Missing Images**: Check if images are accessible from the source URL

## 📝 Examples

### Example 1: Single Article
```bash
python article_translator.py "https://softwareshop.sk/blog/d5-render-article"
```

### Example 2: Batch Processing
```bash
python batch_translator.py -u \
  "https://site.sk/article1" \
  "https://site.sk/article2" \
  "https://site.sk/article3" \
  -o batch_results -v
```

### Example 3: From CSV with Custom Output
```bash
python batch_translator.py -c my_articles.csv -o shoptet_imports
```

## 📄 License

**Non-Commercial Use License**

This software is available for **free non-commercial use only**. Key points:

✅ **Allowed:**
- Personal use and learning
- Educational purposes  
- Non-profit organizations
- Open source projects
- Research and development

❌ **Not Allowed Without Permission:**
- Commercial use or profit generation
- Selling the software or charging fees
- Incorporating into commercial products
- Using in commercial services

📧 **Commercial Licensing:** For commercial use, contact **labovskyviktor@gmail.com**

See the [LICENSE](LICENSE) file for complete terms and conditions.

## 📞 Support

For issues or feature requests, check the error logs and batch reports generated by the translator. The verbose mode (`-v`) provides additional debugging information.

Contact: **labovskyviktor@gmail.com**

## 📄 Updates

The translation dictionary can be easily updated by modifying the `translations` dictionary in `article_translator.py`. Consider backing up your custom modifications before updates.

---

**Perfect for Shoptet workflows!** 🛒 Generate Czech content from Slovak sources automatically.

*Copyright © 2025 Viktor Labovský. All rights reserved.*

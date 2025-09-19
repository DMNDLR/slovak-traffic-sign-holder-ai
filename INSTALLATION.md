# 🚀 Slovak-Czech-Translator - Windows Installation

## 📦 Quick Installation (Recommended)

### Option 1: Direct Executable (No Python Required)

1. **Download** the `Slovak-Czech-Translator.exe` file
2. **Double-click** to run - that's it! 🎉

> ✅ **No Python installation required**  
> ✅ **No dependencies to install**  
> ✅ **Runs on any Windows 10/11 computer**

### Option 2: Install from Source (Python Required)

If you have Python 3.8+ installed:

```bash
# Clone the repository
git clone https://github.com/labovskyviktor-design/slovak-czech-article-translator.git
cd slovak-czech-article-translator

# Install dependencies
pip install -r requirements.txt

# Run the translator
python article_translator.py
```

## 📋 System Requirements

- **Operating System**: Windows 10 or Windows 11
- **Memory**: 512MB RAM minimum
- **Storage**: 50MB free space
- **Internet**: Required for translation and image downloads

## 🎯 First Run

1. **Launch** the application by double-clicking `Slovak-Czech-Translator.exe`
2. **Enter** the Slovak article URL in the input field
3. **Click "Translate Article"** button
4. **Wait** for the translation to complete (usually 1-2 minutes)
5. **Find** your translated article in the automatically created output folder

## 📁 Output Location

The translator creates a new folder for each translation:
```
output/
└── article_YYYYMMDD_HHMMSS/
    ├── translated_article.html
    ├── images/
    └── article_info.txt
```

## 🔧 Troubleshooting

### Application Won't Start
- **Windows Defender Warning**: Click "More info" → "Run anyway"
- **Missing DLL Error**: Update Windows to the latest version
- **Slow Startup**: The first run takes longer (30-60 seconds)

### Translation Issues
- **Timeout Error**: Check your internet connection
- **Invalid URL**: Make sure the URL starts with `http://` or `https://`
- **Empty Output**: The source article might have unusual formatting

### Performance Tips
- **Close other applications** during translation for faster processing
- **Check disk space** - ensure at least 100MB free for images
- **Stable internet** connection recommended for Google Translate API

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Restart the application
3. Contact: labovskyviktor@gmail.com

## 🔄 Updates

To get the latest version:
1. Download the newest `Slovak-Czech-Translator.exe` 
2. Replace your old file
3. No uninstall needed!

---
**Created by Viktor Labovský** | [GitHub Repository](https://github.com/labovskyviktor-design/slovak-czech-article-translator)
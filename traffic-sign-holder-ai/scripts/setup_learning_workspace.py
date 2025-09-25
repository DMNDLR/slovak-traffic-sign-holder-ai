"""
Setup learning workspace for Slovak traffic sign holder detection.
Imports photos from desktop and prepares them for AI training.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Add src directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from import_photos import (
    copy_and_organize_photos, 
    create_import_manifest,
    find_image_files
)
from slovak_signs_database import get_database

def setup_workspace():
    """Setup the complete learning workspace."""
    print("=== Slovak Traffic Sign Holder AI - Learning Workspace Setup ===")
    print()
    
    # Paths configuration
    BASE_DIR = Path(__file__).parent.parent
    SOURCE_DIR = Path(r"C:\Users\adamm\Desktop\holders-photos")
    DATA_DIR = BASE_DIR / "data"
    
    print(f"Base directory: {BASE_DIR}")
    print(f"Source photos: {SOURCE_DIR}")
    print(f"Data directory: {DATA_DIR}")
    print()
    
    # Check if source directory exists
    if not SOURCE_DIR.exists():
        print(f"❌ ERROR: Source directory does not exist: {SOURCE_DIR}")
        print("Please make sure the holders-photos folder is on your desktop.")
        return False
    
    # Count available photos
    image_files = find_image_files(str(SOURCE_DIR))
    print(f"📸 Found {len(image_files)} images in source directory")
    
    if len(image_files) == 0:
        print("❌ No image files found in source directory!")
        return False
    
    # Show sample of found files
    print("Sample files found:")
    for i, file in enumerate(image_files[:5]):
        print(f"  {i+1}. {Path(file).name}")
    if len(image_files) > 5:
        print(f"  ... and {len(image_files) - 5} more")
    print()
    
    # Create necessary directories
    directories = [
        DATA_DIR / "raw",
        DATA_DIR / "processed", 
        DATA_DIR / "annotations",
        DATA_DIR / "training_samples",
        BASE_DIR / "output" / "detections",
        BASE_DIR / "output" / "training_data",
        BASE_DIR / "output" / "analysis_results"
    ]
    
    print("📁 Creating directory structure...")
    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {dir_path.relative_to(BASE_DIR)}")
    
    print()
    
    # Import photos
    print("📂 Importing photos...")
    try:
        processed_files = copy_and_organize_photos(
            source_dir=str(SOURCE_DIR),
            target_dir=str(DATA_DIR / "raw"),
            create_subdirs=False  # Keep all in one directory for easier processing
        )
        
        # Create import manifest
        manifest_path = DATA_DIR / "import_manifest.json"
        manifest = create_import_manifest(processed_files, str(manifest_path))
        
        print(f"✓ Successfully imported {manifest['successful_imports']} photos")
        if manifest['failed_imports'] > 0:
            print(f"⚠️  Failed to import {manifest['failed_imports']} files")
        
    except Exception as e:
        print(f"❌ Error during photo import: {e}")
        return False
    
    # Setup Slovak signs database
    print("🗃️  Setting up Slovak traffic signs database...")
    try:
        signs_db = get_database()
        
        # Export database to JSON for reference
        db_export = signs_db.export_to_json()
        db_path = DATA_DIR / "slovak_signs_database.json"
        
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(db_export, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Slovak signs database ready with {len(signs_db.signs)} signs")
        print(f"  📝 Database exported to: {db_path.relative_to(BASE_DIR)}")
        
        # Print categories summary
        categories = signs_db.get_sign_categories()
        print("  📊 Sign categories:")
        for category, codes in categories.items():
            print(f"    - {category}: {len(codes)} signs")
        
    except Exception as e:
        print(f"❌ Error setting up signs database: {e}")
        return False
    
    # Create initial workspace configuration
    config = {
        "workspace_created": datetime.now().isoformat(),
        "source_directory": str(SOURCE_DIR),
        "total_photos": len(image_files),
        "successfully_imported": manifest['successful_imports'],
        "failed_imports": manifest['failed_imports'],
        "signs_database_version": "1.0",
        "total_signs_in_db": len(signs_db.signs),
        "directories": {
            "raw_photos": str(DATA_DIR / "raw"),
            "processed": str(DATA_DIR / "processed"),
            "annotations": str(DATA_DIR / "annotations"), 
            "training_samples": str(DATA_DIR / "training_samples"),
            "detections": str(BASE_DIR / "output" / "detections"),
            "training_data": str(BASE_DIR / "output" / "training_data"),
            "analysis_results": str(BASE_DIR / "output" / "analysis_results")
        }
    }
    
    config_path = BASE_DIR / "workspace_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"⚙️  Workspace configuration saved: {config_path.relative_to(BASE_DIR)}")
    print()
    
    # Create README with next steps
    readme_content = f"""# Slovak Traffic Sign Holder AI - Learning Workspace

## Setup Summary
- **Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Photos imported:** {manifest['successful_imports']} out of {len(image_files)}
- **Signs database:** {len(signs_db.signs)} Slovak traffic signs

## Directory Structure
```
traffic-sign-holder-ai/
├── data/
│   ├── raw/                    # Original imported photos ({manifest['successful_imports']} files)
│   ├── processed/              # Processed images (will be created during analysis)
│   ├── annotations/            # Manual annotations (for training data)
│   ├── training_samples/       # Prepared training samples
│   └── import_manifest.json    # Photo import details
├── output/
│   ├── detections/             # Detection results (JSON + images with bboxes)
│   ├── training_data/          # Exported training data (COCO, YOLO formats)
│   └── analysis_results/       # Analysis reports and statistics
├── src/                        # Source code
├── models/                     # Trained AI models
└── scripts/                    # Utility scripts
```

## Next Steps

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Run Initial Analysis
```powershell
python scripts/analyze_photos.py
```

### 3. Review and Annotate
- Review detection results in `output/detections/`
- Add manual annotations in `data/annotations/`

### 4. Train Model
```powershell
python scripts/train_model.py
```

## Slovak Signs Database
The system includes a comprehensive database of Slovak traffic signs with:
- Sign codes (101, 201, 250, etc.)
- Slovak and English names
- Expected text patterns for OCR
- Visual characteristics (shape, colors)

See `data/slovak_signs_database.json` for the complete reference.

## Data Schema
All detection results follow the structured schema defined in `src/data_schema.py`:
- Holder detection with green bounding boxes
- Material, owner, base type, and orientation classification
- OCR text extraction from sign plates
- Confidence scores for all predictions
- GPS coordinates (if available in photo metadata)

Ready for GIS integration and model training! 🚀
"""
    
    readme_path = BASE_DIR / "README_WORKSPACE.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("📋 Created workspace README with next steps")
    print()
    
    # Final summary
    print("🎉 LEARNING WORKSPACE SETUP COMPLETE!")
    print()
    print("📊 Summary:")
    print(f"  ✓ Imported {manifest['successful_imports']} photos")
    print(f"  ✓ Slovak signs database with {len(signs_db.signs)} signs ready")
    print(f"  ✓ Directory structure created")
    print(f"  ✓ Configuration files saved")
    print()
    print("🚀 Ready to start AI training!")
    print(f"   Next: Run 'pip install -r requirements.txt' to install dependencies")
    print(f"   Then: Run detection analysis on your photos")
    
    return True

def show_workspace_status():
    """Show current workspace status."""
    BASE_DIR = Path(__file__).parent.parent
    config_path = BASE_DIR / "workspace_config.json"
    
    if not config_path.exists():
        print("❌ Workspace not set up yet. Run setup_workspace() first.")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("=== Current Workspace Status ===")
    print(f"Created: {config['workspace_created']}")
    print(f"Photos: {config['successfully_imported']} imported")
    print(f"Signs DB: {config['total_signs_in_db']} Slovak signs")
    
    # Check directory contents
    raw_dir = Path(config['directories']['raw_photos'])
    if raw_dir.exists():
        photo_count = len([f for f in raw_dir.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        print(f"Raw photos: {photo_count} files")
    
    print("\n📁 Directory status:")
    for name, path in config['directories'].items():
        path_obj = Path(path)
        status = "✓ exists" if path_obj.exists() else "❌ missing"
        if path_obj.exists() and path_obj.is_dir():
            file_count = len(list(path_obj.iterdir()))
            if file_count > 0:
                status += f" ({file_count} items)"
        print(f"  {name}: {status}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        show_workspace_status()
    else:
        setup_workspace()
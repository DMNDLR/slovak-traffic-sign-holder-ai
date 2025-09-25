"""
Photo import utility for traffic sign holder detection project.
Processes photos from source directory and prepares them for analysis.
"""

import os
import shutil
import json
from pathlib import Path
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import hashlib

def get_image_metadata(image_path: str) -> Dict:
    """Extract comprehensive metadata from image file."""
    try:
        with Image.open(image_path) as img:
            # Basic image info
            metadata = {
                "filename": os.path.basename(image_path),
                "file_path": str(image_path),
                "image_width": img.width,
                "image_height": img.height,
                "file_size_bytes": os.path.getsize(image_path),
                "format": img.format,
                "mode": img.mode
            }
            
            # File timestamps
            stat = os.stat(image_path)
            metadata["creation_date"] = datetime.fromtimestamp(stat.st_ctime).isoformat()
            metadata["modification_date"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
            
            # Generate file hash for uniqueness
            with open(image_path, 'rb') as f:
                metadata["file_hash"] = hashlib.md5(f.read()).hexdigest()
            
            # Extract EXIF data if available
            exif_data = {}
            gps_data = {}
            
            if hasattr(img, '_getexif') and img._getexif():
                exif = img._getexif()
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    
                    # GPS coordinates
                    if tag == 'GPSInfo':
                        for gps_tag in value:
                            gps_tag_name = ExifTags.GPSTAGS.get(gps_tag, gps_tag)
                            gps_data[gps_tag_name] = value[gps_tag]
                    
                    # Other useful EXIF data
                    elif tag in ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized', 
                               'Make', 'Model', 'Software', 'Orientation', 
                               'XResolution', 'YResolution', 'ExposureTime', 'FNumber']:
                        exif_data[tag] = str(value)
            
            metadata["exif_data"] = exif_data
            metadata["gps_data"] = gps_data
            
            # Convert GPS coordinates to decimal degrees if available
            if gps_data:
                try:
                    lat, lng = convert_gps_to_decimal(gps_data)
                    if lat is not None and lng is not None:
                        metadata["latitude"] = lat
                        metadata["longitude"] = lng
                except:
                    pass
                    
            return metadata
            
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return {
            "filename": os.path.basename(image_path),
            "file_path": str(image_path),
            "error": str(e)
        }

def convert_gps_to_decimal(gps_data: Dict) -> Tuple[Optional[float], Optional[float]]:
    """Convert GPS coordinates from EXIF format to decimal degrees."""
    try:
        lat_ref = gps_data.get('GPSLatitudeRef')
        lat = gps_data.get('GPSLatitude')
        lng_ref = gps_data.get('GPSLongitudeRef') 
        lng = gps_data.get('GPSLongitude')
        
        if not all([lat_ref, lat, lng_ref, lng]):
            return None, None
            
        # Convert to decimal
        lat_decimal = lat[0] + lat[1]/60 + lat[2]/3600
        if lat_ref == 'S':
            lat_decimal = -lat_decimal
            
        lng_decimal = lng[0] + lng[1]/60 + lng[2]/3600
        if lng_ref == 'W':
            lng_decimal = -lng_decimal
            
        return lat_decimal, lng_decimal
        
    except:
        return None, None

def find_image_files(directory: str, extensions: List[str] = None) -> List[str]:
    """Find all image files in directory and subdirectories."""
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    
    image_files = []
    directory_path = Path(directory)
    
    if not directory_path.exists():
        print(f"Directory does not exist: {directory}")
        return image_files
    
    for ext in extensions:
        # Case insensitive search
        image_files.extend(directory_path.rglob(f"*{ext}"))
        image_files.extend(directory_path.rglob(f"*{ext.upper()}"))
    
    return [str(f) for f in image_files]

def copy_and_organize_photos(source_dir: str, target_dir: str, create_subdirs: bool = True) -> List[Dict]:
    """Copy photos from source to target directory and extract metadata."""
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    # Create target directory
    target_path.mkdir(parents=True, exist_ok=True)
    
    # Find all image files
    image_files = find_image_files(source_dir)
    print(f"Found {len(image_files)} image files in {source_dir}")
    
    processed_files = []
    
    for i, image_file in enumerate(image_files):
        try:
            # Extract metadata
            metadata = get_image_metadata(image_file)
            
            # Generate new filename with index
            original_name = Path(image_file).stem
            extension = Path(image_file).suffix
            new_filename = f"holder_{i+1:04d}_{original_name}{extension}"
            
            # Create subdirectory based on date if requested
            if create_subdirs and "creation_date" in metadata:
                try:
                    date_obj = datetime.fromisoformat(metadata["creation_date"].replace('Z', '+00:00'))
                    subdir = date_obj.strftime("%Y-%m-%d")
                    target_file_dir = target_path / subdir
                    target_file_dir.mkdir(exist_ok=True)
                except:
                    target_file_dir = target_path
            else:
                target_file_dir = target_path
            
            target_file_path = target_file_dir / new_filename
            
            # Copy file
            shutil.copy2(image_file, target_file_path)
            
            # Update metadata with new path
            metadata["original_path"] = image_file
            metadata["processed_path"] = str(target_file_path)
            metadata["processed_filename"] = new_filename
            metadata["processing_timestamp"] = datetime.now().isoformat()
            
            processed_files.append(metadata)
            
            print(f"Processed {i+1}/{len(image_files)}: {original_name}")
            
        except Exception as e:
            print(f"Error processing {image_file}: {e}")
            processed_files.append({
                "original_path": image_file,
                "error": str(e),
                "processing_timestamp": datetime.now().isoformat()
            })
    
    return processed_files

def create_import_manifest(processed_files: List[Dict], output_path: str):
    """Create a JSON manifest of all imported files."""
    manifest = {
        "import_timestamp": datetime.now().isoformat(),
        "total_files": len(processed_files),
        "successful_imports": len([f for f in processed_files if "error" not in f]),
        "failed_imports": len([f for f in processed_files if "error" in f]),
        "files": processed_files
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"Import manifest saved to: {output_path}")
    return manifest

def main():
    """Main import function."""
    # Configuration
    SOURCE_DIR = r"C:\Users\adamm\Desktop\holders-photos"
    TARGET_DIR = r"C:\Users\adamm\Documents\github\slovak-czech-article-translator\traffic-sign-holder-ai\data\raw"
    MANIFEST_PATH = r"C:\Users\adamm\Documents\github\slovak-czech-article-translator\traffic-sign-holder-ai\data\import_manifest.json"
    
    print("=== Traffic Sign Holder Photo Import ===")
    print(f"Source directory: {SOURCE_DIR}")
    print(f"Target directory: {TARGET_DIR}")
    print()
    
    # Check if source directory exists
    if not Path(SOURCE_DIR).exists():
        print(f"ERROR: Source directory does not exist: {SOURCE_DIR}")
        return
    
    # Process and copy files
    processed_files = copy_and_organize_photos(SOURCE_DIR, TARGET_DIR)
    
    # Create manifest
    manifest = create_import_manifest(processed_files, MANIFEST_PATH)
    
    print(f"\n=== Import Summary ===")
    print(f"Total files found: {manifest['total_files']}")
    print(f"Successfully imported: {manifest['successful_imports']}")
    print(f"Failed imports: {manifest['failed_imports']}")
    
    if manifest['failed_imports'] > 0:
        print("\nFailed files:")
        for f in processed_files:
            if "error" in f:
                print(f"  - {f['original_path']}: {f['error']}")
    
    print(f"\nFiles imported to: {TARGET_DIR}")
    print(f"Manifest saved to: {MANIFEST_PATH}")

if __name__ == "__main__":
    main()
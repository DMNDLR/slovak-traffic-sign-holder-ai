"""
🎯 Slovak Traffic Sign Holder Annotation App Launcher

Simple launcher with error handling to test the annotation app.
"""

import sys
import traceback
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import tkinter as tk
        print("  ✅ tkinter - OK")
    except ImportError as e:
        print(f"  ❌ tkinter - FAILED: {e}")
        return False
    
    try:
        import cv2
        print("  ✅ opencv-python - OK")
    except ImportError as e:
        print(f"  ❌ opencv-python - FAILED: {e}")
        return False
    
    try:
        from PIL import Image, ImageTk
        print("  ✅ Pillow - OK")
    except ImportError as e:
        print(f"  ❌ Pillow - FAILED: {e}")
        return False
    
    try:
        import numpy as np
        print("  ✅ numpy - OK")
    except ImportError as e:
        print(f"  ❌ numpy - FAILED: {e}")
        return False
    
    return True

def launch_app():
    """Launch the annotation app with error handling."""
    try:
        print("🚀 Launching Slovak Traffic Sign Holder Annotation App...")
        print()
        print("Features:")
        print("  📸 Browse through your 6,094 imported photos")
        print("  🎯 Draw bounding boxes around holders (green) and signs (blue)")
        print("  🏗️ Define holder attributes (material, owner, base type, orientation)")
        print("  🚦 Match signs with Slovak traffic codes (101, 201, 250, etc.)")
        print("  📝 Add notes about what's correct/wrong")
        print("  💾 Save annotations for AI training")
        print()
        print("Controls:")
        print("  • Left click & drag: Draw new bounding box")
        print("  • Left click: Select existing box") 
        print("  • Right click: Delete/Edit menu")
        print("  • Radio buttons: Switch between Holder/Sign drawing mode")
        print()
        
        # Import the app
        from annotation_app import AnnotationApp
        import tkinter as tk
        
        # Create and run
        root = tk.Tk()
        app = AnnotationApp(root)
        
        print("✅ App launched successfully!")
        print("📋 The annotation window should now be open.")
        print("🔄 Use Previous/Next buttons to browse photos")
        print("💡 Start by drawing a green box around a holder, then set its attributes")
        print()
        
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\n👋 App closed by user (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ Error launching app: {e}")
        print("\nFull error details:")
        traceback.print_exc()
        print("\n💡 Try:")
        print("  pip install opencv-python pillow numpy")

def main():
    """Main launcher function."""
    print("🇸🇰 Slovak Traffic Sign Holder Annotation App Launcher")
    print("=" * 55)
    print()
    
    # Test imports first
    if not test_imports():
        print("\n❌ Missing dependencies. Please install:")
        print("  pip install opencv-python pillow numpy")
        return
    
    print("  ✅ All dependencies available!")
    print()
    
    # Check workspace
    workspace_config = Path("workspace_config.json")
    if workspace_config.exists():
        print("  ✅ Workspace configuration found")
    else:
        print("  ⚠️  Workspace config not found - you can still open photos manually")
    
    print()
    
    # Launch app
    input("Press Enter to launch the annotation app...")
    launch_app()

if __name__ == "__main__":
    main()
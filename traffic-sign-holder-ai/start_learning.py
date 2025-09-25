"""
🚀 Slovak Traffic Sign Holder AI - Start Learning Process

Simple script to begin AI training on your photos.
Run this to start the complete learning pipeline!
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent / "scripts"))

from learning_pipeline import main

if __name__ == "__main__":
    print("🇸🇰 Slovak Traffic Sign Holder AI Training")
    print("==========================================")
    print()
    print("This will train AI models using your 6,094 imported photos to:")
    print("✅ Detect traffic sign holders with green bounding boxes")  
    print("✅ Classify materials (metal, concrete, wood, plastic, etc.)")
    print("✅ Identify owner (city, municipality, other)")
    print("✅ Determine base type (pole, portal, guardrail, building, etc.)")
    print("✅ Recognize Slovak traffic signs with proper codes (101, 201, 250, etc.)")
    print("✅ Extract text from sign plates using OCR")
    print("✅ Generate GIS-ready structured output")
    print()
    print("The learning process has 5 phases:")
    print("📊 Phase 1: Initial Photo Analysis (computer vision)")
    print("🔍 Phase 2: Feature Extraction (ML feature engineering)")
    print("🧠 Phase 3: AI Model Training (train neural networks)")
    print("✅ Phase 4: Model Validation (test accuracy)")
    print("🎯 Phase 5: Deployment Preparation (package for production)")
    print()
    
    # Run the learning pipeline
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify spacing fixes work correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from article_translator import SlovakCzechTranslator
import re

def test_spacing_fixes():
    """Test the spacing fix methods with problematic patterns"""
    
    translator = SlovakCzechTranslator()
    
    # Test cases that were problematic
    test_cases = [
        "nástroj na<strong>fotorealistické vykreslování</strong>v reálném",
        "SketchUp patří mezi nejoblíbenější nástroje na<strong>3D modelování</strong>.",
        "moderný nástroj na<strong>Fotorealistické vykreslování</strong>V reálnom čase",
        "získate silnú kombináciu pro<strong>rychlé modelování</strong>a efektívnu prácu",
        "doplnok<strong>D5 Converter</strong>slúži na priame spojenie",
        "funkciu<strong>LiveSync</strong>od tohto momentu",
        "<!-- CTA blok: kontaktujte nás -->",
        "<!-- CTA blok: kurz -->",
    ]
    
    print("TESTING SPACING AND COMMENT FIXES")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases):
        print(f"\\nTest {i+1}: {test_case[:50]}...")
        
        # Apply the force_strong_tag_spacing method
        fixed = translator.force_strong_tag_spacing(test_case)
        
        # Also test comment removal (simulate clean_html_content regex)
        fixed = re.sub(r'<!--.*?-->', '', fixed, flags=re.DOTALL)
        
        print(f"Fixed: {fixed}")
        
        # Check if spacing issues are resolved
        if "<strong>" in fixed and "</strong>" in fixed:
            has_space_before = not re.search(r'[^\s]<strong', fixed)
            has_space_after = not re.search(r'</strong>[^\s]', fixed)
            
            if has_space_before and has_space_after:
                print("✅ PASS: Proper spacing around <strong> tags")
            else:
                print("❌ FAIL: Still has spacing issues")
                if not has_space_before:
                    print("   - Missing space before <strong>")
                if not has_space_after:
                    print("   - Missing space after </strong>")
        else:
            print("✅ PASS: No <strong> tags or comments removed")

if __name__ == "__main__":
    test_spacing_fixes()
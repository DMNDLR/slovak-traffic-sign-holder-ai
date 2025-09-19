#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Slovak to Czech Article Translator for Shoptet
Automatically translates articles from Slovak websites to Czech while preserving HTML structure,
images, and SEO metadata.
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
import argparse
from datetime import datetime
from urllib.parse import urljoin, urlparse
import re
import time
from googletrans import Translator
from pathlib import Path

def safe_print(text):
    """Print text safely, handling Unicode encoding issues on Windows"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback: encode to ASCII with replacement characters
        print(text.encode('ascii', errors='replace').decode('ascii'))

class SlovakCzechTranslator:
    def __init__(self):
        self.translator = Translator()
        self.max_retries = 3
        self.retry_delay = 1  # seconds
        
        # Keep some critical technical terms and specific translations that need precision
        self.critical_terms = {
            # Software/3D specific terms that need precise translation
            'SketchUp': 'SketchUp',  # Keep brand names as-is
            'skicip': 'SketchUp',  # Fix common mistranslation
            'skicipu': 'SketchUp',  # Fix declension
            'skicipup': 'SketchUp',  # Fix another variant
            'D5 Render': 'D5 Render',
            'vykreslování D5': 'D5 Render',  # Fix back-translation
            'vykreslení D5': 'D5 Render',  # Fix another variant
            'LiveSync': 'LiveSync',
            'Lifesync': 'LiveSync',  # Fix capitalization
            'D5 Converter': 'D5 Converter',
            'Převodník D5': 'D5 Converter',  # Fix back-translation
            'převodníku D5': 'D5 Converter',  # Fix declension
            'PBR materiály': 'PBR materiály',
            'HDRI mapy': 'HDRI mapy',
            'LED pásy': 'LED pásy',
            'LED proužky': 'LED pásy',  # Fix mistranslation
            'fotorealistické': 'fotorealistické',
            'Fotorealistické': 'Fotorealistické',
            '360°': '360°',
            '4K': '4K',
            
            # CTA and link specific terms
            'konzultace': 'konzultace',
            'konzultaci': 'konzultaci',
            'konzultovat': 'konzultovat',
            'kontaktujte': 'kontaktujte',
            'Kontaktuj': 'Kontaktuj',
            'kurz': 'kurz',
            'kurzu': 'kurz',
            'Přihlásit se na kurz': 'Přihlásit se na kurz',
            'Přihlaste se do kurzu': 'Přihlásit se na kurz',
            
            # Common phrases that should be kept consistent
            'za 3 minuty': 'za 3 minuty',
            'za pár minut': 'za pár minut',
            'v reálném čase': 'v reálném čase',
            'bez kompromisů': 'bez kompromisů',
            'profesionální účely': 'profesionální účely',
            
            # Fix common mistranslations
            'modelování': 'modelování',
            'vizualizace': 'vizualizace',
            'kombinace': 'kombinace',
            'nástroj': 'nástroj',
            'nástroje': 'nástroje',
            'program': 'program',
            'programy': 'programy',
            'projekt': 'projekt',
            'projekty': 'projekty',
            'materiál': 'materiál',
            'materiály': 'materiály',
            'textury': 'textury',
            'osvětlení': 'osvětlení',
            'geometrie': 'geometrie',
            'komponenty': 'komponenty',
            'objekty': 'objekty',
            'kamery': 'kamery',
            'animace': 'animace',
            'export': 'export',
            'rozlišení': 'rozlišení',
        }
    
    def preprocess_for_translation(self, text):
        """Replace HTML tags with placeholders to prevent Google Translate from damaging them"""
        if not text:
            return text
            
        # Store HTML tags in a dictionary and replace with safe placeholders
        self.html_replacements = {}
        counter = 0
        result = text
        
        # Find all HTML tags and replace with placeholders
        html_pattern = r'</?(?:strong|em|b|i|u|span)[^>]*>'
        
        def replace_tag(match):
            nonlocal counter
            tag = match.group(0)
            placeholder = f'HTMLTAG{counter}ENDTAG'
            self.html_replacements[placeholder] = tag
            counter += 1
            return f' {placeholder} '  # Add spaces around placeholder
        
        result = re.sub(html_pattern, replace_tag, result)
        
        # Clean up multiple spaces
        result = re.sub(r' {2,}', ' ', result)
        
        return result
    
    def restore_html_tags(self, text):
        """Restore HTML tags from placeholders after translation"""
        if not text or not hasattr(self, 'html_replacements'):
            return text
            
        result = text
        for placeholder, original_tag in self.html_replacements.items():
            result = result.replace(placeholder, original_tag)
        
        # AGGRESSIVE SPACING ENFORCEMENT FOR STRONG TAGS
        # Force space before every <strong> tag (any character followed by <strong>)
        result = re.sub(r'([a-zA-Z0-9\u00C0-\u017F.,;:!?\-])(<strong[^>]*>)', r'\1 \2', result)
        # Force space after every </strong> tag (</strong> followed by any character)
        result = re.sub(r'(</strong>)([a-zA-Z\u00C0-\u017F0-9.,;:!?\-])', r'\1 \2', result)
        
        # Also ensure spacing for other formatting tags
        # Ensure space before opening tags (em, b, i, u, span)
        result = re.sub(r'([a-zA-Z0-9\u00C0-\u017F.,;:!?\-])(<(?:em|b|i|u|span)[^>]*>)', r'\1 \2', result)
        # Ensure space after closing tags (em, b, i, u, span)
        result = re.sub(r'(</(?:em|b|i|u|span)>)([a-zA-Z\u00C0-\u017F0-9.,;:!?\-])', r'\1 \2', result)
        
        # Clean up any extra spaces that might have been introduced
        result = re.sub(r' {2,}', ' ', result)
        
        return result
    
    def translate_with_google(self, text):
        """Translate text using Google Translate API with retry logic"""
        if not text or not text.strip():
            return text
            
        # Preprocess text to add necessary spaces around HTML tags
        preprocessed_text = self.preprocess_for_translation(text)
            
        for attempt in range(self.max_retries):
            try:
                # Split long text into smaller chunks to avoid API limits
                if len(preprocessed_text) > 4500:  # Google Translate has ~5000 char limit
                    return self._translate_long_text(preprocessed_text)
                    
                result = self.translator.translate(preprocessed_text, src='sk', dest='cs')
                # Restore HTML tags after translation
                translated_text = self.restore_html_tags(result.text)
                return translated_text
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    safe_print(f"Translation attempt {attempt + 1} failed: {str(e)}. Retrying...")
                    time.sleep(self.retry_delay)
                else:
                    safe_print(f"Translation failed after {self.max_retries} attempts: {str(e)}")
                    return preprocessed_text  # Return preprocessed text if all attempts fail
    
    def _translate_long_text(self, text):
        """Translate long text by splitting into sentences"""
        # Split text into sentences
        sentences = re.split(r'([.!?]+\s*)', text)
        translated_parts = []
        
        current_chunk = ""
        for part in sentences:
            if len(current_chunk + part) < 4500:
                current_chunk += part
            else:
                if current_chunk:
                    # Preprocess each chunk before translation
                    preprocessed_chunk = self.preprocess_for_translation(current_chunk)
                    # Use direct API call to avoid recursion
                    try:
                        result = self.translator.translate(preprocessed_chunk, src='sk', dest='cs')
                        # Restore HTML tags after translation
                        translated_chunk = self.restore_html_tags(result.text)
                        translated_parts.append(translated_chunk)
                    except Exception as e:
                        safe_print(f"Failed to translate chunk: {str(e)}")
                        restored_chunk = self.restore_html_tags(preprocessed_chunk)
                        translated_parts.append(restored_chunk)  # Keep preprocessed with restored tags if translation fails
                current_chunk = part
                
        if current_chunk:
            # Preprocess final chunk before translation
            preprocessed_chunk = self.preprocess_for_translation(current_chunk)
            try:
                result = self.translator.translate(preprocessed_chunk, src='sk', dest='cs')
                # Restore HTML tags after translation
                translated_chunk = self.restore_html_tags(result.text)
                translated_parts.append(translated_chunk)
            except Exception as e:
                safe_print(f"Failed to translate final chunk: {str(e)}")
                restored_chunk = self.restore_html_tags(preprocessed_chunk)
                translated_parts.append(restored_chunk)
            
        return ''.join(translated_parts)
    
    def apply_critical_terms(self, text):
        """Apply critical term replacements that should override Google Translate"""
        if not text:
            return text
            
        result = text
        
        # Sort by length (longer first) to avoid partial replacements
        sorted_terms = sorted(self.critical_terms.items(), key=lambda x: len(x[0]), reverse=True)
        
        for slovak_term, czech_term in sorted_terms:
            # Use different patterns for different types of terms
            if any(char.isupper() for char in slovak_term) or slovak_term in ['SketchUp', 'D5 Render', 'LiveSync', 'D5 Converter']:
                # For brand names and proper nouns, use exact case matching
                result = result.replace(slovak_term, czech_term)
            else:
                # For common terms, use word boundaries with case-insensitive matching
                pattern = r'\b' + re.escape(slovak_term) + r'\b'
                result = re.sub(pattern, czech_term, result, flags=re.IGNORECASE)
            
        return result
    
    def translate_text(self, text):
        """Main translation method: Google Translate + critical terms"""
        if not text or not text.strip():
            return text
            
        # First apply Google Translate
        translated = self.translate_with_google(text)
        
        # Then apply critical terms to override any incorrect translations
        translated = self.apply_critical_terms(translated)
        
        # Fix HTML spacing issues (PRIORITY)
        translated = self.fix_html_spacing(translated)
        
        # Apply aggressive post-translation spacing fix
        translated = self.post_translation_spacing_fix(translated)
        
        # Fix capitalization
        translated = self.fix_capitalization(translated)
        
        # FINAL STEP: Force spacing around strong tags (ultra-aggressive)
        translated = self.force_strong_tag_spacing(translated)
        
        # ADDITIONAL FINAL PASS: Simple direct replacements
        translated = translated.replace('na<strong>', 'na <strong>')
        translated = translated.replace('</strong>V', '</strong> V')
        translated = translated.replace('</strong>T', '</strong> T')
        translated = translated.replace('</strong>A', '</strong> A')
        translated = translated.replace('</strong>I', '</strong> I')
        translated = translated.replace('</strong>O', '</strong> O')
        translated = translated.replace('</strong>U', '</strong> U')
        
        # ULTIMATE MULTIPLE-PASS FINAL SPACING FIX
        import re
        
        # Pass 1: Basic patterns
        translated = re.sub(r'([a-z])(<strong)', r'\1 \2', translated, flags=re.IGNORECASE)
        translated = re.sub(r'(</strong>)([a-z])', r'\1 \2', translated, flags=re.IGNORECASE)
        
        # Pass 2: Target specific problematic patterns
        problematic_before = ['na', 'pro', 'do', 'za', 'od', 'po', 'v', 's', 'k', 'o', 'se', 'na ', 'nástroje', 'při', 'před', 'nad', 'pod', 'mezi', 'bez', 'podle', 'během', 'kolem', 'nástroj', 'program', 'software', 'funkce', 'možnost', 'způsob', 'metoda']
        for word in problematic_before:
            translated = translated.replace(f'{word}<strong>', f'{word} <strong>')
        
        # Pass 3: Target specific problematic after patterns
        problematic_after = ['V', 'T', 'A', 'I', 'O', 'U', 'E', 'N', 'S', 'K', 'P', 'R', 'L', 'M', 'D', 'B', 'C', 'F', 'G', 'H', 'J', 'Q', 'W', 'X', 'Y', 'Z']
        for letter in problematic_after:
            translated = translated.replace(f'</strong>{letter}', f'</strong> {letter}')
            
        # Pass 4: Catch-all regex with different approach - MOST AGGRESSIVE
        translated = re.sub(r'([^\s])(<strong>)', r'\1 \2', translated)
        translated = re.sub(r'(</strong>)([^\s])', r'\1 \2', translated)
        
        # Pass 5: NUCLEAR OPTION - direct character-by-character fix for common patterns
        # This handles cases where Google Translate might have messed up the spacing after our processing
        nuclear_patterns = [
            ('na<strong>', 'na <strong>'),
            ('pro<strong>', 'pro <strong>'),
            ('do<strong>', 'do <strong>'),
            ('za<strong>', 'za <strong>'),
            ('od<strong>', 'od <strong>'),
            ('po<strong>', 'po <strong>'),
            ('v<strong>', 'v <strong>'),
            ('s<strong>', 's <strong>'),
            ('k<strong>', 'k <strong>'),
            ('o<strong>', 'o <strong>'),
            ('na<strong>', 'na <strong>'),
            ('nástroje<strong>', 'nástroje <strong>'),
            ('při<strong>', 'při <strong>'),
            ('před<strong>', 'před <strong>'),
            ('nad<strong>', 'nad <strong>'),
            ('pod<strong>', 'pod <strong>'),
            ('mezi<strong>', 'mezi <strong>'),
            ('bez<strong>', 'bez <strong>'),
            ('podle<strong>', 'podle <strong>'),
            ('během<strong>', 'během <strong>'),
            ('kolem<strong>', 'kolem <strong>'),
            ('nástroj<strong>', 'nástroj <strong>'),
            ('program<strong>', 'program <strong>'),
            ('software<strong>', 'software <strong>'),
            ('funkce<strong>', 'funkce <strong>'),
            ('možnost<strong>', 'možnost <strong>'),
            ('způsob<strong>', 'způsob <strong>'),
            ('metoda<strong>', 'metoda <strong>'),
            ('</strong>V', '</strong> V'),
            ('</strong>T', '</strong> T'),
            ('</strong>A', '</strong> A'),
            ('</strong>I', '</strong> I'),
            ('</strong>O', '</strong> O'),
            ('</strong>U', '</strong> U'),
            ('</strong>E', '</strong> E'),
            ('</strong>N', '</strong> N'),
            ('</strong>S', '</strong> S'),
            ('</strong>K', '</strong> K'),
            ('</strong>P', '</strong> P'),
            ('</strong>R', '</strong> R'),
            ('</strong>L', '</strong> L'),
            ('</strong>M', '</strong> M'),
            ('</strong>D', '</strong> D'),
            ('</strong>B', '</strong> B'),
            ('</strong>C', '</strong> C'),
            ('</strong>F', '</strong> F'),
            ('</strong>G', '</strong> G'),
            ('</strong>H', '</strong> H'),
            ('</strong>J', '</strong> J'),
            ('</strong>Q', '</strong> Q'),
            ('</strong>W', '</strong> W'),
            ('</strong>X', '</strong> X'),
            ('</strong>Y', '</strong> Y'),
            ('</strong>Z', '</strong> Z'),
        ]
        
        for original, fixed in nuclear_patterns:
            translated = translated.replace(original, fixed)
        
        # Pass 6: Clean up multiple spaces
        translated = re.sub(r'\s{2,}', ' ', translated)
        
        # Pass 7: FINAL SAFETY NET - One more ultra-aggressive spacing fix
        translated = re.sub(r'([a-zA-Z0-9áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ.,;:!?])(<strong)', r'\1 \2', translated)
        translated = re.sub(r'(</strong>)([a-zA-Z0-9áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ.,;:!?])', r'\1 \2', translated)
        
        return translated
    
    def fix_capitalization(self, text):
        """Fix capitalization issues in translated text"""
        if not text:
            return text
            
        # Split text into sentences and fix capitalization
        # Sentence endings: . ! ? followed by space or end of string
        sentences = re.split(r'([.!?]+\s*)', text)
        
        fixed_sentences = []
        for i, sentence in enumerate(sentences):
            if sentence.strip():  # Skip empty parts
                # If it's actual sentence content (not punctuation)
                if not re.match(r'^[.!?\s]+$', sentence):
                    # Capitalize first letter of sentence
                    sentence = self.capitalize_first_letter(sentence)
                    
                    # Also capitalize after specific punctuation within the sentence
                    # Like after '. ' or '! ' or '? ' in the middle
                    sentence = re.sub(r'([.!?]\s+)([a-záčďéěíňóřšťúůýž])', 
                                     lambda m: m.group(1) + m.group(2).upper(), sentence)
                    
                    # Capitalize 'i' when it stands alone (Czech 'I' = 'já')
                    sentence = re.sub(r'\bi\b', 'I', sentence)
                    
            fixed_sentences.append(sentence)
        
        result = ''.join(fixed_sentences)
        
        # Additional fixes for specific cases
        # Capitalize after HTML tags that end sentences
        result = re.sub(r'(</[^>]+>\s*)([a-záčďéěíňóřšťúůýž])', 
                       lambda m: m.group(1) + m.group(2).upper(), result)
        
        # Capitalize after line breaks if they start a new sentence
        result = re.sub(r'(\n\s*)([a-záčďéěíňóřšťúůýž])', 
                       lambda m: m.group(1) + m.group(2).upper(), result)
        
        return result
    
    def fix_html_spacing(self, text):
        """Comprehensive fix for spacing issues around HTML tags"""
        if not text:
            return text
            
        result = text
        
        # PHASE 1: Fix missing spaces before ALL formatting tags with universal pattern
        # This catches ANY alphanumeric character directly followed by opening tags
        html_tags = ['strong', 'em', 'b', 'i', 'u', 'span']
        for tag in html_tags:
            # Pattern: word character/punctuation directly followed by opening tag
            result = re.sub(f'([\\w.,;:!?])(<{tag}[^>]*>)', r'\1 \2', result, flags=re.UNICODE)
        
        # PHASE 2: Fix missing spaces after ALL closing formatting tags
        for tag in html_tags:
            # Pattern: closing tag directly followed by word character
            result = re.sub(f'(</{tag}>)([\\w])', r'\1 \2', result, flags=re.UNICODE)
        
        # PHASE 3: Special focus on sentence-ending punctuation
        # Google Translate often creates "sentence.<strong>" patterns
        result = re.sub(r'([.!?:;,])(<(?:strong|em|b|i|u|span)[^>]*>)', r'\1 \2', result)
        
        # PHASE 4: Word boundary fixes for Czech prepositions
        # These are the most common cases where Google Translate fails
        czech_words = [
            'na', 'pro', 'do', 'za', 'od', 'po', 'při', 'před', 'nad', 'pod', 'mezi',
            'v', 's', 'k', 'o', 'u', 'z', 'i', 'a', 'ale', 'nebo', 'že', 'aby',
            'nástroj', 'program', 'funkce', 'možnost', 'způsob', 'metoda'
        ]
        
        for word in czech_words:
            # Fix word directly connected to any opening tag
            for tag in html_tags:
                result = re.sub(f'\\b{word}(<{tag}[^>]*>)', f'{word} \\1', result)
        
        # PHASE 5: Handle camelCase breaking but preserve brand names
        result = re.sub(r'([a-záčďéěíňóřšťúůýž]{2,})([A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ])(?!Up|Sync|Render|Max|CAD|Live)', 
                       r'\1 \2', result)
        
        # PHASE 6: Clean up multiple spaces that may have been introduced
        result = re.sub(r' {2,}', ' ', result)
        
        # PHASE 7: Restore brand names that might have been split
        brand_fixes = {
            'Sketch Up': 'SketchUp',
            'sketch up': 'SketchUp', 
            'Live Sync': 'LiveSync',
            'live sync': 'LiveSync',
            'D5 Render': 'D5 Render',  # This one should stay split
            '3ds Max': '3ds Max',  # This one should stay split
            'Archi CAD': 'ArchiCAD',
            'archi cad': 'ArchiCAD'
        }
        
        for wrong, correct in brand_fixes.items():
            result = result.replace(wrong, correct)
        
        return result
    
    def post_translation_spacing_fix(self, text):
        """Ultra-aggressive fix for spacing issues that Google Translate introduces"""
        if not text:
            return text
            
        result = text
        
        # PHASE 1: Universal spacing fixes for ANY character followed by HTML tags
        # This is the most comprehensive approach - any letter/number directly touching a tag gets a space
        # Use \w for word characters which includes Czech characters properly
        result = re.sub(r'([\w])(<(?:strong|em|b|i|u|span)[^>]*>)', r'\1 \2', result, flags=re.UNICODE)
        
        # PHASE 2: Fix missing spaces after closing tags before ANY character
        result = re.sub(r'(</(?:strong|em|b|i|u|span)>)([\w])', r'\1 \2', result, flags=re.UNICODE)
        
        # PHASE 3: Fix punctuation directly followed by HTML tags
        result = re.sub(r'([.,;:!?])(<(?:strong|em|b|i|u|span)[^>]*>)', r'\1 \2', result)
        
        # PHASE 4: Fix specific word boundaries that Google Translate often breaks
        # Focus on Czech prepositions and common words
        czech_prepositions = [
            'na', 'pro', 'do', 'za', 'od', 'po', 'při', 'před', 'nad', 'pod', 'mezi', 
            'bez', 'podle', 'během', 'kolem', 'okolo', 'vedle', 'mimo', 'skrz', 'přes',
            'v', 's', 'k', 'o', 'u', 'z', 'i', 'a', 'ale', 'nebo', 'že', 'aby',
            'obsahuje', 'nabízí', 'umožní', 'můžete', 'budete', 'budou', 'mají', 'jsou',
            'této', 'tohoto', 'této', 'tomto', 'tyto', 'také', 'více', 'všechny',
            'práce', 'nástroj', 'program', 'software', 'funkce', 'možnost'
        ]
        
        for word in czech_prepositions:
            # Fix word directly connected to <strong> tag
            result = re.sub(f'{word}<strong>', f'{word} <strong>', result)
            # Fix word directly connected to <em> tag  
            result = re.sub(f'{word}<em>', f'{word} <em>', result)
        
        # PHASE 5: Fix sentence-ending punctuation issues
        # Google Translate often produces "sentence.<strong>" instead of "sentence. <strong>"
        result = re.sub(r'([.!?])(<(?:strong|em|b|i|u|span)[^>]*>)', r'\1 \2', result)
        
        # PHASE 6: Fix missing spaces after closing tags followed by capital letters (sentence starts)
        # This catches "</strong>V reálném" -> "</strong> V reálném"
        result = re.sub(r'(</(?:strong|em|b|i|u|span)>)([A-Z\u00C0-\u017F])', r'\1 \2', result, flags=re.UNICODE)
        
        # PHASE 7: FINAL BRUTE FORCE - catch any remaining direct connections
        # This is an ultra-aggressive final pass to catch anything we missed
        result = re.sub(r'([a-zA-Z0-9\u00C0-\u017F])(<strong[^>]*>)', r'\1 \2', result)
        result = re.sub(r'(</strong>)([a-zA-Z\u00C0-\u017F])', r'\1 \2', result)
        result = re.sub(r'([a-zA-Z0-9\u00C0-\u017F])(<em[^>]*>)', r'\1 \2', result)
        result = re.sub(r'(</em>)([a-zA-Z\u00C0-\u017F])', r'\1 \2', result)
        
        # PHASE 8: Clean up multiple spaces that may have been introduced
        result = re.sub(r' {2,}', ' ', result)
        
        return result
    
    def force_strong_tag_spacing(self, text):
        """ULTIMATE: Direct and aggressive spacing enforcement for strong tags"""
        if not text:
            return text
            
        result = text
        
        # NUCLEAR OPTION: Multiple comprehensive passes to catch everything
        
        # Pass 1: Universal regex - any non-space before <strong>
        result = re.sub(r'([^\s])(<strong)', r'\1 \2', result)
        
        # Pass 2: Universal regex - any non-space after </strong>
        result = re.sub(r'(</strong>)([^\s])', r'\1 \2', result)
        
        # Pass 3: Specific problematic patterns we've observed
        problematic_patterns = [
            # Czech prepositions and words that stick to <strong>
            ('na<strong>', 'na <strong>'),
            ('pro<strong>', 'pro <strong>'),
            ('do<strong>', 'do <strong>'),
            ('za<strong>', 'za <strong>'),
            ('od<strong>', 'od <strong>'),
            ('po<strong>', 'po <strong>'),
            ('při<strong>', 'při <strong>'),
            ('před<strong>', 'před <strong>'),
            ('nad<strong>', 'nad <strong>'),
            ('pod<strong>', 'pod <strong>'),
            ('mezi<strong>', 'mezi <strong>'),
            ('bez<strong>', 'bez <strong>'),
            ('podle<strong>', 'podle <strong>'),
            ('během<strong>', 'během <strong>'),
            ('kolem<strong>', 'kolem <strong>'),
            ('nástroj<strong>', 'nástroj <strong>'),
            ('program<strong>', 'program <strong>'),
            ('software<strong>', 'software <strong>'),
            ('funkce<strong>', 'funkce <strong>'),
            ('možnost<strong>', 'možnost <strong>'),
            ('způsob<strong>', 'způsob <strong>'),
            ('metoda<strong>', 'metoda <strong>'),
            # Any single letter patterns
            ('a<strong>', 'a <strong>'),
            ('e<strong>', 'e <strong>'),
            ('i<strong>', 'i <strong>'),
            ('o<strong>', 'o <strong>'),
            ('u<strong>', 'u <strong>'),
            ('y<strong>', 'y <strong>'),
            ('v<strong>', 'v <strong>'),
            ('s<strong>', 's <strong>'),
            ('k<strong>', 'k <strong>'),
            ('z<strong>', 'z <strong>'),
            # Czech diacritics
            ('ě<strong>', 'ě <strong>'),
            ('á<strong>', 'á <strong>'),
            ('é<strong>', 'é <strong>'),
            ('í<strong>', 'í <strong>'),
            ('ó<strong>', 'ó <strong>'),
            ('ú<strong>', 'ú <strong>'),
            ('ů<strong>', 'ů <strong>'),
            ('ý<strong>', 'ý <strong>'),
            ('č<strong>', 'č <strong>'),
            ('ď<strong>', 'ď <strong>'),
            ('ň<strong>', 'ň <strong>'),
            ('ř<strong>', 'ř <strong>'),
            ('š<strong>', 'š <strong>'),
            ('ť<strong>', 'ť <strong>'),
            ('ž<strong>', 'ž <strong>'),
            # Numbers and punctuation
            ('0<strong>', '0 <strong>'),
            ('1<strong>', '1 <strong>'),
            ('2<strong>', '2 <strong>'),
            ('3<strong>', '3 <strong>'),
            ('4<strong>', '4 <strong>'),
            ('5<strong>', '5 <strong>'),
            ('6<strong>', '6 <strong>'),
            ('7<strong>', '7 <strong>'),
            ('8<strong>', '8 <strong>'),
            ('9<strong>', '9 <strong>'),
            ('.<strong>', '. <strong>'),
            (',<strong>', ', <strong>'),
            (';<strong>', '; <strong>'),
            (':<strong>', ': <strong>'),
            ('!<strong>', '! <strong>'),
            ('?<strong>', '? <strong>'),
        ]
        
        for original, fixed in problematic_patterns:
            result = result.replace(original, fixed)
            
        # Pass 4: Closing tag patterns - exhaustive list
        closing_patterns = [
            ('</strong>V', '</strong> V'),
            ('</strong>T', '</strong> T'),
            ('</strong>A', '</strong> A'),
            ('</strong>I', '</strong> I'),
            ('</strong>O', '</strong> O'),
            ('</strong>U', '</strong> U'),
            ('</strong>E', '</strong> E'),
            ('</strong>N', '</strong> N'),
            ('</strong>S', '</strong> S'),
            ('</strong>K', '</strong> K'),
            ('</strong>P', '</strong> P'),
            ('</strong>R', '</strong> R'),
            ('</strong>L', '</strong> L'),
            ('</strong>M', '</strong> M'),
            ('</strong>D', '</strong> D'),
            ('</strong>B', '</strong> B'),
            ('</strong>C', '</strong> C'),
            ('</strong>F', '</strong> F'),
            ('</strong>G', '</strong> G'),
            ('</strong>H', '</strong> H'),
            ('</strong>J', '</strong> J'),
            ('</strong>Q', '</strong> Q'),
            ('</strong>W', '</strong> W'),
            ('</strong>X', '</strong> X'),
            ('</strong>Y', '</strong> Y'),
            ('</strong>Z', '</strong> Z'),
            # Czech diacritics after closing
            ('</strong>Á', '</strong> Á'),
            ('</strong>É', '</strong> É'),
            ('</strong>Í', '</strong> Í'),
            ('</strong>Ó', '</strong> Ó'),
            ('</strong>Ú', '</strong> Ú'),
            ('</strong>Ů', '</strong> Ů'),
            ('</strong>Ý', '</strong> Ý'),
            ('</strong>Č', '</strong> Č'),
            ('</strong>Ď', '</strong> Ď'),
            ('</strong>Ě', '</strong> Ě'),
            ('</strong>Ň', '</strong> Ň'),
            ('</strong>Ř', '</strong> Ř'),
            ('</strong>Š', '</strong> Š'),
            ('</strong>Ť', '</strong> Ť'),
            ('</strong>Ž', '</strong> Ž'),
            # Numbers and punctuation after closing
            ('</strong>0', '</strong> 0'),
            ('</strong>1', '</strong> 1'),
            ('</strong>2', '</strong> 2'),
            ('</strong>3', '</strong> 3'),
            ('</strong>4', '</strong> 4'),
            ('</strong>5', '</strong> 5'),
            ('</strong>6', '</strong> 6'),
            ('</strong>7', '</strong> 7'),
            ('</strong>8', '</strong> 8'),
            ('</strong>9', '</strong> 9'),
        ]
        
        for original, fixed in closing_patterns:
            result = result.replace(original, fixed)
        
        # Pass 5: Final safety net - catch any remaining patterns
        # This is an ultra-aggressive regex that catches ANYTHING touching <strong>
        result = re.sub(r'([a-zA-Z0-9áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ.,;:!?])(<strong)', r'\1 \2', result)
        result = re.sub(r'(</strong>)([a-zA-Z0-9áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ.,;:!?])', r'\1 \2', result)
        
        # Pass 6: Clean up multiple spaces
        result = re.sub(r' {2,}', ' ', result)
        
        return result
    
    def capitalize_first_letter(self, text):
        """Capitalize the first letter of text, handling special characters"""
        if not text:
            return text
            
        # Find the first letter (skip whitespace and special characters)
        for i, char in enumerate(text):
            if char.isalpha():
                return text[:i] + char.upper() + text[i+1:]
        
        return text

class ArticleTranslator:
    """Main class for automated article translation"""
    
    def __init__(self):
        self.translator = SlovakCzechTranslator()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_article(self, url):
        """Fetch article content from URL"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch article from {url}: {str(e)}")
    
    def extract_article_data(self, html_content, url):
        """Extract article content, metadata, and images from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract metadata
        metadata = {
            'title': '',
            'description': '',
            'keywords': '',
            'author': '',
            'published_date': '',
            'cover_image': ''
        }
        
        # Title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text().strip()
        
        # Meta tags
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            if tag.get('name') == 'description':
                metadata['description'] = tag.get('content', '').strip()
            elif tag.get('name') == 'keywords':
                metadata['keywords'] = tag.get('content', '').strip()
            elif tag.get('name') == 'author':
                metadata['author'] = tag.get('content', '').strip()
            elif tag.get('property') == 'og:image':
                metadata['cover_image'] = urljoin(url, tag.get('content', ''))
        
        # Try to find article content (common selectors)
        article_selectors = [
            'article',
            '.article-content',
            '.post-content',
            '.entry-content',
            '#content',
            '.content',
            'main'
        ]
        
        article_content = None
        for selector in article_selectors:
            element = soup.select_one(selector)
            if element:
                article_content = element
                break
        
        if not article_content:
            # Fallback: use body content
            article_content = soup.find('body')
        
        return {
            'metadata': metadata,
            'content': article_content,
            'soup': soup
        }
    
    def detect_software_topic(self, title, content_text):
        """Detect the main software/topic from title and content"""
        title_lower = title.lower()
        content_lower = content_text.lower()
        
        # Software detection patterns
        software_patterns = {
            'sketchup': ['sketchup', 'sketch up'],
            'd5-render': ['d5 render', 'd5render', 'd5 rendering'],
            'archicad': ['archicad', 'archi cad'],
            'revit': ['revit', 'autodesk revit'],
            'rhino': ['rhino', 'rhinoceros', 'rhino3d'],
            '3dsmax': ['3ds max', '3dsmax', 'autodesk 3ds'],
            'blender': ['blender'],
            'lumion': ['lumion'],
            'twinmotion': ['twinmotion', 'twin motion'],
            'vray': ['v-ray', 'vray', 'v ray'],
            'corona': ['corona render', 'corona'],
            'cinema4d': ['cinema 4d', 'cinema4d', 'c4d']
        }
        
        detected_software = []
        for software, patterns in software_patterns.items():
            for pattern in patterns:
                if pattern in title_lower or pattern in content_lower:
                    detected_software.append(software)
                    break
        
        return detected_software
    
    def get_czech_topic_name(self, software_list):
        """Get Czech topic name based on detected software"""
        czech_topics = {
            'sketchup': 'SketchUp - 3D modelování',
            'd5-render': 'D5 Render - Vizuální renderování',
            'archicad': 'ArchiCAD - Architektonický návrh',
            'revit': 'Revit - BIM a architektura',
            'rhino': 'Rhino - 3D modelování a design',
            '3dsmax': '3ds Max - 3D animace a rendering',
            'blender': 'Blender - 3D tvůrba a animace',
            'lumion': 'Lumion - Architektonická vizualizace',
            'twinmotion': 'Twinmotion - Reálný čas vizualizace',
            'vray': 'V-Ray - Fotorealistický rendering',
            'corona': 'Corona Renderer - Realistický rendering',
            'cinema4d': 'Cinema 4D - 3D animace a design'
        }
        
        if software_list:
            # Return the first detected software's Czech topic name
            primary_software = software_list[0]
            return czech_topics.get(primary_software, 'Softwarové nástroje - Návody a tipy')
        
        return 'Softwarové nástroje - Návody a tipy'
    
    def get_czech_cta_links(self, software_list, original_href):
        """Generate appropriate Czech CTA links based on detected software"""
        
        # Czech website base URLs (adjust these to your actual Czech site structure)
        czech_links = {
            'sketchup': {
                'product': '/sketchup/',
                'courses': '/kurzy/sketchup-kurz/',
                'tutorials': '/navody/sketchup/',
                'licenses': '/sketchup-licence/'
            },
            'd5-render': {
                'product': '/d5-render/',
                'courses': '/kurzy/d5-render-kurz/',
                'tutorials': '/navody/d5-render/',
                'licenses': '/d5-render-licence/'
            },
            'archicad': {
                'product': '/archicad/',
                'courses': '/kurzy/archicad-kurz/',
                'tutorials': '/navody/archicad/',
                'licenses': '/archicad-licence/'
            },
            'revit': {
                'product': '/revit/',
                'courses': '/kurzy/revit-kurz/',
                'tutorials': '/navody/revit/',
                'licenses': '/revit-licence/'
            },
            'rhino': {
                'product': '/rhino/',
                'courses': '/kurzy/rhino-kurz/',
                'tutorials': '/navody/rhino/',
                'licenses': '/rhino-licence/'
            },
            # Add more software as needed
            'general': {
                'product': '/software/',
                'courses': '/kurzy/',
                'tutorials': '/navody/',
                'contact': '/kontakt/',
                'consultation': '/konzultace/'
            }
        }
        
        # Determine link type based on original href content
        original_lower = original_href.lower()
        
        if not software_list:
            software_list = ['general']
        
        primary_software = software_list[0]  # Use the first detected software
        
        # Map Slovak patterns to Czech equivalents
        if any(word in original_lower for word in ['licenc', 'license', 'predaj', 'shop']):
            return czech_links.get(primary_software, czech_links['general']).get('licenses', '/software/')
        elif any(word in original_lower for word in ['kurz', 'skoleni', 'training', 'learn']):
            return czech_links.get(primary_software, czech_links['general']).get('courses', '/kurzy/')
        elif any(word in original_lower for word in ['navod', 'tutorial', 'guide', 'help']):
            return czech_links.get(primary_software, czech_links['general']).get('tutorials', '/navody/')
        elif any(word in original_lower for word in ['kontakt', 'contact', 'konzultac']):
            return czech_links.get(primary_software, czech_links['general']).get('consultation', '/konzultace/')
        else:
            # Default to product page
            return czech_links.get(primary_software, czech_links['general']).get('product', '/software/')
    
    def replace_cta_links(self, soup, title, content_text):
        """Replace Slovak CTA links with appropriate Czech ones"""
        detected_software = self.detect_software_topic(title, content_text)
        
        # Find all links in CTA buttons (styled links)
        cta_links = soup.find_all('a', style=True)
        
        for link in cta_links:
            if link.has_attr('href'):
                original_href = link['href']
                # Only replace internal Slovak links (starting with /)
                if original_href.startswith('/'):
                    new_href = self.get_czech_cta_links(detected_software, original_href)
                    link['href'] = new_href
                    safe_print(f"CTA link updated: {original_href} -> {new_href} (detected: {detected_software})")
    
    def translate_html_content(self, soup, title="", content_text=""):
        """Translate all text content in the HTML while preserving structure"""
        from bs4 import NavigableString
        
        # First replace CTA links with appropriate Czech ones
        self.replace_cta_links(soup, title, content_text)
        
        # Find all text nodes and translate them
        for text_node in soup.find_all(string=True):
            if text_node.strip():  # Skip empty strings
                translated_text = self.translator.translate_text(text_node.strip())
                if translated_text != text_node.strip():  # Only replace if translation changed
                    text_node.replace_with(translated_text)
        
        # Translate attributes that might contain text
        for element in soup.find_all():
            for attr in ['title', 'alt', 'placeholder']:
                if element.has_attr(attr) and element[attr]:
                    element[attr] = self.translator.translate_text(element[attr])
        
        # CRITICAL: Apply final spacing fixes to the entire HTML after translation
        # This catches any spacing issues that Google Translate might have introduced
        soup_str = str(soup)
        soup_str = self.translator.force_strong_tag_spacing(soup_str)
        
        # Parse the fixed HTML back into BeautifulSoup
        from bs4 import BeautifulSoup
        fixed_soup = BeautifulSoup(soup_str, 'html.parser')
        
        # Replace the original soup content with the fixed content
        soup.clear()
        for child in fixed_soup.children:
            if hasattr(child, 'name'):
                soup.append(child)
    
    def process_images(self, soup, base_url, output_dir):
        """Download and process images"""
        images_dir = Path(output_dir) / 'images'
        images_dir.mkdir(exist_ok=True)
        
        img_tags = soup.find_all('img')
        downloaded_images = []
        
        for img in img_tags:
            src = img.get('src')
            if not src:
                continue
            
            # Convert relative URLs to absolute
            img_url = urljoin(base_url, src)
            
            try:
                # Download image
                response = self.session.get(img_url)
                response.raise_for_status()
                
                # Generate filename
                parsed_url = urlparse(img_url)
                filename = os.path.basename(parsed_url.path)
                if not filename or '.' not in filename:
                    filename = f"image_{len(downloaded_images) + 1}.jpg"
                
                # Save image
                img_path = images_dir / filename
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                
                downloaded_images.append({
                    'original_url': img_url,
                    'local_path': str(img_path),
                    'filename': filename
                })
                
                safe_print(f"Downloaded image: {filename}")
                
            except Exception as e:
                safe_print(f"Failed to download image {img_url}: {str(e)}")
        
        return downloaded_images
    
    def clean_html_content(self, translated_content):
        """Remove title and header image from HTML content, keep content images"""
        from bs4 import BeautifulSoup
        
        # Convert to soup if it's not already
        if isinstance(translated_content, str):
            soup = BeautifulSoup(translated_content, 'html.parser')
        else:
            soup = translated_content
        
        # Remove header section with title
        header = soup.find('header')
        if header:
            header.decompose()
        
        # Remove ONLY the main header image (first img with specific attributes)
        # Look for the header image specifically by attributes
        header_img = soup.find('img', attrs={
            'itemprop': 'image',
            'fetchpriority': 'high'
        })
        if header_img:
            header_img.decompose()
            safe_print("Removed header image")
        
        # Remove duplicate h1 titles
        h1_tags = soup.find_all('h1')
        for h1 in h1_tags:
            h1.decompose()
        
        # Remove extra paragraph with title
        paragraphs = soup.find_all('p')
        if paragraphs and len(paragraphs) > 0:
            first_p = paragraphs[0]
            # Check if first paragraph is just the title
            if first_p.get_text().strip().lower().startswith('ktorou verzi') or first_p.get_text().strip().lower().startswith('kterou verzi'):
                first_p.decompose()
        
        # IMPORTANT: Remove all HTML comments (including CTA block comments)
        # Use regex on string representation to remove comments
        soup_str = str(soup)
        # Remove HTML comments like <!-- CTA blok: kontaktujte nás -->
        soup_str = re.sub(r'<!--.*?-->', '', soup_str, flags=re.DOTALL)
        
        # Remove CTA block labels that appear as plain text (keep the button blocks)
        soup_str = re.sub(r'Blok CTA:[^<]*', '', soup_str, flags=re.IGNORECASE)
        
        soup = BeautifulSoup(soup_str, 'html.parser')
        
        # Keep all other images in the content
        remaining_images = soup.find_all('img')
        safe_print(f"Content images preserved: {len(remaining_images)}")
        
        return soup
    
    def download_header_image(self, cover_image_url, output_dir):
        """Download the header/cover image separately"""
        if not cover_image_url:
            return None
            
        try:
            response = self.session.get(cover_image_url)
            response.raise_for_status()
            
            # Generate filename
            parsed_url = urlparse(cover_image_url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                filename = "header_image.jpg"
            
            # Save image
            header_img_path = Path(output_dir) / filename
            with open(header_img_path, 'wb') as f:
                f.write(response.content)
            
            return {
                'filename': filename,
                'local_path': str(header_img_path),
                'original_url': cover_image_url
            }
        except Exception as e:
            safe_print(f"Failed to download header image {cover_image_url}: {str(e)}")
            return None
    
    def generate_output(self, article_data, translated_content, images, output_dir, czech_topic=None):
        """Generate translated article files in separate folder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Translate metadata
        translated_metadata = {}
        for key, value in article_data['metadata'].items():
            if isinstance(value, str) and value.strip():
                translated_metadata[key] = self.translator.translate_text(value)
            else:
                translated_metadata[key] = value
        
        # Create article-specific folder
        article_folder = Path(output_dir) / f"article_{timestamp}"
        article_folder.mkdir(exist_ok=True)
        
        # Clean HTML content (remove title and header image)
        clean_content = self.clean_html_content(translated_content)
        
        # 1. Clean HTML content file
        html_file = article_folder / "content.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            # Extract the main content but preserve everything except header/title
            content_div = clean_content.find('div', class_='text')
            if content_div:
                # Write the content div with all its children (including any images)
                content_html = str(content_div)
            else:
                # If no text div found, write the whole cleaned content
                # Remove the article wrapper but keep everything else
                if clean_content.name == 'article':
                    # Write all children of the article tag
                    content_html = ''
                    for child in clean_content.children:
                        if hasattr(child, 'name') and child.name:  # Skip text nodes
                            content_html += str(child)
                else:
                    content_html = str(clean_content)
            
            # FINAL SPACING FIX: Ensure perfect spacing around <strong> and <em> tags
            content_html = re.sub(r'([^\s])(<strong[^>]*>)', r'\1 \2', content_html)
            content_html = re.sub(r'(</strong>)([^\s])', r'\1 \2', content_html)
            content_html = re.sub(r'([^\s])(<em[^>]*>)', r'\1 \2', content_html)
            content_html = re.sub(r'(</em>)([^\s])', r'\1 \2', content_html)
            
            # Remove CTA block labels (but keep the button blocks)
            content_html = re.sub(r'Blok CTA:[^<\n]*', '', content_html, flags=re.IGNORECASE)
            
            content_html = re.sub(r' {2,}', ' ', content_html)  # Clean up double spaces
            
            f.write(content_html)
        
        # 2. SEO metadata text file
        seo_file = article_folder / "seo_metadata.txt"
        with open(seo_file, 'w', encoding='utf-8') as f:
            f.write(f"TITLE: {translated_metadata.get('title', '')}\n")
            f.write(f"DESCRIPTION: {translated_metadata.get('description', '')}\n")
            f.write(f"KEYWORDS: {translated_metadata.get('keywords', '')}\n")
            f.write(f"AUTHOR: {translated_metadata.get('author', '')}\n")
            if czech_topic:
                f.write(f"TOPIC: {czech_topic}\n")
            f.write(f"\n--- ORIGINAL METADATA ---\n")
            f.write(f"SOURCE: {article_data['metadata'].get('title', '')}\n")
            f.write(f"TRANSLATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 3. Download header image
        header_image = None
        if translated_metadata.get('cover_image'):
            header_image = self.download_header_image(translated_metadata['cover_image'], article_folder)
        
        # 4. Create images subfolder for content images
        if images:
            images_folder = article_folder / "images"
            images_folder.mkdir(exist_ok=True)
            # Move downloaded images to article folder
            for img in images:
                try:
                    old_path = Path(img['local_path'])
                    if old_path.exists():
                        new_path = images_folder / img['filename']
                        old_path.rename(new_path)
                        img['local_path'] = str(new_path)
                except Exception as e:
                    safe_print(f"Error moving image {img['filename']}: {e}")
        
        # 5. Create summary file
        summary_file = article_folder / "README.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"ARTICLE TRANSLATION SUMMARY\n")
            f.write(f"=========================\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Language: Slovak -> Czech\n\n")
            f.write(f"FILES:\n")
            f.write(f"- content.html: Main article content (without title/header)\n")
            f.write(f"- seo_metadata.txt: Title, description, keywords for SEO\n")
            if header_image:
                f.write(f"- {header_image['filename']}: Header/cover image\n")
            if images:
                f.write(f"- images/: {len(images)} content images\n")
            f.write(f"\nUSAGE:\n")
            f.write(f"1. Use seo_metadata.txt for title and description\n")
            f.write(f"2. Upload header image as article cover\n")
            f.write(f"3. Copy content.html into article editor\n")
            f.write(f"4. Upload images from images/ folder\n")
        
        return {
            'article_folder': article_folder,
            'html_file': html_file,
            'seo_file': seo_file,
            'header_image': header_image,
            'content_images': images,
            'translated_metadata': translated_metadata
        }
    
    def translate_article(self, url, output_dir=None):
        """Main method to translate an article from URL"""
        if output_dir is None:
            output_dir = Path.cwd() / 'translated_articles'
        
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        print(f"Fetching article from: {url}")
        html_content = self.fetch_article(url)
        
        print("Extracting article data...")
        article_data = self.extract_article_data(html_content, url)
        
        print("Translating content...")
        # Create a copy of the BeautifulSoup element
        from copy import deepcopy
        translated_content = deepcopy(article_data['content'])
        
        # Get title and content text for smart link replacement
        title = article_data['metadata'].get('title', '')
        content_text = translated_content.get_text() if translated_content else ''
        
        # Detect software topic for Czech categorization
        detected_software = self.detect_software_topic(title, content_text)
        czech_topic = self.get_czech_topic_name(detected_software)
        
        self.translate_html_content(translated_content, title, content_text)
        
        print("Processing images...")
        images = self.process_images(article_data['soup'], url, output_dir)
        
        print("Generating output files...")
        result = self.generate_output(article_data, translated_content, images, output_dir, czech_topic)
        
        safe_print(f"\n[OK] Translation completed!")
        safe_print(f"[FOLDER] Article folder: {result['article_folder']}")
        safe_print(f"[FILE] Content file: {result['html_file']}")
        safe_print(f"[SEO] SEO file: {result['seo_file']}")
        if result.get('header_image'):
            safe_print(f"[IMG] Header image: {result['header_image']['filename']}")
        safe_print(f"[IMG] Content images: {len(result.get('content_images', []))}")
        safe_print(f"[TITLE] Translated title: {result['translated_metadata']['title']}")
        
        return result

def main():
    # Check if GUI mode (no arguments) or CLI mode
    import sys
    
    if len(sys.argv) == 1:
        # No arguments provided - launch GUI
        launch_gui()
    else:
        # Command line arguments provided - use CLI mode
        parser = argparse.ArgumentParser(description='Translate Slovak articles to Czech for Shoptet')
        parser.add_argument('url', help='URL of the Slovak article to translate')
        parser.add_argument('-o', '--output', help='Output directory', default='translated_articles')
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
        
        args = parser.parse_args()
        
        try:
            translator = ArticleTranslator()
            result = translator.translate_article(args.url, args.output)
            
            if args.verbose:
                print("\n[SUMMARY] Translation Summary:")
                print(f"Source URL: {args.url}")
                print(f"Output directory: {args.output}")
                print(f"Files generated: 3")
                print(f"Images downloaded: {result['images_count']}")
                
        except Exception as e:
            print(f"[X] Error: {str(e)}")
            exit(1)

def launch_gui():
    """Launch the GUI version of the translator"""
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    import threading
    import webbrowser
    from pathlib import Path
    
    class TranslatorGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("Slovak to Czech Article Translator")
            self.root.geometry("600x500")
            self.root.configure(bg='#f0f0f0')
            
            # Style
            style = ttk.Style()
            style.theme_use('clam')
            
            # Main frame
            main_frame = ttk.Frame(root, padding="20")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Title
            title_label = ttk.Label(main_frame, text="Slovak to Czech Article Translator", 
                                  font=('Arial', 16, 'bold'))
            title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
            
            # URL input
            ttk.Label(main_frame, text="Article URL:", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
            self.url_var = tk.StringVar()
            self.url_entry = ttk.Entry(main_frame, textvariable=self.url_var, font=('Arial', 10))
            self.url_entry.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
            
            # Output directory
            ttk.Label(main_frame, text="Output Directory:", font=('Arial', 10)).grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
            self.output_var = tk.StringVar(value=str(Path.cwd()))
            output_frame = ttk.Frame(main_frame)
            output_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
            self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var, font=('Arial', 10))
            self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
            ttk.Button(output_frame, text="Browse", command=self.browse_output).grid(row=0, column=1, padx=(5, 0))
            output_frame.columnconfigure(0, weight=1)
            
            # Translate button
            self.translate_btn = ttk.Button(main_frame, text="Translate Article", 
                                          command=self.start_translation, 
                                          style='Accent.TButton')
            self.translate_btn.grid(row=5, column=0, columnspan=2, pady=20)
            
            # Progress bar
            self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
            self.progress.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
            
            # Status text
            self.status_var = tk.StringVar(value="Ready to translate")
            self.status_label = ttk.Label(main_frame, textvariable=self.status_var, font=('Arial', 9))
            self.status_label.grid(row=7, column=0, columnspan=2)
            
            # Log area
            ttk.Label(main_frame, text="Translation Log:", font=('Arial', 10)).grid(row=8, column=0, sticky=tk.W, pady=(20, 5))
            self.log_text = tk.Text(main_frame, height=10, font=('Consolas', 9), bg='#f8f8f8')
            self.log_text.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
            
            # Result buttons frame
            self.result_frame = ttk.Frame(main_frame)
            self.result_frame.grid(row=10, column=0, columnspan=2, pady=(10, 0))
            
            # Configure grid weights
            main_frame.columnconfigure(0, weight=1)
            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)
            main_frame.rowconfigure(9, weight=1)
            
            self.translator = None
            self.result = None
            
        def browse_output(self):
            directory = filedialog.askdirectory(initialdir=self.output_var.get())
            if directory:
                self.output_var.set(directory)
                
        def log_message(self, message):
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
            self.root.update_idletasks()
            
        def start_translation(self):
            url = self.url_var.get().strip()
            if not url:
                messagebox.showerror("Error", "Please enter a URL")
                return
                
            if not url.startswith(('http://', 'https://')):
                messagebox.showerror("Error", "Please enter a valid URL (starting with http:// or https://)")
                return
                
            # Clear previous results
            self.log_text.delete(1.0, tk.END)
            for widget in self.result_frame.winfo_children():
                widget.destroy()
                
            # Start translation in thread
            self.translate_btn.configure(state='disabled', text='Translating...')
            self.progress.start(10)
            self.status_var.set("Translation in progress...")
            
            thread = threading.Thread(target=self.translate_article, args=(url,))
            thread.daemon = True
            thread.start()
            
        def translate_article(self, url):
            try:
                self.translator = ArticleTranslator()
                output_dir = self.output_var.get()
                
                # Override print function to log to GUI
                import builtins
                original_print = builtins.print
                def gui_print(*args, **kwargs):
                    message = ' '.join(str(arg) for arg in args)
                    self.root.after(0, lambda: self.log_message(message))
                    original_print(*args, **kwargs)
                builtins.print = gui_print
                
                # Perform translation
                self.result = self.translator.translate_article(url, output_dir)
                
                # Restore original print
                builtins.print = original_print
                
                # Update GUI on success
                self.root.after(0, self.translation_completed)
                
            except Exception as e:
                # Restore original print
                import builtins
                builtins.print = original_print if 'original_print' in locals() else print
                
                error_msg = str(e)
                self.root.after(0, lambda: self.translation_failed(error_msg))
                
        def translation_completed(self):
            self.progress.stop()
            self.translate_btn.configure(state='normal', text='Translate Article')
            self.status_var.set("Translation completed successfully!")
            
            # Add result buttons
            if self.result and 'article_folder' in self.result:
                folder_path = self.result['article_folder']
                
                ttk.Button(self.result_frame, text="Open Output Folder", 
                         command=lambda: webbrowser.open(f"file:///{folder_path}")).pack(side=tk.LEFT, padx=5)
                
                if 'html_file' in self.result:
                    html_file = self.result['html_file']
                    ttk.Button(self.result_frame, text="Open Article HTML", 
                             command=lambda: webbrowser.open(f"file:///{html_file}")).pack(side=tk.LEFT, padx=5)
                             
                messagebox.showinfo("Success", f"Translation completed!\nOutput folder: {folder_path}")
                
        def translation_failed(self, error_msg):
            self.progress.stop()
            self.translate_btn.configure(state='normal', text='Translate Article')
            self.status_var.set("Translation failed")
            self.log_message(f"ERROR: {error_msg}")
            messagebox.showerror("Translation Failed", f"Translation failed:\n{error_msg}")
            
    # Create and run GUI
    root = tk.Tk()
    app = TranslatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
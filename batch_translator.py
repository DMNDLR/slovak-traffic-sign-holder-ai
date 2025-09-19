#!/usr/bin/env python3
"""
Batch Slovak to Czech Article Translator
Process multiple articles from URLs list or CSV file
"""

import csv
import json
import argparse
from pathlib import Path
from datetime import datetime
import sys
import os

# Import our main translator
from article_translator import ArticleTranslator

class BatchTranslator:
    """Handles batch processing of multiple articles"""
    
    def __init__(self, output_base_dir=None):
        self.translator = ArticleTranslator()
        self.output_base_dir = Path(output_base_dir) if output_base_dir else Path.cwd() / 'batch_translations'
        self.results = []
        self.errors = []
    
    def process_urls_list(self, urls_list):
        """Process a list of URLs"""
        total = len(urls_list)
        print(f"🔄 Starting batch translation of {total} articles...")
        
        for i, url in enumerate(urls_list, 1):
            print(f"\n📖 Processing {i}/{total}: {url}")
            
            try:
                # Create individual output directory for each article
                article_dir = self.output_base_dir / f"article_{i:03d}"
                result = self.translator.translate_article(url, article_dir)
                
                self.results.append({
                    'url': url,
                    'status': 'success',
                    'result': result,
                    'processed_at': datetime.now().isoformat()
                })
                
                print(f"✅ Success: {result['translated_metadata']['title']}")
                
            except Exception as e:
                error_info = {
                    'url': url,
                    'status': 'error',
                    'error': str(e),
                    'processed_at': datetime.now().isoformat()
                }
                self.errors.append(error_info)
                print(f"❌ Error: {str(e)}")
    
    def process_csv_file(self, csv_file):
        """Process URLs from CSV file with additional metadata"""
        urls = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                # Try to detect if it has headers
                sample = f.read(1024)
                f.seek(0)
                
                sniffer = csv.Sniffer()
                has_header = sniffer.has_header(sample)
                
                reader = csv.reader(f)
                
                if has_header:
                    headers = next(reader)
                    print(f"📋 CSV Headers: {headers}")
                
                for row in reader:
                    if row and row[0].strip():  # Skip empty rows
                        urls.append(row[0].strip())
        
        except Exception as e:
            print(f"❌ Error reading CSV file: {str(e)}")
            return
        
        print(f"📄 Found {len(urls)} URLs in CSV file")
        self.process_urls_list(urls)
    
    def generate_batch_report(self):
        """Generate batch processing report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_base_dir / f"batch_report_{timestamp}.json"
        
        report = {
            'batch_info': {
                'processed_at': datetime.now().isoformat(),
                'total_articles': len(self.results) + len(self.errors),
                'successful': len(self.results),
                'failed': len(self.errors),
                'success_rate': len(self.results) / (len(self.results) + len(self.errors)) * 100 if (len(self.results) + len(self.errors)) > 0 else 0
            },
            'successful_translations': self.results,
            'errors': self.errors
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📊 Batch Report Generated: {report_file}")
        return report_file

def main():
    parser = argparse.ArgumentParser(description='Batch translate Slovak articles to Czech')
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-u', '--urls', nargs='+', help='List of URLs to translate')
    input_group.add_argument('-f', '--file', help='Text file with URLs (one per line)')
    input_group.add_argument('-c', '--csv', help='CSV file with URLs in first column')
    
    # Output options
    parser.add_argument('-o', '--output', help='Output base directory', default='batch_translations')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--report-only', action='store_true', help='Generate report only (skip translation)')
    
    args = parser.parse_args()
    
    try:
        batch_translator = BatchTranslator(args.output)
        
        # Ensure output directory exists
        batch_translator.output_base_dir.mkdir(exist_ok=True)
        
        if not args.report_only:
            if args.urls:
                # Process URLs from command line
                batch_translator.process_urls_list(args.urls)
            
            elif args.file:
                # Process URLs from text file
                try:
                    with open(args.file, 'r', encoding='utf-8') as f:
                        urls = [line.strip() for line in f if line.strip()]
                    batch_translator.process_urls_list(urls)
                except Exception as e:
                    print(f"❌ Error reading file {args.file}: {str(e)}")
                    exit(1)
            
            elif args.csv:
                # Process URLs from CSV file
                batch_translator.process_csv_file(args.csv)
        
        # Generate report
        report_file = batch_translator.generate_batch_report()
        
        # Summary
        print(f"\n🎯 Batch Translation Complete!")
        print(f"📁 Output directory: {batch_translator.output_base_dir}")
        print(f"✅ Successful: {len(batch_translator.results)}")
        print(f"❌ Failed: {len(batch_translator.errors)}")
        print(f"📊 Report: {report_file}")
        
        if args.verbose and batch_translator.errors:
            print(f"\n🚨 Errors encountered:")
            for error in batch_translator.errors:
                print(f"  • {error['url']}: {error['error']}")
        
    except Exception as e:
        print(f"❌ Batch processing failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
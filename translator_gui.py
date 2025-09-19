#!/usr/bin/env python3
"""
Slovak-to-Czech Article Translator - GUI Application
====================================================

A user-friendly graphical interface for translating Slovak articles to Czech
with automatic HTML processing, image handling, and CTA link replacement.

Features:
- Single article translation
- Batch processing from URLs or CSV files
- Real-time translation progress
- Output folder management
- Translation history
- Metadata preview

Author: AI Assistant
Created: 2025-09-18
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import subprocess
import threading
import json
from datetime import datetime
import webbrowser
import sys
from pathlib import Path

class TranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Slovak → Czech Article Translator")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Variables
        self.output_folder = tk.StringVar(value="translated_articles")
        self.current_url = tk.StringVar()
        self.translation_running = tk.BooleanVar(value=False)
        self.history_file = "translation_history.json"
        
        # Load translation history
        self.history = self.load_history()
        
        # Create GUI
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Slovak → Czech Article Translator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(1, weight=1)
        
        # Single Article Tab
        self.create_single_tab(notebook)
        
        # Batch Processing Tab
        self.create_batch_tab(notebook)
        
        # History Tab
        self.create_history_tab(notebook)
        
        # Settings Tab
        self.create_settings_tab(notebook)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_single_tab(self, notebook):
        """Create single article translation tab"""
        single_frame = ttk.Frame(notebook, padding="20")
        notebook.add(single_frame, text="Single Article")
        
        # URL input section
        url_frame = ttk.LabelFrame(single_frame, text="Article URL", padding="10")
        url_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        single_frame.columnconfigure(0, weight=1)
        
        ttk.Label(url_frame, text="Slovak Article URL:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        url_entry = ttk.Entry(url_frame, textvariable=self.current_url, font=('Arial', 10))
        url_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        url_frame.columnconfigure(0, weight=1)
        
        paste_btn = ttk.Button(url_frame, text="📋 Paste", 
                              command=self.paste_from_clipboard, width=8)
        paste_btn.grid(row=1, column=1, padx=(5, 0))
        
        # Example URLs
        example_frame = ttk.Frame(url_frame)
        example_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(example_frame, text="Examples:", font=('Arial', 9, 'italic')).pack(anchor=tk.W)
        
        examples = [
            "https://www.softwareshop.sk/blog/ktoru-verziu-sketchup-si-vybrat--kompletny-sprievodca-2025/",
            "https://www.softwareshop.sk/blog/7-praktickych-dovodov--preco-architekti-miluju-sketchup/"
        ]
        
        for i, example in enumerate(examples):
            link_label = ttk.Label(example_frame, text=f"• {example[:70]}...", 
                                  foreground="blue", cursor="hand2", font=('Arial', 8))
            link_label.pack(anchor=tk.W, padx=(10, 0))
            link_label.bind("<Button-1>", lambda e, url=example: self.current_url.set(url))
        
        # Output settings
        output_frame = ttk.LabelFrame(single_frame, text="Output Settings", padding="10")
        output_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(output_frame, text="Output Folder:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        output_entry_frame = ttk.Frame(output_frame)
        output_entry_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        output_frame.columnconfigure(0, weight=1)
        
        output_entry = ttk.Entry(output_entry_frame, textvariable=self.output_folder, 
                                font=('Arial', 10))
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(output_entry_frame, text="📁 Browse", 
                               command=self.browse_output_folder, width=10)
        browse_btn.pack(side=tk.RIGHT)
        
        # Translation controls
        control_frame = ttk.Frame(single_frame)
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.translate_btn = ttk.Button(control_frame, text="🚀 Translate Article", 
                                       command=self.translate_single_article,
                                       style="Accent.TButton")
        self.translate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(control_frame, text="⏹ Stop", 
                                  command=self.stop_translation, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Progress bar
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate')
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Output log
        log_frame = ttk.LabelFrame(single_frame, text="Translation Log", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        single_frame.rowconfigure(3, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD, 
                                                 font=('Consolas', 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def create_batch_tab(self, notebook):
        """Create batch processing tab"""
        batch_frame = ttk.Frame(notebook, padding="20")
        notebook.add(batch_frame, text="Batch Processing")
        
        # Input options
        input_frame = ttk.LabelFrame(batch_frame, text="Batch Input", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        batch_frame.columnconfigure(0, weight=1)
        
        self.batch_mode = tk.StringVar(value="urls")
        
        urls_radio = ttk.Radiobutton(input_frame, text="Multiple URLs (one per line)", 
                                    variable=self.batch_mode, value="urls")
        urls_radio.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        csv_radio = ttk.Radiobutton(input_frame, text="CSV file with URLs", 
                                   variable=self.batch_mode, value="csv")
        csv_radio.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        # URL input area
        self.urls_text = scrolledtext.ScrolledText(input_frame, height=8, wrap=tk.WORD,
                                                  font=('Arial', 10))
        self.urls_text.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # File selection for CSV
        csv_frame = ttk.Frame(input_frame)
        csv_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        self.csv_file = tk.StringVar()
        csv_entry = ttk.Entry(csv_frame, textvariable=self.csv_file, state=tk.DISABLED)
        csv_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        csv_browse_btn = ttk.Button(csv_frame, text="📄 Select CSV", 
                                   command=self.browse_csv_file)
        csv_browse_btn.pack(side=tk.RIGHT)
        
        # Batch controls
        batch_control_frame = ttk.Frame(batch_frame)
        batch_control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.batch_translate_btn = ttk.Button(batch_control_frame, text="🚀 Start Batch Translation",
                                             command=self.translate_batch,
                                             style="Accent.TButton")
        self.batch_translate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Batch progress
        self.batch_progress = ttk.Progressbar(batch_control_frame, mode='determinate')
        self.batch_progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.batch_status = tk.StringVar(value="Ready for batch processing")
        status_label = ttk.Label(batch_control_frame, textvariable=self.batch_status)
        status_label.pack(side=tk.RIGHT)
        
        # Batch log
        batch_log_frame = ttk.LabelFrame(batch_frame, text="Batch Processing Log", padding="10")
        batch_log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        batch_frame.rowconfigure(2, weight=1)
        
        self.batch_log_text = scrolledtext.ScrolledText(batch_log_frame, height=15, wrap=tk.WORD,
                                                       font=('Consolas', 9))
        self.batch_log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        batch_log_frame.columnconfigure(0, weight=1)
        batch_log_frame.rowconfigure(0, weight=1)
    
    def create_history_tab(self, notebook):
        """Create translation history tab"""
        history_frame = ttk.Frame(notebook, padding="20")
        notebook.add(history_frame, text="History")
        
        # History controls
        history_controls = ttk.Frame(history_frame)
        history_controls.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        history_frame.columnconfigure(0, weight=1)
        
        ttk.Button(history_controls, text="🔄 Refresh", 
                  command=self.refresh_history).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(history_controls, text="📁 Open Folder", 
                  command=self.open_output_folder).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(history_controls, text="🗑️ Clear History", 
                  command=self.clear_history).pack(side=tk.RIGHT)
        
        # History table
        columns = ('Date', 'Title', 'URL', 'Status', 'Output')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=20)
        
        # Define column headings and widths
        self.history_tree.heading('Date', text='Date')
        self.history_tree.heading('Title', text='Translated Title')
        self.history_tree.heading('URL', text='Source URL')
        self.history_tree.heading('Status', text='Status')
        self.history_tree.heading('Output', text='Output Folder')
        
        self.history_tree.column('Date', width=120)
        self.history_tree.column('Title', width=250)
        self.history_tree.column('URL', width=300)
        self.history_tree.column('Status', width=80)
        self.history_tree.column('Output', width=150)
        
        # Scrollbars for history table
        history_scroll_y = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        history_scroll_x = ttk.Scrollbar(history_frame, orient=tk.HORIZONTAL, command=self.history_tree.xview)
        
        self.history_tree.configure(yscrollcommand=history_scroll_y.set, xscrollcommand=history_scroll_x.set)
        
        self.history_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        history_scroll_y.grid(row=1, column=1, sticky=(tk.N, tk.S))
        history_scroll_x.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        history_frame.rowconfigure(1, weight=1)
        
        # Double-click to open folder
        self.history_tree.bind('<Double-1>', self.open_selected_folder)
        
        # Populate history
        self.refresh_history()
    
    def create_settings_tab(self, notebook):
        """Create settings and help tab"""
        settings_frame = ttk.Frame(notebook, padding="20")
        notebook.add(settings_frame, text="Settings & Help")
        
        # Settings section
        settings_section = ttk.LabelFrame(settings_frame, text="Settings", padding="10")
        settings_section.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        settings_frame.columnconfigure(0, weight=1)
        
        # Default output folder setting
        ttk.Label(settings_section, text="Default Output Folder:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        default_output_frame = ttk.Frame(settings_section)
        default_output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_section.columnconfigure(0, weight=1)
        
        self.default_output = tk.StringVar(value=self.output_folder.get())
        default_entry = ttk.Entry(default_output_frame, textvariable=self.default_output)
        default_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(default_output_frame, text="📁 Browse",
                  command=self.browse_default_output).pack(side=tk.RIGHT)
        
        ttk.Button(settings_section, text="💾 Save Settings",
                  command=self.save_settings).grid(row=2, column=0, pady=(10, 0))
        
        # Help section
        help_section = ttk.LabelFrame(settings_frame, text="Help & Information", padding="10")
        help_section.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        settings_frame.rowconfigure(1, weight=1)
        
        help_text = scrolledtext.ScrolledText(help_section, height=20, wrap=tk.WORD, font=('Arial', 10))
        help_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        help_section.columnconfigure(0, weight=1)
        help_section.rowconfigure(0, weight=1)
        
        help_content = """
Slovak → Czech Article Translator - Help

FEATURES:
✅ Automatic Slovak-to-Czech translation with extensive dictionary
✅ Smart CTA link replacement based on detected software/topics
✅ HTML structure preservation 
✅ Image processing (header + content images)
✅ SEO metadata extraction and translation
✅ Clean output ready for Shoptet CMS import
✅ Batch processing for multiple articles

HOW TO USE:

Single Article:
1. Paste or enter a Slovak article URL
2. Choose output folder (optional)
3. Click "Translate Article"
4. Wait for completion and check the output folder

Batch Processing:
1. Choose input method (URLs or CSV file)
2. For URLs: Enter one URL per line in the text area
3. For CSV: Select a CSV file with URLs in the first column
4. Click "Start Batch Translation"
5. Monitor progress in the log

OUTPUT STRUCTURE:
Each translated article creates a folder containing:
• content.html - Clean article content (no header image)
• seo_metadata.txt - SEO title, description, etc.
• [header_image] - Main article image for manual upload
• images/ - All content images referenced in the article
• README.txt - Import instructions

SUPPORTED WEBSITES:
• www.softwareshop.sk blog articles
• Articles about SketchUp, D5 Render, ArchiCAD, Rhino, Revit, etc.

SMART FEATURES:
• Detects software mentioned in articles
• Updates Slovak internal links to Czech equivalents
• Preserves all HTML formatting and structure
• Handles complex tables, lists, and media

TROUBLESHOOTING:
• Make sure URLs are accessible and contain article content
• Check that Python dependencies are installed (requests, beautifulsoup4, lxml, Pillow)
• Output folder must be writable
• Internet connection required for image downloads

For technical support or feature requests, check the translation logs for detailed error information.
        """
        
        help_text.insert(tk.END, help_content.strip())
        help_text.configure(state=tk.DISABLED)
        
        # Action buttons
        action_frame = ttk.Frame(settings_frame)
        action_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(action_frame, text="📁 Open Output Folder",
                  command=self.open_output_folder).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(action_frame, text="📊 View Translation Dictionary",
                  command=self.view_dictionary).pack(side=tk.LEFT, padx=(0, 10))
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def paste_from_clipboard(self):
        """Paste URL from clipboard"""
        try:
            clipboard_text = self.root.clipboard_get()
            if clipboard_text and ('http' in clipboard_text):
                self.current_url.set(clipboard_text.strip())
                self.status_var.set("URL pasted from clipboard")
        except tk.TclError:
            messagebox.showwarning("Clipboard", "No text found in clipboard")
    
    def browse_output_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title="Select Output Folder", 
                                        initialdir=self.output_folder.get())
        if folder:
            self.output_folder.set(folder)
    
    def browse_default_output(self):
        """Browse for default output folder"""
        folder = filedialog.askdirectory(title="Select Default Output Folder")
        if folder:
            self.default_output.set(folder)
    
    def browse_csv_file(self):
        """Browse for CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.csv_file.set(file_path)
    
    def translate_single_article(self):
        """Start single article translation"""
        if not self.current_url.get().strip():
            messagebox.showerror("Error", "Please enter an article URL")
            return
        
        if not self.current_url.get().startswith('http'):
            messagebox.showerror("Error", "Please enter a valid HTTP/HTTPS URL")
            return
        
        # Prepare output folder
        output_dir = self.output_folder.get().strip() or "translated_articles"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Start translation in separate thread
        self.translation_running.set(True)
        self.translate_btn.configure(state=tk.DISABLED)
        self.stop_btn.configure(state=tk.NORMAL)
        self.progress.start(10)
        
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"Starting translation...\nURL: {self.current_url.get()}\nOutput: {output_dir}\n\n")
        
        threading.Thread(target=self._run_translation, 
                        args=(self.current_url.get(), output_dir), 
                        daemon=True).start()
    
    def _run_translation(self, url, output_dir):
        """Run translation in background thread"""
        try:
            # Run the translation script
            cmd = [sys.executable, "article_translator.py", url, "-o", output_dir]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, bufsize=1, universal_newlines=True)
            
            # Read output line by line
            while True:
                if not self.translation_running.get():
                    process.terminate()
                    break
                
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                
                if output:
                    self.root.after(0, lambda o=output: self._update_log(o.strip()))
            
            return_code = process.poll()
            
            if return_code == 0 and self.translation_running.get():
                self.root.after(0, lambda: self._translation_complete(url, output_dir, True))
            else:
                self.root.after(0, lambda: self._translation_complete(url, output_dir, False))
                
        except Exception as e:
            self.root.after(0, lambda: self._translation_error(str(e)))
    
    def _update_log(self, message):
        """Update log text widget"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.status_var.set(message[:100] + "..." if len(message) > 100 else message)
    
    def _translation_complete(self, url, output_dir, success):
        """Handle translation completion"""
        self.progress.stop()
        self.translate_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        self.translation_running.set(False)
        
        if success:
            self.log_text.insert(tk.END, "\n✅ Translation completed successfully!\n")
            self.status_var.set("Translation completed successfully")
            
            # Add to history
            title = "Translation completed"  # We could parse this from the output
            self.add_to_history(url, title, "Success", output_dir)
            
            # Ask if user wants to open output folder
            if messagebox.askyesno("Complete", "Translation completed! Open output folder?"):
                self.open_output_folder()
        else:
            self.log_text.insert(tk.END, "\n❌ Translation failed. Check the log for details.\n")
            self.status_var.set("Translation failed")
            self.add_to_history(url, "Failed", "Error", output_dir)
        
        self.log_text.see(tk.END)
    
    def _translation_error(self, error):
        """Handle translation error"""
        self.progress.stop()
        self.translate_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        self.translation_running.set(False)
        
        self.log_text.insert(tk.END, f"\n❌ Error: {error}\n")
        self.status_var.set(f"Error: {error}")
        messagebox.showerror("Translation Error", f"An error occurred:\n{error}")
    
    def stop_translation(self):
        """Stop current translation"""
        self.translation_running.set(False)
        self.progress.stop()
        self.translate_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        self.log_text.insert(tk.END, "\n⏹ Translation stopped by user\n")
        self.status_var.set("Translation stopped")
    
    def translate_batch(self):
        """Start batch translation"""
        # Get URLs based on mode
        urls = []
        
        if self.batch_mode.get() == "urls":
            text_content = self.urls_text.get(1.0, tk.END).strip()
            if not text_content:
                messagebox.showerror("Error", "Please enter URLs in the text area")
                return
            urls = [url.strip() for url in text_content.split('\n') if url.strip() and url.strip().startswith('http')]
        else:
            if not self.csv_file.get():
                messagebox.showerror("Error", "Please select a CSV file")
                return
            # TODO: Parse CSV file
            messagebox.showinfo("Info", "CSV batch processing will be implemented in the next version")
            return
        
        if not urls:
            messagebox.showerror("Error", "No valid URLs found")
            return
        
        # Start batch processing
        self.batch_translate_btn.configure(state=tk.DISABLED)
        self.batch_progress.configure(maximum=len(urls))
        self.batch_progress['value'] = 0
        
        self.batch_log_text.delete(1.0, tk.END)
        self.batch_log_text.insert(tk.END, f"Starting batch translation of {len(urls)} articles...\n\n")
        
        # TODO: Implement actual batch processing
        messagebox.showinfo("Info", f"Batch processing of {len(urls)} URLs will be implemented in the next version")
        self.batch_translate_btn.configure(state=tk.NORMAL)
    
    def load_history(self):
        """Load translation history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_history(self):
        """Save translation history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Could not save history: {e}")
    
    def add_to_history(self, url, title, status, output_folder):
        """Add translation to history"""
        entry = {
            'date': datetime.now().isoformat(),
            'url': url,
            'title': title,
            'status': status,
            'output_folder': output_folder
        }
        
        self.history.insert(0, entry)  # Add to beginning
        self.history = self.history[:100]  # Keep only last 100
        self.save_history()
        self.refresh_history()
    
    def refresh_history(self):
        """Refresh history display"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add history items
        for entry in self.history:
            date = entry.get('date', '')
            if date:
                try:
                    date = datetime.fromisoformat(date).strftime('%Y-%m-%d %H:%M')
                except:
                    pass
            
            self.history_tree.insert('', tk.END, values=(
                date,
                entry.get('title', '')[:50] + ('...' if len(entry.get('title', '')) > 50 else ''),
                entry.get('url', '')[:60] + ('...' if len(entry.get('url', '')) > 60 else ''),
                entry.get('status', ''),
                entry.get('output_folder', '')
            ))
    
    def clear_history(self):
        """Clear translation history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all translation history?"):
            self.history = []
            self.save_history()
            self.refresh_history()
            self.status_var.set("History cleared")
    
    def open_output_folder(self):
        """Open output folder in file explorer"""
        output_dir = self.output_folder.get() or "translated_articles"
        if os.path.exists(output_dir):
            os.startfile(output_dir)
        else:
            messagebox.showwarning("Folder Not Found", f"Output folder does not exist: {output_dir}")
    
    def open_selected_folder(self, event):
        """Open selected history item folder"""
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            output_folder = item['values'][4]  # Output folder column
            if os.path.exists(output_folder):
                os.startfile(output_folder)
            else:
                messagebox.showwarning("Folder Not Found", f"Output folder no longer exists: {output_folder}")
    
    def view_dictionary(self):
        """Show translation dictionary info"""
        messagebox.showinfo("Translation Dictionary", 
                           "The Slovak-Czech translation dictionary is built into the article_translator.py script.\n\n"
                           "It includes:\n"
                           "• Technical terms for 3D software\n"
                           "• UI elements and buttons\n"
                           "• Common phrases and expressions\n"
                           "• Smart CTA link replacements\n\n"
                           "The dictionary is automatically updated and can be extended by modifying the translator script.")
    
    def save_settings(self):
        """Save application settings"""
        self.output_folder.set(self.default_output.get())
        messagebox.showinfo("Settings", "Settings saved successfully!")

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = TranslatorGUI(root)
    
    # Handle window closing
    def on_closing():
        if app.translation_running.get():
            if messagebox.askokcancel("Quit", "Translation is running. Stop and quit?"):
                app.translation_running.set(False)
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        messagebox.showerror("Application Error", f"An unexpected error occurred:\n{str(e)}")

if __name__ == "__main__":
    main()
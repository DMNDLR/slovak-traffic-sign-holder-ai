#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple launcher for Slovak to Czech Article Translator
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime
import webbrowser

# Import the translator directly
try:
    from article_translator import ArticleTranslator
    DIRECT_IMPORT = True
except ImportError:
    DIRECT_IMPORT = False

# Import Slovak manual
try:
    from slovak_manual import SLOVAK_MANUAL
except ImportError:
    SLOVAK_MANUAL = "Návod nie je k dispozícii. Kontaktujte technickú podporu."

class SimpleTranslatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Slovak → Czech Article Translator")
        self.root.geometry("800x500")
        self.root.minsize(700, 400)
        
        # Variables
        self.url_var = tk.StringVar()
        self.output_var = tk.StringVar(value="translated_articles")
        self.is_translating = False
        
        self.create_widgets()
        self.center_window()
        
    def create_widgets(self):
        """Create GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Slovak → Czech Article Translator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # URL input
        ttk.Label(main_frame, text="Slovak Article URL:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        url_frame = ttk.Frame(main_frame)
        url_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        url_frame.columnconfigure(0, weight=1)
        
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, font=('Arial', 10))
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        paste_btn = ttk.Button(url_frame, text="📋 Paste", command=self.paste_url, width=8)
        paste_btn.grid(row=0, column=1)
        
        # Example link
        example_frame = ttk.Frame(main_frame)
        example_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        ttk.Label(example_frame, text="Example:", font=('Arial', 9, 'italic')).pack(side=tk.LEFT)
        example_link = ttk.Label(example_frame, 
                                text="https://www.softwareshop.sk/blog/ako-prepojit-sketchup-s-d5-render...",
                                foreground="blue", cursor="hand2", font=('Arial', 9))
        example_link.pack(side=tk.LEFT, padx=(5, 0))
        example_link.bind("<Button-1>", lambda e: self.url_var.set(
            "https://www.softwareshop.sk/blog/ako-prepojit-sketchup-s-d5-render-za-3-minuty/"))
        
        # Output directory
        ttk.Label(main_frame, text="Output Directory:", font=('Arial', 10, 'bold')).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var, font=('Arial', 10))
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(output_frame, text="📁 Browse", command=self.browse_output, width=10)
        browse_btn.grid(row=0, column=1)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(0, 20))
        
        self.translate_btn = ttk.Button(button_frame, text="🚀 Translate Article", 
                                       command=self.start_translation,
                                       style='Accent.TButton')
        self.translate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.open_folder_btn = ttk.Button(button_frame, text="📁 Open Output Folder", 
                                         command=self.open_output_folder)
        self.open_folder_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.help_btn = ttk.Button(button_frame, text="❓ Návod (Slovak)", 
                                  command=self.show_help)
        self.help_btn.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status
        self.status_var = tk.StringVar(value="Ready to translate")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Log area
        ttk.Label(main_frame, text="Translation Log:", font=('Arial', 10, 'bold')).grid(
            row=9, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=10, font=('Consolas', 9))
        self.log_text.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def paste_url(self):
        """Paste URL from clipboard"""
        try:
            clipboard_content = self.root.clipboard_get()
            if clipboard_content.startswith(('http://', 'https://')):
                self.url_var.set(clipboard_content)
                self.log_message("URL pasted from clipboard")
            else:
                messagebox.showwarning("Invalid URL", "Clipboard doesn't contain a valid URL")
        except tk.TclError:
            messagebox.showwarning("Clipboard Empty", "Clipboard is empty")
            
    def browse_output(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory", 
                                          initialdir=self.output_var.get())
        if directory:
            self.output_var.set(directory)
            self.log_message(f"Output directory set to: {directory}")
            
    def open_output_folder(self):
        """Open the output folder"""
        output_dir = self.output_var.get()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        try:
            if sys.platform == "win32":
                os.startfile(output_dir)
            elif sys.platform == "darwin":
                subprocess.run(["open", output_dir])
            else:
                subprocess.run(["xdg-open", output_dir])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {e}")
    
    def show_help(self):
        """Show Slovak manual in a new window"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Návod na použitie prekladača (Slovak Manual)")
        help_window.geometry("900x700")
        help_window.minsize(800, 600)
        
        # Make window modal
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Center the help window
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (900 // 2)
        y = (help_window.winfo_screenheight() // 2) - (700 // 2)
        help_window.geometry(f'900x700+{x}+{y}')
        
        # Create main frame
        main_frame = ttk.Frame(help_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="NÁVOD NA POUŽITIE PREKLADAČA ČLÁNKOV", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Manual text in scrollable area
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        manual_text = scrolledtext.ScrolledText(text_frame, 
                                              font=('Segoe UI', 10), 
                                              wrap=tk.WORD,
                                              state=tk.NORMAL)
        manual_text.pack(fill=tk.BOTH, expand=True)
        
        # Insert the Slovak manual text
        manual_text.insert(tk.END, SLOVAK_MANUAL)
        manual_text.configure(state=tk.DISABLED)  # Make it read-only
        
        # Close button
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        close_btn = ttk.Button(button_frame, text="Zavrieť (Close)", 
                              command=help_window.destroy)
        close_btn.pack(side=tk.RIGHT)
        
        # Focus on the help window
        help_window.focus_set()
            
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_translation(self):
        """Start translation process"""
        if self.is_translating:
            return
            
        url = self.url_var.get().strip()
        output_dir = self.output_var.get().strip()
        
        if not url:
            messagebox.showerror("Missing URL", "Please enter a Slovak article URL")
            return
            
        if not url.startswith(('http://', 'https://')):
            messagebox.showerror("Invalid URL", "URL must start with http:// or https://")
            return
            
        if not output_dir:
            messagebox.showerror("Missing Output", "Please select an output directory")
            return
            
        # Start translation in separate thread
        self.is_translating = True
        self.translate_btn.configure(state=tk.DISABLED)
        self.progress.start()
        self.status_var.set("Translating...")
        
        thread = threading.Thread(target=self.run_translation, args=(url, output_dir), daemon=True)
        thread.start()
        
    def run_translation(self, url, output_dir):
        """Run translation process"""
        try:
            self.log_message(f"Starting translation for: {url}")
            
            if DIRECT_IMPORT:
                # Use direct import method (preferred)
                self.run_translation_direct(url, output_dir)
            else:
                # Fallback to subprocess method
                self.run_translation_subprocess(url, output_dir)
                
        except Exception as e:
            self.root.after(0, lambda: self.translation_failed(str(e)))
            
    def run_translation_direct(self, url, output_dir):
        """Run translation using direct import"""
        try:
            # Create translator instance
            translator = ArticleTranslator()
            
            # Hook into safe_print to capture logs
            def gui_logger(text):
                try:
                    # Clean text of any problematic characters
                    clean_text = text.encode('ascii', errors='replace').decode('ascii')
                    self.root.after(0, lambda: self.log_message(clean_text))
                except:
                    self.root.after(0, lambda: self.log_message("[Log message with special characters]"))
            
            # Replace the safe_print function temporarily
            import article_translator
            original_safe_print = article_translator.safe_print
            article_translator.safe_print = gui_logger
            
            try:
                # Run the translation
                result = translator.translate_article(url, output_dir)
                self.root.after(0, lambda: self.translation_completed(output_dir))
            finally:
                # Restore original function
                article_translator.safe_print = original_safe_print
                
        except Exception as e:
            self.root.after(0, lambda: self.translation_failed(str(e)))
            
    def run_translation_subprocess(self, url, output_dir):
        """Run translation using subprocess (fallback)"""
        try:
            # Get path to the translator script
            script_path = Path(__file__).parent / "article_translator.py"
            
            # Run the translator script
            cmd = [sys.executable, str(script_path), url, "-o", output_dir]
            
            # Use environment to force UTF-8 encoding
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, encoding='utf-8', errors='replace', env=env)
            
            # Read output line by line
            for line in process.stdout:
                try:
                    line = line.strip()
                    if line:
                        # Replace any problematic characters
                        line = line.encode('ascii', errors='replace').decode('ascii')
                        self.root.after(0, lambda msg=line: self.log_message(msg))
                except UnicodeDecodeError:
                    # Skip problematic lines
                    continue
            
            process.wait()
            
            if process.returncode == 0:
                self.root.after(0, lambda: self.translation_completed(output_dir))
            else:
                self.root.after(0, lambda: self.translation_failed("Translation process failed"))
                
        except Exception as e:
            self.root.after(0, lambda: self.translation_failed(str(e)))
            
    def translation_completed(self, output_dir):
        """Handle successful translation"""
        self.is_translating = False
        self.translate_btn.configure(state=tk.NORMAL)
        self.progress.stop()
        self.status_var.set("Translation completed successfully!")
        
        self.log_message("✅ Translation completed successfully!")
        
        # Show success message with option to open folder
        result = messagebox.askyesno("Translation Complete", 
                                   "Translation completed successfully!\n\n"
                                   "Would you like to open the output folder?")
        if result:
            self.open_output_folder()
            
    def translation_failed(self, error_msg):
        """Handle translation failure"""
        self.is_translating = False
        self.translate_btn.configure(state=tk.NORMAL)
        self.progress.stop()
        self.status_var.set("Translation failed")
        
        self.log_message(f"❌ Translation failed: {error_msg}")
        messagebox.showerror("Translation Failed", f"Translation failed:\n\n{error_msg}")
        
    def run(self):
        """Start the GUI"""
        self.log_message("Slovak → Czech Article Translator ready")
        self.log_message("Enter a Slovak article URL and click 'Translate Article'")
        self.root.mainloop()

if __name__ == "__main__":
    app = SimpleTranslatorGUI()
    app.run()
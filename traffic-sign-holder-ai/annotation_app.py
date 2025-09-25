"""
🎯 Slovak Traffic Sign Holder Annotation App

Interactive GUI application for manually labeling photos to create training data.
Click to draw bounding boxes, select attributes, and correct AI predictions.
"""

import sys
import os
import json
import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from slovak_signs_database import get_database

class AnnotationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🇸🇰 Slovak Traffic Sign Holder Annotation Tool")
        self.root.geometry("1600x1000")
        
        # Apply dark theme
        self.setup_dark_theme()
        
        # Initialize variables
        self.current_image = None
        self.current_image_path = None
        self.photo_tk = None
        self.canvas_image = None
        self.scale_factor = 1.0
        
        # Bounding boxes and annotations
        self.current_boxes = []  # List of bounding box data
        self.drawing = False
        self.start_x = 0
        self.start_y = 0
        self.current_box_id = None
        self.selected_box = None
        
        # Slovak signs database
        self.signs_db = get_database()
        
        # Annotation data for current image
        self.annotation_data = {
            "filename": "",
            "image_size": {"width": 0, "height": 0},
            "holders": [],
            "signs": [],
            "notes": "",
            "annotated_by": "human",
            "annotation_date": ""
        }
        
        self.create_ui()
        self.setup_keyboard_shortcuts()
        
        # Ensure UI is fully initialized before loading photos
        self.root.update_idletasks()
        
        # Delay photo loading to ensure canvas is ready
        self.root.after(100, self.load_workspace_photos)
        
    def setup_dark_theme(self):
        """Setup dark theme for better appearance."""
        # Configure root window
        self.root.configure(bg='#2b2b2b')
        
        # Configure ttk styles for dark theme
        style = ttk.Style()
        
        # Set theme to 'clam' as base
        style.theme_use('clam')
        
        # Configure dark colors
        self.colors = {
            'bg_dark': '#2b2b2b',      # Dark background
            'bg_medium': '#3c3c3c',    # Medium background  
            'bg_light': '#4d4d4d',     # Light background
            'fg_normal': '#ffffff',    # Normal text
            'fg_dim': '#cccccc',       # Dimmed text
            'accent': '#0078d4',       # Accent blue
            'success': '#00ff00',      # Success green
            'warning': '#ffaa00',      # Warning orange
            'error': '#ff4444'         # Error red
        }
        
        # Configure ttk styles
        style.configure('TFrame', background=self.colors['bg_dark'])
        style.configure('TLabelFrame', background=self.colors['bg_dark'], foreground=self.colors['fg_normal'])
        style.configure('TLabelFrame.Label', background=self.colors['bg_dark'], foreground=self.colors['fg_normal'])
        style.configure('TLabel', background=self.colors['bg_dark'], foreground=self.colors['fg_normal'])
        style.configure('TButton', background=self.colors['bg_medium'], foreground=self.colors['fg_normal'])
        style.map('TButton', background=[('active', self.colors['bg_light'])])
        
        # Improved Combobox styling for better readability
        style.configure('TCombobox', 
                       fieldbackground=self.colors['bg_light'], 
                       background=self.colors['bg_light'], 
                       foreground=self.colors['fg_normal'],
                       arrowcolor=self.colors['fg_normal'],
                       bordercolor=self.colors['accent'],
                       lightcolor=self.colors['bg_light'],
                       darkcolor=self.colors['bg_medium'])
        style.map('TCombobox',
                 fieldbackground=[('readonly', self.colors['bg_light'])],
                 selectbackground=[('readonly', self.colors['accent'])],
                 selectforeground=[('readonly', 'white')])
        
        style.configure('TEntry', fieldbackground=self.colors['bg_medium'], foreground=self.colors['fg_normal'])
        
        print("🌙 Dark theme applied")
        
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for faster navigation."""
        # Arrow keys for navigation
        self.root.bind("<Left>", lambda e: self.previous_photo())
        self.root.bind("<Right>", lambda e: self.next_photo())
        
        # Page up/down for faster navigation
        self.root.bind("<Prior>", lambda e: self.jump_by_offset(-10))  # Page Up = -10 photos
        self.root.bind("<Next>", lambda e: self.jump_by_offset(10))    # Page Down = +10 photos
        
        # Ctrl+S to save
        self.root.bind("<Control-s>", lambda e: self.save_annotations())
        
        # Space to switch drawing mode
        self.root.bind("<space>", lambda e: self.toggle_drawing_mode())
        
        # Delete key to delete selected box
        self.root.bind("<Delete>", lambda e: self.delete_selected_box())
        
        # Home/End keys
        self.root.bind("<Home>", lambda e: self.jump_to_first_photo())
        self.root.bind("<End>", lambda e: self.jump_to_last_photo())
        
        print("⌨️ Keyboard shortcuts enabled:")
        print("   ← → : Previous/Next photo")
        print("   Page Up/Down: Jump ±10 photos")
        print("   Space: Toggle Holder/Sign mode")
        print("   Ctrl+S: Save annotations")
        print("   Delete: Delete selected box")
        print("   Home/End: First/Last photo")
        
    def create_ui(self):
        """Create the main UI layout."""
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Image and tools
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right panel - Annotation controls
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_panel.configure(width=450)  # Increased width for better space
        
        self.create_image_panel(left_panel)
        self.create_control_panel(right_panel)
        
    def create_image_panel(self, parent):
        """Create image display and annotation canvas."""
        
        # Toolbar
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # Navigation section
        nav_frame = ttk.Frame(toolbar)
        nav_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(nav_frame, text="📁 Open Photo", command=self.open_photo).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(nav_frame, text="📂 Load All Photos", command=self.load_all_photos_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Separator(nav_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(nav_frame, text="⬅️ Previous", command=self.previous_photo).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="➡️ Next", command=self.next_photo).pack(side=tk.LEFT, padx=2)
        
        # Photo counter
        self.photo_counter_label = ttk.Label(nav_frame, text="No photos loaded", foreground="blue")
        self.photo_counter_label.pack(side=tk.LEFT, padx=10)
        
        # Action buttons
        ttk.Button(toolbar, text="💾 Save Annotations", command=self.save_annotations).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🗑️ Clear All", command=self.clear_all_boxes).pack(side=tk.LEFT, padx=5)
        
        # Quick jump entry
        jump_frame = ttk.Frame(toolbar)
        jump_frame.pack(side=tk.RIGHT)
        ttk.Label(jump_frame, text="Jump to:").pack(side=tk.LEFT, padx=2)
        self.jump_entry = ttk.Entry(jump_frame, width=6)
        self.jump_entry.pack(side=tk.LEFT, padx=2)
        self.jump_entry.bind("<Return>", self.jump_to_photo)
        ttk.Button(jump_frame, text="Go", command=self.jump_to_photo).pack(side=tk.LEFT, padx=2)
        
        # Image canvas with scrollbars
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='#1e1e1e', cursor='crosshair', highlightthickness=0,
                               width=1000, height=700)  # Set initial size
        
        # Scrollbars
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # Pack scrollbars and canvas
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind mouse events for drawing
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Button-3>", self.on_right_click)  # Right-click for context menu
        
    def create_control_panel(self, parent):
        """Create annotation controls panel."""
        
        # Compact info bar
        info_frame = ttk.Frame(parent)
        info_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.photo_info_label = ttk.Label(info_frame, text="No photo", font=('TkDefaultFont', 8))
        self.photo_info_label.pack(side=tk.LEFT, padx=5)
        
        self.save_status_label = ttk.Label(info_frame, text="❌", font=('TkDefaultFont', 10))
        self.save_status_label.pack(side=tk.RIGHT, padx=5)
        
        # Quick actions (most important buttons at top)
        actions_frame = ttk.Frame(parent)
        actions_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(actions_frame, text="🤖 Auto", width=8,
                  command=self.auto_detect_attributes).pack(side=tk.LEFT, padx=1)
        ttk.Button(actions_frame, text="🔄 Reset", width=8,
                  command=self.reset_attributes).pack(side=tk.LEFT, padx=1)
        ttk.Button(actions_frame, text="💾 Save", width=8,
                  command=self.save_annotations).pack(side=tk.LEFT, padx=1)
        
        # Drawing mode - compact
        mode_frame = ttk.LabelFrame(parent, text="🎯 Režim")
        mode_frame.pack(fill=tk.X, pady=(0, 5))
        
        mode_buttons_frame = ttk.Frame(mode_frame)
        mode_buttons_frame.pack(fill=tk.X, padx=5, pady=3)
        
        self.draw_mode = tk.StringVar(value="holder")
        ttk.Radiobutton(mode_buttons_frame, text="Nosič", variable=self.draw_mode, value="holder").pack(side=tk.LEFT)
        ttk.Radiobutton(mode_buttons_frame, text="Značka", variable=self.draw_mode, value="sign").pack(side=tk.LEFT, padx=10)
        
        # Multi-sign checkbox - compact
        self.multi_sign_var = tk.BooleanVar()
        self.multi_sign_check = ttk.Checkbutton(mode_buttons_frame, text="Viac značiek", 
                                              variable=self.multi_sign_var,
                                              command=self.on_multi_sign_toggle)
        self.multi_sign_check.pack(side=tk.RIGHT)
        
        # Current selection info - compact
        selection_frame = ttk.LabelFrame(parent, text="📝 Vybratý")
        selection_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.selection_info = ttk.Label(selection_frame, text="Nič", wraplength=350, font=('TkDefaultFont', 8))
        self.selection_info.pack(padx=5, pady=3)
        
        # Holder attributes (shown when holder is selected)
        self.holder_frame = ttk.LabelFrame(parent, text="🏗️ Nosič")
        self.holder_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Material
        ttk.Label(self.holder_frame, text="Materiál:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.holder_material = ttk.Combobox(self.holder_frame, width=20, state="readonly")
        self.holder_material.configure(values=["kov", "betón", "drevo", "plast", "budova/stena", "iné"])
        self.holder_material.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        
        # Owner
        ttk.Label(self.holder_frame, text="Vlastník:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.holder_owner = ttk.Combobox(self.holder_frame, width=20, state="readonly")
        self.holder_owner.configure(values=["mesto", "obec", "štát", "súkromník", "firma", "iný"])
        self.holder_owner.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        
        # Base Type
        ttk.Label(self.holder_frame, text="Typ Základu:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.holder_base_type = ttk.Combobox(self.holder_frame, width=20, state="readonly")
        base_types = ["jeden stĺp", "dva stĺpy", "tri stĺpy", "štyri stĺpy", 
                     "pouličný stĺp", "elektrický stĺp", "telekom stĺp", "semafor stĺp",
                     "portálová konštrukcia", "mostová konštrukcia", "zábradlie/zábranka", 
                     "autobusová zastávka", "plot", "budova", "brána/dvere", "bariéra", "iné"]
        self.holder_base_type.configure(values=base_types)
        self.holder_base_type.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        
        # Orientation
        ttk.Label(self.holder_frame, text="Orientácia:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.holder_orientation = ttk.Combobox(self.holder_frame, width=20, state="readonly")
        self.holder_orientation.configure(values=["v smere jazdy", "kolmo na smer jazdy", "proti smeru jazdy", "diagonálne", "iná"])
        self.holder_orientation.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
        
        # Configure grid weights for proper expansion
        self.holder_frame.grid_columnconfigure(1, weight=1)
        
        # Apply button for holder - compact
        ttk.Button(self.holder_frame, text="✅ Aplikovať", command=self.apply_holder_attributes).grid(row=4, column=0, columnspan=2, pady=5)
        
        # Sign attributes (shown when sign is selected)
        self.sign_frame = ttk.LabelFrame(parent, text="🚦 Značka")
        self.sign_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Slovak sign search - compact
        ttk.Label(self.sign_frame, text="Hľadať:").pack(anchor=tk.W, padx=5, pady=(3, 0))
        self.sign_search = ttk.Entry(self.sign_frame, width=30)
        self.sign_search.pack(fill=tk.X, padx=5, pady=1)
        self.sign_search.bind("<KeyRelease>", self.on_sign_search)
        
        # Sign results listbox - more compact
        self.sign_listbox = tk.Listbox(self.sign_frame, height=4, 
                                     bg=self.colors['bg_medium'], fg=self.colors['fg_normal'],
                                     selectbackground=self.colors['accent'], selectforeground='white')
        self.sign_listbox.pack(fill=tk.X, padx=5, pady=1)
        self.sign_listbox.bind("<<ListboxSelect>>", self.on_sign_select)
        
        # Selected sign info - compact
        self.selected_sign_info = ttk.Label(self.sign_frame, text="Nič", wraplength=350, font=('TkDefaultFont', 8))
        self.selected_sign_info.pack(padx=5, pady=1)
        
        # OCR text entry - compact
        ttk.Label(self.sign_frame, text="OCR:").pack(anchor=tk.W, padx=5, pady=(5, 0))
        self.sign_ocr_text = ttk.Entry(self.sign_frame, width=30)
        self.sign_ocr_text.pack(fill=tk.X, padx=5, pady=1)
        
        # Apply button for sign - compact
        ttk.Button(self.sign_frame, text="✅ Aplikovať", command=self.apply_sign_attributes).pack(pady=5)
        
        # Notes section - compact
        notes_frame = ttk.LabelFrame(parent, text="📝 Poznámky")
        notes_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.notes_text = scrolledtext.ScrolledText(notes_frame, width=40, height=3,
                                                  bg=self.colors['bg_medium'], fg=self.colors['fg_normal'],
                                                  insertbackground=self.colors['fg_normal'])
        self.notes_text.pack(padx=3, pady=3, fill=tk.BOTH, expand=True)
        
        # Statistics - compact
        stats_frame = ttk.Frame(parent)
        stats_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.stats_label = ttk.Label(stats_frame, text="Nosiče: 0 | Značky: 0", font=('TkDefaultFont', 8))
        self.stats_label.pack(padx=5, pady=2)
        
        # Hide attribute frames initially
        self.holder_frame.pack_forget()
        self.sign_frame.pack_forget()
        
    def load_workspace_photos(self):
        """Load all photos from the workspace for fast switching."""
        try:
            config_path = Path(__file__).parent / "workspace_config.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                self.photos_dir = Path(config['directories']['raw_photos'])
                print(f"📂 Loading photos from: {self.photos_dir}")
                
                # Find all image files
                image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff"]
                self.photo_files = []
                
                for ext in image_extensions:
                    self.photo_files.extend(self.photos_dir.glob(ext))
                    self.photo_files.extend(self.photos_dir.glob(ext.upper()))
                
                # Remove duplicates and sort
                self.photo_files = sorted(list(set(self.photo_files)))
                self.current_photo_index = 0
                
                print(f"📸 Found {len(self.photo_files)} photos total")
                
                if self.photo_files:
                    # Add small delay to ensure canvas is fully ready
                    self.root.after(200, lambda: self.load_photo_safely(str(self.photo_files[0])))
                    self.update_photo_navigation_info()
                else:
                    messagebox.showwarning("No Photos", "No image files found in the workspace directory.")
                    
            else:
                messagebox.showwarning("Warning", "Workspace not found. Use 'Open Photo' to select images manually.")
                self.photo_files = []
                self.current_photo_index = 0
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load workspace: {e}")
            self.photo_files = []
            self.current_photo_index = 0
    
    def open_photo(self):
        """Open photo file dialog."""
        file_path = filedialog.askopenfilename(
            title="Select Photo",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.load_photo(file_path)
    
    def load_all_photos_dialog(self):
        """Load all photos from a selected directory."""
        folder_path = filedialog.askdirectory(
            title="Select Folder with Photos",
            initialdir=str(Path.home() / "Desktop")
        )
        if folder_path:
            self.load_photos_from_directory(folder_path)
    
    def load_photos_from_directory(self, directory_path: str):
        """Load all photos from specified directory."""
        directory = Path(directory_path)
        print(f"📂 Loading photos from: {directory}")
        
        # Find all image files
        image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tiff"]
        self.photo_files = []
        
        for ext in image_extensions:
            self.photo_files.extend(directory.glob(ext))
            self.photo_files.extend(directory.glob(ext.upper()))
        
        # Remove duplicates and sort
        self.photo_files = sorted(list(set(self.photo_files)))
        self.current_photo_index = 0
        
        print(f"📸 Found {len(self.photo_files)} photos in directory")
        
        if self.photo_files:
            self.load_photo(str(self.photo_files[0]))
            self.update_photo_navigation_info()
            messagebox.showinfo("Success", f"Loaded {len(self.photo_files)} photos from:\n{directory}")
        else:
            messagebox.showwarning("No Photos", "No image files found in the selected directory.")
    
    def load_photo(self, image_path: str):
        """Load and display photo."""
        try:
            self.current_image_path = image_path
            self.current_image = cv2.imread(image_path)
            
            if self.current_image is None:
                messagebox.showerror("Error", f"Could not load image: {image_path}")
                return
            
            # Convert BGR to RGB for display
            rgb_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_image)
            
            # Calculate scale to fit in canvas (optimized for layout)
            # Force canvas to update and get real dimensions
            self.canvas.update_idletasks()
            canvas_width = max(self.canvas.winfo_width(), 1000)  # Ensure minimum size
            canvas_height = max(self.canvas.winfo_height(), 700)  # Ensure minimum size
            
            img_width, img_height = pil_image.size
            
            # Ensure dimensions are valid
            if img_width <= 0 or img_height <= 0:
                messagebox.showerror("Error", f"Invalid image dimensions: {img_width}x{img_height}")
                return
            
            scale_x = (canvas_width - 40) / img_width  # Leave some margin
            scale_y = (canvas_height - 40) / img_height
            self.scale_factor = min(scale_x, scale_y, 2.5)  # Allow upscaling up to 2.5x
            
            # Resize image
            new_width = int(img_width * self.scale_factor)
            new_height = int(img_height * self.scale_factor)
            
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.photo_tk = ImageTk.PhotoImage(pil_image)
            
            # Display on canvas
            self.canvas.delete("all")
            self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_tk)
            
            # Update canvas scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
        # Update UI
            filename = Path(image_path).name
            # Check if annotations exist for this image
            annotations_file = Path(__file__).parent / "data" / "annotations" / f"{Path(filename).stem}_annotations.json"
            annotation_status = "✅ Saved" if annotations_file.exists() else "❌ Not saved"
            
            # Update compact photo info
            img_info = f"{filename[:20]}{'...' if len(filename) > 20 else ''}"
            self.photo_info_label.configure(text=img_info)
            
            # Update save status icon
            status_icon = "✅" if annotations_file.exists() else "❌"
            self.save_status_label.configure(text=status_icon)
            
            # Load existing annotations if available
            self.load_existing_annotations()
            
            # Reset selection
            self.selected_box = None
            self.update_selection_info()
            
            print(f"✅ Loaded: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load photo: {e}")
    
    def on_canvas_click(self, event):
        """Handle mouse click on canvas."""
        if not self.current_image_path:
            return
            
        # Convert canvas coordinates to image coordinates
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Check if clicking on existing box
        clicked_box = self.find_box_at_position(canvas_x, canvas_y)
        if clicked_box:
            self.selected_box = clicked_box
            self.update_selection_info()
            self.highlight_selected_box()
            return
        
        # Start drawing new box
        self.drawing = True
        self.start_x = canvas_x
        self.start_y = canvas_y
        self.selected_box = None
        
    def on_canvas_drag(self, event):
        """Handle mouse drag on canvas."""
        if not self.drawing:
            return
            
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Remove previous temporary rectangle
        if self.current_box_id:
            self.canvas.delete(self.current_box_id)
        
        # Draw current rectangle
        color = "green" if self.draw_mode.get() == "holder" else "blue"
        self.current_box_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, canvas_x, canvas_y,
            outline=color, width=3, fill="", stipple="gray25"
        )
    
    def on_canvas_release(self, event):
        """Handle mouse release on canvas."""
        if not self.drawing:
            return
            
        self.drawing = False
        
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Calculate bounding box
        x1, y1 = min(self.start_x, canvas_x), min(self.start_y, canvas_y)
        x2, y2 = max(self.start_x, canvas_x), max(self.start_y, canvas_y)
        
        # Convert to original image coordinates
        orig_x1 = int(x1 / self.scale_factor)
        orig_y1 = int(y1 / self.scale_factor)
        orig_x2 = int(x2 / self.scale_factor)
        orig_y2 = int(y2 / self.scale_factor)
        
        # Minimum size check
        if abs(x2 - x1) < 10 or abs(y2 - y1) < 10:
            if self.current_box_id:
                self.canvas.delete(self.current_box_id)
            self.current_box_id = None
            return
        
        # Create annotation data
        box_type = self.draw_mode.get()
        box_data = {
            "id": len(self.current_boxes),
            "type": box_type,
            "canvas_coords": (x1, y1, x2, y2),
            "image_coords": (orig_x1, orig_y1, orig_x2, orig_y2),
            "canvas_id": self.current_box_id,
            "attributes": {}
        }
        
        if box_type == "holder":
            box_data["attributes"] = {
                "material": "unknown",
                "owner": "unknown", 
                "base_type": "unknown",
                "orientation": "unknown"
            }
        else:  # sign
            box_data["attributes"] = {
                "sign_code": "unknown",
                "sign_name": "",
                "ocr_text": "",
                "shape": "unknown"
            }
        
        self.current_boxes.append(box_data)
        self.selected_box = box_data
        
        self.update_selection_info()
        self.update_stats()
        
        self.current_box_id = None
        
        print(f"✅ Created {box_type} box: {orig_x1},{orig_y1} to {orig_x2},{orig_y2}")
    
    def on_right_click(self, event):
        """Handle right-click context menu."""
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        clicked_box = self.find_box_at_position(canvas_x, canvas_y)
        if clicked_box:
            # Create context menu
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="🗑️ Delete", command=lambda: self.delete_box(clicked_box))
            context_menu.add_separator()
            context_menu.add_command(label="📝 Edit Attributes", command=lambda: self.edit_box_attributes(clicked_box))
            
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
    
    def find_box_at_position(self, x: float, y: float):
        """Find bounding box at given position."""
        for box in self.current_boxes:
            x1, y1, x2, y2 = box["canvas_coords"]
            if x1 <= x <= x2 and y1 <= y <= y2:
                return box
        return None
    
    def update_selection_info(self):
        """Update the selection info display."""
        if self.selected_box:
            box = self.selected_box
            box_type = box["type"]
            x1, y1, x2, y2 = box["image_coords"]
            
            info = f"🎯 Selected: {box_type.title()}\n📏 Size: {x2-x1} × {y2-y1} px\n📍 Position: ({x1}, {y1})"
            
            if box_type == "holder":
                attrs = box["attributes"]
                info += f"\n🏗️ Material: {attrs.get('material', 'unknown')}"
                info += f"\n🏢 Owner: {attrs.get('owner', 'unknown')}"
                info += f"\n🔧 Type: {attrs.get('base_type', 'unknown')}"
                
                # Show holder attributes panel
                self.holder_frame.pack(fill=tk.X, pady=(0, 10))
                self.sign_frame.pack_forget()
                
                # Load current values
                self.holder_material.set(attrs.get('material', ''))
                self.holder_owner.set(attrs.get('owner', ''))
                self.holder_base_type.set(attrs.get('base_type', ''))
                self.holder_orientation.set(attrs.get('orientation', ''))
                
            else:  # sign
                attrs = box["attributes"]
                info += f"\n🚦 Code: {attrs.get('sign_code', 'unknown')}"
                info += f"\n📝 Name: {attrs.get('sign_name', '')[:20]}..."
                info += f"\n🔤 OCR: {attrs.get('ocr_text', '')[:20]}..."
                
                # Show sign attributes panel
                self.sign_frame.pack(fill=tk.X, pady=(0, 10))
                self.holder_frame.pack_forget()
                
                # Load current values
                self.sign_ocr_text.delete(0, tk.END)
                self.sign_ocr_text.insert(0, attrs.get('ocr_text', ''))
            
            self.selection_info.configure(text=info)
            self.highlight_selected_box()
        else:
            self.selection_info.configure(text="Nič")
            self.holder_frame.pack_forget()
            self.sign_frame.pack_forget()
            self.remove_highlights()
    
    def highlight_selected_box(self):
        """Highlight the selected bounding box."""
        self.remove_highlights()
        
        if self.selected_box:
            x1, y1, x2, y2 = self.selected_box["canvas_coords"]
            self.selected_box["highlight_id"] = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="yellow", width=4, fill="", stipple=""
            )
    
    def remove_highlights(self):
        """Remove all highlight rectangles."""
        for box in self.current_boxes:
            if "highlight_id" in box and box["highlight_id"]:
                self.canvas.delete(box["highlight_id"])
                box["highlight_id"] = None
    
    def apply_holder_attributes(self):
        """Apply holder attributes to selected box."""
        if not self.selected_box or self.selected_box["type"] != "holder":
            messagebox.showwarning("Warning", "Please select a holder box first.")
            return
        
        # Update attributes
        self.selected_box["attributes"].update({
            "material": self.holder_material.get(),
            "owner": self.holder_owner.get(),
            "base_type": self.holder_base_type.get(),
            "orientation": self.holder_orientation.get()
        })
        
        self.update_selection_info()
        messagebox.showinfo("Success", "Holder attributes applied!")
    
    def on_sign_search(self, event):
        """Handle search in Slovak signs database."""
        search_term = self.sign_search.get().lower()
        if len(search_term) < 2:
            self.sign_listbox.delete(0, tk.END)
            return
        
        # Search in database
        matches = []
        for code, sign in self.signs_db.signs.items():
            if (search_term in sign.name_sk.lower() or 
                search_term in sign.name_en.lower() or
                search_term in code):
                matches.append((code, sign))
        
        # Update listbox
        self.sign_listbox.delete(0, tk.END)
        for code, sign in matches[:20]:  # Limit to 20 results
            display_text = f"{code} - {sign.name_sk}"
            self.sign_listbox.insert(tk.END, display_text)
    
    def on_sign_select(self, event):
        """Handle sign selection from listbox."""
        selection = self.sign_listbox.curselection()
        if not selection:
            return
            
        # Get selected sign
        selected_text = self.sign_listbox.get(selection[0])
        sign_code = selected_text.split(" - ")[0]
        
        sign = self.signs_db.get_sign_by_code(sign_code)
        if sign:
            info = f"🚦 {sign_code} - {sign.name_sk}\n📝 {sign.name_en}\n🔤 Expected: {', '.join(sign.common_variations[:3])}"
            self.selected_sign_info.configure(text=info)
            
            # Store for applying
            self.current_sign_selection = {
                "code": sign_code,
                "name_sk": sign.name_sk,
                "name_en": sign.name_en,
                "shape": sign.shape
            }
    
    def apply_sign_attributes(self):
        """Apply sign attributes to selected box."""
        if not self.selected_box or self.selected_box["type"] != "sign":
            messagebox.showwarning("Warning", "Please select a sign box first.")
            return
        
        # Update attributes
        if hasattr(self, 'current_sign_selection'):
            self.selected_box["attributes"].update({
                "sign_code": self.current_sign_selection["code"],
                "sign_name": self.current_sign_selection["name_sk"],
                "shape": self.current_sign_selection["shape"]
            })
        
        self.selected_box["attributes"]["ocr_text"] = self.sign_ocr_text.get()
        
        self.update_selection_info()
        messagebox.showinfo("Success", "Sign attributes applied!")
    
    def delete_box(self, box):
        """Delete a bounding box."""
        # Remove from canvas
        if "canvas_id" in box and box["canvas_id"]:
            self.canvas.delete(box["canvas_id"])
        if "highlight_id" in box and box["highlight_id"]:
            self.canvas.delete(box["highlight_id"])
        
        # Remove from list
        self.current_boxes.remove(box)
        
        if self.selected_box == box:
            self.selected_box = None
            self.update_selection_info()
        
        self.update_stats()
        print(f"🗑️ Deleted {box['type']} box")
    
    def clear_all_boxes(self):
        """Clear all bounding boxes."""
        if not self.current_boxes:
            return
            
        if messagebox.askyesno("Confirm", "Delete all bounding boxes?"):
            for box in self.current_boxes:
                if "canvas_id" in box and box["canvas_id"]:
                    self.canvas.delete(box["canvas_id"])
                if "highlight_id" in box and box["highlight_id"]:
                    self.canvas.delete(box["highlight_id"])
            
            self.current_boxes.clear()
            self.selected_box = None
            self.update_selection_info()
            self.update_stats()
            print("🗑️ Cleared all boxes")
    
    def update_stats(self):
        """Update statistics display."""
        holders = sum(1 for box in self.current_boxes if box["type"] == "holder")
        signs = sum(1 for box in self.current_boxes if box["type"] == "sign")
        
        self.stats_label.configure(text=f"Nosiče: {holders} | Značky: {signs}")
    
    def save_annotations(self):
        """Save current annotations to file."""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "No image loaded.")
            return
        
        # Prepare annotation data
        filename = Path(self.current_image_path).name
        annotations = {
            "filename": filename,
            "image_path": str(self.current_image_path),
            "image_size": {
                "width": self.current_image.shape[1],
                "height": self.current_image.shape[0]
            },
            "holders": [],
            "signs": [],
            "notes": self.notes_text.get("1.0", tk.END).strip(),
            "annotated_by": "human",
            "annotation_date": datetime.now().isoformat(),
            "total_boxes": len(self.current_boxes)
        }
        
        # Organize boxes by type
        for box in self.current_boxes:
            x1, y1, x2, y2 = box["image_coords"]
            
            box_data = {
                "bounding_box": {
                    "x_min": x1, "y_min": y1, "x_max": x2, "y_max": y2,
                    "width": x2 - x1, "height": y2 - y1
                },
                "attributes": box["attributes"]
            }
            
            if box["type"] == "holder":
                annotations["holders"].append(box_data)
            else:
                annotations["signs"].append(box_data)
        
        # Save to annotations directory
        annotations_dir = Path(__file__).parent / "data" / "annotations"
        annotations_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = annotations_dir / f"{Path(filename).stem}_annotations.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(annotations, f, indent=2, ensure_ascii=False)
        
        messagebox.showinfo("Success", f"Annotations saved to:\n{output_file}")
        print(f"💾 Saved annotations: {output_file}")
    
    def load_existing_annotations(self):
        """Load existing annotations if available."""
        if not self.current_image_path:
            return
            
        filename = Path(self.current_image_path).name
        annotations_file = Path(__file__).parent / "data" / "annotations" / f"{Path(filename).stem}_annotations.json"
        
        if annotations_file.exists():
            try:
                with open(annotations_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Clear current boxes
                self.current_boxes.clear()
                self.canvas.delete("all")
                
                # Recreate image
                self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_tk)
                
                # Load holders
                for holder_data in data.get("holders", []):
                    self.load_annotation_box(holder_data, "holder")
                
                # Load signs  
                for sign_data in data.get("signs", []):
                    self.load_annotation_box(sign_data, "sign")
                
                # Load notes
                notes = data.get("notes", "")
                self.notes_text.delete("1.0", tk.END)
                self.notes_text.insert("1.0", notes)
                
                self.update_stats()
                print(f"📂 Loaded existing annotations: {len(self.current_boxes)} boxes")
                
            except Exception as e:
                print(f"⚠️ Could not load annotations: {e}")
    
    def load_annotation_box(self, box_data: Dict, box_type: str):
        """Load a single annotation box."""
        bbox = box_data["bounding_box"]
        
        # Convert to canvas coordinates
        x1 = int(bbox["x_min"] * self.scale_factor)
        y1 = int(bbox["y_min"] * self.scale_factor) 
        x2 = int(bbox["x_max"] * self.scale_factor)
        y2 = int(bbox["y_max"] * self.scale_factor)
        
        # Draw on canvas
        color = "green" if box_type == "holder" else "blue"
        canvas_id = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline=color, width=3, fill="", stipple="gray25"
        )
        
        # Create box data
        box = {
            "id": len(self.current_boxes),
            "type": box_type,
            "canvas_coords": (x1, y1, x2, y2),
            "image_coords": (bbox["x_min"], bbox["y_min"], bbox["x_max"], bbox["y_max"]),
            "canvas_id": canvas_id,
            "attributes": box_data.get("attributes", {})
        }
        
        self.current_boxes.append(box)
    
    def update_photo_navigation_info(self):
        """Update the photo navigation information display."""
        if hasattr(self, 'photo_files') and self.photo_files:
            current = self.current_photo_index + 1  # 1-based for user
            total = len(self.photo_files)
            self.photo_counter_label.configure(text=f"Photo {current} of {total}")
        else:
            self.photo_counter_label.configure(text="No photos loaded")
    
    def previous_photo(self):
        """Load previous photo."""
        if hasattr(self, 'photo_files') and self.photo_files:
            if len(self.photo_files) > 0:
                self.current_photo_index = (self.current_photo_index - 1) % len(self.photo_files)
                self.load_photo(str(self.photo_files[self.current_photo_index]))
                self.update_photo_navigation_info()
                print(f"⬅️ Previous photo: {self.current_photo_index + 1}/{len(self.photo_files)}")
    
    def next_photo(self):
        """Load next photo."""
        if hasattr(self, 'photo_files') and self.photo_files:
            if len(self.photo_files) > 0:
                self.current_photo_index = (self.current_photo_index + 1) % len(self.photo_files)
                self.load_photo(str(self.photo_files[self.current_photo_index]))
                self.update_photo_navigation_info()
                print(f"➡️ Next photo: {self.current_photo_index + 1}/{len(self.photo_files)}")
    
    def jump_to_photo(self, event=None):
        """Jump to a specific photo by number."""
        if not hasattr(self, 'photo_files') or not self.photo_files:
            messagebox.showwarning("Warning", "No photos loaded.")
            return
        
        try:
            photo_num = int(self.jump_entry.get())
            if 1 <= photo_num <= len(self.photo_files):
                self.current_photo_index = photo_num - 1  # Convert to 0-based
                self.load_photo(str(self.photo_files[self.current_photo_index]))
                self.update_photo_navigation_info()
                self.jump_entry.delete(0, tk.END)
                print(f"🎯 Jumped to photo: {photo_num}/{len(self.photo_files)}")
            else:
                messagebox.showwarning("Invalid Number", f"Please enter a number between 1 and {len(self.photo_files)}")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number.")
    
    def jump_by_offset(self, offset: int):
        """Jump by a specific offset (positive or negative)."""
        if not hasattr(self, 'photo_files') or not self.photo_files:
            return
        
        new_index = self.current_photo_index + offset
        new_index = max(0, min(new_index, len(self.photo_files) - 1))  # Clamp to valid range
        
        if new_index != self.current_photo_index:
            self.current_photo_index = new_index
            self.load_photo(str(self.photo_files[self.current_photo_index]))
            self.update_photo_navigation_info()
            print(f"🚀 Jumped {offset:+d} photos to: {self.current_photo_index + 1}/{len(self.photo_files)}")
    
    def toggle_drawing_mode(self):
        """Toggle between holder and sign drawing modes."""
        if self.draw_mode.get() == "holder":
            self.draw_mode.set("sign")
            print("🔄 Switched to Sign drawing mode (blue boxes)")
        else:
            self.draw_mode.set("holder")
            print("🔄 Switched to Holder drawing mode (green boxes)")
    
    def delete_selected_box(self):
        """Delete the currently selected box using keyboard shortcut."""
        if self.selected_box:
            self.delete_box(self.selected_box)
    
    def jump_to_first_photo(self):
        """Jump to the first photo."""
        if hasattr(self, 'photo_files') and self.photo_files:
            self.current_photo_index = 0
            self.load_photo(str(self.photo_files[self.current_photo_index]))
            self.update_photo_navigation_info()
            print(f"🏁 Jumped to first photo: 1/{len(self.photo_files)}")
    
    def jump_to_last_photo(self):
        """Jump to the last photo."""
        if hasattr(self, 'photo_files') and self.photo_files:
            self.current_photo_index = len(self.photo_files) - 1
            self.load_photo(str(self.photo_files[self.current_photo_index]))
            self.update_photo_navigation_info()
            print(f"🏁 Jumped to last photo: {len(self.photo_files)}/{len(self.photo_files)}")
    
    def on_multi_sign_toggle(self):
        """Handle multi-sign recognition toggle."""
        if self.multi_sign_var.get():
            print("🔢 Multi-sign recognition ENABLED - More than one sign on holder expected")
            messagebox.showinfo("Multi-Sign Mode", 
                              "Viac značiek na nosiči je teraz ZAPNUTÉ\n" +
                              "Očakáva sa viac ako jedna značka na nosič.\n\n" +
                              "Tip: Nakresli všetky značky na jednom nosiči.")
        else:
            print("🔢 Multi-sign recognition DISABLED - Single sign per holder expected")
    
    def auto_detect_attributes(self):
        """Auto-detect attributes using simple heuristics."""
        if not self.current_image_path or not self.current_boxes:
            messagebox.showwarning("Warning", "Načítaj obrázok a nakresli nejaké rámy najprv.")
            return
        
        detected_count = 0
        
        for box in self.current_boxes:
            if box["type"] == "holder":
                # Auto-detect holder attributes based on image analysis
                x1, y1, x2, y2 = box["image_coords"]
                width = x2 - x1
                height = y2 - y1
                area = width * height
                aspect_ratio = width / height if height > 0 else 1
                
                # Simple heuristics for material detection
                if area > 50000:  # Large holders are often concrete
                    box["attributes"]["material"] = "betón"
                elif aspect_ratio > 2:  # Wide holders often metal
                    box["attributes"]["material"] = "kov"
                else:
                    box["attributes"]["material"] = "kov"  # Default
                
                # Owner heuristics (simplified)
                if area > 100000:  # Very large = likely city/state
                    box["attributes"]["owner"] = "mesto"
                else:
                    box["attributes"]["owner"] = "obec"
                
                # Base type heuristics
                if height > width:  # Tall = likely single pole
                    box["attributes"]["base_type"] = "jeden stĺp"
                elif aspect_ratio > 3:  # Very wide = likely portal
                    box["attributes"]["base_type"] = "portálová konštrukcia"
                else:
                    box["attributes"]["base_type"] = "jeden stĺp"
                
                # Orientation default
                box["attributes"]["orientation"] = "v smere jazdy"
                
                detected_count += 1
                
            elif box["type"] == "sign":
                # Auto-detect sign attributes
                x1, y1, x2, y2 = box["image_coords"]
                width = x2 - x1
                height = y2 - y1
                aspect_ratio = width / height if height > 0 else 1
                
                # Shape detection based on aspect ratio
                if abs(aspect_ratio - 1) < 0.3:  # Nearly square
                    box["attributes"]["shape"] = "square"
                elif aspect_ratio > 1.5:  # Wide rectangle
                    box["attributes"]["shape"] = "rectangular"
                elif aspect_ratio < 0.7:  # Tall rectangle
                    box["attributes"]["shape"] = "rectangular"
                else:
                    box["attributes"]["shape"] = "circular"
                
                # Set some common defaults
                box["attributes"]["sign_code"] = "unknown"
                box["attributes"]["sign_name"] = "Detekcia potrebuje manuálne overenie"
                box["attributes"]["ocr_text"] = "[auto-detected]"
                
                detected_count += 1
        
        # Update UI if something was detected
        if detected_count > 0:
            self.update_selection_info()
            messagebox.showinfo("Auto-Detection Complete", 
                              f"Automaticky rozpoznané atribúty pre {detected_count} objektov.\n\n" +
                              "⚠️ Prosím skontroluj a oprav detekované hodnoty!")
            print(f"🤖 Auto-detected attributes for {detected_count} objects")
        else:
            messagebox.showinfo("No Objects", "Žiadne objekty na detekciu.")
    
    def reset_attributes(self):
        """Reset all attributes to unknown/default values."""
        if not self.current_boxes:
            messagebox.showwarning("Warning", "Žiadne objekty na reset.")
            return
        
        if not messagebox.askyesno("Confirm Reset", "Naozaj chceš resetovať všetky atribúty?"):
            return
        
        reset_count = 0
        
        for box in self.current_boxes:
            if box["type"] == "holder":
                box["attributes"] = {
                    "material": "unknown",
                    "owner": "unknown", 
                    "base_type": "unknown",
                    "orientation": "unknown"
                }
                reset_count += 1
            elif box["type"] == "sign":
                box["attributes"] = {
                    "sign_code": "unknown",
                    "sign_name": "",
                    "ocr_text": "",
                    "shape": "unknown"
                }
                reset_count += 1
        
        # Clear input fields
        self.holder_material.set('')
        self.holder_owner.set('')
        self.holder_base_type.set('')
        self.holder_orientation.set('')
        
        self.sign_search.delete(0, tk.END)
        self.sign_ocr_text.delete(0, tk.END)
        self.sign_listbox.delete(0, tk.END)
        self.selected_sign_info.configure(text="Nič")
        
        self.update_selection_info()
        
        messagebox.showinfo("Reset Complete", f"Resetované atribúty pre {reset_count} objektov.")
        print(f"🔄 Reset attributes for {reset_count} objects")
    
    def load_photo_safely(self, image_path: str):
        """Safely load photo with proper error handling."""
        try:
            # Ensure canvas is ready
            if not self.canvas.winfo_exists():
                print("⚠️ Canvas not ready, retrying...")
                self.root.after(100, lambda: self.load_photo_safely(image_path))
                return
                
            self.load_photo(image_path)
        except Exception as e:
            print(f"⚠️ Failed to load photo safely: {e}")
            messagebox.showerror("Error", f"Failed to load photo: {e}")

def main():
    """Run the annotation application."""
    root = tk.Tk()
    app = AnnotationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
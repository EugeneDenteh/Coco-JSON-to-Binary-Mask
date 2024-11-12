import os
import sys
import numpy as np
import cv2
from pycocotools.coco import COCO
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
from pathlib import Path

class CocoMaskConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("COCO JSON to Mask Converter")
        self.root.geometry("800x600")
        
        # Variables
        self.data_dir = tk.StringVar()
        self.ann_file = tk.StringVar()
        self.mask_dir = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready")
        self.preview_image = None
        
        self.create_widgets()
        self.center_window()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input Settings", padding="5")
        input_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Data directory
        ttk.Label(input_frame, text="Data Directory:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.data_dir, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_data_dir).grid(row=0, column=2)
        
        # Annotation file
        ttk.Label(input_frame, text="COCO JSON File:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.ann_file, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_ann_file).grid(row=1, column=2)
        
        # Output directory
        ttk.Label(input_frame, text="Output Directory:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.mask_dir, width=50).grid(row=2, column=1, padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_mask_dir).grid(row=2, column=2)
        
        # Preview section
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="5")
        preview_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.preview_label = ttk.Label(preview_frame, text="No preview available")
        self.preview_label.grid(row=0, column=0, padx=5, pady=5)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="5")
        progress_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Convert", command=self.start_conversion).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).grid(row=0, column=1, padx=5)

    def browse_data_dir(self):
        """Browse for data directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.data_dir.set(directory)
            
    def browse_ann_file(self):
        """Browse for annotation file"""
        file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file:
            self.ann_file.set(file)
            
    def browse_mask_dir(self):
        """Browse for mask output directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.mask_dir.set(directory)
            
    def update_preview(self, mask_path):
        """Update the preview with the latest generated mask"""
        try:
            # Load and resize the mask for preview
            mask = Image.open(mask_path)
            mask.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(mask)
            
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo  # Keep a reference
        except Exception as e:
            self.status_var.set(f"Preview error: {str(e)}")
            
    def convert_masks(self):
        """Convert COCO annotations to masks"""
        try:
            # Validate inputs
            if not all([self.data_dir.get(), self.ann_file.get(), self.mask_dir.get()]):
                raise ValueError("Please fill in all required fields")
                
            # Create mask directory if it doesn't exist
            os.makedirs(self.mask_dir.get(), exist_ok=True)
            
            # Load COCO annotations
            coco = COCO(self.ann_file.get())
            img_ids = coco.getImgIds()
            total_images = len(img_ids)
            
            for idx, img_id in enumerate(img_ids):
                # Update progress
                progress = (idx + 1) / total_images * 100
                self.progress_var.set(progress)
                self.status_var.set(f"Processing image {idx + 1} of {total_images}")
                self.root.update_idletasks()
                
                # Load image info and annotations
                img = coco.loadImgs(img_id)[0]
                ann_ids = coco.getAnnIds(imgIds=img['id'])
                anns = coco.loadAnns(ann_ids)
                
                # Create mask
                mask = np.zeros((img['height'], img['width']), dtype=np.uint8)
                for ann in anns:
                    if 'segmentation' in ann:
                        ann_mask = coco.annToMask(ann)
                        mask = np.maximum(mask, ann_mask)
                
                # Save mask
                mask_filename = os.path.splitext(img['file_name'])[0] + '_mask.png'
                mask_path = os.path.join(self.mask_dir.get(), mask_filename)
                cv2.imwrite(mask_path, mask * 255)
                
                # Update preview
                self.update_preview(mask_path)
                
            self.status_var.set("Conversion completed successfully!")
            messagebox.showinfo("Success", "Mask conversion completed!")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
            
        finally:
            self.progress_var.set(0)
            
    def start_conversion(self):
        """Start the conversion process in a separate thread"""
        conversion_thread = threading.Thread(target=self.convert_masks)
        conversion_thread.daemon = True
        conversion_thread.start()

def main():
    root = tk.Tk()
    app = CocoMaskConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
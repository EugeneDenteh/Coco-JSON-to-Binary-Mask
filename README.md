# COCO JSON to Binary Mask Converter
A user-friendly desktop application for converting COCO format annotations to binary segmentation masks.

## Overview
COCO Mask Converter is a graphical tool that converts COCO format JSON annotations into binary segmentation masks. It processes all images referenced in the COCO JSON file and generates corresponding mask files where annotated regions are represented as white pixels (255) on a black background (0).

## Installation

### Windows Installer (Recommended)
1. Download `COCO_Mask_Converter_Setup.exe` from the releases page
2. Run the installer
3. Follow the installation wizard prompts
4. Launch the application from the Start Menu or Desktop shortcut

### Manual Installation (Advanced Users)
If you prefer to run from source:
- Python 3.x required
- Install dependencies:
  ```bash
  pip install numpy opencv-python matplotlib pycocotools pillow
  ```

## Using the Application

1. **Launch the Application**:
   - Open "COCO Mask Converter" from the Start Menu or Desktop shortcut
   - The main window will appear with input fields and controls

2. **Select Input/Output Locations**:
   - Click "Browse" next to "Data Directory" to select your image folder
   - Click "Browse" next to "COCO JSON File" to select your annotations file
   - Click "Browse" next to "Output Directory" to choose where masks will be saved

3. **Convert Files**:
   - Click the "Convert" button to start processing
   - Progress bar will show conversion status
   - Preview window will show the latest generated mask
   - Wait for completion message

4. **View Results**:
   - Generated masks will be saved in your chosen output directory
   - Naming convention: `{original_image_name}_mask.png`

## Input Requirements

1. **COCO JSON Format**:
   - Must follow COCO format specification
   - Must contain valid segmentation annotations
   - Image references must match actual image files

2. **Images**:
   - Must be accessible at the paths specified in the COCO JSON
   - Supported formats: common image formats (jpg, png, etc.)

## Output Format
- Binary masks saved as PNG files
- Naming convention: `{original_image_name}_mask.png`
- Pixel values:
  - 0 (black): background
  - 255 (white): annotated regions

## Features
- User-friendly graphical interface
- Real-time conversion progress
- Mask preview functionality
- Automatic error handling
- Session history saving
- Configurable output options

## Limitations
- Processes only binary masks (no multi-class support)
- All overlapping segments are merged
- Memory usage scales with image size

## Troubleshooting

1. **Installation Issues**:
   - Ensure you have administrator rights when installing
   - Try running the installer in compatibility mode
   - Check Windows Defender or antivirus permissions

2. **Application Won't Start**:
   - Verify Windows version compatibility
   - Check for .NET Framework requirements
   - Try reinstalling the application

3. **Conversion Errors**:
   - Verify COCO JSON format
   - Check image file paths and permissions
   - Ensure sufficient disk space
   - Monitor system memory usage

## License
MIT License with Additional Restrictions

Copyright (c) 2024 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, and distribute copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the
following conditions:

1. The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

2. Commercial use is restricted. The Software may not be sold, either standalone
or as part of a larger package, without explicit written permission.

3. Any modifications or derivatives must also be shared under these same terms.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Support
For bug reports, feature requests, or general questions:
1. Open an issue in the repository
2. Provide detailed information about your system and the problem
3. Include steps to reproduce any issues

---
Remember to check for updates periodically for new features and improvements.

"""
**************************************************************************
**
**   adventure-utils.rpy - Utils for Adventure Module (for Ren'Py)
**
**   See adventure.rpy for version information.
**
**************************************************************************
This module is released under the MIT License:
==========================================================================

Copyright 2025 Jeffrey R. Day

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the “Software”),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

**************************************************************************
"""

# <init>
init python:
    import struct

    # <def>
    def adventure_create_multi_size_icns(base_image_path, output_icns_path):
        """
        Create .icns with multiple icon sizes by scaling down from 512x512
        Uses PNG embedding for better compatibility with modern macOS
        """
        import pygame
        import pygame.transform
        import struct
        
        try:
            # Load base image
            base_surface = pygame.image.load(base_image_path)
            base_width, base_height = base_surface.get_size()
            
            # If not square, we'll scale to the largest square that fits
            if base_width != base_height:
                print("Warning: Image is not square ({}x{}). Will crop/scale to square.".format(base_width, base_height))
                size = min(base_width, base_height)
                # Center crop to square
                x_offset = (base_width - size) // 2
                y_offset = (base_height - size) // 2
                crop_rect = pygame.Rect(x_offset, y_offset, size, size)
                base_surface = base_surface.subsurface(crop_rect).copy()
            
            # Scale to 512x512 if not already that size
            if base_surface.get_size() != (512, 512):
                print("Warning: Scaling image from {} to 512x512".format(base_surface.get_size()))
                base_surface = pygame.transform.smoothscale(base_surface, (512, 512))
            
            # Define icon sizes and their corresponding type codes
            # Using PNG-based type codes for better compatibility
            icon_sizes = [
                (512, 512, b'ic10'),  # 512x512 PNG
                (256, 256, b'ic09'),  # 256x256 PNG  
                (128, 128, b'ic08'),  # 128x128 PNG
                (64, 64, b'ic07'),    # 64x64 PNG
                (32, 32, b'ic12'),    # 32x32 PNG (retina 16x16)
                (16, 16, b'ic04')     # 16x16 PNG
            ]
            
            icon_data = []
            total_data_size = 0
            
            # Create temporary directory for scaled images
            temp_dir = "temp_icons"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            try:
                # Generate data for each size
                for i, (width, height, type_code) in enumerate(icon_sizes):
                    # Scale surface
                    if width == 512 and height == 512:
                        scaled_surface = base_surface.convert_alpha()
                    else:
                        scaled_surface = pygame.transform.smoothscale(base_surface, (width, height))
                        scaled_surface = scaled_surface.convert_alpha()
                    
                    # Save as temporary PNG
                    temp_png_path = os.path.join(temp_dir, "temp_{}.png".format(i))
                    pygame.image.save(scaled_surface, temp_png_path)
                    
                    # Read PNG data
                    with open(temp_png_path, 'rb') as f:
                        png_data = f.read()
                    
                    # Clean up temp file
                    os.remove(temp_png_path)
                    
                    icon_data.append((type_code, png_data))
                    total_data_size += 8 + len(png_data)  # 8 bytes header + data
                
                # Clean up temp directory
                os.rmdir(temp_dir)
                
            except Exception as e:
                # Clean up on error
                import shutil
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                raise e
            
            # Write .icns file
            with open(output_icns_path, 'wb') as f:
                # Main header
                f.write(b'icns')
                f.write(struct.pack('>I', 8 + total_data_size))
                
                # Write each icon entry
                for type_code, png_data in icon_data:
                    f.write(type_code)
                    f.write(struct.pack('>I', 8 + len(png_data)))
                    f.write(png_data)
            
            return True
            
        except Exception as e:
            print("Error creating multi-size .icns: {}".format(str(e)))
            return False
    # </def adventure_create_multi_size_icns>
    
    # <def>
    def adventure_create_multi_size_ico(base_image_path, output_ico_path):
        """
        Create .ico with multiple icon sizes by scaling down from base image
        Uses PNG embedding for better quality and transparency support
        """
        import pygame
        import pygame.transform
        import struct
        
        try:
            # Load base image
            base_surface = pygame.image.load(base_image_path)
            base_width, base_height = base_surface.get_size()
            
            # Define icon sizes for Windows .ico
            icon_sizes = [
                (16, 16),
                (32, 32), 
                (48, 48),
                (256, 256)
            ]
            
            png_data_list = []
            
            # Create temporary directory for scaled images
            temp_dir = "temp_ico"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            try:
                # Generate PNG data for each size
                for i, (width, height) in enumerate(icon_sizes):
                    # Scale surface
                    if (width, height) == (base_width, base_height):
                        scaled_surface = base_surface.convert_alpha()
                    else:
                        scaled_surface = pygame.transform.smoothscale(base_surface, (width, height))
                        scaled_surface = scaled_surface.convert_alpha()
                    
                    # Save as temporary PNG
                    temp_png_path = os.path.join(temp_dir, "temp_{}.png".format(i))
                    pygame.image.save(scaled_surface, temp_png_path)
                    
                    # Read PNG data
                    with open(temp_png_path, 'rb') as f:
                        png_data = f.read()
                    
                    png_data_list.append((width, height, png_data))
                    
                    # Clean up temp file
                    os.remove(temp_png_path)
                
                # Clean up temp directory
                os.rmdir(temp_dir)
                
            except Exception as e:
                # Clean up on error
                import shutil
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                raise e
            
            # Write .ico file
            with open(output_ico_path, 'wb') as f:
                num_images = len(png_data_list)
                
                # ICO Header (6 bytes)
                f.write(struct.pack('<H', 0))        # Reserved, must be 0
                f.write(struct.pack('<H', 1))        # Image type: 1 = icon
                f.write(struct.pack('<H', num_images)) # Number of images
                
                # Calculate offset for image data (header + directory entries)
                data_offset = 6 + (16 * num_images)
                
                # Write directory entries (16 bytes each)
                for width, height, png_data in png_data_list:
                    # For 256x256, width/height are stored as 0 in directory
                    w = 0 if width == 256 else width
                    h = 0 if height == 256 else height
                    
                    f.write(struct.pack('<B', w))           # Width (0 = 256)
                    f.write(struct.pack('<B', h))           # Height (0 = 256)  
                    f.write(struct.pack('<B', 0))           # Color palette size (0 = no palette)
                    f.write(struct.pack('<B', 0))           # Reserved
                    f.write(struct.pack('<H', 1))           # Color planes
                    f.write(struct.pack('<H', 32))          # Bits per pixel (32 for RGBA)
                    f.write(struct.pack('<L', len(png_data))) # Image data size
                    f.write(struct.pack('<L', data_offset))   # Offset to image data
                    
                    data_offset += len(png_data)
                
                # Write image data (PNG format)
                for width, height, png_data in png_data_list:
                    f.write(png_data)
            
            return True
            
        except Exception as e:
            print("Error creating multi-size .ico: {}".format(str(e)))
            return False
    # </def adventure_create_multi_size_ico>

    # <def>
    def adventure_create_scaled_png(base_image_path, output_png_path, target_width, target_height):
        """
        Create a PNG file scaled to specified dimensions using the same crop/scale logic as the icon generators
        
        Args:
            base_image_path (str): Path to input image
            output_png_path (str): Path where PNG will be saved
            target_width (int): Desired width in pixels
            target_height (int): Desired height in pixels
        
        Returns:
            bool: True if successful, False otherwise
        """
        import pygame
        import pygame.transform
        import struct
        import os
        
        try:
            # Load base image
            base_surface = pygame.image.load(base_image_path)
            base_width, base_height = base_surface.get_size()
            
            print("Input image: {}x{}".format(base_width, base_height))
            print("Target size: {}x{}".format(target_width, target_height))
            
            # Handle non-square input if target is square
            if target_width == target_height and base_width != base_height:
                print("Warning: Input is not square ({}x{}). Will center crop to square.".format(base_width, base_height))
                size = min(base_width, base_height)
                # Center crop to square
                x_offset = (base_width - size) // 2
                y_offset = (base_height - size) // 2
                crop_rect = pygame.Rect(x_offset, y_offset, size, size)
                base_surface = base_surface.subsurface(crop_rect).copy()
                print("Cropped to: {}x{}".format(size, size))
            
            # Handle non-square target with square input (stretch to fit)
            elif target_width != target_height and base_width == base_height:
                print("Warning: Square input will be stretched to {}x{} aspect ratio".format(target_width, target_height))
            
            # Handle different aspect ratios - fit within target maintaining aspect ratio
            elif target_width != target_height and base_width != base_height:
                # Calculate scaling to fit within target dimensions
                scale_x = target_width / base_width
                scale_y = target_height / base_height
                scale = min(scale_x, scale_y)  # Use smaller scale to fit within bounds
                
                new_width = int(base_width * scale)
                new_height = int(base_height * scale)
                
                print("Scaling to fit: {}x{} (scale factor: {:.3f})".format(new_width, new_height, scale))
                
                # Scale to fit size
                base_surface = pygame.transform.smoothscale(base_surface, (new_width, new_height))
                
                # Create target-sized surface with transparent background
                final_surface = pygame.Surface((target_width, target_height), pygame.SRCALPHA)
                final_surface.fill((0, 0, 0, 0))  # Transparent
                
                # Center the scaled image
                x_offset = (target_width - new_width) // 2
                y_offset = (target_height - new_height) // 2
                final_surface.blit(base_surface, (x_offset, y_offset))
                
                base_surface = final_surface
            
            # Scale to exact target size if not already handled above
            if base_surface.get_size() != (target_width, target_height) and not (target_width != target_height and base_width != base_height):
                print("Scaling from {} to {}x{}".format(base_surface.get_size(), target_width, target_height))
                base_surface = pygame.transform.smoothscale(base_surface, (target_width, target_height))
            
            # Convert to RGBA format
            final_surface = base_surface.convert_alpha()
            
            # Create output directory if needed
            output_dir = os.path.dirname(output_png_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Save as PNG
            pygame.image.save(final_surface, output_png_path)
            
            print("Successfully created PNG: {}".format(output_png_path))
            return True
            
        except Exception as e:
            print("Error creating scaled PNG: {}".format(str(e)))
            return False
    # </def adventure_create_scaled_png>

# </init>
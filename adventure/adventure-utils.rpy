init python:
     """
#*************************************************************************
#*
#*   adventure-utils.rpy - Utils for Adventure Module (for Ren'Py)
#*
#*   See adventure.rpy for version information.
#*
#*************************************************************************
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

#*************************************************************************
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
            temp_dir = os.path.join(renpy.config.basedir, "temp_icons")
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
            
            # If not square, we'll scale to the largest square that fits
            if base_width != base_height:
                print("Warning: Image is not square ({}x{}). Will crop/scale to square.".format(base_width, base_height))
                size = min(base_width, base_height)
                # Center crop to square
                x_offset = (base_width - size) // 2
                y_offset = (base_height - size) // 2
                crop_rect = pygame.Rect(x_offset, y_offset, size, size)
                base_surface = base_surface.subsurface(crop_rect).copy()
            
            # Scale to 256x256 if not already that size (using largest common size for ico)
            if base_surface.get_size() != (256, 256):
                print("Warning: Scaling image from {} to 256x256".format(base_surface.get_size()))
                base_surface = pygame.transform.smoothscale(base_surface, (256, 256))
            
            # Define icon sizes for Windows .ico
            icon_sizes = [
                (16, 16),
                (32, 32), 
                (48, 48),
                (256, 256)
            ]
            
            png_data_list = []
            
            # Create temporary directory for scaled images
            temp_dir = os.path.join(renpy.config.basedir, "temp_ico")
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            try:
                # Generate PNG data for each size
                for i, (width, height) in enumerate(icon_sizes):
                    # Scale surface
                    if width == 256 and height == 256:
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
                # print("Scaling from {} to {}x{}".format(base_surface.get_size(), target_width, target_height))
                base_surface = pygame.transform.smoothscale(base_surface, (target_width, target_height))
            
            # Convert to RGBA format
            final_surface = base_surface.convert_alpha()
            
            # Create output directory if needed
            output_dir = os.path.dirname(output_png_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Save as PNG
            pygame.image.save(final_surface, output_png_path)
            return True
            
        except Exception as e:
            print("Error creating scaled PNG: {}".format(str(e)))
            return False
    # </def adventure_create_scaled_png>

    # <def>
    def adventure_extract_png_from_ico(ico_path):
        """Extract highest resolution PNG data from .ico file"""
        try:
            with open(ico_path, 'rb') as f:
                # Read ICO header
                reserved = struct.unpack('<H', f.read(2))[0]
                image_type = struct.unpack('<H', f.read(2))[0]
                num_images = struct.unpack('<H', f.read(2))[0]
                
                if reserved != 0 or image_type != 1:
                    return None
                
                best_size = 0
                best_offset = 0
                best_data_size = 0
                
                # Read directory entries to find largest image
                for i in range(num_images):
                    width = struct.unpack('<B', f.read(1))[0]
                    height = struct.unpack('<B', f.read(1))[0]
                    f.read(2)  # Skip palette and reserved
                    f.read(4)  # Skip planes and bpp
                    data_size = struct.unpack('<L', f.read(4))[0]
                    offset = struct.unpack('<L', f.read(4))[0]
                    
                    # Handle 256x256 stored as 0
                    actual_width = 256 if width == 0 else width
                    actual_height = 256 if height == 0 else height
                    size = actual_width * actual_height
                    
                    if size > best_size:
                        best_size = size
                        best_offset = offset
                        best_data_size = data_size
                
                # Read the best image data
                f.seek(best_offset)
                return f.read(best_data_size)
        except:
            return None
    # </def adventure_extract_png_from_ico>
    
    # <def>
    def adventure_extract_png_from_icns(icns_path):
        """Extract highest resolution PNG data from .icns file"""
        try:
            with open(icns_path, 'rb') as f:
                # Read ICNS header
                magic = f.read(4)
                if magic != b'icns':
                    return None
                
                file_size = struct.unpack('>I', f.read(4))[0]
                
                best_size = 0
                best_data = None
                
                # Read chunks
                while f.tell() < file_size:
                    chunk_type = f.read(4)
                    if len(chunk_type) < 4:
                        break
                    
                    chunk_size = struct.unpack('>I', f.read(4))[0]
                    chunk_data_size = chunk_size - 8
                    
                    # PNG-based icon types with their sizes
                    png_types = {
                        b'ic04': 16,   # 16x16
                        b'ic05': 32,   # 32x32  
                        b'ic07': 64,   # 64x64
                        b'ic08': 128,  # 128x128
                        b'ic09': 256,  # 256x256
                        b'ic10': 512,  # 512x512
                        b'ic11': 32,   # 32x32 retina
                        b'ic12': 32,   # 32x32 retina
                        b'ic13': 256,  # 256x256 retina
                        b'ic14': 512   # 512x512 retina
                    }
                    
                    if chunk_type in png_types:
                        size = png_types[chunk_type]
                        if size >= best_size:
                            best_size = size
                            best_data = f.read(chunk_data_size)
                        else:
                            f.seek(chunk_data_size, 1)
                    else:
                        f.seek(chunk_data_size, 1)
                
                return best_data
        except:
            return None
    # </def adventure_extract_png_from_icns>
    
    # <def>
    def adventure_load_icon_as_displayable(file_path):
        """
        Load an icon file (.png, .ico, .icns) as a Ren'Py displayable.
        For .ico and .icns files, extracts the highest resolution available.
        
        Args:
            file_path (str): Path to the icon file
            
        Returns:
            renpy.display.im.Image or None: Displayable image or None on error
        """
        try:
            if not os.path.exists(file_path):
                print("Icon file not found: {}".format(file_path))
                return None
            
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.png':
                # Direct load for PNG files
                return Image(file_path)
            
            elif file_ext == '.ico':
                # Extract PNG data from ICO
                png_data = adventure_extract_png_from_ico(file_path)
                if png_data:
                    # Write to temporary file and load
                    temp_path = os.path.join(renpy.config.basedir, "temp_icon_display.png")
                    try:
                        with open(temp_path, 'wb') as f:
                            f.write(png_data)
                        # Load as Ren'Py image
                        img = Image(temp_path)
                        # Clean up temp file
                        os.remove(temp_path)
                        return img
                    except:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                        return None
                else:
                    print("Could not extract PNG data from ICO: {}".format(file_path))
                    return None
            
            elif file_ext == '.icns':
                # Extract PNG data from ICNS
                png_data = adventure_extract_png_from_icns(file_path)
                if png_data:
                    # Write to temporary file and load
                    temp_path = os.path.join(renpy.config.basedir, "temp_icon_display.png")
                    try:
                        with open(temp_path, 'wb') as f:
                            f.write(png_data)
                        # Load as Ren'Py image
                        img = Image(temp_path)
                        # Clean up temp file
                        os.remove(temp_path)
                        return img
                    except:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                        return None
                else:
                    print("Could not extract PNG data from ICNS: {}".format(file_path))
                    return None
            
            else:
                # Try to load as regular image
                try:
                    return Image(file_path)
                except:
                    print("Unsupported image format: {}".format(file_ext))
                    return None
                    
        except Exception as e:
            print("Error loading icon as displayable: {}".format(str(e)))
            return None
    # </def adventure_load_icon_as_displayable>

    # <def>
    def adventure_compare_icon_files(file1_path, file2_path, tolerance=0.05):
        """
        Compare two icon files (.png, .ico, .icns) by extracting highest resolution
        images and computing visual similarity with tolerance for compression artifacts.
        
        Args:
            file1_path (str): Path to first icon file
            file2_path (str): Path to second icon file  
            tolerance (float): Color difference tolerance (0.0-1.0, default 0.05)
        
        Returns:
            float: Similarity score from 0.0 (no similarity) to 1.0 (identical)
            Returns -1.0 on error
        """
        import pygame
        import pygame.transform
        import struct
        import os
        import math
                
        def load_image_from_data(data, is_png_data=False):
            """Load pygame surface from raw data or PNG data"""
            try:
                if is_png_data and data:
                    # Write PNG data to temp file and load
                    temp_path = os.path.join(renpy.config.basedir, "temp_compare.png")
                    try:
                        with open(temp_path, 'wb') as f:
                            f.write(data)
                        surface = pygame.image.load(temp_path)
                        os.remove(temp_path)
                        return surface
                    except:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                        return None
                else:
                    # Direct load for regular files
                    return pygame.image.load(data)
            except:
                return None
        
        def get_highest_resolution_surface(file_path):
            """Get highest resolution surface from any supported icon file"""
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.png':
                return load_image_from_data(file_path)
            elif file_ext == '.ico':
                png_data = adventure_extract_png_from_ico(file_path)
                return load_image_from_data(png_data, is_png_data=True)
            elif file_ext == '.icns':
                png_data = adventure_extract_png_from_icns(file_path)
                return load_image_from_data(png_data, is_png_data=True)
            else:
                # Try to load as regular image
                return load_image_from_data(file_path)
        
        def calculate_color_distance(color1, color2):
            """Calculate perceptual color distance using weighted RGB"""
            r1, g1, b1 = color1[:3]
            r2, g2, b2 = color2[:3]
            
            # Weighted RGB distance (accounts for human perception)
            dr = (r1 - r2) * 0.3
            dg = (g1 - g2) * 0.59  
            db = (b1 - b2) * 0.11
            
            return math.sqrt(dr*dr + dg*dg + db*db) / 255.0
        
        def compare_surfaces(surf1, surf2, tolerance):
            """Compare two pygame surfaces pixel by pixel with tolerance"""
            width1, height1 = surf1.get_size()
            width2, height2 = surf2.get_size()
            
            # Scale larger surface down to match smaller one
            if width1 * height1 > width2 * height2:
                surf1 = pygame.transform.smoothscale(surf1, (width2, height2))
                width1, height1 = width2, height2
            elif width2 * height2 > width1 * height1:
                surf2 = pygame.transform.smoothscale(surf2, (width1, height1))
                width2, height2 = width1, height1
            
            # Convert to same format
            surf1 = surf1.convert_alpha()
            surf2 = surf2.convert_alpha()
            
            total_pixels = width1 * height1
            matching_pixels = 0
            similarity_sum = 0.0
            
            for x in range(width1):
                for y in range(height1):
                    color1 = surf1.get_at((x, y))
                    color2 = surf2.get_at((x, y))
                    
                    # Handle alpha channel
                    alpha1 = color1[3] / 255.0 if len(color1) > 3 else 1.0
                    alpha2 = color2[3] / 255.0 if len(color2) > 3 else 1.0
                    
                    # If both pixels are fully transparent, consider them matching
                    if alpha1 == 0 and alpha2 == 0:
                        matching_pixels += 1
                        similarity_sum += 1.0
                        continue
                    
                    # Calculate alpha difference
                    alpha_diff = abs(alpha1 - alpha2)
                    
                    # Calculate color difference (weighted by alpha)
                    color_dist = calculate_color_distance(color1, color2)
                    
                    # Combine color and alpha differences
                    total_diff = (color_dist + alpha_diff) / 2.0
                    
                    # Calculate pixel similarity
                    pixel_similarity = max(0.0, 1.0 - (total_diff / tolerance)) if tolerance > 0 else (1.0 if total_diff == 0 else 0.0)
                    
                    if pixel_similarity > 0.5:  # Consider it a match if > 50% similar
                        matching_pixels += 1
                    
                    similarity_sum += pixel_similarity
            
            # Return average pixel similarity
            return similarity_sum / total_pixels if total_pixels > 0 else 0.0
        
        try:
            # Validate inputs
            if not os.path.exists(file1_path):
                print("Error: File does not exist: {}".format(file1_path))
                return -1.0
            
            if not os.path.exists(file2_path):
                print("Error: File does not exist: {}".format(file2_path))
                return -1.0
            
            if not (0.0 <= tolerance <= 1.0):
                print("Error: Tolerance must be between 0.0 and 1.0")
                return -1.0
            
            # Load highest resolution surfaces
            surface1 = get_highest_resolution_surface(file1_path)
            surface2 = get_highest_resolution_surface(file2_path)
            
            if surface1 is None:
                print("Error: Could not load image from {}".format(file1_path))
                return -1.0
            
            if surface2 is None:
                print("Error: Could not load image from {}".format(file2_path))
                return -1.0
            
            # Compare the surfaces
            similarity = compare_surfaces(surface1, surface2, tolerance)
            
            return similarity
            
        except Exception as e:
            print("Error comparing icon files: {}".format(str(e)))
            return -1.0
    # </def adventure_compare_icon_files>
    
    # <def>
    def adventure_compare_install_icons(new_icon, proceed = False):
        cand = os.path.join(renpy.config.gamedir, "gui/window_icon_candidate.png")
        adventure_create_scaled_png(new_icon, cand, 128, 128)     
        # <try>
        try:
            wicscore = adventure_compare_icon_files(cand, os.path.join(renpy.config.gamedir, "gui/window_icon.png"))
        except:
            wicscore = 0
        # </try>

        # <try>
        try:
            icnsscore = adventure_compare_icon_files(cand, os.path.join(renpy.config.basedir, "icon.icns"), 0.1)
        except:
            icnsscore = 0
        # </try>
        
        # <try>
        try:
            icoscore = adventure_compare_icon_files(cand, os.path.join(renpy.config.basedir, "icon.ico"))
        except:
            icoscore = 0
        # </try>

        # <if>
        if icnsscore < 0.8 or icoscore < 0.8 or wicscore < 0.8:
            # <if>
            if proceed:
                print("Converting icon ", adventure.game_icon, "...")
                # <try>
                try:
                    if icnsscore < 0.8:
                        adventure_create_multi_size_icns(os.path.join(renpy.config.gamedir, adventure.game_icon), os.path.join(renpy.config.basedir, "icon.icns"))
                        print("Created icon.icns")
                    if icoscore < 0.8:
                        adventure_create_multi_size_ico(os.path.join(renpy.config.gamedir, adventure.game_icon), os.path.join(renpy.config.basedir, "icon.ico"))
                        print("Created icon.ico")
                    if wicscore < 0.8:
                        import shutil
                        shutil.copy(cand, os.path.join(renpy.config.gamedir, "gui/window_icon.png"))
                    return True
                except Exception as e:
                    print("An error occurred: {}".format(str(e)))
                    return False
                # </try>
            else:
                return False
            # </if>
        else:
            return True
        # </if>
    # </def>

# </init>


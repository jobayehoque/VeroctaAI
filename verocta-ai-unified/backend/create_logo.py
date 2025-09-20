#!/usr/bin/env python3
"""
FinDash Logo Creator
Creates the official FinDash logo for PDF reports and branding
"""

import os
from PIL import Image, ImageDraw, ImageFont
import logging

def create_findash_logo(output_path="static/assets/images/findash-logo.png", size=(400, 200)):
    """Use the professional FinDash logo (no generation needed - logo already provided)"""
    # The professional FinDash logo is already in place
    # This function is kept for compatibility but doesn't generate anything
    if os.path.exists(output_path):
        logging.info(f"Professional FinDash logo already in place: {output_path}")
        return output_path
    else:
        logging.warning(f"Professional FinDash logo not found at: {output_path}")
        return None

def create_simple_text_logo(output_path="static/assets/images/findash-text-logo.png", size=(300, 100)):
    """Create a simple text-based logo"""
    try:
        # Create white background image
        img = Image.new('RGB', size, 'white')
        draw = ImageDraw.Draw(img)
        
        # Colors
        primary_blue = '#2E86AB'
        accent_orange = '#F18F01'
        
        try:
            font = ImageFont.truetype("Arial", 24)
        except:
            font = ImageFont.load_default()
        
        # Draw text
        text = "FinDash"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # Draw "FinDash" text
        draw.text((x, y), text, fill=primary_blue, font=font)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save logo
        img.save(output_path, 'PNG')
        logging.info(f"Simple text logo created: {output_path}")
        return output_path
        
    except Exception as e:
        logging.error(f"Error creating simple logo: {str(e)}")
        return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create logos
    print("Creating FinDash logos...")
    
    logo_path = create_findash_logo()
    if logo_path:
        print(f"✅ Main logo created: {logo_path}")
    
    text_logo_path = create_simple_text_logo()
    if text_logo_path:
        print(f"✅ Text logo created: {text_logo_path}")
    
    print("Logo creation complete!")

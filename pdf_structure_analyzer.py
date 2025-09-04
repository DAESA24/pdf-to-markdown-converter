#!/usr/bin/env python3
"""
PDF Structure Analyzer
Purpose: Determine if PDF contains actual text or is image-based (scanned)
"""

import sys
import os
import fitz  # PyMuPDF

def analyze_pdf_structure(pdf_path):
    """Analyze PDF structure to determine if it's text-based or image-based"""
    print("PDF STRUCTURE ANALYSIS")
    print("="*60)
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        print(f"Total pages: {total_pages}")
        
        # Analyze first few pages
        pages_to_check = min(3, total_pages)
        print(f"Analyzing first {pages_to_check} pages...")
        
        image_based_pages = 0
        text_based_pages = 0
        
        for page_num in range(pages_to_check):
            page = doc[page_num]
            print(f"\nPage {page_num + 1}:")
            print("-" * 30)
            
            # Check for text
            text = page.get_text().strip()
            text_length = len(text)
            print(f"  Text characters: {text_length}")
            
            # Check for images
            image_list = page.get_images()
            image_count = len(image_list)
            print(f"  Images found: {image_count}")
            
            # Check page dimensions and image coverage
            if image_count > 0:
                page_rect = page.rect
                page_area = page_rect.width * page_rect.height
                print(f"  Page dimensions: {page_rect.width:.0f} x {page_rect.height:.0f}")
                
                total_image_area = 0
                for img_index, img in enumerate(image_list):
                    # Get basic image info from the list
                    try:
                        # img is a tuple: (xref, smask, width, height, bpc, colorspace, alt. colorspace, name, filter)
                        if len(img) >= 4:
                            width = img[2] if img[2] else 0
                            height = img[3] if img[3] else 0
                            img_area = width * height
                            total_image_area += img_area
                            print(f"    Image {img_index + 1}: {width}x{height} pixels")
                        else:
                            print(f"    Image {img_index + 1}: Unable to determine dimensions")
                    except Exception as e:
                        print(f"    Image {img_index + 1}: Error getting dimensions - {e}")
                
                image_coverage = (total_image_area / page_area) * 100 if page_area > 0 else 0
                print(f"  Estimated image coverage: {image_coverage:.1f}% of page")
            
            # Classification logic
            if text_length < 50 and image_count > 0:
                print("  CLASSIFICATION: Likely IMAGE-BASED")
                image_based_pages += 1
            elif text_length > 100:
                print("  CLASSIFICATION: TEXT-BASED")
                text_based_pages += 1
            else:
                print("  CLASSIFICATION: UNCLEAR")
        
        doc.close()
        
        # Overall assessment
        print(f"\n" + "="*60)
        print("OVERALL ASSESSMENT")
        print("="*60)
        
        if image_based_pages > text_based_pages:
            print("RESULT: PDF appears to be IMAGE-BASED (scanned document)")
            print("RECOMMENDATION: OCR (Optical Character Recognition) needed for text extraction")
            print("NEXT STEPS:")
            print("  1. Install OCR library (like Tesseract + pytesseract)")
            print("  2. Extract images from PDF pages")
            print("  3. Run OCR on extracted images")
            print("  4. Compare OCR results with Claude's Markdown output")
            return "image-based"
        elif text_based_pages > image_based_pages:
            print("RESULT: PDF appears to be TEXT-BASED")
            print("WARNING: Text extraction still failed - investigate encoding/format issues")
            return "text-based"
        else:
            print("RESULT: MIXED or UNCLEAR PDF structure")
            print("RECOMMENDATION: Try OCR approach as fallback")
            return "unclear"
            
    except Exception as e:
        print(f"ERROR analyzing PDF structure: {str(e)}")
        return "error"

def main():
    # Default test file path
    default_pdf = r"C:\Users\drewa\My Drive - DA72\@File - DA72\@SOR Growth Framework\Scaling Innovation\scaling innovation up to page 33_2025-08-25_11.04.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_pdf
    
    print(f"Analyzing PDF: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"ERROR: File not found: {pdf_path}")
        return
    
    result = analyze_pdf_structure(pdf_path)
    
    print(f"\nFINAL DIAGNOSIS: {result}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Full Scope OCR Extractor
Purpose: Extract OCR text from pages 1-33 to match Claude's conversion scope
Strategy: Process same pages Claude converted for proper comparison
"""

import sys
import os
import fitz
import time

def extract_full_scope_ocr(pdf_path, max_pages=33, output_file="full_scope_ocr_text.txt"):
    """Extract OCR text from pages 1-33 to match Claude's scope"""
    print("FULL SCOPE OCR EXTRACTION")
    print("="*50)
    print(f"Target: Extract text from pages 1-{max_pages}")
    print("Goal: Match the scope Claude converted for proper fidelity comparison")
    
    try:
        import easyocr
        
        print("Loading EasyOCR...")
        reader = easyocr.Reader(['en'], verbose=False)
        print("[OK] EasyOCR ready")
        
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        pages_to_process = min(max_pages, total_pages)
        
        print(f"[OK] PDF opened: {total_pages} pages")
        print(f"[OK] Processing pages 1-{pages_to_process} to match Claude's scope")
        
        all_text = []
        total_chars = 0
        
        for page_num in range(pages_to_process):
            print(f"Processing page {page_num + 1}...", end=" ")
            
            page = doc[page_num]
            mat = fitz.Matrix(2.0, 2.0)  # Higher resolution for better OCR
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            # Run OCR
            results = reader.readtext(img_data)
            
            if results:
                page_text = " ".join([text for (bbox, text, confidence) in results if confidence > 0.5])
                all_text.append(page_text)
                page_chars = len(page_text)
                total_chars += page_chars
                print(f"[OK] {page_chars} chars")
            else:
                print("[WARNING] No text")
        
        doc.close()
        
        # Combine all pages into single text block for comparison
        full_text = " ".join(all_text)
        
        # Save extracted text
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        print(f"\n[SUCCESS] Full scope OCR extraction complete")
        print(f"[OK] Total pages processed: {pages_to_process}")
        print(f"[OK] Total characters: {len(full_text)}")
        print(f"[OK] Saved to: {output_file}")
        
        return output_file if len(full_text) > 1000 else None
        
    except ImportError:
        print("[ERROR] EasyOCR not available")
        return None
    except Exception as e:
        print(f"[ERROR] OCR extraction failed: {e}")
        return None

def main():
    """Test full scope extraction"""
    pdf_path = r"C:\Users\drewa\My Drive - DA72\@File - DA72\@SOR Growth Framework\Scaling Innovation\scaling innovation up to page 33_2025-08-25_11.04.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"[ERROR] PDF file not found: {pdf_path}")
        return
    
    result = extract_full_scope_ocr(pdf_path, max_pages=33)
    
    if result:
        print(f"\n[FOUNDATION TEST PASSED]")
        print("OCR text extraction successful with proper scope matching")
        print("Ready for word-for-word fidelity comparison")
    else:
        print(f"\n[FOUNDATION TEST FAILED]")
        print("Cannot proceed with validation - OCR extraction unsuccessful")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
PDF OCR Text Extractor
Purpose: Extract text from image-based PDFs using EasyOCR
Strategy: Convert PDF pages to images, then run OCR to extract text
"""

import sys
import os
import fitz  # PyMuPDF
from pathlib import Path
import time

# Set UTF-8 encoding for output
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def extract_text_with_ocr(pdf_path, max_pages=3):
    """Extract text from image-based PDF using OCR"""
    print("PDF OCR TEXT EXTRACTION")
    print("="*60)
    
    try:
        # Import EasyOCR
        print("Loading EasyOCR (this may take a moment on first run)...")
        import easyocr
        reader = easyocr.Reader(['en'])  # English language
        print("[OK] EasyOCR loaded successfully")
        
        # Open PDF
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        print(f"[OK] PDF opened: {total_pages} pages")
        
        # Process pages
        pages_to_process = min(max_pages, total_pages)
        print(f"[OK] Processing first {pages_to_process} pages for OCR...")
        
        all_text = []
        
        for page_num in range(pages_to_process):
            print(f"\nProcessing page {page_num + 1}...")
            page = doc[page_num]
            
            # Convert page to image
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better OCR accuracy
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            
            print(f"  [OK] Page converted to image ({len(img_data)} bytes)")
            
            # Run OCR
            print("  [OCR] Running text recognition...")
            start_time = time.time()
            
            # EasyOCR expects image as bytes, numpy array, or file path
            results = reader.readtext(img_data)
            
            ocr_time = time.time() - start_time
            print(f"  [OK] OCR completed in {ocr_time:.1f} seconds")
            
            # Extract text from results
            page_text = ""
            detected_text_blocks = len(results)
            
            if detected_text_blocks > 0:
                print(f"  [OK] Found {detected_text_blocks} text blocks")
                
                # Show first few text blocks for verification
                for i, (bbox, text, confidence) in enumerate(results[:3]):
                    print(f"    Block {i+1}: '{text[:50]}...' (confidence: {confidence:.2f})")
                
                # Combine all text
                page_text = " ".join([text for (bbox, text, confidence) in results if confidence > 0.5])
                
                print(f"  [OK] Extracted {len(page_text)} characters from page {page_num + 1}")
                if len(page_text) > 0:
                    print(f"  [PREVIEW] First 200 characters:")
                    print("  " + "-" * 50)
                    print("  " + page_text[:200])
                    print("  " + "-" * 50)
                else:
                    print("  [WARNING] No text extracted (low confidence)")
            else:
                print("  [WARNING] No text blocks detected")
            
            all_text.append(f"=== PAGE {page_num + 1} ===\n{page_text}\n")
        
        doc.close()
        
        # Combine all pages
        full_text = "\n".join(all_text)
        
        print(f"\n" + "="*60)
        print("OCR EXTRACTION SUMMARY")
        print("="*60)
        print(f"Total characters extracted: {len(full_text)}")
        print(f"Pages processed: {pages_to_process}")
        
        if len(full_text) > 100:
            print("[SUCCESS] OCR text extraction working!")
            print(f"\nFirst 500 characters of combined text:")
            print("-" * 60)
            print(full_text[:500])
            print("-" * 60)
            return full_text
        else:
            print("[WARNING] Very little text extracted - may need OCR tuning")
            return full_text
            
    except ImportError:
        print("[ERROR] EasyOCR not installed. Run: pip install easyocr")
        return None
    except Exception as e:
        print(f"[ERROR] OCR extraction failed: {str(e)}")
        return None

def main():
    # Default test file path
    default_pdf = r"C:\Users\drewa\My Drive - DA72\@File - DA72\@SOR Growth Framework\Scaling Innovation\scaling innovation up to page 33_2025-08-25_11.04.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_pdf
    
    print(f"Testing OCR extraction on: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"[ERROR] File not found: {pdf_path}")
        return
    
    # Extract text using OCR
    extracted_text = extract_text_with_ocr(pdf_path, max_pages=3)
    
    if extracted_text:
        print(f"\n{'='*60}")
        print("FOUNDATION TEST RESULT")
        print("="*60)
        print("[SUCCESS] OCR-based PDF text extraction is working!")
        print("Next step: Build word-level comparison with Markdown output")
        
        # Save extracted text for comparison
        output_file = "ocr_extracted_text_sample.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        print(f"[OK] Sample OCR text saved to: {output_file}")
        
    else:
        print(f"\n{'='*60}")
        print("FOUNDATION TEST RESULT")
        print("="*60)
        print("[FAILED] OCR text extraction failed")
        print("Cannot proceed with validation system")

if __name__ == "__main__":
    main()
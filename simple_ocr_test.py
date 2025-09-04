#!/usr/bin/env python3
"""
Simple OCR Test - No fancy formatting, just results
"""

import sys
import os
import fitz

def test_ocr_extraction(pdf_path):
    print("Simple OCR Test")
    print("===============")
    
    try:
        # Import EasyOCR
        print("Loading EasyOCR...")
        import easyocr
        reader = easyocr.Reader(['en'], verbose=False)  # Disable verbose to avoid unicode issues
        print("EasyOCR loaded successfully")
        
        # Open PDF
        doc = fitz.open(pdf_path)
        print(f"PDF opened: {len(doc)} pages")
        
        # Test first page only
        page = doc[0]
        print("Converting page 1 to image...")
        
        # Convert to image with higher resolution
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        
        print(f"Image created: {len(img_data)} bytes")
        print("Running OCR...")
        
        # Run OCR
        results = reader.readtext(img_data)
        
        print(f"OCR completed: found {len(results)} text blocks")
        
        # Extract text
        if results:
            print("\nFirst few text blocks:")
            for i, (bbox, text, confidence) in enumerate(results[:5]):
                clean_text = text.encode('ascii', 'ignore').decode('ascii')[:50]
                print(f"  {i+1}: '{clean_text}' (confidence: {confidence:.2f})")
            
            # Combine all text
            full_text = " ".join([text for (bbox, text, confidence) in results if confidence > 0.5])
            print(f"\nTotal characters extracted: {len(full_text)}")
            
            if len(full_text) > 100:
                print("SUCCESS: OCR extraction working!")
                
                # Save to file
                with open('ocr_test_output.txt', 'w', encoding='utf-8') as f:
                    f.write(full_text)
                print("OCR text saved to: ocr_test_output.txt")
                
            else:
                print("WARNING: Very little text extracted")
        else:
            print("ERROR: No text blocks found")
        
        doc.close()
        
    except Exception as e:
        print(f"ERROR: {str(e)}")

def main():
    pdf_path = r"C:\Users\drewa\My Drive - DA72\@File - DA72\@SOR Growth Framework\Scaling Innovation\scaling innovation up to page 33_2025-08-25_11.04.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"ERROR: File not found: {pdf_path}")
        return
    
    test_ocr_extraction(pdf_path)

if __name__ == "__main__":
    main()
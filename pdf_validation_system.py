#!/usr/bin/env python3
"""
Complete PDF-to-Markdown Validation System
Purpose: End-to-end validation from PDF OCR through comparison analysis
Strategy: Combine OCR extraction with comparison engine for full validation
"""

import sys
import os
import time
from text_comparison_engine import TextComparisonEngine

def extract_pdf_text_ocr(pdf_path, output_file="extracted_pdf_text.txt", max_pages=5):
    """Extract text from PDF using OCR and save to file"""
    print("STEP 1: OCR TEXT EXTRACTION")
    print("="*50)
    
    try:
        import easyocr
        import fitz
        
        print("Loading EasyOCR...")
        reader = easyocr.Reader(['en'], verbose=False)
        print("[OK] EasyOCR ready")
        
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        pages_to_process = min(max_pages, total_pages)
        
        print(f"[OK] PDF opened: {total_pages} pages")
        print(f"[OK] Processing first {pages_to_process} pages...")
        
        all_text = []
        
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
                all_text.append(f"=== PAGE {page_num + 1} ===\n{page_text}\n")
                print(f"[OK] {len(page_text)} chars extracted")
            else:
                print("[WARNING] No text extracted")
        
        doc.close()
        
        # Save extracted text
        full_text = "\n".join(all_text)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        print(f"\n[SUCCESS] OCR extraction complete")
        print(f"[OK] Total characters: {len(full_text)}")
        print(f"[OK] Saved to: {output_file}")
        
        return output_file if len(full_text) > 100 else None
        
    except ImportError:
        print("[ERROR] EasyOCR not available")
        return None
    except Exception as e:
        print(f"[ERROR] OCR extraction failed: {e}")
        return None

def run_validation_comparison(ocr_file, markdown_file, report_file="validation_report.txt"):
    """Run complete validation comparison and save report"""
    print(f"\nSTEP 2: VALIDATION COMPARISON")
    print("="*50)
    
    engine = TextComparisonEngine()
    
    if not engine.load_texts(ocr_file, markdown_file):
        print("[ERROR] Could not load text files for comparison")
        return None
    
    print("[OK] Text files loaded successfully")
    results = engine.run_full_comparison()
    
    # Save detailed report
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("PDF-TO-MARKDOWN VALIDATION REPORT\n")
        f.write("="*60 + "\n\n")
        f.write(f"Source (PDF OCR): {ocr_file}\n")
        f.write(f"Target (Markdown): {markdown_file}\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("VALIDATION METRICS\n")
        f.write("-" * 30 + "\n")
        f.write(f"Word Fidelity:     {results['word_fidelity']:.1f}%\n")
        f.write(f"Grammar Structure: {results['grammar_score']:.1f}%\n") 
        f.write(f"Header Structure:  {results['header_score']:.1f}%\n")
        f.write(f"Overall Score:     {results['overall_score']:.1f}%\n\n")
        
        if results['word_fidelity'] >= 90:
            f.write("ASSESSMENT: Excellent word fidelity - conversion preserved nearly all content\n")
        elif results['word_fidelity'] >= 75:
            f.write("ASSESSMENT: Good word fidelity - minor content gaps identified\n")
        else:
            f.write("ASSESSMENT: Significant content differences - review conversion process\n")
    
    print(f"[OK] Detailed report saved to: {report_file}")
    return results

def main():
    """Complete PDF-to-Markdown validation workflow"""
    print("PDF-TO-MARKDOWN VALIDATION SYSTEM")
    print("="*60)
    
    # Default paths
    pdf_path = r"C:\Users\drewa\My Drive - DA72\@File - DA72\@SOR Growth Framework\Scaling Innovation\scaling innovation up to page 33_2025-08-25_11.04.pdf"
    markdown_path = r"C:\Users\drewa\My Drive - DA72\@File - DA72\@SOR Growth Framework\Scaling Innovation\scaling innovation up to page 33_2025-08-25_11.04_sonnet_20250825_131410.md"
    
    # Allow command line arguments
    if len(sys.argv) >= 3:
        pdf_path = sys.argv[1]
        markdown_path = sys.argv[2]
    
    print(f"PDF Source: {os.path.basename(pdf_path)}")
    print(f"Markdown Target: {os.path.basename(markdown_path)}")
    
    # Check files exist
    if not os.path.exists(pdf_path):
        print(f"[ERROR] PDF file not found: {pdf_path}")
        return
    
    if not os.path.exists(markdown_path):
        print(f"[ERROR] Markdown file not found: {markdown_path}")
        return
    
    # Step 1: Extract PDF text using OCR
    ocr_output_file = extract_pdf_text_ocr(pdf_path, max_pages=3)
    
    if not ocr_output_file:
        print(f"\n{'='*60}")
        print("VALIDATION FAILED - OCR EXTRACTION UNSUCCESSFUL")
        print("="*60)
        print("Cannot proceed without PDF text extraction")
        return
    
    # Step 2: Run comparison analysis
    results = run_validation_comparison(ocr_output_file, markdown_path)
    
    if not results:
        print(f"\n{'='*60}")
        print("VALIDATION FAILED - COMPARISON UNSUCCESSFUL")
        print("="*60)
        return
    
    # Final summary
    print(f"\n{'='*60}")
    print("VALIDATION COMPLETE - FINAL SUMMARY")
    print("="*60)
    print(f"Word Fidelity: {results['word_fidelity']:.1f}% (Your Priority #1)")
    print(f"Grammar Preservation: {results['grammar_score']:.1f}% (Your Priority #2)")
    print(f"Header Structure: {results['header_score']:.1f}% (Your Priority #3)")
    print(f"Overall Quality: {results['overall_score']:.1f}%")
    
    if results['overall_score'] >= 85:
        print("\n[EXCELLENT] PDF-to-Markdown conversion quality is very high")
    elif results['overall_score'] >= 70:
        print("\n[GOOD] PDF-to-Markdown conversion quality is acceptable")
    else:
        print("\n[NEEDS IMPROVEMENT] PDF-to-Markdown conversion has significant issues")
    
    print(f"\nDetailed report available in: validation_report.txt")

if __name__ == "__main__":
    main()
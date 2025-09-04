#!/usr/bin/env python3
"""
PDF Text Extraction Diagnostic Tool
Purpose: Test various PDF text extraction methods on Drew's test file
Strategy: Show exactly what each method extracts (or fails to extract)
"""

import sys
import os
from pathlib import Path

def test_pypdf2(pdf_path):
    """Test PyPDF2 extraction method"""
    print("\n" + "="*60)
    print("TESTING PYPDF2")
    print("="*60)
    
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            print(f"[OK] PDF opened successfully")
            print(f"[OK] Number of pages: {len(reader.pages)}")
            
            # Test first page
            if len(reader.pages) > 0:
                page = reader.pages[0]
                text = page.extract_text()
                
                print(f"[OK] Text length from page 1: {len(text)} characters")
                if len(text) > 0:
                    print(f"[OK] First 500 characters:")
                    print("-" * 40)
                    print(text[:500])
                    print("-" * 40)
                    return "SUCCESS", text
                else:
                    print("[ERROR] EXTRACTED ZERO CHARACTERS")
                    return "FAILED - NO TEXT", ""
            else:
                print("[ERROR] NO PAGES FOUND")
                return "FAILED - NO PAGES", ""
                
    except ImportError:
        print("[ERROR] PyPDF2 not installed")
        return "FAILED - NOT INSTALLED", ""
    except Exception as e:
        print(f"[ERROR] ERROR: {str(e)}")
        return "FAILED - EXCEPTION", str(e)

def test_pdfplumber(pdf_path):
    """Test pdfplumber extraction method"""
    print("\n" + "="*60)
    print("TESTING PDFPLUMBER")
    print("="*60)
    
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            print(f"[OK] PDF opened successfully")
            print(f"[OK] Number of pages: {len(pdf.pages)}")
            
            # Test first page
            if len(pdf.pages) > 0:
                page = pdf.pages[0]
                text = page.extract_text()
                
                if text:
                    print(f"[OK] Text length from page 1: {len(text)} characters")
                    print(f"[OK] First 500 characters:")
                    print("-" * 40)
                    print(text[:500])
                    print("-" * 40)
                    return "SUCCESS", text
                else:
                    print("[ERROR] EXTRACTED ZERO CHARACTERS")
                    return "FAILED - NO TEXT", ""
            else:
                print("[ERROR] NO PAGES FOUND")
                return "FAILED - NO PAGES", ""
                
    except ImportError:
        print("[ERROR] pdfplumber not installed")
        return "FAILED - NOT INSTALLED", ""
    except Exception as e:
        print(f"[ERROR] ERROR: {str(e)}")
        return "FAILED - EXCEPTION", str(e)

def test_pymupdf(pdf_path):
    """Test PyMuPDF (fitz) extraction method"""
    print("\n" + "="*60)
    print("TESTING PYMUPDF (FITZ)")
    print("="*60)
    
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        print(f"[OK] PDF opened successfully")
        print(f"[OK] Number of pages: {len(doc)}")
        
        # Test first page
        if len(doc) > 0:
            page = doc[0]
            text = page.get_text()
            
            print(f"[OK] Text length from page 1: {len(text)} characters")
            if len(text) > 0:
                print(f"[OK] First 500 characters:")
                print("-" * 40)
                print(text[:500])
                print("-" * 40)
                doc.close()
                return "SUCCESS", text
            else:
                print("[ERROR] EXTRACTED ZERO CHARACTERS")
                doc.close()
                return "FAILED - NO TEXT", ""
        else:
            print("[ERROR] NO PAGES FOUND")
            doc.close()
            return "FAILED - NO PAGES", ""
                
    except ImportError:
        print("[ERROR] PyMuPDF (fitz) not installed")
        return "FAILED - NOT INSTALLED", ""
    except Exception as e:
        print(f"[ERROR] ERROR: {str(e)}")
        return "FAILED - EXCEPTION", str(e)

def main():
    print("PDF TEXT EXTRACTION DIAGNOSTIC TOOL")
    print("="*60)
    
    # Default test file path
    default_pdf = r"C:\Users\drewa\My Drive - DA72\@File - DA72\@SOR Growth Framework\Scaling Innovation\scaling innovation up to page 33_2025-08-25_11.04.pdf"
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = default_pdf
    
    print(f"Testing PDF: {pdf_path}")
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"[ERROR] ERROR: File not found: {pdf_path}")
        print("Please provide the correct path as an argument or update the default path in the script.")
        return
    
    print(f"[OK] File exists ({os.path.getsize(pdf_path)} bytes)")
    
    # Test all extraction methods
    results = {}
    results['PyPDF2'] = test_pypdf2(pdf_path)
    results['pdfplumber'] = test_pdfplumber(pdf_path)
    results['PyMuPDF'] = test_pymupdf(pdf_path)
    
    # Summary
    print("\n" + "="*60)
    print("EXTRACTION METHOD SUMMARY")
    print("="*60)
    
    successful_methods = []
    for method, (status, text) in results.items():
        print(f"{method}: {status}")
        if "SUCCESS" in status:
            successful_methods.append((method, text))
    
    print(f"\nSuccessful methods: {len(successful_methods)}")
    
    if successful_methods:
        print(f"\nTARGET: RECOMMENDATION: Use {successful_methods[0][0]} for PDF extraction")
        print("[OK] FOUNDATION TEST PASSED - PDF text extraction is working")
    else:
        print("\nCRITICAL: CRITICAL FAILURE: NO EXTRACTION METHOD WORKED")
        print("[ERROR] FOUNDATION TEST FAILED - Cannot proceed with validation system")
        print("\nPossible issues:")
        print("- PDF might be image-based (scanned) rather than text-based")
        print("- PDF might be encrypted or password-protected")
        print("- PDF might use non-standard encoding")
        print("- Missing required libraries")

if __name__ == "__main__":
    main()
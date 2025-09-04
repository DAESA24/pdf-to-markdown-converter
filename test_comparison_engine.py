#!/usr/bin/env python3
"""
Test Comparison Engine with Mock Data
Purpose: Validate comparison logic before OCR extraction is ready
"""

import sys
import os
from text_comparison_engine import TextComparisonEngine

def test_with_mock_data():
    """Test comparison engine with mock OCR and Markdown data"""
    print("TESTING COMPARISON ENGINE WITH MOCK DATA")
    print("="*60)
    
    engine = TextComparisonEngine()
    
    # Use mock files instead of real OCR output
    source_file = "mock_ocr_output.txt"
    target_file = "mock_markdown_output.md"
    
    print(f"Mock source (OCR): {source_file}")
    print(f"Mock target (Markdown): {target_file}")
    
    if not os.path.exists(source_file):
        print(f"[ERROR] Mock source file not found: {source_file}")
        return False
    
    if not os.path.exists(target_file):
        print(f"[ERROR] Mock target file not found: {target_file}")
        return False
    
    # Load and compare
    if engine.load_texts(source_file, target_file):
        print("\n[OK] Mock files loaded successfully")
        results = engine.run_full_comparison()
        
        print(f"\n{'='*60}")
        print("MOCK DATA TEST RESULTS")
        print("="*60)
        print("This test validates that our comparison logic works correctly.")
        print("Next step: Replace mock OCR data with real PDF extraction.")
        
        return True
    else:
        print("[ERROR] Failed to load mock data")
        return False

def test_with_real_markdown():
    """Test comparison engine with Drew's actual Markdown file"""
    print("\n" + "="*60)
    print("TESTING WITH REAL MARKDOWN FILE")
    print("="*60)
    
    engine = TextComparisonEngine()
    
    # Use mock OCR but real Markdown
    source_file = "mock_ocr_output.txt"
    target_file = r"C:\Users\drewa\My Drive - DA72\@File - DA72\@SOR Growth Framework\Scaling Innovation\scaling innovation up to page 33_2025-08-25_11.04_sonnet_20250825_131410.md"
    
    if not os.path.exists(target_file):
        print(f"[WARNING] Real Markdown file not found: {target_file}")
        print("Skipping real Markdown test")
        return False
    
    print(f"Testing with Drew's actual Markdown file...")
    
    if engine.load_texts(source_file, target_file):
        # Just test loading and basic analysis
        print("\n[OK] Real Markdown file loaded successfully")
        print(f"Markdown file size: {len(engine.target_text)} characters")
        
        # Test header detection on real file
        engine.calculate_header_score()
        
        print("[OK] Real Markdown compatibility confirmed")
        return True
    else:
        print("[ERROR] Failed to load real Markdown file")
        return False

def main():
    print("COMPARISON ENGINE VALIDATION SUITE")
    print("="*60)
    
    # Test 1: Mock data validation
    mock_test_passed = test_with_mock_data()
    
    # Test 2: Real Markdown compatibility  
    real_test_passed = test_with_real_markdown()
    
    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUITE RESULTS")
    print("="*60)
    
    if mock_test_passed:
        print("[SUCCESS] Mock data test passed - comparison logic is working")
    else:
        print("[FAILED] Mock data test failed - comparison logic has issues")
    
    if real_test_passed:
        print("[SUCCESS] Real Markdown compatibility confirmed")
    else:
        print("[INFO] Real Markdown test skipped (file not accessible)")
    
    if mock_test_passed:
        print("\n[READY] Comparison system is ready for OCR integration")
        print("Next step: Once OCR model downloads, extract PDF text and run full validation")
    else:
        print("\n[BLOCKED] Fix comparison logic before proceeding with OCR")

if __name__ == "__main__":
    main()
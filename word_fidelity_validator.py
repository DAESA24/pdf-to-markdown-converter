#!/usr/bin/env python3
"""
Word-for-Word Fidelity Validator
Purpose: Compare OCR-extracted PDF text with Claude's Markdown for word preservation
Strategy: Foundation-first approach - focus only on Priority #1 (word fidelity)
"""

import re
from collections import Counter
import os

class WordFidelityValidator:
    def __init__(self):
        self.source_words = []
        self.target_words = []
        self.fidelity_score = 0.0
    
    def load_texts(self, ocr_file, markdown_file):
        """Load OCR and Markdown texts for comparison"""
        print("LOADING TEXTS FOR WORD FIDELITY ANALYSIS")
        print("="*50)
        
        try:
            with open(ocr_file, 'r', encoding='utf-8') as f:
                ocr_text = f.read().strip()
            print(f"[OK] OCR text loaded: {len(ocr_text)} characters")
            
            with open(markdown_file, 'r', encoding='utf-8') as f:
                markdown_text = f.read().strip()
            print(f"[OK] Markdown loaded: {len(markdown_text)} characters")
            
            # Extract words for comparison
            self.source_words = self.extract_words(ocr_text)
            self.target_words = self.extract_words(markdown_text)
            
            print(f"[OK] Source words extracted: {len(self.source_words)}")
            print(f"[OK] Target words extracted: {len(self.target_words)}")
            
            return True
            
        except FileNotFoundError as e:
            print(f"[ERROR] File not found: {e}")
            return False
        except Exception as e:
            print(f"[ERROR] Loading failed: {e}")
            return False
    
    def extract_words(self, text):
        """Extract meaningful words for fidelity comparison"""
        # Clean text for comparison
        # Remove markdown formatting
        clean_text = re.sub(r'[#*_`\-\|]', ' ', text)
        # Remove extra whitespace and page markers
        clean_text = re.sub(r'={3,}.*?={3,}', ' ', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text)
        # Convert to lowercase
        clean_text = clean_text.lower().strip()
        
        # Extract words (3+ characters to avoid noise)
        words = re.findall(r'\b[a-z]{3,}\b', clean_text)
        return words
    
    def calculate_word_fidelity(self):
        """Calculate word-for-word fidelity score"""
        print("\nWORD-FOR-WORD FIDELITY ANALYSIS")
        print("="*50)
        
        if not self.source_words:
            print("[ERROR] No source words found!")
            self.fidelity_score = 0.0
            return
        
        # Count word occurrences
        source_counter = Counter(self.source_words)
        target_counter = Counter(self.target_words)
        
        print(f"Source vocabulary: {len(source_counter)} unique words")
        print(f"Target vocabulary: {len(target_counter)} unique words")
        
        # Calculate fidelity using word intersection
        common_words = source_counter & target_counter
        total_common_occurrences = sum(common_words.values())
        total_source_occurrences = sum(source_counter.values())
        
        self.fidelity_score = (total_common_occurrences / total_source_occurrences) * 100 if total_source_occurrences > 0 else 0
        
        print(f"\nFIDELITY RESULTS:")
        print(f"Common words: {len(common_words)} unique types")
        print(f"Common word occurrences: {total_common_occurrences}")
        print(f"Source word occurrences: {total_source_occurrences}")
        print(f"WORD FIDELITY SCORE: {self.fidelity_score:.1f}%")
        
        # Show sample analysis
        missing_words = source_counter - target_counter
        if missing_words:
            print(f"\nSample missing words (first 15):")
            missing_list = list(missing_words.keys())[:15]
            print(f"  {', '.join(missing_list)}")
        
        # Show sample preserved words
        if common_words:
            print(f"\nSample preserved words (first 15):")
            preserved_list = list(common_words.keys())[:15]
            print(f"  {', '.join(preserved_list)}")
    
    def generate_fidelity_report(self, report_file="word_fidelity_report.txt"):
        """Generate focused word fidelity report"""
        print(f"\nSaving detailed report to: {report_file}")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("WORD-FOR-WORD FIDELITY VALIDATION REPORT\n")
            f.write("="*60 + "\n\n")
            f.write(f"PRIORITY #1: WORD FIDELITY SCORE: {self.fidelity_score:.1f}%\n\n")
            
            if self.fidelity_score >= 90:
                f.write("ASSESSMENT: Excellent - Nearly all words preserved in conversion\n")
                f.write("BUSINESS IMPACT: Claude's conversion maintained very high content fidelity\n")
            elif self.fidelity_score >= 75:
                f.write("ASSESSMENT: Good - Most words preserved with minor gaps\n") 
                f.write("BUSINESS IMPACT: Claude's conversion maintained acceptable content fidelity\n")
            elif self.fidelity_score >= 50:
                f.write("ASSESSMENT: Moderate - Significant word gaps identified\n")
                f.write("BUSINESS IMPACT: Conversion quality needs improvement\n")
            else:
                f.write("ASSESSMENT: Poor - Major word loss in conversion\n")
                f.write("BUSINESS IMPACT: Conversion quality is inadequate for business use\n")
            
            f.write(f"\nSOURCE ANALYSIS: {len(self.source_words)} total words, {len(set(self.source_words))} unique\n")
            f.write(f"TARGET ANALYSIS: {len(self.target_words)} total words, {len(set(self.target_words))} unique\n")
        
        return report_file
    
    def run_word_fidelity_validation(self):
        """Complete word fidelity validation workflow"""
        self.calculate_word_fidelity()
        report_file = self.generate_fidelity_report()
        
        return {
            'fidelity_score': self.fidelity_score,
            'report_file': report_file,
            'foundation_solid': self.fidelity_score >= 70  # Threshold for proceeding to grammar/formatting
        }

def main():
    """Test word fidelity validator"""
    print("WORD-FOR-WORD FIDELITY FOUNDATION TEST")
    print("="*60)
    
    # File paths
    ocr_file = "full_scope_ocr_text.txt"  # Will be created by full scope extractor
    markdown_file = r"C:\Users\drewa\My Drive - DA72\@File - DA72\@SOR Growth Framework\Scaling Innovation\scaling innovation up to page 33_2025-08-25_11.04_sonnet_20250825_131410.md"
    
    # Check if OCR extraction completed
    if not os.path.exists(ocr_file):
        print(f"[WAITING] OCR extraction not complete yet")
        print("Run full_scope_ocr_extractor.py first to extract text from pages 1-33")
        return
    
    # Run validation
    validator = WordFidelityValidator()
    
    if validator.load_texts(ocr_file, markdown_file):
        results = validator.run_word_fidelity_validation()
        
        print(f"\n{'='*60}")
        print("FOUNDATION TEST RESULTS")
        print("="*60)
        print(f"Word Fidelity Score: {results['fidelity_score']:.1f}%")
        
        if results['foundation_solid']:
            print("[FOUNDATION SOLID] Ready to proceed with grammar and formatting validation")
        else:
            print("[FOUNDATION ISSUES] Word fidelity below 70% - investigate before adding grammar/formatting")
        
        print(f"Detailed report: {results['report_file']}")
    
    else:
        print("[ERROR] Could not load texts for validation")

if __name__ == "__main__":
    main()
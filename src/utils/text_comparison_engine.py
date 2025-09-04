#!/usr/bin/env python3
"""
Text Comparison Engine for PDF-to-Markdown Validation
Purpose: Compare OCR-extracted PDF text with Claude's Markdown output
Strategy: Word-level comparison with business-focused metrics
"""

import re
import difflib
from collections import Counter
import os

class TextComparisonEngine:
    def __init__(self):
        self.source_text = ""
        self.target_text = ""
        self.word_fidelity_score = 0.0
        self.grammar_score = 0.0
        self.header_score = 0.0
    
    def load_texts(self, source_file, target_file):
        """Load source (OCR) and target (Markdown) texts"""
        print("LOADING TEXT FILES")
        print("="*50)
        
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                self.source_text = f.read().strip()
            print(f"[OK] Source loaded: {len(self.source_text)} characters")
            
            with open(target_file, 'r', encoding='utf-8') as f:
                self.target_text = f.read().strip()
            print(f"[OK] Target loaded: {len(self.target_text)} characters")
            
            return True
            
        except FileNotFoundError as e:
            print(f"[ERROR] File not found: {e}")
            return False
        except Exception as e:
            print(f"[ERROR] Loading failed: {e}")
            return False
    
    def clean_text_for_comparison(self, text):
        """Clean text for word-level comparison"""
        # Remove markdown formatting but keep structure
        text = re.sub(r'[#*_`]', '', text)  # Remove markdown symbols
        text = re.sub(r'\s+', ' ', text)    # Normalize whitespace
        text = text.lower().strip()         # Lowercase for comparison
        return text
    
    def extract_words(self, text):
        """Extract words from text for comparison"""
        clean_text = self.clean_text_for_comparison(text)
        words = re.findall(r'\b\w+\b', clean_text)
        return words
    
    def calculate_word_fidelity(self):
        """Calculate word-for-word fidelity score"""
        print("\nWORD FIDELITY ANALYSIS")
        print("-" * 30)
        
        source_words = self.extract_words(self.source_text)
        target_words = self.extract_words(self.target_text)
        
        print(f"Source words: {len(source_words)}")
        print(f"Target words: {len(target_words)}")
        
        if not source_words:
            print("[ERROR] No source words found!")
            self.word_fidelity_score = 0.0
            return
        
        # Count word matches
        source_counter = Counter(source_words)
        target_counter = Counter(target_words)
        
        # Calculate similarity using intersection
        common_words = source_counter & target_counter
        total_common = sum(common_words.values())
        total_source = sum(source_counter.values())
        
        self.word_fidelity_score = (total_common / total_source) * 100 if total_source > 0 else 0
        
        print(f"Common words: {len(common_words)} unique, {total_common} total")
        print(f"Word fidelity: {self.word_fidelity_score:.1f}%")
        
        # Show sample word differences
        missing_words = source_counter - target_counter
        if missing_words:
            print(f"Sample missing words: {list(missing_words.keys())[:10]}")
    
    def calculate_grammar_score(self):
        """Calculate grammar and sentence structure preservation"""
        print("\nGRAMMAR STRUCTURE ANALYSIS")
        print("-" * 30)
        
        # Extract sentences
        source_sentences = re.split(r'[.!?]+', self.source_text)
        target_sentences = re.split(r'[.!?]+', self.target_text)
        
        source_sentences = [s.strip() for s in source_sentences if s.strip()]
        target_sentences = [s.strip() for s in target_sentences if s.strip()]
        
        print(f"Source sentences: {len(source_sentences)}")
        print(f"Target sentences: {len(target_sentences)}")
        
        if not source_sentences:
            print("[ERROR] No source sentences found!")
            self.grammar_score = 0.0
            return
        
        # Simple grammar score based on sentence count similarity
        sentence_ratio = min(len(target_sentences), len(source_sentences)) / max(len(target_sentences), len(source_sentences), 1)
        self.grammar_score = sentence_ratio * 100
        
        print(f"Sentence structure score: {self.grammar_score:.1f}%")
    
    def calculate_header_score(self):
        """Calculate header identification and structure score"""
        print("\nHEADER STRUCTURE ANALYSIS")
        print("-" * 30)
        
        # Extract headers from markdown
        markdown_headers = re.findall(r'^#+\s+(.+)$', self.target_text, re.MULTILINE)
        
        # Extract potential headers from source (uppercase lines, etc.)
        source_lines = self.source_text.split('\n')
        potential_headers = []
        
        for line in source_lines:
            line = line.strip()
            if line and (line.isupper() or len(line.split()) <= 8):
                potential_headers.append(line)
        
        print(f"Markdown headers found: {len(markdown_headers)}")
        print(f"Potential source headers: {len(potential_headers)}")
        
        if markdown_headers:
            print("Sample markdown headers:")
            for i, header in enumerate(markdown_headers[:3]):
                print(f"  H{i+1}: {header}")
        
        if potential_headers:
            print("Sample potential headers:")
            for i, header in enumerate(potential_headers[:3]):
                print(f"  {i+1}: {header}")
        
        # Simple header score - presence of headers in markdown
        if len(markdown_headers) > 0:
            self.header_score = min(100, len(markdown_headers) * 20)  # 20 points per header, max 100
        else:
            self.header_score = 0.0
        
        print(f"Header structure score: {self.header_score:.1f}%")
    
    def generate_detailed_comparison(self):
        """Generate detailed text comparison using difflib"""
        print("\nDETAILED TEXT COMPARISON")
        print("-" * 30)
        
        source_lines = self.source_text.split('\n')
        target_lines = self.target_text.split('\n')
        
        # Create unified diff
        diff = list(difflib.unified_diff(
            source_lines, 
            target_lines, 
            fromfile='PDF (OCR)', 
            tofile='Markdown (Claude)', 
            n=3
        ))
        
        if diff:
            print("Sample differences (first 20 lines):")
            for line in diff[:20]:
                print(f"  {line.rstrip()}")
        else:
            print("No line-by-line differences found")
    
    def run_full_comparison(self):
        """Run complete comparison analysis"""
        print("\nPDF-TO-MARKDOWN VALIDATION ANALYSIS")
        print("="*60)
        
        self.calculate_word_fidelity()
        self.calculate_grammar_score()
        self.calculate_header_score()
        self.generate_detailed_comparison()
        
        # Overall assessment
        print(f"\n{'='*60}")
        print("VALIDATION RESULTS SUMMARY")
        print("="*60)
        print(f"1. Word Fidelity:     {self.word_fidelity_score:.1f}% (Priority #1)")
        print(f"2. Grammar Structure: {self.grammar_score:.1f}% (Priority #2)")
        print(f"3. Header Structure:  {self.header_score:.1f}% (Priority #3)")
        
        # Business-focused assessment
        overall_score = (self.word_fidelity_score * 0.6 + self.grammar_score * 0.3 + self.header_score * 0.1)
        print(f"\nWeighted Overall Score: {overall_score:.1f}%")
        
        if self.word_fidelity_score >= 90:
            print("[EXCELLENT] WORD FIDELITY: Nearly all words preserved")
        elif self.word_fidelity_score >= 75:
            print("[GOOD] WORD FIDELITY: Most words preserved, minor gaps")
        else:
            print("[NEEDS WORK] WORD FIDELITY: Significant word loss")
        
        return {
            'word_fidelity': self.word_fidelity_score,
            'grammar_score': self.grammar_score,
            'header_score': self.header_score,
            'overall_score': overall_score
        }

def main():
    """Test the comparison engine"""
    engine = TextComparisonEngine()
    
    # Test files (will be created by OCR extraction)
    source_file = "ocr_test_output.txt"  # OCR extracted text
    target_file = r"C:\Users\drewa\My Drive - DA72\@File - DA72\@SOR Growth Framework\Scaling Innovation\scaling innovation up to page 33_2025-08-25_11.04_sonnet_20250825_131410.md"
    
    print(f"Testing comparison engine...")
    print(f"Source (OCR): {source_file}")
    print(f"Target (Markdown): {target_file}")
    
    if engine.load_texts(source_file, target_file):
        results = engine.run_full_comparison()
        print(f"\nComparison complete. Results saved for further analysis.")
    else:
        print("Cannot run comparison - missing text files")
        print("Next steps:")
        print("1. Ensure OCR extraction completed successfully")
        print("2. Verify both source and target files exist")

if __name__ == "__main__":
    main()
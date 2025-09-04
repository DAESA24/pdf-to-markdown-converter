import os
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class QualityMetrics:
    """Container for markdown quality analysis results"""
    overall_quality_score: float
    structure_score: float
    content_richness_score: float
    formatting_score: float
    readability_score: float
    total_pages_processed: int
    word_count: int
    recommendations: List[str]

class PDFMarkdownQualityAnalyzer:
    """Analyzes the quality of PDF-to-Markdown conversion output"""
    
    def __init__(self):
        pass
    
    def analyze_structure(self, markdown_content: str) -> float:
        """Analyze document structure quality"""
        # Count structural elements
        headers = len(re.findall(r'^#+\s+', markdown_content, re.MULTILINE))
        h1_headers = len(re.findall(r'^#\s+', markdown_content, re.MULTILINE))
        h2_headers = len(re.findall(r'^##\s+', markdown_content, re.MULTILINE))
        h3_headers = len(re.findall(r'^###\s+', markdown_content, re.MULTILINE))
        
        # Lists
        bullet_lists = len(re.findall(r'^\s*[-*+]\s+', markdown_content, re.MULTILINE))
        numbered_lists = len(re.findall(r'^\s*\d+\.\s+', markdown_content, re.MULTILINE))
        
        # Other structural elements
        horizontal_rules = len(re.findall(r'^---+$', markdown_content, re.MULTILINE))
        bold_text = len(re.findall(r'\*\*[^*]+\*\*', markdown_content))
        italic_text = len(re.findall(r'\*[^*]+\*', markdown_content))
        
        # Calculate score based on structural richness
        structure_elements = headers + bullet_lists + numbered_lists + horizontal_rules
        formatting_elements = bold_text + italic_text
        
        # Normalize based on content length
        content_length = len(markdown_content)
        if content_length < 1000:
            base_score = 0.5
        else:
            # Expect roughly 1 structural element per 200 characters for good structure
            expected_structure = content_length // 200
            structure_ratio = min(structure_elements / max(expected_structure, 1), 2.0) * 0.5
            
            # Bonus for header hierarchy
            hierarchy_bonus = 0.1 if (h1_headers > 0 and h2_headers > 0) else 0
            
            # Bonus for formatting variety
            formatting_bonus = min(formatting_elements / 50, 0.2)
            
            base_score = structure_ratio + hierarchy_bonus + formatting_bonus
        
        return min(base_score, 1.0)
    
    def analyze_content_richness(self, markdown_content: str) -> float:
        """Analyze content richness and completeness"""
        # Word count and sentence analysis
        words = len(re.findall(r'\b\w+\b', markdown_content))
        sentences = len(re.findall(r'[.!?]+', markdown_content))
        paragraphs = len([p for p in markdown_content.split('\n\n') if p.strip()])
        
        # Check for various content types
        has_toc = bool(re.search(r'(table of contents|contents)', markdown_content, re.IGNORECASE))
        has_references = bool(re.search(r'(references|bibliography|notes)', markdown_content, re.IGNORECASE))
        has_numbers = bool(re.search(r'\d', markdown_content))
        has_mixed_case = bool(re.search(r'[A-Z]', markdown_content) and re.search(r'[a-z]', markdown_content))
        
        # Calculate richness score
        if words < 100:
            return 0.2
        elif words < 500:
            base_score = 0.4
        elif words < 2000:
            base_score = 0.6
        else:
            base_score = 0.8
        
        # Bonuses for content variety
        content_bonuses = 0
        if has_toc:
            content_bonuses += 0.05
        if has_references:
            content_bonuses += 0.05
        if has_numbers:
            content_bonuses += 0.05
        if has_mixed_case:
            content_bonuses += 0.05
        
        # Sentence variety bonus
        if sentences > 0:
            avg_words_per_sentence = words / sentences
            if 10 <= avg_words_per_sentence <= 25:  # Good sentence length variety
                content_bonuses += 0.05
        
        return min(base_score + content_bonuses, 1.0)
    
    def analyze_formatting_quality(self, markdown_content: str) -> float:
        """Analyze markdown formatting quality"""
        # Check for proper markdown syntax
        proper_headers = len(re.findall(r'^#+\s+[^\n]+$', markdown_content, re.MULTILINE))
        improper_headers = len(re.findall(r'^#+[^\s]', markdown_content, re.MULTILINE))  # No space after #
        
        # Check for consistent list formatting
        consistent_bullets = len(re.findall(r'^\s*-\s+', markdown_content, re.MULTILINE))
        mixed_bullets = len(re.findall(r'^\s*[*+]\s+', markdown_content, re.MULTILINE))
        
        # Check for proper emphasis formatting
        proper_bold = len(re.findall(r'\*\*[^*\n]+\*\*', markdown_content))
        proper_italic = len(re.findall(r'(?<!\*)\*(?!\*)([^*\n]+)\*(?!\*)', markdown_content))
        
        # Check for clean line breaks
        excessive_breaks = len(re.findall(r'\n{4,}', markdown_content))
        
        # Calculate formatting quality score
        total_formatting_elements = proper_headers + consistent_bullets + proper_bold + proper_italic
        formatting_issues = improper_headers + excessive_breaks
        
        if total_formatting_elements == 0:
            return 0.5  # Neutral if no formatting
        
        quality_ratio = total_formatting_elements / max(total_formatting_elements + formatting_issues, 1)
        
        # Bonus for formatting variety
        variety_bonus = 0.1 if (proper_bold > 0 and proper_italic > 0 and proper_headers > 0) else 0
        
        return min(quality_ratio + variety_bonus, 1.0)
    
    def analyze_readability(self, markdown_content: str) -> float:
        """Analyze readability of the converted content"""
        # Remove markdown formatting for readability analysis
        clean_text = re.sub(r'[#*\-\[\]()_`]', '', markdown_content)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        if not clean_text:
            return 0.0
        
        # Basic readability metrics
        words = len(re.findall(r'\b\w+\b', clean_text))
        sentences = len(re.findall(r'[.!?]+', clean_text))
        
        if sentences == 0:
            return 0.3  # Some content but no clear sentence structure
        
        avg_words_per_sentence = words / sentences
        
        # Readability scoring based on sentence length
        if 5 <= avg_words_per_sentence <= 20:
            sentence_score = 1.0
        elif 20 < avg_words_per_sentence <= 30:
            sentence_score = 0.8
        elif avg_words_per_sentence > 30:
            sentence_score = 0.6
        else:
            sentence_score = 0.7
        
        # Check for text flow indicators
        has_transitions = bool(re.search(r'\b(however|therefore|furthermore|moreover|additionally)\b', clean_text, re.IGNORECASE))
        has_varied_punctuation = bool(re.search(r'[;:]', clean_text))
        
        flow_bonus = 0.1 if (has_transitions or has_varied_punctuation) else 0
        
        return min(sentence_score + flow_bonus, 1.0)
    
    def generate_recommendations(self, metrics: Dict) -> List[str]:
        """Generate recommendations based on quality analysis"""
        recommendations = []
        
        if metrics['structure_score'] < 0.6:
            recommendations.append("Improve document structure by ensuring proper headers and consistent formatting")
        
        if metrics['content_richness_score'] < 0.6:
            recommendations.append("Content richness is low - verify all sections and details were captured")
        
        if metrics['formatting_score'] < 0.7:
            recommendations.append("Markdown formatting needs improvement - check for proper syntax usage")
        
        if metrics['readability_score'] < 0.7:
            recommendations.append("Readability could be improved - check sentence structure and flow")
        
        if metrics['overall_quality_score'] > 0.85:
            recommendations.append("Excellent conversion quality! Document is well-structured and readable.")
        elif metrics['overall_quality_score'] > 0.7:
            recommendations.append("Good conversion quality with some room for improvement.")
        else:
            recommendations.append("Conversion quality needs attention - consider reviewing extraction and formatting processes.")
        
        return recommendations
    
    def analyze_quality(self, markdown_path: str, pdf_pages_hint: int = None) -> QualityMetrics:
        """Main quality analysis function"""
        print(f"Analyzing markdown quality: {markdown_path}")
        
        # Read markdown content
        try:
            with open(markdown_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
        except Exception as e:
            raise Exception(f"Error reading markdown file: {e}")
        
        print("Analyzing document structure...")
        structure_score = self.analyze_structure(markdown_content)
        
        print("Analyzing content richness...")
        content_richness_score = self.analyze_content_richness(markdown_content)
        
        print("Analyzing formatting quality...")
        formatting_score = self.analyze_formatting_quality(markdown_content)
        
        print("Analyzing readability...")
        readability_score = self.analyze_readability(markdown_content)
        
        # Calculate overall quality score (weighted average)
        overall_quality_score = (
            structure_score * 0.3 +
            content_richness_score * 0.25 +
            formatting_score * 0.25 +
            readability_score * 0.2
        )
        
        # Additional metrics
        word_count = len(re.findall(r'\b\w+\b', markdown_content))
        
        # Estimate pages processed (if not provided)
        if pdf_pages_hint is None:
            # Rough estimate: 250-300 words per page
            estimated_pages = max(word_count // 275, 1)
        else:
            estimated_pages = pdf_pages_hint
        
        # Prepare metrics
        metrics_dict = {
            'overall_quality_score': overall_quality_score,
            'structure_score': structure_score,
            'content_richness_score': content_richness_score,
            'formatting_score': formatting_score,
            'readability_score': readability_score
        }
        
        recommendations = self.generate_recommendations(metrics_dict)
        
        return QualityMetrics(
            overall_quality_score=overall_quality_score,
            structure_score=structure_score,
            content_richness_score=content_richness_score,
            formatting_score=formatting_score,
            readability_score=readability_score,
            total_pages_processed=estimated_pages,
            word_count=word_count,
            recommendations=recommendations
        )
    
    def generate_report(self, metrics: QualityMetrics, output_path: Optional[str] = None) -> str:
        """Generate a detailed quality report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# PDF-to-Markdown Quality Analysis Report
Generated: {timestamp}

## Overall Results
- **Overall Quality Score**: {metrics.overall_quality_score:.2%}
- **Structure Score**: {metrics.structure_score:.2%}
- **Content Richness Score**: {metrics.content_richness_score:.2%}
- **Formatting Score**: {metrics.formatting_score:.2%}
- **Readability Score**: {metrics.readability_score:.2%}

## Grade
"""
        
        # Add grade based on overall quality
        if metrics.overall_quality_score >= 0.9:
            report += "🟢 **Excellent** (90%+)\n"
        elif metrics.overall_quality_score >= 0.8:
            report += "🟢 **Very Good** (80-89%)\n"
        elif metrics.overall_quality_score >= 0.7:
            report += "🟡 **Good** (70-79%)\n"
        elif metrics.overall_quality_score >= 0.6:
            report += "🟠 **Fair** (60-69%)\n"
        else:
            report += "🔴 **Needs Improvement** (<60%)\n"
        
        report += f"""
## Document Statistics
- **Estimated Pages Processed**: {metrics.total_pages_processed}
- **Total Word Count**: {metrics.word_count:,}
- **Average Words Per Page**: {metrics.word_count // max(metrics.total_pages_processed, 1):,}

## Detailed Analysis

### Document Structure ({metrics.structure_score:.2%})
Evaluates the presence and quality of headers, lists, and other structural elements.

### Content Richness ({metrics.content_richness_score:.2%})
Measures the completeness and variety of content captured in the conversion.

### Formatting Quality ({metrics.formatting_score:.2%})
Assesses the proper use of Markdown syntax and formatting consistency.

### Readability ({metrics.readability_score:.2%})
Analyzes sentence structure, flow, and overall text readability.

## Recommendations
"""
        
        for i, rec in enumerate(metrics.recommendations, 1):
            report += f"{i}. {rec}\n"
        
        report += f"""
## Technical Details
- Analysis Method: Markdown content quality assessment
- Focus Areas: Structure, Content, Formatting, Readability
- Word-based metrics for comprehensive evaluation
"""
        
        # Save report if output path provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Quality analysis report saved to: {output_path}")
        
        return report

def main():
    """Main function for command-line usage"""
    print("PDF-to-Markdown Quality Analyzer")
    print("-" * 40)
    
    if len(sys.argv) < 2:
        print("Usage: python pdf_markdown_quality_analyzer.py <markdown_file> [output_report] [estimated_pages]")
        print("\nExample:")
        print('python pdf_markdown_quality_analyzer.py "document.md" "quality_report.md" 25')
        sys.exit(1)
    
    markdown_path = sys.argv[1]
    output_report = sys.argv[2] if len(sys.argv) > 2 else None
    estimated_pages = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    # Validate file path
    if not os.path.exists(markdown_path):
        print(f"Error: Markdown file not found: {markdown_path}")
        sys.exit(1)
    
    try:
        # Create analyzer
        analyzer = PDFMarkdownQualityAnalyzer()
        
        # Run analysis
        metrics = analyzer.analyze_quality(markdown_path, estimated_pages)
        
        # Generate and display report
        report = analyzer.generate_report(metrics, output_report)
        
        print("\n" + "="*60)
        print("QUALITY ANALYSIS RESULTS")
        print("="*60)
        print(f"Overall Quality Score: {metrics.overall_quality_score:.2%}")
        print(f"Structure Score: {metrics.structure_score:.2%}")
        print(f"Content Richness: {metrics.content_richness_score:.2%}")
        print(f"Formatting Quality: {metrics.formatting_score:.2%}")
        print(f"Readability Score: {metrics.readability_score:.2%}")
        print(f"\nWord Count: {metrics.word_count:,}")
        print(f"Estimated Pages: {metrics.total_pages_processed}")
        print("\nRecommendations:")
        for i, rec in enumerate(metrics.recommendations, 1):
            print(f"  {i}. {rec}")
        
        if output_report:
            print(f"\nDetailed report saved to: {output_report}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
import os
import sys
import re
import PyPDF2
import io
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import difflib
import statistics

# Try to import alternative PDF libraries
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import pymupdf  # fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    try:
        import fitz
        PYMUPDF_AVAILABLE = True
    except ImportError:
        PYMUPDF_AVAILABLE = False

# Try to import sentence transformers for semantic similarity
SEMANTIC_ANALYSIS_AVAILABLE = False
try:
    from sentence_transformers import SentenceTransformer
    SEMANTIC_ANALYSIS_AVAILABLE = True
except ImportError:
    pass

@dataclass
class ValidationMetrics:
    """Container for validation results"""
    overall_accuracy: float
    text_completeness: float
    structure_preservation: float
    semantic_similarity: float
    chunk_details: List[Dict]
    recommendations: List[str]

class PDFAccuracyValidator:
    """Validates accuracy of PDF-to-Markdown conversion"""
    
    def __init__(self):
        self.semantic_model = None
        if SEMANTIC_ANALYSIS_AVAILABLE:
            try:
                # Load a lightweight sentence transformer model
                self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("Semantic analysis enabled with SentenceTransformer")
            except Exception as e:
                print(f"Warning: Could not load semantic model: {e}")
                self.semantic_model = None
    
    def extract_text_from_pdf(self, pdf_path: str) -> Tuple[str, List[str]]:
        """Extract raw text from PDF for comparison using multiple methods"""
        full_text = ""
        pages = []
        
        # Try multiple extraction methods in order of preference
        methods = []
        
        if PDFPLUMBER_AVAILABLE:
            methods.append(("pdfplumber", self._extract_with_pdfplumber))
        if PYMUPDF_AVAILABLE:
            methods.append(("PyMuPDF", self._extract_with_pymupdf))
        methods.append(("PyPDF2", self._extract_with_pypdf2))
        
        for method_name, method_func in methods:
            try:
                print(f"Trying text extraction with {method_name}...")
                full_text, pages = method_func(pdf_path)
                if len(full_text.strip()) > 100:  # If we got reasonable text
                    print(f"Successfully extracted text using {method_name}")
                    break
                else:
                    print(f"{method_name} extracted minimal text, trying next method...")
            except Exception as e:
                print(f"Error with {method_name}: {e}")
                continue
        
        if not full_text.strip():
            raise Exception("Could not extract text from PDF using any available method")
            
        return full_text.strip(), pages
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> Tuple[str, List[str]]:
        """Extract text using pdfplumber"""
        full_text = ""
        pages = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                pages.append(page_text)
                full_text += page_text + "\n"
                
        return full_text.strip(), pages
    
    def _extract_with_pymupdf(self, pdf_path: str) -> Tuple[str, List[str]]:
        """Extract text using PyMuPDF (fitz)"""
        import fitz
        full_text = ""
        pages = []
        
        doc = fitz.open(pdf_path)
        for page_num in range(doc.page_count):
            page = doc[page_num]
            page_text = page.get_text()
            pages.append(page_text)
            full_text += page_text + "\n"
        doc.close()
                
        return full_text.strip(), pages
    
    def _extract_with_pypdf2(self, pdf_path: str) -> Tuple[str, List[str]]:
        """Extract text using PyPDF2"""
        full_text = ""
        pages = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                pages.append(page_text)
                full_text += page_text + "\n"
                
        return full_text.strip(), pages
    
    def clean_text_for_comparison(self, text: str) -> str:
        """Normalize text for comparison"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove common PDF artifacts
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)
        # Convert to lowercase for comparison
        return text.lower().strip()
    
    def extract_markdown_content(self, markdown_path: str) -> str:
        """Extract content from markdown file"""
        try:
            with open(markdown_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Remove markdown formatting for text comparison
            # Remove headers
            content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
            # Remove bold/italic
            content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
            content = re.sub(r'\*([^*]+)\*', r'\1', content)
            # Remove links but keep text
            content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
            # Remove horizontal rules
            content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)
            
            return content
        except Exception as e:
            raise Exception(f"Error reading markdown file: {e}")
    
    def analyze_structure_preservation(self, pdf_text: str, markdown_content: str) -> float:
        """Analyze how well document structure was preserved"""
        # Count structural elements in markdown
        markdown_headers = len(re.findall(r'^#+\s+', markdown_content, re.MULTILINE))
        markdown_lists = len(re.findall(r'^\s*[-*+]\s+', markdown_content, re.MULTILINE))
        markdown_numbered_lists = len(re.findall(r'^\s*\d+\.\s+', markdown_content, re.MULTILINE))
        
        # Simple heuristic: if we have reasonable structure elements, score higher
        structure_elements = markdown_headers + markdown_lists + markdown_numbered_lists
        
        # Normalize based on content length (rough heuristic)
        content_length = len(markdown_content)
        if content_length > 1000:
            expected_elements = content_length // 500  # Rough expectation
            structure_score = min(structure_elements / max(expected_elements, 1), 1.0)
        else:
            structure_score = 0.8 if structure_elements > 0 else 0.5
            
        return structure_score
    
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using difflib"""
        # Clean both texts
        clean_text1 = self.clean_text_for_comparison(text1)
        clean_text2 = self.clean_text_for_comparison(text2)
        
        # Use sequence matcher for similarity
        matcher = difflib.SequenceMatcher(None, clean_text1, clean_text2)
        return matcher.ratio()
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity using sentence transformers"""
        if not self.semantic_model:
            return 0.0  # Fallback if no semantic model available
            
        try:
            # Split into sentences for better comparison
            sentences1 = [s.strip() for s in re.split(r'[.!?]+', text1) if s.strip()]
            sentences2 = [s.strip() for s in re.split(r'[.!?]+', text2) if s.strip()]
            
            if not sentences1 or not sentences2:
                return 0.0
            
            # Take sample if too many sentences (for performance)
            max_sentences = 20
            if len(sentences1) > max_sentences:
                sentences1 = sentences1[:max_sentences]
            if len(sentences2) > max_sentences:
                sentences2 = sentences2[:max_sentences]
            
            # Get embeddings
            embeddings1 = self.semantic_model.encode(sentences1)
            embeddings2 = self.semantic_model.encode(sentences2)
            
            # Calculate average similarity
            similarities = []
            for emb1 in embeddings1:
                best_sim = 0
                for emb2 in embeddings2:
                    sim = float(emb1 @ emb2.T)  # Cosine similarity
                    if sim > best_sim:
                        best_sim = sim
                similarities.append(best_sim)
            
            return statistics.mean(similarities) if similarities else 0.0
            
        except Exception as e:
            print(f"Warning: Semantic similarity calculation failed: {e}")
            return 0.0
    
    def generate_recommendations(self, metrics: Dict) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        if metrics['text_completeness'] < 0.8:
            recommendations.append("Text completeness is low - check for missing content or text extraction issues")
        
        if metrics['structure_preservation'] < 0.7:
            recommendations.append("Structure preservation could be improved - consider better header and list detection")
        
        if metrics['semantic_similarity'] < 0.7 and SEMANTIC_ANALYSIS_AVAILABLE:
            recommendations.append("Semantic similarity is low - content meaning may not be fully preserved")
        
        if metrics['overall_accuracy'] > 0.9:
            recommendations.append("Excellent conversion quality!")
        elif metrics['overall_accuracy'] > 0.8:
            recommendations.append("Good conversion quality with minor improvements possible")
        else:
            recommendations.append("Conversion quality needs improvement - review extraction and formatting logic")
        
        return recommendations
    
    def validate_conversion(self, pdf_path: str, markdown_path: str) -> ValidationMetrics:
        """Main validation function"""
        print(f"Starting validation of:")
        print(f"  PDF: {pdf_path}")
        print(f"  Markdown: {markdown_path}")
        
        # Extract texts
        print("Extracting PDF text...")
        pdf_full_text, pdf_pages = self.extract_text_from_pdf(pdf_path)
        
        print("Reading markdown content...")
        with open(markdown_path, 'r', encoding='utf-8') as f:
            markdown_raw = f.read()
        markdown_clean = self.extract_markdown_content(markdown_path)
        
        print("Analyzing conversion accuracy...")
        
        # Debug info
        print(f"PDF text length: {len(pdf_full_text)} characters")
        print(f"Markdown text length: {len(markdown_clean)} characters")
        print(f"PDF preview: {pdf_full_text[:200]}..." if pdf_full_text else "No PDF text extracted")
        print(f"Markdown preview: {markdown_clean[:200]}..." if markdown_clean else "No markdown text")
        
        # Calculate metrics
        text_similarity = self.calculate_text_similarity(pdf_full_text, markdown_clean)
        structure_score = self.analyze_structure_preservation(pdf_full_text, markdown_raw)
        
        semantic_similarity = 0.0
        if SEMANTIC_ANALYSIS_AVAILABLE and self.semantic_model:
            print("Calculating semantic similarity...")
            semantic_similarity = self.calculate_semantic_similarity(pdf_full_text, markdown_clean)
        
        # Calculate overall accuracy (weighted average)
        if SEMANTIC_ANALYSIS_AVAILABLE and semantic_similarity > 0:
            overall_accuracy = (
                text_similarity * 0.4 + 
                structure_score * 0.3 + 
                semantic_similarity * 0.3
            )
        else:
            overall_accuracy = (
                text_similarity * 0.6 + 
                structure_score * 0.4
            )
        
        # Prepare metrics
        metrics_dict = {
            'overall_accuracy': overall_accuracy,
            'text_completeness': text_similarity,
            'structure_preservation': structure_score,
            'semantic_similarity': semantic_similarity
        }
        
        # Generate chunk details (simplified for now)
        chunk_details = [{
            'chunk_number': 1,
            'pages': f"1-{len(pdf_pages)}",
            'accuracy': overall_accuracy,
            'notes': f"Full document analysis with {len(pdf_pages)} pages"
        }]
        
        recommendations = self.generate_recommendations(metrics_dict)
        
        return ValidationMetrics(
            overall_accuracy=overall_accuracy,
            text_completeness=text_similarity,
            structure_preservation=structure_score,
            semantic_similarity=semantic_similarity,
            chunk_details=chunk_details,
            recommendations=recommendations
        )
    
    def generate_report(self, metrics: ValidationMetrics, output_path: Optional[str] = None) -> str:
        """Generate a detailed validation report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# PDF-to-Markdown Validation Report
Generated: {timestamp}

## Overall Results
- **Overall Accuracy**: {metrics.overall_accuracy:.2%}
- **Text Completeness**: {metrics.text_completeness:.2%}
- **Structure Preservation**: {metrics.structure_preservation:.2%}
- **Semantic Similarity**: {metrics.semantic_similarity:.2%}

## Grade
"""
        
        # Add grade based on overall accuracy
        if metrics.overall_accuracy >= 0.9:
            report += "🟢 **Excellent** (90%+)\n"
        elif metrics.overall_accuracy >= 0.8:
            report += "🟡 **Good** (80-89%)\n"
        elif metrics.overall_accuracy >= 0.7:
            report += "🟠 **Fair** (70-79%)\n"
        else:
            report += "🔴 **Needs Improvement** (<70%)\n"
        
        report += f"""
## Detailed Analysis

### Text Completeness ({metrics.text_completeness:.2%})
Measures how much of the original PDF text was captured in the markdown conversion.

### Structure Preservation ({metrics.structure_preservation:.2%})
Evaluates how well document structure (headers, lists, formatting) was maintained.

### Semantic Similarity ({metrics.semantic_similarity:.2%})
"""
        
        if SEMANTIC_ANALYSIS_AVAILABLE and metrics.semantic_similarity > 0:
            report += "Analyzes how well the meaning and context of the content was preserved.\n"
        else:
            report += "Not available - install sentence-transformers for semantic analysis.\n"
        
        report += f"""
## Chunk Details
"""
        
        for chunk in metrics.chunk_details:
            report += f"""
### Chunk {chunk['chunk_number']} (Pages {chunk['pages']})
- **Accuracy**: {chunk['accuracy']:.2%}
- **Notes**: {chunk['notes']}
"""
        
        report += f"""
## Recommendations
"""
        for i, rec in enumerate(metrics.recommendations, 1):
            report += f"{i}. {rec}\n"
        
        report += f"""
## Technical Details
- Semantic Analysis Available: {SEMANTIC_ANALYSIS_AVAILABLE}
- PDF Text Extraction: PyPDF2
- Text Similarity: difflib.SequenceMatcher
- Structure Analysis: Regex pattern matching
"""
        
        # Save report if output path provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Validation report saved to: {output_path}")
        
        return report

def main():
    """Main function for command-line usage"""
    print("PDF-to-Markdown Accuracy Validator")
    print("-" * 40)
    
    if len(sys.argv) < 3:
        print("Usage: python pdf_accuracy_validator.py <pdf_file> <markdown_file> [output_report]")
        print("\nExample:")
        print('python pdf_accuracy_validator.py "document.pdf" "document.md" "validation_report.md"')
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    markdown_path = sys.argv[2]
    output_report = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Validate file paths
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    if not os.path.exists(markdown_path):
        print(f"Error: Markdown file not found: {markdown_path}")
        sys.exit(1)
    
    try:
        # Create validator
        validator = PDFAccuracyValidator()
        
        # Run validation
        metrics = validator.validate_conversion(pdf_path, markdown_path)
        
        # Generate and display report
        report = validator.generate_report(metrics, output_report)
        
        print("\n" + "="*60)
        print("VALIDATION RESULTS")
        print("="*60)
        print(f"Overall Accuracy: {metrics.overall_accuracy:.2%}")
        print(f"Text Completeness: {metrics.text_completeness:.2%}")
        print(f"Structure Preservation: {metrics.structure_preservation:.2%}")
        print(f"Semantic Similarity: {metrics.semantic_similarity:.2%}")
        print("\nRecommendations:")
        for i, rec in enumerate(metrics.recommendations, 1):
            print(f"  {i}. {rec}")
        
        if output_report:
            print(f"\nDetailed report saved to: {output_report}")
        
    except Exception as e:
        print(f"Error during validation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
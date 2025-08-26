# PDF-to-Markdown Converter

Professional PDF-to-Markdown conversion tool with comprehensive validation and fidelity analysis.

## Overview

This project provides a complete solution for converting PDF documents to high-quality Markdown format, with built-in validation to ensure content fidelity. Designed for business users who need reliable document conversion with measurable quality assurance.

## Key Features

### 🔄 PDF Conversion
- **Claude AI Integration**: Leverages Claude Sonnet for intelligent document conversion
- **Chunked Processing**: Handles large documents by processing in 5-page segments
- **Batch Processing**: Convert multiple PDFs with simple batch files
- **Image-Based PDF Support**: OCR extraction for scanned documents

### 🔍 Validation System
- **Word-for-Word Fidelity**: Measures preservation of source content (currently achieving 90.6%)
- **Grammar Structure Analysis**: Validates sentence boundaries and paragraph structure *(planned)*
- **Document Formatting**: Ensures proper headers, bullets, and tables *(planned)*
- **Foundation-First Approach**: Incremental validation with clear quality gates

### 📊 Quality Assurance
- **Comprehensive Reporting**: Detailed analysis of conversion quality
- **Business-Focused Metrics**: Prioritized validation based on business needs
- **Diagnostic Tools**: PDF structure analysis and OCR capabilities testing

## Quick Start

### Prerequisites
```bash
pip install PyPDF2 pdfplumber PyMuPDF easyocr anthropic
```

### Basic Usage

**1. Convert a PDF to Markdown:**
```bash
# Set your Claude API key
set ANTHROPIC_API_KEY=your_key_here

# Convert PDF
python pdf_to_markdown_sonnet.py "path/to/your/document.pdf"
```

**2. Validate conversion quality:**
```bash
# Run complete validation
python pdf_validation_system.py
```

**3. Use batch processing:**
```bash
# Windows
convert_pdf_sonnet.bat "path/to/your/document.pdf"

# Validation
run_full_validation.bat
```

## Project Structure

```
pdf-to-markdown-converter/
├── conversion/
│   ├── pdf_to_markdown_sonnet.py    # Core conversion script
│   └── convert_pdf_sonnet.bat       # Batch conversion wrapper
├── validation/
│   ├── pdf_validation_system.py     # Complete validation workflow
│   ├── word_fidelity_validator.py   # Word-level fidelity analysis
│   ├── full_scope_ocr_extractor.py  # OCR text extraction
│   └── run_full_validation.bat      # Validation batch script
├── utilities/
│   ├── pdf_structure_analyzer.py    # PDF diagnostic tool
│   ├── pdf_text_diagnostic.py       # Text extraction testing
│   └── test_comparison_engine.py    # Validation system testing
├── checkpoints/                     # Project progress tracking
└── docs/                           # Documentation
```

## Validation System

### Priority-Based Validation
Our validation system measures three key areas in order of business priority:

1. **Word-for-Word Fidelity (90.6% achieved)** 
   - Measures preservation of source content
   - Identifies missing or altered words
   - Current target: >90% (achieved)

2. **Grammar & Sentence Structure** *(in development)*
   - Validates sentence boundaries and paragraph structure
   - Target: >80% structure preservation

3. **Document Formatting** *(planned)*
   - Ensures proper headers, bullets, tables
   - Target: >85% formatting preservation

### Foundation-First Approach
- Each validation component is built and tested independently
- Clear quality gates prevent building on flawed foundations
- Incremental development with business outcome focus

## Technical Details

### Conversion Process
1. **PDF Analysis**: Determines if PDF is text-based or image-based
2. **Content Extraction**: Direct text extraction or OCR processing
3. **AI Processing**: Claude Sonnet converts content to Markdown
4. **Chunking Strategy**: Large documents processed in 5-page segments
5. **Quality Validation**: Multi-level fidelity analysis

### OCR Integration
- **EasyOCR**: Primary OCR engine for image-based PDFs
- **Local Processing**: No cloud dependencies for basic functionality
- **High Resolution**: 2x scaling for improved text recognition
- **Performance**: ~30 seconds per page (CPU processing)

## Current Limitations

- **OCR Speed**: CPU-only processing (cloud OCR enhancement planned)
- **Grammar Validation**: In development
- **Formatting Validation**: Planned for next release
- **Word Fidelity**: 90.6% (investigating 9.4% gap)

## Planned Enhancements

See our [GitHub Issues](../../issues) for detailed roadmap:
- [ ] Grammar and sentence structure validation
- [ ] Document formatting fidelity analysis
- [ ] Word fidelity improvement (target: >95%)
- [ ] Cloud OCR integration for performance
- [ ] Web interface for non-technical users

## Development Workflow

This project uses a foundation-first development approach:
1. **Incremental Validation**: Each component tested independently
2. **Business Outcome Focus**: Work aligned to clear business priorities
3. **Quality Gates**: Clear success criteria before advancing
4. **GitHub Integration**: Issues, project boards, and milestone tracking

## Contributing

1. Check [GitHub Issues](../../issues) for current priorities
2. Follow the foundation-first approach
3. Ensure validation tests pass before submitting
4. Update relevant documentation

## Business Value

This tool addresses the critical need for reliable PDF-to-Markdown conversion in business environments where document fidelity is essential. The validation system provides measurable quality assurance, ensuring converted documents maintain their professional integrity and content accuracy.

Perfect for:
- **Business Documentation**: Converting reports, proposals, and presentations
- **Content Migration**: Moving PDF libraries to Markdown-based systems
- **Quality Assurance**: Validating conversion accuracy for critical documents

## License

MIT License - see [LICENSE](LICENSE) file for details.

This project is open source and welcomes contributions from the community. The MIT License allows free use, modification, and distribution while requiring only attribution to the original author.

**Why Open Source?**
This project demonstrates practical coding skills development by a business user learning efficient development practices. By sharing this work publicly, we hope to:
- Help other business users learn practical coding approaches
- Encourage foundation-first development methodologies  
- Showcase real-world document conversion challenges and solutions
- Build a community around reliable PDF-to-Markdown conversion tools

**Contributing**: We welcome contributions from developers and business users alike. Check our [Issues](../../issues) for current priorities and enhancement opportunities.

---

**Need Help?** Check our [Issues](../../issues) or [Project Board](../../projects) for current development status and support.

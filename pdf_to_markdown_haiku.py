import os
import sys
import base64
from pathlib import Path
import anthropic
from typing import Optional
import PyPDF2
import io
from datetime import datetime

def split_pdf(pdf_path: str, pages_per_chunk: int = 5):
    """Split a PDF into smaller chunks."""
    chunks = []
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        for start_page in range(0, total_pages, pages_per_chunk):
            pdf_writer = PyPDF2.PdfWriter()
            end_page = min(start_page + pages_per_chunk, total_pages)
            
            for page_num in range(start_page, end_page):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            
            # Write to bytes
            output_stream = io.BytesIO()
            pdf_writer.write(output_stream)
            output_stream.seek(0)
            chunks.append({
                'data': output_stream.read(),
                'start_page': start_page + 1,
                'end_page': end_page,
                'total_pages': total_pages
            })
    
    return chunks

def convert_pdf_chunk_to_markdown(pdf_data: bytes, api_key: str, chunk_info: dict) -> str:
    """Convert a PDF chunk to Markdown using Anthropic's Claude Haiku model."""
    
    # Initialize the Anthropic client
    client = anthropic.Anthropic(api_key=api_key)
    
    # Encode PDF to base64
    pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
    
    # Create the message for Claude Haiku
    message = client.messages.create(
        model="claude-3-5-haiku-latest",  # Using latest Haiku model
        max_tokens=8192,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": f"Convert this PDF excerpt (pages {chunk_info['start_page']}-{chunk_info['end_page']} of {chunk_info['total_pages']}) to complete, well-formatted Markdown. \n\nIMPORTANT: Extract ALL text content from every page - do not skip any paragraphs, sentences, or sections. Include every piece of body text, headings, subheadings, quotes, lists, and captions. \n\nYou may streamline the formatting by:\n- Simplifying complex layouts to clean Markdown\n- Removing excessive whitespace or decorative elements\n- Using standard Markdown headers (# ## ###) consistently\n\nBut you MUST preserve:\n- Every word of actual content\n- All headings and subheadings\n- All body paragraphs and text blocks\n- All quotes, lists, and important text\n- Document structure and flow\n\nDo not summarize, condense, or skip any text content. The goal is complete content extraction with clean formatting. Do not add any introductory text about this being a partial document."
                    }
                ]
            }
        ]
    )
    
    return message.content[0].text

def convert_pdf_to_markdown_haiku(pdf_path: str, api_key: Optional[str] = None, pages_per_chunk: int = 5) -> str:
    """
    Convert a large PDF document to Markdown using Claude Haiku (faster and cheaper).
    
    Args:
        pdf_path: Path to the PDF file
        api_key: Anthropic API key (optional, can use environment variable)
        pages_per_chunk: Number of pages to process at once (default 5 for Haiku)
    
    Returns:
        Markdown formatted text from the PDF
    """
    
    # Get API key from parameter or environment variable
    if api_key is None:
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError(
                "No API key provided. Either pass it as a parameter or set the ANTHROPIC_API_KEY environment variable."
            )
    
    # Check if PDF exists
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    print(f"Splitting PDF into chunks of {pages_per_chunk} pages...")
    chunks = split_pdf(pdf_path, pages_per_chunk)
    
    markdown_parts = []
    
    for i, chunk in enumerate(chunks, 1):
        print(f"Converting chunk {i}/{len(chunks)} (pages {chunk['start_page']}-{chunk['end_page']})...")
        try:
            markdown_text = convert_pdf_chunk_to_markdown(chunk['data'], api_key, chunk)
            markdown_parts.append(markdown_text)
            print(f"  [OK] Chunk {i} converted successfully")
        except Exception as e:
            print(f"  [ERROR] Failed to convert chunk {i}: {e}")
            markdown_parts.append(f"\n\n---\n\n**[Error converting pages {chunk['start_page']}-{chunk['end_page']}]**\n\n---\n\n")
    
    # Combine all parts with page breaks
    full_markdown = "\n\n---\n\n".join(markdown_parts)
    return full_markdown

def main():
    """Main function to handle command-line usage."""
    
    print("PDF to Markdown Converter (Haiku - Fast Mode) using Anthropic API")
    print("-" * 66)
    print("[INFO] Using Claude 3.5 Haiku for faster, more economical conversion")
    print("-" * 66)
    
    # Check if PDF path was provided as command-line argument
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1].strip()
        print(f"Using PDF file: {pdf_path}")
    else:
        # Get PDF path from user
        pdf_path = input("Enter the path to your PDF file: ").strip()
    
    # Optional: pages per chunk (default 5 for consistency)
    pages_per_chunk = 5
    if len(sys.argv) > 2:
        try:
            pages_per_chunk = int(sys.argv[2])
            print(f"Using {pages_per_chunk} pages per chunk")
        except ValueError:
            print("Invalid pages per chunk, using default of 5")
    
    # Check for API key in environment or prompt for it
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("\nNo ANTHROPIC_API_KEY found in environment variables.")
        api_key = input("Enter your Anthropic API key: ").strip()
    
    try:
        print("\nConverting PDF to Markdown...")
        markdown_content = convert_pdf_to_markdown_haiku(pdf_path, api_key, pages_per_chunk)
        
        # Save the output with _haiku suffix and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = Path(pdf_path).stem
        output_filename = f"{base_name}_haiku_{timestamp}.md"
        output_path = Path(pdf_path).parent / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"\n[OK] Conversion successful!")
        print(f"[OK] Markdown saved to: {output_path}")
        print(f"[OK] Total length: {len(markdown_content)} characters")
        print(f"[INFO] Used Haiku model for ~10x faster and cheaper conversion")
        
    except FileNotFoundError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
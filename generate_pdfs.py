#!/usr/bin/env python3
"""
DealScout Report PDF Generator
Converts markdown reports to professional PDFs with branding and styling.
"""

import subprocess
import sys
from pathlib import Path

def markdown_to_html(md_content, title):
    """Convert markdown to HTML with DealScout branding and styling."""
    
    # CSS for professional report styling
    css = """
    <style>
        @page {
            size: A4;
            margin: 2cm 2cm 3cm 2cm;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 210mm;
            margin: 0 auto;
            background: white;
            font-size: 11pt;
        }
        
        /* Header/Branding */
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            margin: -2cm -2cm 30px -2cm;
            text-align: center;
        }
        
        .header h1 {
            margin: 0;
            font-size: 28pt;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        .header .tagline {
            font-size: 12pt;
            opacity: 0.9;
            margin-top: 5px;
        }
        
        /* Main content */
        h1 {
            color: #667eea;
            font-size: 24pt;
            margin-top: 30px;
            margin-bottom: 15px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }
        
        h2 {
            color: #764ba2;
            font-size: 18pt;
            margin-top: 25px;
            margin-bottom: 12px;
            border-left: 4px solid #667eea;
            padding-left: 12px;
        }
        
        h3 {
            color: #555;
            font-size: 14pt;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        h4 {
            color: #666;
            font-size: 12pt;
            margin-top: 15px;
            margin-bottom: 8px;
        }
        
        /* Links and verification */
        a {
            color: #667eea;
            text-decoration: none;
            border-bottom: 1px dotted #667eea;
        }
        
        a:hover {
            border-bottom: 1px solid #667eea;
        }
        
        /* Verification badges */
        a[href*="Verify"]:before,
        a[title*="Verify"]:before {
            content: "📎 ";
        }
        
        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 10pt;
        }
        
        th {
            background: #f0f0f0;
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
            font-weight: 600;
        }
        
        td {
            padding: 8px 10px;
            border: 1px solid #ddd;
        }
        
        tr:nth-child(even) {
            background: #f9f9f9;
        }
        
        /* Blockquotes */
        blockquote {
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin-left: 0;
            color: #555;
            font-style: italic;
        }
        
        /* Code blocks */
        code {
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 10pt;
            font-family: 'Courier New', monospace;
        }
        
        pre {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 9pt;
        }
        
        pre code {
            background: none;
            padding: 0;
        }
        
        /* Lists */
        ul, ol {
            margin: 15px 0;
            padding-left: 25px;
        }
        
        li {
            margin: 8px 0;
        }
        
        /* Emoji indicators */
        .emoji {
            font-size: 14pt;
            margin-right: 5px;
        }
        
        /* Horizontal rules */
        hr {
            border: none;
            border-top: 2px solid #e0e0e0;
            margin: 30px 0;
        }
        
        /* Strong emphasis */
        strong {
            color: #222;
            font-weight: 600;
        }
        
        /* Warning/info boxes */
        p:has(> strong:first-child:contains("Red Flag")),
        p:has(> strong:first-child:contains("Quick Verdict")),
        p:has(> strong:first-child:contains("Bottom Line")) {
            background: #fff3cd;
            border-left: 4px solid #ff9800;
            padding: 12px 15px;
            margin: 15px 0;
        }
        
        /* Page breaks for sections */
        .page-break {
            page-break-before: always;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #999;
            font-size: 9pt;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }
    </style>
    """
    
    # Convert markdown to HTML using pandoc
    try:
        result = subprocess.run(
            ['pandoc', '-f', 'markdown', '-t', 'html'],
            input=md_content,
            capture_output=True,
            text=True,
            check=True
        )
        html_body = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error converting markdown to HTML: {e}")
        sys.exit(1)
    
    # Construct full HTML document
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {css}
</head>
<body>
    <div class="header">
        <h1>🎯 DealScout</h1>
        <div class="tagline">Professional Business Intelligence Reports</div>
    </div>
    
    {html_body}
    
    <div class="footer">
        <p>Generated by DealScout | For informational purposes only | Verify all data independently</p>
    </div>
</body>
</html>
"""
    return html


def html_to_pdf(html_content, output_path):
    """Convert HTML to PDF using wkhtmltopdf."""
    
    try:
        result = subprocess.run(
            [
                'wkhtmltopdf',
                '--enable-local-file-access',
                '--encoding', 'UTF-8',
                '--page-size', 'A4',
                '--margin-top', '15mm',
                '--margin-bottom', '20mm',
                '--margin-left', '15mm',
                '--margin-right', '15mm',
                '--print-media-type',
                '--no-stop-slow-scripts',
                '--enable-internal-links',
                '--enable-external-links',
                '--footer-center', '[page] of [toPage]',
                '--footer-font-size', '8',
                '--footer-spacing', '5',
                '-',  # Read from stdin
                str(output_path)
            ],
            input=html_content,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting HTML to PDF: {e}")
        print(f"stderr: {e.stderr}")
        return False


def generate_pdf(md_file, pdf_file):
    """Generate PDF from markdown file."""
    
    print(f"Generating PDF: {pdf_file.name}")
    
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Extract title from filename
    title = md_file.stem.replace('-', ' ').title()
    
    # Convert to HTML
    html_content = markdown_to_html(md_content, title)
    
    # Convert to PDF
    success = html_to_pdf(html_content, pdf_file)
    
    if success:
        print(f"✓ Successfully created: {pdf_file}")
    else:
        print(f"✗ Failed to create: {pdf_file}")
        return False
    
    return True


def main():
    """Main function to generate all report PDFs."""
    
    reports_dir = Path('/root/openclaw-workspace/tracks/dealscout/sample-reports')
    
    reports = [
        'report-1-stinkin-crawfish-inglewood.md',
        'report-2-35w-auto-repair-mounds-view.md',
        'report-3-woof-gang-mueller-austin.md'
    ]
    
    print("=" * 60)
    print("DealScout PDF Generator")
    print("=" * 60)
    print()
    
    success_count = 0
    
    for report_file in reports:
        md_path = reports_dir / report_file
        pdf_path = reports_dir / report_file.replace('.md', '.pdf')
        
        if not md_path.exists():
            print(f"⚠ Warning: {report_file} not found, skipping...")
            continue
        
        if generate_pdf(md_path, pdf_path):
            success_count += 1
        
        print()
    
    print("=" * 60)
    print(f"Completed: {success_count}/{len(reports)} PDFs generated successfully")
    print("=" * 60)
    
    return success_count == len(reports)


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

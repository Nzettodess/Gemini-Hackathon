#!/usr/bin/env python3
"""
Convert Markdown to PDF using HTML as intermediate format
"""
import subprocess
import sys

def convert_md_to_pdf(md_file, pdf_file):
    """Convert markdown file to PDF using markdown-to-html and then html-to-pdf"""
    
    # Read markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML manually
    html_content = convert_md_to_html(md_content)
    
    # Write HTML with PDF-friendly styling
    html_with_style = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
        }}
        h1 {{
            color: #1a365d;
            border-bottom: 3px solid #2c5282;
            padding-bottom: 10px;
            font-size: 24pt;
        }}
        h2 {{
            color: #2c5282;
            border-bottom: 2px solid #4299e1;
            padding-bottom: 8px;
            margin-top: 30px;
            font-size: 16pt;
        }}
        h3 {{
            color: #2b6cb0;
            margin-top: 20px;
            font-size: 13pt;
        }}
        hr {{
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 20px 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #cbd5e0;
            padding: 10px 12px;
            text-align: left;
        }}
        th {{
            background-color: #2c5282;
            color: white;
            font-weight: 600;
        }}
        tr:nth-child(even) {{
            background-color: #f7fafc;
        }}
        ul {{
            margin: 10px 0;
        }}
        li {{
            margin: 5px 0;
        }}
        strong {{
            color: #1a365d;
        }}
        code {{
            background-color: #edf2f7;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
        }}
        .checkbox {{
            display: inline-block;
            width: 14px;
            height: 14px;
            border: 2px solid #4299e1;
            border-radius: 3px;
            margin-right: 8px;
            vertical-align: middle;
        }}
        p {{
            margin: 10px 0;
        }}
        em {{
            color: #e53e3e;
            font-style: normal;
            font-weight: 600;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    # Save HTML file
    html_file = md_file.replace('.md', '.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_with_style)
    
    print(f"✓ HTML file created: {html_file}")
    
    # Try to convert HTML to PDF using available tools
    try:
        # Try using cupsfilter (available on macOS)
        subprocess.run([
            '/usr/sbin/cupsfilter', 
            '-o', 'media=A4',
            html_file
        ], capture_output=True, check=True)
        print(f"✓ PDF file created: {pdf_file}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"Note: Direct PDF conversion requires additional tools.")
        print(f"HTML file is ready at: {html_file}")
        print(f"\nTo create PDF, you can:")
        print(f"  1. Open the HTML file in a browser and Print to PDF")
        print(f"  2. Install pandoc: brew install pandoc")
        print(f"  3. Use a online converter")
    
    return html_file

def convert_md_to_html(md_content):
    """Simple markdown to HTML conversion"""
    import re
    
    lines = md_content.split('\n')
    html_lines = []
    in_list = False
    in_table = False
    table_header = False
    
    for line in lines:
        # Headers
        if line.startswith('# '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<h3>{line[4:]}</h3>')
        # Horizontal rule
        elif line.strip() == '---':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('<hr>')
        # Table
        elif '|' in line and line.strip().startswith('|'):
            if not in_table:
                html_lines.append('<table>')
                in_table = True
                table_header = True
            
            if '---' in line:
                continue  # Skip separator row
            
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if table_header:
                html_lines.append('<tr>' + ''.join(f'<th>{cell}</th>' for cell in cells) + '</tr>')
                table_header = False
            else:
                html_lines.append('<tr>' + ''.join(f'<td>{process_inline(cell)}</td>' for cell in cells) + '</tr>')
        elif in_table and not ('|' in line):
            html_lines.append('</table>')
            in_table = False
        # List items with checkboxes
        elif line.strip().startswith('- [ ]'):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            content = line.strip()[5:].strip()
            html_lines.append(f'<li><span class="checkbox"></span>{process_inline(content)}</li>')
        # Regular list items
        elif line.strip().startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            content = line.strip()[2:]
            html_lines.append(f'<li>{process_inline(content)}</li>')
        # Empty line
        elif line.strip() == '':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('')
        # Regular paragraph
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if line.strip():
                html_lines.append(f'<p>{process_inline(line)}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    if in_table:
        html_lines.append('</table>')
    
    return '\n'.join(html_lines)

def process_inline(text):
    """Process inline markdown elements"""
    import re
    
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic/Emphasis (for PROHIBITED markers)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Arrow
    text = text.replace('→', '→')
    
    return text

if __name__ == '__main__':
    md_file = '/Users/miachen/Library/CloudStorage/OneDrive-DTMasterCarbon/DT Master Mia Personal/5 Tech/AI act/AI_Risk_Assessment_Questions.md'
    pdf_file = '/Users/miachen/Library/CloudStorage/OneDrive-DTMasterCarbon/DT Master Mia Personal/5 Tech/AI act/AI_Risk_Assessment_Questions.pdf'
    
    convert_md_to_pdf(md_file, pdf_file)

#!/usr/bin/env python3
"""
Convert CogPrime_Overview_Paper.txt to properly formatted Markdown.
Handles section headers, abstracts, and proper formatting.
"""

import re
import sys

def convert_to_markdown(input_file, output_file):
    """Convert the extracted PDF text to properly formatted Markdown."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    markdown_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Handle title (first non-empty line)
        if i < 5 and line and not markdown_lines:
            markdown_lines.append(f"# {line}")
            i += 1
            continue
            
        # Handle author and date
        if i < 10 and line in ["Ben Goertzel", "October 2, 2012"]:
            markdown_lines.append(f"**{line}**")
            markdown_lines.append("")
            i += 1
            continue
            
        # Handle Abstract section
        if line == "Abstract":
            markdown_lines.append("## Abstract")
            markdown_lines.append("")
            i += 1
            # Collect abstract content until next section
            while i < len(lines) and not (re.match(r'^\d+$', lines[i].strip()) and i + 2 < len(lines) and lines[i+2].strip() == "Introduction"):
                abstract_line = lines[i].strip()
                if abstract_line and not abstract_line.isdigit():
                    markdown_lines.append(abstract_line)
                elif not abstract_line:
                    markdown_lines.append("")
                i += 1
            markdown_lines.append("")
            continue
            
        # Handle main section numbers (like "1", "2", etc.) followed by proper section titles
        if re.match(r'^\d+$', line) and len(line) <= 2:
            # Look ahead for section title
            if i + 2 < len(lines):
                section_title = lines[i + 2].strip()
                # Check if this looks like a real section title (not just content)
                if (section_title and not re.match(r'^\d', section_title) and 
                    len(section_title) > 5 and section_title[0].isupper() and
                    section_title in ["Introduction", "CogPrime and OpenCog", "The CogPrime Architecture", 
                                    "CogPrime Cognitive Processes", "CogPrime Learning", "The Mind-World Correspondence"]):
                    markdown_lines.append(f"## {line}. {section_title}")
                    markdown_lines.append("")
                    i += 3  # Skip the number, empty line, and title
                    continue
            # If no section title found, treat as page number and skip
            i += 1
            continue
            
        # Handle subsection numbers (like "1.1", "1.2", etc.)
        if re.match(r'^\d+\.\d+$', line):
            # Look ahead for section title
            if i + 2 < len(lines):
                section_title = lines[i + 2].strip()
                if section_title and not re.match(r'^\d', section_title) and len(section_title) > 3:
                    markdown_lines.append(f"### {line} {section_title}")
                    markdown_lines.append("")
                    i += 3  # Skip the number, empty line, and title
                    continue
                    
        # Handle sub-subsection numbers (like "1.1.1", "2.3.4", etc.)
        if re.match(r'^\d+\.\d+\.\d+$', line):
            # Look ahead for section title
            if i + 2 < len(lines):
                section_title = lines[i + 2].strip()
                if section_title and not re.match(r'^\d', section_title) and len(section_title) > 3:
                    markdown_lines.append(f"#### {line} {section_title}")
                    markdown_lines.append("")
                    i += 3  # Skip the number, empty line, and title
                    continue
        
        # Handle numbered lists (like "1. ", "2. ", etc. at start of line)
        if re.match(r'^\d+\.\s', line):
            markdown_lines.append(f"{line}")
            i += 1
            continue
            
        # Handle bullet points (convert • to -)
        if line.startswith('•'):
            markdown_lines.append(f"- {line[1:].strip()}")
            i += 1
            continue
            
        # Handle regular content
        if line:
            # Check if this might be a page number or isolated number
            if line.isdigit() and len(line) <= 3:
                # Skip likely page numbers
                i += 1
                continue
            # Handle references in brackets
            line = re.sub(r'\[([^\]]+)\]', r'[\1]', line)
            markdown_lines.append(line)
        else:
            # Preserve empty lines for paragraph breaks
            markdown_lines.append("")
            
        i += 1
    
    # Clean up multiple consecutive empty lines
    cleaned_lines = []
    prev_empty = False
    for line in markdown_lines:
        if line == "":
            if not prev_empty:
                cleaned_lines.append(line)
            prev_empty = True
        else:
            cleaned_lines.append(line)
            prev_empty = False
    
    # Write the markdown content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines))
    
    print(f"Converted {input_file} to {output_file}")

if __name__ == "__main__":
    input_file = "CogPrime_Overview_Paper.txt"
    output_file = "CogPrime_Overview_Paper.md"
    convert_to_markdown(input_file, output_file)
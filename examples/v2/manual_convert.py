#!/usr/bin/env python3
"""
Manually convert CogPrime_Overview_Paper.txt to properly formatted Markdown.
Based on analysis of the actual document structure.
"""

import re
import sys

def convert_to_markdown(input_file, output_file):
    """Convert the extracted PDF text to properly formatted Markdown."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    markdown_lines = []
    
    # Known section mappings based on analysis
    section_headers = {
        14: "Introduction",
        266: "CogPrime and OpenCog", 
        617: "High-Level Architecture of CogPrime",
        1239: "Memory Types and Associated Cognitive Processes in CogPrime"
    }
    
    subsection_patterns = [
        (38, "AI versus AGI"),
        (81, "What's the Secret Sauce?"),
        (120, "What Kind of \"Intelligence\" is CogPrime Aimed At?"),
        (175, "Key Claims"),
        (281, "Current and Prior Applications of OpenCog"),
        (347, "Transitioning from Virtual Agents to a Physical Robot")
    ]
    
    i = 0
    section_num = 1
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Handle title
        if i == 0:
            markdown_lines.append(f"# {line}")
            i += 1
            continue
        elif i == 1:
            markdown_lines[-1] += f" {line}"
            i += 1
            continue
            
        # Handle author and date
        if line == "Ben Goertzel":
            markdown_lines.append(f"**{line}**")
            markdown_lines.append("")
            i += 1
            continue
        elif line == "October 2, 2012":
            markdown_lines.append(f"**{line}**")
            markdown_lines.append("")
            i += 1
            continue
            
        # Handle Abstract
        if line == "Abstract":
            markdown_lines.append("## Abstract")
            markdown_lines.append("")
            i += 1
            # Process abstract content
            while i < len(lines) and i < 14:  # Abstract ends before Introduction
                abstract_line = lines[i].strip()
                if abstract_line and not abstract_line.isdigit():
                    markdown_lines.append(abstract_line)
                elif not abstract_line:
                    markdown_lines.append("")
                i += 1
            continue
            
        # Handle main sections
        if i in section_headers:
            markdown_lines.append(f"## {section_num}. {section_headers[i]}")
            markdown_lines.append("")
            section_num += 1
            i += 1
            continue
            
        # Handle subsections  
        subsection_found = False
        for line_num, title in subsection_patterns:
            if i == line_num:
                markdown_lines.append(f"### {title}")
                markdown_lines.append("")
                subsection_found = True
                break
        if subsection_found:
            i += 1
            continue
            
        # Handle numbered lists
        if re.match(r'^\d+\.\s', line):
            markdown_lines.append(f"{line}")
            i += 1
            continue
            
        # Handle bullet points
        if line.startswith('•'):
            markdown_lines.append(f"- {line[1:].strip()}")
            i += 1
            continue
            
        # Skip isolated numbers (likely page numbers)
        if line.isdigit() and len(line) <= 3:
            i += 1
            continue
            
        # Handle regular content
        if line:
            markdown_lines.append(line)
        else:
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
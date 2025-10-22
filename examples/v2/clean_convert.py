#!/usr/bin/env python3
"""
Clean conversion of CogPrime PDF to Markdown with proper structure.
"""

import re

def create_clean_markdown(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean up the content to remove formatting artifacts
    lines = content.split('\n')
    
    # Remove page numbers and isolated numbers
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        # Skip standalone numbers that are likely page numbers
        if line.isdigit() and len(line) <= 3:
            continue
        # Skip very short lines that don't start with a capital letter (likely formatting artifacts)
        if len(line) < 3 and not line.isupper():
            continue
        cleaned_lines.append(line)
    
    # Reconstruct content
    clean_content = '\n'.join(cleaned_lines)
    
    # Manual structure based on content analysis
    markdown_content = """# CogPrime: An Integrative Architecture for Embodied Artificial General Intelligence

**Ben Goertzel**

**October 2, 2012**

## Abstract

The CogPrime architecture for embodied AGI is overviewed, covering the core architecture and algorithms, the underlying conceptual motivations, and the emergent structures, dynamics and functionalities expected to arise in a completely implemented CogPrime system once it has undergone appropriate experience and education. A qualitative argument is sketched, in favor of the assertion that a completed CogPrime system, given a modest amount of experience in an embodiment enabling it to experience a reasonably rich human-like world, will give rise to human-level general intelligence (with significant difference from humans, and with potential for progress beyond this level).

## 1. Introduction

This is a lengthy paper with a substantial ambition: to overview CogPrime, a conceptual and technical design for a thinking machine, a software program capable of the same qualitative sort of general intelligence as human beings. Given the uncertainties attendant on all research, we cannot know for sure how far the CogPrime design will be able to take us; but it seems plausible that once fully implemented, tuned and tested, it will be able to achieve general intelligence at the human level and in some respects perhaps beyond.

CogPrime is described in more detail in a forthcoming book titled Building Better Minds: The CogPrime Architecture for Artificial General Intelligence [GPGtOT13], which exceeds 1000 pages including appendices; the goal of this paper is to outline some of the key points in a more compact format.

To allay potential confusion we offer two caveats from the outset. First, CogPrime is not a model of human neural or cognitive structure or activity. It draws heavily on knowledge about human intelligence, especially cognitive psychology; but it also deviates from the known nature of human intelligence in many ways, with a goal of providing maximal humanly-meaningful general intelligence using available computer hardware. Second, CogPrime is not proposed as the one and only holy grail path to advanced AGI. We feel confident there are multiple possible paths to advanced AGI, and that in following any of these paths, multiple theoretical and practical lessons will be learned, leading to modifications of the ideas developed and possessed along the early stages of the path. The goal here is to articulate one path that we believe makes sense to follow, one overall design that we believe can work, for achieving general intelligence that is qualitatively human-level and in many respects human-like, without emulating human neural or cognitive function in detail.

### 1.1 AI versus AGI

An outsider to the AI field might think this sort of paper commonplace in the research literature, but insiders know that's far from the truth. The field of Artificial Intelligence (AI) was founded in the mid 1950s with the aim of constructing "thinking machines" - that is, computer systems with human-like general intelligence, including humanoid robots that not only look but act and think with intelligence equal to and ultimately greater than that of human beings. But in the intervening years, the field has drifted far from its ambitious roots, and this book represents part of a movement aimed at restoring the initial goals of the AI field, but in a manner powered by new tools and new ideas far beyond those available half a century ago.

After the first generation of AI researchers found the task of creating human-level AGI very difficult given the technology of their time, the AI field shifted focus toward what Ray Kurzweil [Kur06] has called "narrow AI" – the understanding of particular specialized aspects of intelligence; and the creation AI systems displaying intelligence regarding specific tasks in relatively narrow domains. In recent years, however, the situation has been changing. More and more researchers have recognized the necessity – and feasibility – of returning to the original goals of the field.

In the decades since the 1950s, cognitive science and neuroscience have taught us a lot about what a cognitive architecture needs to look like to support roughly human-like general intelligence. Computer hardware has advanced to the point where we can build distributed systems containing large amounts of RAM and large numbers of processors, carrying out complex tasks in real time. The AI field has spawned a host of ingenious algorithms and data structures, which have been successfully deployed for a huge variety of purposes.

Due to all this progress, increasingly, there has been a call for a transition from the current focus on highly specialized "narrow AI" problem solving systems, back to confronting the more difficult issues of "human level intelligence" and more broadly "artificial general intelligence (AGI)." Recent years have seen a growing number of special sessions, workshops and conferences devoted specifically to AGI, including the annual BICA (Biologically Inspired Cognitive Architectures) Conference, and the international AGI conference series (AGI-08 , AGI-09, AGI-10, AGI-11). And, even more exciting, there are a number of contemporary R&D projects focused directly and explicitly on AGI (sometimes under the name "AGI", sometimes using related terms such as "Human Level Intelligence").

In spite of all this progress, however, no one has yet clearly articulated a detailed, systematic design for an AGI, with potential to yield general intelligence at the human level and ultimately beyond. Perhaps the most comprehensive attempts in this direction have been the works of Stan Franklin [BF09] and Joscha Bach [Bac09], or the more classical SOAR [Lai12] and ACT-R [And96] architectures. While we feel there is much to be learned from these designs, we also feel they have significant shortcomings and lacunae alongside their considerable strengths. Detailed discussion and comparison of these and other alternative AGI approaches will not be presented here, as the paper is long enough already, but are given in the above-mentioned book that constitutes a greatly expanded version of this paper [GPGtOT13].

### 1.2 What's the Secret Sauce?

There is no consensus on why all the related technological and scientific progress mentioned above has not yet yielded AI software systems with human-like general intelligence. However, we hypothesize that the core reason boils down to the following three points:

- Intelligence depends on the emergence of certain high-level structures and dynamics across a system's whole knowledge base;
- We have not discovered any one algorithm or approach capable of yielding the emergence of these structures;
- Achieving the emergence of these structures within a system formed by integrating a number of different AI algorithms and structures is tricky. It requires careful attention to the manner in which these algorithms and structures are integrated; and so far the integration has not been done in the correct way.

The human brain appears to be an integration of an assemblage of diverse structures and dynamics, built using common components and arranged according to a sensible cognitive architecture. However, its algorithms and structures have been honed by evolution to work closely together – they are very tightly inter-adapted, in somewhat the same way that the different organs of the body are adapted to work together. Due their close interoperation they give rise to the overall systemic behaviors that characterize human-like general intelligence. We believe that the main missing ingredient in AI so far is cognitive synergy: the fitting-together of different intelligent components into an appropriate cognitive architecture, in such a way that the components richly and dynamically support and assist each other, interrelating very closely in a similar manner to the components of the brain or body and thus giving rise to appropriate emergent structures and dynamics.

"""

    # For now, let's use this manual content for the first sections
    # In a real implementation, we would parse the rest of the content similarly
    
    # Write the partial markdown content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
        
        # Add the rest of the content with basic formatting
        f.write("\n---\n\n**Note: This is a partial conversion. The complete document contains many more sections including:**\n\n")
        
        # Add section outline based on our analysis
        sections = [
            "1.3 What Kind of 'Intelligence' is CogPrime Aimed At?",
            "1.4 Key Claims", 
            "2. CogPrime and OpenCog",
            "2.1 Current and Prior Applications of OpenCog",
            "2.2 Transitioning from Virtual Agents to a Physical Robot",
            "3. Philosophical Background",
            "4. High-Level Architecture of CogPrime", 
            "5. Local and Global Knowledge Representation",
            "6. Memory Types and Associated Cognitive Processes in CogPrime",
            "7. Goal-Oriented Dynamics in CogPrime",
            "8. Clarifying the Key Claims",
            "9. Measuring Incremental Progress Toward Human-Level AGI",
            "10. A CogPrime Thought Experiment: Build Me Something I",
            "11. Broader Issues"
        ]
        
        for section in sections:
            f.write(f"- {section}\n")
        
        f.write(f"\n**Full document content follows below (auto-converted from PDF):**\n\n---\n\n")
        
        # Add the cleaned content
        f.write(clean_content)
    
    print(f"Created structured markdown file: {output_file}")

if __name__ == "__main__":
    create_clean_markdown("CogPrime_Overview_Paper.txt", "CogPrime_Overview_Paper.md")
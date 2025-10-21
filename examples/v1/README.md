# OpenCog v1 Model Implementations

This directory contains standalone implementations of OpenCog cognitive architecture components, based on the v1 documentation cards, schemas, and playbooks.

## Overview

The v1 models provide a complete, working implementation of core OpenCog concepts without requiring the full OpenCog stack. All implementations are based on the documentation in this directory and follow the JSON schemas defined in `schemas/`.

## Components

### 1. AtomSpace (`models/atomspace.py`)
- **Atoms**: Base class for all atomic units of knowledge
- **Nodes**: Atomic symbols (ConceptNode, PredicateNode, NumberNode)  
- **Links**: Hyperedges connecting atoms (InheritanceLink, ImplicationLink, EvaluationLink)
- **Truth Values**: (strength, confidence) pairs for uncertain knowledge
- **Attention Values**: (STI, LTI) for importance weighting
- **AtomSpace**: Container and query interface for atoms

Based on: `cards/opencog/atomspace-basics.md` and `schemas/atom.json`

### 2. PLN Reasoner (`models/pln.py`)
- **Deduction**: A⇒B ∧ A ⊢ B
- **Induction**: Multiple A∧B observations ⊢ A⇒B  
- **Abduction**: A⇒B ∧ B ⊢ A (with penalty)
- **Revision**: Combine independent evidence for same proposition
- **Forward/Backward Chaining**: Automated inference

Based on: `cards/pln/uncertain-inference.md` and `schemas/inference_step.json`

### 3. MOSES Programs (`models/moses.py`)
- **Expression Trees**: Typed expression representation
- **Operators**: Arithmetic, comparison, logical, conditional
- **Program Evolution**: Genetic programming for program synthesis
- **Fitness Functions**: Accuracy, MDL-based evaluation

Based on: `cards/moses/program-representation.md` and `schemas/program.json`

### 4. Pattern Mining (`models/pattern_mining.py`)
- **Subgraph Patterns**: Frequent structures in heterogeneous graphs
- **Metrics**: Support, confidence, lift, MDL gain, attention weighting
- **Mining Algorithm**: Iterative pattern growth with frequency pruning

Based on: `cards/pattern-mining/hetero-graphs.md`

## Usage

### Quick Start

```python
from models import AtomSpace, ConceptNode, InheritanceLink, TruthValue
from models import PLNReasoner

# Create knowledge base
atomspace = AtomSpace()

# Add concepts
cat = ConceptNode("Cat", tv=TruthValue(0.9, 0.8))
mammal = ConceptNode("Mammal", tv=TruthValue(0.95, 0.9))
atomspace.add_atom(cat)
atomspace.add_atom(mammal)

# Add relationship
inheritance = InheritanceLink(cat, mammal, tv=TruthValue(0.9, 0.85))
atomspace.add_atom(inheritance)

# Reason with PLN
reasoner = PLNReasoner(atomspace)
result_tv, step = reasoner.deduction(inheritance, cat)
print(f"Deduction result: {result_tv}")
```

### Complete Example

Run the comprehensive demonstration:

```bash
python3 real_example_v1.py
```

This demonstrates:
- Knowledge base construction
- PLN reasoning (all 4 rule types)
- MOSES program evolution
- Pattern mining
- Belief network processing (following playbook)
- JSON serialization

### Testing

Validate all components:

```bash
python3 test_models.py
```

## Files

### Implementation
- `models/__init__.py` - Module interface
- `models/atomspace.py` - AtomSpace and atom types  
- `models/pln.py` - PLN reasoner implementation
- `models/moses.py` - Program representation and evolution
- `models/pattern_mining.py` - Graph pattern mining

### Examples & Tests
- `real_example_v1.py` - Complete demonstration
- `test_models.py` - Unit tests for all components
- `v1_example_results.json` - Sample output from demo

### Documentation (existing)
- `cards/` - Implementation specifications
- `playbooks/` - Usage guidelines  
- `schemas/` - JSON schemas for data structures

## Key Features

### Standards Compliance
- All implementations follow the v1 cards exactly
- JSON serialization matches schemas precisely
- Truth value calculations use specified formulas
- Attention value integration as documented

### No External Dependencies
- Pure Python implementation
- No OpenCog installation required
- Self-contained cognitive architecture
- Portable across platforms

### Complete Integration
- All components work together seamlessly
- Shared AtomSpace for unified knowledge representation
- PLN reasoning over MOSES-generated programs
- Pattern mining discovers frequent reasoning patterns
- Attention values guide processing focus

### Educational Value
- Clear, readable implementations
- Extensive documentation and examples
- Step-by-step inference traces
- Modular design for easy experimentation

## Architecture

The v1 models implement a simplified but complete cognitive architecture:

```
┌─────────────────┐    ┌─────────────────┐
│   AtomSpace     │◄──►│  PLN Reasoner   │
│   (Knowledge)   │    │  (Inference)    │
└─────────────────┘    └─────────────────┘
         ▲                       ▲
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│ Pattern Mining  │    │ MOSES Evolution │
│ (Learning)      │    │ (Adaptation)    │
└─────────────────┘    └─────────────────┘
```

- **AtomSpace**: Central knowledge representation
- **PLN**: Probabilistic logical inference
- **MOSES**: Program synthesis and optimization  
- **Pattern Mining**: Statistical learning from data

## Truth Value Semantics

Truth values use Simple Truth Value (STV) format:
- **Strength (s)**: Probability/degree ∈ [0,1]
- **Confidence (c)**: Evidence reliability ∈ [0,1]

### PLN Rule Implementations

1. **Deduction**: `s_B = s_AB × s_A`, `c_B = 1 - (1-c_AB)(1-c_A)`
2. **Induction**: `s = positive_cases/total`, `c = min(0.6, √n/(√n+10))`  
3. **Abduction**: `s_A = s_B × s_AB × λ`, `c_A = 1 - (1-c_AB)(1-c_B)`
4. **Revision**: `s = (w₁s₁ + w₂s₂)/(w₁+w₂)`, `c = 1 - (1-c₁)(1-c₂)`

Where `w = c/(1-c+ε)` and `λ = 0.5` (abduction penalty).

## Performance Notes

The v1 implementations prioritize clarity and correctness over performance:
- Suitable for research, education, and prototyping
- Knowledge bases up to ~1000 atoms perform well
- Pattern mining scales to ~100 patterns
- MOSES evolution handles populations up to ~100 programs

For production systems with larger knowledge bases, consider:
- Indexing optimizations for AtomSpace queries
- Incremental pattern mining algorithms
- Parallel MOSES evolution
- Attention-based processing focus

## Extensions

The modular design supports easy extension:
- Additional atom types (inherit from `Atom`)
- New PLN rules (extend `PLNReasoner`)
- Custom fitness functions (for MOSES)
- Specialized pattern types (extend pattern mining)
- Alternative truth value types
- Integration with external knowledge sources

## License

Same as parent repository (AGPL-3.0).

---

*This implementation demonstrates that cognitive architectures can be built with clear, understandable code while maintaining theoretical rigor.*
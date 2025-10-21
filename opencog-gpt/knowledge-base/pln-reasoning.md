# Probabilistic Logic Networks (PLN) Knowledge Base

## Overview
PLN is OpenCog's uncertain inference system that enables reasoning with probabilistic truth values, combining logical inference with uncertainty handling.

## Core PLN Concepts

### Truth Values in PLN
PLN extends basic truth values with:
- **Strength (s)**: Probability that the statement is true
- **Confidence (c)**: Degree of confidence in the strength estimate
- **Count (n)**: Amount of evidence (for IndefiniteTruthValue)

### PLN Rules Categories

#### Deduction Rules
- **Deduction**: If A→B and B→C, then A→C
- **Modus Ponens**: If A→B and A, then B
- **Universal Instantiation**: From ∀x P(x) infer P(a)

#### Induction Rules
- **Induction**: If A→B observed frequently, strengthen A→B
- **Abduction**: If B observed and A→B known, strengthen A

#### Revision Rules
- **Revision**: Combine multiple truth values for same atom
- **Choice**: Select between conflicting beliefs

### Forward vs Backward Chaining

#### Forward Chaining
- Start with known facts
- Apply inference rules
- Derive new conclusions
- Bottom-up reasoning

#### Backward Chaining  
- Start with goal/query
- Find rules that could prove goal
- Recursively prove subgoals
- Top-down reasoning

### PLN Control Strategies

#### Attention-Based Control
- Focus inference on high-STI atoms
- Use AttentionalFocus for efficiency
- Priority-based rule selection

#### Goal-Driven Control
- Target-specific inference chains
- Minimize irrelevant computations
- Dynamic rule ordering

### Truth Value Calculations

#### Deduction Formula
```
If P(A→B) = <s1, c1> and P(B→C) = <s2, c2>
Then P(A→C) = <s1*s2, c1*c2*consistency>
```

#### Revision Formula
```
If P(A) = <s1, c1> and P(A) = <s2, c2> (from different sources)
Then P(A) = <(s1*c1 + s2*c2)/(c1+c2), (c1+c2)/(1+c1*c2)>
```

### PLN Implementation Example

#### Basic PLN Query
```scheme
(pln-bc 
    (InheritanceLink
        (VariableNode "$x")
        (ConceptNode "animal"))
    #:maximum-iterations 100)
```

#### PLN Forward Chaining
```scheme
(pln-fc
    (AtomSpace knowledge-base)
    #:steps 50
    #:focus-set focus-atoms)
```

### Common PLN Patterns

#### Concept Inheritance
```scheme
(InheritanceLink (stv 0.9 0.8)
    (ConceptNode "cat")
    (ConceptNode "mammal"))
    
(InheritanceLink (stv 0.8 0.9)
    (ConceptNode "mammal") 
    (ConceptNode "animal"))
```

#### Property Attribution
```scheme
(EvaluationLink (stv 0.7 0.6)
    (PredicateNode "has-property")
    (ListLink
        (ConceptNode "bird")
        (ConceptNode "can-fly")))
```

### Performance Optimization

#### Rule Selection Strategies
- Fitness-based rule ordering
- Complexity-weighted selection  
- Domain-specific rule priorities

#### Memory Management
- Truth value compression
- Atom importance scoring
- Garbage collection of low-confidence atoms

### Advanced PLN Features

#### Fuzzy Pattern Matching
- Approximate pattern matches
- Similarity-based substitutions
- Confidence-weighted matching

#### Temporal Reasoning
- Time-indexed truth values
- Temporal inference rules
- Event sequence processing

### Best Practices
1. Design appropriate truth value schemes
2. Balance forward and backward chaining
3. Tune attention parameters carefully
4. Monitor inference convergence
5. Validate inference results against ground truth
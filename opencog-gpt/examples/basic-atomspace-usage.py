#!/usr/bin/env python3
"""
Basic AtomSpace Usage Examples
Demonstrates fundamental OpenCog AtomSpace operations
"""

from opencog.atomspace import AtomSpace, types
from opencog.utilities import initialize_opencog
from opencog.type_constructors import *
from opencog.bindlink import execute_atom

def create_basic_atoms():
    """Create basic atoms in the AtomSpace"""
    # Initialize AtomSpace
    atomspace = AtomSpace()
    initialize_opencog(atomspace)
    
    # Create concept nodes
    cat = ConceptNode("cat")
    mammal = ConceptNode("mammal") 
    animal = ConceptNode("animal")
    
    print(f"Created atoms: {cat}, {mammal}, {animal}")
    
    # Create inheritance relationships
    cat_mammal = InheritanceLink(cat, mammal)
    mammal_animal = InheritanceLink(mammal, animal)
    
    print(f"Created inheritance links:")
    print(f"  {cat_mammal}")
    print(f"  {mammal_animal}")
    
    return atomspace

def work_with_truth_values():
    """Demonstrate truth value operations"""
    atomspace = AtomSpace()
    initialize_opencog(atomspace)
    
    # Create atom with truth value
    cat = ConceptNode("cat")
    cat.tv = TruthValue(0.8, 0.9)  # strength=0.8, confidence=0.9
    
    print(f"Cat truth value: {cat.tv}")
    print(f"Strength: {cat.tv.mean}, Confidence: {cat.tv.confidence}")
    
    # Create evaluation with truth value
    likes = PredicateNode("likes")
    john = ConceptNode("John")
    pizza = ConceptNode("pizza")
    
    evaluation = EvaluationLink(
        likes,
        ListLink(john, pizza)
    )
    evaluation.tv = TruthValue(0.7, 0.6)
    
    print(f"Evaluation: {evaluation}")
    print(f"Truth value: {evaluation.tv}")

def pattern_matching_example():
    """Demonstrate pattern matching with queries"""
    atomspace = AtomSpace()
    initialize_opencog(atomspace)
    
    # Add some knowledge
    john = ConceptNode("John")
    mary = ConceptNode("Mary")
    pizza = ConceptNode("pizza")
    pasta = ConceptNode("pasta")
    likes = PredicateNode("likes")
    
    # Create facts
    john_likes_pizza = EvaluationLink(likes, ListLink(john, pizza))
    mary_likes_pasta = EvaluationLink(likes, ListLink(mary, pasta))
    
    # Create query to find who likes what
    var_person = VariableNode("$person")
    var_food = VariableNode("$food")
    
    query = GetLink(
        VariableList(var_person, var_food),
        EvaluationLink(
            likes,
            ListLink(var_person, var_food)
        )
    )
    
    print("Query for who likes what:")
    print(f"Query: {query}")
    
    # Execute query
    results = execute_atom(atomspace, query)
    print(f"Results: {results}")

def hierarchical_knowledge():
    """Build and query hierarchical knowledge"""
    atomspace = AtomSpace()
    initialize_opencog(atomspace)
    
    # Create taxonomy
    animals = [
        ("cat", "mammal"),
        ("dog", "mammal"), 
        ("mammal", "animal"),
        ("bird", "animal"),
        ("robin", "bird"),
        ("eagle", "bird")
    ]
    
    # Add inheritance relationships
    for child, parent in animals:
        child_node = ConceptNode(child)
        parent_node = ConceptNode(parent)
        InheritanceLink(child_node, parent_node)
        
    print("Created taxonomic hierarchy:")
    for child, parent in animals:
        print(f"  {child} -> {parent}")
    
    # Query for all mammals
    var_mammal = VariableNode("$mammal")
    mammal_query = GetLink(
        var_mammal,
        InheritanceLink(var_mammal, ConceptNode("mammal"))
    )
    
    print("\nQuerying for mammals:")
    mammals = execute_atom(atomspace, mammal_query)
    print(f"Found mammals: {mammals}")

def main():
    """Run all examples"""
    print("=== Basic Atom Creation ===")
    create_basic_atoms()
    
    print("\n=== Truth Values ===")
    work_with_truth_values()
    
    print("\n=== Pattern Matching ===")
    pattern_matching_example()
    
    print("\n=== Hierarchical Knowledge ===")
    hierarchical_knowledge()

if __name__ == "__main__":
    main()
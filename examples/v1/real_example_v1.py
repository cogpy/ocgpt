#!/usr/bin/env python3
"""
Real Example v1: Complete OpenCog Model Implementation Demo

This example demonstrates all the v1 model implementations working together:
- AtomSpace with Nodes and Links
- PLN reasoning with deduction, induction, abduction, and revision
- MOSES program evolution
- Pattern mining on heterogeneous graphs

Based on the v1 cards, schemas, and playbooks.
"""

import json
import random
from typing import List, Dict, Any

# Import our v1 model implementations
from models.atomspace import (
    AtomSpace, ConceptNode, PredicateNode, NumberNode,
    InheritanceLink, ImplicationLink, EvaluationLink, ListLink,
    TruthValue, AttentionValue
)
from models.pln import PLNReasoner
from models.moses import Program, Expression, ExprKind, MOSESEvolver, accuracy_fitness
from models.pattern_mining import PatternMiner


def create_knowledge_base() -> AtomSpace:
    """Create a sample knowledge base following the v1 schemas"""
    atomspace = AtomSpace()
    
    # Create concepts
    cat = ConceptNode("Cat", tv=TruthValue(0.9, 0.8), av=AttentionValue(0.7, 0.5))
    dog = ConceptNode("Dog", tv=TruthValue(0.9, 0.8), av=AttentionValue(0.6, 0.4))
    mammal = ConceptNode("Mammal", tv=TruthValue(0.95, 0.9), av=AttentionValue(0.8, 0.7))
    animal = ConceptNode("Animal", tv=TruthValue(0.98, 0.95), av=AttentionValue(0.9, 0.8))
    
    # Add to atomspace
    atomspace.add_atom(cat)
    atomspace.add_atom(dog)
    atomspace.add_atom(mammal)
    atomspace.add_atom(animal)
    
    # Create inheritance relationships
    cat_mammal = InheritanceLink(cat, mammal, tv=TruthValue(0.9, 0.85))
    dog_mammal = InheritanceLink(dog, mammal, tv=TruthValue(0.9, 0.85))
    mammal_animal = InheritanceLink(mammal, animal, tv=TruthValue(0.95, 0.9))
    
    atomspace.add_atom(cat_mammal)
    atomspace.add_atom(dog_mammal)
    atomspace.add_atom(mammal_animal)
    
    # Create some predicates and evaluations
    likes = PredicateNode("likes")
    eats = PredicateNode("eats")
    
    john = ConceptNode("John")
    food = ConceptNode("Food")
    fish = ConceptNode("Fish")
    
    atomspace.add_atom(likes)
    atomspace.add_atom(eats)
    atomspace.add_atom(john)
    atomspace.add_atom(food)
    atomspace.add_atom(fish)
    
    # John likes cats
    john_likes_cats = EvaluationLink(
        likes,
        ListLink([john, cat]),
        tv=TruthValue(0.8, 0.7)
    )
    atomspace.add_atom(john_likes_cats)
    
    # Cats eat fish
    cats_eat_fish = EvaluationLink(
        eats,
        ListLink([cat, fish]),
        tv=TruthValue(0.7, 0.6)
    )
    atomspace.add_atom(cats_eat_fish)
    
    # Create implication: if X is mammal, then X is animal
    var_x = ConceptNode("$X")
    atomspace.add_atom(var_x)
    
    mammal_implies_animal = ImplicationLink(
        InheritanceLink(var_x, mammal),
        InheritanceLink(var_x, animal),
        tv=TruthValue(0.98, 0.95)
    )
    atomspace.add_atom(mammal_implies_animal)
    
    return atomspace


def demonstrate_pln_reasoning(atomspace: AtomSpace):
    """Demonstrate PLN reasoning capabilities"""
    print("=== PLN Reasoning Demonstration ===")
    
    reasoner = PLNReasoner(atomspace)
    
    # Get some atoms for reasoning
    cat = atomspace.get_atoms_by_name("Cat")[0]
    dog = atomspace.get_atoms_by_name("Dog")[0]
    mammal = atomspace.get_atoms_by_name("Mammal")[0]
    animal = atomspace.get_atoms_by_name("Animal")[0]
    
    # Find inheritance links
    cat_mammal = None
    mammal_animal = None
    
    for atom in atomspace.atoms.values():
        if isinstance(atom, InheritanceLink):
            outgoing = atomspace.get_outgoing_atoms(atom)
            if len(outgoing) == 2:
                if outgoing[0].name == "Cat" and outgoing[1].name == "Mammal":
                    cat_mammal = atom
                elif outgoing[0].name == "Mammal" and outgoing[1].name == "Animal":
                    mammal_animal = atom
    
    # 1. Deduction: Cat -> Mammal, Mammal -> Animal, therefore Cat -> Animal
    if cat_mammal and mammal_animal:
        print("\n1. Deduction Example:")
        print(f"   Premise 1: {cat_mammal} {cat_mammal.tv}")
        print(f"   Premise 2: {mammal_animal} {mammal_animal.tv}")
        
        result_tv, step = reasoner.deduction(cat_mammal, cat)
        print(f"   Conclusion: Cat is Animal with {result_tv}")
    
    # 2. Induction: Multiple observations to generalize
    print("\n2. Induction Example:")
    observations = [(cat, mammal), (dog, mammal)]
    result_tv, step = reasoner.induction(observations)
    print(f"   From observations of cats and dogs being mammals:")
    print(f"   Induced rule strength: {result_tv}")
    
    # 3. Abduction: Reasoning from effect to cause
    print("\n3. Abduction Example:")
    if mammal_animal:
        result_tv, step = reasoner.abduction(mammal_animal, animal)
        print(f"   Given: {mammal_animal} and Animal is observed")
        print(f"   Abduced: Mammal with {result_tv}")
    
    # 4. Revision: Combining evidence
    print("\n4. Revision Example:")
    tv1 = TruthValue(0.7, 0.6)
    tv2 = TruthValue(0.8, 0.5)
    result_tv, step = reasoner.revision(tv1, tv2, "cat_is_animal")
    print(f"   Evidence 1: {tv1}")
    print(f"   Evidence 2: {tv2}")
    print(f"   Revised belief: {result_tv}")
    
    # 5. Forward chaining
    print("\n5. Forward Chaining:")
    new_atoms = reasoner.forward_chaining(max_iterations=3)
    print(f"   Derived {len(new_atoms)} new facts")
    for atom in new_atoms[:3]:  # Show first 3
        print(f"   - {atom}")
    
    # Print inference trace
    print("\n6. Inference Trace:")
    reasoner.print_trace()


def demonstrate_moses_evolution():
    """Demonstrate MOSES program evolution"""
    print("\n=== MOSES Program Evolution Demonstration ===")
    
    # Create training data for a simple function: y = x^2 + 2x + 1
    print("Training data: y = x^2 + 2*x + 1")
    
    training_data = []
    for x in range(-5, 6):
        y = x * x + 2 * x + 1
        training_data.append({"x": x, "target": y})
    
    print(f"Generated {len(training_data)} training examples")
    
    # Set up MOSES evolver
    variables = ["x"]
    
    def regression_fitness(program: Program, data: List[Dict[str, Any]], target_key: str) -> float:
        """Fitness function for regression"""
        total_error = 0.0
        valid_predictions = 0
        
        for point in data:
            try:
                predicted = program.evaluate(point)
                actual = point[target_key]
                error = abs(predicted - actual)
                total_error += error
                valid_predictions += 1
            except:
                # Penalize programs that crash
                total_error += 100
                valid_predictions += 1
        
        if valid_predictions == 0:
            return 0.0
        
        avg_error = total_error / valid_predictions
        # Convert to fitness (higher is better)
        fitness = 1.0 / (1.0 + avg_error)
        return fitness
    
    evolver = MOSESEvolver(
        variables=variables,
        fitness_function=regression_fitness,
        population_size=30,
        generations=20,
        mutation_rate=0.2
    )
    
    print("\nEvolving programs...")
    best_programs = evolver.evolve(training_data, "target")
    
    print(f"\nTop 3 evolved programs:")
    for i, program in enumerate(best_programs[:3]):
        print(f"{i+1}. {program.expression} (fitness: {program.fitness:.4f})")
        
        # Test on a few points
        print("   Test predictions:")
        for test_x in [0, 1, 2]:
            try:
                predicted = program.evaluate({"x": test_x})
                actual = test_x * test_x + 2 * test_x + 1
                print(f"   x={test_x}: predicted={predicted:.2f}, actual={actual}")
            except:
                print(f"   x={test_x}: prediction failed")


def demonstrate_pattern_mining(atomspace: AtomSpace):
    """Demonstrate pattern mining on the knowledge base"""
    print("\n=== Pattern Mining Demonstration ===")
    
    miner = PatternMiner(
        atomspace=atomspace,
        min_support=2,
        min_confidence=0.1,
        use_attention=True
    )
    
    print("Mining frequent patterns...")
    patterns = miner.mine_frequent_subgraphs(max_pattern_size=2)
    
    print(f"Discovered {len(patterns)} patterns")
    miner.print_patterns(top_n=3)
    
    return patterns


def demonstrate_belief_network_pln(atomspace: AtomSpace):
    """Demonstrate PLN on belief network as per playbooks/pln_on_belief_network.md"""
    print("\n=== PLN on Belief Network (Playbook Demo) ===")
    
    reasoner = PLNReasoner(atomspace)
    
    print("1. Selecting premises for reasoning...")
    
    # Find implication links for reasoning
    implications = []
    for atom in atomspace.atoms.values():
        if isinstance(atom, (ImplicationLink, InheritanceLink)):
            implications.append(atom)
    
    print(f"   Found {len(implications)} implications/inheritances")
    
    print("2. Normalizing STVs...")
    normalized_count = 0
    for atom in atomspace.atoms.values():
        # Ensure truth values are in [0,1]
        if atom.tv.s < 0 or atom.tv.s > 1 or atom.tv.c < 0 or atom.tv.c > 1:
            atom.tv.s = max(0, min(1, atom.tv.s))
            atom.tv.c = max(0, min(1, atom.tv.c))
            normalized_count += 1
    
    print(f"   Normalized {normalized_count} truth values")
    
    print("3. Applying PLN rules...")
    
    # Run forward chaining to derive new facts
    initial_size = len(atomspace.atoms)
    derived = reasoner.forward_chaining(max_iterations=5)
    final_size = len(atomspace.atoms)
    
    print(f"   AtomSpace grew from {initial_size} to {final_size} atoms")
    print(f"   Derived {len(derived)} new facts")
    
    print("4. Recording inference trace...")
    trace = reasoner.get_inference_trace()
    print(f"   Recorded {len(trace)} inference steps")
    
    print("5. Updating attention values...")
    # Increase STI for atoms touched during inference
    touched_atoms = set()
    for step in trace:
        for premise in step['premises']:
            touched_atoms.add(premise['id'])
        touched_atoms.add(step['conclusion']['id'])
    
    for atom_id in touched_atoms:
        atom = atomspace.get_atom(atom_id)
        if atom:
            atom.av.sti = min(1.0, atom.av.sti + 0.1)
    
    print(f"   Updated attention for {len(touched_atoms)} atoms")
    
    print("6. Generating PLN Trace report...")
    print("   Step | Rule      | Premises | Result TV")
    print("   -----|-----------|----------|----------")
    for i, step in enumerate(trace[:5]):  # Show first 5 steps
        rule = step['rule'][:8].ljust(8)
        premises_count = len(step['premises'])
        tv = step['tv_out']
        print(f"   {i+1:4} | {rule} | {premises_count:8} | s={tv['s']:.2f}, c={tv['c']:.2f}")
    
    if len(trace) > 5:
        print(f"   ... and {len(trace) - 5} more steps")


def save_example_results(atomspace: AtomSpace, patterns: List, filename: str = "v1_example_results.json"):
    """Save all results to JSON file"""
    print(f"\nSaving results to {filename}...")
    
    results = {
        "atomspace": atomspace.to_dict(),
        "patterns": [pattern.to_dict() for pattern in patterns],
        "metadata": {
            "version": "1.0",
            "description": "Real Example v1 - Complete OpenCog Model Implementation Demo",
            "components": ["AtomSpace", "PLN", "MOSES", "Pattern Mining"]
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved! File size: {len(json.dumps(results))} characters")


def main():
    """Main demonstration function"""
    print("Real Example v1: OpenCog Model Implementation Demo")
    print("=" * 55)
    
    print("This example demonstrates the complete v1 model implementation")
    print("based on the cards, schemas, and playbooks in examples/v1/\n")
    
    # 1. Create knowledge base
    print("Step 1: Creating Knowledge Base...")
    atomspace = create_knowledge_base()
    print(f"Created AtomSpace with {len(atomspace)} atoms")
    
    # Show some examples
    print("\nSample atoms:")
    for i, atom in enumerate(list(atomspace.atoms.values())[:5]):
        print(f"  {atom}")
    
    # 2. PLN Reasoning
    demonstrate_pln_reasoning(atomspace)
    
    # 3. MOSES Evolution
    demonstrate_moses_evolution()
    
    # 4. Pattern Mining
    patterns = demonstrate_pattern_mining(atomspace)
    
    # 5. Belief Network PLN (following playbook)
    demonstrate_belief_network_pln(atomspace)
    
    # 6. Save results
    save_example_results(atomspace, patterns)
    
    print("\n" + "=" * 55)
    print("Demo completed! All v1 model components demonstrated.")
    print("\nThe implementation includes:")
    print("- AtomSpace with Nodes, Links, Truth Values, Attention Values")
    print("- PLN Reasoner with deduction, induction, abduction, revision")
    print("- MOSES program evolution with expression trees")
    print("- Pattern mining for heterogeneous graphs")
    print("- Complete JSON serialization following v1 schemas")
    print("\nAll components work together as a unified cognitive architecture.")


if __name__ == "__main__":
    main()
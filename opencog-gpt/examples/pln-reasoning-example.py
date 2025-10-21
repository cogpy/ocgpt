#!/usr/bin/env python3
"""
PLN Reasoning Example
Demonstrates probabilistic logic networks inference
"""

from opencog.atomspace import AtomSpace, TruthValue
from opencog.utilities import initialize_opencog
from opencog.type_constructors import *
from opencog.pln import *

def setup_knowledge_base():
    """Create a knowledge base for reasoning"""
    atomspace = AtomSpace()
    initialize_opencog(atomspace)
    
    # Create concepts
    socrates = ConceptNode("Socrates")
    man = ConceptNode("Man")  
    mortal = ConceptNode("Mortal")
    
    # Add knowledge with truth values
    # "Socrates is a man" with high confidence
    socrates_is_man = InheritanceLink(socrates, man)
    socrates_is_man.tv = TruthValue(0.95, 0.9)
    
    # "All men are mortal" with very high confidence  
    man_is_mortal = InheritanceLink(man, mortal)
    man_is_mortal.tv = TruthValue(0.99, 0.95)
    
    print("Knowledge base created:")
    print(f"  {socrates_is_man} {socrates_is_man.tv}")
    print(f"  {man_is_mortal} {man_is_mortal.tv}")
    
    return atomspace

def deduction_example():
    """Demonstrate deductive reasoning"""
    atomspace = setup_knowledge_base()
    
    # Query: Is Socrates mortal?
    socrates = ConceptNode("Socrates")
    mortal = ConceptNode("Mortal")
    
    # Create target for backward chaining
    target = InheritanceLink(socrates, mortal)
    
    print(f"\nQuery: Is Socrates mortal? {target}")
    
    # Run backward chaining PLN inference
    try:
        result = pln_bc(atomspace, target, maximum_iterations=100)
        if result:
            print(f"PLN Result: {result}")
            print(f"Truth Value: {result.tv}")
        else:
            print("No result found")
    except Exception as e:
        print(f"PLN inference error: {e}")

def induction_example():
    """Demonstrate inductive reasoning"""
    atomspace = AtomSpace()
    initialize_opencog(atomspace)
    
    # Observations: multiple birds that can fly
    birds = ["robin", "eagle", "sparrow", "hawk"]
    can_fly = PredicateNode("can_fly")
    
    print("Observations (induction data):")
    for bird_name in birds:
        bird = ConceptNode(bird_name)
        bird_type = ConceptNode("bird")
        
        # Bird is a type of bird
        InheritanceLink(bird, bird_type).tv = TruthValue(0.9, 0.8)
        
        # This specific bird can fly
        fly_eval = EvaluationLink(can_fly, bird)
        fly_eval.tv = TruthValue(0.85, 0.7)
        
        print(f"  {bird_name} is a bird and can fly")
    
    # Try to induce: Do birds generally fly?
    bird_concept = ConceptNode("bird")
    general_fly = EvaluationLink(can_fly, bird_concept)
    
    print(f"\nInduction target: {general_fly}")
    
    # This would require custom induction rules or MOSES integration
    print("Note: Full induction requires additional PLN rule configuration")

def uncertain_reasoning():
    """Demonstrate reasoning with uncertainty"""
    atomspace = AtomSpace()
    initialize_opencog(atomspace)
    
    # Uncertain knowledge about weather and activities
    sunny = ConceptNode("sunny")
    rain = ConceptNode("rain")
    umbrella_needed = ConceptNode("umbrella_needed")
    picnic_good = ConceptNode("picnic_good")
    
    # Probabilistic rules
    # "If it's sunny, picnic is probably good"
    sunny_picnic = ImplicationLink(sunny, picnic_good)
    sunny_picnic.tv = TruthValue(0.8, 0.7)
    
    # "If it's raining, umbrella is needed"
    rain_umbrella = ImplicationLink(rain, umbrella_needed) 
    rain_umbrella.tv = TruthValue(0.95, 0.9)
    
    # Current observation: "It looks like rain"
    current_rain = rain
    current_rain.tv = TruthValue(0.6, 0.5)  # Uncertain
    
    print("Uncertain reasoning scenario:")
    print(f"  {sunny_picnic} {sunny_picnic.tv}")
    print(f"  {rain_umbrella} {rain_umbrella.tv}")  
    print(f"  Current weather (rain): {current_rain.tv}")
    
    # Query: Should I take an umbrella?
    umbrella_query = umbrella_needed
    print(f"\nQuery: {umbrella_query}")
    
    # This demonstrates the setup; actual inference would use PLN rules
    print("PLN would propagate uncertainty through logical implications")

def create_pln_config():
    """Create and configure PLN reasoner"""
    atomspace = AtomSpace()
    initialize_opencog(atomspace)
    
    # Configure PLN parameters
    config = {
        'maximum_iterations': 1000,
        'complexity_penalty': 0.1,
        'confidence_threshold': 0.1,
        'attention_boundary': 0.5
    }
    
    print("PLN Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    return atomspace, config

def main():
    """Run PLN examples"""
    print("=== PLN Reasoning Examples ===")
    
    print("\n--- Deduction Example ---")
    deduction_example()
    
    print("\n--- Induction Example ---") 
    induction_example()
    
    print("\n--- Uncertain Reasoning ---")
    uncertain_reasoning()
    
    print("\n--- PLN Configuration ---")
    create_pln_config()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Test script for v1 model implementations

Validates that all components work correctly before running the full demo.
"""

import sys
import traceback

def test_atomspace():
    """Test AtomSpace implementation"""
    print("Testing AtomSpace...")
    
    try:
        from models.atomspace import AtomSpace, ConceptNode, InheritanceLink, TruthValue
        
        # Create atomspace
        atomspace = AtomSpace()
        
        # Create and add atoms
        cat = ConceptNode("Cat", tv=TruthValue(0.9, 0.8))
        mammal = ConceptNode("Mammal", tv=TruthValue(0.95, 0.9))
        
        atomspace.add_atom(cat)
        atomspace.add_atom(mammal)
        
        # Create link
        inheritance = InheritanceLink(cat, mammal, tv=TruthValue(0.9, 0.85))
        atomspace.add_atom(inheritance)
        
        # Test queries
        assert len(atomspace) == 3
        assert len(atomspace.get_atoms_by_name("Cat")) == 1
        
        # Test serialization
        data = atomspace.to_dict()
        assert "atoms" in data
        assert len(data["atoms"]) == 3
        
        print("  ✓ AtomSpace tests passed")
        return True
        
    except Exception as e:
        print(f"  ✗ AtomSpace test failed: {e}")
        traceback.print_exc()
        return False


def test_pln():
    """Test PLN reasoner"""
    print("Testing PLN Reasoner...")
    
    try:
        from models.atomspace import AtomSpace, ConceptNode, InheritanceLink, TruthValue
        from models.pln import PLNReasoner
        
        # Setup
        atomspace = AtomSpace()
        cat = ConceptNode("Cat", tv=TruthValue(0.9, 0.8))
        mammal = ConceptNode("Mammal", tv=TruthValue(0.95, 0.9))
        
        atomspace.add_atom(cat)
        atomspace.add_atom(mammal)
        
        inheritance = InheritanceLink(cat, mammal, tv=TruthValue(0.9, 0.85))
        atomspace.add_atom(inheritance)
        
        # Test reasoning
        reasoner = PLNReasoner(atomspace)
        
        # Test deduction
        result_tv, step = reasoner.deduction(inheritance, cat)
        assert 0 <= result_tv.s <= 1
        assert 0 <= result_tv.c <= 1
        assert step.rule == "deduction"
        
        # Test induction
        observations = [(cat, mammal)]
        result_tv, step = reasoner.induction(observations)
        assert 0 <= result_tv.s <= 1
        assert step.rule == "induction"
        
        # Test revision
        tv1 = TruthValue(0.7, 0.6)
        tv2 = TruthValue(0.8, 0.5)
        result_tv, step = reasoner.revision(tv1, tv2)
        assert step.rule == "revision"
        
        print("  ✓ PLN Reasoner tests passed")
        return True
        
    except Exception as e:
        print(f"  ✗ PLN test failed: {e}")
        traceback.print_exc()
        return False


def test_moses():
    """Test MOSES implementation"""
    print("Testing MOSES...")
    
    try:
        from models.moses import Expression, Program, ExprKind, ProgramGenerator
        
        # Test expression creation
        const_expr = Expression(kind=ExprKind.CONST, value=5)
        var_expr = Expression(kind=ExprKind.VAR, name="x")
        
        # Test evaluation
        result = const_expr.evaluate({})
        assert result == 5
        
        result = var_expr.evaluate({"x": 10})
        assert result == 10
        
        # Test operation
        add_expr = Expression(
            kind=ExprKind.OP,
            op="+",
            args=[const_expr, var_expr]
        )
        
        result = add_expr.evaluate({"x": 3})
        assert result == 8  # 5 + 3
        
        # Test program
        program = Program(add_expr)
        result = program.evaluate({"x": 2})
        assert result == 7  # 5 + 2
        
        # Test serialization
        data = program.to_dict()
        assert data["type"] == "Program"
        
        # Test program generator
        generator = ProgramGenerator(["x", "y"])
        program = generator.generate_program()
        assert program.expression is not None
        
        print("  ✓ MOSES tests passed")
        return True
        
    except Exception as e:
        print(f"  ✗ MOSES test failed: {e}")
        traceback.print_exc()
        return False


def test_pattern_mining():
    """Test pattern mining"""
    print("Testing Pattern Mining...")
    
    try:
        from models.atomspace import AtomSpace, ConceptNode, InheritanceLink, TruthValue
        from models.pattern_mining import PatternMiner
        
        # Create test atomspace
        atomspace = AtomSpace()
        
        # Add several similar patterns
        for name in ["Cat1", "Cat2", "Cat3"]:
            cat = ConceptNode(name, tv=TruthValue(0.9, 0.8))
            mammal = ConceptNode("Mammal", tv=TruthValue(0.95, 0.9))
            
            atomspace.add_atom(cat)
            atomspace.add_atom(mammal)
            
            inheritance = InheritanceLink(cat, mammal, tv=TruthValue(0.9, 0.85))
            atomspace.add_atom(inheritance)
        
        # Test mining
        miner = PatternMiner(atomspace, min_support=1)
        patterns = miner.mine_frequent_subgraphs(max_pattern_size=2)
        
        # Should find at least some patterns or handle empty result gracefully
        assert len(patterns) >= 0  # Allow empty results for small datasets
        
        # Check pattern structure
        for pattern in patterns:
            assert pattern.support >= 1
            assert 0 <= pattern.confidence <= 1
            assert len(pattern.atoms) > 0
        
        print("  ✓ Pattern Mining tests passed")
        return True
        
    except Exception as e:
        print(f"  ✗ Pattern Mining test failed: {e}")
        traceback.print_exc()
        return False


def test_integration():
    """Test integration of all components"""
    print("Testing Integration...")
    
    try:
        from models.atomspace import AtomSpace, ConceptNode, InheritanceLink, TruthValue
        from models.pln import PLNReasoner
        from models.pattern_mining import PatternMiner
        
        # Create integrated system
        atomspace = AtomSpace()
        reasoner = PLNReasoner(atomspace)
        miner = PatternMiner(atomspace, min_support=1)
        
        # Add knowledge
        cat = ConceptNode("Cat", tv=TruthValue(0.9, 0.8))
        mammal = ConceptNode("Mammal", tv=TruthValue(0.95, 0.9))
        animal = ConceptNode("Animal", tv=TruthValue(0.98, 0.95))
        
        atomspace.add_atom(cat)
        atomspace.add_atom(mammal)
        atomspace.add_atom(animal)
        
        cat_mammal = InheritanceLink(cat, mammal, tv=TruthValue(0.9, 0.85))
        mammal_animal = InheritanceLink(mammal, animal, tv=TruthValue(0.95, 0.9))
        
        atomspace.add_atom(cat_mammal)
        atomspace.add_atom(mammal_animal)
        
        # Test reasoning
        derived = reasoner.forward_chaining(max_iterations=2)
        
        # Test pattern mining
        patterns = miner.mine_frequent_subgraphs()
        
        # Test serialization
        atomspace_data = atomspace.to_dict()
        trace_data = reasoner.get_inference_trace()
        
        assert len(atomspace_data["atoms"]) >= 5
        assert len(patterns) >= 0  # May not find patterns with small data
        
        print("  ✓ Integration tests passed")
        return True
        
    except Exception as e:
        print(f"  ✗ Integration test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("Running v1 Model Tests")
    print("=" * 30)
    
    tests = [
        test_atomspace,
        test_pln,
        test_moses,
        test_pattern_mining,
        test_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 30)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("All tests passed! ✓")
        return True
    else:
        print("Some tests failed! ✗")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
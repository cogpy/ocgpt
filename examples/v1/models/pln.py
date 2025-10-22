"""
PLN (Probabilistic Logic Networks) Reasoner Implementation (v1)

Based on cards/pln/uncertain-inference.md and schemas/inference_step.json
"""

import math
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from .atomspace import Atom, Link, TruthValue, ImplicationLink, InheritanceLink


@dataclass
class InferenceStep:
    """Inference step following schemas/inference_step.json"""
    rule: str  # deduction, induction, abduction, revision
    premises: List[Dict[str, Any]]  # [{"id": str, "tv": {"s": float, "c": float}}]
    conclusion: Dict[str, str]  # {"id": str}
    tv_in: Optional[Dict[str, float]]  # {"s": float, "c": float}
    tv_out: Dict[str, float]  # {"s": float, "c": float}
    notes: str = ""
    
    def to_dict(self):
        """Export to JSON-compatible dict"""
        return asdict(self)


class PLNReasoner:
    """PLN Reasoner implementing the rules from cards/pln/uncertain-inference.md"""
    
    def __init__(self, atomspace=None):
        self.atomspace = atomspace
        self.inference_history: List[InferenceStep] = []
        
        # Default parameters (simulated defaults as per card)
        self.epsilon = 1e-6  # small value for safe division
        self.abduction_penalty = 0.5  # lambda for abduction
        self.confidence_threshold = 0.1
    
    def deduction(self, implication: Atom, antecedent: Atom) -> Tuple[TruthValue, InferenceStep]:
        """
        Deduction: From A ⇒ B and A infer B
        Strength: sB = s1 * s2
        Confidence: cB = 1 - (1-c1)*(1-c2) (noisy-OR)
        """
        tv_impl = implication.tv
        tv_ante = antecedent.tv
        
        # Calculate new truth value
        s_result = tv_impl.s * tv_ante.s
        c_result = 1 - (1 - tv_impl.c) * (1 - tv_ante.c)
        
        result_tv = TruthValue(s_result, c_result)
        
        # Create inference step record
        step = InferenceStep(
            rule="deduction",
            premises=[
                {"id": implication.id, "tv": tv_impl.to_dict()},
                {"id": antecedent.id, "tv": tv_ante.to_dict()}
            ],
            conclusion={"id": f"deduction_result_{len(self.inference_history)}"},
            tv_in=None,
            tv_out=result_tv.to_dict(),
            notes="Deduction rule: sB = s1 * s2, cB = 1 - (1-c1)*(1-c2)"
        )
        
        self.inference_history.append(step)
        return result_tv, step
    
    def induction(self, observations: List[Tuple[Atom, Atom]], sample_size: int = None) -> Tuple[TruthValue, InferenceStep]:
        """
        Induction: From multiple observations of A & B, estimate P(B|A)
        Conservative confidence (≤0.6) as per simulated defaults
        """
        if not observations:
            raise ValueError("Need at least one observation for induction")
        
        # Count positive cases (both A and B are true with high strength)
        positive_cases = 0
        total_cases = len(observations)
        
        for a_atom, b_atom in observations:
            # Consider it a positive case if both have high strength
            if a_atom.tv.s > 0.5 and b_atom.tv.s > 0.5:
                positive_cases += 1
        
        # Estimate strength as frequency
        s_result = positive_cases / total_cases if total_cases > 0 else 0.0
        
        # Conservative confidence based on sample size
        if sample_size is None:
            sample_size = total_cases
        
        # Confidence grows with sample size but capped at 0.6
        c_result = min(0.6, math.sqrt(sample_size) / (math.sqrt(sample_size) + 10))
        
        result_tv = TruthValue(s_result, c_result)
        
        # Create step record
        premise_ids = []
        for i, (a_atom, b_atom) in enumerate(observations):
            premise_ids.extend([
                {"id": a_atom.id, "tv": a_atom.tv.to_dict()},
                {"id": b_atom.id, "tv": b_atom.tv.to_dict()}
            ])
        
        step = InferenceStep(
            rule="induction",
            premises=premise_ids,
            conclusion={"id": f"induction_result_{len(self.inference_history)}"},
            tv_in=None,
            tv_out=result_tv.to_dict(),
            notes=f"Induction from {total_cases} observations, {positive_cases} positive cases"
        )
        
        self.inference_history.append(step)
        return result_tv, step
    
    def abduction(self, implication: Atom, consequent: Atom) -> Tuple[TruthValue, InferenceStep]:
        """
        Abduction: From A ⇒ B and B infer A with penalty
        sA = s(B) * s(A⇒B) * λ, where λ is abduction penalty (default 0.5)
        cA = noisy-OR of input confidences
        """
        tv_impl = implication.tv
        tv_cons = consequent.tv
        
        # Apply penalty for abductive reasoning
        s_result = tv_cons.s * tv_impl.s * self.abduction_penalty
        c_result = 1 - (1 - tv_impl.c) * (1 - tv_cons.c)
        
        result_tv = TruthValue(s_result, c_result)
        
        step = InferenceStep(
            rule="abduction",
            premises=[
                {"id": implication.id, "tv": tv_impl.to_dict()},
                {"id": consequent.id, "tv": tv_cons.to_dict()}
            ],
            conclusion={"id": f"abduction_result_{len(self.inference_history)}"},
            tv_in=None,
            tv_out=result_tv.to_dict(),
            notes=f"Abduction with penalty λ={self.abduction_penalty}"
        )
        
        self.inference_history.append(step)
        return result_tv, step
    
    def revision(self, tv1: TruthValue, tv2: TruthValue, atom_id: str = None) -> Tuple[TruthValue, InferenceStep]:
        """
        Revision: Combine two independent STVs for same proposition
        s' = (w1*s1 + w2*s2) / (w1 + w2), where w = c / (1-c+ε)
        c' = 1 - (1-c1)*(1-c2)
        """
        # Calculate weights from confidences
        w1 = tv1.c / (1 - tv1.c + self.epsilon)
        w2 = tv2.c / (1 - tv2.c + self.epsilon)
        
        # Weighted average of strengths
        s_result = (w1 * tv1.s + w2 * tv2.s) / (w1 + w2) if (w1 + w2) > 0 else (tv1.s + tv2.s) / 2
        
        # Noisy-OR for confidence
        c_result = 1 - (1 - tv1.c) * (1 - tv2.c)
        
        result_tv = TruthValue(s_result, c_result)
        
        step = InferenceStep(
            rule="revision",
            premises=[
                {"id": atom_id or "evidence1", "tv": tv1.to_dict()},
                {"id": atom_id or "evidence2", "tv": tv2.to_dict()}
            ],
            conclusion={"id": atom_id or f"revision_result_{len(self.inference_history)}"},
            tv_in={"s": (tv1.s + tv2.s) / 2, "c": min(tv1.c, tv2.c)},  # avg of inputs as baseline
            tv_out=result_tv.to_dict(),
            notes=f"Revision: weights w1={w1:.3f}, w2={w2:.3f}"
        )
        
        self.inference_history.append(step)
        return result_tv, step
    
    def backward_chaining(self, target: Atom, max_iterations: int = 100) -> Optional[TruthValue]:
        """
        Simple backward chaining to find evidence for target
        Returns the truth value if evidence is found
        """
        if not self.atomspace:
            return None
        
        # Look for direct evidence in atomspace
        existing_atom = self.atomspace.get_atom(target.id)
        if existing_atom and existing_atom.tv.c > self.confidence_threshold:
            return existing_atom.tv
        
        # Look for implications that could lead to target
        for atom in self.atomspace.atoms.values():
            if isinstance(atom, (ImplicationLink, InheritanceLink)):
                outgoing = self.atomspace.get_outgoing_atoms(atom)
                if len(outgoing) == 2:
                    antecedent, consequent = outgoing
                    
                    # Check if this implication concludes our target
                    if consequent.id == target.id or consequent.name == target.name:
                        # Try to prove the antecedent
                        antecedent_tv = self.backward_chaining(antecedent, max_iterations - 1)
                        if antecedent_tv and max_iterations > 0:
                            # Apply deduction
                            result_tv, _ = self.deduction(atom, antecedent)
                            return result_tv
        
        return None
    
    def forward_chaining(self, max_iterations: int = 10) -> List[Atom]:
        """
        Forward chaining: derive new facts from existing knowledge
        Returns list of newly derived atoms
        """
        if not self.atomspace:
            return []
        
        derived_atoms = []
        iteration = 0
        
        while iteration < max_iterations:
            new_derivations = False
            
            # Look for applicable deduction rules
            for atom in list(self.atomspace.atoms.values()):
                if isinstance(atom, (ImplicationLink, InheritanceLink)):
                    outgoing = self.atomspace.get_outgoing_atoms(atom)
                    if len(outgoing) == 2:
                        antecedent, consequent = outgoing
                        
                        # Check if antecedent exists with sufficient confidence
                        if antecedent.tv.c > self.confidence_threshold:
                            # Derive consequent
                            new_tv, step = self.deduction(atom, antecedent)
                            
                            # Check if this is a new or improved conclusion
                            existing = self.atomspace.get_atom(consequent.id)
                            if not existing or new_tv.c > existing.tv.c:
                                # Create or update the consequent atom
                                if existing:
                                    existing.tv = new_tv
                                else:
                                    new_atom = Atom(
                                        id=consequent.id,
                                        name=consequent.name,
                                        subtype=consequent.subtype,
                                        tv=new_tv
                                    )
                                    self.atomspace.add_atom(new_atom)
                                    derived_atoms.append(new_atom)
                                
                                new_derivations = True
            
            if not new_derivations:
                break
            
            iteration += 1
        
        return derived_atoms
    
    def get_inference_trace(self) -> List[Dict[str, Any]]:
        """Get the complete inference trace as list of dicts"""
        return [step.to_dict() for step in self.inference_history]
    
    def clear_history(self):
        """Clear inference history"""
        self.inference_history.clear()
    
    def print_trace(self):
        """Print human-readable inference trace"""
        print("=== PLN Inference Trace ===")
        for i, step in enumerate(self.inference_history):
            print(f"\nStep {i+1}: {step.rule.upper()}")
            print(f"  Premises: {len(step.premises)} atoms")
            for premise in step.premises:
                tv = premise.get('tv', {})
                print(f"    {premise['id']}: s={tv.get('s', 0):.3f}, c={tv.get('c', 0):.3f}")
            
            tv_out = step.tv_out
            print(f"  Result: s={tv_out['s']:.3f}, c={tv_out['c']:.3f}")
            
            if step.notes:
                print(f"  Notes: {step.notes}")
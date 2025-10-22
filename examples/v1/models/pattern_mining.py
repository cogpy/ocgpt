"""
Pattern Mining for Heterogeneous Graphs Implementation (v1)

Based on cards/pattern-mining/hetero-graphs.md
"""

import math
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass
from collections import defaultdict, Counter
from .atomspace import AtomSpace, Atom, Node, Link


@dataclass
class SubgraphMatch:
    """A match of a pattern in the atomspace"""
    pattern_id: str
    atom_mappings: Dict[str, str]  # pattern_atom_id -> actual_atom_id
    support_score: float = 0.0
    
    def to_dict(self):
        return {
            "pattern_id": self.pattern_id,
            "atom_mappings": self.atom_mappings,
            "support_score": self.support_score
        }


@dataclass
class SubgraphPattern:
    """A discovered pattern in the atomspace"""
    id: str
    atoms: List[Atom]  # Pattern atoms (template)
    support: int = 0  # Number of matches found
    confidence: float = 0.0  # Predictive confidence
    lift: float = 0.0  # Lift score
    mdl_gain: float = 0.0  # MDL compression gain
    attention_score: float = 0.0  # Attention-weighted score
    matches: List[SubgraphMatch] = None
    
    def __post_init__(self):
        if self.matches is None:
            self.matches = []
    
    def to_dict(self):
        return {
            "id": self.id,
            "atoms": [atom.to_dict() for atom in self.atoms],
            "support": self.support,
            "confidence": self.confidence,
            "lift": self.lift,
            "mdl_gain": self.mdl_gain,
            "attention_score": self.attention_score,
            "matches": [match.to_dict() for match in self.matches]
        }


class PatternMiner:
    """Pattern miner for heterogeneous graphs (AtomSpace)"""
    
    def __init__(self, atomspace: AtomSpace, min_support: int = 2, 
                 min_confidence: float = 0.1, use_attention: bool = True):
        self.atomspace = atomspace
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.use_attention = use_attention
        
        self.discovered_patterns: List[SubgraphPattern] = []
        self.pattern_cache: Dict[str, List[SubgraphMatch]] = {}
    
    def mine_frequent_subgraphs(self, max_pattern_size: int = 3) -> List[SubgraphPattern]:
        """
        Mine frequent subgraphs using a simplified approach
        
        Args:
            max_pattern_size: Maximum number of atoms in a pattern
        """
        self.discovered_patterns.clear()
        
        # Start with frequent individual atoms
        frequent_atoms = self._find_frequent_atoms()
        
        # Build patterns of increasing size
        current_patterns = []
        
        # Size 1 patterns (single atoms)
        for atom_type, atoms in frequent_atoms.items():
            if len(atoms) >= self.min_support:
                pattern = self._create_single_atom_pattern(atom_type, atoms)
                current_patterns.append(pattern)
        
        # Grow patterns iteratively
        for size in range(2, max_pattern_size + 1):
            new_patterns = []
            
            # Try to extend existing patterns
            for pattern in current_patterns:
                extensions = self._extend_pattern(pattern)
                new_patterns.extend(extensions)
            
            # Filter by support
            current_patterns = [p for p in new_patterns if p.support >= self.min_support]
        
        # Calculate additional metrics for all patterns
        for pattern in current_patterns:
            self._calculate_pattern_metrics(pattern)
            if pattern.confidence >= self.min_confidence:
                self.discovered_patterns.append(pattern)
        
        # Sort by interestingness (combination of metrics)
        self.discovered_patterns.sort(key=self._pattern_interestingness, reverse=True)
        
        return self.discovered_patterns
    
    def _find_frequent_atoms(self) -> Dict[str, List[Atom]]:
        """Find atoms that occur frequently"""
        atom_groups = defaultdict(list)
        
        for atom in self.atomspace.atoms.values():
            # Group by type and subtype
            key = f"{atom.__class__.__name__}:{atom.subtype}"
            atom_groups[key].append(atom)
        
        return atom_groups
    
    def _create_single_atom_pattern(self, atom_type: str, atoms: List[Atom]) -> SubgraphPattern:
        """Create a pattern from a single atom type"""
        # Use the first atom as template
        template_atom = atoms[0]
        
        pattern = SubgraphPattern(
            id=f"pattern_{atom_type}_{len(self.discovered_patterns)}",
            atoms=[template_atom],
            support=len(atoms)
        )
        
        # Create matches for all atoms of this type
        for atom in atoms:
            match = SubgraphMatch(
                pattern_id=pattern.id,
                atom_mappings={template_atom.id: atom.id}
            )
            pattern.matches.append(match)
        
        return pattern
    
    def _extend_pattern(self, pattern: SubgraphPattern) -> List[SubgraphPattern]:
        """Extend a pattern by adding connected atoms"""
        extensions = []
        
        # For each match of the current pattern
        for match in pattern.matches:
            # Find atoms connected to the matched atoms
            connected_atoms = set()
            
            for template_atom_id, actual_atom_id in match.atom_mappings.items():
                actual_atom = self.atomspace.get_atom(actual_atom_id)
                if actual_atom:
                    # Get incoming and outgoing connections
                    connected_atoms.update(self._get_connected_atoms(actual_atom))
            
            # Try to create extended patterns
            for connected_atom in connected_atoms:
                extended_pattern = self._try_extend_pattern_with_atom(pattern, connected_atom)
                if extended_pattern:
                    extensions.append(extended_pattern)
        
        # Merge duplicate patterns and calculate support
        return self._merge_duplicate_patterns(extensions)
    
    def _get_connected_atoms(self, atom: Atom) -> List[Atom]:
        """Get all atoms connected to the given atom"""
        connected = []
        
        # If it's a link, get its outgoing atoms
        if isinstance(atom, Link):
            connected.extend(self.atomspace.get_outgoing_atoms(atom))
        
        # Get incoming links
        incoming_links = self.atomspace.get_incoming_atoms(atom)
        connected.extend(incoming_links)
        
        # For incoming links, also get their other outgoing atoms
        for link in incoming_links:
            if isinstance(link, Link):
                outgoing = self.atomspace.get_outgoing_atoms(link)
                for out_atom in outgoing:
                    if out_atom.id != atom.id:
                        connected.append(out_atom)
        
        return connected
    
    def _try_extend_pattern_with_atom(self, pattern: SubgraphPattern, new_atom: Atom) -> Optional[SubgraphPattern]:
        """Try to extend pattern by adding a new atom"""
        # Simple extension: add the new atom to the pattern
        # In a full implementation, this would check for structural consistency
        
        extended_atoms = pattern.atoms + [new_atom]
        
        extended_pattern = SubgraphPattern(
            id=f"extended_{pattern.id}_{new_atom.id}",
            atoms=extended_atoms,
            support=1  # Will be calculated properly later
        )
        
        return extended_pattern
    
    def _merge_duplicate_patterns(self, patterns: List[SubgraphPattern]) -> List[SubgraphPattern]:
        """Merge patterns that are structurally equivalent"""
        # Simplified: just remove exact duplicates
        # A full implementation would use graph isomorphism
        
        unique_patterns = {}
        
        for pattern in patterns:
            # Create a signature based on atom types and structure
            signature = self._pattern_signature(pattern)
            
            if signature not in unique_patterns:
                unique_patterns[signature] = pattern
            else:
                # Merge support
                unique_patterns[signature].support += 1
        
        return list(unique_patterns.values())
    
    def _pattern_signature(self, pattern: SubgraphPattern) -> str:
        """Create a signature for pattern matching"""
        # Simple signature based on atom types and subtypes
        signatures = []
        for atom in pattern.atoms:
            signatures.append(f"{atom.__class__.__name__}:{atom.subtype}")
        
        return "|".join(sorted(signatures))
    
    def _calculate_pattern_metrics(self, pattern: SubgraphPattern):
        """Calculate confidence, lift, MDL gain, and attention score"""
        # Confidence: How often the pattern predicts target relationships
        pattern.confidence = self._calculate_confidence(pattern)
        
        # Lift: How much better than random
        pattern.lift = self._calculate_lift(pattern)
        
        # MDL Gain: Compression benefit
        pattern.mdl_gain = self._calculate_mdl_gain(pattern)
        
        # Attention score: Weighted by attention values
        if self.use_attention:
            pattern.attention_score = self._calculate_attention_score(pattern)
    
    def _calculate_confidence(self, pattern: SubgraphPattern) -> float:
        """Calculate predictive confidence of pattern"""
        if not pattern.matches:
            return 0.0
        
        # Simple confidence: ratio of matches that have complete structure
        complete_matches = 0
        for match in pattern.matches:
            # Check if all atoms in the pattern have corresponding matches
            if len(match.atom_mappings) == len(pattern.atoms):
                complete_matches += 1
        
        return complete_matches / len(pattern.matches)
    
    def _calculate_lift(self, pattern: SubgraphPattern) -> float:
        """Calculate lift score (vs random baseline)"""
        if pattern.support == 0:
            return 0.0
        
        total_atoms = len(self.atomspace.atoms)
        if total_atoms == 0:
            return 0.0
        
        # Expected support if random
        pattern_size = len(pattern.atoms)
        expected_random = (1.0 / total_atoms) ** (pattern_size - 1)
        actual_frequency = pattern.support / total_atoms
        
        return actual_frequency / expected_random if expected_random > 0 else 1.0
    
    def _calculate_mdl_gain(self, pattern: SubgraphPattern) -> float:
        """Calculate MDL (Minimum Description Length) gain"""
        # Simplified MDL: bits saved by using pattern vs explicit encoding
        pattern_size_bits = len(pattern.atoms) * 8  # Rough atom encoding cost
        
        # Bits saved by replacing matches with pattern reference
        matches_size_bits = pattern.support * pattern_size_bits
        pattern_ref_bits = pattern.support * 4  # Reference to pattern
        
        return matches_size_bits - (pattern_size_bits + pattern_ref_bits)
    
    def _calculate_attention_score(self, pattern: SubgraphPattern) -> float:
        """Calculate attention-weighted score"""
        total_attention = 0.0
        count = 0
        
        for match in pattern.matches:
            for actual_atom_id in match.atom_mappings.values():
                atom = self.atomspace.get_atom(actual_atom_id)
                if atom:
                    # Weight by short-term importance (STI)
                    total_attention += atom.av.sti
                    count += 1
        
        return total_attention / count if count > 0 else 0.0
    
    def _pattern_interestingness(self, pattern: SubgraphPattern) -> float:
        """Combined interestingness score for ranking"""
        # Weighted combination of metrics
        score = (
            0.3 * pattern.support +
            0.25 * pattern.confidence +
            0.2 * pattern.lift +
            0.15 * pattern.mdl_gain +
            0.1 * pattern.attention_score
        )
        return score
    
    def find_pattern_matches(self, pattern: SubgraphPattern) -> List[SubgraphMatch]:
        """Find all matches of a given pattern in the atomspace"""
        matches = []
        
        # Simple pattern matching - in practice would use more sophisticated algorithms
        for atom in self.atomspace.atoms.values():
            if self._atom_matches_pattern(atom, pattern.atoms[0]):
                match = SubgraphMatch(
                    pattern_id=pattern.id,
                    atom_mappings={pattern.atoms[0].id: atom.id}
                )
                matches.append(match)
        
        return matches
    
    def _atom_matches_pattern(self, atom: Atom, pattern_atom: Atom) -> bool:
        """Check if an atom matches a pattern atom"""
        # Match by type and subtype
        return (atom.__class__ == pattern_atom.__class__ and 
                atom.subtype == pattern_atom.subtype)
    
    def get_top_patterns(self, n: int = 10) -> List[SubgraphPattern]:
        """Get top N most interesting patterns"""
        return self.discovered_patterns[:n]
    
    def save_patterns(self, filename: str):
        """Save discovered patterns to JSON file"""
        import json
        
        patterns_data = {
            "patterns": [pattern.to_dict() for pattern in self.discovered_patterns],
            "mining_params": {
                "min_support": self.min_support,
                "min_confidence": self.min_confidence,
                "use_attention": self.use_attention
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(patterns_data, f, indent=2)
    
    def load_patterns(self, filename: str):
        """Load patterns from JSON file"""
        import json
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.discovered_patterns = []
        for pattern_data in data.get("patterns", []):
            # Reconstruct pattern from data
            atoms = []
            for atom_data in pattern_data["atoms"]:
                atom = self.atomspace._atom_from_dict(atom_data)
                atoms.append(atom)
            
            pattern = SubgraphPattern(
                id=pattern_data["id"],
                atoms=atoms,
                support=pattern_data.get("support", 0),
                confidence=pattern_data.get("confidence", 0.0),
                lift=pattern_data.get("lift", 0.0),
                mdl_gain=pattern_data.get("mdl_gain", 0.0),
                attention_score=pattern_data.get("attention_score", 0.0)
            )
            
            # Reconstruct matches
            for match_data in pattern_data.get("matches", []):
                match = SubgraphMatch(
                    pattern_id=match_data["pattern_id"],
                    atom_mappings=match_data["atom_mappings"],
                    support_score=match_data.get("support_score", 0.0)
                )
                pattern.matches.append(match)
            
            self.discovered_patterns.append(pattern)
    
    def print_patterns(self, top_n: int = 5):
        """Print discovered patterns in human-readable format"""
        print(f"=== Top {top_n} Discovered Patterns ===")
        
        for i, pattern in enumerate(self.get_top_patterns(top_n)):
            print(f"\nPattern {i+1}: {pattern.id}")
            print(f"  Atoms: {len(pattern.atoms)}")
            for atom in pattern.atoms:
                print(f"    {atom}")
            print(f"  Support: {pattern.support}")
            print(f"  Confidence: {pattern.confidence:.3f}")
            print(f"  Lift: {pattern.lift:.3f}")
            print(f"  MDL Gain: {pattern.mdl_gain:.1f} bits")
            if self.use_attention:
                print(f"  Attention Score: {pattern.attention_score:.3f}")
            print(f"  Matches: {len(pattern.matches)}")
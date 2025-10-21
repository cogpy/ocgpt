"""
OpenCog v1 Model Implementations

This module provides standalone implementations of OpenCog concepts
based on the v1 documentation and schemas, without requiring the full OpenCog stack.
"""

from .atomspace import AtomSpace, Atom, Node, Link, TruthValue, AttentionValue
from .pln import PLNReasoner, InferenceStep
from .moses import Program, Expression, MOSESEvolver
from .pattern_mining import PatternMiner, SubgraphPattern

__all__ = [
    'AtomSpace', 'Atom', 'Node', 'Link', 'TruthValue', 'AttentionValue',
    'PLNReasoner', 'InferenceStep',
    'Program', 'Expression', 'MOSESEvolver',
    'PatternMiner', 'SubgraphPattern'
]

__version__ = '0.1.0'
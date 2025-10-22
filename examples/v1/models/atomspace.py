"""
AtomSpace Model Implementation (v1)

Standalone implementation based on cards/opencog/atomspace-basics.md
and schemas/atom.json
"""

import json
import uuid
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict


@dataclass
class TruthValue:
    """Simple Truth Value (s, c) implementation"""
    s: float  # strength [0,1]
    c: float  # confidence [0,1]
    
    def __post_init__(self):
        self.s = max(0.0, min(1.0, self.s))
        self.c = max(0.0, min(1.0, self.c))
    
    def __str__(self):
        return f"TV(s={self.s:.3f}, c={self.c:.3f})"
    
    def to_dict(self):
        return {"s": self.s, "c": self.c}


@dataclass
class AttentionValue:
    """Attention Value (sti, lti) implementation"""
    sti: float = 0.0  # short-term importance [0,1]
    lti: float = 0.0  # long-term importance [0,1]
    
    def __post_init__(self):
        self.sti = max(0.0, min(1.0, self.sti))
        self.lti = max(0.0, min(1.0, self.lti))
    
    def __str__(self):
        return f"AV(sti={self.sti:.3f}, lti={self.lti:.3f})"
    
    def to_dict(self):
        return {"sti": self.sti, "lti": self.lti}


class Atom:
    """Base Atom class following schema/atom.json"""
    
    def __init__(self, id: str = None, subtype: str = "", name: str = "", 
                 tv: TruthValue = None, av: AttentionValue = None, meta: dict = None):
        self.id = id or str(uuid.uuid4())
        self.subtype = subtype
        self.name = name
        self.tv = tv or TruthValue(1.0, 0.0)
        self.av = av or AttentionValue()
        self.meta = meta or {}
    
    def to_dict(self):
        """Export to JSON-compatible dict following schema"""
        result = {
            "id": self.id,
            "type": self.__class__.__name__,
            "subtype": self.subtype,
            "tv": self.tv.to_dict(),
            "av": self.av.to_dict()
        }
        if self.name:
            result["name"] = self.name
        if self.meta:
            result["meta"] = self.meta
        return result
    
    def __str__(self):
        return f"{self.subtype}({self.name or self.id}) {self.tv}"
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Atom) and self.id == other.id


class Node(Atom):
    """Node atom - atomic symbol with subtype"""
    
    def __init__(self, name: str, subtype: str = "ConceptNode", **kwargs):
        super().__init__(name=name, subtype=subtype, **kwargs)
        if not self.id.startswith('n:'):
            self.id = f"n:{self.id}"


class Link(Atom):
    """Link atom - hyperedge with outgoing atoms"""
    
    def __init__(self, outgoing: List[Union[Atom, str]], subtype: str = "Link", **kwargs):
        super().__init__(subtype=subtype, **kwargs)
        if not self.id.startswith('l:'):
            self.id = f"l:{self.id}"
        
        # Store outgoing as atom IDs for serialization
        self.outgoing_ids = []
        for atom in outgoing:
            if isinstance(atom, str):
                self.outgoing_ids.append(atom)
            elif isinstance(atom, Atom):
                self.outgoing_ids.append(atom.id)
            else:
                raise ValueError(f"Invalid outgoing atom type: {type(atom)}")
    
    def to_dict(self):
        result = super().to_dict()
        result["out"] = self.outgoing_ids
        return result
    
    def __str__(self):
        return f"{self.subtype}({', '.join(self.outgoing_ids)}) {self.tv}"


class ConceptNode(Node):
    """Concept node for representing concepts"""
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, subtype="ConceptNode", **kwargs)


class PredicateNode(Node):
    """Predicate node for representing relations/predicates"""
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, subtype="PredicateNode", **kwargs)


class NumberNode(Node):
    """Number node for representing numeric values"""
    def __init__(self, value: Union[int, float], **kwargs):
        name = str(value)
        super().__init__(name=name, subtype="NumberNode", **kwargs)
        self.value = value


class InheritanceLink(Link):
    """Inheritance link: A inherits from B"""
    def __init__(self, source: Union[Atom, str], target: Union[Atom, str], **kwargs):
        super().__init__([source, target], subtype="InheritanceLink", **kwargs)


class ImplicationLink(Link):
    """Implication link: A implies B"""
    def __init__(self, antecedent: Union[Atom, str], consequent: Union[Atom, str], **kwargs):
        super().__init__([antecedent, consequent], subtype="ImplicationLink", **kwargs)


class EvaluationLink(Link):
    """Evaluation link: Predicate(Args...)"""
    def __init__(self, predicate: Union[Atom, str], arguments: Union[Atom, str], **kwargs):
        super().__init__([predicate, arguments], subtype="EvaluationLink", **kwargs)


class ListLink(Link):
    """List link: ordered list of atoms"""
    def __init__(self, items: List[Union[Atom, str]], **kwargs):
        super().__init__(items, subtype="ListLink", **kwargs)


class AtomSpace:
    """AtomSpace container and operations"""
    
    def __init__(self):
        self.atoms: Dict[str, Atom] = {}
        self.index_by_type: Dict[str, List[str]] = {}
        self.index_by_name: Dict[str, List[str]] = {}
    
    def add_atom(self, atom: Atom) -> Atom:
        """Add atom to atomspace"""
        self.atoms[atom.id] = atom
        
        # Update type index
        atom_type = f"{atom.__class__.__name__}:{atom.subtype}"
        if atom_type not in self.index_by_type:
            self.index_by_type[atom_type] = []
        self.index_by_type[atom_type].append(atom.id)
        
        # Update name index (for nodes with names)
        if hasattr(atom, 'name') and atom.name:
            if atom.name not in self.index_by_name:
                self.index_by_name[atom.name] = []
            self.index_by_name[atom.name].append(atom.id)
        
        return atom
    
    def get_atom(self, id: str) -> Optional[Atom]:
        """Get atom by ID"""
        return self.atoms.get(id)
    
    def get_atoms_by_type(self, atom_type: str, subtype: str = None) -> List[Atom]:
        """Get all atoms of given type"""
        if subtype:
            key = f"{atom_type}:{subtype}"
        else:
            key = atom_type
        
        atom_ids = self.index_by_type.get(key, [])
        return [self.atoms[aid] for aid in atom_ids]
    
    def get_atoms_by_name(self, name: str) -> List[Atom]:
        """Get all atoms with given name"""
        atom_ids = self.index_by_name.get(name, [])
        return [self.atoms[aid] for aid in atom_ids]
    
    def get_outgoing_atoms(self, link: Link) -> List[Atom]:
        """Get the actual outgoing atoms for a link"""
        result = []
        for atom_id in link.outgoing_ids:
            atom = self.get_atom(atom_id)
            if atom:
                result.append(atom)
        return result
    
    def get_incoming_atoms(self, atom: Atom) -> List[Link]:
        """Get all links that have this atom in their outgoing set"""
        result = []
        for other_atom in self.atoms.values():
            if isinstance(other_atom, Link) and atom.id in other_atom.outgoing_ids:
                result.append(other_atom)
        return result
    
    def size(self) -> int:
        """Return number of atoms in atomspace"""
        return len(self.atoms)
    
    def clear(self):
        """Clear all atoms"""
        self.atoms.clear()
        self.index_by_type.clear()
        self.index_by_name.clear()
    
    def to_dict(self) -> dict:
        """Export atomspace to JSON-compatible dict"""
        return {
            "atoms": [atom.to_dict() for atom in self.atoms.values()],
            "size": self.size()
        }
    
    def from_dict(self, data: dict):
        """Import atomspace from dict"""
        self.clear()
        for atom_data in data.get("atoms", []):
            atom = self._atom_from_dict(atom_data)
            self.add_atom(atom)
    
    def _atom_from_dict(self, data: dict) -> Atom:
        """Create atom from dict representation"""
        atom_type = data["type"]
        subtype = data["subtype"]
        
        # Reconstruct truth and attention values
        tv_data = data.get("tv", {"s": 1.0, "c": 0.0})
        tv = TruthValue(tv_data["s"], tv_data["c"])
        
        av_data = data.get("av", {"sti": 0.0, "lti": 0.0})
        av = AttentionValue(av_data["sti"], av_data["lti"])
        
        # Create appropriate atom type
        if atom_type == "Node":
            atom = Node(
                name=data.get("name", ""),
                subtype=subtype,
                id=data["id"],
                tv=tv,
                av=av,
                meta=data.get("meta", {})
            )
        elif atom_type == "Link":
            atom = Link(
                outgoing=data.get("out", []),
                subtype=subtype,
                id=data["id"],
                tv=tv,
                av=av,
                meta=data.get("meta", {})
            )
        else:
            # Generic atom
            atom = Atom(
                id=data["id"],
                subtype=subtype,
                name=data.get("name", ""),
                tv=tv,
                av=av,
                meta=data.get("meta", {})
            )
        
        return atom
    
    def save_json(self, filename: str):
        """Save atomspace to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def load_json(self, filename: str):
        """Load atomspace from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        self.from_dict(data)
    
    def __len__(self):
        return self.size()
    
    def __str__(self):
        return f"AtomSpace(size={self.size()})"
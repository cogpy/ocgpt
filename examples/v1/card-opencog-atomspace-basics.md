## cards/opencog/atomspace-basics.md **Title:** AtomSpace Basics **Version:** 0.1 **Purpose:** Minimal, simulation-ready definitions for Atoms, Links, and truth/attention values. ### Atom Types * **Node:** An atomic symbol with a subtype (e.g., ConceptNode, PredicateNode, NumberNode). * **Link:** A hyperedge with ordered or unordered outgoing set of Atoms (e.g., InheritanceLink, ImplicationLink, EvaluationLink). ### Identity & Addressing * Each Atom has a stable id (string or UUID). Links reference the ids of their outgoing Atoms. ### Truth Values (STV) * **Structure:** (strength s ∈ [0,1], confidence c ∈ [0,1]). * **Interpretation:** s approximates probability/degree; c reflects evidence volume/reliability. * **Update (informal):** Combining independent evidence should raise c; contradictory evidence shifts s toward observed frequencies. ### Attention Values (AV) *(optional)* * **Short-term importance (sti):** [0,1] * **Long-term importance (lti):** [0,1] * Used to bias search, inference, and pattern mining. ### Minimal JSON Shape (see schemas/atom.json)
json
{
  "id": "a:cat",
  "type": "Node",
  "subtype": "ConceptNode",
  "name": "Cat",
  "tv": { "s": 0.9, "c": 0.6 },
  "av": { "sti": 0.4, "lti": 0.2 }
}
### Example Links
json
{
  "id": "l:cat-mammal",
  "type": "Link",
  "subtype": "InheritanceLink",
  "out": ["a:cat", "a:mammal"],
  "tv": { "s": 0.95, "c": 0.7 }
}
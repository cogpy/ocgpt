#!/usr/bin/env python3
"""
AtomSpace Visualizer Tool
Creates visual representations of OpenCog AtomSpace contents
"""

import json
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Set, Tuple
import argparse

class AtomSpaceVisualizer:
    """Visualize AtomSpace graphs and relationships"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_colors = {}
        self.node_sizes = {}
        self.edge_labels = {}
        
    def add_atom(self, atom_id: str, atom_type: str, name: str = None, 
                 truth_value: Dict = None, attention_value: Dict = None):
        """Add an atom to the visualization graph"""
        
        # Determine node color based on type
        color_map = {
            'ConceptNode': '#FF6B6B',      # Red
            'PredicateNode': '#4ECDC4',    # Teal  
            'VariableNode': '#45B7D1',     # Blue
            'NumberNode': '#96CEB4',       # Green
            'SchemaNode': '#FFEAA7',       # Yellow
            'ListLink': '#DDA0DD',         # Plum
            'InheritanceLink': '#98D8C8',  # Mint
            'EvaluationLink': '#F7DC6F',   # Light Yellow
            'ImplicationLink': '#BB8FCE',  # Light Purple
            'SimilarityLink': '#85C1E9'    # Light Blue
        }
        
        color = color_map.get(atom_type, '#CCCCCC')  # Default gray
        self.node_colors[atom_id] = color
        
        # Determine node size based on attention value
        size = 300  # Default size
        if attention_value and 'sti' in attention_value:
            size = max(100, min(1000, 300 + attention_value['sti'] * 10))
        self.node_sizes[atom_id] = size
        
        # Add node with attributes
        label = name if name else atom_id
        if truth_value:
            tv_str = f"({truth_value.get('strength', 0):.2f}, {truth_value.get('confidence', 0):.2f})"
            label += f"\nTV: {tv_str}"
            
        self.graph.add_node(atom_id, 
                           type=atom_type,
                           name=name,
                           label=label,
                           truth_value=truth_value,
                           attention_value=attention_value)
    
    def add_link(self, link_id: str, link_type: str, outgoing: List[str], 
                 truth_value: Dict = None):
        """Add a link between atoms"""
        
        # Add the link as a node first
        self.add_atom(link_id, link_type, truth_value=truth_value)
        
        # Connect link to its outgoing atoms
        for i, target_id in enumerate(outgoing):
            self.graph.add_edge(link_id, target_id, order=i)
            self.edge_labels[(link_id, target_id)] = str(i)
    
    def load_from_json(self, json_data: Dict):
        """Load AtomSpace from JSON representation"""
        
        if 'atoms' not in json_data:
            raise ValueError("JSON must contain 'atoms' field")
            
        for atom in json_data['atoms']:
            atom_id = atom.get('id', f"{atom['type']}_{id(atom)}")
            
            if atom['type'] == 'Node':
                self.add_atom(
                    atom_id, 
                    atom.get('node_type', 'Node'),
                    atom.get('name'),
                    atom.get('truth_value'),
                    atom.get('attention_value')
                )
            elif atom['type'] == 'Link':
                # First ensure outgoing atoms exist
                outgoing = atom.get('outgoing', [])
                for out_atom in outgoing:
                    if isinstance(out_atom, dict):
                        out_id = out_atom.get('id', f"{out_atom['type']}_{id(out_atom)}")
                        if out_atom['type'] == 'Node':
                            self.add_atom(
                                out_id,
                                out_atom.get('node_type', 'Node'), 
                                out_atom.get('name'),
                                out_atom.get('truth_value'),
                                out_atom.get('attention_value')
                            )
                
                # Then add the link
                outgoing_ids = [
                    out.get('id', f"{out['type']}_{id(out)}") if isinstance(out, dict) else out
                    for out in outgoing
                ]
                self.add_link(
                    atom_id,
                    atom.get('link_type', 'Link'),
                    outgoing_ids,
                    atom.get('truth_value')
                )
    
    def visualize(self, title: str = "AtomSpace Visualization", 
                  figsize: Tuple[int, int] = (12, 8),
                  layout: str = 'spring',
                  show_labels: bool = True,
                  show_truth_values: bool = True,
                  save_path: str = None):
        """Create and display the visualization"""
        
        if len(self.graph.nodes()) == 0:
            print("No atoms to visualize")
            return
            
        plt.figure(figsize=figsize)
        
        # Choose layout algorithm
        if layout == 'spring':
            pos = nx.spring_layout(self.graph, k=2, iterations=50)
        elif layout == 'circular':
            pos = nx.circular_layout(self.graph)
        elif layout == 'hierarchical':
            pos = nx.nx_agraph.graphviz_layout(self.graph, prog='dot')
        else:
            pos = nx.spring_layout(self.graph)
        
        # Draw nodes
        node_colors_list = [self.node_colors.get(node, '#CCCCCC') for node in self.graph.nodes()]
        node_sizes_list = [self.node_sizes.get(node, 300) for node in self.graph.nodes()]
        
        nx.draw_networkx_nodes(self.graph, pos, 
                              node_color=node_colors_list,
                              node_size=node_sizes_list,
                              alpha=0.8)
        
        # Draw edges
        nx.draw_networkx_edges(self.graph, pos,
                              edge_color='gray',
                              arrows=True,
                              arrowsize=20,
                              alpha=0.6)
        
        # Draw labels
        if show_labels:
            labels = {}
            for node in self.graph.nodes():
                node_data = self.graph.nodes[node]
                label = node_data.get('name', node)
                
                if show_truth_values and node_data.get('truth_value'):
                    tv = node_data['truth_value']
                    tv_str = f"({tv.get('strength', 0):.2f},{tv.get('confidence', 0):.2f})"
                    label += f"\n{tv_str}"
                    
                labels[node] = label
                
            nx.draw_networkx_labels(self.graph, pos, labels, font_size=8)
        
        # Draw edge labels (for link order)
        if self.edge_labels:
            nx.draw_networkx_edge_labels(self.graph, pos, self.edge_labels, font_size=6)
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to {save_path}")
        
        plt.show()
    
    def get_statistics(self) -> Dict:
        """Get statistics about the AtomSpace graph"""
        
        stats = {
            'total_atoms': len(self.graph.nodes()),
            'total_links': len(self.graph.edges()),
            'atom_types': {},
            'connectivity': {
                'connected_components': nx.number_weakly_connected_components(self.graph),
                'diameter': None,
                'average_path_length': None
            }
        }
        
        # Count atom types
        for node in self.graph.nodes():
            atom_type = self.graph.nodes[node].get('type', 'Unknown')
            stats['atom_types'][atom_type] = stats['atom_types'].get(atom_type, 0) + 1
        
        # Graph connectivity metrics (if connected)
        if nx.is_weakly_connected(self.graph):
            try:
                stats['connectivity']['diameter'] = nx.diameter(self.graph.to_undirected())
                stats['connectivity']['average_path_length'] = nx.average_shortest_path_length(self.graph.to_undirected())
            except:
                pass  # Handle cases where metrics can't be computed
        
        return stats
    
    def print_statistics(self):
        """Print visualization statistics"""
        
        stats = self.get_statistics()
        
        print("AtomSpace Visualization Statistics:")
        print(f"  Total Atoms: {stats['total_atoms']}")
        print(f"  Total Links: {stats['total_links']}")
        print(f"  Connected Components: {stats['connectivity']['connected_components']}")
        
        if stats['connectivity']['diameter']:
            print(f"  Graph Diameter: {stats['connectivity']['diameter']}")
        if stats['connectivity']['average_path_length']:
            print(f"  Average Path Length: {stats['connectivity']['average_path_length']:.2f}")
            
        print("  Atom Type Distribution:")
        for atom_type, count in stats['atom_types'].items():
            print(f"    {atom_type}: {count}")

def main():
    """Command-line interface for the visualizer"""
    
    parser = argparse.ArgumentParser(description='Visualize OpenCog AtomSpace')
    parser.add_argument('--input', '-i', type=str, required=True,
                       help='Input JSON file containing AtomSpace data')
    parser.add_argument('--output', '-o', type=str, 
                       help='Output image file path')
    parser.add_argument('--layout', '-l', type=str, default='spring',
                       choices=['spring', 'circular', 'hierarchical'],
                       help='Graph layout algorithm')
    parser.add_argument('--title', '-t', type=str, default='AtomSpace Visualization',
                       help='Visualization title')
    parser.add_argument('--no-labels', action='store_true',
                       help='Hide node labels')
    parser.add_argument('--no-truth-values', action='store_true', 
                       help='Hide truth values in labels')
    
    args = parser.parse_args()
    
    # Load data
    try:
        with open(args.input, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        return
    
    # Create visualization
    visualizer = AtomSpaceVisualizer()
    visualizer.load_from_json(data)
    visualizer.print_statistics()
    
    visualizer.visualize(
        title=args.title,
        layout=args.layout,
        show_labels=not args.no_labels,
        show_truth_values=not args.no_truth_values,
        save_path=args.output
    )

if __name__ == "__main__":
    main()
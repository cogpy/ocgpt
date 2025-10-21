# OpenCog-GPT: GPT Builder Process Model

This repository demonstrates the complete process of creating an OpenCog expert GPT using ChatGPT's GPT Builder tool. It includes the conversation thread, gizmo template configurations, and the specialized OpenCog-GPT implementation.

## Repository Structure

```
ocgpt/
├── gpt-builder-session/     # ChatGPT Builder conversation process
├── gizmo-template/          # Generic GPT template structure  
├── opencog-gpt/            # OpenCog-specific GPT implementation
├── README.md               # This file
└── LICENSE                 # AGPL-3.0 License
```

## 📁 Folder Breakdown

### `gpt-builder-session/`
Documents the actual ChatGPT GPT Builder conversation thread that led to creating the OpenCog Expert GPT.

```
conversation-thread/
├── 01-initial-request.md      # Initial user request to create OpenCog GPT
├── 02-clarifications.md       # Builder questions and user responses  
└── 03-final-configuration.md  # Final GPT setup and completion

iterations/                    # Different versions during development
screenshots/                   # Visual documentation of the builder process
```

### `gizmo-template/`
Generic template structure for GPT creation that can be adapted for other domains.

```
config/
├── gpt-config.json           # GPT configuration parameters

instructions/
├── system-prompt.md          # Main system instructions template

capabilities/
├── web-browsing.md          # Web browsing capability documentation
└── code-interpreter.md      # Code interpreter capability documentation

tools/                       # Additional tools and integrations
knowledge-base/             # Template knowledge organization
```

### `opencog-gpt/`
The complete OpenCog Expert GPT implementation with domain-specific content.

```
config/
├── model-parameters.json    # OpenCog GPT specific parameters

knowledge-base/
├── atomspace-fundamentals.md   # Core AtomSpace concepts
├── pln-reasoning.md           # PLN reasoning knowledge
└── [additional knowledge files]

examples/
├── basic-atomspace-usage.py   # Code examples for users
├── pln-reasoning-example.py   # PLN demonstration code
└── [more examples]

schemas/
├── atomspace-schema.json     # JSON schemas for validation

tools/
├── atomspace-visualizer.py   # Visualization utilities
└── [additional tools]

interactions/
├── conversation-examples.md   # Example conversations with the GPT
└── [interaction patterns]
```

## 🚀 Getting Started

### Using the OpenCog Expert GPT
1. The GPT is designed to help with OpenCog cognitive architecture development
2. Ask questions about AtomSpace, PLN reasoning, MOSES, pattern mining, etc.
3. Request code examples, architectural guidance, or troubleshooting help

### Adapting This Template
1. Fork this repository
2. Modify the `gizmo-template/` structure for your domain
3. Replace OpenCog content with your specialized knowledge
4. Follow the same builder conversation pattern
5. Document your GPT creation process

## 🎯 OpenCog Expert GPT Features

- **Comprehensive Coverage**: AtomSpace, PLN, MOSES, pattern mining, language processing
- **Multiple Expertise Levels**: Adapts explanations for researchers, developers, students  
- **Practical Code Examples**: Working examples in Python, Scheme, and C++
- **Architecture Guidance**: Help designing cognitive architectures
- **Troubleshooting Support**: Performance optimization and debugging assistance
- **Current Information**: Web browsing for latest OpenCog developments

## 📚 Knowledge Domains

### Core OpenCog Components
- **AtomSpace**: Hypergraph knowledge representation
- **PLN**: Probabilistic logic networks and uncertain reasoning
- **MOSES**: Meta-optimizing semantic evolutionary search
- **Pattern Mining**: Frequent pattern extraction and learning
- **Natural Language Processing**: Language understanding and generation

### Related AI Fields
- Cognitive architectures and AGI theory
- Neurosymbolic AI approaches  
- Machine learning integration
- Symbolic reasoning systems
- Multi-agent cognitive systems

## 🛠️ Tools and Utilities

### AtomSpace Visualizer
```bash
python opencog-gpt/tools/atomspace-visualizer.py \
    --input your_atomspace.json \
    --output visualization.png \
    --layout spring
```

### Code Examples
Run the provided examples to learn OpenCog concepts:
```bash
python opencog-gpt/examples/basic-atomspace-usage.py
python opencog-gpt/examples/pln-reasoning-example.py
```

## 📖 Documentation

- **Conversation Examples**: See `opencog-gpt/interactions/` for typical user interactions
- **Knowledge Base**: Comprehensive documentation in `opencog-gpt/knowledge-base/`
- **API Schemas**: JSON schemas for validation in `opencog-gpt/schemas/`
- **Builder Process**: Full creation process documented in `gpt-builder-session/`

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional code examples and tutorials
- More comprehensive knowledge base content
- Enhanced visualization tools
- Extended conversation examples
- Performance optimization guides

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). See [LICENSE](LICENSE) file for details.

## 🔗 Related Resources

- [OpenCog Official Repository](https://github.com/opencog/opencog)
- [OpenCog Documentation](https://wiki.opencog.org/)
- [AtomSpace Tutorial](https://wiki.opencog.org/w/AtomSpace)
- [PLN Handbook](https://wiki.opencog.org/w/PLNHandbook)

---

*This repository serves as both a working OpenCog expert system and a template for creating domain-specific GPTs using the ChatGPT Builder tool.*
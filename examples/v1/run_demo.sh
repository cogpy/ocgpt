#!/bin/bash

# OpenCog v1 Model Demo Runner
# Runs the complete real_example_v1.py demonstration

echo "OpenCog v1 Model Implementation Demo"
echo "===================================="
echo ""

# Check if we're in the right directory
if [ ! -f "real_example_v1.py" ]; then
    echo "Error: Please run this script from the examples/v1 directory"
    echo "Usage: cd examples/v1 && ./run_demo.sh"
    exit 1
fi

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is required but not found"
    exit 1
fi

echo ""
echo "Running model tests..."
echo "----------------------"
python3 test_models.py
if [ $? -ne 0 ]; then
    echo "Error: Model tests failed. Please check the implementation."
    exit 1
fi

echo ""
echo "All tests passed! Running full demonstration..."
echo "----------------------------------------------"
echo ""

python3 real_example_v1.py

if [ $? -eq 0 ]; then
    echo ""
    echo "Demo completed successfully!"
    echo ""
    echo "Generated files:"
    if [ -f "v1_example_results.json" ]; then
        echo "  - v1_example_results.json ($(wc -c < v1_example_results.json) bytes)"
    fi
    echo ""
    echo "Next steps:"
    echo "  1. Examine the generated JSON file to see the knowledge representation"
    echo "  2. Modify real_example_v1.py to experiment with different scenarios"
    echo "  3. Read README.md for detailed documentation"
    echo "  4. Explore the models/ directory for implementation details"
else
    echo "Demo failed with exit code $?"
    exit 1
fi
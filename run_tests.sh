#!/bin/bash

# Step 1: Activate the virtual environment
source venv/Scripts/activate

# Step 2: Execute the test suite
pytest test_app.py -v

# Step 3: Return exit code based on test result
if [ $? -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed!"
    exit 1
fi
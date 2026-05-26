# Clone / navigate to the tool directory
cd margo-linkml-to-openapi

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install the tool
pip install -e ".[dev]"

linkml-to-openapi <template.yaml> <output.yaml>

# All tests
pytest tests/

# With coverage
pytest --cov=src tests/

# Specific test file
pytest tests/test_converter.py -v
pytest tests/test_composition.py -v



# Install
pip install -e ".[dev]"

# Run
linkml-to-openapi \
  spec/openapi/workload-management-api.yaml \
  spec/openapi/workload-management-api.generated.yaml

# With debug output
linkml-to-openapi -v \
  spec/openapi/workload-management-api.yaml \
  spec/openapi/workload-management-api.generated.yaml

# Run tests
pytest --cov=src tests/

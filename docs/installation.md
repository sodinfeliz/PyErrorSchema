# Installation Guide

PyErrorSchema can be installed using pip:

```bash
pip install pyerrorschema
```

## Prerequisites

- Python 3.8 or higher
- Pydantic 2.6.4 or higher

## Development Installation

For development, it's recommended to install the package with development dependencies:

1. Clone the repository:
   ```bash
   git clone https://github.com/sodinfeliz/PyErrorSchema.git
   cd PyErrorSchema
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up pre-commit hooks (optional):
   ```bash
   pre-commit install
   ``` 
# Publishing Guide

How to package and publish Storyteller (or your fork) to PyPI.

## Prerequisites

- `pip`
- `build`
- `twine`

## Steps

1.  **Build the Package**:
    ```bash
    python -m build
    ```
    This creates a `dist/` directory with `.tar.gz` and `.whl` files.

2.  **Test Upload (Optional)**:
    Upload to TestPyPI to verify everything looks right.
    ```bash
    python -m twine upload --repository testpypi dist/*
    ```

3.  **Publish to PyPI**:
    ```bash
    python -m twine upload dist/*
    ```

## Installation

Once published, users can install your version via pip:

```bash
pip install ai-storyteller
```

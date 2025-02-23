# tfdoc 

## Overview
tfdoc is a command-line tool designed to parse Terraform (`.tf`) files and extract relevant information about resources and variables. It generates structured Markdown tables, making it easier to analyze and document Terraform configurations.

## Features
- Extracts resource names and attributes from Terraform files
- Supports optional dependency tracking between resources
- Outputs results as Markdown tables
- Simple command-line interface for easy usage

## Installation
### Prerequisites
Ensure you have Python (>=3.7) installed. You can check your Python version using:
```sh
python --version
```

### Installation Instructions
**Note:** `tfdoc` is not available on PyPI. To install it, you need to clone the repository and install it manually.

#### Clone the Repository
```sh
git clone https://github.com/th3r3ald0n/tfdoc.git
cd tfdoc
```

#### Install via `pipx` (Global installation) 

```sh
pipx install .
```
This will make the `tfdoc` command available globally.


#### Install via `pip` with Virtual Environment
It is recommended to use a virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install .
```

## Usage
Once installed, you can use the `tfdoc` command from any directory containing Terraform files.

### Basic Usage
To extract basic information about Terraform resources:
```sh
tfdoc
```

### Extract Specific Attributes
To extract specific attributes from resources (e.g., `type` and `description`):
```sh
tfdoc -l type description
```

### Include Dependency Analysis
To include resource dependencies in the output:
```sh
tfdoc --include-depends
```

### Output
After running `tfdoc`, two output files are generated:
- `tfdoc.md`: Contains a table of resources and selected attributes.
- `tfdoc_vars.md`: Lists Terraform variables with their types and descriptions.

## Limitations
- Only supports Terraform files written in HCL2.
- Does not validate Terraform syntax or state files.
- Requires all `.tf` files to be in the same directory or subdirectories.




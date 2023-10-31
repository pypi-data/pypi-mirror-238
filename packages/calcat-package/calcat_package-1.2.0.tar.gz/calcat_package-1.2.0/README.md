# Calcat Calculator Package

A Python package for basic arithmetic operations. This package provides a `Calculator` class that allows users to perform addition, subtraction, multiplication, division, exponentiation, and extraction of roots. The `Calculator` class also features memory functionality, allowing users to store and manipulate results.

## Installation

You can install the calculator package using `pip`:

```bash
pip install calcat-package==1.0.0
```

You can also explore the package on Google Collab: [Link](https://colab.research.google.com/drive/1l8WPPTghRXa-_CsxxtB_GSfUYFBP1fJf?usp=sharing).

Calcat package on PyPI: [Link](https://pypi.org/project/calcat-package/1.0.0/#files)

## Usage

### Basic Usage

```python
from calcat_package.src.calcat_package_aginsideout.calculator import Calculator

# Create a calculator object
calc = Calculator()

# Perform arithmetic operations
result = calc.add(5, 3)  # Addition: 5 + 3
print(result)  # Output: 8

result = calc.subtract(5, 3)  # Subtraction: 5 - 3
print(result)  # Output: 2

result = calc.multiply(5, 3)  # Multiplication: 5 * 3
print(result)  # Output: 15

result = calc.divide(15, 3)  # Division: 15 / 3
print(result)  # Output: 5

result = calc.power(5, 3)  # Raising to the power: 5 ** 3
print(result)  # Output: 125

result = calc.root(8, 3)  # Root extraction: 3 √ 8
print(result)  # Output: 2

```
### Command-Line Interface (CLI)

You can also use the calculator from the command line. After installation, navigate to the `calcat_package/calculator` directory in your terminal and run:

```bash
python calculator_cli.py
```

This will start an interactive session where you can choose operations and input numbers directly in the terminal.

## Available Operations

- **Addition:** `calc.add(x, y)` - Adds `x` and `y`.
- **Subtraction:** `calc.subtract(x, y)` - Subtracts `y` from `x`.
- **Multiplication:** `calc.multiply(x, y)` - Multiplies `x` and `y`.
- **Division:** `calc.divide(x, y)` - Divides `x` by `y`.
- **Exponentiation:** `calc.power(x, y)` - Raises `x` to the power of `y`.
- **Root Extraction:** `calc.root(x, y)` - Extracts the `y`-th root from `x`.

## Memory Functionality

The `Calculator` class has a built-in memory. The result of the last operation is stored in the memory and can be accessed using `calc.memory`. You can reset the memory to 0 using `calc.reset_memory()`.

```python
# Example of memory usage
result = calc.add(2, 3)  # Result = 5, memory = 5
print(calc.memory)  # Output: 5

calc.reset_memory()  # Reset the memory to 0
print(calc.memory)  # Output: 0
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://choosealicense.com/licenses/mit/) file for details.

For more information, visit the [GitHub repository](https://github.com/TuringCollegeSubmissions/athiel-DWWP.1.5).

Feel free to contribute and report issues!
```
# pyseal

Cryptographically sign your Python functions and classes to detect version control changes

> 💡 **code version controls code**

- 🦀 Built with the [maturin build system](https://www.maturin.rs/) for easy Rust-Python packaging
- 🔗 [PyO3](https://pyo3.rs/v0.27.1/index.html) bindings for seamless Python-Rust integration
- 🔏 [Ed25519](https://docs.rs/ed25519-dalek/latest/ed25519_dalek/) signatures to ensure code integrity and authorship
- 🖥️ [Typer](https://typer.tiangolo.com/) for a clean and user-friendly command line interface

Pyseal helps you maintain code integrity by automatically adding cryptographic signatures to your Python functions and classes. Each function or class receives a unique decorator containing a cryptographic signature that verifies both authorship and integrity, making it easy to detect unauthorized code modifications.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Usage](#usage)
3. [How It Works](#how-it-works)
4. [Model Context Protocol (MCP) Security Use Cases](#model-context-protocol-mcp-security-use-cases)
5. [Contributing](#contributing)
6. [License](#license)

## Getting Started

```shell
pip install pyseal
# or
uv pip install pyseal
```

## Usage

```shell
pyseal init [ENV_FILE]         # Initialize the pyseal tool by generating and saving keys to an ENV_FILE (default: .env)
pyseal decorate <file.py>...   # Add cryptographic decorators to all functions/classes in one or more .py files
pyseal check <file.py>...      # Verify the integrity and validity of pyseal decorators in one or more .py files
pyseal remove <file.py>...     # Remove all pyseal decorators from one or more .py files
pyseal --help                  # Show all available commands and options
```

## How It Works

Pyseal works by automatically injecting cryptographic decorators into your Python functions and classes. Here’s how the process works:

### Step-by-Step Example

Suppose you have a file `fibonacci.py`:

```python
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
```

#### 1. Decorate the file

```shell
pyseal decorate examples/fibonacci.py

Successfully added decorators to 1 file:
  ✓ /path/to/examples/fibonacci.py
```

```python
@pyseal._GnCLaWr9B6TD524JZ3v1CENXmo5Drwfgvc9arVagbghQ6hMH4Aqc8whs3Tf57pkTjsAVNDybviW9XG5Eu3JSP6T()
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
```

#### 2. Check integrity

```shell
pyseal check examples/fibonacci.py

All decorators are valid in 1 file:
✓ /path/to/examples/fibonacci.py: 1 decorators valid
```

#### 3. Tamper with the code (change return 0 to return 42)

```python
@pyseal._GnCLaWr9B6TD524JZ3v1CENXmo5Drwfgvc9arVagbghQ6hMH4Aqc8whs3Tf57pkTjsAVNDybviW9XG5Eu3JSP6T()
def fibonacci(n):
    if n <= 0:
        return 42
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
```

#### 4. Check again

```shell
pyseal check examples/fibonacci.py

1/1 decorators failed verification across 1 file:
  ✗ /path/to/examples/fibonacci.py: 1/1 decorators failed
```

## Model Context Protocol (MCP) Security Use Cases

One use case of Pyseal is to protect MCP servers from upstream attacks by cryptographically signing tool functions and their docstrings. Since LLMs rely on docstrings to understand tool behavior, attackers can inject malicious instructions or create fake tools that mimic legitimate ones. Pyseal's signatures ensure tool authenticity and detect tampering because any modification to code or docstrings breaks the signature and flags compromised tools.

- **Detect Version Control Changes**
  - Automatically detect unauthorized code modifications through cryptographic signatures
  - Each function's decorator contains a signature based on its code and docstring
  - Any mismatch between code and signature is immediately flagged

- **Defense-in-Depth for Source Control**
  - Add an additional security layer to version control systems
  - Complement existing security measures with cryptographic verification
  - Reduce risk through multiple layers of protection

## Contributing

**🙌 Contributions are welcome!**

If you have suggestions, bug reports, or want to help improve Pyseal, feel free to open an [issue](https://github.com/MCP-Security-Research/pyseal/issues) or submit a pull request.

All ideas and contributions are appreciated—thanks for helping make pyseal better!

## License

Pyseal is licensed under the MIT License. See [LICENSE](LICENSE) for details.

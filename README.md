**C++ compiler**
A Python-based C++ compiler with a Qt5 GUI that simulates all major compilation phases including lexical analysis, syntax analysis (AST), semantic checks, intermediate code generation, and code optimization. Designed as an educational tool to demonstrate how a compiler processes and transforms C++ code step by step.

**Lexical Analysis**
Tokenizes the input code
Identifies keywords, identifiers, operators, literals, etc.

**Syntax Analysis**
Constructs an Abstract Syntax Tree (AST)
Uses grammar rules to verify structure

**Semantic Analysis**
Validates variable declarations, scope, type compatibility
Detects semantic errors

**Intermediate Code Generation**
Translates AST into intermediate three-address code
Structured and easier to optimize

**Code Optimization**
Simplifies and refines intermediate code
Improves runtime performance and efficiency

**GUI Highlights**
Built with PyQt5, the GUI makes this compiler user-friendly and interactive:
Code input section
Step-by-step display of each compilation phase
Token table and semantic error output
Intermediate and optimized code panels

## Project Structure

- `main.py` – Entry point with GUI
- `exer.py` – Token generation logic
- `parser.py` – Syntax analysis and AST generation
- `semantic.py` – Semantic checks
- `icg.py` – Intermediate Code Generation
- `optimizer.py` – Code optimization logic
- `ui/` – Qt UI files

**Requirements**
Python 3.8+
PyQt5

**Installation**
Clone the repository and run the project locally:

```bash
git clone https://github.com/yourusername/cpp-compiler-python.git
cd cpp-compiler-python
pip install -r requirements.txt
python main.py

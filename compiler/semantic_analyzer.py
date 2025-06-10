def analyze(ast):
    # Simple semantic analyzer: check for duplicate declarations
    symbol_table = set()
    errors = []

    for node in ast:
        if node[0] == 'declare':
            var_name = node[1]
            if var_name in symbol_table:
                errors.append(f"Semantic Error: Variable '{var_name}' already declared.")
            else:
                symbol_table.add(var_name)

    if errors:
        return "\n".join(errors)
    else:
        return "Semantic analysis passed."

def generate_ir(ast):
    # Generate a very basic IR representation as strings
    ir_code = []
    for node in ast:
        if node[0] == 'declare':
            var_name = node[1]
            expr = node[2]
            ir_code.append(f"DECLARE {var_name}")
            ir_code.append(f"ASSIGN {var_name} {expr}")
    return "\n".join(ir_code)

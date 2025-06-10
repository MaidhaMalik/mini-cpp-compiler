def generate_code(ir):
    # Dummy code generator that outputs pseudo-assembly
    lines = ir.splitlines()
    asm = []
    for line in lines:
        if line.startswith("DECLARE"):
            var = line.split()[1]
            asm.append(f"; Declaring variable {var}")
        elif line.startswith("ASSIGN"):
            parts = line.split()
            var = parts[1]
            expr = " ".join(parts[2:])
            asm.append(f"MOV {var}, {expr}")
    return "\n".join(asm)

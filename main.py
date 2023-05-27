from itertools import product

def solve_karnaugh_map(inputs, num_vars):
    variables = [chr(65 + i) for i in range(num_vars)]
    minterms = [inputs[i] for i in range(2 ** num_vars)]
    
    terms = []
    for i, value in enumerate(minterms):
        if value == '1':
            term = ""
            for j, var in enumerate(variables):
                if (i >> (num_vars - 1 - j)) & 1:
                    term += var
                else:
                    term += f"~{var}"
            terms.append(term)
    
    if len(terms) == 0:
        return "0"
    
    expression = " + ".join(terms)
    return expression

def print_truth_table(inputs, num_vars):
    variables = [chr(65 + i) for i in range(num_vars)]
    
    header = " | ".join(variables + ["Output"])
    line = "-" * len(header)
    
    print(header)
    print(line)
    
    for i, values in enumerate(product("01", repeat=num_vars)):
        row = " | ".join(list(values) + [inputs[i]])
        print(row)

# Exemplo de uso
num_vars = int(input("\nDigite o número de variáveis do mapa de Karnaugh (2 a 5): "))
inputs = []
print()
for i in range(2 ** num_vars):
    input_str = input(f"Informe a entrada para {bin(i)[2:].zfill(num_vars)}: ")
    inputs.append(input_str)

print("\nTabela Verdade:")
print_truth_table(inputs, num_vars)

print("\nMapa de Karnaugh:")
for i in range(2 ** num_vars):
    print(" | ".join(inputs[i * 2 ** (num_vars - 1): (i + 1) * 2 ** (num_vars - 1)]))

expression = solve_karnaugh_map(inputs, num_vars)
print("\nExpressão final:", expression)


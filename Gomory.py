# Importar la librería PuLP
from pulp import *

# Crear el problema de programación lineal y especificar si se busca maximizar o minimizar la función objetivo
prob = LpProblem("Problema de Programación Lineal", LpMaximize)

# Definir las variables de decisión, junto con sus límites inferiores y el tipo de variable
x1 = LpVariable("x1", lowBound=0, cat='Integer')
x2 = LpVariable("x2", lowBound=0, cat='Integer')

# Definir la función objetivo del problema
prob += 3*x1 + 5*x2

# Definir las restricciones del problema
prob += x1 + x2 <= 5
prob += 2*x1 + 3*x2 <= 12

# Resolver el problema usando el algoritmo Gomory
while True:
    # Resolver el problema
    prob.solve()

    # Verificar si alguna variable de decisión tiene un valor fraccionario
    fractional_vars = [v for v in prob.variables() if v.varValue != int(v.varValue)]
    if not fractional_vars:
        # Si no hay variables fraccionarias, el problema está resuelto y se sale del loop while
        break

    # Tomar la primera variable fraccionaria
    frac_var = fractional_vars[0]

    # Obtener los índices de la variable fraccionaria
    frac_var_indices = [i for i in range(len(frac_var.name)) if frac_var.name[i].isdigit()]

    # Obtener el índice de la variable fraccionaria
    frac_var_index = int(frac_var.name[frac_var_indices[0]:frac_var_indices[-1]+1])

    # Obtener el valor de la variable fraccionaria
    frac_var_value = frac_var.varValue

    # Encontrar la restricción que involucra la variable fraccionaria
    constraint = None
    for c in prob.constraints.values():
        if frac_var.name in c.name:
            constraint = c
            break

    # Si no se encuentra la restricción, continuar con el siguiente ciclo del while
    if not constraint:
        continue

    # Obtener los coeficientes de la restricción y el lado derecho de la restricción
    constraint_coeffs = constraint.values()
    constraint_rhs = constraint.constant

    # Aplicar el algoritmo Gomory para crear una nueva restricción a partir de la restricción original
    gomory_constraint_coeffs = [int(2 * c) for c in constraint_coeffs]
    gomory_constraint_rhs = int(2 * constraint_rhs)
    gomory_constraint_coeffs[frac_var_index] -= 1
    gomory_constraint = LpConstraint(LpAffineExpression(list(zip(prob.variables(), gomory_constraint_coeffs))), LpConstraintLE, gomory_constraint_rhs, name="Gomory")

    # Agregar la nueva restricción al problema
    prob += gomory_constraint

# Imprimir los resultados del problema
print("Status:", LpStatus[prob.status])
print("Solución óptima:")
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Valor objetivo:", value(prob.objective))

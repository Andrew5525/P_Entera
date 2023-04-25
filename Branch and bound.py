from pulp import *

# Crear el problema
prob = LpProblem("Problema de Programación Lineal", LpMaximize)

# Variables de decisión
x1 = LpVariable("x1", lowBound=0, cat='Integer')
x2 = LpVariable("x2", lowBound=0, cat='Integer')

# Función objetivo
prob += 3*x1 + 5*x2

# Restricciones
prob += x1 + x2 <= 5
prob += 2*x1 + 3*x2 <= 12

# Resolver usando Branch and Bound
prob.solve(PULP_CBC_CMD(msg=0))

# Imprimir resultados
print("Status:", LpStatus[prob.status])
print("Solución óptima:")
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Valor objetivo:", value(prob.objective))

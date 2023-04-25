# Importar la librería PuLP
from pulp import *

# Crear el problema
prob = LpProblem("Problema de Programación Lineal", LpMaximize)

# Definir las variables de decisión
# Se definen dos variables de decisión x1 y x2 con un límite inferior de 0 y se establece que son enteras
x1 = LpVariable("x1", lowBound=0, cat='Integer')
x2 = LpVariable("x2", lowBound=0, cat='Integer')

# Definir la función objetivo
# Se define la función objetivo como una expresión lineal en términos de las variables de decisión x1 y x2
prob += 3*x1 + 5*x2

# Definir las restricciones
# Se definen dos restricciones lineales, que limitan la combinación de las variables de decisión x1 y x2
# La primera restricción establece que la suma de x1 y x2 debe ser menor o igual a 5
prob += x1 + x2 <= 5
# La segunda restricción establece que la combinación lineal de x1 y x2 ponderada por 2 y 3, respectivamente,
# debe ser menor o igual a 12
prob += 2*x1 + 3*x2 <= 12

# Resolver el problema utilizando el algoritmo de Egon Balas
# El algoritmo de Egon Balas es un método heurístico para resolver problemas de programación lineal mixta entera
while True:
    # Se resuelve el problema
    prob.solve()
    # Se identifican las variables fraccionales
    fractional_vars = [v for v in prob.variables() if v.varValue != int(v.varValue)]
    # Si no hay variables fraccionales, se ha encontrado la solución óptima y se sale del ciclo while
    if not fractional_vars:
        break
    # Se selecciona la primera variable fraccional encontrada
    frac_var = fractional_vars[0]
    # Se obtiene el índice de la variable fraccional
    frac_var_indices = [i for i in range(len(frac_var.name)) if frac_var.name[i].isdigit()]
    frac_var_index = int(frac_var.name[frac_var_indices[0]:frac_var_indices[-1]+1])
    # Se obtiene el valor de la variable fraccional
    frac_var_value = frac_var.varValue
    # Se agregan nuevas restricciones para acotar la variable fraccional
    prob += frac_var <= int(frac_var_value)
    prob2 = LpProblem("Problema de Programación Lineal", LpMaximize)
    prob2 += prob.objective
    prob2 += frac_var >= int(frac_var_value) + 1
    for constraint in prob.constraints.values():
        # Se copian las restricciones del problema original al nuevo problema, excepto aquellas que contienen
        # la variable fraccional
        if frac_var.name not in constraint.name:
            prob2 += constraint
    # Se actualiza el problema original con las nuevas restricciones
    prob = prob2

# Imprimir resultados
# Se imprime el estado del problema
print("Estado:", LpStatus[prob.status])
# Se imprime la solución óptima encontrada
for v in prob.variables():
    print(v.name, "=", v.varValue)


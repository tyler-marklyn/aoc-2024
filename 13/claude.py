import sympy

def solve_diophantine_system(a, b, c, d, e, f):
    # Define symbolic variables
    x, y = sympy.symbols('x y')
    
    # Create system of equations
    eq1 = sympy.Eq(a*x + b*y, c)
    eq2 = sympy.Eq(d*x + e*y, f)
    
    # Solve the system
    solution = sympy.solve((eq1, eq2), (x, y))
    
    return solution

# Solve specific problem
result = solve_diophantine_system(26, 67, 10000000012748, 66, 21, 10000000012176)
print(result)
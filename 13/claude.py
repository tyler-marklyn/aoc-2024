import math

def solve_diophantine_overlap(a, b, c, d, e, f):
    # Compute initial solution for first equation
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = extended_gcd(b, a % b)
        return gcd, y1, x1 - (a // b) * y1

    gcd_ab = math.gcd(a, b)
    gcd_de = math.gcd(d, e)
    
    if c % gcd_ab != 0 or f % gcd_de != 0:
        return None

    gcd_ab, m, n = extended_gcd(a, b)
    m *= c // gcd_ab
    n *= c // gcd_ab

    b_term = b // gcd_ab
    a_term = a // gcd_ab

    # Algebraically solve for k
    # 26(m + k*b/gcd) + 67(n - k*a/gcd) = 10000000012748
    # 66(m + k*b/gcd) + 21(n - k*a/gcd) = 10000000012176

    # Rearrange to isolate k
    num1 = 10000000012748 - 26*m - 67*n
    num2 = 10000000012176 - 66*m - 21*n
    
    coeff1 = 26*b_term + 67*(-a_term)
    coeff2 = 66*b_term + 21*(-a_term)

    # Find k that satisfies both equations
    if num1 % coeff1 == 0 and num2 % coeff2 == 0:
        k1 = num1 // coeff1
        k2 = num2 // coeff2
        
        if k1 == k2:
            x = m + k1*b_term
            y = n - k1*a_term
            return x, y

    return None

# Solve specific problem
result = solve_diophantine_overlap(26, 67, 10000000012748, 66, 21, 10000000012176)
print(result)
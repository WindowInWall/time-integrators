import numpy as np

# elements of the array correspond to coefficients, and indices to powers
polynomial = np.array([-50, 4, 6, 3.1415, 7])
polynomial = np.array([5, 0, -1])

def gen_mat(num_terms):
    mat = np.zeros((num_terms - 1,1))
    for i in range(num_terms - 1):
        arr = np.zeros((num_terms-1,1))
        arr[i][0] = i + 1
        mat = np.hstack((mat, arr))
    return mat

def eval_poly(poly, x):
    res = 0
    for i, coef in enumerate(poly):
        res += coef * pow(x, i)
    return res

def derivative(poly):
    mat = gen_mat(len(poly))
    return mat.dot(poly)

root_est = 0
derivative = derivative(polynomial)
while abs(eval_poly(polynomial, root_est)) > 1e-6:
    poly_at_est_root = eval_poly(polynomial, root_est)
    deriv_at_est_root = eval_poly(derivative, root_est)

    root_est -= poly_at_est_root / deriv_at_est_root
print(f"estimated root at: {root_est}")

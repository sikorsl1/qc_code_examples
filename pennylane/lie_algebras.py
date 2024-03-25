import numpy as np
import pennylane as qml
from pennylane import X, Y, Z

qml.operation.enable_new_opmath()

su2_base = [1j * X(0), 1j * Y(0), 1j * Z(0)] # this is a base of su(2) Lie algebra - it can spans over reals all skew-Hermitian matrices

coeffs = np.random.randn(3)                          # some real coefficients
exponent = qml.dot(coeffs, su2_base)                 # linear combination of operators
U = qml.math.expm(exponent.matrix())                 # exponent of a skew-Hermitian matrix is unitary
print(np.allclose(np.matmul(U.conj().T, U), np.eye(2)))   # check that result is unitary UU* = 1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

v = Statevector([1/np.sqrt(2), 1/np.sqrt(2)])
w = Statevector.from_label('+')
vw = v.tensor(w)
print(vw.draw("text"))

circuit = QuantumCircuit(2)

circuit.h(0)
circuit.h(1)
# circuit.t(0)
# circuit.h(0)
# circuit.t(0)
# circuit.z(0)

res = vw.evolve(circuit)
print(res.draw("text"))
from qiskit.visualization import plot_bloch_vector, plot_bloch_multivector
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

v = Statevector.from_label('0')
w = Statevector.from_label('1')
vw = v.tensor(w)
print(vw.draw("text"))

circuit = QuantumCircuit(2)

circuit.h(0)
circuit.x(0)
circuit.h(1)

res = vw.evolve(circuit)
print(res.draw("text"))

plot_bloch_multivector(res)

# plot_bloch_vector(v)
plt.show()
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt
from qiskit.quantum_info import Operator

v = Statevector.from_label('0')
w = Statevector.from_label('1')
vw = v.tensor(w)
print(vw.draw("text"))

circuit = QuantumCircuit(2)

circuit.x(0)
circuit.s(1)
circuit.cx(1, 0)
circuit.h(0)
circuit.h(1)

circuit.draw(output='mpl')
plt.show()

print(Operator(circuit))

res = vw.evolve(circuit)
print(res.draw("text"))
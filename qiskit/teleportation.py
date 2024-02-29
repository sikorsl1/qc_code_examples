from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit.result import marginal_counts
import numpy as np
import matplotlib.pyplot as plt

q_reg = QuantumRegister(3)
c_reg = ClassicalRegister(2)
c_res = ClassicalRegister(1)
qc = QuantumCircuit(q_reg, c_reg, c_res)

alpha, theta = 2*np.pi*np.random.rand(), 2*np.pi*np.random.rand()
psi = Statevector([np.cos(alpha), np.exp(theta*1j)*np.sin(alpha)])

print(f'Initial state: {psi.draw("text")}')

qc.initialize(psi, q_reg[0])
qc.barrier()
qc.cx(q_reg[0], q_reg[1])
qc.h(q_reg[0])
qc.barrier()
qc.measure([q_reg[0], q_reg[1]], c_reg)
qc.barrier()

with qc.if_test((c_reg[0], 1)):
    qc.z(q_reg[2])
with qc.if_test((c_reg[1], 1)):
    qc.x(q_reg[2])

qc.barrier()
qc.measure([q_reg[2]], [c_res[0]])

# qc.draw(output='mpl')
# plt.show()

num_shots = 10000
result = AerSimulator().run(qc, shots=num_shots).result()
marginal_counts(result, [2], inplace=True)
statistics = result.get_counts()
print(f'Experimental result: [{np.sqrt(statistics.get("0")/num_shots)}, {np.sqrt(statistics.get("1")/num_shots)}]')
plt.show()

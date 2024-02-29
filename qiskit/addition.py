from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit.circuit.library import XGate

import matplotlib.pyplot as plt

def addition_circuit(bits_a, bits_b):
# this circuit realizes the following arithmetic operation: a += b
    q_a = QuantumRegister(bits_a)
    q_b = QuantumRegister(bits_b)
    qc = QuantumCircuit(q_a, q_b, name='Addition')

    for idx_b in range(bits_b):
        for idx_a in range(0, bits_a - idx_b):
            q_idx = [q_b[idx_b]] + [*q_a[idx_b:(bits_a - idx_a)]]
            controlled_gate = XGate().control(bits_a - idx_a - idx_b)
            qc.append(controlled_gate, q_idx)

    return qc

def main():
    bit_num_a, bit_num_b = 5, 5
    q_a = QuantumRegister(bit_num_a)
    q_b = QuantumRegister(bit_num_b)
    c_reg = ClassicalRegister(bit_num_a)
    qc = QuantumCircuit(q_a, q_b, c_reg)

    # initialize state vectors
    a_bin = '10011'
    b_bin = '01011'
    a = Statevector.from_label(a_bin)
    b = Statevector.from_label(b_bin)

    qc.initialize(a, q_a)
    qc.initialize(b, q_b)

    # append addition circuitv
    qc.barrier()
    qc_add = addition_circuit(bit_num_a, bit_num_b)
    qc.compose(qc_add, [*q_a, *q_b], inplace=True)

    # measure the result
    qc.barrier()
    qc.measure(q_a, c_reg)

    qc.draw(output='mpl')
    plt.show()

    num_shots = 100
    result = AerSimulator().run(qc, shots=num_shots).result()
    statistics = result.get_counts()
    print(f'Addition result: {statistics}')

if __name__ == "__main__":
    main()

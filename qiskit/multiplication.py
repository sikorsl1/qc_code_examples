from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit.primitives import Sampler

import matplotlib.pyplot as plt
from addition import addition_circuit

def multiplication_circuit(bits_a, bits_b):
# this circuit realizes the following arithmetic operation: a += b*b
    q_a = QuantumRegister(bits_a)
    q_b = QuantumRegister(bits_b)
    qc = QuantumCircuit(q_a, q_b)

    q_add_1 = addition_circuit(bits_a, 1)
    qc.compose(q_add_1, [*q_a, q_b[0]], inplace=True)

    add_gate = addition_circuit(bits_a-1, 1).to_gate()
    controll_add = add_gate.control(1)
    qc.append(controll_add, [q_b[1], q_a[1], q_a[2], q_a[3], q_b[0]])
    qc.append(controll_add, [q_b[1], q_a[1], q_a[2], q_a[3], q_b[0]])

    q_add_2 = addition_circuit(bits_a-2, 1)
    qc.compose(q_add_2, [q_a[2], q_a[3], q_b[1]], inplace=True)

    return qc

def main():
    bit_num_a, bit_num_b = 4, 2
    q_a = QuantumRegister(bit_num_a)
    q_b = QuantumRegister(bit_num_b)
    c_reg = ClassicalRegister(bit_num_a)
    qc = QuantumCircuit(q_a, q_b, c_reg)

    # initialize state vectors
    a_bin = '1001'
    b_bin = '10'
    a = Statevector.from_label(a_bin)
    b = Statevector.from_label(b_bin)

    qc.initialize(a, q_a)
    qc.initialize(b, q_b)

    # append addition circuitv
    qc.barrier()
    qc_mltpl = multiplication_circuit(bit_num_a, bit_num_b)
    qc.compose(qc_mltpl, [*q_a, *q_b], inplace=True)

    # measure the result
    qc.barrier()
    qc.measure(q_a, c_reg)

    sampler = Sampler()
    job = sampler.run(qc)
    print(job.result())

    # # qc.draw(output='mpl')
    # # plt.show()

if __name__ == "__main__":
    main()

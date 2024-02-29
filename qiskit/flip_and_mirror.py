from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import ZGate
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

import matplotlib.pyplot as plt

def flip_circuit(bits_num, numbers_to_flip):
    qr = QuantumRegister(bits_num)
    qc = QuantumCircuit(qr)
    numbers_idxs = []
    for number in numbers_to_flip:
        idxs = [i for i, x in enumerate(number[::-1]) if x == "0"]
        numbers_idxs.append(idxs)

    for idxs in numbers_idxs:
        for idx in idxs:
            qc.x(idx)
        c_phase = ZGate().control(num_ctrl_qubits=bits_num-1)
        qc.append(c_phase, [*qr])
        for idx in idxs:
            qc.x(idx)
    return qc

def mirror_circuit(bits_num):
    qr = QuantumRegister(bits_num)
    qc = QuantumCircuit(qr)
    qc.h(qr)
    qc.x(qr)
    c_phase = ZGate().control(num_ctrl_qubits=bits_num-1)
    qc.append(c_phase, [*qr])
    qc.x(qr)
    qc.h(qr)
    return qc

def main():
    numbers = ['1100']
    bits_num = 4
    success_probs = []
    num_iters = list(range(1, 50))
    for num_iter in num_iters:

        qr = QuantumRegister(bits_num)
        cr = ClassicalRegister(bits_num)
        qc = QuantumCircuit(qr, cr)

        qc.h(qr)

        # flip and mirror
        for _ in range(num_iter):
            flip_c = flip_circuit(bits_num, numbers)
            qc.compose(flip_c, qr, inplace=True)
            qc.barrier()

            mirror_c = mirror_circuit(bits_num)
            qc.compose(mirror_c, qr, inplace=True)
            qc.barrier()

        # measure the results
        qc.measure(qubit=qr, cbit=cr)

        # qc.draw(output='mpl')
        # plt.show()

        num_shots = 100
        sim = AerSimulator()
        compiled_qc = transpile(qc, sim)
        result = sim.run(compiled_qc, shots=num_shots).result()
        statistics = result.get_counts()
        
        print(f'Results: {statistics}')
        success_prob = statistics.get(numbers[0], 0)
        success_probs.append(success_prob)
        # plot_histogram(statistics)
        # plt.show()
    plt.plot(num_iters, success_probs)
    plt.show()

if __name__ == "__main__":
    main()
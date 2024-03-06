from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import random_unitary
from qiskit_aer import AerSimulator
from qiskit.result import marginal_counts

import numpy as np
import matplotlib.pyplot as plt


def circuit_factory():
    q_code = QuantumRegister(9, 'q_code')
    q_rand = QuantumRegister(4, 'q_rand')
    c_rand = ClassicalRegister(4, 'c_rand')
    c_result = ClassicalRegister(1, 'c_results')

    qc = QuantumCircuit(q_code, q_rand, c_rand, c_result)

    # initialize state
    alpha = 2*np.pi*np.random.rand()
    print(f'True - |0> : {np.cos(alpha)**2}, |1>: {np.sin(alpha)**2}.')
    qc.initialize([np.cos(alpha), np.sin(alpha)], 0)

    # prepare the code
    qc.cx(q_code[0], q_code[3])
    qc.cx(q_code[0], q_code[6])
    qc.h([q_code[0], q_code[3], q_code[6]])

    qc.cx(q_code[0], q_code[1])
    qc.cx(q_code[0], q_code[2])
    qc.cx(q_code[3], q_code[4])
    qc.cx(q_code[3], q_code[5])
    qc.cx(q_code[6], q_code[7])
    qc.cx(q_code[6], q_code[8])

    # introduce error
    qc.h(q_rand)
    qc.measure([q_rand[0], q_rand[1], q_rand[2], q_rand[3]], c_rand)
    random_error = random_unitary(2)

    with qc.switch(c_rand) as case:
        with case(0b0000, 0b1010):
            qc.append(random_error, [q_code[0]])
        with case(0b0001, 0b1011):
            qc.append(random_error, [q_code[1]])
        with case(0b0010, 0b1100):
            qc.append(random_error, [q_code[2]])
        with case(0b0011, 0b1101):
            qc.append(random_error, [q_code[3]])
        with case(0b0100, 0b1110):
            qc.append(random_error, [q_code[4]])
        with case(0b0101, 0b1111):
            qc.append(random_error, [q_code[5]])
        with case(0b0110):
            qc.append(random_error, [q_code[6]])
        with case(0b0111):
            qc.append(random_error, [q_code[7]])
        with case(0b1000):
            qc.append(random_error, [q_code[8]])
        with case(0b1001):
            pass

    qc.barrier()

    # decode and correct
    qc.cx(q_code[0], q_code[1])
    qc.cx(q_code[0], q_code[2])
    qc.ccx(q_code[2], q_code[1], q_code[0])
    qc.cx(q_code[3], q_code[4])
    qc.cx(q_code[3], q_code[5])
    qc.ccx(q_code[5], q_code[4], q_code[3])
    qc.cx(q_code[6], q_code[7])
    qc.cx(q_code[6], q_code[8])
    qc.ccx(q_code[8], q_code[7], q_code[6])

    qc.h([q_code[0], q_code[3], q_code[6]])
    qc.cx(q_code[0], q_code[3])
    qc.cx(q_code[0], q_code[6])
    qc.ccx(q_code[6], q_code[3], q_code[0])

    qc.barrier()

    # measure the result
    qc.measure([q_code[0]], [c_result[0]])

    return qc



def main():

    sim_runs = 5000
    simulator = AerSimulator()
    circuit = circuit_factory(simulator)
    # circuit.draw(output='mpl')
    # plt.show()

    job = simulator.run(circuit, shots=sim_runs)

    result = job.result()
    marginal_counts(result, [4], inplace=True)
    counts = result.get_counts(circuit)
    print(f'Experimental - |0> : {counts.get("0")/sim_runs}, |1>: {counts.get("1")/sim_runs}.')

if __name__ == "__main__":
    main()


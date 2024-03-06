from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from math import pi
from qiskit.result import marginal_counts

import matplotlib.pyplot as plt
import numpy as np

def circuit_factory():
    q_register = QuantumRegister(3, 'q_register')
    q_rand = QuantumRegister(2, 'q_rand')
    c_rand = ClassicalRegister(2, 'c_rand')
    c_results = ClassicalRegister(1, 'c_results')
    circuit = QuantumCircuit(q_register, q_rand, c_rand,
                             c_results)
    
    # initialize state
    alpha = 2*pi*np.random.rand()
    print(f'True - |0> : {np.cos(alpha)**2}, |1>: {np.sin(alpha)**2}.')
    circuit.initialize([np.cos(alpha), np.sin(alpha)], 0)
    
    # prepare the code
    circuit.cx(q_register[0], q_register[1])
    circuit.cx(q_register[0], q_register[2])

    circuit.barrier()
    # introduce error
    circuit.h(q_rand[0])
    circuit.h(q_rand[1])
    circuit.measure([q_rand[0], q_rand[1]],
                    [c_rand[0], c_rand[1]])

    with circuit.switch(c_rand) as case:
        with case(0b00):
            circuit.x(q_register[0])
        with case(0b01):
            circuit.x(q_register[1])
        with case(0b10):
            circuit.x(q_register[2])
        with case(0b11):
            pass
    
    circuit.barrier()
    # apply corrections
    circuit.cx(q_register[0], q_register[1])
    circuit.cx(q_register[0], q_register[2])
    circuit.ccx(q_register[2], q_register[1], q_register[0])
    
    circuit.measure([q_register[0]], [c_results[0]])

    return circuit

def main():

    sim_runs = 100000
    simulator = AerSimulator()
    circuit = circuit_factory()
    # circuit.draw(output='mpl', plot_barriers=False)
    # plt.show()

    job = simulator.run(circuit, shots=sim_runs)

    result = job.result()
    marginal_counts(result, [2], inplace=True)
    counts = result.get_counts(circuit)
    print(f'Experimental - |0> : {counts.get("0")/sim_runs}, |1>: {counts.get("1")/sim_runs}.')

if __name__ == "__main__":
    main()
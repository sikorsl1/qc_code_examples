from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from math import pi
from qiskit.result import marginal_counts

import matplotlib.pyplot as plt
import numpy as np

def identity(simulator):
    q_register = QuantumRegister(1, 'q_register')
    c_results = ClassicalRegister(1, 'c_results')
    circuit = QuantumCircuit(q_register, c_results)
    
    # initialize state
    alpha = 2*pi*np.random.rand()
    print(f'True - |0> : {np.cos(alpha)**2}, |1>: {np.sin(alpha)**2}.')
    print(f'Value: {np.cos(alpha)/np.sin(alpha)}')
    circuit.initialize([np.cos(alpha), np.sin(alpha)], 0)
    
    circuit.measure(q_register, c_results)

    compiled_circuit = transpile(circuit, simulator)

    return compiled_circuit, circuit

def multiplication(simulator):
    q_register = QuantumRegister(2, 'q_register')
    c_results = ClassicalRegister(2, 'c_results')
    circuit = QuantumCircuit(q_register, c_results)
    
    # initialize state
    values = []
    for i in range(2):
        alpha = pi*np.random.rand()/2
        values.append(np.cos(alpha)/np.sin(alpha))
        circuit.initialize([np.cos(alpha), np.sin(alpha)], i)

    print(f'Multiplication: {values[0]} * {values[1]} = {values[0]*values[1]}')
    print(f'Addition: {values[0]} + {values[1]} = {values[0]+values[1]}')
    
    circuit.measure(q_register, c_results)

    compiled_circuit = transpile(circuit, simulator)

    return compiled_circuit, circuit

def main():

    sim_runs = 100000
    simulator = AerSimulator()
    compiled_circuit, circuit = multiplication(simulator)
    # print(circuit)
    # circuit.draw(output='mpl')
    # plt.show()

    job = simulator.run(compiled_circuit, shots=sim_runs)

    result = job.result()
    marginal_counts(result, [0, 1], inplace=True)
    counts = result.get_counts(compiled_circuit)
    # print(counts)
    res_mul = np.sqrt(counts.get("00")/sim_runs)/np.sqrt(counts.get("11")/sim_runs)
    res_add = np.sqrt(counts.get("01")/sim_runs)/np.sqrt(counts.get("11")/sim_runs) + np.sqrt(counts.get("10")/sim_runs)/np.sqrt(counts.get("11")/sim_runs)
    print(f'Experimental result multiplication: {res_mul}')
    print(f'Experimental result addition: {res_add}')
    # alpha = counts.get("0")/sim_runs
    # beta = counts.get("1")/sim_runs
    # print(f'Experimental - |0> : {counts.get("0")/sim_runs}, |1>: {counts.get("1")/sim_runs}.')
    # print(f'Doubled value: {np.sqrt(alpha/beta)}')

if __name__ == "__main__":
    main()
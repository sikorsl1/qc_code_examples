from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import TwoLocal
from qiskit.primitives import BackendEstimator
from qiskit_aer import AerSimulator
import numpy as np
from scipy.optimize import minimize

def cost_function(params, estimator, ansatz, observable):
    job = estimator.run(circuits=[ansatz], observables=[observable], parameter_values=params)
    return job.result().values[0]

def prepare_ansatz(num_qubits, num_reps):
    ansatz = TwoLocal(
        num_qubits=num_qubits,
        rotation_blocks=["rx", "rz"],
        entanglement_blocks="cz",
        entanglement="linear",
        reps=num_reps,
        insert_barriers=True,
    )
    return ansatz

def main():
    num_qubits = 4
    num_reps = 3
    num_params = num_qubits*2*(num_reps + 1)
    init_params = np.random.randn(num_params)
    observable = SparsePauliOp.from_list([('IIZZ', 3), ('IZIZ', -2), ('ZIZI', 1), ('ZZII', -0.5)])
    ansatz = prepare_ansatz(num_qubits, num_reps)
    estimator = BackendEstimator(backend=AerSimulator())
    result = minimize(cost_function, init_params, args=(estimator, ansatz, observable), method="COBYLA", options={'disp': True})
    print(f'Result: {result}')

if __name__ == "__main__":
    main()
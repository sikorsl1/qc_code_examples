from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import BackendEstimator
from qiskit_aer.noise import NoiseModel
from qiskit.quantum_info import SparsePauliOp

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

from qiskit.providers.fake_provider import GenericBackendV2

# prepare the GHZ state
def circuit_factory(n_qubits):
    qc = QuantumCircuit(n_qubits)
    qc.h(0)
    for k in range(0, n_qubits-1):
        qc.cx(k, k+1)

    return qc

def main():
    n_qubits = 5
    backend = GenericBackendV2(n_qubits)
    noise_model = NoiseModel.from_backend(backend)
    print(noise_model)

    # prepare circuits
    qc = circuit_factory(n_qubits)
    print(qc.draw())

    # transpilation for specific hardware 
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(qc)

    # prepare observalbes
    Z_n = SparsePauliOp('Z'*n_qubits)
    X_n = SparsePauliOp('X'*n_qubits)
    I_n = SparsePauliOp('I'*n_qubits)

    # align observables with the transpiled circuit layout
    Z_n = Z_n.apply_layout(isa_circuit.layout)
    X_n = X_n.apply_layout(isa_circuit.layout)
    I_n = I_n.apply_layout(isa_circuit.layout)

    # prepare and run estimator
    estimator = BackendEstimator(backend=AerSimulator(noise_model=noise_model))
    job = estimator.run(circuits=[qc]*3, observables=[I_n, Z_n, X_n])
    
    # Once the job is complete, get the result
    print(job.result())

if __name__ == "__main__":
    main()
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import BackendEstimator

from qiskit.circuit import Parameter
import numpy as np

def main():

    theta = Parameter('theta')
    qc = QuantumCircuit(2)
    # create entangled pair
    qc.h(0)
    qc.rx(theta, 1)
    qc.cx(0, 1)

    # define observables
    ZZ = SparsePauliOp('ZZ')
    ZI = SparsePauliOp('ZI')
    IZ = SparsePauliOp('IZ')
    XX = SparsePauliOp('XX')
    XI = SparsePauliOp('XI')
    IX = SparsePauliOp('IX')
    
    # Create an Estimator object
    estimator = BackendEstimator(backend=AerSimulator())
    
    # Submit the circuit to Estimator
    job = estimator.run(circuits=[qc]*6, observables=[IZ, IX, ZI, XI, ZZ, XX],
                        parameter_values= [[np.pi/k] for k in range(1, 7)], shots = 5000)
    
    # Once the job is complete, get the result
    print(job.result())

if __name__ == "__main__":
    main()
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator


def circuit_factory(message):
    q_reg = QuantumRegister(2)
    c_reg = ClassicalRegister(2)
    qc = QuantumCircuit(q_reg, c_reg)

    # Bell state prepartion
    qc.h(q_reg[0])
    qc.cx(q_reg[0], q_reg[1])

    # message encoding
    match message:
        case 0b00:
            pass
        case 0b01:
            qc.z(0)
        case 0b10:
            qc.x(0)
        case 0b11:
            qc.z(0)
            qc.x(0)

    qc.barrier()

    # measurement in Bell basis
    qc.cx(q_reg[0], q_reg[1])
    qc.h(q_reg[0])
    qc.measure(q_reg, c_reg)
    return qc

for mess in [0b00, 0b01, 0b10, 0b11]:
    num_shots = 100
    qc = circuit_factory(mess)
    result = AerSimulator().run(qc, shots=num_shots).result()
    statistics = result.get_counts()
    print(f'EMessage obtained: {statistics}')

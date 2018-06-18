from wrapper.experiment import Experiment


def entanglement(backend):
    """ Basic entanglement, setting up a bell state """
    experiment = Experiment(backend)
    experiment.connect_to_IBM()

    # Initialise circuit
    experiment.create_registers(qubits=2, classical_bits=2)
    experiment.create_quantum_circuit()

    # Gates 
    experiment.bell_state(control_qubit=0, target_qubit=1)
    experiment.measure_gate()

    # Execute
    experiment.compile_and_run()


def teleport(backend):
    """ Teleport the quantum state of the initial state. """
    experiment = Experiment(backend)
    experiment.connect_to_IBM()

    # Initialise circuit
    experiment.create_registers(qubits=3, classical_bits=3)
    experiment.create_quantum_circuit()

    # Prepare and initial state
    experiment.single_qubit_gate(gate='u3', qubit=2, angles=[0.3,0.2,0.1])

    # Gates
    experiment.bell_state(control_qubit=1, target_qubit=2)
    experiment.two_qubit_gate(gate='cx',  control_qubit=0, target_qubit=1)
    experiment.single_qubit_gate(gate='h', qubit=0)

    experiment.measure_gate(qubits=[0], classical_bits=[0])
    experiment.measure_gate(qubits=[1], classical_bits=[1])

    experiment.controlled_gate(gate='cz', target_qubit=2, control_bit=0, control_value=1)
    experiment.controlled_gate(gate='cx', target_qubit=2, control_bit=1, control_value=1)
    experiment.measure_gate(qubits=[2], classical_bits=[2])

    # Execute
    experiment.compile_and_run()

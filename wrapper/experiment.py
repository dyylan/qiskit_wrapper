from IBMQuantumExperience import IBMQuantumExperience
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, register, execute
import Qconfig

class Experiment:
    """ Experiment class for defining config, connecting to IBMQ and setting up quantum circuit. """

    def __init__(self, backend=None, shots=1024):
        try:
            register(Qconfig.APItoken, Qconfig.config['url'])
            print("Successfully connected to IBMQ.")
        except ConnectionError as e:
            print("{}\n\nFailed to connect to IBMQ - only local simulations are possible.".format(e))
        self.backend = backend
        self.shots = shots
        self.register_initialised = False
        self.qc_initialised = False
        self.coupling_map = False

    def connect_to_IBM(self, verify=False):
        """ Connect to IMB quantum experience using the class token value and config. """
        self.api = IBMQuantumExperience(Qconfig.APItoken, Qconfig.config, verify=verify)

    def create_registers(self, qubits=2, classical_bits=2):
        """ Create the quantum and classical registers with the specified number of bits. """
        if qubits != classical_bits:
            print("Warning: number of quantum register bits does not equal classical ")
        self.q = QuantumRegister(qubits)
        self.c = [ClassicalRegister(1) for _ in range(classical_bits)]
        self.register_initialised = True

    def create_quantum_circuit(self):
        """ Initialise the quantum circuit if the quantum and classical registers have been initialised. """
        if self.register_initialised:
            self.qc = QuantumCircuit(self.q)
            for c in self.c:
                self.qc.add(c)
            self.qc_initialised = True
        else:
            print("Create quantum and classical registers first!")

    def bell_state(self, control_qubit=0, target_qubit=1):
        """ Create a bell state of specified qubits from an Experiment object. """
        if not self.qc_initialised:
            print("Initialise quantum circuit first.")
            return
        try:
            control_qubit = self.q[control_qubit]
            target_qubit = self.q[target_qubit]
        except:
            print("Initialising control and target qubits failed")
            return
        self.qc.h(control_qubit)
        self.qc.cx(control_qubit, target_qubit)
        self.qc.barrier(self.q)

    def single_qubit_gate(self, gate, qubit, angles=[0,0,0]):
        """ Adding a one qubit gate to the quantum circuit """
        gate = str(gate).lower()
        if not self.qc_initialised:
            print("Initialise quantum circuit first.")
            return
        try:
            qubit = self.q[qubit]
        except:
            print("Initialising control and target qubits failed")
            return
        if gate == 'h' or gate == 'hadamard':
            self.qc.h(qubit)
        elif gate == 'x':
            self.qc.x(qubit)
        elif gate == 'y':
            self.qc.y(qubit)
        elif gate == 'z':
            self.qc.z(qubit)
        elif gate == 'u1':
            self.qc.u1(angles[0], qubit)
        elif gate == 'u2':
            self.qc.u2(angles[0], angles[1], qubit)
        elif gate == 'u3':
            self.qc.u3(angles[0], angles[1], angles[2], qubit)
        else:
            print("Not a valid single qubit gate. Gate not added to the circuit.")

    def two_qubit_gate(self, gate, control_qubit, target_qubit):
        """ Adding a two qubit gate to the quantum circuit """
        gate = str(gate).lower()
        if not self.qc_initialised:
            print("Initialise quantum circuit first.")
            return
        try:
            control_qubit = self.q[control_qubit]
            target_qubit = self.q[target_qubit]
        except:
            print("Initialising control and target qubits failed")
            return
        if gate == 'h' or gate == 'ch' or gate == 'control hadamard':
            self.qc.h(control_qubit, target_qubit)
        elif gate == 'x' or gate == 'cx' or gate == 'control x':
            self.qc.cx(control_qubit, target_qubit)
        elif gate == 'y' or gate == 'cy' or gate == 'control y':
            self.qc.cy(control_qubit, target_qubit)
        elif gate == 'z' or gate == 'cz' or gate == 'control z':
            self.qc.cz(control_qubit, target_qubit)
        else:
            print("Not a valid two qubit gate. Gate not added to the circuit.")      

    def controlled_gate(self, gate, target_qubit, control_bit, control_value=1):
        """ Adding a two qubit gate to the quantum circuit """
        gate = str(gate).lower()
        if not self.qc_initialised:
            print("Initialise quantum circuit first.")
            return
        try:
            control = self.c[control_bit] 
            qubit = self.q[target_qubit]
        except:
            print("Initialising control and target qubits failed")
            return
        if gate == 'h' or gate == 'ch' or gate == 'control hadamard':
            self.qc.h(qubit).c_if(control[0], control_value)
        elif gate == 'x' or gate == 'cx' or gate == 'control x':
            self.qc.x(qubit).c_if(control, control_value)
        elif gate == 'y' or gate == 'cy' or gate == 'control y':
            self.qc.y(qubit).c_if(control[0], control_value)
        elif gate == 'z' or gate == 'cz' or gate == 'control z':
            self.qc.z(qubit).c_if(control, control_value)
        else:
            print("Not a valid two qubit gate. Gate not added to the circuit.")             

    def measure_gate(self, qubits=None, classical_bits=None):
        """ Add a measure gate to the quantum circuit of the Experiment class. 

            If you give a list of qubits, then give a list of controls where the 
            index matches where the qubit measurement is stored.        
        """
        if not qubits and not classical_bits:
            for i in self.c:
                self.qc.measure(self.q[i], i)
        elif qubits:
            for index, q in enumerate(qubits):
                self.qc.measure(self.q[q], self.c[classical_bits[index]][0])
                print("measured q: {}, c: {}".format(self.q[q], self.c[classical_bits[index]]))

    def compile_and_run(self):
        if self.register_initialised and self.qc_initialised:
            print("Running on backend: {}".format(self.backend))
            if self.coupling_map:
                print("Using coupling map for {}...".format(self.backend))
                job = execute(self.qc, backend=self.backend, coupling_map=self.coupling_map, shots=self.shots)
            else:
                job = execute(self.qc, backend=self.backend, shots=self.shots)
            result = job.result()
            print("Result: {}".format(result))
            print(result.get_counts(self.qc))
        else:
            print("Initialise register and quantum circuit first.")

    @staticmethod
    def IBMQ_register():
        try:
            register(Qconfig.APItoken, Qconfig.config['url'])
            print("Successfully connected to IBMQ.")
        except ConnectionError as e:
            print("{}\n\nFailed to connect to IBMQ - only local simulations are possible.".format(e))
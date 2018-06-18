from wrapper.experiment import Experiment
from qiskit import available_backends
from wrapper.circuits import entanglement, teleport

def main():
    remote_backends, remote_simulator, local_simulators = backend_lists()
    local_sim = "local_qasm_simulator" 
    remote_sim = remote_simulator[0]
    remote_machine = "ibmqx2"
    backend = remote_sim
    #entanglement(backend)
    teleport(backend)

def backend_lists():
    Experiment().IBMQ_register()
    remote_backends = available_backends({'local': False, 'simulator': False})
    remote_simulator = available_backends({'local': False, 'simulator': True})
    local_simulators = available_backends({'local': True})
    print("Remote backends: {}".format(remote_backends))
    print("Remote simulator: {}".format(remote_simulator))
    print("Local backends: {}".format(local_simulators))
    return (remote_backends, remote_simulator, local_simulators)

if __name__ == "__main__":
    main()

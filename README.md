# qiskit_wrapper
Running IBM Q experiments. Simple python to make it easier. The intention is also to add visualisation and a range of different algorithms. 

## Simple wrapper made from:
- [ibmqx backend information](https://github.com/QISKit/ibmqx-backend-information) Information about the different IBM Q experience backends.
- [ibmqx user guide](https://github.com/QISKit/ibmqx-user-guides) The users guides for the IBM Q experience.
- [Python API](https://github.com/QISKit/qiskit-api-py) API Client to use IBM Q experience in Python.
- [Python SDK](https://github.com/QISKit/qiskit-sdk-py) Software development kit for working with quantum programs in Python.

## How to use the wrapper
### Prerequisites 
- Python 3.6
- Get a token from IBMQ, start here: https://quantumexperience.ng.bluemix.net/qx/experience 
- Install pipenv with
> pip install pipenv

### Run an experiment on the IBM Quantum computer
- Clone this repository
- Install all the required packages
> pipenv install

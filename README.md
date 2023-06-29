# PowerFlow
#Power Flow Solver Readme

Overview

This code provides a power flow solver that calculates the power flow in an electrical power system. The solver implements various methods, including Newton-Raphson (NR), forward-backward sweep, fast decouple, Gauss-Seidel, and parallel implementation of the methods.

Requirements

Python 3.x
Numpy library
Pandas library (for input/output operations)
pandapower
power_grid_model

Usage

Install Python 3.x on your system if not already installed.
Install the required libraries by running the following command:
Copy code
pip install numpy pandas power_grid_model pandapower
Prepare the input data in the required format (check the test example in the data folder). The input data should include the system's bus data and line data.

Modify the code to specify the method you want to use for power flow calculation. Set the desired method in the main function.
Run the code using the following command:
python main.py
The code will read the input data, perform the power flow calculation using the specified method, and display the results.
Methods

Newton-Raphson (NR)
The NR method is an iterative technique used to solve a system of nonlinear equations. It is commonly used for power flow calculations due to its robustness and convergence properties. The NR method iteratively updates the voltage magnitudes and angles at each bus until the power mismatches are minimized.

Forward-Backward Sweep
The forward-backward sweep method is a simplified power flow technique that assumes the power flow in a radial distribution system. It iteratively calculates the voltage magnitudes and angles starting from the slack bus (forward sweep) and then propagates the results back to the slack bus (backward sweep).

Fast Decouple
The fast decouple method is an extension of the Gauss-Seidel method that decouples the voltage magnitude and angle calculations. It updates the voltage magnitudes and angles iteratively until convergence is achieved.

Gauss-Seidel
The Gauss-Seidel method is an iterative technique that updates the voltage magnitudes and angles at each bus sequentially based on the most recently calculated values. It continues the updates until convergence is reached.

Parallel Implementation
This code also provides a parallel implementation of the power flow methods (default id NR). It utilizes parallel computing techniques to speed up the power flow calculations by distributing the workload across multiple processors or threads. This can significantly reduce the computation time for large power systems.

Limitations

The code assumes a balanced three-phase power system and does not consider unbalanced or asymmetrical conditions.
The code may not converge for certain system conditions or configurations. In such cases, alternative methods or system adjustments may be required.
The parallel implementation may require additional setup and configuration to work correctly based on your system's specifications.

Support

For any issues or questions, please open an issue on the code repository or contact us at b.ahmadi@utwente.nl.

Acknowledgements

This code is under development, so please be patient with bugs and errors ;)


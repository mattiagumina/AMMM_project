from pathlib import Path
import sys

from datParser import DATParser
from solvers.solver_Greedy import Solver_Greedy
from solvers.solver_GreedyLocalSearch import Solver_GreedyLocalSearch
from solvers.solver_GRASP import Solver_GRASP

class Main:
    def __init__(self, config):
        self.config = config

    def run(self):
        """
        Executes the selected algorithm based on the configuration.
        :return: Exit code.
        """
        try:
            # Parse input data using the inputDataFile attribute
            input_data = DATParser.parse(self.config.inputDataFile)

            if self.config.verbose:
                print('Input Data:', self.config.inputDataFile)
            
            if self.config.solver == 'GRASP':
                solver = Solver_GRASP(input_data, max_iterations=10000, alpha=0.1)
            elif self.config.solver == 'GreedyLocalSearch':
                solver = Solver_GreedyLocalSearch(input_data)
            elif self.config.solver == 'Greedy':
                solver = Solver_Greedy(input_data)
            else:
                raise ValueError(f"Solver '{self.config.solver}' is not supported.")

            # Solve the problem
            if self.config.verbose:
                print(f'Running {self.config.solver} Solver...')
            committee, objective = solver.solve()
            committee.sort()
            print("Selected Committee:", [member + 1 for member in committee])
            return 0
        except Exception as e:
            print('Exception:', e)
            return 1


if __name__ == '__main__':
    # Default path to the configuration file
    default_config_path = Path('config/config.dat')

    # Check if the config file exists
    if not default_config_path.exists():
        print(f"Error: Configuration file not found at '{default_config_path}'.")
        sys.exit(1)

    # Parse the configuration file
    config = DATParser.parse(default_config_path)

    # Process the verbose flag
    if hasattr(config, 'verbose') and isinstance(config.verbose, str):
        config.verbose = config.verbose.lower() == 'true'
    elif not hasattr(config, 'verbose'):
        config.verbose = False

    # Run the main process
    main = Main(config)
    sys.exit(main.run())

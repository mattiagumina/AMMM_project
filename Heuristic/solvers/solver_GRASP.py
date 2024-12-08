import random


class Solver_GRASP:
    def __init__(self, data, max_iterations=50, alpha=0.2):
        """
        Initializes the GRASP solver.
        :param data: Parsed input data containing D, N, n, d, and m.
        :param max_iterations: Number of iterations for the GRASP algorithm.
        :param alpha: Parameter for controlling the greediness vs randomness in the RCL.
        """
        self.N = data.N  # Number of candidates
        self.D = data.D  # Number of departments
        self.n_required = data.n  # List of required members per department
        self.department_list = data.d  # Department assignment for each member
        self.compatibility_matrix = data.m  # Compatibility matrix
        self.max_iterations = max_iterations  # Number of GRASP iterations
        self.alpha = alpha  # RCL parameter
        self.best_committee = []  # Best committee found
        self.best_objective = -1  # Best objective value

        # Local state for current iteration
        self.current_committee = []
        self.dept_count = {i: 0 for i in range(1, self.D + 1)}  # Count of members per department

    def _is_valid_candidate(self, candidate):
        """
        Checks if a candidate is valid for the committee.
        :param candidate: Candidate index.
        :return: True if valid, False otherwise.
        """
        candidate_department = self.department_list[candidate]

        if self.dept_count[candidate_department] >= self.n_required[candidate_department - 1]:
            return False

        if any(self.compatibility_matrix[candidate][member] == 0 for member in self.current_committee):
            return False

        for member in self.current_committee:
            if 0 < self.compatibility_matrix[candidate][member] < 0.15:
                if not any(
                    self.compatibility_matrix[candidate][k] > 0.85 and self.compatibility_matrix[member][k] > 0.85
                    for k in self.current_committee
                ):
                    return False

        return True

    def _calculate_avg_compatibility(self, committee):
        """
        Calculates the average compatibility among all pairs of committee members.
        :param committee: List of committee members.
        :return: Average compatibility.
        """
        if len(committee) < 2:
            return 0  # No pairs to calculate compatibility
        total_compatibility = sum(
            self.compatibility_matrix[i][j] for i in committee for j in committee if i < j
        )
        num_pairs = len(committee) * (len(committee) - 1) / 2
        return total_compatibility / num_pairs

    def _greedy_randomized_construction(self):
        """
        Constructs a solution using a greedy randomized procedure.
        """
        self.current_committee = []
        self.dept_count = {i: 0 for i in range(1, self.D + 1)}

        while len(self.current_committee) < sum(self.n_required):
            candidates = []
            scores = []

            # Evaluate all candidates
            for candidate in range(self.N):
                if candidate not in self.current_committee and self._is_valid_candidate(candidate):
                    total_compatibility = sum(
                        self.compatibility_matrix[candidate][member] for member in self.current_committee
                    )
                    avg_compatibility = total_compatibility / (len(self.current_committee) + 1) if self.current_committee else 1
                    candidates.append(candidate)
                    scores.append(avg_compatibility)

            if not candidates:
                raise ValueError("Unable to form a valid committee under given constraints.")

            # Build Restricted Candidate List (RCL)
            min_score = min(scores)
            max_score = max(scores)
            threshold = max_score - self.alpha * (max_score - min_score)
            rcl = [candidates[i] for i in range(len(candidates)) if scores[i] >= threshold]

            # Select a random candidate from RCL
            selected_candidate = random.choice(rcl)
            self.current_committee.append(selected_candidate)
            self.dept_count[self.department_list[selected_candidate]] += 1

    def _local_search(self):
        """
        Improves the solution by replacing committee members to increase the objective.
        """
        improved = True
        while improved:
            improved = False
            for i in range(len(self.current_committee)):
                for candidate in range(self.N):
                    if candidate in self.current_committee:
                        continue

                    new_committee = self.current_committee[:i] + [candidate] + self.current_committee[i+1:]

                    if self._is_valid_candidate(candidate):
                        current_objective = self._calculate_avg_compatibility(self.current_committee)
                        new_objective = self._calculate_avg_compatibility(new_committee)

                        if new_objective > current_objective:
                            old_member = self.current_committee[i]
                            self.current_committee = new_committee
                            self.dept_count[self.department_list[candidate]] += 1
                            self.dept_count[self.department_list[old_member]] -= 1
                            improved = True
                            break
                if improved:
                    break

    def solve(self):
        """
        Executes the GRASP algorithm.
        :return: Best committee and its objective value.
        """
        for _ in range(self.max_iterations):
            try:
                # Step 1: Construct initial solution
                self._greedy_randomized_construction()

                # Step 2: Improve solution with local search
                self._local_search()

                # Evaluate current solution
                current_objective = self._calculate_avg_compatibility(self.current_committee)

                # Update best solution
                if current_objective > self.best_objective:
                    self.best_committee = list(self.current_committee)
                    self.best_objective = current_objective
            except ValueError:
                continue  # Skip invalid constructions

        print(f"Best Objective: {self.best_objective:.15f}")
        return self.best_committee, self.best_objective

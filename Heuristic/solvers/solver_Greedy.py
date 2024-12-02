class Solver_Greedy:
    def __init__(self, data):
        """
        Initializes the greedy solver.
        :param data: Parsed input data containing D, N, n, d, and m.
        """
        self.N = data.N  # Number of candidates
        self.D = data.D  # Number of departments
        self.n_required = data.n  # List of required members per department
        self.department_list = data.d  # Department assignment for each member
        self.compatibility_matrix = data.m  # Compatibility matrix
        self.committee = []  # Final committee members
        self.dept_count = {i: 0 for i in range(1, self.D + 1)}  # Count of members per department

    def _is_valid_candidate(self, candidate):
        """
        Checks if a candidate is valid for the committee.
        :param candidate: Candidate index.
        :return: True if valid, False otherwise.
        """
        candidate_department = self.department_list[candidate]

        # Check if the department quota is already filled
        if self.dept_count[candidate_department] >= self.n_required[candidate_department - 1]:
            return False

        # Check for incompatible candidates
        if any(self.compatibility_matrix[candidate][member] == 0 for member in self.committee):
            return False

        # Check for conditional compatibility
        for member in self.committee:
            if 0 < self.compatibility_matrix[candidate][member] < 0.15:
                if not any(
                    self.compatibility_matrix[candidate][k] > 0.85 and self.compatibility_matrix[member][k] > 0.85
                    for k in self.committee
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
            self.compatibility_matrix[i][j] for i in committee for j in committee if i != j
        )
        num_pairs = len(committee) * (len(committee) - 1) / 2
        return total_compatibility / num_pairs

    def solve(self):
        """
        Executes the greedy algorithm to select the committee.
        :return: List of selected committee members and the objective value.
        """
        while len(self.committee) < sum(self.n_required):
            best_candidate = None
            best_avg_compatibility = -1

            # Iterate through all candidates
            for candidate in range(self.N):
                if candidate in self.committee:
                    continue

                # Check if candidate is valid
                if self._is_valid_candidate(candidate):
                    total_compatibility = sum(self.compatibility_matrix[candidate][member] for member in self.committee)
                    avg_compatibility = total_compatibility / (len(self.committee) + 1) if self.committee else 1

                    # Select the candidate with the best average compatibility
                    if avg_compatibility > best_avg_compatibility:
                        best_candidate = candidate
                        best_avg_compatibility = avg_compatibility

            # Add the best candidate to the committee
            if best_candidate is not None:
                self.committee.append(best_candidate)
                self.dept_count[self.department_list[best_candidate]] += 1
            else:
                raise ValueError("Unable to form a valid committee under given constraints.")

        # Calculate the objective value
        objective = self._calculate_avg_compatibility(self.committee)
        print(f"Objective: {objective:.2f}")

        return self.committee, objective

class Solver_GreedyLocalSearch:
    def __init__(self, data):
        self.N = data.N
        self.D = data.D
        self.n_required = data.n
        self.department_list = data.d
        self.compatibility_matrix = data.m
        self.committee = []
        self.dept_count = {i: 0 for i in range(1, self.D + 1)}

    def _is_valid_candidate(self, candidate):
        candidate_department = self.department_list[candidate]
        if self.dept_count[candidate_department] >= self.n_required[candidate_department - 1]:
            return False
        if any(self.compatibility_matrix[candidate][member] == 0 for member in self.committee):
            return False
        for member in self.committee:
            if 0 < self.compatibility_matrix[candidate][member] < 0.15:
                if not any(
                    self.compatibility_matrix[candidate][k] > 0.85 and self.compatibility_matrix[member][k] > 0.85
                    for k in self.committee
                ):
                    return False
        return True

    def _calculate_avg_compatibility(self, committee):
        if len(committee) < 2:
            return 0
        total_compatibility = sum(
            self.compatibility_matrix[i][j] for i in committee for j in committee if i != j
        )
        num_pairs = len(committee) * (len(committee) - 1) / 2
        return total_compatibility / num_pairs

    def _greedy_constructive(self):
        while len(self.committee) < sum(self.n_required):
            best_candidate = None
            best_avg_compatibility = -1
            for candidate in range(self.N):
                if candidate in self.committee:
                    continue
                if self._is_valid_candidate(candidate):
                    total_compatibility = sum(self.compatibility_matrix[candidate][member] for member in self.committee)
                    avg_compatibility = total_compatibility / (len(self.committee) + 1) if self.committee else 1
                    if avg_compatibility > best_avg_compatibility:
                        best_candidate = candidate
                        best_avg_compatibility = avg_compatibility
            if best_candidate is not None:
                self.committee.append(best_candidate)
                self.dept_count[self.department_list[best_candidate]] += 1
            else:
                raise ValueError("Unable to form a valid committee under given constraints.")

    def _local_search(self):
        improved = True
        while improved:
            improved = False
            for i in range(len(self.committee)):
                for candidate in range(self.N):
                    if candidate in self.committee:
                        continue
                    new_committee = self.committee[:i] + [candidate] + self.committee[i+1:]
                    if self._is_valid_candidate(candidate):
                        current_objective = self._calculate_avg_compatibility(self.committee)
                        new_objective = self._calculate_avg_compatibility(new_committee)
                        if new_objective > current_objective:
                            old_member = self.committee[i]
                            self.committee = new_committee
                            self.dept_count[self.department_list[candidate]] += 1
                            self.dept_count[self.department_list[old_member]] -= 1
                            improved = True
                            break
                if improved:
                    break

    def solve(self):
        self._greedy_constructive()
        self._local_search()
        objective = self._calculate_avg_compatibility(self.committee)
        print(f"Objective: {objective:.2f}")
        return self.committee, objective

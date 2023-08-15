class Relocation_move:
    def __init__(self, solution, matrix, capacity):
        self.sol = solution
        self.cost_matrix = matrix
        self.capacity = capacity

        self.origin_rt_pos = None
        self.target_rt_pos = None
        self.selected_node1_pos = None
        self.selected_node2_pos = None
        self.cost_change_origin_rt = None
        self.cost_change_target_rt = None
        self.move_cost_difference = 10**9    
    
    def reset(self):
        self.origin_rt_pos = None
        self.target_rt_pos = None
        self.selected_node1_pos = None
        self.selected_node2_pos = None
        self.cost_change_origin_rt = None
        self.cost_change_target_rt = None
        self.move_cost_difference = 10**9

    def find_best_relocation_move(self):
        for rt1_index in range(len(self.sol.routes)):
            origin_rt = self.sol.routes[rt1_index]
            time_so_far_in_origin_rt = 0

            for node1_index_in_origin_rt in range(1, len(origin_rt.nodes_sequence)):
                tmp_node1_rt1 = origin_rt.nodes_sequence[node1_index_in_origin_rt-1]
                tmp_node2_rt1 = origin_rt.nodes_sequence[node1_index_in_origin_rt]
                time_so_far_in_origin_rt += self.cost_matrix[tmp_node1_rt1.id][tmp_node2_rt1.id] + tmp_node2_rt1.uploading_time
                
                for rt2_index in range(len(self.sol.routes)):
                    target_rt = self.sol.routes[rt2_index]
                    time_so_far_in_target_rt = 0

                    for node2_index_in_target_rt in range(1,len(target_rt.nodes_sequence)):
                        tmp_node1_rt2 = target_rt.nodes_sequence[node2_index_in_target_rt-1]
                        tmp_node2_rt2 = target_rt.nodes_sequence[node2_index_in_target_rt]
                        time_so_far_in_target_rt += self.cost_matrix[tmp_node1_rt2.id][tmp_node2_rt2.id] + tmp_node2_rt2.uploading_time
                    
                        if origin_rt == target_rt and (node1_index_in_origin_rt==node2_index_in_target_rt or node1_index_in_origin_rt-1==node2_index_in_target_rt):
                            continue

                        #Nodes and multiplier for origin_route
                        is_last1 = (len(origin_rt.nodes_sequence)-node1_index_in_origin_rt-1) == 0
                        p1 = origin_rt.nodes_sequence[node1_index_in_origin_rt - 1]
                        s1 = origin_rt.nodes_sequence[node1_index_in_origin_rt]
                        if is_last1 is False:
                            n1 = origin_rt.nodes_sequence[node1_index_in_origin_rt + 1]
                        cost_multiplier1 = len(origin_rt.nodes_sequence) - node1_index_in_origin_rt

                        #Nodes and multiplier for target_route
                        is_last2 = (len(target_rt.nodes_sequence)-node2_index_in_target_rt-1) == 0
                        s2 = target_rt.nodes_sequence[node2_index_in_target_rt]
                        if is_last2 is False:
                            n2 = target_rt.nodes_sequence[node2_index_in_target_rt + 1]
                        cost_multiplier2 = len(target_rt.nodes_sequence) - node2_index_in_target_rt

                        total_move_cost_differce = None
                        origin_route_cost_difference = None
                        target_route_cost_difference = None

                        if origin_rt == target_rt:                          
                            cost_added_rt2, cost_removed_rt2 = 0, 0

                            if node2_index_in_target_rt > node1_index_in_origin_rt:
                                inclusive_time_from_s1_to_s2 = 0
                                for i in range(node1_index_in_origin_rt +1, node2_index_in_target_rt):
                                    tmp_node1 = origin_rt.nodes_sequence[i]
                                    tmp_node2 = origin_rt.nodes_sequence[i+1]
                                    inclusive_time_from_s1_to_s2 += self.cost_matrix[tmp_node1.id][tmp_node2.id] + tmp_node1.uploading_time

                                cost_removed_rt1 = cost_multiplier1 * self.cost_matrix[p1.id][s1.id]
                                cost_removed_rt1 += (cost_multiplier1-1) * self.cost_matrix[s1.id][n1.id]
                                cost_removed_rt1 += (cost_multiplier1 - cost_multiplier2) * s1.uploading_time
                                cost_added_rt1 = cost_multiplier1 * self.cost_matrix[p1.id][n1.id]
                                cost_added_rt1 += cost_multiplier2 * self.cost_matrix[s2.id][s1.id]
                                cost_added_rt1 += inclusive_time_from_s1_to_s2
                                cost_added_rt1 += s2.uploading_time
                                if is_last2 is False:
                                    cost_added_rt1 += (cost_multiplier2-1) * self.cost_matrix[s1.id][n2.id]
                                    cost_removed_rt1 += (cost_multiplier2-1) * self.cost_matrix[s2.id][n2.id]
                            else:
                                inclusive_time_from_s2_to_s1 = 0
                                for i in range(node2_index_in_target_rt +1, node1_index_in_origin_rt - 1):
                                    tmp_node1 = origin_rt.nodes_sequence[i]
                                    tmp_node2 = origin_rt.nodes_sequence[i+1]
                                    inclusive_time_from_s2_to_s1 += self.cost_matrix[tmp_node1.id][tmp_node2.id] + tmp_node1.uploading_time
                                inclusive_time_from_s2_to_s1 += p1.uploading_time
                                                                
                                cost_removed_rt1 = cost_multiplier1 * self.cost_matrix[p1.id][s1.id]
                                cost_removed_rt1 += (cost_multiplier2-1) * self.cost_matrix[s2.id][n2.id]
                                cost_removed_rt1 += inclusive_time_from_s2_to_s1
                                cost_added_rt1 = (cost_multiplier2-1) * self.cost_matrix[s2.id][s1.id]
                                cost_added_rt1 += (cost_multiplier2-2) * self.cost_matrix[s1.id][n2.id]
                                cost_added_rt1 += (cost_multiplier2 - 1 - cost_multiplier1) * s1.uploading_time
                                if is_last1 is False:
                                    cost_added_rt1 += (cost_multiplier1-1) * self.cost_matrix[p1.id][n1.id]
                                    cost_removed_rt1 += (cost_multiplier1-1) * self.cost_matrix[s1.id][n1.id]                                
                        else:
                            if target_rt.load + s1.demand > origin_rt.capacity:
                                continue

                            if is_last1 is True:
                                cost_removed_rt1 = time_so_far_in_origin_rt
                                cost_added_rt1 = 0
                            elif is_last2 is False:
                                cost_removed_rt1 = time_so_far_in_origin_rt
                                cost_removed_rt1 += (cost_multiplier1-1) * (self.cost_matrix[p1.id][s1.id] + s1.uploading_time)
                                cost_removed_rt1 += (cost_multiplier1-1) * self.cost_matrix[s1.id][n1.id]
                                cost_added_rt1 = (cost_multiplier1-1) * self.cost_matrix[p1.id][n1.id]

                            if is_last2 is True:
                                cost_removed_rt2 = 0
                                cost_added_rt2 = cost_multiplier2 * (self.cost_matrix[s2.id][s1.id] + s1.uploading_time)
                                cost_added_rt2 += time_so_far_in_target_rt
                            elif is_last2 is False:
                                cost_removed_rt2 = (cost_multiplier2-1) * self.cost_matrix[s2.id][n2.id]
                                cost_added_rt2 = time_so_far_in_target_rt
                                cost_added_rt2 += cost_multiplier2 * (self.cost_matrix[s2.id][s1.id] + s1.uploading_time)
                                cost_added_rt2 += (cost_multiplier2-1) * self.cost_matrix[s1.id][n2.id]

                        origin_route_cost_difference = cost_added_rt1 - cost_removed_rt1
                        target_route_cost_difference = cost_added_rt2 - cost_removed_rt2
                        total_move_cost_differce = origin_route_cost_difference + target_route_cost_difference

                        if total_move_cost_differce < self.move_cost_difference:
                            self.origin_rt_pos = rt1_index
                            self.target_rt_pos = rt2_index
                            self.selected_node1_pos = node1_index_in_origin_rt
                            self.selected_node2_pos = node2_index_in_target_rt
                            self.cost_change_origin_rt = origin_route_cost_difference
                            self.cost_change_target_rt = target_route_cost_difference
                            self.move_cost_difference = total_move_cost_differce

    def apply_relocation_move(self):
        origin_route = self.sol.routes[self.origin_rt_pos]
        target_route = self.sol.routes[self.target_rt_pos]
        selected_node1 = origin_route.nodes_sequence[self.selected_node1_pos]

        if origin_route == target_route:
            del origin_route.nodes_sequence[self.selected_node1_pos]
            if (self.selected_node1_pos < self.selected_node2_pos):
                target_route.nodes_sequence.insert(self.selected_node2_pos, selected_node1)
            else:
                target_route.nodes_sequence.insert(self.selected_node2_pos + 1, selected_node1) #den vrike gia seed=39, vrike gia seed=3, swsto me +1 gia selected_node1_pos > selected_node2_pos      
        else:
            del origin_route.nodes_sequence[self.selected_node1_pos]
            target_route.nodes_sequence.insert(self.selected_node2_pos + 1, selected_node1)
            origin_route.load -= selected_node1.demand
            target_route.load += selected_node1.demand

        origin_route.cumulative_cost += self.cost_change_origin_rt
        target_route.cumulative_cost += self.cost_change_target_rt
        self.sol.cost += self.move_cost_difference

#iterations: 13 31924.448077515277
class TwoOpt_move:
    def __init__(self, solution, matrix, capacity):
        self.sol = solution
        self.cost_matrix = matrix
        self.capacity = capacity

        self.route1_pos = None
        self.route2_pos = None
        self.origin_node1_pos = None
        self.target_node2_pos = None
        self.cost_change_route1 = None
        self.cost_change_route2 = None
        self.route1_new_load = None
        self.route2_new_load = None
        self.move_cost_difference = 10**9
    
    def reset(self):
        self.route1_pos = None
        self.route2_pos = None
        self.origin_node1_pos = None
        self.target_node2_pos = None
        self.cost_change_route1 = None
        self.cost_change_route2 = None
        self.route1_new_load = None
        self.route2_new_load = None
        self.move_cost_difference = 10**9


    def find_best_two_opt(self):
        for rt1_index in range(len(self.sol.routes)):
            route1 = self.sol.routes[rt1_index]

            for rt2_index in range(len(self.sol.routes)):
                route2 = self.sol.routes[rt2_index]
                rt1_time_cost_so_far = 0
                rt1_calc_cost_so_far = 0
                rt1_load_so_far = 0              
                
                for node1_index_in_route1 in range(len(route1.nodes_sequence)-1):
                    if node1_index_in_route1 != 0:
                        tmp_node1_rt1 = route1.nodes_sequence[node1_index_in_route1 - 1]
                        tmp_node2_rt1 = route1.nodes_sequence[node1_index_in_route1]
                        rt1_time_cost_so_far += self.cost_matrix[tmp_node1_rt1.id][tmp_node2_rt1.id] + tmp_node2_rt1.uploading_time
                        rt1_calc_cost_so_far += rt1_time_cost_so_far
                        rt1_load_so_far += tmp_node2_rt1.demand
                                      
                    start_node2_index = 0
                    if rt1_index == rt2_index:
                        start_node2_index = node1_index_in_route1 + 2
                    rt2_time_cost_so_far = 0
                    rt2_calc_cost_so_far = 0
                    rt2_load_so_far = 0

                    for node2_index_in_route2 in range(start_node2_index, len(route2.nodes_sequence)-1):
                        if node2_index_in_route2 != 0:
                            tmp_node1_rt2 = route2.nodes_sequence[node2_index_in_route2 - 1]
                            tmp_node2_rt2 = route2.nodes_sequence[node2_index_in_route2]
                            rt2_time_cost_so_far += self.cost_matrix[tmp_node1_rt2.id][tmp_node2_rt2.id] + tmp_node2_rt2.uploading_time
                            rt2_calc_cost_so_far += rt2_time_cost_so_far
                            rt2_load_so_far += tmp_node2_rt2.demand

                        #Nodes and multiplier for route1
                        s1 = route1.nodes_sequence[node1_index_in_route1]
                        n1 = route1.nodes_sequence[node1_index_in_route1 + 1]
                        cost_multiplier1 = len(route1.nodes_sequence) - node1_index_in_route1

                        #Nodes and multiplier for route2                                                
                        s2 = route2.nodes_sequence[node2_index_in_route2 ]
                        n2 = route2.nodes_sequence[node2_index_in_route2 + 1]
                        cost_multiplier2 = len(route2.nodes_sequence) - node2_index_in_route2

                        if route1 == route2:
                            rt1_new_load, changed_rt1 = 0, 0
                            rt2_new_load, changed_rt2 = 0, 0
                            if node1_index_in_route1 and node2_index_in_route2 == len(route1.nodes_sequence) - 1:
                                continue
                            
                            cost_removed_rt2, cost_added_rt2 = 0, 0
                            cost_removed_rt1 = (cost_multiplier1-1) * self.cost_matrix[s1.id][n1.id] + (cost_multiplier2-1) * self.cost_matrix[s2.id][n2.id]
                            cost_added_rt1 = (cost_multiplier1-1) * self.cost_matrix[s1.id][s2.id] + (cost_multiplier2-1) * self.cost_matrix[n1.id][n2.id]

                            #Calculate route cost: from n1 to s1 (remove)
                            multiplier_decreaser = 1
                            for i in range(node1_index_in_route1 + 1, node2_index_in_route2):
                                tmp_node1 = route1.nodes_sequence[i]
                                tmp_node2 = route1.nodes_sequence[i+1]
                                cost_removed_rt1 += (cost_multiplier1-multiplier_decreaser) * self.cost_matrix[tmp_node1.id][tmp_node2.id]
                                multiplier_decreaser += 1

                            #Calculate REVERSED route cost: from n1 to s1 (add)
                            multiplier_increaser = cost_multiplier1 - 1
                            for i in range(node2_index_in_route2, node1_index_in_route1 + 1, -1):
                                tmp_node1 = route1.nodes_sequence[i]
                                tmp_node2 = route1.nodes_sequence[i-1]
                                cost_added_rt1 += multiplier_increaser * self.cost_matrix[tmp_node1.id][tmp_node2.id]
                                multiplier_increaser -= 1
                        
                        else:                            
                            route1_load_second_segment = route1.load - rt1_load_so_far
                            route2_load_second_segment = route2.load - rt2_load_so_far
                            rt1_new_load = rt1_load_so_far + route2_load_second_segment
                            rt2_new_load = rt2_load_so_far + route1_load_second_segment
                            if rt1_new_load > self.capacity:
                                continue
                            if rt2_new_load > self.capacity:
                                continue
                            
                            #Calculate route1 cost: second_segment
                            route1_length_second_segment = 1
                            time_cost1 = 0
                            route1_calc_cost_second_segment = 0
                            for i in range(node1_index_in_route1 + 1, len(route1.nodes_sequence)-1):
                                temp_node1 = route1.nodes_sequence[i]
                                temp_node2 = route1.nodes_sequence[i+1]                                
                                time_cost1 += self.cost_matrix[temp_node1.id][temp_node2.id] + temp_node2.uploading_time
                                route1_calc_cost_second_segment += time_cost1
                                route1_length_second_segment += 1

                            #Calculate route2 cost: second_segment
                            route2_length_second_segment = 1                            
                            time_cost2 = 0
                            route2_calc_cost_second_segment = 0 
                            for i in range(node2_index_in_route2 + 1, len(route2.nodes_sequence)-1):
                                temp_node11 = route2.nodes_sequence[i]
                                temp_node22 = route2.nodes_sequence[i+1]                                
                                time_cost2 += self.cost_matrix[temp_node11.id][temp_node22.id] + temp_node22.uploading_time
                                route2_calc_cost_second_segment += time_cost2
                                route2_length_second_segment += 1
                                                                                    
                            cost_removed_rt1 = route1_calc_cost_second_segment
                            cost_removed_rt1 += (cost_multiplier1 - 1) * (self.cost_matrix[s1.id][n1.id] + n1.uploading_time)
                            cost_added_rt1 = (cost_multiplier2 - 1) * (self.cost_matrix[s1.id][n2.id] + n2.uploading_time)
                            cost_added_rt1 += route2_calc_cost_second_segment                                                        
                            changed_rt1 = (cost_multiplier2-cost_multiplier1) * rt1_time_cost_so_far

                            cost_removed_rt2 = route2_calc_cost_second_segment
                            cost_removed_rt2 += (cost_multiplier2 - 1) * (self.cost_matrix[s2.id][n2.id] + n2.uploading_time)
                            cost_added_rt2 = (cost_multiplier1 - 1) * (self.cost_matrix[s2.id][n1.id] + n1.uploading_time)
                            cost_added_rt2 += route1_calc_cost_second_segment
                            changed_rt2 = (cost_multiplier1 - cost_multiplier2) * rt2_time_cost_so_far
                                                                                   
                        cost_change_route1 = cost_added_rt1 - cost_removed_rt1 + changed_rt1
                        cost_change_route2 = cost_added_rt2 - cost_removed_rt2 + changed_rt2
                        total_move_cost_difference = cost_change_route1 + cost_change_route2

                        if total_move_cost_difference < self.move_cost_difference:
                            self.route1_pos = rt1_index
                            self.route2_pos = rt2_index
                            self.origin_node_pos = node1_index_in_route1
                            self.target_node_pos = node2_index_in_route2
                            self.cost_change_route1 = cost_change_route1
                            self.cost_change_route2 = cost_change_route2
                            self.route1_new_load = rt1_new_load
                            self.route2_new_load = rt2_new_load
                            self.move_cost_difference = total_move_cost_difference

    def apply_two_opt_move(self):
        route1 = self.sol.routes[self.route1_pos]
        route2 = self.sol.routes[self.route2_pos]
        
        if route1 == route2:
            reversed_segment = reversed(route1.nodes_sequence[self.origin_node_pos + 1: self.target_node_pos + 1])
            route1.nodes_sequence[self.origin_node_pos + 1 : self.target_node_pos + 1] = reversed_segment
        else:
            relocatedSegmentOfRt1 = route1.nodes_sequence[self.origin_node_pos + 1 :]
            relocatedSegmentOfRt2 = route2.nodes_sequence[self.target_node_pos + 1 :]
            del route1.nodes_sequence[self.origin_node_pos + 1 :]
            del route2.nodes_sequence[self.target_node_pos + 1 :]
            route1.nodes_sequence.extend(relocatedSegmentOfRt2)
            route2.nodes_sequence.extend(relocatedSegmentOfRt1)
            route1.load = self.route1_new_load
            route2.load = self.route2_new_load
            
        route1.cumulative_cost += self.cost_change_route1
        route2.cumulative_cost += self.cost_change_route2 
        self.sol.cost += self.move_cost_difference

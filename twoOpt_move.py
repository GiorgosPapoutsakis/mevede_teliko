#iterations: 16 32234.708521766195
class TwoOpt_move:
    def __init__(self, solution, matrix, capacity):
        self.sol = solution
        self.cost_matrix = matrix
        self.capacity = capacity

        self.origin_rt_pos = None
        self.target_rt_pos = None
        self.origin_node1_pos = None
        self.target_node2_pos = None
        self.cost_change_origin_rt = None
        self.cost_change_target_rt = None
        self.origin_rt_new_load = None
        self.target_rt_new_load = None
        self.move_cost_difference = 10**9
    
    def reset(self):
        self.origin_rt_pos = None
        self.target_rt_pos = None
        self.origin_node1_pos = None
        self.target_node2_pos = None
        self.cost_change_origin_rt = None
        self.cost_change_target_rt = None
        self.origin_rt_new_load = None
        self.target_rt_new_load = None
        self.move_cost_difference = 10**9


    def find_best_two_opt(self):
        for rt1_index in range(len(self.sol.routes)):
            origin_rt = self.sol.routes[rt1_index]

            for rt2_index in range(len(self.sol.routes)):
                target_rt = self.sol.routes[rt2_index]
                rt1_time_cost_so_far = 0
                rt1_calc_cost_so_far = 0
                rt1_load_so_far = 0              
                
                for node1_index_in_origin_rt in range(len(origin_rt.nodes_sequence)-1):
                    if node1_index_in_origin_rt != 0:
                        tmp_node1_rt1 = origin_rt.nodes_sequence[node1_index_in_origin_rt - 1]
                        tmp_node2_rt1 = origin_rt.nodes_sequence[node1_index_in_origin_rt]
                        rt1_time_cost_so_far += self.cost_matrix[tmp_node1_rt1.id][tmp_node2_rt1.id] + tmp_node2_rt1.uploading_time
                        rt1_calc_cost_so_far += rt1_time_cost_so_far
                        rt1_load_so_far += tmp_node2_rt1.demand
                                      
                    start_node2_index = 0
                    if rt1_index == rt2_index:
                        start_node2_index = node1_index_in_origin_rt + 2
                    rt2_time_cost_so_far = 0
                    rt2_calc_cost_so_far = 0
                    rt2_load_so_far = 0

                    for node2_index_in_target_rt in range(start_node2_index, len(target_rt.nodes_sequence)-1):
                        if node2_index_in_target_rt != 0:
                            tmp_node1_rt2 = target_rt.nodes_sequence[node2_index_in_target_rt - 1]
                            tmp_node2_rt2 = target_rt.nodes_sequence[node2_index_in_target_rt]
                            rt2_time_cost_so_far += self.cost_matrix[tmp_node1_rt2.id][tmp_node2_rt2.id] + tmp_node2_rt2.uploading_time
                            rt2_calc_cost_so_far += rt2_time_cost_so_far
                            rt2_load_so_far += tmp_node2_rt2.demand


                        s1 = origin_rt.nodes_sequence[node1_index_in_origin_rt]
                        n1 = origin_rt.nodes_sequence[node1_index_in_origin_rt + 1]
                        cost_multiplier1 = len(origin_rt.nodes_sequence) - node1_index_in_origin_rt
                                                
                        s2 = target_rt.nodes_sequence[node2_index_in_target_rt ]
                        n2 = target_rt.nodes_sequence[node2_index_in_target_rt + 1]
                        cost_multiplier2 = len(target_rt.nodes_sequence) - node2_index_in_target_rt

                        if origin_rt == target_rt:
                            rt1_new_load, changed_rt1 = 0, 0
                            rt2_new_load, changed_rt2 = 0, 0
                            if node1_index_in_origin_rt and node2_index_in_target_rt == len(origin_rt.nodes_sequence) - 1:
                                continue
                            
                            cost_removed_rt2, cost_added_rt2 = 0, 0
                            cost_removed_rt1 = (cost_multiplier1-1) * self.cost_matrix[s1.id][n1.id] + (cost_multiplier2-1) * self.cost_matrix[s2.id][n2.id]
                            cost_added_rt1 = (cost_multiplier1-1) * self.cost_matrix[s1.id][s2.id] + (cost_multiplier2-1) * self.cost_matrix[n1.id][n2.id]

                            #Calculate route cost: from n1 to s1 to remove
                            multiplier_decreaser = 1
                            for i in range(node1_index_in_origin_rt + 1, node2_index_in_target_rt):
                                tmp_node1 = origin_rt.nodes_sequence[i]
                                tmp_node2 = origin_rt.nodes_sequence[i+1]
                                cost_removed_rt1 += (cost_multiplier1-multiplier_decreaser) * self.cost_matrix[tmp_node1.id][tmp_node2.id]
                                multiplier_decreaser += 1

                            #Calculate REVERSED route cost: from n1 to s1 to add
                            multiplier_increaser = cost_multiplier1 - 1
                            for i in range(node2_index_in_target_rt, node1_index_in_origin_rt + 1, -1):
                                tmp_node1 = origin_rt.nodes_sequence[i]
                                tmp_node2 = origin_rt.nodes_sequence[i-1]
                                cost_added_rt1 += multiplier_increaser * self.cost_matrix[tmp_node1.id][tmp_node2.id]
                                multiplier_increaser -= 1
                        
                        else:                            
                            origin_rt_load_second_segment = origin_rt.load - rt1_load_so_far
                            target_rt_load_second_segment = target_rt.load - rt2_load_so_far
                            rt1_new_load = rt1_load_so_far + target_rt_load_second_segment
                            rt2_new_load = rt2_load_so_far + origin_rt_load_second_segment
                            if rt1_new_load > self.capacity:
                                continue
                            if rt2_new_load > self.capacity:
                                continue
                            
                            #Calculate route1 cost: second_segment
                            origin_rt_length_second_segment = 1
                            time_cost1 = 0
                            origin_rt_calc_cost_second_segment = 0
                            for i in range(node1_index_in_origin_rt + 1, len(origin_rt.nodes_sequence)-1):
                                temp_node1 = origin_rt.nodes_sequence[i]
                                temp_node2 = origin_rt.nodes_sequence[i+1]                                
                                time_cost1 += self.cost_matrix[temp_node1.id][temp_node2.id] + temp_node2.uploading_time
                                origin_rt_calc_cost_second_segment += time_cost1
                                origin_rt_length_second_segment += 1

                            #Calculate route2 cost: second_segment
                            target_rt_length_second_segment = 1                            
                            time_cost2 = 0
                            target_rt_calc_cost_second_segment = 0 
                            for i in range(node2_index_in_target_rt + 1, len(target_rt.nodes_sequence)-1):
                                temp_node11 = target_rt.nodes_sequence[i]
                                temp_node22 = target_rt.nodes_sequence[i+1]                                
                                time_cost2 += self.cost_matrix[temp_node11.id][temp_node22.id] + temp_node22.uploading_time
                                target_rt_calc_cost_second_segment += time_cost2
                                target_rt_length_second_segment += 1
                                                                                    
                            cost_removed_rt1 = origin_rt_calc_cost_second_segment
                            cost_removed_rt1 += (cost_multiplier1 - 1) * (self.cost_matrix[s1.id][n1.id] + n1.uploading_time)
                            cost_added_rt1 = (cost_multiplier2 - 1) * (self.cost_matrix[s1.id][n2.id] + n2.uploading_time)
                            cost_added_rt1 += target_rt_calc_cost_second_segment                                                        
                            changed_rt1 = (cost_multiplier2-cost_multiplier1) * rt1_time_cost_so_far

                            cost_removed_rt2 = target_rt_calc_cost_second_segment
                            cost_removed_rt2 += (cost_multiplier2 - 1) * (self.cost_matrix[s2.id][n2.id] + n2.uploading_time)
                            cost_added_rt2 = (cost_multiplier1 - 1) * (self.cost_matrix[s2.id][n1.id] + n1.uploading_time)
                            cost_added_rt2 += origin_rt_calc_cost_second_segment
                            changed_rt2 = (cost_multiplier1 - cost_multiplier2) * rt2_time_cost_so_far
                                                                                   
                        cost_change_origin_rt = cost_added_rt1 - cost_removed_rt1 + changed_rt1
                        cost_change_target_rt = cost_added_rt2 - cost_removed_rt2 + changed_rt2
                        total_move_cost_differce = cost_added_rt1 + cost_added_rt2 - (cost_removed_rt1 + cost_removed_rt2) + changed_rt1 + changed_rt2

                        if total_move_cost_differce < self.move_cost_difference:
                            self.origin_rt_pos = rt1_index
                            self.target_rt_pos = rt2_index
                            self.origin_node_pos = node1_index_in_origin_rt
                            self.target_node_pos = node2_index_in_target_rt
                            self.cost_change_origin_rt = cost_change_origin_rt
                            self.cost_change_target_rt = cost_change_target_rt
                            self.origin_rt_new_load = rt1_new_load
                            self.target_rt_new_load = rt2_new_load
                            self.move_cost_difference = total_move_cost_differce

    def apply_two_opt_move(self):
        origin_route = self.sol.routes[self.origin_rt_pos]
        target_route = self.sol.routes[self.target_rt_pos]
        
        if origin_route == target_route:
            reversed_segment = reversed(origin_route.nodes_sequence[self.origin_node_pos + 1: self.target_node_pos + 1])
            origin_route.nodes_sequence[self.origin_node_pos + 1 : self.target_node_pos + 1] = reversed_segment
        else:
            relocatedSegmentOfRt1 = origin_route.nodes_sequence[self.origin_node_pos + 1 :]
            relocatedSegmentOfRt2 = target_route.nodes_sequence[self.target_node_pos + 1 :]
            del origin_route.nodes_sequence[self.origin_node_pos + 1 :]
            del target_route.nodes_sequence[self.target_node_pos + 1 :]
            origin_route.nodes_sequence.extend(relocatedSegmentOfRt2)
            target_route.nodes_sequence.extend(relocatedSegmentOfRt1)
            origin_route.load = self.origin_rt_new_load
            target_route.load = self.target_rt_new_load
            
        origin_route.cumulative_cost += self.cost_change_origin_rt
        target_route.cumulative_cost += self.cost_change_target_rt 
        self.sol.cost += self.move_cost_difference

    def calculate_route_details(self,message,route, route_pos):
        load = 0
        timecost = 0
        calccost = 0
        numberOfNodes = 0
        nodes_in_route = [0]
        for i in range(0, len(route.nodes_sequence)-1):
            node1 = route.nodes_sequence[i]
            node2 = route.nodes_sequence[i+1]
            dist_cost = self.cost_matrix[node1.id][node2.id] + node2.uploading_time
            timecost += dist_cost
            calccost += timecost
            load += node2.demand
            numberOfNodes += 1
            nodes_in_route.append(node2.id)
        print()
        print("ROUTEDETAILS:",route_pos, message,"calcCost, nodes_in_route, numberOfNodes", calccost, nodes_in_route, numberOfNodes)
        print()
    
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
                        node1 = origin_rt.nodes_sequence[node1_index_in_origin_rt - 1]
                        node2 = origin_rt.nodes_sequence[node1_index_in_origin_rt]
                        cost_from_1_to_2 = self.cost_matrix[node1.id][node2.id] + node2.uploading_time
                        rt1_time_cost_so_far += cost_from_1_to_2
                        rt1_calc_cost_so_far += rt1_time_cost_so_far
                        rt1_load_so_far += node2.demand

                    rt2_time_cost_so_far = 0
                    rt2_calc_cost_so_far = 0
                    rt2_load_so_far = 0                                       
                    start_node2_index = 0
                    if rt1_index == rt2_index:
                        start_node2_index = node1_index_in_origin_rt + 2
                    for node2_index_in_target_rt in range(start_node2_index, len(target_rt.nodes_sequence)-1):
                        if node2_index_in_target_rt != 0:
                            node11 = target_rt.nodes_sequence[node2_index_in_target_rt - 1]
                            node22 = target_rt.nodes_sequence[node2_index_in_target_rt]
                            cost_from_11_to_22 = self.cost_matrix[node11.id][node22.id] + node22.uploading_time
                            rt2_time_cost_so_far += cost_from_11_to_22
                            rt2_calc_cost_so_far += rt2_time_cost_so_far
                            rt2_load_so_far += node22.demand


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

                            minus_multiplier = 1
                            for i in range(node1_index_in_origin_rt + 1, node2_index_in_target_rt):
                                node1 = origin_rt.nodes_sequence[i]
                                node2 = origin_rt.nodes_sequence[i+1]
                                cost_removed_rt1 += (cost_multiplier1-minus_multiplier) * self.cost_matrix[node1.id][node2.id]
                                minus_multiplier += 1

                            adder_multiplier = cost_multiplier1 - 1
                            for i in range(node2_index_in_target_rt, node1_index_in_origin_rt + 1, -1):
                                node1 = origin_rt.nodes_sequence[i]
                                node2 = origin_rt.nodes_sequence[i-1]
                                cost_added_rt1 += (adder_multiplier) * self.cost_matrix[node1.id][node2.id]
                                adder_multiplier -= 1
                        else:
                            # print("CHECK0",origin_rt.cumulative_cost, rt1_calc_cost_so_far, origin_rt.cumulative_cost-rt1_calc_cost_so_far)
                            # print("CHECK0.1",target_rt.cumulative_cost, rt2_calc_cost_so_far, target_rt.cumulative_cost-rt2_calc_cost_so_far)
                            
                            origin_rt_load_second_segment = origin_rt.load - rt1_load_so_far
                            target_rt_load_second_segment = target_rt.load - rt2_load_so_far
                            rt1_new_load = rt1_load_so_far + target_rt_load_second_segment
                            rt2_new_load = rt2_load_so_far + origin_rt_load_second_segment
                            #print("loads1", origin_rt.load, rt1_load_so_far, origin_rt_load_second_segment)
                            #print("loads2", target_rt.load, rt2_load_so_far, target_rt_load_second_segment)
                            if rt1_new_load > self.capacity:
                                continue
                            if rt2_new_load > self.capacity:
                                continue
                            

                            #print("TEST IF CORRECT LOAD, myLoad, functionLoad", rt2_load_so_far, self.calculate_loadSoFar_until_nodeIndex_for_route(target_rt,node2_index_in_target_rt) )
                            #rt1_load_so_far CORRECT
                            #rt2_load_so_far CORRECT

                            #print("TEST IF CORRECT TIME COST, myCost, functionCost", rt2_time_cost_so_far, self.calculate_timeCostSoFar_until_nodeIndex_for_route(target_rt,node2_index_in_target_rt) )
                            #rt1_time_cost_so_far CORRECT
                            #rt2_time_cost_so_far CORRECT

                            origin_rt_length_second_segment = 1
                            time_cost1 = 0
                            origin_rt_calc_cost_second_segment = 0
                            for i in range(node1_index_in_origin_rt + 1, len(origin_rt.nodes_sequence)-1):
                                temp_node1 = origin_rt.nodes_sequence[i]
                                temp_node2 = origin_rt.nodes_sequence[i+1]                                
                                time_cost1 += self.cost_matrix[temp_node1.id][temp_node2.id] + temp_node2.uploading_time
                                origin_rt_calc_cost_second_segment += time_cost1
                                origin_rt_length_second_segment += 1

                            target_rt_length_second_segment = 1                            
                            time_cost2 = 0
                            target_rt_calc_cost_second_segment = 0 
                            for i in range(node2_index_in_target_rt + 1, len(target_rt.nodes_sequence)-1):
                                temp_node11 = target_rt.nodes_sequence[i]
                                temp_node22 = target_rt.nodes_sequence[i+1]                                
                                time_cost2 += self.cost_matrix[temp_node11.id][temp_node22.id] + temp_node22.uploading_time
                                target_rt_calc_cost_second_segment += time_cost2
                                target_rt_length_second_segment += 1

                            #print("TEST IF CORRECT 2nd_segment_cCost, myCost, functionCost", target_rt_calc_cost_second_segment, self.calculate_cumulativeCost_from_nodeIndex_until_end_of_route(target_rt, node2_index_in_target_rt + 1))
                            #rt1_2nd_segment_cCost CORRECT
                            #rt2_2nd_segment_cCost CORRECT

                            #route1 + route2_secondSegment                                                                                    
                            cost_removed_rt1 = origin_rt_calc_cost_second_segment
                            cost_removed_rt1 += (cost_multiplier1 - 1) * (self.cost_matrix[s1.id][n1.id] + n1.uploading_time)

                            cost_added_rt1 = (cost_multiplier2 - 1) * (self.cost_matrix[s1.id][n2.id] + n2.uploading_time)
                            cost_added_rt1 += target_rt_calc_cost_second_segment

                                                        
                            changed_rt1 = (cost_multiplier2-cost_multiplier1) * rt1_time_cost_so_far
                            changed_rt2 = (cost_multiplier1 - cost_multiplier2) * rt2_time_cost_so_far

                            #route2 + route1_secondSegment
                            cost_removed_rt2 = target_rt_calc_cost_second_segment
                            cost_removed_rt2 += (cost_multiplier2 - 1) * (self.cost_matrix[s2.id][n2.id] + n2.uploading_time)

                            cost_added_rt2 = (cost_multiplier1 - 1) * (self.cost_matrix[s2.id][n1.id] + n1.uploading_time)
                            cost_added_rt2 += origin_rt_calc_cost_second_segment

                                                       
                            #print("CHECK1",cost_added_rt1, cost_added_rt2, cost_removed_rt1, cost_removed_rt2, cost_added_rt1+cost_added_rt2-(cost_removed_rt1+cost_removed_rt2))
                            #print("CHECK2", cost_added_rt1 + cost_added_rt2 - (cost_removed_rt1 + cost_removed_rt2) )

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
            origin_route.cumulative_cost += self.cost_change_origin_rt
        else:
            #self.calculate_route_details("origin_route_before",origin_route, self.origin_rt_pos + 1 )
            #self.calculate_route_details("target_route_before",target_route, self.target_rt_pos + 1)
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
            #self.calculate_route_details("origin_route_after",origin_route, self.origin_rt_pos + 1)
            #self.calculate_route_details("target_route_after",target_route, self.target_rt_pos + 1)
 

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

    def calculate_timeCostSoFar_until_nodeIndex_for_route(self, route, node_index_in_route):
        timecost = 0
        for i in range(0, node_index_in_route):
            node1 = route.nodes_sequence[i]
            node2 = route.nodes_sequence[i+1]
            dist_cost = self.cost_matrix[node1.id][node2.id] + node2.uploading_time
            timecost += dist_cost
        return timecost
    
    def calculate_loadSoFar_until_nodeIndex_for_route(self, route, node_index_in_route):
        load = 0
        for i in range(0, node_index_in_route):
            node1 = route.nodes_sequence[i]
            node2 = route.nodes_sequence[i+1]
            load += node2.demand
        return load
    
    def calculate_cumulativeCost_from_nodeIndex_until_end_of_route(self, route, node_index_in_route):
        tCost = 0
        cCost = 0
        for i in range(node_index_in_route, len(route.nodes_sequence)-1):
            node1 = route.nodes_sequence[i]
            node2 = route.nodes_sequence[i+1]
            dist_cost = self.cost_matrix[node1.id][node2.id] + node2.uploading_time
            tCost += dist_cost
            cCost += tCost
        return cCost
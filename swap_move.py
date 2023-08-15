class Swap_move:
    def __init__(self, solution, matrix, capacity):
        self.sol = solution
        self.cost_matrix = matrix
        self.capacity = capacity
        
        self.route1_pos = None
        self.route2_pos = None
        self.selected_node1_pos = None
        self.selected_node2_pos = None
        self.cost_change_route1 = None
        self.cost_change_route2 = None
        self.move_cost_difference = 10**9    
    
    def reset(self):
        self.route1_pos = None
        self.route2_pos = None
        self.selected_node1_pos = None
        self.selected_node2_pos = None
        self.cost_change_route1 = None
        self.cost_change_route2 = None
        self.move_cost_difference = 10**9

    def find_best_swap_move(self):
        for rt1_index in range(len(self.sol.routes)):
            route1 = self.sol.routes[rt1_index]

            for rt2_index in range(rt1_index, len(self.sol.routes)):
                route2 = self.sol.routes[rt2_index]

                for node1_index_in_route in range(1, len(route1.nodes_sequence)):
                    start_node2_index = 1
                    if route1 == route2:
                        start_node2_index = node1_index_in_route + 1

                    for node2_index_in_route in range(start_node2_index, len(route2.nodes_sequence)):

                        #Nodes and multiplier for route1
                        is_last1 = (len(route1.nodes_sequence)-node1_index_in_route-1) == 0
                        p1 = route1.nodes_sequence[node1_index_in_route - 1] #previous
                        s1 = route1.nodes_sequence[node1_index_in_route] #selected
                        if is_last1 is False:
                            n1 = route1.nodes_sequence[node1_index_in_route + 1] #next
                        cost_multiplier1 = len(route1.nodes_sequence)-node1_index_in_route #fores pou prostithetai to cost[ dist(previous->selected)+selected.uploading_time ] sto cumulative_cost gia to sugkekrimeno route. Ean o selected OXI TELEUTAIOS: +cost[ dist(selcted->next)]*(multiplier-1)

                        #Nodes and multiplier for route2
                        is_last2 = (len(route2.nodes_sequence)-node2_index_in_route-1) == 0
                        p2 = route2.nodes_sequence[node2_index_in_route - 1]
                        s2 = route2.nodes_sequence[node2_index_in_route]
                        if is_last2 is False:
                            n2 = route2.nodes_sequence[node2_index_in_route + 1]
                        cost_multiplier2 = len(route2.nodes_sequence)-node2_index_in_route

                        total_move_cost_differce = None
                        origin_route_cost_difference = None
                        target_route_cost_difference = None

                        if (route1 == route2) and (node1_index_in_route == node2_index_in_route - 1):
                            cost_removed_rt2, cost_added_rt2 = 0, 0

                            cost_removed_rt1 = cost_multiplier1 * (self.cost_matrix[p1.id][s1.id] + s1.uploading_time)
                            cost_removed_rt1 += cost_multiplier2 * (self.cost_matrix[s1.id][s2.id] + s2.uploading_time)
                            if is_last2 is False:
                                cost_removed_rt1 += (cost_multiplier2-1) * self.cost_matrix[s2.id][n2.id]
                            cost_added_rt1 = cost_multiplier1 * (self.cost_matrix[p1.id][s2.id] + s2.uploading_time)
                            cost_added_rt1 += cost_multiplier2 * (self.cost_matrix[s2.id][s1.id] + s1.uploading_time)
                            if is_last2 is False:
                                cost_added_rt1 += (cost_multiplier2-1) * self.cost_matrix[s1.id][n2.id]
                                                     
                        else:
                            if route1 != route2:
                                if route1.load - s1.demand + s2.demand > self.capacity:
                                    continue
                                if route2.load - s2.demand + s1.demand > self.capacity:
                                    continue

                            cost_removed_rt1 = cost_multiplier1 * (self.cost_matrix[p1.id][s1.id] + s1.uploading_time)
                            if is_last1 is False:
                                cost_removed_rt1 += (cost_multiplier1-1) * self.cost_matrix[s1.id][n1.id]
                            cost_added_rt1 = cost_multiplier1 * (self.cost_matrix[p1.id][s2.id] + s2.uploading_time)
                            if is_last1 is False:
                                cost_added_rt1 += (cost_multiplier1-1) * self.cost_matrix[s2.id][n1.id]              
                            
                            cost_removed_rt2 = cost_multiplier2 * (self.cost_matrix[p2.id][s2.id] + s2.uploading_time)
                            if is_last2 is False:
                                cost_removed_rt2 += (cost_multiplier2-1) * self.cost_matrix[s2.id][n2.id]
                            cost_added_rt2 = cost_multiplier2 * (self.cost_matrix[p2.id][s1.id] + s1.uploading_time)
                            if is_last2 is False:
                                cost_added_rt2 += (cost_multiplier2-1)*self.cost_matrix[s1.id][n2.id]
                            
                        origin_route_cost_difference = cost_added_rt1 - cost_removed_rt1
                        target_route_cost_difference = cost_added_rt2 - cost_removed_rt2
                        total_move_cost_differce = origin_route_cost_difference + target_route_cost_difference

                        if total_move_cost_differce < self.move_cost_difference:
                            self.route1_pos = rt1_index
                            self.route2_pos = rt2_index
                            self.selected_node1_pos = node1_index_in_route
                            self.selected_node2_pos = node2_index_in_route
                            self.cost_change_route1 = origin_route_cost_difference
                            self.cost_change_route2 = target_route_cost_difference
                            self.move_cost_difference = total_move_cost_differce
    
    def apply_swap_move(self):
        route1 = self.sol.routes[self.route1_pos]
        route2 = self.sol.routes[self.route2_pos]
        selected_node1 = route1.nodes_sequence[self.selected_node1_pos]
        selected_node2 = route2.nodes_sequence[self.selected_node2_pos]
        route1.nodes_sequence[self.selected_node1_pos] = selected_node2
        route2.nodes_sequence[self.selected_node2_pos] = selected_node1

        if route1 == route2:
            route1.cumulative_cost += self.cost_change_route1
        else:
            route1.cumulative_cost += self.cost_change_route1
            route2.cumulative_cost += self.cost_change_route2
            route1.load = route1.load - selected_node1.demand + selected_node2.demand
            route2.load = route2.load - selected_node2.demand + selected_node1.demand

        self.sol.cost += self.move_cost_difference
from vrp_model import *
    
class CustomerInsertion(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.cost = 10 ** 9
    
class Constructor:
    def __init__(self,model):
        self.allNodes = model.allNodes
        self.warehouse = model.allNodes[0]
        self.cost_matrix = model.matrix
        self.capacity = model.capacity
        self.max_routes = model.maxRoutes
        self.initial_solution = Solution()

    def construct_solution(self):
        self.create_all_routes()
        self.find_best_customer_with_nearest_neighbor_method()
        self.initial_solution.report_solution("INITIAL SOLUTION")
        return self.initial_solution
    
    def create_all_routes(self):
        for i in range(self.max_routes):
            new_route = Route(self.warehouse, self.capacity)
            self.initial_solution.routes.append(new_route)
    
    def find_best_customer_with_nearest_neighbor_method(self):
        for i in range(1,len(self.allNodes)):
            customer_to_insert = self.allNodes[i]
            bestInsertionObject = CustomerInsertion()

            for j in range(len(self.initial_solution.routes)):
                route_to_insert = self.initial_solution.routes[j]

                if route_to_insert.load + customer_to_insert.demand > self.capacity:
                    continue

                #calculate distance cost if added to this route
                previous_cust = route_to_insert.nodes_sequence[-1]
                canditate_cost = self.cost_matrix[previous_cust.id][customer_to_insert.id]

                if canditate_cost < bestInsertionObject.cost:
                    bestInsertionObject.customer = customer_to_insert
                    bestInsertionObject.route = route_to_insert
                    bestInsertionObject.cost = canditate_cost

            if bestInsertionObject.route is None:
                print("model is impossible")
                exit()

            self.apply_best_customer_insertion(bestInsertionObject)
        
    def apply_best_customer_insertion(self,bestInsertionObject):
        customer_to_insert = bestInsertionObject.customer
        route_to_insert = bestInsertionObject.route
        route_to_insert.nodes_sequence.append(customer_to_insert)
        node_before_inserted = route_to_insert.nodes_sequence[-2]

        distance_time_cost_added = self.cost_matrix[node_before_inserted.id][customer_to_insert.id] + customer_to_insert.uploading_time

        route_to_insert.initial_time_cost += distance_time_cost_added
        route_to_insert.cumulative_cost += route_to_insert.initial_time_cost
        route_to_insert.load += customer_to_insert.demand
        customer_to_insert.isRouted = True
        self.initial_solution.cost += route_to_insert.initial_time_cost

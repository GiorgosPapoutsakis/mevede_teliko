from swap_move import *
from relocation_move import *
from twoOpt_move import *
from SolutionDrawer import *
#30608.973585927415

class Improver:
    def __init__(self, initial_solution, model):
        self.sol = initial_solution
        self.allNodes = model.allNodes     
        self.cost_matrix = model.matrix
        self.capacity = model.capacity

    def improve(self):
        self.local_search(0)
        #self.NVD()
        print("IMPROVED")
        self.sol.report_solution()

    def local_search(self, operator):
        termination_condition = False
        local_search_iterations = 0
        
        sm_obj = Swap_move(self.sol, self.cost_matrix, self.capacity)
        rm_obj = Relocation_move(self.sol, self.cost_matrix, self.capacity)
        tOpt_obj = TwoOpt_move(self.sol, self.cost_matrix, self.capacity)

        while termination_condition is False:
            rm_obj.reset()
            sm_obj.reset()
            tOpt_obj.reset()
            #SolDrawer.draw(local_search_iterations, self.sol, self.allNodes)
            
            #Relocations
            if operator == 0:
                rm_obj.find_best_relocation_move()
                if rm_obj.origin_rt_pos is not None:
                    if rm_obj.move_cost_difference <0:
                        rm_obj.apply_relocation_move()
                    else:
                        termination_condition = True
            #Swaps
            elif operator == 1:
                sm_obj.find_best_swap_move()
                if sm_obj.route1_pos is not None:
                    if sm_obj.move_cost_difference < 0:
                        sm_obj.apply_swap_move()
                    else:
                        termination_condition = True
            #Two_Opt
            elif operator == 2:
                tOpt_obj.find_best_two_opt()
                if tOpt_obj.origin_rt_pos is not None:
                    if tOpt_obj.move_cost_difference < 0:
                        tOpt_obj.apply_two_opt_move()
                    else:
                        termination_condition = True

            local_search_iterations += 1
            print("iterations:",local_search_iterations, self.sol.cost) #extra mia epanalipsi gia na vgei

            #TESTING
            # if self.TestSolution() > 0:
            #     print("PROBLEM")
            #     termination_condition = True
            # else:
            #     print("Test passed")


    def NVD(self):
        nvd_iterations = 0
        operator = 0
        max_operator = 2
        draw = False
        report_each_iteration = False
        
        sm_obj = Swap_move(self.sol, self.cost_matrix, self.capacity)
        rm_obj = Relocation_move(self.sol, self.cost_matrix, self.capacity)
        tOpt_obj = TwoOpt_move(self.sol, self.cost_matrix, self.capacity)

        while operator <= max_operator:
            rm_obj.reset()
            sm_obj.reset()
            tOpt_obj.reset()
            
            #Relocations
            if operator == 0:
                rm_obj.find_best_relocation_move()
                if rm_obj.origin_rt_pos is not None and rm_obj.move_cost_difference <0:
                    rm_obj.apply_relocation_move()

                    if report_each_iteration:
                        print("iteration:",nvd_iterations, self.sol.cost, "operator:",operator)
                    if draw:
                        SolDrawer.draw(nvd_iterations, self.sol, self.allNodes)                        

                    nvd_iterations += 1
                    operator = 0
                else:
                    operator += 1
            #Swaps
            elif operator == 1:
                sm_obj.find_best_swap_move()
                if sm_obj.origin_rt_pos is not None and sm_obj.move_cost_difference < 0:
                    sm_obj.apply_swap_move()

                    if report_each_iteration:
                        print("iteration:",nvd_iterations, self.sol.cost, "operator:",operator)
                    if draw:
                        SolDrawer.draw(nvd_iterations, self.sol, self.allNodes) 

                    nvd_iterations += 1
                    operator = 0
                else:
                    operator += 1
            #Two_Opt
            elif operator == 2:
                tOpt_obj.find_best_two_opt()
                if tOpt_obj.origin_rt_pos is not None and tOpt_obj.move_cost_difference < 0:
                    tOpt_obj.apply_two_opt_move()

                    if report_each_iteration:
                        print("iteration:",nvd_iterations, self.sol.cost, "operator:",operator)
                    if draw:
                        SolDrawer.draw(nvd_iterations, self.sol, self.allNodes)  
                    
                    nvd_iterations += 1
                    operator = 0
                else:
                    operator += 1

            #Testing
            # if self.TestSolution() > 0:
            #     print("PROBLEM")
            #     operator = 3
            # else:
            #     print("Test passed")

       
################
    def TestSolution(self):
        failed_test = 0
        testing_solution = self.sol
        totalSolCost = 0
        for r in range (len(testing_solution.routes)):
            route = testing_solution.routes[r]
            calc_rt_TimeCost = 0
            calc_rtCost = 0
            calc_rtLoad = 0
            for n in range (len(route.nodes_sequence)-1):
                A = route.nodes_sequence[n]
                B = route.nodes_sequence[n+1]
                calc_rt_TimeCost += self.cost_matrix[A.id][B.id] + B.uploading_time
                calc_rtCost += calc_rt_TimeCost
                calc_rtLoad += B.demand

            if abs(calc_rtCost - route.cumulative_cost) > 0.0001:
                print(r+1, calc_rtCost, route.cumulative_cost)
                print ('Route Cost problem')
                failed_test += 1
            if calc_rtLoad != route.load:
                #print(r, calc_rtLoad, route.load)
                print ('Route Load problem')
                failed_test += 1
            
            totalSolCost += route.cumulative_cost
        if abs(totalSolCost - self.sol.cost) > 0.0001:
            print('Solution Cost problem')
        return failed_test
#################   
    
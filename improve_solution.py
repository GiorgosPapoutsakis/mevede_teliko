from swap_move import *
from relocation_move import *
from twoOpt_move import *

class Improver:
    def __init__(self, initial_solution, model):
        self.sol = initial_solution
        self.allNodes = model.allNodes     
        self.cost_matrix = model.matrix
        self.capacity = model.capacity

    def improve_solution(self):
        self.nvd()
        self.sol.report_solution("FINAL SOLUTION")
    
    def nvd(self):
        operator = 0
        max_operator = 2
        nvd_iterations = 0
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
                    nvd_iterations += 1
                    operator = 0
                else:
                    operator += 1
            #Swaps
            elif operator == 1:
                sm_obj.find_best_swap_move()
                if sm_obj.route1_pos is not None and sm_obj.move_cost_difference < 0:
                    sm_obj.apply_swap_move()
                    if report_each_iteration:
                        print("iteration:",nvd_iterations, self.sol.cost, "operator:",operator)
                    nvd_iterations += 1
                    operator = 0
                else:
                    operator += 1
            #Two_Opt
            elif operator == 2:
                tOpt_obj.find_best_two_opt()
                if tOpt_obj.route1_pos is not None and tOpt_obj.move_cost_difference < 0:
                    tOpt_obj.apply_two_opt_move()
                    if report_each_iteration:
                        print("iteration:",nvd_iterations, self.sol.cost, "operator:",operator)               
                    nvd_iterations += 1
                    operator = 0
                else:
                    operator += 1

        #print("NVD-iterations:", nvd_iterations - 1, ",Final cost:", self.sol.cost)

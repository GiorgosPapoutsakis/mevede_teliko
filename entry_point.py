from vrp_model import *
from initial_solution import *
from improve_solution import *

vrpModel = Model()
vrpModel.build_model()
s = Solver(vrpModel)
initial_solution = s.solve()
imp = Improver(initial_solution, vrpModel)
imp.improve()
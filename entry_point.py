from vrp_model import *
from construct_solution import *
from improve_solution import *

vrpModel = Model()
vrpModel.build_model()
constr = Constructor(vrpModel)
initial_solution = constr.construct_solution()
impr = Improver(initial_solution, vrpModel)
impr.improve_solution()
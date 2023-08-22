import random
import math

class Model:
    def __init__(self):
        self.allNodes = []
        self.matrix = []
        self.capacity = 1700
        self.maxRoutes = 14

    def build_model(self):
        warehouse = Node(0, 250, 250, 0, 0)
        self.allNodes.append(warehouse)
        birthday = 39
        random.seed(birthday)
        for i in range(100):
            idd = i+1
            x = random.randint(0, 500)
            y = random.randint(0, 500)
            demand = random.randint(100, 300)
            unloading_time = 10
            customer = Node(idd, x, y, demand, unloading_time)
            self.allNodes.append(customer)

        rows = len(self.allNodes)
        self.matrix = [ [0.0 for x in range(rows)] for y in range(rows)]

        for i in range(0, len(self.allNodes)):
            for j in range(0, len(self.allNodes)):
                a = self.allNodes[i]
                b = self.allNodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                self.matrix[i][j] = dist

        # NODES INFO for Instance.txt(sol_checker)
        # for node in self.allNodes:
        #     print(f"{node.id},{node.x},{node.y},{node.demand},{node.uploading_time}")

class Node:
    def __init__(self,idd,xx,yy,dem,time):
        self.id = idd
        self.x = xx
        self.y = yy
        self.demand = dem
        self.uploading_time = time

class Route:
    def __init__(self,warehouse,capacity):
        self.nodes_sequence = []
        self.nodes_sequence.append(warehouse)
        self.initial_time_cost = 0.0
        self.cumulative_cost = 0.0
        self.capacity = capacity
        self.load = 0

class Solution():
    def __init__(self):
        self.cost = 0.0
        self.routes = []

    def report_solution(self, message=""):
            print(message)
            print("Cost:")
            print(self.cost)
            print("Routes:")
            print(len(self.routes))
            for i in range(len(self.routes)):
                rt = self.routes[i]
                for j in range(len(rt.nodes_sequence)):
                    if j != len(rt.nodes_sequence)-1:
                        print(rt.nodes_sequence[j].id, end=',')
                    else:
                        print(rt.nodes_sequence[j].id, end='')
                        #print(" ",rt.cumulative_cost, end="")
                        print()
            print()

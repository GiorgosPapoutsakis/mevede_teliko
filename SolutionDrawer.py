import matplotlib.pyplot as plt

class SolDrawer:
    @staticmethod
    def get_cmap(n, name='hsv'):
        return plt.cm.get_cmap(name, n)

    @staticmethod
    def draw(name, sol, nodes):
        plt.clf()
        SolDrawer.drawPoints(nodes)
        SolDrawer.drawRoutes(sol)
        plt.savefig(str(name))

    @staticmethod
    def drawPoints(nodes:list):
        x = []
        y = []
        for i in range(len(nodes)):
            n = nodes[i]
            x.append(n.x)
            y.append(n.y)
        plt.scatter(x, y, c="blue")

    @staticmethod
    def drawRoutes(sol):
        cmap = SolDrawer.get_cmap(len(sol.routes))
        if sol is not None:
            for r in range(0, len(sol.routes)):
                rt = sol.routes[r]
                for i in range(0, len(rt.nodes_sequence) - 1):
                    c0 = rt.nodes_sequence[i]
                    c1 = rt.nodes_sequence[i + 1]
                    plt.plot([c0.x, c1.x], [c0.y, c1.y], c=cmap(r))

"""
Поясню, моя игра подразумевает перемещение по карте,
поэтому помимо информации о каждом тайле, которую можно будет найти здесь, можно будет найти класс карта,
который будет хранить информацию о том где, каждый тайл находиться и граф для перемещений, а также позиции сущностей и
препятствий
"""
# кажется, лучше всего передерживаться вот такой логики работы с координатами: координаты в тайлах -> |интерпретация
# под pygame| работа с координатами |интерпретация под pygame| -> координаты в тайлах
from project.settings import ConfigurationProject

config = ConfigurationProject()


class Map:
    def __init__(self):
        self.graph = []  # по заветам дискретной математики граф - (V, E), V - вершины, E - рёбра

        # self.graph.append(self.get_vertexes(
        #     config.WINDOW_SIZE[0] // config.TILE_SIZE,
        #     config.WINDOW_SIZE[1] // config.TILE_SIZE
        # ))  # не факт, что это нужно
        self.graph.append(self.get_vertexes())  # не факт, что это нужно
        self.graph.append(self.get_edges())

    @staticmethod
    def get_vertexes():
        vertexes = []
        for x in range(config.WINDOW_SIZE[0] // config.TILE_SIZE):
            for y in range(config.WINDOW_SIZE[1] // config.TILE_SIZE):
                vertexes.append(
                    [x, y]
                )
        return vertexes

    # @lru_cache()
    # def get_vertexes(self, x, y):
    #     if x == 0:
    #         return [[0, y]]
    #     if y == 0:
    #         return [[x, 0]]
    #     return [[x, y]] + self.get_vertexes(x - 1, y) + self.get_vertexes(x, y - 1)

    @staticmethod
    def get_edges():
        edges = {}

        rows = config.WINDOW_SIZE[0] // config.TILE_SIZE
        cols = config.WINDOW_SIZE[1] // config.TILE_SIZE

        for r in range(rows):
            for c in range(cols):
                edges[(r, c)] = []

        for r in range(rows):
            for c in range(cols):
                u = (r, c)

                if c + 1 < cols:
                    v = (r, c + 1)
                    edges[u].append(v)
                    edges[v].append(u)

                if r + 1 < rows:
                    v = (r + 1, c)
                    edges[u].append(v)
                    edges[v].append(u)

        return edges

    def bellman_ford(self, vertices, source):
        distance = [float('inf')] * vertices
        distance[source] = 0

        for _ in range(vertices - 1):
            for u, v, weight in graph:
                if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight

        for u, v, weight in graph:
            if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                raise ValueError("Graph contains negative weight cycle")

        return distance


if __name__ == '__main__':
    map = Map()
    # print(list(map.graph))




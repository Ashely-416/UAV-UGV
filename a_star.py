import numpy as np
import heapq


class AStar:
    def __init__(self, obstacle_map):
        self.obstacle_map = obstacle_map
        self.len = obstacle_map.shape[0]
        self.width = obstacle_map.shape[1]

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start, goal):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: self.heuristic(start, goal)}
        open_heap = []

        heapq.heappush(open_heap, (fscore[start], start))

        while open_heap:
            current = heapq.heappop(open_heap)[1]

            if current == goal:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data[::-1]

            close_set.add(current)
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                tentative_g_score = gscore[current] + self.heuristic(current, neighbor)

                if 0 <= neighbor[0] < self.len:
                    if 0 <= neighbor[1] < self.width:
                        if self.obstacle_map[neighbor[0], neighbor[1], 0] == 1:
                            continue
                    else:
                        continue
                else:
                    continue

                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in open_heap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_heap, (fscore[neighbor], neighbor))

        return False


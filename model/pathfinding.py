import heapq
import random

def a_star_search(grid, start, goal):
    def heuristic(a, b):
        # Slight randomness + Euclidean to make it more natural
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return (dx ** 2 + dy ** 2) ** 0.5 + random.uniform(0, 0.3)

    def get_neighbors(pos):
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # cardinal directions
            (-1, -1), (-1, 1), (1, -1), (1, 1) # diagonals
        ]
        neighbors = []
        for dr, dc in directions:
            nr, nc = pos[0] + dr, pos[1] + dc
            if (
                0 <= nr < len(grid) and
                0 <= nc < len(grid[0]) and
                grid[nr][nc] in ("floor", "door")
            ):
                neighbors.append((nr, nc))
        random.shuffle(neighbors)  # add randomness in tie-breaking
        return neighbors

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        visited.add(current)
        for neighbor in get_neighbors(current):
            if neighbor in visited:
                continue

            tentative_g = g_score[current] + 1  # All steps cost 1 for now
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

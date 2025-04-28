from collections import deque
import heapq
from constants import DIRECTIONS

def heuristic(pos, goal):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

class SearchAlgorithms:
    def __init__(self, maze):
        self.maze = maze
        self.maze_height = len(maze)
        self.maze_width = len(maze[0]) if self.maze_height > 0 else 0
        self.visited_nodes = set()
        self.frontier_nodes = set()
        self.nodes_expanded = 0
    
    def reset_stats(self):
        self.visited_nodes = set()
        self.frontier_nodes = set()
        self.nodes_expanded = 0
    
    def is_valid_move(self, pos):
        x, y = pos
        if 0 <= x < self.maze_width and 0 <= y < self.maze_height:
            return self.maze[y][x] == 0
        return False

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        for dx, dy in DIRECTIONS:
            new_x, new_y = x + dx, y + dy
            if self.is_valid_move((new_x, new_y)):
                neighbors.append((new_x, new_y))
        return neighbors

    def bfs_search(self, start, foods):
        self.reset_stats()

        # if no food
        if not foods:
            return [], 0, True, False
        
        # Find closest food using heuristic
        goal = min(foods, key=lambda food: heuristic(start, food))
        
        # BFS implementation
        frontier = deque([(start, [])])  # (position, path)
        explored = set()
        self.frontier_nodes = {start}
        
        while frontier:
            node, path = frontier.popleft()
            self.frontier_nodes.discard(node)
            
            if node in explored:
                continue
                
            explored.add(node)
            self.visited_nodes.add(node)
            self.nodes_expanded += 1
            
            if node == goal:
                return path + [node], len(path), True, True
                
            for neighbor in self.get_neighbors(node):
                if neighbor not in explored:
                    frontier.append((neighbor, path + [node]))
                    self.frontier_nodes.add(neighbor)
                    
        return [], 0, True, False  # No path found

    def dfs_search(self, start, foods):
        """Depth-First Search algorithm"""
        self.reset_stats()
        
        # If no food, return empty path
        if not foods:
            return [], 0, True, False
            
        # Find closest food as goal
        goal = min(foods, key=lambda food: heuristic(start, food))
        
        # DFS implementation
        frontier = [(start, [])]  # Stack: (position, path)
        explored = set()
        self.frontier_nodes = {start}
        
        while frontier:
            node, path = frontier.pop()  # DFS uses stack (LIFO)
            self.frontier_nodes.discard(node)
            
            if node in explored:
                continue
                
            explored.add(node)
            self.visited_nodes.add(node)
            self.nodes_expanded += 1
            
            if node == goal:
                return path + [node], len(path), True, True
                
            # Add neighbors in reverse order for DFS
            neighbors = self.get_neighbors(node)
            for neighbor in reversed(neighbors):
                if neighbor not in explored:
                    frontier.append((neighbor, path + [node]))
                    self.frontier_nodes.add(neighbor)
                    
        return [], 0, True, False  # No path found

    def greedy_search(self, start, foods):
        """Greedy Best-First Search algorithm"""
        self.reset_stats()
        
        # If no food, return empty path
        if not foods:
            return [], 0, True, False
            
        # Find closest food as goal
        goal = min(foods, key=lambda food: heuristic(start, food))
        
        # Greedy Search implementation
        frontier = [(heuristic(start, goal), start, [])]  # (heuristic, position, path)
        heapq.heapify(frontier)
        explored = set()
        self.frontier_nodes = {start}
        
        while frontier:
            _, node, path = heapq.heappop(frontier)
            self.frontier_nodes.discard(node)
            
            if node in explored:
                continue
                
            explored.add(node)
            self.visited_nodes.add(node)
            self.nodes_expanded += 1
            
            if node == goal:
                return path + [node], len(path), True, True
                
            for neighbor in self.get_neighbors(node):
                if neighbor not in explored:
                    # Use heuristic for priority
                    priority = heuristic(neighbor, goal)
                    heapq.heappush(frontier, (priority, neighbor, path + [node]))
                    self.frontier_nodes.add(neighbor)
                    
        return [], 0, True, False  # No path found
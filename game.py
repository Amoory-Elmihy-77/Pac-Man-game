import random
from constants import *
from search_algo import SearchAlgorithms, heuristic

class PacmanGame:
    def __init__(self):
        # Set up the screen
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pacman AI Search")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        # Game state
        self.running = True
        self.algorithm = "BFS"  # Default algorithm
        self.step_mode = False
        self.visualize_search = True
        self.reset_game()

    def reset_game(self):
        # Generate maze
        self.maze_width = 20
        self.maze_height = 15
        self.maze = self.generate_maze(self.maze_width, self.maze_height)

        # Initialize search algorithms
        self.search = SearchAlgorithms(self.maze)

        # Place pacman and food
        self.pacman_pos = (1, 1)
        self.foods = []
        self.place_food(20)  # Place 20 food pellets

        # Ghosts
        self.ghosts = [(self.maze_width - 2, self.maze_height - 2)]

        # Path and search info
        self.current_path = []
        self.visited_nodes = set()
        self.frontier_nodes = set()
        self.step_index = 0
        self.search_completed = False
        self.path_found = False

        # Stats
        self.nodes_expanded = 0
        self.path_length = 0

    def generate_maze(self, width, height):
        # Create a grid filled with walls
        maze = [[1 for _ in range(width)] for _ in range(height)]

        # Set the borders
        for i in range(width):
            maze[0][i] = 1
            maze[height - 1][i] = 1
        for i in range(height):
            maze[i][0] = 1
            maze[i][width - 1] = 1

        # Create a simple maze pattern
        for i in range(1, height - 1):
            for j in range(1, width - 1):
                if (i % 2 == 0 and j % 2 == 0) and random.random() < 0.7:
                    maze[i][j] = 1  # Wall
                else:
                    maze[i][j] = 0  # Path

        # Ensure start position is empty
        maze[1][1] = 0
        maze[2][1] = 0
        maze[1][2] = 0

        return maze

    def place_food(self, count):
        """Place food pellets in the maze"""
        self.foods = []
        empty_cells = [(x, y) for y in range(self.maze_height)
                       for x in range(self.maze_width)
                       if self.maze[y][x] == 0 and (x, y) != self.pacman_pos]

        # Pick random empty cells for food
        if empty_cells:
            for _ in range(min(count, len(empty_cells))):
                food = random.choice(empty_cells)
                self.foods.append(food)
                empty_cells.remove(food)

    def draw(self):
        """Draw the game state"""
        self.screen.fill(BLACK)

        # Draw maze
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.maze[y][x] == 1:  # Wall
                    pygame.draw.rect(self.screen, BLUE, rect)
                else:  # Path
                    pygame.draw.rect(self.screen, BLACK, rect)

        # Draw search visualization if enabled
        if self.visualize_search:
            # Draw visited nodes
            for x, y in self.visited_nodes:
                if (x, y) != self.pacman_pos and (x, y) not in self.foods:
                    pygame.draw.rect(self.screen, (50, 50, 50),
                                     pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # Draw frontier nodes
            for x, y in self.frontier_nodes:
                if (x, y) != self.pacman_pos and (x, y) not in self.foods:
                    pygame.draw.rect(self.screen, PURPLE,
                                     pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw path
        if self.path_found:
            for i, (x, y) in enumerate(self.current_path):
                if i >= self.step_index:  # Only draw future path
                    pygame.draw.rect(self.screen, GREEN,
                                     pygame.Rect(x * CELL_SIZE + CELL_SIZE // 4,
                                                 y * CELL_SIZE + CELL_SIZE // 4,
                                                 CELL_SIZE // 2, CELL_SIZE // 2))

        # Draw food
        for food_x, food_y in self.foods:
            pygame.draw.circle(self.screen, YELLOW,
                               (food_x * CELL_SIZE + CELL_SIZE // 2,
                                food_y * CELL_SIZE + CELL_SIZE // 2),
                               CELL_SIZE // 4)

        # Draw Pacman
        pacman_x, pacman_y = self.pacman_pos
        pygame.draw.circle(self.screen, YELLOW,
                           (pacman_x * CELL_SIZE + CELL_SIZE // 2,
                            pacman_y * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 2 - 2)

        # Draw ghosts
        for ghost_x, ghost_y in self.ghosts:
            pygame.draw.circle(self.screen, RED,
                               (ghost_x * CELL_SIZE + CELL_SIZE // 2,
                                ghost_y * CELL_SIZE + CELL_SIZE // 2),
                               CELL_SIZE // 2 - 2)

        # Draw UI text
        algorithm_text = self.font.render(f"Algorithm: {self.algorithm}", True, WHITE)
        nodes_text = self.font.render(f"Nodes Expanded: {self.nodes_expanded}", True, WHITE)
        path_text = self.font.render(f"Path Length: {self.path_length}", True, WHITE)

        self.screen.blit(algorithm_text, (620, 30))
        self.screen.blit(nodes_text, (620, 60))
        self.screen.blit(path_text, (620, 90))

        # Draw instructions
        instructions = [
            "Controls:",
            "R - Reset",
            "B - BFS",
            "D - DFS",
            "G - Greedy",
            "V - Toggle Visualization",
            "Space - Step Mode"
        ]

        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, WHITE)
            self.screen.blit(text, (620, 150 + i * 30))

        pygame.display.flip()

    def run_search(self):
        self.search_completed = False
        self.path_found = False

        if self.algorithm == "BFS":
            path, path_cost, completed, found = self.search.bfs_search(self.pacman_pos, self.foods)
        elif self.algorithm == "DFS":
            path, path_cost, completed, found = self.search.dfs_search(self.pacman_pos, self.foods)
        elif self.algorithm == "Greedy":
            path, path_cost, completed, found = self.search.greedy_search(self.pacman_pos, self.foods)

        # Update game state with search results
        self.current_path = path
        self.path_length = path_cost
        self.search_completed = completed
        self.path_found = found
        self.visited_nodes = self.search.visited_nodes
        self.frontier_nodes = self.search.frontier_nodes
        self.nodes_expanded = self.search.nodes_expanded

    def update(self):
        # If we have a path and not in step mode, move along the path
        if self.path_found and not self.step_mode:
            if self.step_index < len(self.current_path):
                self.pacman_pos = self.current_path[self.step_index]
                self.step_index += 1

                # Check if pacman ate food
                if self.pacman_pos in self.foods:
                    self.foods.remove(self.pacman_pos)

                    # If all food eaten, game over
                    if not self.foods:
                        print("All food eaten! You win!")
                    else:
                        # Run search again for next food
                        self.current_path = []
                        self.step_index = 0
                        self.search_completed = False
                        self.path_found = False
                        self.run_search()

            # If we're at the end of the path, rerun search
            elif self.foods:
                self.current_path = []
                self.step_index = 0
                self.search_completed = False
                self.path_found = False
                self.run_search()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset
                    self.reset_game()
                    self.run_search()

                elif event.key == pygame.K_b:  # BFS
                    self.algorithm = "BFS"
                    self.reset_game()
                    self.run_search()

                elif event.key == pygame.K_d:  # DFS
                    self.algorithm = "DFS"
                    self.reset_game()
                    self.run_search()

                elif event.key == pygame.K_g:  # Greedy
                    self.algorithm = "Greedy"
                    self.reset_game()
                    self.run_search()

                elif event.key == pygame.K_v:  # Toggle visualization
                    self.visualize_search = not self.visualize_search

                elif event.key == pygame.K_SPACE:  # Step mode
                    self.step_mode = not self.step_mode
                    if self.step_mode and self.path_found:
                        if self.step_index < len(self.current_path):
                            self.pacman_pos = self.current_path[self.step_index]

                            # Check if pacman ate food
                            if self.pacman_pos in self.foods:
                                self.foods.remove(self.pacman_pos)

                            self.step_index += 1

    def run(self):
        # Initial search
        self.run_search()

        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
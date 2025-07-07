from typing import List, Tuple, Optional, Dict, Set
import random

class Tile:
    def __init__(self, walkable: bool = True, has_clue: bool = False, has_up_stairs: bool = False, has_down_stairs: bool = False) -> None:
        self.walkable = walkable
        self.has_clue = has_clue
        self.has_up_stairs = has_up_stairs
        self.has_down_stairs = has_down_stairs

class Dungeon:
    def __init__(self, width: int = 20, height: int = 15, num_loops: int = 10) -> None:
        self.width = width
        self.height = height
        self.grid: List[List[Tile]] = [
            [Tile(False) for _ in range(width)]
            for _ in range(height)
        ]
        self.clues: Dict[Tuple[int, int], str] = {}
        self.path: List[Tuple[int, int]] = []
        self._generate_maze()
        self._add_loops(num_loops)
        self._generate_clues()
        self._generate_stairs()
    
    def _generate_maze(self) -> None:
        """Generates a maze using randomized DFS. All walkable tiles will be connected."""
        width, height = self.width, self.height
        visited = [[False for _ in range(width)] for _ in range(height)]
        stack = []
        start = (random.randrange(width), random.randrange(height))
        stack.append(start)
        self.grid[start[1]][start[0]].walkable = True
        self.path.append(start)

        while stack:
            x, y = stack[-1]
            visited[y][x] = True
            neighbors = []
            directions = [(-2,0),(2,0),(0,-2),(0,2)] # 2-step neighbors for maze
            for dx, dy in directions:
                nx, ny = x+dx, y+dy
                if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                    neighbors.append((nx, ny, dx, dy))
            if neighbors:
                nx, ny, dx, dy = random.choice(neighbors)
                # Carve passage between (x, y) and (nx, ny)
                mx, my = x + dx//2, y + dy//2
                self.grid[ny][nx].walkable = True
                self.grid[my][mx].walkable = True
                self.path.append((mx, my))
                self.path.append((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

    def _add_loops(self, num_loops: int) -> None:
        """Add extra random connections (loops) to the maze."""
        width, height = self.width, self.height
        tries = 0
        added = 0
        while added < num_loops and tries < num_loops * 10:
            x = random.randrange(1, width-1)
            y = random.randrange(1, height-1)
            if not self.grid[y][x].walkable:
                # Check if two non-adjacent walkable tiles are separated by this wall
                directions = [(-1,0),(1,0),(0,-1),(0,1)]
                walkable_neighbors = []
                for dx, dy in directions:
                    nx, ny = x+dx, y+dy
                    if self.grid[ny][nx].walkable:
                        walkable_neighbors.append((nx, ny))
                if len(walkable_neighbors) >= 2:
                    self.grid[y][x].walkable = True
                    added += 1
            tries += 1

    def _generate_clues(self) -> None:
        # Place 3-5 clues at random walkable tiles (not on player start)
        walkable = [(x, y) for y in range(self.height) for x in range(self.width)
                    if self.grid[y][x].walkable]
        num_clues = random.randint(3, 5)
        clue_locs = set()
        while len(clue_locs) < num_clues:
            x, y = random.choice(walkable)
            if (x, y) not in clue_locs:
                self.grid[y][x].has_clue = True
                self.clues[(x, y)] = f"Clue {len(clue_locs)+1}: Something cryptic."
                clue_locs.add((x, y))

    def _generate_stairs(self) -> None:
        """Place up stairs and down stairs at random walkable tiles."""
        walkable = [(x, y) for y in range(self.height) for x in range(self.width)
                    if self.grid[y][x].walkable and not self.grid[y][x].has_clue]
        
        if len(walkable) >= 2:
            # Place up stairs
            up_pos = random.choice(walkable)
            self.grid[up_pos[1]][up_pos[0]].has_up_stairs = True
            walkable.remove(up_pos)
            
            # Place down stairs
            down_pos = random.choice(walkable)
            self.grid[down_pos[1]][down_pos[0]].has_down_stairs = True

    def get_clue(self, x: int, y: int) -> Optional[str]:
        return self.clues.get((x, y))

    def get_random_walkable(self) -> Tuple[int, int]:
        walkable = [(x, y) for y in range(self.height) for x in range(self.width)
                    if self.grid[y][x].walkable]
        return random.choice(walkable)
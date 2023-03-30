import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # mark the cell as a move that has been made
        self.moves_made.add(cell)

        # mark the cell as safe
        self.mark_safe(cell)

        # add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`
        possible_cells = set()
        x, y = cell[0], cell[1]
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if x+i < 0 or x+i >=self.height or y+j < 0 or y+j >= self.width or (i == j == 0):
                    continue
                possible_cells.add((x + i, y + j))
        possible_cells -= self.safes
        neighbor_known_mines = len(possible_cells & self.mines)
        possible_cells -= self.mines
        possible_cells -= self.moves_made
        self.knowledge.append(Sentence(possible_cells, count-neighbor_known_mines))

        # mark any additional cells as safe or as mines
        # if it can be concluded based on the AI's knowledge base
        def add(self):
            """
            return a positive number if there is anything updated
            """
            cnt = 0
            new_mines = []
            new_safes = []
            for sentence in self.knowledge:
                if sentence.known_mines():
                    cnt += 1
                    new_mines += list(sentence.known_mines())
                    self.knowledge.remove(sentence)
                if sentence.known_safes():
                    cnt += 1
                    new_safes += list(sentence.known_safes())
                    self.knowledge.remove(sentence)
            while True:
                while len(new_safes) != 0:
                    safe = new_safes.pop()
                    self.mark_safe(safe)
                    for sentence in self.knowledge:
                        if sentence.known_mines():
                            cnt += 1
                            new_mines += list(sentence.known_mines())
                        if sentence.known_safes():
                            cnt += 1
                            new_safes += list(sentence.known_safes())
                while len(new_mines) != 0:
                    mine = new_mines.pop()
                    self.mark_mine(mine)
                    for sentence in self.knowledge:
                        if sentence.known_mines():
                            cnt += 1
                            new_mines += list(sentence.known_mines())
                        if sentence.known_safes():
                            cnt += 1
                            new_safes += list(sentence.known_safes())
                if len(new_mines) == 0 and len(new_safes) == 0:
                    return cnt

        # add any new sentences to the AI's knowledge base
        # if they can be inferred from existing knowledge
        def infer(self):
            cnt = 0
            for i in range(len(self.knowledge)):
                for j in range(i + 1, len(self.knowledge)):
                    flag = False
                    sentence1, sentence2 = self.knowledge[i], self.knowledge[j]
                    if sentence1.cells < sentence2.cells:
                        newpart = sentence2.cells - sentence1.cells
                        mine_cnt = sentence2.count - sentence1.count
                    elif sentence1.cells > sentence2.cells:
                        newpart = sentence1.cells - sentence2.cells
                        mine_cnt = sentence1.count - sentence2.count
                    else:
                        continue
                    if not newpart:
                        continue
                    tmp = Sentence(newpart, mine_cnt)
                    for sentence in self.knowledge:
                        if tmp == sentence:
                            flag = True
                            break
                    if flag:
                        continue
                    self.knowledge.append(tmp)
                    cnt += 1
            return cnt
        
        while True:
            add_cnt = add(self)
            infer_cnt = infer(self)
            if not add_cnt and not infer_cnt:
                break

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made
        if len(safe_moves) == 0:
            return None
        return safe_moves.pop()

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = set()
        for i in range(self.width):
            for j in range(self.height):
                possible_moves.add((i, j))
        possible_moves -= self.moves_made
        possible_moves -= self.mines
        if len(possible_moves) == 0:
            return None
        return possible_moves.pop()

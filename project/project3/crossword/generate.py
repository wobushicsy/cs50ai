import sys
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for x in self.crossword.words:
            for v in self.domains.keys():
                if len(x) != v.length:
                    self.domains[v].remove(x)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # get overlap=(i, j) between x and y
        revised = False
        flag = False
        overlap = self.crossword.overlaps[(x, y)]
        if overlap == None:
            return revised
        x_th, y_th = overlap
        unmatch = set()
        for x_word in self.domains[x]:
            for y_word in self.domains[y]:
                if x_word[x_th] == y_word[y_th]:
                    flag = True
            if not flag:
                unmatch.add(x_word)
                revised = True
        self.domains[x] -= unmatch
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = arcs if arcs else [
            var for var in self.crossword.overlaps.keys() 
            if self.crossword.overlaps[var]
        ]
        while len(queue) > 0:
            # dequeue
            x, y = queue[0]
            queue = queue[1:]
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    # enqueue
                    if neighbor != y:
                        queue += [(neighbor, x)]
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.domains)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # check if all values are distinct
        check_list = []
        for key in assignment.keys():
            if assignment[key] not in check_list:
                check_list.append(assignment[key])
            else:
                return False
        
        # check if every value is the correct length
        for key, word in assignment.items():
            if len(word) != key.length:
                return False
            
        # check if there is conflicts between neighboring variables or not
        for var, loc in self.crossword.overlaps.items():
            if not loc:
                continue
            x, y = var
            i, j = loc
            if x in assignment and y in assignment and assignment[x][i] != assignment[y][j]:
                return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        word_cnt_pair = {}
        for x_word in self.domains[var]:
            cnt = 0
            overlaps = self.crossword.overlaps.keys()
            for overlap in overlaps:
                if not self.crossword.overlaps[overlap] or overlap in assignment.keys():
                    continue
                x, y = overlap
                if x != var:
                    continue
                for y_word in self.domains[y]:
                    i, j = self.crossword.overlaps[overlap]
                    if x_word[i] != y_word[j]:
                        cnt += 1
            word_cnt_pair[x_word] = cnt
        sorted_list = sorted(word_cnt_pair.items())
        return [item[0] for item in sorted_list]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_variable = set(self.domains.keys() - set(assignment.keys()))
        unassigned = []
        cnt = float("inf")
        for var in unassigned_variable:
            if len(self.domains[var]) < cnt:
                cnt = len(self.domains[var])
                unassigned = [var]
            elif self.domains[var] == cnt:
                unassigned += [var]
        max_neighbors = -1
        most_neighbors = []
        for var in unassigned:
            if len(self.crossword.neighbors(var)) > max_neighbors:
                most_neighbors = [var]
            elif len(self.crossword.neighbors(var)) == max_neighbors:
                most_neighbors += [var]
        return most_neighbors[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        `assignment` is a mapping from variables (keys) to words (values).
        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        unassigned_var = self.select_unassigned_variable(assignment)
        domain = self.order_domain_values(unassigned_var, assignment)
        for word in domain:
            assignment_copy = assignment.copy()
            assignment_copy[unassigned_var] = word
            if self.consistent(assignment_copy):
                result = self.backtrack(assignment_copy)
                if result != None:
                    return result
        return None


def main():

    """
    test
    sys.argv.append("data\\structure1.txt")
    sys.argv.append("data\\words1.txt")
    sys.argv.append("output1.png")
    """

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()

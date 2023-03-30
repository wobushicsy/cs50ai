from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
Asay0 = And(AKnight, AKnave)
knowledge0 = And(
    # TODO
    Or(AKnave, AKnight), 
    Implication(AKnight, Not(AKnave)),
    Implication(AKnave, Not(AKnight)),
    Implication(AKnight, Asay0), 
    Implication(AKnave, Not(Asay0)), 
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
Asay1 = And(AKnave, BKnave)
knowledge1 = And(
    # TODO
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave),
    Implication(AKnight, Not(AKnave)), 
    Implication(AKnave, Not(AKnight)), 
    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)),
    Implication(AKnight, Asay1), 
    Implication(AKnave, Not(Asay1))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
Asay2 = Or(And(AKnight, BKnight), And(AKnave, BKnave))
Bsay2 = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    # TODO
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave), 
    Implication(AKnight, Not(AKnave)), 
    Implication(AKnave, Not(AKnight)), 
    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)),
    Implication(AKnight, Asay2), 
    Implication(AKnave, Not(Asay2)), 
    Implication(BKnight, Bsay2), 
    Implication(BKnave, Not(Bsay2))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
Asayin31 = Symbol("I am a knight")
Asayin32 = Symbol("I am a knave")
Asay3 = Or(Asayin31, Asayin32)
Bsay31 = Asayin32
Bsay32 = CKnave
Csay3 = AKnight
knowledge3 = And(
    # TODO
    Or(AKnight, AKnave), 
    Or(BKnight, BKnave), 
    Or(CKnight, CKnave),
    Implication(AKnight, Not(AKnave)), 
    Implication(AKnave, Not(AKnight)), 
    Implication(BKnight, Not(BKnave)),
    Implication(BKnave, Not(BKnight)),
    Implication(CKnight, Not(CKnave)), 
    Implication(CKnave, Not(CKnight)),
    Implication(AKnight, Asay3), 
    Implication(AKnave, Not(Asay3)), 
    Implication(BKnight, And(Bsay31, Bsay32)),
    Implication(BKnave, And(Not(Bsay31), Not(Bsay32))), 
    Implication(CKnight, Csay3), 
    Implication(CKnave, Not(Csay3))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

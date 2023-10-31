#Primarily From https://github.com/kosayoda/chickenpy/

from peppy.vm import OPCODE


class ParseError(Exception):
    def __init__(self, message):
        super().__init__(message)


def compile(code: str):
    """Compiles source code into a list of tokens."""
    lines = code.splitlines()
    tokens = []
    for line_no, line in enumerate(lines, start=1):

        # Check for start character
        if line_no==1 and not line.strip() == 'pep':
            print("Program must start with pep")
            break
        
        if line.strip() == 'pep':
            continue 

        # Check for halt character
        if line.strip() == 'erdine':
            tokens.append(OPCODE.EXIT)
            continue

        #Convert p's into chickens
        line = line.replace('p', 'chicken ')

        words = line.split()
        # Raise syntax error if any word other than 'chicken' or whitespace is found
        if word_set := (set(words) - {"chicken", " "}):
            raise ParseError(f"Invalid token(s) on line {line_no}: {' '.join(word_set)}")
            return False

        num_chickens = len(line.split())
        # Any number of chickens > 9 is used as is
        if num_chickens > 9:
            tokens.append(num_chickens)
        else:
            tokens.append(OPCODE(num_chickens))
    return tokens
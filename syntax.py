import os
import sys
import collections

try:
    oldTerm = os.environ['TERM']
    os.environ['TERM'] = ''
    import readline
    os.environ['TERM'] = oldTerm
    del oldTerm

except ImportError:
    pass
if sys.version_info < (3,0):
    input = raw_input

class ParseError(Exception):
    pass

TreeType = list

def parse_expr(w):
    """Convert an s-expression to a tree.

    The tree is a list whose elements are either strings or
    sub-trees. For example,

    parse_expr("(lambda (x) (x x))") => ["lambda", ["x"], ["x", "x"]].

    Raises ParseError if the s-expression is not well-formed.
    """
    w = collections.deque(w)

    def parse_atom():
        cs = []
        while len(w) > 0 and w[0] != ")" and not w[0].isspace():
            cs.append(w.popleft())
        return ''.join(cs)

    def parse_whitespace():
        while len(w) > 0 and w[0].isspace():
            w.popleft()

    def parse_start():
        if w[0] == "(":
            left = w[0]
            w.popleft()
            children = []
            parse_whitespace()
            while len(w) > 0 and w[0] != ")":
                children.append(parse_start())
                parse_whitespace()
            if len(w) == 0:
                raise ParseError("unexpected end of string")
            w.popleft()
            return TreeType(children)
        else:
            return parse_atom()

    parse_whitespace()
    if len(w) == 0:
        raise ParseError("unexpected end of string")
    e = parse_start()
    parse_whitespace()
    if len(w) != 0:
        raise ParseError("extra characters after expression")
    return e

def format_expr(expr):
    """Convert a tree to an s-expression.

    The tree is a list who elements are either strings or
    sub-trees. For example,

    format_expr(["lambda", ["x"], ["x", "x"]]) => "(lambda (x) (x x))".
    """

    if isinstance(expr, TreeType):
        return "({})".format(" ".join(map(format_expr, expr)))
    else:
        return str(expr)

def readlines(file=sys.stdin, prompt=""):
    """Read lines from file. If the file is a tty, that is, keyboard input
    from the user, then display a prompt and allow editing and history."""
    if os.isatty(file.fileno()):
        while True:
            try:
                line = input(prompt)
            except EOFError:
                print()
                break
            yield line
    else:
        for line in file:
            yield line

if __name__ == "__main__":
    # REPL that does nothing
    import sys
    for line in readlines(sys.stdin, "> "):
        try:
            expr = parse_expr(line)
    	    print(format_expr(expr))
        except ParseError as e:
            print("error: {}".format(e))


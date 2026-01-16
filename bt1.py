class Expr:
    pass

class Var(Expr):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

class Not(Expr):
    def __init__(self, x):
        self.x = x
    def __repr__(self):
        return f"~{self.x}"

class And(Expr):
    def __init__(self, a, b):
        self.a, self.b = a, b
    def __repr__(self):
        return f"({self.a} & {self.b})"

class Or(Expr):
    def __init__(self, a, b):
        self.a, self.b = a, b
    def __repr__(self):
        return f"({self.a} | {self.b})"

class Implies(Expr):
    def __init__(self, a, b):
        self.a, self.b = a, b

class Iff(Expr):
    def __init__(self, a, b):
        self.a, self.b = a, b

def eliminate_implications(e):
    if isinstance(e, Var):
        return e
    if isinstance(e, Not):
        return Not(eliminate_implications(e.x))
    if isinstance(e, And):
        return And(eliminate_implications(e.a), eliminate_implications(e.b))
    if isinstance(e, Or):
        return Or(eliminate_implications(e.a), eliminate_implications(e.b))
    if isinstance(e, Implies):
        return Or(Not(eliminate_implications(e.a)), eliminate_implications(e.b))
    if isinstance(e, Iff):
        a = eliminate_implications(e.a)
        b = eliminate_implications(e.b)
        return And(Or(Not(a), b), Or(Not(b), a))


def push_negation(e):
    if isinstance(e, Var):
        return e
    if isinstance(e, Not):
        x = e.x
        if isinstance(x, Var):
            return e
        if isinstance(x, Not):
            return push_negation(x.x)
        if isinstance(x, And):
            return Or(push_negation(Not(x.a)), push_negation(Not(x.b)))
        if isinstance(x, Or):
            return And(push_negation(Not(x.a)), push_negation(Not(x.b)))
    if isinstance(e, And):
        return And(push_negation(e.a), push_negation(e.b))
    if isinstance(e, Or):
        return Or(push_negation(e.a), push_negation(e.b))


def distribute(e):
    if isinstance(e, And):
        return And(distribute(e.a), distribute(e.b))
    if isinstance(e, Or):
        a, b = distribute(e.a), distribute(e.b)
        if isinstance(a, And):
            return And(distribute(Or(a.a, b)), distribute(Or(a.b, b)))
        if isinstance(b, And):
            return And(distribute(Or(a, b.a)), distribute(Or(a, b.b)))
        return Or(a, b)
    return e


def to_cnf(expr):
    expr = eliminate_implications(expr)
    expr = push_negation(expr)
    expr = distribute(expr)
    return expr
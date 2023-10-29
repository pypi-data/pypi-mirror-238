from mathesis.forms import Formula, Negation, Conjunction, Disjunction, Conditional


class SAxiom:
    """Axiom schema of substitution"""

    def __init__(self, x: Formula, y: Formula, z: Formula):
        return Conditional(
            Conditional(x, Conditional(y, z)),
            Conditional(Conditional(x, y), Conditional(x, z)),
        )


class KAxiom:
    """Axiom schema of constant"""

    def __init__(self, x: Formula, y: Formula):
        return Conditional(x, Conditional(y, x))


class IdentityAxiom:
    """Axiom schema of identity"""

    def __init__(self, x: Formula):
        return Conditional(x, x)


class DisjunctionIntroductionAxiom:
    """Axiom schema of disjunction introduction"""

    def __init__(self, disj1: Formula, disj2: Formula, antecendent: Formula):
        """
        Args:
            disj1 (Formula): Left disjunct
            disj2 (Formula): Right disjunct
            antecendent (Formula): Antecendent identical to one of the disjuncts
        """
        if antecendent != disj1 and antecendent != disj2:
            raise ValueError("Antecendent must be one of the disjunctions")
        return Conditional(disj1, Disjunction(disj1, disj2))


class DisjunctionEliminationAxiom:
    """Axiom schema of disjunction elimination"""

    def __init__(self, disj1: Formula, disj2: Formula, consequent: Formula):
        return Conditional(
            Conditional(disj1, consequent),
            Conditional(
                Conditional(disj2, consequent),
                Conditional(Disjunction(disj1, disj2), consequent),
            ),
        )


class ConjunctionIntroductionAxiom:
    """Axiom schema of conjunction introduction"""

    def __init__(self, conj1: Formula, conj2: Formula):
        return Conditional(conj1, Conditional(conj2, Conjunction(conj1, conj2)))


class ConjunctionEliminationAxiom:
    """Axiom schema of conjunction elimination"""

    def __init__(self, conj1: Formula, conj2: Formula, consequent: Formula):
        if consequent != conj1 and consequent != conj2:
            raise ValueError("Antecendent must be one of the disjunctions")
        return Conditional(
            Conjunction(conj1, conj2),
            consequent,
        )


class DNEAxiom:
    """Axiom schema of double negation elimination"""

    def __init__(self, x: Formula):
        return Conditional(Negation(Negation(x)), x)

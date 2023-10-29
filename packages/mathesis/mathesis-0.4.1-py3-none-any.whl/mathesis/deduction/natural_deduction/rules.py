from itertools import count
from typing import Literal
from anytree import Node
from mathesis.deduction.tableau import signed_rules, sign
from mathesis import forms

Rule = signed_rules.Rule


class EFQ(Rule):
    def __init__(self, intro: Node):
        self.intro = intro

    def apply(self, target, tip, counter=count(1)):
        assert target.sign == sign.POSITIVE, "Sign is not positive"
        # TODO: Fix this
        assert str(target.fml) == "⊥", "Not an atom"
        node = Node(
            str(self.intro.fml),
            sign=sign.POSITIVE,
            fml=self.intro.fml,
            parent=tip,
            n=next(counter),
        )
        return {
            "queue_items": [[node]],
            "counter": counter,
        }


class Negation:
    # Intro = signed_rules.NegativeNegationRule
    class Intro(Rule):
        def apply(self, target, tip, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Sign is not negative"
            assert isinstance(target.fml, forms.Negation), "Not a negation"
            subfml = target.fml.sub

            # TODO: Fix this
            falsum = forms.Atom("⊥")

            antec = Node(
                str(subfml), sign=sign.POSITIVE, fml=subfml, parent=tip, n=next(counter)
            )
            conseq = Node(
                str(falsum),
                sign=sign.NEGATIVE,
                fml=falsum,
                parent=antec,
                n=next(counter),
            )

            return {
                "queue_items": [[antec, conseq]],
                "counter": counter,
            }

    class Elim(Rule):
        def __init__(self):
            pass

        def apply(self, target, tip, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Sign is not positive"
            assert isinstance(target.fml, forms.Negation), "Not a negation"
            subfml = target.fml.sub

            # TODO: Better way to check conditions
            premises = list(map(lambda x: str(x.fml), target.sequent_node.sequent.left))
            assert str(subfml) in premises, f"`{str(subfml)}` must be in premises"

            # TODO: Fix this
            falsum = forms.Atom("⊥")
            node = Node(
                str(falsum), sign=sign.POSITIVE, fml=falsum, parent=tip, n=next(counter)
            )
            return {
                "queue_items": [[node]],
                "counter": counter,
            }


class Conjunction:
    Intro = signed_rules.NegativeConjunctionRule
    # TODO: Choice of conjunct
    Elim = signed_rules.PositiveConjunctionRule


class Disjunction:
    # Intro = signed_rules.NegativeDisjunctionRule
    class Intro(Rule):
        def __init__(self, disjunct: Literal["left", "right"]):
            self.disjunct = disjunct

        def apply(self, target, tip, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Sign is not negative"
            assert isinstance(target.fml, forms.Disjunction), "Not a disjunction"
            disj1, disj2 = target.fml.subs
            node1 = Node(
                str(disj1), sign=sign.NEGATIVE, fml=disj1, parent=tip, n=next(counter)
            )
            node2 = Node(
                str(disj2), sign=sign.NEGATIVE, fml=disj2, parent=node1, n=next(counter)
            )

            if self.disjunct == "left":
                node = node1
            elif self.disjunct == "right":
                node = node2

            return {
                "queue_items": [[node]],
                "counter": counter,
            }

    Elim = signed_rules.PositiveDisjunctionRule


class Conditional:
    Intro = signed_rules.NegativeConditionalRule

    class Elim(Rule):
        def __init__(self):
            pass

        def apply(self, target, tip, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Sign is not positive"
            assert isinstance(target.fml, forms.Conditional), "Not a conditional"
            antec, conseq = target.fml.subs

            # TODO: Better way to check conditions
            premises = list(map(lambda x: str(x.fml), target.sequent_node.sequent.left))
            # print(premises)
            assert str(antec) in premises, "Antecendent does not match"

            # conclusion = str(target.sequent_node.sequent.right[0].fml)
            # print(conclusion)
            # assert str(conseq) == conclusion, "Consequent does not match"

            node2 = Node(
                str(conseq), sign=sign.POSITIVE, fml=conseq, parent=tip, n=next(counter)
            )
            return {
                "queue_items": [[node2]],
                "counter": counter,
            }

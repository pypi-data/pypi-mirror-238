from itertools import count

from mathesis.deduction.tableau import signed_rules


class StructuralRule:
    pass


class Negation:
    Left = signed_rules.PositiveNegationRule
    Right = signed_rules.NegativeNegationRule


class Conjunction:
    Left = signed_rules.PositiveConjunctionRule
    Right = signed_rules.NegativeConjunctionRule


class Disjunction:
    Left = signed_rules.PositiveDisjunctionRule
    Right = signed_rules.NegativeDisjunctionRule


class Conditional:
    Left = signed_rules.PositiveConditionalRule
    Right = signed_rules.NegativeConditionalRule


class Weakening:
    class Left(StructuralRule):
        def apply(self, target, tips, counter=count(1)):
            target.weakened = True
            # left = [v for v in target.sequent_node.sequent[0] if v != target]
            # right = target.sequent_node.sequent[1]
            # sequent_node = Node(
            #     "{} ⇒ {}".format(
            #         ", ".join(map(lambda x: f"{x.name}", left)),
            #         ", ".join(map(lambda x: f"{x.name}", right)),
            #     ),
            #     sequent=[left, right],
            #     parent=target.sequent_node,
            # )
            return {
                "queue_items": [[]],
                "counter": counter,
            }

    class Right(StructuralRule):
        def apply(self, target, tips, counter=count(1)):
            target.weakened = True
            # target.sequent_node.sequent[1].remove(target)
            return {
                "queue_items": [[]],
                "counter": counter,
            }

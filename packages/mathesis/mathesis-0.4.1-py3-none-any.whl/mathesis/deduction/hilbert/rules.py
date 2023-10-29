from anytree import Node
from itertools import count
from copy import copy

from mathesis import forms


class Rule:
    pass


# class ModusPonens(Rule):
#     def apply(self, target, tip, antecendent=None, counter=count(1)):
#         conditional = forms.Conditional(antecendent, target.fml)
#         nodeL = Node(
#             str(antecendent),
#             sign=target.sign,
#             fml=antecendent,
#             parent=tip,
#             n=next(counter),
#         )
#         nodeR = Node(
#             str(conditional),
#             sign=target.sign,
#             fml=conditional,
#             parent=tip,
#             n=next(counter),
#         )
#         return {
#             "queue_items": [nodeL, nodeR],
#             "counter": counter,
#         }

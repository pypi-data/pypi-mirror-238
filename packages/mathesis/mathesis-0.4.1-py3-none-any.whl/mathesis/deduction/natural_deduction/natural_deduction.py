from anytree import Node

from mathesis.deduction.sequent_calculus import SequentTree
from mathesis.forms import Formula


class NDTree:
    def __init__(self, premises, conclusion):
        assert isinstance(conclusion, Formula), "Conclusion must be a single formula"
        self._tableau = SequentTree(premises, [conclusion])
        self.bookkeeper = self._tableau.bookkeeper
        self.counter = self._tableau.counter
        self.tree = self._tableau.tree

    def __getitem__(self, index):
        return self.bookkeeper[index]

    def apply(self, target: Node, rule):
        self._tableau.apply(target, rule)
        return self

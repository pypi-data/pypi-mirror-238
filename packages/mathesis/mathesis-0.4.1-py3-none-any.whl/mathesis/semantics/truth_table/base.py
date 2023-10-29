import logging
from itertools import permutations, product
from typing import List, Set

from anytree import Node, NodeMixin, PostOrderIter, RenderTree
from prettytable import PrettyTable, PLAIN_COLUMNS

from mathesis import forms

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ConnectiveClause:
    column_names: List[str]
    table: dict
    truth_value_symbols: None

    def __init__(self, truth_value_symbols=None) -> None:
        self.truth_value_symbols = truth_value_symbols

    def apply(self, *values):
        if None in values:
            return None
        return self.table[values]

    def __str__(self):
        return self.to_string()

    def to_table(self):
        table = PrettyTable()
        table.align = "c"
        table.format = True

        places = len(list(self.table.keys())[0])

        table.field_names = self.column_names

        for values_from, value_to in self.table.items():
            if self.truth_value_symbols:
                values_from = tuple(
                    self.truth_value_symbols.get(v, v) for v in values_from
                )
                value_to = self.truth_value_symbols.get(value_to, value_to)
            table.add_row(values_from + (value_to,))

        return table

    def to_string(self, style=PLAIN_COLUMNS):
        table = self.to_table()
        table.set_style(style)
        return str(table)

    def _repr_html_(self):
        table = self.to_table()
        return table.get_html_string(format=False)


class AssignedNodeBase:
    pass


class AssignedNode(AssignedNodeBase, NodeMixin):
    def __init__(self, name, fml, parent=None, children=[]):
        self.name = name
        self.fml = fml
        self.parent = parent
        self.children = children
        self._truth_value = None

    @property
    def truth_value(self):
        # NOTE: Make sure to specify `is not None`: _truth_value can be 0 and accidentally return False
        if self._truth_value is not None:
            return self._truth_value
        else:
            raise Exception("Truth value not assigned")

    @truth_value.setter
    def truth_value(self, value):
        self._truth_value = value

    def assign_atom_values(self, atom_assignments):
        if isinstance(self.fml, forms.Atom):
            self._truth_value = atom_assignments.get(str(self.fml), None)
        else:
            for child in self.children:
                child.assign_atom_values(atom_assignments)

    def __repr__(self):
        return f"{repr(self.fml)} = {self.truth_value}"

    def __str__(self):
        return f"{str(self.fml)} = {self.truth_value}"


class TruthTable:
    """The truth table class."""

    truth_values: Set = (set(),)
    designated_values: Set = (set(),)
    clauses = {}

    def __init__(
        self,
        formula_or_premises: List[forms.Formula],
        conclusions: List[forms.Formula] = [],
    ):
        if type(formula_or_premises) is list:
            raise NotImplementedError()
        else:
            self.premises = [formula_or_premises]

        self.conclusions = conclusions

    def __str__(self):
        return self.to_string()

    def compute_truth_value(self, assigned_node):
        if isinstance(assigned_node.fml, forms.Atom):
            # assigned_node.truth_value = assigned_node._truth_value
            pass
        elif isinstance(assigned_node.fml, forms.Negation):
            if not forms.Negation in self.clauses:
                raise NotImplementedError("Negation clause not implemented")
            assigned_node.truth_value = self.clauses[forms.Negation].apply(
                assigned_node.children[0].truth_value
            )
        elif isinstance(assigned_node.fml, forms.Conjunction):
            if not forms.Conjunction in self.clauses:
                raise NotImplementedError("Conjunction clause not implemented")
            assigned_node.truth_value = self.clauses[forms.Conjunction].apply(
                *tuple(child.truth_value for child in assigned_node.children)
            )
        elif isinstance(assigned_node.fml, forms.Disjunction):
            if not forms.Disjunction in self.clauses:
                raise NotImplementedError("Disjunction clause not implemented")
            assigned_node.truth_value = self.clauses[forms.Disjunction].apply(
                *tuple(child.truth_value for child in assigned_node.children)
            )
        elif isinstance(assigned_node.fml, forms.Conditional):
            if not forms.Conditional in self.clauses:
                raise NotImplementedError("Conditional clause not implemented")
            assigned_node.truth_value = self.clauses[forms.Conditional].apply(
                *tuple(child.truth_value for child in assigned_node.children)
            )
        else:
            raise NotImplementedError(
                f"Clause for {type(assigned_node.fml)} not implemented"
            )

    def wrap_fml(self, fml):
        def transformer(fml):
            node = AssignedNode(str(fml), fml=fml)
            if isinstance(fml, forms.Binary):
                node.children = [transformer(subfml) for subfml in fml.subs]
            elif isinstance(fml, forms.Unary):
                node.children = [transformer(fml.sub)]
            # NOTE: No truth table for quantifiers
            # elif isinstance(fml, forms.Quantifier):
            #     node.children = [transformer(fml.sub)]
            return node

        wrapped_fml = fml.transform(transformer)
        return wrapped_fml

    def is_valid(self):
        for fml in self.premises + self.conclusions:
            atom_symbols = fml.atoms.keys()
            atom_symbols = sorted(atom_symbols)
            values = []
            for tv in product(self.truth_values, repeat=len(atom_symbols)):
                assignments = dict(zip(atom_symbols, tv))
                tv_fml = self.wrap_fml(fml)
                tv_fml.assign_atom_values(assignments)
                for node in PostOrderIter(tv_fml):
                    self.compute_truth_value(node)
                values.append(tv_fml.truth_value)
            if all([value in self.designated_values for value in values]):
                return True
            else:
                return False

    def counterexample(self):
        pass

    def to_table(self):
        table = PrettyTable()
        table.align = "c"
        table.format = True

        for fml in self.premises + self.conclusions:
            atom_symbols = fml.atoms.keys()
            atom_symbols = sorted(atom_symbols)
            for tv in product(self.truth_values, repeat=len(atom_symbols)):
                assignments = dict(zip(atom_symbols, tv))
                tree = self.wrap_fml(fml)
                # print(RenderTree(tree))
                tree.assign_atom_values(assignments)
                # print(tree.truth_value)
                # print(RenderTree(tree))
                field_names = []
                row = []
                for node in PostOrderIter(tree):
                    self.compute_truth_value(node)
                    # print(str(node.fml), node.truth_value)
                    if str(node.fml) not in field_names:
                        field_names.append(str(node.fml))
                        if hasattr(self, "truth_value_symbols"):
                            truth_value = self.truth_value_symbols.get(
                                node.truth_value, node.truth_value
                            )
                        else:
                            truth_value = node.truth_value
                        row.append(truth_value)
                # print(field_names, row)
                if not table.field_names:
                    table.field_names = field_names
                table.add_row(row)
        return table

    def to_string(self, style=PLAIN_COLUMNS):
        table = self.to_table()
        table.set_style(style)
        return str(table)

    def _repr_html_(self):
        table = self.to_table()
        return table.get_html_string(format=False)

import logging
from typing import Any, List
from anytree import Node, RenderTree, find_by_attr
from operator import itemgetter, neg
from itertools import count
from types import SimpleNamespace

from anytree import Node

from mathesis import forms, _utils
from mathesis.deduction.tableau import rules

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


# class Hilbert:
#     counter = count(1)

#     def __init__(
#         self, premises: List[forms.Formula], conclusions: List[forms.Formula] = []
#     ):
#         self.counter = count(1)
#         self.root = None
#         parent = None
#         for fml in premises:
#             node = Node(
#                 str(fml),
#                 sign=sign.POSITIVE,
#                 fml=fml,
#                 n=next(self.counter),
#             )
#             if not self.root:
#                 self.root = node
#             if parent:
#                 node.parent = parent
#             parent = node
#         for fml in conclusions:
#             node = Node(
#                 str(fml),
#                 sign=sign.NEGATIVE,
#                 fml=fml,
#                 n=next(self.counter),
#             )
#             if not self.root:
#                 self.root = node
#             if parent:
#                 node.parent = parent
#             parent = node

#     def __getitem__(self, index):
#         return find_by_attr(self.root, name="n", value=index)

#     def check_close(self, node1, node2):
#         return node1.name == node2.name and node1.sign != node2.sign

#     def is_closed(self):
#         logger.debug(("leaves: %s", self.root.leaves))
#         if all(getattr(node, "marked", False) for node in self.root.leaves):
#             return True
#         return False

#     def apply(self, target: Node, rule: rules.Rule):
#         self.apply_and_queue(target, rule)
#         return self

#     def apply_and_queue(self, target: Node, rule: rules.Rule, all=True, flatten=True):
#         branch_tips = [
#             leaf for leaf in target.leaves if not getattr(leaf, "branch_marked", False)
#         ]
#         queue_items_all = []
#         for tip in branch_tips:
#             queue_items = itemgetter("queue_items")(
#                 rule.apply(target, tip, self.counter)
#             )
#             # NOTE: check if newly queued nodes are to be marked
#             flattened_queue_items = list(_utils.flatten_list(queue_items))
#             for node in flattened_queue_items:
#                 ancestor = node.parent
#                 while ancestor is not None:
#                     if self.check_close(node, ancestor):
#                         node.marked = True
#                         node.branch_marked = True
#                         for desc in node.descendants:
#                             desc.branch_marked = True
#                         break
#                     ancestor = ancestor.parent
#             queue_items_all += flattened_queue_items
#         return queue_items_all if all else queue_items

#     def htree(self):
#         output = ""
#         for pre, fill, node in RenderTree(self.root):
#             output += "{}{} {} {}{}\n".format(
#                 pre,
#                 node.sign,
#                 node.name,
#                 node.n,
#                 " ×" if getattr(node, "marked", False) else "",
#             )
#         return output

#     def tree(self):
#         return self.htree()

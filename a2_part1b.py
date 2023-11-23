"""CSC148 Assignment 2: Tree Practice (Part 1b)

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This file contains an exercise for the Tree class. This part is optional (not to
be handed in or graded), but we strongly recommend completing it before continuing
to Part 1c.
"""
from __future__ import annotations
from typing import Any
from python_ta.contracts import check_contracts


@check_contracts
class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.

    Attributes:
    - _root:
        The item stored at this tree's root, or None if the tree is empty.
    - _subtrees:
        The list of all subtrees of this tree.

    Representation Invariants:
    - (self._root is None and self._subtrees == []) or self._root is not None
        # i.e. If self._root is None then self._subtrees is an empty list.
        # This setting of attributes represents an empty Tree.
    - self._subtrees does not contain any empty trees

    Note: self._subtrees may be empty when self._root is not None.
    This setting of attributes represents a tree consisting of just one
    node (a 'leaf')
    """
    _root: Any | None
    _subtrees: list[Tree]

    def __init__(self, root: Any | None, subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + str(self._root) + '\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                s += subtree._str_indented(depth + 1)
            return s

    ###########################################################################
    # Exercise
    ###########################################################################
    def insert_repeat(self, item: Any, n: int) -> None:
        """Insert the given item <n> times into this tree.

        The newly inserted <item> values should form a *chain of descendents*,
        starting as a *child* of this tree's root. This chain is added to the right
        of any existing subtrees. See doctest examples.

        Do nothing if n == 0.

        You MUST use recursion to complete this method.

        Preconditions:
        - not self.is_empty()
        - item is not in self
        - n >= 0

        >>> tree1 = Tree(1, [])
        >>> tree1.insert_repeat(5, 0)  # Doesn't insert anything
        >>> print(tree1)
        1
        <BLANKLINE>
        >>> tree1.insert_repeat(10, 1)  # Inserts 10 once
        >>> print(tree1)
        1
          10
        <BLANKLINE>
        >>> tree1.insert_repeat(20, 2)  # Inserts 20 twice
        >>> print(tree1)
        1
          10
          20
            20
        <BLANKLINE>
        >>> tree1.insert_repeat(30, 3)  # Inserts 30 three times
        >>> print(tree1)
        1
          10
          20
            20
          30
            30
              30
        <BLANKLINE>
        """
        if n > 0:
            tree_item = Tree(item, [])
            self._subtrees.append(tree_item)
            n -= 1
            if n > 0:
                tree_item.insert_repeat(item, n)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

"""CSC148 Assignment 2: Autocompleter classes

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This file contains the definition of an Abstract Data Type (Autocompleter) and two
implementations of this interface, SimplePrefixTree and CompressedPrefixTree.
You'll complete both of these subclasses over the course of this assignment.

As usual, be sure not to change any parts of the given *public interface* in the
starter code---and this includes the instance attributes, which we will be
testing directly! You may, however, add new private attributes, methods, and
top-level functions to this file.
"""
from __future__ import annotations
from typing import Any
from python_ta.contracts import check_contracts


################################################################################
# The Autocompleter ADT
################################################################################
class Autocompleter:
    """An abstract class representing the Autocompleter Abstract Data Type.
    """
    def __len__(self) -> int:
        """Return the number of values stored in this Autocompleter."""
        raise NotImplementedError

    def insert(self, value: Any, weight: float, prefix: list) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this autocompleter
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
        - weight > 0
        - the given value is either:
            1) not in this Autocompleter, or
            2) was previously inserted with the SAME prefix sequence
        """
        raise NotImplementedError

    def autocomplete(self, prefix: list,
                     limit: int | None = None) -> list[tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        sorted by non-increasing weight. You can decide how to break ties.

        If limit is None, return *every* match for the given prefix.

        Preconditions:
        - limit is None or limit > 0
        """
        raise NotImplementedError

    def remove(self, prefix: list) -> None:
        """Remove all values that match the given prefix.
        """
        raise NotImplementedError


################################################################################
# SimplePrefixTree (Tasks 1-3)
################################################################################
@check_contracts
class SimplePrefixTree(Autocompleter):
    """A simple prefix tree.

    Instance Attributes:
    - root:
        The root of this prefix tree.
        - If this tree is empty, <root> equals [].
        - If this tree is a leaf, <root> represents a value stored in the Autocompleter
          (e.g., 'cat').
        - If this tree is not a leaf and non-empty, <root> is a list representing a prefix
          (e.g., ['c', 'a']).
    - subtrees:
        A list of subtrees of this prefix tree.
    - weight:
        The weight of this prefix tree.
        - If this tree is empty, this equals 0.0.
        - If this tree is a leaf, this stores the weight of the value stored in the leaf.
        - If this tree is not a leaf and non-empty, this stores the *total weight* of
          the leaf weights in this tree.

    Representation invariants:
    - self.weight >= 0

    - (EMPTY TREE):
        If self.weight == 0.0, then self.root == [] and self.subtrees == [].
        This represents an empty prefix tree.
    - (LEAF):
        If self.subtrees == [] and self.weight > 0, then this tree is a leaf.
        (self.root is a value that was inserted into this tree.)
    - (NON-EMPTY, NON-LEAF):
        If self.subtrees != [], then self.root is a list (representing a prefix),
        and self.weight is equal to the sum of the weights of all leaves in self.

    - self.subtrees does not contain any empty prefix trees.
    - self.subtrees is *sorted* in non-increasing order of weight.
      (You can break ties any way you like.)
      Note that this applies to both leaves and non-leaf subtrees:
      both can appear in the same self.subtrees list, and both have a weight
      attribute.
    """
    root: Any
    weight: float
    subtrees: list[SimplePrefixTree]

    ###########################################################################
    # Part 1(a)
    ###########################################################################
    def __init__(self) -> None:
        """Initialize an empty simple prefix tree.
        """
        self.root = []
        self.weight = 0.0
        self.subtrees = []

    def is_empty(self) -> bool:
        """Return whether this simple prefix tree is empty."""
        if self.weight == 0.0:
            return True
        return False

    def is_leaf(self) -> bool:
        """Return whether this simple prefix tree is a leaf."""
        if self.weight > 0 and self.subtrees == []:
            return True
        return False

    def __len__(self) -> int:
        """Return the number of LEAF values stored in this prefix tree.

        Note that this is a different definition than how we calculate __len__
        of regular trees from lecture!
        """
        leaves = 0
        for item in self.subtrees:
            if item.is_leaf():
                leaves += 1
            elif self.weight > 0:
                leaves += len(item)
        return leaves

    ###########################################################################
    # Extra helper methods
    ###########################################################################
    def __str__(self) -> str:
        """Return a string representation of this prefix tree.

        You may find this method helpful for debugging. You should not change this method
        (nor the helper _str_indented).
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this prefix tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + f'{self.root} ({self.weight})\n'
            for subtree in self.subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    ###########################################################################
    # Add code for Parts 1(c), 2, and 3 here
    ###########################################################################

    def insert(self, value: Any, weight: float, prefix: list, ) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this autocompleter
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
        - weight > 0
        - the given value is either:
            1) not in this Autocompleter, or
            2) was previously inserted with the SAME prefix sequence
        """
        if not prefix:
            self.update_existing_value(value, weight)
            return

        for subtree in self.subtrees:
            if subtree.root == [prefix[0]]:
                if len(prefix) == 1:
                    subtree.update_existing_value(value, weight)
                else:
                    subtree.insert(value, weight, prefix[1:])
                subtree.weight += weight  # Update the weight of the subtree
                return

        # If the first element of the prefix is not found, create a new subtree
        new_subtree = SimplePrefixTree()
        new_subtree.root = [prefix[0]]
        if len(prefix) == 1:
            new_subtree.update_existing_value(value, weight)
        else:
            new_subtree.insert(value, weight, prefix[1:])
        self.subtrees.append(new_subtree)
        self.weight += weight  # Update the weight of the main tree

    def update_existing_value(self, value: Any, weight: float) -> None:
        """ Helper for insert() """
        for subtree in self.subtrees:
            if subtree.root == value[0]:  # Change this line to check the first element of value
                subtree.weight += weight
                return

        # If the value is not found, create a new subtree for it
        new_subtree = SimplePrefixTree()
        new_subtree.root = value[0]  # Change this line to use the first element of value
        new_subtree.weight = weight
        self.subtrees.append(new_subtree)


################################################################################
# CompressedPrefixTree (Part 6)
################################################################################
@check_contracts
class CompressedPrefixTree(SimplePrefixTree):
    """A compressed prefix tree implementation.

    While this class has the same public interface as SimplePrefixTree,
    (including the initializer!) this version follows the definitions
    described in Part 6 of the assignment handout, which reduces the number of
    tree objects used to store values in the tree.

    Representation Invariants:
    - (NEW) This tree does not contain any compressible internal values.
    """
    subtrees: list[CompressedPrefixTree]  # Note the different type annotation

    ###########################################################################
    # Add code for Part 6 here
    ###########################################################################


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Uncomment the python_ta lines below and run this module.
    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run a2_prefix_tree" or
    # "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # you see "None!" under both "Code Errors" and "Style and Convention Errors".
    # TIP: To quickly uncomment lines in PyCharm, select the lines below and press
    # "Ctrl + /" or "⌘ + /".
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'max-nested-blocks': 4
    # })

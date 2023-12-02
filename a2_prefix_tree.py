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
        # If the prefix is empty, directly update or add the value as a leaf
        if not prefix:
            self.update_value_or_add_new(value, weight)
        else:
            # Search for the subtree with the next element in the prefix
            subtree = next((sub for sub in self.subtrees if sub.root == self.root + [prefix[0]]),
                           None)
            if subtree is None:
                # Create a new subtree if not found
                subtree = SimplePrefixTree()
                subtree.root = self.root + [prefix[0]]  # Append to existing root list
                self.subtrees.append(subtree)

            # Recursively insert in the found or new subtree
            subtree.insert(value, weight, prefix[1:])

        # Update the weight of the current tree
        self.update_weight()

    def update_value_or_add_new(self, value: Any, weight: float) -> None:
        """Update an existing value or add a new leaf."""
        for subtree in self.subtrees:
            if subtree.root == value:
                subtree.weight += weight
                return

        # Create a new leaf if the value doesn't exist
        new_leaf = SimplePrefixTree()
        new_leaf.root = value
        new_leaf.weight = weight
        self.subtrees.append(new_leaf)

    def update_weight(self) -> None:
        """Update the weight of this tree based on its subtrees."""
        self.weight = sum(subtree.weight for subtree in self.subtrees)

    def autocomplete(self, prefix: list,
                     limit: int | None = None) -> list[tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        sorted by non-increasing weight. You can decide how to break ties.

        If limit is None, return *every* match for the given prefix.

        Preconditions:
        - limit is None or limit > 0
        """
        suggestions = []

        # Find the subtree corresponding to the given prefix
        subtree = self.find_subtree(prefix)
        if subtree is not None:
            # Recursively collect suggestions from the subtree
            suggestions = subtree.collect_suggestions(limit)

        # Sort the suggestions in non-increasing weight order
        suggestions.sort(key=lambda x: x[1], reverse=True)

        # Limit the number of suggestions if a limit is specified
        if limit is not None:
            suggestions = suggestions[:limit]

        return suggestions

    def find_subtree(self, prefix: list) -> Any:
        """Find the subtree corresponding to the given prefix."""
        if not prefix:
            return self

        # Search for the subtree with the next element in the prefix
        subtree = next((sub for sub in self.subtrees if sub.root[-1] == prefix[0]), None)
        if subtree is not None:
            # Recursively search in the found subtree
            return subtree.find_subtree(prefix[1:])
        else:
            return None

    def collect_suggestions(self, limit: int | None) -> list[tuple[Any, float]]:
        """Recursively collect suggestions from the subtree."""
        suggestions = []

        # Sort subtrees by non-increasing weight order
        sorted_subtrees = sorted(self.subtrees, key=lambda subtree: subtree.weight, reverse=True)

        for subtree in sorted_subtrees:
            # Collect suggestions from each subtree until the limit is reached
            subtree_suggestions = subtree.collect_suggestions(limit)
            suggestions.extend(subtree_suggestions)

            # Update the limit after collecting suggestions from each subtree
            if limit is not None:
                limit -= len(subtree_suggestions)
                if limit <= 0:
                    break

        # Include the root value if it's a leaf node
        if not self.subtrees:
            suggestions.append((self.root, self.weight))

        return suggestions

    def remove(self, prefix: list) -> None:
        """Remove all values associated with the given prefix.

        Preconditions:
        - the given prefix is associated with at least one value in this Autocompleter """
        if not prefix:
            # If the prefix is empty, remove all leaf values
            self.subtrees = []
            self.weight = 0
        else:
            # Search for the subtree with the next element  in the prefix
            subtree = next((sub for sub in self.subtrees if sub.root[-1] == prefix[0]), None)
            if subtree is not None:
                # Recursively remove in the found subtree
                subtree.remove(prefix[1:])

                # If the subtree is now empty, remove it from the list of subtrees
                if subtree.is_empty():
                    self.subtrees.remove(subtree)

            # Update the weight of the current tree
            self.update_weight()


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

    def insert(self, value: Any, weight: float, prefix: list) -> None:
        if not prefix:
            self.root = value
            self.weight += weight
            return

        self.insert_helper(value, weight, prefix)

    def insert_helper(self, value: Any, weight: float, prefix: list, is_recursive = False) -> None:
        """ Helper function to deal with recurse calls"""
        inserted = False
        for i, subtree in enumerate(self.subtrees):
            overlap = self._get_overlap_length(subtree.root, prefix)

            leaf = True
            if len(subtree.subtrees) > 1:
                leaf = False

            if overlap > 0:
                if overlap < len(subtree.root):

                    common_prefix = subtree.root[:overlap]
                    subtree_suffix = subtree.root[overlap:]

                    new_subtree = CompressedPrefixTree()
                    new_subtree.root = common_prefix
                    new_subtree.weight = subtree.weight + weight

                    full_existing_prefix = common_prefix + subtree_suffix
                    subtree.root = full_existing_prefix

                    full_new_prefix = prefix
                    new_value_subtree = CompressedPrefixTree()
                    new_value_subtree.root = full_new_prefix
                    new_value_subtree.insert_simple_subtree(value, weight, [])

                    new_subtree.subtrees.append(subtree)
                    new_subtree.subtrees.append(new_value_subtree)

                    self.subtrees[i] = new_subtree
                    inserted = True
                    break

                elif overlap == len(subtree.root) and not leaf:
                    if is_recursive:
                        subtree.insert(value, weight, prefix[overlap:])
                        inserted = True
                        break
                    else:
                        potential_overlap = subtree._find_deepest_overlap(prefix, overlap)

                        if potential_overlap:
                            potential_overlap.insert_helper(value, weight, prefix, True)
                            inserted = True
                            break

                        new_value = CompressedPrefixTree()
                        new_value.root = value
                        new_value.weight = weight

                        new_subtree = CompressedPrefixTree()
                        new_subtree.root = prefix
                        new_subtree.weight = weight
                        new_subtree.subtrees.append(new_value)

                        subtree.weight += weight
                        subtree.subtrees.append(new_subtree)

                        inserted = True
                elif overlap == len(prefix):

                    potential_overlap = subtree._find_deepest_overlap(prefix, overlap)

                    if potential_overlap:
                        potential_overlap.insert_helper(value, weight, prefix)
                        inserted = True
                        break
                    subtree.insert(value, weight, prefix)
                    inserted = True
                    break

        if not inserted:
            new_subtree = CompressedPrefixTree()
            new_subtree.root = prefix
            new_subtree.insert_simple_subtree(value, weight, [])
            self.subtrees.append(new_subtree)
            self.weight += weight

        self.update_weight()

    def _get_overlap_length(self, subtree_root: Any, new_prefix: list) -> int:
        """Return the length of the overlap between two prefixes."""
        overlap_length = 0
        for a, b in zip(subtree_root, new_prefix):
            if a == b:
                overlap_length += 1
            else:
                break
        return overlap_length

    def _find_deepest_overlap(self, prefix: list, old_overlap: int) -> Any:
        """Return a subtree with the deepest overlap"""
        max_overlap_subtree = None
        max_overlap = old_overlap

        for subtree in self.subtrees:
            overlap = self._get_overlap_length(subtree.root, prefix)
            if overlap > max_overlap:
                max_overlap = overlap
                max_overlap_subtree = subtree

        if max_overlap_subtree:
            # Check if a deeper overlap can be found in the subtrees of the max_overlap_subtree
            deeper_overlap_subtree = max_overlap_subtree._find_deepest_overlap(prefix, max_overlap)
            return deeper_overlap_subtree if deeper_overlap_subtree else max_overlap_subtree

        return None

    def insert_simple_subtree(self, value: Any, weight: float, prefix: list) -> None:
        """Insert a new compressed prefix tree as a subtree with the given prefix."""
        new_subtree = CompressedPrefixTree()
        new_subtree.root = prefix
        new_subtree.weight = weight
        new_subtree.subtrees = []  # Initialize with no subtrees

        if not prefix:
            # If the prefix is empty, this subtree is a leaf with the given value
            new_subtree.root = value
        else:
            # For non-empty prefixes, create a leaf node with the value
            leaf = CompressedPrefixTree()
            leaf.root = value
            leaf.weight = weight
            new_subtree.subtrees.append(leaf)

        self.subtrees.append(new_subtree)
        self.update_weight()

    def update_complete_weight(self) -> None:
        """Recursively update the weight of this tree based on all nested subtrees."""
        self.weight = 0  # Reset weight to 0 before recalculating
        for subtree in self.subtrees:
            subtree.update_weight()  # Recursively update the weight of each subtree
            self.weight += subtree.weight  # Add the updated weight of the subtree


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
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'max-nested-blocks': 4
    })

"""CSC148 Assignment 2: Sample tests

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 2.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

Note: this file is for support purposes only, and is not part of your
assignment submission.
"""
from a2_prefix_tree import SimplePrefixTree, CompressedPrefixTree
from a2_autocomplete_engines import SentenceAutocompleteEngine


###########################################################################
# Parts 1(c) - 3 sample tests
def test_insert_with_empty_prefix() -> None:
    """Test inserting a single value with an empty prefix into a new prefix tree."""
    t = SimplePrefixTree()
    t.insert('value', 1.0, [])

    assert len(t) == 1  # Only the inserted value is counted
    assert t.weight == 1.0  # Weight of the tree should be 1.0

    # Check the structure of the tree
    assert t.root == []  # Root of the tree should have an empty prefix
    assert len(t.subtrees) == 1  # There should be one subtree (the leaf)
    assert t.subtrees[0].root == 'value'  # The leaf should contain the inserted value
    assert t.subtrees[0].weight == 1.0  # The leaf's weight should be 1.0


def test_insert_with_length_one_prefix() -> None:
    """Test inserting a single value with a length-one prefix into a new prefix tree."""
    t = SimplePrefixTree()
    t.insert('value', 1.0, ['x'])

    assert len(t) == 1  # Only the inserted value is counted
    assert t.weight == 1.0  # Weight of the tree should be 1.0

    # Check the structure of the tree
    assert t.root == []  # Root of the tree should have an empty prefix
    assert len(t.subtrees) == 1  # There should be one subtree (internal node with prefix [x])
    assert t.subtrees[0].root == ['x']  # The internal node should have the prefix [x]
    assert len(t.subtrees[0].subtrees) == 1  # The internal node should have one subtree (the leaf)
    assert t.subtrees[0].subtrees[0].root == 'value'  # The leaf should contain the inserted value
    assert t.subtrees[0].subtrees[0].weight == 1.0  # The leaf's weight should be 1.0


# def test_insert_with_length_n_prefix() -> None:
#     """Test inserting a single value with a length-n prefix into a new prefix tree."""
#     t = SimplePrefixTree()
#     prefix = ['x1', 'x2', 'x3']
#     t.insert('value', 1.0, prefix)
#
#     assert len(t) == 1  # Only the inserted value is counted
#     assert t.weight == 1.0  # Weight of the tree should be 1.0
#
#     # Check the structure of the tree
#     current = t
#     for element in prefix:
#         assert len(current.subtrees) == 1  # Each node should have exactly one subtree
#         current = current.subtrees[0]
#         assert current.root == [element]  # Each node should have the correct prefix
#
#     # Check the leaf node
#     assert current.subtrees[0].root == 'value'  # The leaf should contain the inserted value
#     assert current.subtrees[0].weight == 1.0  # The leaf's weight should be 1.0

###########################################################################


def test_simple_prefix_tree_structure() -> None:
    """This is a test for the structure of a small simple prefix tree.

    NOTE: This test should pass even if you insert these values in a different
    order. This is a good thing to try out.
    """
    t = SimplePrefixTree()
    t.insert('cat', 2.0, ['c', 'a', 't'])
    t.insert('car', 3.0, ['c', 'a', 'r'])
    t.insert('dog', 4.0, ['d', 'o', 'g'])

    # t has 3 values (note that __len__ only counts the inserted values,
    # which are stored at the *leaves* of the tree).
    assert len(t) == 3

    # t has a total weight of 9.0
    assert t.weight == 2.0 + 3.0 + 4.0

    # t has two subtrees, and order matters (because of weights).
    assert len(t.subtrees) == 2
    left = t.subtrees[0]
    right = t.subtrees[1]

    assert left.root == ['c']
    assert left.weight == 5.0

    assert right.root == ['d']
    assert right.weight == 4.0


def test_simple_prefix_tree_autocomplete() -> None:
    """This is a test for the correct autocomplete behaviour for a small
    simple prefix tree.

    NOTE: This test should pass even if you insert these values in a different
    order. This is a good thing to try out.
    """
    t = SimplePrefixTree()
    t.insert('dog', 4.0, ['d', 'o', 'g'])
    t.insert('car', 3.0, ['c', 'a', 'r'])
    t.insert('cat', 2.0, ['c', 'a', 't'])
    t.insert('camp', 5.0, ['c', 'a', 'm', 'p'])

    # Note that the returned tuples *must* be sorted in non-increasing weight
    # order. You can (and should) sort the tuples yourself inside
    # SimplePrefixTree.autocomplete.
    assert t.autocomplete([]) == [('camp', 5.0), ('dog', 4.0), ('car', 3.0), ('cat', 2.0)]

    # But keep in mind that the greedy algorithm here does not necessarily
    # return the highest-weight values!! In this case, the ['c'] subtree
    # is recursed on first.
    assert t.autocomplete([], 1) == [('camp', 5.0)]
    assert t.autocomplete([], 2) == [('camp', 5.0), ('car', 3.0)]
    assert t.autocomplete([], 4) == [('camp', 5.0), ('dog', 4.0), ('car', 3.0), ('cat', 2.0)]

    assert t.autocomplete(['c'], 2) == [('camp', 5.0), ('car', 3.0)]
    assert t.autocomplete(['c'], 3) == [('camp', 5.0), ('car', 3.0), ('cat', 2.0)]
    assert t.autocomplete(['d'], 2) == [('dog', 4.0)]
    assert t.autocomplete(['c', 'a'], 2) == [('camp', 5.0), ('car', 3.0)]


def test_simple_prefix_tree_remove() -> None:
    """This is a test for the correct remove behaviour for a small
    simple prefix tree.

    NOTE: This test should pass even if you insert these values in a different
    order. This is a good thing to try out.
    """
    t = SimplePrefixTree()
    t.insert('cat', 2.0, ['c', 'a', 't'])
    t.insert('car', 3.0, ['c', 'a', 'r'])
    t.insert('dog', 4.0, ['d', 'o', 'g'])
    print(t)

    # The trickiest part is that only *values* should be stored at leaves,
    # so even if you remove a specific prefix, its parent might get removed
    # from the tree as well!
    t.remove(['c', 'a'])

    assert len(t) == 1
    assert t.weight == 4.0

    # There is no more ['c'] subtree!
    assert len(t.subtrees) == 1
    assert t.subtrees[0].root == ['d']


###########################################################################
# Part 4 sample test (add your own for Parts 4 and 5!)
###########################################################################
def test_sentence_autocompleter() -> None:
    """Basic test for SentenceAutocompleteEngine.

    This test relies on the sample_sentences.csv dataset. That file consists
    of just a few lines, but there are three important details to notice:

        1. You should use the second entry of each csv file as the weight of
           the sentence. This entry can be a float! (Don't assume it's an int.)
        2. The file contains two sentences that are sanitized to the same
           string, and so this value is inserted twice. This means its weight
           is the *sum* of the weights from each of the two lines in the file.
        3. Numbers *are allowed* in the strings (this is true for both types
           of text-based autocomplete engines). Don't remove them!
    """
    engine = SentenceAutocompleteEngine({
        'file': 'data/texts/sample_sentences.csv',
        'autocompleter': 'simple'
    })

    # Check simple autocompletion and sanitization
    results = engine.autocomplete('what a')
    assert len(results) == 1
    assert results[0][0] == 'what a wonderful world'
    assert results[0][1] == 1.0

    # Check that numbers are allowed in the sentences
    results = engine.autocomplete('numbers')
    assert len(results) == 1
    assert results[0][0] == 'numbers are 0k4y'

    # Check that one sentence can be inserted twice
    results = engine.autocomplete('a')
    assert len(results) == 1
    assert results[0][0] == 'a star is born'
    assert results[0][1] == 15.0 + 6.5


# ###########################################################################
# # Part 6 sample tests
# ###########################################################################
def test_compressed_prefix_tree_structure() -> None:
    """This is a test for the correct structure of a compressed prefix tree.

    NOTE: This test should pass even if you insert these values in a different
    order. This is a good thing to try out.
    """
    t = CompressedPrefixTree()
    t.insert('cat', 2.0, ['c', 'a', 't'])
    t.insert('car', 3.0, ['c', 'a', 'r'])
    t.insert('dog', 4.0, ['d', 'o', 'g'])

    # t has 3 values (note that __len__ only counts the values, which are
    # stored at the *leaves* of the tree).
    assert len(t) == 3

    # t has a total weight of 9.0
    assert t.weight == 2.0 + 3.0 + 4.0

    # t has two subtrees, and order matters (because of weights).
    assert len(t.subtrees) == 2
    left = t.subtrees[0]
    right = t.subtrees[1]

    # But note that the prefix values are different than for a SimplePrefixTree!
    assert left.root == ['c', 'a']
    assert left.weight == 5.0

    assert right.root == ['d', 'o', 'g']
    assert right.weight == 4.0



if __name__ == '__main__':
    import pytest
    pytest.main(['a2_sample_test.py'])

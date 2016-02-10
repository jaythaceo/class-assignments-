"""
Binary Search Tree: A sorted collection of values that supports
efficient insertion, deletion, and minimum/maximum value finding.
"""

# IMPLEMENTATION NOTES:
#
# Internally, we represent tree nodes using Python lists.  These lists
# may either be empty (for empty nodes) or may have length four (for
# non-empty nodes).  The non-empty nodes contain:
#
#     [left_child, right_child, value, sort_key]
#
# Using lists rather than a node class more than doubles the overall
# performance in the benchmarks that I have run.
#
# The sort key is always accessed as node[-1].  This allows us to
# optimize the case where the sort key is identical to the value, by
# encoding such nodes as simply:
#
#     [left_child, right_child, value]
#
_LEFT = 0
_RIGHT = 1
_VALUE = 2
_SORT_KEY = -1

class BinarySearchTree(object):
    """
    A sorted collection of values that supports efficient insertion,
    deletion, and minimum/maximum value finding.  Values may sorted
    either based on their own value, or based on a key value whose
    value is computed by a key function (specified as an argument to
    the constructor).

    BinarySearchTree allows duplicates -- i.e., a BinarySearchTree may
    contain multiple values that are equal to one another (or multiple
    values with the same key).  The ordering of equal values, or
    values with equal keys, is undefined.
    """
    def __init__(self, sort_key=None):
        """
        Create a new empty BST.  If a sort key is specified, then it
        will be used to define the sort order for the BST.  If an
        explicit sort key is not specified, then each value is
        considered its own sort key.
        """
        self._root = [] # = empty node
        self._sort_key = sort_key
        self._len = 0 # keep track of how many items we contain.

    #/////////////////////////////////////////////////////////////////
    # Public Methods
    #/////////////////////////////////////////////////////////////////

    def insert(self, value):
        """
        Insert the specified value into the BST.
        """
        # Get the sort key for this value.
        if self._sort_key is None:
            sort_key = value
        else:
            sort_key = self._sort_key(value)
        # Walk down the tree until we find an empty node.
        node = self._root
        while node:
            if sort_key < node[_SORT_KEY]:
                node = node[_LEFT]
            else:
                node = node[_RIGHT]
        # Put the value in the empty node.
        if sort_key is value:
            node[:] = [[], [], value]
        else:
            node[:] = [[], [], value, sort_key]
        self._len += 1

    def minimum(self):
        """
        Return the value with the minimum sort key.  If multiple
        values have the same (minimum) sort key, then it is undefined
        which one will be returned.
        """
        return self._extreme_node(_LEFT)[_VALUE]

    def maximum(self):
        """
        Return the value with the maximum sort key.  If multiple values
        have the same (maximum) sort key, then it is undefined which one
        will be returned.
        """
        return self._extreme_node(_RIGHT)[_VALUE]

    def find(self, sort_key):
        """
        Find a value with the given sort key, and return it.  If no such
        value is found, then raise a KeyError.
        """
        return self._find(sort_key)[_VALUE]

    def pop_min(self):
        """
        Return the value with the minimum sort key, and remove that value
        from the BST.  If multiple values have the same (minimum) sort key,
        then it is undefined which one will be returned.
        """
        return self._pop_node(self._extreme_node(_LEFT))

    def pop_max(self):
        """
        Return the value with the maximum sort key, and remove that value
        from the BST.  If multiple values have the same (maximum) sort key,
        then it is undefined which one will be returned.
        """
        return self._pop_node(self._extreme_node(_RIGHT))

    def pop(self, sort_key):
        """
        Find a value with the given sort key, remove it from the BST, and
        return it.  If multiple values have the same sort key, then it is
        undefined which one will be returned.  If no value has the
        specified sort key, then raise a KeyError.
        """
        return self._pop_node(self._find(sort_key))

    def values(self, reverse=False):
        """Generate the values in this BST in sorted order."""
        if reverse:
            return self._iter(_RIGHT, _LEFT)
        else:
            return self._iter(_LEFT, _RIGHT)
    __iter__ = values

    def __len__(self):
        """Return the number of items in this BST"""
        return self._len

    def __nonzero__(self):
        """Return true if this BST is not empty"""
        return self._len>0

    def __repr__(self):
        return '<BST: (%s)>' % ', '.join('%r' % v for v in self)

    def __str__(self):
        return self.pprint()

    def pprint(self, max_depth=10, frame=True, show_key=True):
        """
        Return a pretty-printed string representation of this binary
        search tree.
        """
        t,m,b = self._pprint(self._root, max_depth, show_key)
        lines = t+[m]+b
        if frame:
            width = max(40, max(len(line) for line in lines))
            s = '+-'+'MIN'.rjust(width, '-')+'-+\n'
            s += ''.join('| %s |\n' % line.ljust(width) for line in lines)
            s += '+-'+'MAX'.rjust(width, '-')+'-+\n'
            return s
        else:
            return '\n'.join(lines)

    #/////////////////////////////////////////////////////////////////
    # Private Helper Methods
    #/////////////////////////////////////////////////////////////////

    def _extreme_node(self, side):
        """
        Return the leaf node found by descending the given side of the
        BST (either _LEFT or _RIGHT).
        """
        if not self._root:
            raise IndexError('Empty Binary Search Tree!')
        node = self._root
        # Walk down the specified side of the tree.
        while node[side]:
            node = node[side]
        return node

    def _find(self, sort_key):
        """
        Return a node with the given sort key, or raise KeyError if not found.
        """
        node = self._root
        while node:
            node_key = node[_SORT_KEY]
            if sort_key < node_key:
                node = node[_LEFT]
            elif sort_key > node_key:
                node = node[_RIGHT]
            else:
                return node
        raise KeyError("Key %r not found in BST" % sort_key)

    # Add pop-node here

    def _iter(self, pre, post):
        # Helper for sorted iterators.
        #   - If (pre,post) = (_LEFT,_RIGHT), then this will generate items
        #     in sorted order.
        #   - If (pre,post) = (_RIGHT,_LEFT), then this will generate items
        #     in reverse-sorted order.
        # We use an iterative implemenation (rather than the recursive one)
        # for efficiency.
        stack = []
        node = self._root
        while stack or node:
            if node: # descending the tree
                stack.append(node)
                node = node[pre]
            else: # ascending the tree
                node = stack.pop()
                yield node[_VALUE]
                node = node[post]

    def _pprint(self, node, max_depth, show_key, spacer=2):
        """
        Returns a (top_lines, mid_line, bot_lines) tuple,
        """
        if max_depth == 0:
            return ([], '- ...', [])
        elif not node:
            return ([], '- EMPTY', [])
        else:
            top_lines = []
            bot_lines = []
            mid_line = '-%r' % node[_VALUE]
            if len(node) > 3: mid_line += ' (key=%r)' % node[_SORT_KEY]
            if node[_LEFT]:
                t,m,b = self._pprint(node[_LEFT], max_depth-1,
                                     show_key, spacer)
                indent = ' '*(len(b)+spacer)
                top_lines += [indent+' '+line for line in t]
                top_lines.append(indent+'/'+m)
                top_lines += [' '*(len(b)-i+spacer-1)+'/'+' '*(i+1)+line
                              for (i, line) in enumerate(b)]
            if node[_RIGHT]:
                t,m,b = self._pprint(node[_RIGHT], max_depth-1,
                                     show_key, spacer)
                indent = ' '*(len(t)+spacer)
                bot_lines += [' '*(i+spacer)+'\\'+' '*(len(t)-i)+line
                              for (i, line) in enumerate(t)]
                bot_lines.append(indent+'\\'+m)
                bot_lines += [indent+' '+line for line in b]
            return (top_lines, mid_line, bot_lines)

try:

    from optimize_constants import bind_all
    bind_all(BinarySearchTree)
except:
    pass

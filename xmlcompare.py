from itertools import product


class XMLCompare:
    """ Compare ElementTree Elements looking for an identical
    tree strucure. """
    def is_equal(self, expected_node, actual_node):
        if not self._compare_nodes(expected_node, actual_node):
            # not the same root node
            return False

        return self._compare_children(expected_node, actual_node)

    @staticmethod
    def _compare_nodes(node1, node2):
        return (
            node1.tag == node2.tag and
            node1.attrib == node2.attrib and
            node1.text == node2.text
        )

    def _get_matching_pairs(self, list1, list2):
        # lists of children are unorderd, cannot easily be generically
        # ordered and can have attributes declared in any order too.
        # so this is a brute force approach to comparing elements in 2
        # lists and returning those that are identical in a list of
        # two-tuples.
        pairs = []
        for pair in product(list1, list2):
            if self._compare_nodes(*pair):
                pairs.append(pair)

        return pairs

    def _compare_children(self, expected_node, actual_node):
        # assumes parents are equal
        next_expected_nodes = expected_node.getchildren()
        next_actual_nodes = actual_node.getchildren()

        if len(next_expected_nodes) != len(next_actual_nodes):
            return False

        if len(next_expected_nodes) == 0:
            return True

        pairs = self._get_matching_pairs(
            next_expected_nodes, next_actual_nodes)

        if len(pairs) != len(next_expected_nodes):
            # children do not match on either tag names or attributes,
            # or both.
            return False

        for pair in pairs:
            are_equal = self._compare_children(*pair)
            if not are_equal:
                print('unequal XML pairs: %s, %s', *pair)
                return False

        return True

#!/usr/bin/env python3

import potatolib

class Example:
    def nor(a, b):
        # lobster-trace: req_nor
        assert isinstance(a, bool)
        assert isinstance(b, bool)

        def helper(a, b):
            # potato
            return a or b

        # kitten

        return helper(a, b)

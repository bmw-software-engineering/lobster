import potatolib


def trlc_reference(requirement):
    # lobster-exclude: helper function
    def decorator(obj):
        return obj
    return decorator


class Example:
    @trlc_reference(requirement="example.req_nor")
    def helper_function(a, b):
        # potato
        return a or b

    def nor(a, b):
        # lobster-trace: example.req_nor
        assert isinstance(a, bool)
        assert isinstance(b, bool)

        return not helper_function(a, b)

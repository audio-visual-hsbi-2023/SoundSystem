from functools import total_ordering


@total_ordering
class Phase:
    def __init__(self, order, name, directory):
        self.order = order
        self.name = name
        self.directory = directory

    @staticmethod
    def _is_valid_operand(other):
        return isinstance(other, Phase)

    def __eq__(self, other):
        if not Phase._is_valid_operand(other):
            return NotImplemented
        return self.order == other.order

    def __lt__(self, other):
        if not Phase._is_valid_operand(other):
            return NotImplemented
        return self.order < other.order

    def __le__(self, other):
        if not Phase._is_valid_operand(other):
            return NotImplemented
        return self.order <= other.order

    def __gt__(self, other):
        if not Phase._is_valid_operand(other):
            return NotImplemented
        return self.order > other.order

    def __ge__(self, other):
        if not Phase._is_valid_operand(other):
            return NotImplemented
        return self.order >= other.order

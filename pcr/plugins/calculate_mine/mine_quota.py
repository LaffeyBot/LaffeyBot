class Mine(object):
    def __init__(self, start_rank, end_rank, per_mine):
        self.start_rank = start_rank
        self.per_mine = per_mine  # 矿区单位矿
        self.end_rank = end_rank

    def range_mine_calculate(self) -> int:
        pass

    def get_before_mine(self, rank) -> int:
        pass

    def get_after_mine(self, rank) -> int:
        pass

    def range_in_mine(self, rank1, rank2) -> int:
        pass

    def is_this_range(self, rank) -> bool:
        if self.start_rank <= rank < self.end_rank:
            return True
        else:
            return False


class Season_sequence_mine(Mine):
    def range_mine_calculate(self):
        return self.calculate(self.start_rank, self.end_rank)

    def get_before_mine(self, rank):
        return self.calculate(self.start_rank, rank)

    def get_after_mine(self, rank):
        return self.calculate(rank, self.end_rank)

    def range_in_mine(self, rank1, rank2):
        return self.calculate(rank1, rank2)

    def calculate(self, sr, er):
        count = 0
        for i in range(sr, er):
            count += 1
        return count * self.per_mine


class Season_nonsequence_mine(Mine):
    def range_mine_calculate(self):
        return self.calculate(self.start_rank, self.end_rank)

    def get_before_mine(self, rank):
        return self.calculate(self.start_rank, rank)

    def get_after_mine(self, rank):
        return self.calculate(rank, self.end_rank)

    def range_in_mine(self, rank1, rank2):
        return self.calculate(rank1, rank2)

    def calculate(self, sr, er):
        count = 0
        for i in range(sr, er):
            if i % 100 == 0:
                count += 1
        return count * self.per_mine


class History_sequence_mine(Season_sequence_mine):
    pass


class History_nonsequence_mine(Season_nonsequence_mine):
    pass

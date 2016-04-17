class Congruential:
    def __init__(self, m, a, c, seed):
        self.m = m
        self.a = a
        self.c = c
        self.seed = seed
        self.prev = 0

    def next(self):
        some_op = float(self.a * self.prev + self.c)
        self.prev = divmod(some_op, self.m)
        return float(self.prev) / float(self.m)
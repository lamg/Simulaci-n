class stats:
    def random_num_congr(self, seed, a, c, m, num_quantity, is_seed_included):
        num_rand_list = []
        if (a > 0 and c > 0 and m > 0) and (a < m and c < m):
            i = 0
            if is_seed_included:
                num_rand_list[i] = seed
                i = 1
            else:
                n = divmod(float(a * seed + c), m)
                num_rand_list[i] = n
                i += 1
            while i < num_quantity:
                n = divmod(float(a * num_rand_list[i - 1] + c), m)
                num_rand_list[i] = n
                i += 1
            for j in range(len(num_rand_list)):
                num_rand_list[j] /= float(m)

            return num_rand_list
        else:
            raise Exception("Some parameters got errors.")
from typing import List


def sample_list_without_bound(population: List, k: int):
    from random import sample
    q = k // len(population)
    return population * q + sample(population, k % len(population))


def sample_list_with_bound(population: List, k: int):
    from random import sample
    if k >= len(population):
        return population
    return sample(population, k)

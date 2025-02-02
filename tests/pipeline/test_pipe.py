import math

from src.useful_decorators.pipeline.pipe import Pipe


def test_pipe():
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        return not any(n % i == 0 for i in range(2, int(math.sqrt(n)) + 1))

    @Pipe.stage()
    def get_primes(numbers):
        try:
            return list(filter(is_prime, numbers))
        except TypeError as e:
            return None, e

    @Pipe.stage()
    def sum_indexes(numbers):
        return (sum(numbers[::2]), sum(numbers[1::2]))

    @Pipe.stage()
    def larger_item(numbers):
        return max(*numbers)

    assert Pipe.run([get_primes, sum_indexes, larger_item], range(100)) == 556

"""Round-trip tests for PTM signed exponent vectors and formal prime realizations."""
from __future__ import annotations

import random
import unittest
from dataclasses import dataclass
from typing import Iterable, Tuple

PRIMES: Tuple[int, ...] = (2, 3, 7, 11, 13)


def split_signed_exponents(delta: Iterable[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return positive and negative exponent vectors for a signed delta."""
    d = tuple(int(x) for x in delta)
    return tuple(max(x, 0) for x in d), tuple(max(-x, 0) for x in d)


def inverse_exponentiation(positive: Iterable[int], negative: Iterable[int]) -> tuple[int, ...]:
    """Recover the signed exponent vector from its positive/negative decomposition."""
    p, n = tuple(positive), tuple(negative)
    if len(p) != len(n):
        raise ValueError("positive and negative exponent vectors must have equal length")
    if any(x < 0 for x in p + n):
        raise ValueError("factor exponents must be nonnegative")
    return tuple(a - b for a, b in zip(p, n))


def compose_delta(a: Iterable[int], b: Iterable[int]) -> tuple[int, ...]:
    a, b = tuple(a), tuple(b)
    if len(a) != len(b):
        raise ValueError("delta vectors must have equal length")
    return tuple(x + y for x, y in zip(a, b))


def materialize_ratio(delta: Iterable[int], primes: Iterable[int] = PRIMES) -> tuple[int, int]:
    """Materialize Q+/Q- only for modest exponents used in unit tests."""
    d, ps = tuple(delta), tuple(primes)
    if len(d) != len(ps):
        raise ValueError("delta and prime vectors must have equal length")
    positive, negative = split_signed_exponents(d)
    q_plus = 1
    q_minus = 1
    for prime, ep, en in zip(ps, positive, negative):
        q_plus *= prime ** ep
        q_minus *= prime ** en
    return q_plus, q_minus


class TestPTMRoundTrips(unittest.TestCase):
    def test_dense_whole_vector_round_trip(self):
        delta = (-3, 0, 5, -2, 4)
        pos, neg = split_signed_exponents(delta)
        self.assertEqual(inverse_exponentiation(pos, neg), delta)

    def test_positive_zero_negative_coordinates(self):
        for delta in [(4, 6, 2), (0, 0, 0), (-1, -9, -2)]:
            pos, neg = split_signed_exponents(delta)
            self.assertEqual(inverse_exponentiation(pos, neg), delta)

    def test_large_exponents_beyond_64_bit(self):
        huge = 2**255
        delta = (huge, -huge, huge + 17, -(huge + 31), 0)
        pos, neg = split_signed_exponents(delta)
        self.assertEqual(inverse_exponentiation(pos, neg), delta)

    def test_composition_then_round_trip(self):
        d1 = (-2, 3, 0, 7, -5)
        d2 = (3, -2, 4, -7, 5)
        composite = compose_delta(d1, d2)
        self.assertEqual(composite, (1, 1, 4, 0, 0))
        pos, neg = split_signed_exponents(composite)
        self.assertEqual(inverse_exponentiation(pos, neg), composite)

    def test_prime_realization_composition(self):
        d1 = (-2, 3, 0, 0, 0)
        d2 = (3, -2, 0, 0, 0)
        dc = compose_delta(d1, d2)
        n1, m1 = materialize_ratio(d1)
        n2, m2 = materialize_ratio(d2)
        nc, mc = materialize_ratio(dc)
        # Compare exact rationals by cross multiplication, avoiding float arithmetic.
        self.assertEqual(n1 * n2 * mc, nc * m1 * m2)

    def test_randomized_round_trips(self):
        rng = random.Random(1300)
        for _ in range(10_000):
            delta = tuple(rng.randint(-(10**40), 10**40) for _ in PRIMES)
            pos, neg = split_signed_exponents(delta)
            self.assertEqual(inverse_exponentiation(pos, neg), delta)

    def test_no_materialization_needed_for_huge_vectors(self):
        delta = (10**1000, -(10**1000), 2**1024, -(2**1024), 0)
        pos, neg = split_signed_exponents(delta)
        self.assertEqual(inverse_exponentiation(pos, neg), delta)

    def test_reject_negative_factor_exponents(self):
        with self.assertRaises(ValueError):
            inverse_exponentiation((1, -1), (0, 0))

    def test_reject_dimension_mismatch(self):
        with self.assertRaises(ValueError):
            inverse_exponentiation((1, 2), (1,))
        with self.assertRaises(ValueError):
            compose_delta((1, 2), (1,))


if __name__ == "__main__":
    unittest.main(verbosity=2)

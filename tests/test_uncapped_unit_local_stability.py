"""Algebraic checks of the general saddle-path proof in Proposition 4.

Exact rational identities and independent polynomial determinants supplement
the analytic sign argument; a parameter grid is not itself an existence proof.
No transition is simulated and no simulation code is changed.
"""
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from define_positive_ai_branch import (
    PositiveAIBenchmarkParameters, balanced_growth_seed,
    normalized_dynamics, normalized_jacobian,
)


def coefficients(alpha, eta, omega, d, g, delta):
    """Proof abbreviations, preserving exact arithmetic for rational inputs."""
    weight = (1-alpha)*omega
    aK = alpha/(1-weight)
    aT = weight*eta/((1-weight)*(1-eta))
    P = d+g+delta
    h = d+eta*g
    k = alpha/P
    m = weight**2*eta**2*g/((1-eta)*h)
    cs = 1-weight**2-(g+delta)*k-m
    A = d+weight*P
    B = ((1-weight**2)*aT-m)/k
    C = cs/k
    V = m/(k*(1-eta))
    D = eta*g/(1-eta)
    G, H = P*(1-aK), P*aT
    E, Fcoef = G+h*aK, H+h*(1-aT)
    L = B-V*d/D
    N, Q = C*G+V*E, C*H+V*Fcoef
    J = [[A, B, -C, -V], [0, 0, 0, D],
         [-G, H, 0, 0], [-E, Fcoef, 0, d]]
    return locals()


def multiply(left, right):
    """Polynomial product, constant coefficient first."""
    result = [F(0)]*(len(left)+len(right)-1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i+j] += x*y
    return result


def determinant_polynomial(matrix):
    """Independent Leibniz expansion of det(x I-J), all 24 permutations."""
    result = [F(0)]*5
    for permutation in permutations(range(4)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(4) for j in range(i+1, 4))
        term = [F((-1)**inversions)]
        for row, col in enumerate(permutation):
            term = multiply(term, [-matrix[row][col], int(row == col)])
        for i, value in enumerate(term):
            result[i] += value
    return result


class UncappedUnitLocalStability(unittest.TestCase):
    def test_exact_polynomial_identities_and_signs(self):
        count = 0
        for alpha, eta, omega in product(
            map(F, (".05", ".33", ".6", ".85", ".99")),
            map(F, (".01", ".2", ".5", ".75", ".98")),
            map(F, (".01", ".1", ".2", ".49", ".7", ".98")),
        ):
            if not (eta < alpha and eta+omega < 1
                    and (1-alpha)*omega <= F(1, 2)):
                continue
            for d, g, delta in (
                (F(".037"), F(".014"), F(".05")),
                (F(".001"), F(".3"), F(0)),
                (F(".000001"), F(".000002"), F(".5")),
            ):
                with self.subTest(alpha=alpha, eta=eta, omega=omega,
                                  d=d, g=g, delta=delta):
                    z = coefficients(alpha, eta, omega, d, g, delta)
                    A, C, D, E, G, H, h, P, N, Q, L, Fc = (
                        z[key] for key in
                        ("A", "C", "D", "E", "G", "H", "h", "P",
                         "N", "Q", "L", "Fcoef"))
                    gap = 1-z["aK"]-z["aT"]
                    self.assertEqual(gap, (1-alpha)*(1-eta-omega)
                                     / ((1-(1-alpha)*omega)*(1-eta)))
                    self.assertEqual(L, (1-alpha)*omega*eta/((1-eta)*z["k"]))
                    self.assertEqual(G*Fc-H*E, h*P*gap)
                    for value in (A, C, D, E, G, H, h, P, N, Q, L, Fc, gap):
                        self.assertGreater(value, 0)
                    expected = [D*C*h*P*gap, A*D*Fc+d*N+L*D*E,
                                A*d-N-D*Fc, -(A+d), F(1)]
                    self.assertEqual(determinant_polynomial(z["J"]), expected)
                    factorized = multiply([-N, -A, F(1)], [-D*Fc, -d, F(1)])
                    factorized[0] -= D*E*Q
                    factorized[1] += D*E*L
                    self.assertEqual(factorized, expected)
                    # Descartes on p(-x): ignore zero coefficients.
                    signs = [np.sign(value*(-1)**power)
                             for power, value in enumerate(expected) if value]
                    self.assertEqual(sum(a != b for a, b in zip(signs, signs[1:])), 2)
                    count += 1
        self.assertEqual(count, 198)

    def test_similarity_to_preserved_equilibrium_jacobian(self):
        for alpha, eta, omega in ((.33, .2, .2), (.6, .5, .2), (.7, .6, .2),
                                  (.85, .75, .1), (.33, .2, .7), (.6, .02, .9)):
            p = PositiveAIBenchmarkParameters(alpha=alpha, eta=eta, omega_x=omega)
            s = balanced_growth_seed(p)
            z = coefficients(alpha, eta, omega, p.discount-p.population_growth,
                             s.output_growth, p.depreciation)
            nu = (1-eta)/eta
            transform = np.array([[1, 0, 0, 0], [0, nu, 0, 0],
                                  [0, 0, 1, 0], [0, 1-nu, 0, 1]])
            matrix = np.array(z["J"])
            actual = transform @ normalized_jacobian(np.zeros(4), p, s) @ np.linalg.inv(transform)
            # Tolerances cover floating-point cancellation only, not a
            # numerical rule for accepting an equilibrium or its existence.
            np.testing.assert_allclose(actual, matrix, rtol=5e-13, atol=2e-14)
            roots, vectors = np.linalg.eig(matrix)
            stable = sorted(roots[roots.real < 0].real)
            self.assertEqual(len(stable), 2)
            D, Fc, d = z["D"], z["Fcoef"], z["d"]
            mu = (d-np.sqrt(d*d+4*D*Fc))/2
            self.assertLess(stable[0], mu)
            self.assertLess(mu, stable[1])
            projections = [(D*Fc+d*ell-ell*ell)/(D*z["E"]) for ell in stable]
            self.assertLess(projections[0], 0)
            self.assertGreater(projections[1], 0)
            for index in np.flatnonzero(roots.real < 0):
                eigenvector = vectors[:, index]/vectors[1, index]
                expected_x = (D*Fc+d*roots[index]-roots[index]**2)/(D*z["E"])
                np.testing.assert_allclose(eigenvector[0], expected_x, rtol=2e-11, atol=2e-12)

    def test_normalized_field_is_independent_of_initial_exogenous_levels(self):
        reference = PositiveAIBenchmarkParameters()
        seed = balanced_growth_seed(reference)
        for A0, N0 in ((.8, 1.2), (2., .4), (10., 5.)):
            p = PositiveAIBenchmarkParameters(initial_labor_productivity=A0,
                                               initial_population=N0)
            s = balanced_growth_seed(p)
            for point in (np.zeros(4), np.array([.01, -.02, .03, -.01])):
                np.testing.assert_allclose(normalized_dynamics(point, p, s),
                                           normalized_dynamics(point, reference, seed),
                                           rtol=5e-13, atol=2e-14)


if __name__ == "__main__":
    unittest.main()

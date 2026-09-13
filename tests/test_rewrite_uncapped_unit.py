"""Validate the recovered uncapped unit-elastic appendix without new simulations.

Independent formulas for its levels, rates and Jacobian are compared with the
preserved positive-AI implementation. Source checks enforce the appendix/proof
split. Floating-point tolerances check arithmetic, not existence theorems.
"""
from pathlib import Path
import re
import sys
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from define_positive_ai_branch import (  # noqa: E402
    PositiveAIBenchmarkParameters,
    balanced_growth_seed,
    canonical_seed_residuals,
    normalized_jacobian,
    stable_subspace,
)


class UncappedUnitAppendix(unittest.TestCase):
    def test_closed_form_levels_rates_and_all_dated_conditions(self):
        # Includes the main and historical research productivities and the
        # boundary eta=1/2, where research is weakly jointly concave.
        configurations = [
            PositiveAIBenchmarkParameters(omega_x=w, chi=chi)
            for w in (0.05, 0.20, 0.40, 0.70)
            for chi in (0.01, 1.4378)
        ] + [PositiveAIBenchmarkParameters(alpha=0.60, eta=0.50, omega_x=0.20)]
        for p in configurations:
            with self.subTest(parameters=p):
                s = balanced_growth_seed(p)
                beta = (1 - p.alpha) * p.omega_x
                lam = (1 - p.alpha) * (1 - p.omega_x)
                delta_feedback = (1 - p.alpha) * (1 - p.eta - p.omega_x)
                gy = ((1 - p.eta) * (1 - p.omega_x)
                      / (1 - p.eta - p.omega_x)
                      * (p.population_growth + p.labor_productivity_growth))
                gb = p.eta * gy / (1 - p.eta)
                premium = (p.eta * p.omega_x
                           / (1 - p.eta - p.omega_x)
                           * (p.population_growth + p.labor_productivity_growth))
                self.assertAlmostEqual(gy, s.output_growth, places=13)
                self.assertAlmostEqual(gb, s.capability_growth, places=13)
                self.assertAlmostEqual(
                    gy - p.population_growth,
                    p.labor_productivity_growth + premium, places=13,
                )
                k = p.alpha / (p.discount + gy - p.population_growth + p.depreciation)
                u = beta**2
                m = u * p.eta * gb / (p.discount - p.population_growth + p.eta * gy)
                c = 1 - u - m - (gy + p.depreciation) * k
                b0 = (p.initial_labor_productivity * p.initial_population
                      * k**(p.alpha / lam) * u**(beta / lam)
                      * m * (p.chi / gb)**(1 / p.eta))**(p.eta * lam / delta_feedback)
                y0 = (p.initial_labor_productivity * p.initial_population
                      * k**(p.alpha / lam) * (u * b0)**(beta / lam))
                np.testing.assert_allclose(
                    [b0, y0, k*y0, c*y0, m*y0/(p.eta*gb*b0)],
                    [s.capability, s.output, s.capital, s.consumption, s.shadow_value],
                    rtol=5e-12, atol=0,
                )
                audit = canonical_seed_residuals(p, s)
                self.assertLess(audit["max_abs_equilibrium_residual"], 5e-12)
                self.assertGreater(c, 0)
                self.assertGreater(audit["tvc_decay_rate"], 0)
                for t in (0.0, 25.0, 200.0):
                    # Evaluate equations at finite dates rather than merely
                    # comparing their date-zero levels.
                    B = b0 * np.exp(gb*t)
                    Y = y0 * np.exp(gy*t)
                    K, C, U, M = k*Y, c*Y, u*Y, m*Y
                    N = p.initial_population * np.exp(p.population_growth*t)
                    A = p.initial_labor_productivity * np.exp(p.labor_productivity_growth*t)
                    X = B*U
                    q = M/(p.eta*gb*B)
                    w = lam*Y/N
                    px = beta*Y/X
                    r = p.alpha*Y/K-p.depreciation
                    profit = px*X-U-M
                    np.testing.assert_allclose(
                        [Y, gb*B, gy*K, gy*C, (gy-gb)*q, gy*K],
                        [K**p.alpha * (A*N)**lam * X**beta,
                         p.chi*(B*M)**p.eta,
                         Y-C-U-M-p.depreciation*K,
                         (p.population_growth+r-p.discount)*C,
                         r*q-X/B**2-p.eta*gb*q,
                         r*K+w*N+profit-C],
                        rtol=5e-11, atol=5e-13,
                    )

    def test_both_tvc_rates_and_objectives_are_finite(self):
        p = PositiveAIBenchmarkParameters(chi=1.4378)
        s = balanced_growth_seed(p)
        a = p.discount - p.population_growth
        self.assertAlmostEqual(s.output_growth - s.net_interest_rate, -a)
        self.assertAlmostEqual(
            s.shadow_value_growth + s.capability_growth - s.net_interest_rate, -a,
        )
        household_value = p.initial_population * (
            np.log(s.consumption / p.initial_population)/a
            + (s.output_growth-p.population_growth)/a**2
        )
        developer_value = s.distributed_profit/a
        self.assertTrue(np.isfinite(household_value))
        self.assertTrue(np.isfinite(developer_value))
        # Integrated household budget, including labor income and profits.
        np.testing.assert_allclose(
            s.consumption/a,
            s.capital + (s.wage*s.population+s.distributed_profit)/a,
            rtol=1e-13,
        )

    def test_paper_jacobian_and_main_calibration_projection(self):
        for chi in (0.01, 1.4378):
            p = PositiveAIBenchmarkParameters(chi=chi)
            s = balanced_growth_seed(p)
            eK, eB, eC, eq = np.eye(4)
            y = np.array([p.alpha/(1-s.beta), s.beta/(1-s.beta), 0, 0])
            m = (p.eta*eB+eq)/(1-p.eta)
            b = s.capability_growth*((p.eta-1)*eB+p.eta*m)
            k = s.capital_output_ratio
            gross = s.net_interest_rate+p.depreciation
            paper_jacobian = np.vstack([
                (1-s.inference_share)/k*y-(s.output_growth+p.depreciation)*eK
                -s.consumption_share/k*eC-s.research_share/k*m,
                b,
                gross*(y-eK),
                gross*(y-eK)-(p.discount-p.population_growth+p.eta*s.output_growth)
                *(y-eq-eB)-p.eta*b,
            ])
            np.testing.assert_allclose(
                paper_jacobian, normalized_jacobian(np.zeros(4), p, s), atol=1e-14,
            )
            subspace = stable_subspace(p, s)
            self.assertEqual(np.count_nonzero(subspace.eigenvalues.real < 0), 2)
            self.assertEqual(np.count_nonzero(subspace.eigenvalues.real > 0), 2)
            np.testing.assert_allclose(
                np.sort(subspace.eigenvalues.real),
                [-0.098971, -0.003194, 0.040391, 0.149290], atol=5e-7, rtol=0,
            )
            # The manuscript reports unit eigenvectors, whereas stable_subspace
            # uses an orthonormal basis. Their determinants need not coincide.
            roots, vectors = np.linalg.eig(paper_jacobian)
            unit_basis = vectors[:, roots.real < 0].real
            self.assertAlmostEqual(abs(np.linalg.det(unit_basis[:2])), 0.6037, places=4)
            self.assertGreater(abs(subspace.state_projection_determinant), 0.60)

    def test_main_bgp_uses_unstarred_notation_with_appendix_mapping(self):
        body = (ROOT / "sections_rewrite/05_uncapped_equilibria.tex").read_text(encoding="utf-8")
        section = body.split(r"\label{subsec:rewrite-uncapped-unit-bgp}", 1)[1].split(
            r"\subsection{", 1
        )[0]
        self.assertNotRegex(section, r"\^\s*(?:\*|\{\s*\*\s*\})")
        self.assertNotIn("A superscript", section)
        for expression in (
            r"$K_0,B_0>0$", r"g_{Y/N}=g_w&=g_Y-n",
            r"r&=\rho+g_Y-n", r"g_B&=",
        ):
            self.assertIn(expression, section)
        appendix = (ROOT / "sections_rewrite/appendix_uncapped_unit.tex").read_text(encoding="utf-8")
        self.assertIn("a superscript $*$ denotes the reference", appendix)
        self.assertIn(r"\xi_K=\log\frac K{K^*}", appendix)

    def test_source_scope_numbering_and_single_proof_section(self):
        appendix = (ROOT / "sections_rewrite/appendix_uncapped_unit.tex").read_text(encoding="utf-8")
        proofs = (ROOT / "sections_rewrite/appendix_uncapped_unit_proofs.tex").read_text(encoding="utf-8")
        main = (ROOT / "main_rewrite.tex").read_text(encoding="utf-8")
        existing = (ROOT / "sections_rewrite/appendix.tex").read_text(encoding="utf-8")
        body = (ROOT / "sections_rewrite/05_uncapped_equilibria.tex").read_text(encoding="utf-8")
        self.assertIn(r"\input{sections_rewrite/appendix_uncapped_unit}", main)
        self.assertLess(existing.index(r"\input{sections_rewrite/appendix_uncapped_unit_proofs}"),
                        existing.index(r"\section{Numerical algorithm"))
        self.assertNotRegex(proofs, r"\\(?:sub)*section\{")
        self.assertEqual(appendix.count(r"\begin{proposition}"), 1)
        for suffix in ("bgp", "local"):
            label = "prop:rewrite-uncapped-unit-" + suffix
            location = body if suffix == "bgp" else appendix
            other = appendix if suffix == "bgp" else body
            self.assertIn(r"\label{" + label + "}", location)
            self.assertNotIn(r"\label{" + label + "}", other)
            self.assertIn(r"\begin{proof}[Proof of Proposition~\ref{" + label + "}]", proofs)
        self.assertNotRegex(appendix + proofs, r"\\gamma_A|\\sigma_\{XL\}|\\omega_H|\\sigma_\{HM\}")
        self.assertIn("not every possible equilibrium", appendix)
        self.assertIn("local in initial stocks, not in time", appendix)
        self.assertIn("does not extend to the uncapped economy", appendix)
        for suffix in ("household-tvc", "developer-tvc", "developer-verification"):
            self.assertIn(r"\label{eq:rewrite-uncapped-unit-" + suffix + "}", proofs)


if __name__ == "__main__":
    unittest.main()

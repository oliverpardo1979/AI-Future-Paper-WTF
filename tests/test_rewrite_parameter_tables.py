"""Check displayed parameter tables against saved simulations; never run a BVP."""
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
SECTION=ROOT/'sections_rewrite'
SHARED=(SECTION/'parameter_tables.tex').read_text(encoding='utf-8')
COMMON,MAIN=SHARED.split(r'\newcommand{\rewriteMainParameterRows}',1)
SOURCES=[SECTION/p for p in ('05_quantitative_equilibria.tex',
                            '06_price_calibration.tex','07_low_ai_price_calibration.tex')]
TEXT='\n'.join(p.read_text(encoding='utf-8') for p in SOURCES)
TABLES={label:body for label,body in re.findall(
    r'\\begin\{rewriteParameterTable\}\{[^\n]*?\}\{([^}]+)\}(.*?)'
    r'\\end\{rewriteParameterTable\}',TEXT,re.S)}
SCENARIOS={
    'tab:rewrite-parameters':'',
    'tab:rewrite-method-parameters':'',
    'tab:rewrite-distribution-parameters':'',
    'tab:rewrite-ramsey-parameters':'ramsey_start',
    'tab:rewrite-price-parameters':'price_calibrated',
    'tab:rewrite-low-ai-price-parameters':'price_calibrated_low_ai_high_cap',
    'tab:rewrite-near-terminal-parameters':'near_terminal',
    'tab:rewrite-slow-parameters':'slow_transition',
}


def rows(body):
    expanded=COMMON+'\n'+body.replace(r'\rewriteMainParameterRows',MAIN)
    return dict(re.findall(r'^\$([^$]+)\$ & (.*?) &',expanded,re.M))


def number(segment):
    text=segment.replace('{','').replace('}','').replace(',','').lstrip('$ ')
    token=re.match(r'\d+(?:\.\d+)?',text).group()
    decimals=len(token.split('.')[1]) if '.' in token else 0
    return float(token),.5*10**(-decimals)


class ParameterTables(unittest.TestCase):
    def check_display(self,segment,actual):
        displayed,tolerance=number(segment)
        self.assertLessEqual(abs(displayed-actual),tolerance+1e-10,
                             f'{segment} does not round {actual}')

    def test_every_quantitative_subsection_has_a_table(self):
        self.assertEqual(TEXT.count(r'\subsection{'),9)
        self.assertEqual(len(TABLES),9)
        self.assertIn('tab:rewrite-financing-parameters',TABLES)
        for label in TABLES:
            self.assertIn(r'\ref{'+label+'}',TEXT)

    def test_parameters_and_initial_stocks_match_saved_runs(self):
        mapping={r'\alpha':'alpha',r'\delta':'depreciation',r'\rho':'discount',
                 'n':'population_growth',r'\gamma':'labor_productivity_growth',
                 r'\eta':'eta',r'\omega_X':'omega_x',r'\chi':'chi'}
        for label,directory in SCENARIOS.items():
            data=rows(TABLES[label])
            for index,sigma in enumerate((.9,1.,1.1,1.5)):
                with self.subTest(table=label,sigma=sigma):
                    file=ROOT/'numerical_rewrite'/directory/('sigma_'+f'{sigma:.2f}'.replace('.','_')+'_audit.json')
                    audit=json.loads(file.read_text(encoding='utf-8'))
                    self.assertTrue(audit['equilibrium_certified'])
                    p=audit['parameters']
                    for symbol,field in mapping.items():
                        self.check_display(data[symbol],p[field])
                    self.check_display(data[r'\omega_L'],1-p['omega_x'])
                    self.check_display(data[r'\sigma'].split(';')[index],sigma)
                    self.check_display(data[r'\overline B'],audit['frontier'])
                    self.check_display(data['A_0,N_0'].split(';')[0],p['initial_labor_productivity'])
                    self.check_display(data['A_0,N_0'].split(';')[1],p['initial_population'])
                    capital=data['K_0'].split(r';\newline ')[index] if directory=='near_terminal' else data['K_0']
                    self.check_display(capital,audit['initial_capital'])
                    self.check_display(data['B_0'],audit['initial_capability'])

    def test_financing_comparison_uses_its_own_calibration(self):
        data=rows(TABLES['tab:rewrite-financing-parameters'])
        main=json.loads((ROOT/'numerical_rewrite/sigma_1_50_audit.json').read_text())
        distant=json.loads((ROOT/'numerical_rewrite/initial_financing_sensitivity.json').read_text())
        for j,audit in enumerate((main,distant)):
            self.check_display(data[r'\chi'].split(r';\newline ')[j],audit['parameters']['chi'])
            self.check_display(data['K_0'].split(r';\newline ')[j],audit['initial_capital'])
            self.check_display(data['B_0'].split(r';\newline ')[j],audit['initial_capability'])
            self.check_display(data[r'\overline B'],audit['frontier'])
        self.assertIn('arbitrary 50-year',TABLES['tab:rewrite-financing-parameters'])

    def test_sources_do_not_disguise_assumptions_as_estimates(self):
        self.assertIn('Arbitrary trend assumption',COMMON)
        self.assertIn('Arbitrary illustrative value',COMMON)
        self.assertIn('not supplied as inputs',COMMON)
        self.assertIn(r'\citep{unwpp2024}',COMMON)
        self.assertIn(r'\citep{oecdlongrun2025}',COMMON)
        self.assertIn(r'\citep{pwt110}',COMMON)
        for label in ('tab:rewrite-price-parameters','tab:rewrite-low-ai-price-parameters'):
            self.assertIn(r'\citep{oecdaimarkets2026}',TABLES[label])
            self.assertIn('0.20',TABLES[label])


if __name__=='__main__':
    unittest.main()

"""Render the two agreed six-panel figures from admitted equilibrium data."""
import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.python-packages'))
sys.path.insert(0,str(ROOT/'scripts'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, MaxNLocator, FuncFormatter
from simulate_rewrite_finite_frontier import SIGMAS, OUT, CACHE, key

PANELS_1=(
 ('output_effective_labor', 'A. Output\n$Y/(AL)$', 'log'),
 ('output_per_person_growth', 'B. Growth per person\n$g_Y-n$', 'rate'),
 ('wage_productivity', 'C. Wage / productivity\n$w/A$', 'log'),
 ('net_interest', 'D. Net interest rate\n$r$', 'rate'),
 ('labor_income_share', 'E. Labor income share\n$wL/Y$', 'share'),
 ('ai_revenue_output_share', 'F. AI-industry revenue\n$p_X X/Y$', 'share'),
)
PANELS_2=(
 ('capability_frontier_ratio', 'A. Capability / frontier\n$B/\\bar{B}$', 'fraction'),
 ('consumption_effective_labor', 'B. Consumption\n$C/(AL)$', 'log'),
 ('capital_effective_labor', 'C. Capital\n$K/(AL)$', 'log'),
 ('inference_revenue_share', 'D. Inference / AI revenue\n$U/(p_X X)$', 'share'),
 ('research_revenue_share', 'E. Research / AI revenue\n$M/(p_X X)$', 'share'),
 ('profit_revenue_share', 'F. Profit / AI revenue\n$\\Pi/(p_X X)$', 'share'),
)
STYLES={.9:('#677748',(0,(5,2))),1.:('#414141','-'),
        1.1:('#bd8620',(0,(1,1.8))),1.5:('#24618c',(0,(5,1.8,1,1.8)))}


def render():
    reports={s:json.loads((OUT/f'{key(s)}_audit.json').read_text()) for s in SIGMAS}
    provenance=json.loads((OUT/'paths_manifest.json').read_text())
    if hashlib.sha256((OUT/'equilibrium_paths.csv').read_bytes()).hexdigest()!=provenance['csv_sha256']:
        raise ValueError('The plotted data have changed since their audited export.')
    for s,r in reports.items():
        if not r['equilibrium_certified']:
            raise ValueError(f'sigma={s} is not admitted; refuse a partial comparison.')
        if hashlib.sha256((CACHE/r['checkpoint_filename']).read_bytes()).hexdigest()!=r['checkpoint_sha256']:
            raise ValueError('An audited checkpoint has changed.')
        if provenance['checkpoint_sha256'][key(s)]!=r['checkpoint_sha256']:
            raise ValueError('The CSV and current audit refer to different checkpoints.')
    rows=list(csv.DictReader((OUT/'equilibrium_paths.csv').open(encoding='utf-8')))
    data={s:[{k:float(v) for k,v in r.items()} for r in rows if float(r['sigma'])==s] for s in SIGMAS}
    if any(not v for v in data.values()):
        raise ValueError('The CSV omits a requested scenario.')
    figdir=ROOT/'figures_rewrite'
    figdir.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Serif','font.size':9,
                         'axes.titlesize':9,'axes.labelsize':9,
                         'xtick.labelsize':8,'ytick.labelsize':8,
                         'legend.fontsize':9,'pdf.fonttype':42})
    for filename, panels in (('equilibrium_growth_distribution',PANELS_1),
                             ('equilibrium_technology_revenue',PANELS_2)):
        fig,axes=plt.subplots(2,3,figsize=(7,5.85),sharex=True)
        for axis,(field,title,scale) in zip(axes.flat,panels):
            for sigma in SIGMAS:
                series=data[sigma]
                values=np.array([r[field] for r in series])
                if not np.all(np.isfinite(values)) or (scale=='log' and np.any(values<=0)):
                    raise ValueError(f'Invalid plotted values in {field}, sigma={sigma}.')
                color,linestyle=STYLES[sigma]
                axis.plot([r['time'] for r in series],values,color=color,linestyle=linestyle,
                          linewidth=1.5,label=fr'$\sigma={sigma:.2f}$')
            # An explicit title coordinate prevents Matplotlib from moving the
            # top-row titles into the shared legend when log-axis offset text
            # differs across panels.
            axis.set_title(title,loc='left',pad=7,y=1.02)
            if scale=='log':
                axis.set_yscale('log')
            elif scale in ('rate','share'):
                decimals = 1 if scale=='rate' or field=='research_revenue_share' else 0
                axis.yaxis.set_major_formatter(PercentFormatter(1,decimals=decimals))
                axis.yaxis.set_major_locator(MaxNLocator(5))
            if scale=='fraction':
                axis.set_ylim(0,1.02)
                axis.set_yticks([0,.5,1])
            if scale=='share':
                lower,upper=axis.get_ylim()
                axis.set_ylim(min(0,lower),upper)
            if field=='profit_revenue_share':
                axis.axhline(0,color='#999999',linewidth=.6,zorder=0)
            axis.set_xlim(0,data[1.][-1]['time'])
            axis.set_xticks([0,2000,4000])
            axis.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:,.0f}'))
            axis.grid(axis='y',which='major',color='#dddddd',linewidth=.5)
            axis.spines[['top','right']].set_visible(False)
            axis.spines[['left','bottom']].set_color('#888888')
            axis.tick_params(length=3,color='#888888')
        for axis in axes[-1,:]:
            axis.set_xlabel('Years')
        handles,labels=axes.flat[0].get_legend_handles_labels()
        fig.legend(handles,labels,ncol=4,loc='upper center',frameon=False,
                   bbox_to_anchor=(.5,.995),handlelength=2.6,columnspacing=1.6)
        fig.subplots_adjust(left=.095,right=.970,bottom=.10,top=.82,hspace=.46,wspace=.48)
        fig.savefig(figdir/f'{filename}.pdf',metadata={'Title':filename})
        fig.savefig(figdir/f'{filename}.png',dpi=190)
        plt.close(fig)
    manifest=dict(data_sha256=hashlib.sha256((OUT/'equilibrium_paths.csv').read_bytes()).hexdigest(),
                  sigmas=list(SIGMAS),horizon=data[1.][-1]['time'],
                  panels={'figure_1':[p[0] for p in PANELS_1], 'figure_2':[p[0] for p in PANELS_2]},
                  all_scenarios_admitted=True)
    (OUT/'figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':
    render()

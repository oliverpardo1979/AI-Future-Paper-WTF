"""Reproducible title screen of Crossref's top-five journal metadata.

Discovery only: relevance and publication status require original-source review.
No manuscript or bibliography is modified. Cached responses make reruns cheap.
"""
import concurrent.futures
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit' / 'jones_top5_2026-09-16'
CACHE = ROOT / 'tmp' / 'top5_crossref_2026-09-16'
JOURNALS = {
    'American Economic Review': '0002-8282',
    'Quarterly Journal of Economics': '0033-5533',
    'Journal of Political Economy': '0022-3808',
    'Econometrica': '0012-9682',
    'Review of Economic Studies': '0034-6527',
}
PATTERN = re.compile(r'artificial intelligence|\bAI\b|automat|robot|algorithm|machine learning|generative|technolog|innovation|economic growth|labor share|labour share|tasks|knowledge|new work|machines|job loss', re.I)


def retrieve(pair):
    name, issn = pair
    CACHE.mkdir(parents=True, exist_ok=True)
    target = CACHE / (issn + '.json')
    url = 'https://api.crossref.org/journals/' + issn + '/works?' + urllib.parse.urlencode({
        'filter': 'from-pub-date:2022-01-01,until-pub-date:2026-09-16,type:journal-article',
        'rows': 1000,
        'select': 'DOI,title,author,published,published-online,published-print,container-title,volume,issue,page,URL',
    })
    try:
        if target.exists():
            payload = json.loads(target.read_text(encoding='utf-8'))
        else:
            req = urllib.request.Request(url, headers={'User-Agent': 'AcademicBibliographyAudit/1.0'})
            with urllib.request.urlopen(req, timeout=55) as response:
                payload = json.load(response)
            target.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
        msg = payload['message']
        rows = msg['items']
        selected = [r for r in rows if PATTERN.search(' '.join(r.get('title', [])))]
        return {'journal': name, 'issn': issn, 'query_url': url, 'total_results': msg['total-results'],
                'retrieved': len(rows), 'complete_response': len(rows) == msg['total-results'],
                'candidates': selected}
    except Exception as exc:
        return {'journal': name, 'issn': issn, 'query_url': url, 'error': str(exc), 'candidates': []}


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        results = list(pool.map(retrieve, JOURNALS.items()))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'crossref_screen.json').write_text(json.dumps({
        'review_date': '2026-09-16', 'start_date': '2022-01-01',
        'scope': 'Title screening, not a claim of exhaustive full-text coverage. Publisher publication dates govern final inclusion.',
        'journals': results,
    }, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    for result in results:
        print(result['journal'], result.get('retrieved'), '/', result.get('total_results'), result.get('error', ''))
        for row in result['candidates']:
            print(' | '.join([str(row.get('published', {}).get('date-parts', [])), row['DOI'], ' '.join(row.get('title', []))]))

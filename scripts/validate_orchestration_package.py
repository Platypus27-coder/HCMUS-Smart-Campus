"""Check subspace 06 artifacts. Does not evaluate live Wesome behavior."""
import json
from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'subspaces/06-central-orchestration'


def validate():
    errors = []
    directory = yaml.safe_load((ROOT / 'shared/agent-directory.yaml').read_text(encoding='utf-8'))['agents']
    agents = {a['id'] for a in directory}
    specialists = agents - {'campus-router-agent', 'campus-aggregator-agent'}
    deprecated = ('Teaching Material Assistant', 'Research Assistant', 'Class Support Agent',
                  'teaching-material-assistant', 'research-assistant-agent', 'class-support-agent')
    for aid in ('campus-router-agent', 'campus-aggregator-agent'):
        folder = BASE / aid
        for name in ('info.docx', 'agent/knowledge.docx', 'agent/QA.xlsx', 'agent/background.png',
                     'info.md', 'agent/knowledge.md', 'agent/knowledge-upload.md', 'system-prompt.md', 'space/welcome.md'):
            p = folder / name
            if not p.is_file() or p.stat().st_size == 0:
                errors.append(f'Missing or empty {p.relative_to(ROOT)}')
        for name in ('info.docx', 'agent/knowledge.docx', 'agent/QA.xlsx'):
            p = folder / name
            try:
                with zipfile.ZipFile(p) as z:
                    if z.testzip():
                        errors.append(f'Corrupt ZIP: {p}')
                    for entry in z.namelist():
                        if entry.endswith('.xml'):
                            ET.fromstring(z.read(entry))
            except (OSError, zipfile.BadZipFile, ET.ParseError) as exc:
                errors.append(f'Invalid Office file {p.name}: {exc}')
        qa = json.loads((folder / 'agent/qa.json').read_text(encoding='utf-8'))
        if len({r['question'] for r in qa}) != len(qa):
            errors.append(f'Duplicate questions: {aid}')
        if not all(r['question'].strip() and r['answer'].strip() for r in qa):
            errors.append(f'Empty QA: {aid}')
        with zipfile.ZipFile(folder / 'agent/QA.xlsx') as z:
            ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
            rows = ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//s:row', ns)
            values = [[ ''.join(c.itertext()) for c in row.findall('s:c',ns)] for row in rows]
            expected = [['Question','Answer','Display as Suggested Question?\nyes/no']] + [[r['question'],r['answer'],'yes' if r.get('suggested') else 'no'] for r in qa]
            if values != expected:
                errors.append(f'Excel and QA source differ: {aid}')
        for path in [folder/'info.md',folder/'agent/knowledge.md',folder/'system-prompt.md',folder/'agent/qa.json']:
            text = path.read_text(encoding='utf-8')
            for old in deprecated:
                if old in text:
                    errors.append(f'Deprecated agent {old}: {path.name}')
            if re.search(r'[A-Za-z]:[\\/]|file:///', text):
                errors.append(f'Absolute local path: {path.name}')
        config = json.loads((folder/'space/space_config.json').read_text(encoding='utf-8'))
        for rel in [config['background']] + config['menu_resources']['files'] + config['menu_resources']['guides']:
            if not (folder/rel).is_file():
                errors.append(f'Missing resource {aid}/{rel}')
    cases = json.loads((BASE/'evaluation/cases.json').read_text(encoding='utf-8'))
    if len({c['id'] for c in cases}) != len(cases):
        errors.append('Duplicate evaluation case IDs')
    covered = set()
    for c in cases:
        covered.update(c['targets'])
        if c['agent'] not in agents or set(c['targets']) - agents:
            errors.append(f'Unknown agent in case {c["id"]}')
    if not specialists <= covered:
        errors.append(f'Missing specialist coverage: {specialists-covered}')
    links = json.loads((BASE/'deployment/agent-links.json').read_text(encoding='utf-8'))['agents']
    if {a['id'] for a in links} != agents or len(links) != len(agents):
        errors.append('Deployment manifest does not match canonical directory')
    fixture = json.loads((BASE/'evaluation/partial-responses.example.json').read_text(encoding='utf-8'))
    required = {'response_version','agent','status','result','sources','assumptions','missing_information','limitations'}
    for response in fixture['specialist_responses']:
        if not required <= response.keys() or response['agent'] not in specialists:
            errors.append('Invalid demo response envelope')
        if response['status'] not in {'success','partial','needs_user_input','unsupported','error'}:
            errors.append('Invalid response status')
    bundle = BASE/'deployment/subspace-06-upload.zip'
    try:
        with zipfile.ZipFile(bundle) as z:
            for name in z.namelist():
                if 'archive/' in name or re.search(r'knowledge\d+\.docx', name):
                    errors.append(f'Legacy file in upload bundle: {name}')
                source = BASE/name
                if not source.is_file() or z.read(name) != source.read_bytes():
                    errors.append(f'Bundle differs from source: {name}')
    except (OSError, zipfile.BadZipFile) as exc:
        errors.append(f'Invalid upload bundle: {exc}')
    return errors


if __name__ == '__main__':
    problems = validate()
    for problem in problems:
        print('[ERROR]', problem)
    if not problems:
        print('[OK] Office structure, Q&A parity, resources, agent IDs, 15-specialist coverage and demo envelopes')
        print('[NOTICE] Live behavior cases remain NOT_RUN until tested on the deployment platform.')
    raise SystemExit(bool(problems))

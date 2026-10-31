"""Repository/schema/provenance checks. No scientific evidence upgrades."""
from __future__ import annotations
from pathlib import Path
import ast,hashlib,json,re
import jsonschema


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dependencies_acyclic(claims: list[dict]) -> bool:
    graph={c['id']:c['dependencies'] for c in claims}
    done=set();active=set()
    def visit(node):
        if node not in graph or node in active:return False
        if node in done:return True
        active.add(node)
        if not all(visit(child) for child in graph[node]):return False
        active.remove(node);done.add(node);return True
    return all(visit(node) for node in graph)


def validate_repository(root: Path) -> list[dict]:
    root=root.resolve();checks=[]
    def check(name,ok,scope):
        checks.append({'name':name,'passed':bool(ok),'scope':scope})
    claims=json.loads((root/'LEDGER/CLAIMS.json').read_text())
    schema=json.loads((root/'LEDGER/claims.schema.json').read_text())
    errors=list(jsonschema.Draft202012Validator(schema).iter_errors(claims))
    check('claims_schema',not errors,'JSON structure, not physical truth')
    constants=json.loads((root/'CANONICAL/constants.json').read_text())
    cschema=json.loads((root/'CANONICAL/constants.schema.json').read_text())
    check('constants_schema',not list(jsonschema.Draft202012Validator(cschema).iter_errors(constants)),'JSON structure')
    ids=[c['id'] for c in claims['claims']]
    check('unique_claim_ids',len(ids)==len(set(ids)),'curated ledger only')
    check('claim_dependency_closure',all(set(c['dependencies'])<=set(ids) for c in claims['claims']),'declared claim graph')
    check('claim_graph_acyclic',dependencies_acyclic(claims['claims']),'declared dependency graph; not scientific independence')
    check('claim_count_matches',len(ids)==claims['metadata']['total_claims'],'document state')
    check('no_invented_pi_approval',claims['metadata']['new_pi_approval'] is None,'document state')
    main=(root/'manuscript/RAP_v4_0.tex').read_text()
    old=(root/'provenance/input/RAP_v4_0_previous_working.tex').read_text()
    snapshot=json.loads((root/'provenance/source-snapshot.json').read_text())
    check('corrected_input_hash',sha256(root/'provenance/input/RAP_v4_0_previous_working.tex')==snapshot['manuscript_corrected_input_sha256'],'provided predecessor identity')
    a=old.index('\\begin{thebibliography}');b=old.index('\\end{thebibliography}')+len('\\end{thebibliography}')
    c=main.index('% Bibliography externalized');d=main.index('\\bibliography{references}')+len('\\bibliography{references}')
    check('manuscript_body_unchanged',old[:a]==main[:c] and old[b:]==main[d:],'only bibliography externalization; no changed physics or PI boxes')
    check('claim_source_anchors',all('\\label{'+c['source']['anchor']+'}' in main for c in claims['claims']),'source links exist')
    # This is a syntactic guard, not a proof of target-independent research history.
    solver=(root/'rap/structural.py').read_text();tree=ast.parse(solver)
    imports=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):imports.extend(a.name for a in node.names)
        if isinstance(node,ast.ImportFrom):imports.append(node.module or '')
    check('structural_import_allowlist',set(imports)<= {'__future__','dataclasses','fractions','math','typing'},'source-level import boundary only')
    forbidden=('16.339','16339','1.710','2.44','47.7','49/3')
    check('no_calibrated_target_literals_in_solver',not any(t in solver for t in forbidden),'literal scan; not a full target-shape audit')
    check('no_named_partition_branch',not re.search(r'\bn\s*==\s*(6|7|15)\b',solver),'source scan only')
    numeric_tree=ast.parse((root/'rap/numerics.py').read_text())
    assigned=[]
    for node in ast.walk(numeric_tree):
        targets=node.targets if isinstance(node,ast.Assign) else [node.target] if isinstance(node,(ast.AugAssign,ast.AnnAssign,ast.NamedExpr)) else []
        assigned.extend(ast.unparse(t) for t in targets)
    check('no_shared_precision_assignment',not (set(assigned)&{'mp.dps','mp.prec','mpmath.mp.dps','mpmath.mp.prec'}),'AST assignment guard and independent-context runtime checks')
    base='10.5281/zenodo.22731224'
    metadata=json.loads((root/'.zenodo.json').read_text())
    check('no_new_doi_fabricated','doi' not in metadata,'base DOI retained only as prior record')
    check('no_publication_date_fabricated','publication_date' not in metadata,'actual date must be confirmed')
    check('base_doi_relationship',any(r.get('identifier')==base and r.get('relation')=='isDerivedFrom' for r in metadata['related_identifiers']),'textual provenance, not physics')
    # All cited keys are covered; bibliography membership is checked separately from full-text support.
    citepattern=r'\\cite(?:p|t|alp|author|year)?\*?(?:\[[^\]]*\])*\{([^}]+)\}'
    used={k.strip() for g in re.findall(citepattern,main) for k in g.split(',')}
    bib=(root/'manuscript/references.bib').read_text()
    bibkeys=re.findall(r'(?m)^@\w+\{([^,]+),',bib)
    check('manuscript_citation_keys_covered',used<=set(bibkeys),'citation membership, not claim support')
    check('manuscript_bib_unique',len(bibkeys)==len(set(bibkeys)),'bibliography integrity')
    check('supplementary_bib_not_silently_imported',len(bibkeys)==124 and len(re.findall(r'(?m)^@\w+\{([^,]+),',(root/'references.bib').read_text()))==131,'124 manuscript records; seven supplements remain separate')
    hist=json.loads((root/'governance/RECORDED_PI_DECISIONS.json').read_text())
    ok=True
    for item in hist['decisions']:
        ok &= (item['verbatim_tex'] in main and hashlib.sha256(item['verbatim_tex'].encode()).hexdigest()==item['sha256'])
    check('historical_pi_boxes_verbatim',ok and {x['id'] for x in hist['decisions']}=={'D'+str(i) for i in range(19,26)},'record preservation; not a new approval')
    notes=[x for x in (root/'docs/research').glob('*.md') if x.name!='INDEX.md']
    index=(root/'docs/research/INDEX.md').read_text()
    check('research_index_complete',all('('+x.name+')' in index for x in notes),'actual bundled notes, not inherited count 47')
    for item in constants['constants']:
        u=item['uncertainty']
        check('constant_uncertainty_'+item['id'],(u['status']!='reported' or u['value'] is not None),'unknown uncertainty is never zero by default')
    # Basic static TeX structure; deliberately no claim of compilation.
    stripped=re.sub(r'\\begin\{verbatim\}.*?\\end\{verbatim\}','',main,flags=re.S)
    envs=[];valid=True
    for direction,name in re.findall(r'\\(begin|end)\{([^}]+)\}',stripped):
        if direction=='begin':envs.append(name)
        elif not envs or envs.pop()!=name:valid=False;break
    check('tex_environment_nesting',valid and not envs,'static source only; PDF build NOT_RUN')
    for f in root.rglob('*.py'):
        if '__pycache__' not in f.parts:
            try:ast.parse(f.read_text());ok=True
            except SyntaxError:ok=False
            check('python_syntax_'+str(f.relative_to(root)),ok,'parse, not execution')
    return checks

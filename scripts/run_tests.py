#!/usr/bin/env python3
"""Execute actual unittest cases and save their observed outcome."""
import io,json,sys,unittest
from datetime import datetime,timezone
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
stream=io.StringIO()
suite=unittest.defaultTestLoader.discover(str(root/'tests'),top_level_dir=str(root))
result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
log=stream.getvalue();print(log,end='')
out=root/'results';out.mkdir(exist_ok=True)
(out/'unit-tests.log').write_text(log,encoding='utf-8')
report={'run_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if result.wasSuccessful() else 'FAIL',
        'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
        'skipped':len(result.skipped),'scope':'new RAP regression tests; not independent physics or Lean verification'}
(out/'unit-tests.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
sys.exit(0 if result.wasSuccessful() else 1)

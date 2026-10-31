#!/usr/bin/env python3
"""Post-hoc reference arithmetic only. This file is not imported by the structural solver."""
from fractions import Fraction as F
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
items=json.loads((root/'CANONICAL/constants.json').read_text())['constants']
values={x['id']:x for x in items}
gamma=F(values['gamma_calibrated']['value'])
mc=F(values['gamma_mc']['value'])
spread=F(values['gamma_mc']['uncertainty']['value'])
ratio=(mc-gamma)/spread
print(json.dumps({'status':'ARITHMETIC_COMPLETED','physical_validation':False,
 'source':'CANONICAL/constants.json; adopted references, not solver inputs',
 'gamma_mc_difference':{'value_exact':str(mc-gamma),'unit':'dimensionless'},
 'spread_normalized_difference':{'value_exact':str(ratio),'approximate':str(float(ratio)),
   'certified_sigma':False,'reason':'uncertainty convention and covariance are not established'},
 'gamma_origin':'calibrated reference; no first-principles or colour-algebra derivation asserted',
 'delta':'reference only; no particle identification or Yang-Mills proof',
 'scope':'comparison arithmetic, not prediction or evidence-class upgrade'},indent=2))

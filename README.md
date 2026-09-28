# DELUXE AIR PRO SOLUTIONS — Stage 1

Florida HVAC load calculator prototype built with Streamlit.

## Run

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Scope and limitations

The displayed values are **preliminary whole-building estimates**, retained from
the original prototype. They are not a validated Manual J calculation, Manual S
equipment selection, duct design, or permit-ready report. The city temperatures,
75 °F indoor temperature, 30-grain humidity difference, 164 solar factor,
occupant loads and 25 BTU/h per ft² rule are unverified prototype assumptions.
Door conduction, orientation, room-by-room loads, mechanical ventilation,
manufacturer capacity tables, and duct pressure losses are not yet modeled.

The component sum is the primary preliminary result. The area-only rule remains
available separately for historical comparison. Nominal tons and the prototype
115% reference do not approve equipment.

## Reference results and tests

`tests/reference_results.json` records two results calculated with the original
`main/app.py` formulas before stage 1, including the original default inputs.
`legacy_estimate.py` holds those formulas without Streamlit so they can be
regression-tested. The defaults produce 21,009.77 BTU/h by components and
30,000 BTU/h by the separate area rule; that difference is why the UI labels
the two methods explicitly.

```bash
python -m unittest discover -s tests -v
python -m py_compile app.py legacy_estimate.py
```

Future stages will add validated room loads, equipment performance data, airflow
and duct design, then the complete English/Spanish product interface.

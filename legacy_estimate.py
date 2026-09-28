"""Frozen preliminary formulas from the original app.py (not a Manual J/S engine).

The constants and arithmetic are retained for stage 1 regression comparisons.
They are assumptions of the prototype, not validated design conditions.
"""

from dataclasses import dataclass


DESIGN_TEMPERATURES_F = {
    "Cape Coral": 94,
    "Fort Myers": 94,
    "Naples": 93,
    "Miami": 92,
    "Orlando": 93,
    "Tampa": 93,
}


@dataclass(frozen=True)
class EstimateInputs:
    city: str
    area: float
    height: float
    occupants: int
    gross_wall_area: float
    window_area: float
    door_area: float
    wall_r: float
    ceiling_area: float
    ceiling_r: float
    window_u: float
    window_shgc: float
    ach: float
    equipment_watts: float
    kitchen_laundry: bool


def calculate_preliminary(inputs: EstimateInputs) -> dict[str, float]:
    """Return the original component estimate and separate area rule of thumb."""
    if inputs.city not in DESIGN_TEMPERATURES_F:
        raise ValueError("Unsupported city")
    if inputs.wall_r <= 0 or inputs.ceiling_r <= 0:
        raise ValueError("R-values must be positive")
    if any(value < 0 for value in (
        inputs.area, inputs.height, inputs.occupants, inputs.gross_wall_area,
        inputs.window_area, inputs.door_area, inputs.ceiling_area,
        inputs.window_u, inputs.window_shgc, inputs.ach, inputs.equipment_watts,
    )):
        raise ValueError("Inputs cannot be negative")

    wall_area = max(inputs.gross_wall_area - inputs.window_area - inputs.door_area, 0)
    volume = inputs.area * inputs.height
    cfm = inputs.ach * volume / 60
    outdoor_temp = DESIGN_TEMPERATURES_F[inputs.city]
    indoor_temp = 75
    delta_t = outdoor_temp - indoor_temp
    wall_load = wall_area / inputs.wall_r * delta_t
    ceiling_load = inputs.ceiling_area / inputs.ceiling_r * delta_t
    window_conduction = inputs.window_u * inputs.window_area * delta_t
    window_solar = inputs.window_area * inputs.window_shgc * 164
    envelope_load = wall_load + ceiling_load + window_conduction + window_solar
    sensible_infiltration = 1.08 * cfm * delta_t
    latent_infiltration = 0.68 * cfm * 30
    people_sensible = inputs.occupants * 230
    people_latent = inputs.occupants * 200
    equipment_load = inputs.equipment_watts * 3.412
    kitchen_laundry_load = 1200 if inputs.kitchen_laundry else 0
    total_internal_load = people_sensible + people_latent + equipment_load + kitchen_laundry_load
    component_total = envelope_load + sensible_infiltration + latent_infiltration + total_internal_load
    area_rule_load = inputs.area * 25
    return {
        "net_wall_area": wall_area, "volume": volume, "cfm": cfm,
        "outdoor_temp": outdoor_temp, "indoor_temp": indoor_temp, "delta_t": delta_t,
        "wall_load": wall_load, "ceiling_load": ceiling_load,
        "window_conduction": window_conduction, "window_solar": window_solar,
        "envelope_load": envelope_load, "sensible_infiltration": sensible_infiltration,
        "latent_infiltration": latent_infiltration, "people_sensible": people_sensible,
        "people_latent": people_latent, "equipment_load": equipment_load,
        "kitchen_laundry_load": kitchen_laundry_load,
        "total_internal_load": total_internal_load,
        "component_total": component_total, "component_tons": component_total / 12000,
        "area_rule_load": area_rule_load, "area_rule_tons": area_rule_load / 12000,
    }

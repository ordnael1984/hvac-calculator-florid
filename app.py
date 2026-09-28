import streamlit as st
from legacy_estimate import EstimateInputs, calculate_preliminary

st.set_page_config(
    page_title="DELUXE AIR PRO SOLUTIONS",
    page_icon="❄️"
)

st.title("DELUXE AIR PRO SOLUTIONS")
st.subheader("Florida HVAC Load Calculator — Preliminary Estimate")
st.warning("Preliminary estimates only. This prototype is not a validated Manual J load calculation, Manual S equipment selection, or permit-ready report.")

st.header("Project Information")

project_name = st.text_input("Project Name")
customer_name = st.text_input("Customer Name")
address = st.text_input("Address")

city = st.selectbox("City", [
    "Cape Coral",
    "Fort Myers",
    "Naples",
    "Miami",
    "Orlando",
    "Tampa"
])

area = st.number_input("Area (ft²)", value=1200)
height = st.number_input("Ceiling Height (ft)", value=8.0)
occupants = st.number_input("Occupants", value=3)
st.header("Building Envelope")
st.subheader("Walls — Preliminary Component Estimate")

wall_method = st.selectbox(
    "Wall Area Method",
    [
        "Auto (Room Dimensions)",
        "Manual Input"
    ]
)

if wall_method == "Auto (Room Dimensions)":
    length = st.number_input("Room Length (ft)", value=40.0)
    width = st.number_input("Room Width (ft)", value=30.0)
    height_wall = st.number_input("Wall Height (ft)", value=8.0)

    gross_wall_area = 2 * (length + width) * height_wall

else:
    gross_wall_area = st.number_input("Gross Wall Area (ft²)", value=800.0)

window_area = st.number_input("Window Area (ft²)", value=150.0, key="window_area")
door_area = st.number_input("Exterior Door Area (ft²)", value=40.0)

wall_area = max(gross_wall_area - window_area - door_area, 0)

st.write(f"Net Wall Area: {wall_area:.1f} ft²")

wall_type = st.selectbox(
    "Wall Type",
    [
        "Block (no insulation)",
        "Block + insulation",
        "Wood Frame 2x4",
        "Wood Frame 2x6",
        "Custom"
    ]
)

if wall_type == "Block (no insulation)":
    wall_r = 4.5
elif wall_type == "Block + insulation":
    wall_r = 7.0
elif wall_type == "Wood Frame 2x4":
    wall_r = 13.0
elif wall_type == "Wood Frame 2x6":
    wall_r = 19.0
else:
    wall_r = st.number_input("Custom Wall R-Value", value=13.0)

ceiling_area = st.number_input("Ceiling/Roof Area (ft²)", value=1200)
ceiling_r = st.number_input("Ceiling/Roof R-Value", value=30.0)

window_u = st.number_input("Window U-Factor", value=0.35)
window_shgc = st.number_input("Window SHGC", value=0.25)
# --- AIR INFILTRATION ---

st.header("Infiltration / Ventilation")

ach = st.number_input("Air Changes per Hour (ACH)", value=0.5)
# --- INTERNAL LOADS ---

st.header("Internal Loads")

equipment_watts = st.number_input("Lighting / Equipment Watts", value=1000)
kitchen_laundry = st.checkbox("Add Kitchen / Laundry Load", value=True)

try:
    result = calculate_preliminary(EstimateInputs(
        city=city, area=area, height=height, occupants=occupants,
        gross_wall_area=gross_wall_area, window_area=window_area,
        door_area=door_area, wall_r=wall_r, ceiling_area=ceiling_area,
        ceiling_r=ceiling_r, window_u=window_u, window_shgc=window_shgc,
        ach=ach, equipment_watts=equipment_watts,
        kitchen_laundry=kitchen_laundry,
    ))
except ValueError as error:
    st.error(f"Please correct the inputs: {error}")
    st.stop()

if window_area + door_area > gross_wall_area:
    st.warning("Window and door area exceeds gross wall area; net wall area is capped at zero.")
st.write(f"Infiltration CFM: {result['cfm']:,.0f}")
st.caption("This prototype estimates infiltration only; mechanical ventilation is not calculated.")
st.header("Design Conditions — Prototype Assumptions")
st.write(f"Outdoor Design Temp: {result['outdoor_temp']} °F")
st.write(f"Indoor Design Temp: {result['indoor_temp']} °F")
st.write(f"ΔT: {result['delta_t']} °F")
st.write(f"Volume: {result['volume']} ft³")

st.header("Preliminary Component Loads")
for label, key in [
    ("Wall Load", "wall_load"),
    ("Ceiling/Roof Load", "ceiling_load"),
    ("Window Conduction Load", "window_conduction"),
    ("Window Solar Load", "window_solar"),
    ("Total Envelope Load", "envelope_load"),
    ("Sensible Infiltration Load", "sensible_infiltration"),
    ("Latent Infiltration Load", "latent_infiltration"),
    ("People Sensible Load", "people_sensible"),
    ("People Latent Load", "people_latent"),
    ("Lighting / Equipment Load", "equipment_load"),
    ("Kitchen / Laundry Load", "kitchen_laundry_load"),
    ("Total Internal Load", "total_internal_load"),
]:
    st.write(f"{label}: {result[key]:,.0f} BTU/h")

st.header("Preliminary Cooling Estimate — Component Sum")
st.write(f"Component Total: {result['component_total']:,.0f} BTU/h")
st.write(f"Equivalent Nominal Tons (arithmetic only): {result['component_tons']:.2f}")
st.info("This component sum is preliminary; missing envelope and design details can change it.")
with st.expander("Separate area rule of thumb — not an equipment recommendation"):
    st.write("Original prototype assumption: 25 BTU/h per ft².")
    st.write(f"Area-only estimate: {result['area_rule_load']:,.0f} BTU/h")
    st.write(f"Area-only equivalent: {result['area_rule_tons']:.2f} nominal tons")

st.header("Equipment Size — Preliminary Nominal Comparison")
selected_tons = st.number_input("Selected System Size (tons)", value=3.0)
selected_capacity = selected_tons * 12000
st.write(f"Nominal Selected Capacity: {selected_capacity:,.0f} BTU/h")
st.write(f"Prototype 115% Reference: {result['component_total'] * 1.15:,.0f} BTU/h")
if selected_capacity < result["component_total"]:
    st.warning("Nominal size is below the preliminary component estimate. Verify equipment data and loads.")
elif selected_capacity > result["component_total"] * 1.15:
    st.warning("Nominal size exceeds the prototype 115% reference. Verify equipment data and loads.")
else:
    st.info("Nominal size falls within the prototype comparison range; this is not equipment approval.")
st.caption("Actual total and sensible capacities at design conditions are required for equipment selection.")

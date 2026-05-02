import streamlit as st

st.set_page_config(
    page_title="Florida HVAC Load Calculator",
    page_icon="❄️"
)

st.title("HVAC Load Calculator - Florida")
st.subheader("Manual J / Manual S (Permit Style)")

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

wall_area = st.number_input("Wall Area (ft²)", value=800)
wall_r = st.number_input("Wall R-Value", value=13.0)

ceiling_area = st.number_input("Ceiling/Roof Area (ft²)", value=1200)
ceiling_r = st.number_input("Ceiling/Roof R-Value", value=30.0)

window_area = st.number_input("Window Area (ft²)", value=150)
window_u = st.number_input("Window U-Factor", value=0.35)
window_shgc = st.number_input("Window SHGC", value=0.25)
# --- AIR INFILTRATION ---

st.header("Infiltration / Ventilation")

ach = st.number_input("Air Changes per Hour (ACH)", value=0.5)
# --- INTERNAL LOADS ---

st.header("Internal Loads")

equipment_watts = st.number_input("Lighting / Equipment Watts", value=1000)
kitchen_laundry = st.checkbox("Add Kitchen / Laundry Load", value=True)

people_sensible = occupants * 230
people_latent = occupants * 200
equipment_load = equipment_watts * 3.412

kitchen_laundry_load = 1200 if kitchen_laundry else 0
volume = area * height
cfm = (ach * volume) / 60

st.write(f"Infiltration CFM: {cfm:,.0f}")
volume = area * height
# --- DESIGN CONDITIONS (Florida) ---

design_data = {
    "Cape Coral": 94,
    "Fort Myers": 94,
    "Naples": 93,
    "Miami": 92,
    "Orlando": 93,
    "Tampa": 93
}

outdoor_temp = design_data.get(city, 94)
indoor_temp = 75

delta_t = outdoor_temp - indoor_temp

st.header("Design Conditions")

st.write(f"Outdoor Design Temp: {outdoor_temp} °F")
st.write(f"Indoor Design Temp: {indoor_temp} °F")
st.write(f"ΔT: {delta_t} °F")

st.header("Results")

st.write(f"Volume: {volume} ft³")

st.success("Step 1 ready ✅")
# --- COOLING LOAD ESTIMATE ---

st.header("Cooling Load Estimate")
# --- MANUAL J COMPONENT LOADS ---

st.header("Manual J Component Loads")

wall_u = 1 / wall_r
ceiling_u = 1 / ceiling_r

wall_load = wall_u * wall_area * delta_t
ceiling_load = ceiling_u * ceiling_area * delta_t
window_conduction = window_u * window_area * delta_t

solar_factor = 164
window_solar = window_area * window_shgc * solar_factor

envelope_load = wall_load + ceiling_load + window_conduction + window_solar

st.write(f"Wall Load: {wall_load:,.0f} BTU/h")
st.write(f"Ceiling/Roof Load: {ceiling_load:,.0f} BTU/h")
st.write(f"Window Conduction Load: {window_conduction:,.0f} BTU/h")
st.write(f"Window Solar Load: {window_solar:,.0f} BTU/h")
st.write(f"Total Envelope Load: {envelope_load:,.0f} BTU/h")
btu_factor = 25
# --- INFILTRATION LOADS ---

sensible_infiltration = 1.08 * cfm * delta_t

# Diferencia de humedad típica Florida
delta_grains = 30

latent_infiltration = 0.68 * cfm * delta_grains

st.write(f"Sensible Infiltration Load: {sensible_infiltration:,.0f} BTU/h")
st.write(f"Latent Infiltration Load: {latent_infiltration:,.0f} BTU/h")

cooling_load = area * btu_factor
tons = cooling_load / 12000

st.write(f"Estimated Cooling Load: {cooling_load:,.0f} BTU/h")
st.write(f"Estimated Tons: {tons:.2f} tons")
# --- TOTAL LOAD (REAL) ---

total_load = envelope_load + sensible_infiltration + latent_infiltration
total_internal_load = people_sensible + people_latent + equipment_load + kitchen_laundry_load

total_load = (
    envelope_load
    + sensible_infiltration
    + latent_infiltration
    + total_internal_load
)
st.write(f"People Sensible Load: {people_sensible:,.0f} BTU/h")
st.write(f"People Latent Load: {people_latent:,.0f} BTU/h")
st.write(f"Lighting / Equipment Load: {equipment_load:,.0f} BTU/h")
st.write(f"Kitchen / Laundry Load: {kitchen_laundry_load:,.0f} BTU/h")
st.write(f"Total Internal Load: {total_internal_load:,.0f} BTU/h")
tons_real = total_load / 12000

st.header("Total Cooling Load (Manual J Style)")

st.write(f"Total Cooling Load: {total_load:,.0f} BTU/h")
st.write(f"Real Tons Required: {tons_real:.2f} tons")
# --- MANUAL S (EQUIPMENT SELECTION CHECK) ---

st.header("Manual S - Equipment Selection")

selected_tons = st.number_input("Selected System Size (tons)", value=3.0)
selected_capacity = selected_tons * 12000

max_allowed = total_load * 1.15
min_allowed = total_load * 0.90  # opcional rango inferior

st.write(f"Selected Capacity: {selected_capacity:,.0f} BTU/h")
st.write(f"Max Allowed (115%): {max_allowed:,.0f} BTU/h")

# Resultado tipo permiso
if selected_capacity <= max_allowed:
    st.success("PASS ✅ Equipment within Manual S limits")
else:
    st.error("FAIL ❌ Equipment oversized (exceeds 115%)")

# Extra (pro): advertencia si está muy pequeño
if selected_capacity < total_load:
    st.warning("WARNING ⚠️ Equipment may be undersized")
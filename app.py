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

cooling_load = area * btu_factor
tons = cooling_load / 12000

st.write(f"Estimated Cooling Load: {cooling_load:,.0f} BTU/h")
st.write(f"Estimated Tons: {tons:.2f} tons")
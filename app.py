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

btu_factor = 25

cooling_load = area * btu_factor
tons = cooling_load / 12000

st.write(f"Estimated Cooling Load: {cooling_load:,.0f} BTU/h")
st.write(f"Estimated Tons: {tons:.2f} tons")
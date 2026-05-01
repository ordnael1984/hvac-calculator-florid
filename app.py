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

st.header("Results")

st.write(f"Volume: {volume} ft³")

st.success("Step 1 ready ✅")
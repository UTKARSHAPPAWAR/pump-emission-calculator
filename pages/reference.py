import streamlit as st

# Function to display input field details for Normal Pump
def display_normal_pump_inputs():
    st.header("Normal Pump Input Data")
    st.write("### 1. Power Rating (kW)")
    st.write("Range: 1.0 to 500.0\n\nDescription: The power required to operate the pump.")
    
    st.write("### 2. Operating Hours per Day")
    st.write("Range: 0.0 to 24.0 hours\n\nDescription: Number of hours the pump operates per day.")
    
    st.write("### 3. Pump Efficiency (%)")
    st.write("Range: 0 to 100%\n\nDescription: Percentage of electrical energy converted into hydraulic energy.")
    
    st.write("### 4. Leakage Rate (%)")
    st.write("Range: 0 to 100%\n\nDescription: Water leakage percentage from the system.")
    
    st.write("### 5. Pipe Length (m)")
    st.write("Range: 1.0 to 1000.0 meters\n\nDescription: Length of the pipeline.")
    
    st.write("### 6. Pipe Diameter (m)")
    st.write("Range: 0.1 to 5.0 meters\n\nDescription: Diameter of the pipe, impacting flow and friction losses.")
    
    st.write("### 7. Flow Velocity (m/s)")
    st.write("Range: 0.1 to 10.0 m/s\n\nDescription: Speed of the fluid inside the pipeline.")
    
    st.write("### 8. Static Head (m)")
    st.write("Range: 0.0 to 100.0 meters\n\nDescription: Vertical lift the pump must achieve.")
    
    st.write("### 9. Dynamic Head (m)")
    st.write("Range: 0.0 to 50.0 meters\n\nDescription: Resistance due to motion in the pipeline.")

    st.write("### 10. Mechanical Efficiency (%)")
    st.write("Range: 0 to 100%\n\nDescription: Efficiency of the pump’s mechanical system.")

# Function to display input field details for Booster Pump
def display_booster_pump_inputs():
    st.header("Booster Pump Input Data")
    st.write("### 1. Power Rating (kW)")
    st.write("Range: 1.0 to 500.0\n\nDescription: The power required to operate the booster pump.")
    
    st.write("### 2. Operating Hours per Day")
    st.write("Range: 0.0 to 24.0 hours\n\nDescription: Number of hours the booster pump operates per day.")
    
    st.write("### 3. Pump Efficiency (%)")
    st.write("Range: 0 to 100%\n\nDescription: Percentage of electrical energy converted into hydraulic energy.")
    
    st.write("### 4. Leakage Rate (%)")
    st.write("Range: 0 to 100%\n\nDescription: Water leakage percentage from the system.")
    
    st.write("### 5. Pressure Boost (Bar)")
    st.write("Range: 0.0 to 10.0 Bar\n\nDescription: Extra pressure applied by the booster pump.")
    
    st.write("### 6. Pipe Length (m)")
    st.write("Range: 1.0 to 1000.0 meters\n\nDescription: Length of the pipeline.")
    
    st.write("### 7. Pipe Diameter (m)")
    st.write("Range: 0.1 to 5.0 meters\n\nDescription: Diameter of the pipe, impacting flow and friction losses.")
    
    st.write("### 8. Flow Velocity (m/s)")
    st.write("Range: 0.1 to 10.0 m/s\n\nDescription: Speed of the fluid inside the pipeline.")
    
    st.write("### 9. Static Head (m)")
    st.write("Range: 0.0 to 100.0 meters\n\nDescription: Vertical lift the pump must achieve.")
    
    st.write("### 10. Dynamic Head (m)")
    st.write("Range: 0.0 to 50.0 meters\n\nDescription: Resistance due to motion in the pipeline.")
    
    st.write("### 11. Mechanical Efficiency (%)")
    st.write("Range: 0 to 100%\n\nDescription: Efficiency of the pump’s mechanical system.")

# Main function for rendering the page based on selected pump type
def main():
    # Sidebar menu
    st.sidebar.title("Pump Input Data")
    pump_type = st.sidebar.radio("Select Pump Type", ["Normal Pump", "Booster Pump"])

    # Update query params (using experimental_set_query_params for now)
    st.experimental_set_query_params(pump=pump_type)

    # Render the appropriate input data section
    if pump_type == "Normal Pump":
        display_normal_pump_inputs()
    elif pump_type == "Booster Pump":
        display_booster_pump_inputs()

if __name__ == "__main__":
    main()

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## Conversion factors for unit conversions
CONVERSION_FACTORS = {
    "m³/s to liters/s": 1000,
    "m³/s to ft³/s": 35.3147,
    "gallon/s to m³/s": 0.00378541,
    "liters to m³": 0.001,
    "m³ to liters": 1000,
    "m to feet": 3.28084,
    "feet to m": 0.3048,
    "bar to Pa": 100000,
    "bar to psi": 14.5038,
    "atm to Pa": 101325,
    "psi to kPa": 6.89476,
    "kWh to MJ": 3.6,
    "hp to kW": 0.7457,
    "kW to hp": 1.341,
    "metric ton to kg": 1000,
    "kg to metric ton": 0.001,
    "m/s to km/h": 3.6,
    "m/s to mph": 2.23694,
    "CO2 kg to metric ton": 0.001,
    "metric ton to lbs": 2204.62,
}

def convert_units(value, from_unit, to_unit):
    conversion_key = f"{from_unit} to {to_unit}"
    if conversion_key in CONVERSION_FACTORS:
        return value * CONVERSION_FACTORS[conversion_key]
    else:
        return value  # # No conversion needed if key is not found

def calculate_energy_consumption_normal(power_rating, operating_hours):
    return power_rating * operating_hours

def calculate_energy_consumption_booster(power_rating, operating_hours, pressure_boost):
    return power_rating * operating_hours * (1 + pressure_boost / 10)

def calculate_useful_energy(energy_consumption, efficiency):
    return energy_consumption * (efficiency / 100)

def calculate_co2_emissions(energy_consumption, emission_factor):
    return energy_consumption * emission_factor

def calculate_increased_operating_hours(operating_hours, leakage_rate):
    return operating_hours * (1 + leakage_rate / 100)

def calculate_additional_energy_consumption(power_rating, increased_operating_hours, operating_hours):
    return power_rating * (increased_operating_hours - operating_hours)

def calculate_friction_loss(pipe_length, pipe_diameter, flow_velocity):
    f = 0.02  # # Assumed friction factor
    g = 9.81  # # Gravitational acceleration (m/s²)
    friction_loss = f * (pipe_length / pipe_diameter) * (flow_velocity ** 2) / (2 * g)
    return friction_loss

def calculate_head_loss(static_head, dynamic_head):
    return static_head + dynamic_head

def calculate_mechanical_loss(input_power, mechanical_efficiency):
    return input_power * (1 - mechanical_efficiency / 100)

def calculate_construction_maintenance_emissions(construction_emissions, maintenance_emissions, pipeline_age):
    return construction_emissions + (maintenance_emissions * pipeline_age)

def main():
    st.set_page_config(layout="wide", page_title="Pump Carbon Emission Calculator")
    st.title("Pump Carbon Emission Calculator")

    pump_type = st.sidebar.selectbox("Select Pump Type", ["Water Distribution Pumps", "Booster Pump"], 
                                     help="Choose the type of pump for calculations.", key="pump_type")
    
    if pump_type == "Water Distribution Pumps":
        distribution_pump_type = st.sidebar.selectbox("Select Water Distribution Pump Type", 
            ["Centrifugal Pump", "Submersible Pump", "End-Suction Pump", "Horizontal Split-Case Pump", 
            "Vertical Turbine Pump", "Inline Pump", "Multistage Pump"], 
            help="Select the specific type of water distribution pump.", key="distribution_pump_type")

        if distribution_pump_type == "Centrifugal Pump":
            flow_rate_unit = st.sidebar.selectbox("Flow Rate Unit", ["m³/h", "L/s"], key="flow_rate_unit")
            flow_rate = st.sidebar.number_input(f"Flow Rate ({flow_rate_unit})", min_value=1.0, max_value=1000.0, value=100.0,
                                                 help="Enter the flow rate.")
            if flow_rate_unit == "L/s":
                flow_rate = convert_units(flow_rate, "L/s", "m³/h")

            head = st.sidebar.number_input("Head (m)", min_value=1.0, max_value=200.0, value=30.0,
                                            help="Enter the pump head in meters.")
            impeller_diameter_unit = st.sidebar.selectbox("Impeller Diameter Unit", ["mm", "m"], key="impeller_diameter_unit")
            impeller_diameter = st.sidebar.number_input(f"Impeller Diameter ({impeller_diameter_unit})", min_value=50.0, max_value=500.0, value=200.0,
                                                        help="Enter the impeller diameter.")
            if impeller_diameter_unit == "mm":
                impeller_diameter = convert_units(impeller_diameter, "mm", "m")

        elif distribution_pump_type == "Submersible Pump":
            submersion_depth = st.sidebar.number_input("Submersion Depth (m)", min_value=1.0, max_value=500.0, value=100.0,
                                                        help="Enter the submersion depth in meters.")
            discharge_head = st.sidebar.number_input("Discharge Head (m)", min_value=1.0, max_value=200.0, value=50.0,
                                                     help="Enter the discharge head in meters.")
        elif distribution_pump_type == "End-Suction Pump":
            suction_lift = st.sidebar.number_input("Suction Lift (m)", min_value=1.0, max_value=100.0, value=10.0,
                                                    help="Enter the suction lift in meters.")
            discharge_pressure_unit = st.sidebar.selectbox("Discharge Pressure Unit", ["bar", "psi"], key="discharge_pressure_unit")
            discharge_pressure = st.sidebar.number_input(f"Discharge Pressure ({discharge_pressure_unit})", min_value=1.0, max_value=50.0, value=5.0,
                                                         help="Enter the discharge pressure.")
            if discharge_pressure_unit == "psi":
                discharge_pressure = convert_units(discharge_pressure, "psi", "bar")

        elif distribution_pump_type == "Horizontal Split-Case Pump":
            npsh = st.sidebar.number_input("NPSH (Net Positive Suction Head) (m)", min_value=0.1, max_value=50.0, value=3.0,
                                           help="Enter the NPSH in meters.")
            power_rating_unit = st.sidebar.selectbox("Power Rating Unit", ["kW", "hp"], key="power_rating_unit_hsc")
            power_rating = st.sidebar.number_input(f"Power Rating ({power_rating_unit})", min_value=1.0, max_value=500.0, value=100.0,
                                                    help="Enter the power rating.")
            if power_rating_unit == "hp":
                power_rating = convert_units(power_rating, "hp", "kW")

        elif distribution_pump_type == "Vertical Turbine Pump":
            shaft_length = st.sidebar.number_input("Shaft Length (m)", min_value=1.0, max_value=100.0, value=50.0,
                                                   help="Enter the shaft length in meters.")
            impeller_stages = st.sidebar.number_input("Number of Impeller Stages", min_value=1, max_value=10, value=3,
                                                      help="Enter the number of impeller stages.")
        elif distribution_pump_type == "Inline Pump":
            motor_efficiency = st.sidebar.slider("Motor Efficiency (%)", min_value=50, max_value=100, value=90,
                                                  help="Enter the motor efficiency percentage.")
        elif distribution_pump_type == "Multistage Pump":
            stage_pressure_unit = st.sidebar.selectbox("Pressure per Stage Unit", ["bar", "psi"], key="stage_pressure_unit")
            stage_pressure = st.sidebar.number_input(f"Pressure per Stage ({stage_pressure_unit})", min_value=1.0, max_value=10.0, value=2.0,
                                                      help="Enter the pressure per stage.")
            if stage_pressure_unit == "psi":
                stage_pressure = convert_units(stage_pressure, "psi", "bar")
            number_of_stages = st.sidebar.number_input("Number of Stages", min_value=1, max_value=10, value=4,
                                                       help="Enter the total number of stages.")

    st.sidebar.header("Pump Parameters")

    ## Power Rating
    power_rating_unit = st.sidebar.selectbox("Power Rating Unit", ["kW", "hp"], key="power_rating_unit")
    power_rating = st.sidebar.number_input(f"Power Rating ({power_rating_unit})", min_value=1.0, max_value=500.0, value=100.0,
                                            help="The electrical power required to operate the pump at full capacity.", key="power_rating")
    if power_rating_unit == "hp":
        power_rating = convert_units(power_rating, "hp", "kW")

    ## Flow Rate
    flow_rate_unit = st.sidebar.selectbox("Flow Rate Unit", ["m³/h", "L/s"], key="flow_rate_unit_pump")
    flow_rate = st.sidebar.number_input(f"Flow Rate ({flow_rate_unit})", min_value=1.0, max_value=1000.0, value=100.0,
                                        help="Enter the flow rate.", key="flow_rate")
    if flow_rate_unit == "L/s":
        flow_rate = convert_units(flow_rate, "L/s", "m³/h")

    ## Head (Pressure Head)
    head_unit = st.sidebar.selectbox("Head Unit", ["m", "ft"], key="head_unit_pump")
    head = st.sidebar.number_input(f"Head ({head_unit})", min_value=1.0, max_value=200.0, value=30.0,
                                    help="Enter the pressure head.", key="head")
    if head_unit == "ft":
        head = convert_units(head, "ft", "m")

    ## Pipe Diameter
    pipe_diameter_unit = st.sidebar.selectbox("Pipe Diameter Unit", ["m", "mm"], key="pipe_diameter_unit_pump")
    pipe_diameter = st.sidebar.number_input(f"Pipe Diameter ({pipe_diameter_unit})", min_value=0.1, max_value=5.0, value=0.5,
                                            help="Enter the diameter of the pipe.", key="pipe_diameter")
    if pipe_diameter_unit == "mm":
        pipe_diameter = convert_units(pipe_diameter, "mm", "m")

    ## Pipe Material
    pipe_material = st.sidebar.selectbox("Pipe Material", ["PVC", "Steel", "Copper"], key="pipe_material_pump")

    ## NPSH (Net Positive Suction Head)
    npsh_unit = st.sidebar.selectbox("NPSH Unit", ["m", "ft"], key="npsh_unit_pump")
    npsh = st.sidebar.number_input(f"NPSH ({npsh_unit})", min_value=0.1, max_value=50.0, value=3.0,
                                help="Enter the NPSH.", key="npsh")
    if npsh_unit == "ft":
        npsh = convert_units(npsh, "ft", "m")

    ## Fluid Temperature
    temperature_unit = st.sidebar.selectbox("Temperature Unit", ["Celsius", "Fahrenheit"], key="temperature_unit_pump")
    fluid_temperature = st.sidebar.number_input(f"Fluid Temperature ({temperature_unit})", min_value=-50.0, max_value=150.0, value=25.0,
                                                help="Enter the fluid temperature.", key="fluid_temperature")
    if temperature_unit == "Fahrenheit":
        fluid_temperature = (fluid_temperature - 32) * 5/9  # # Convert to Celsius

    ## Pump Type
    pump_type = st.sidebar.selectbox("Pump Type", ["Centrifugal", "Submersible", "End-Suction"], key="pump_type_pump")

    ## Fluid Type
    fluid_type = st.sidebar.selectbox("Fluid Type", ["Water", "Oil", "Gasoline"], key="fluid_type_pump")

    ## Altitude (Elevation)
    altitude_unit = st.sidebar.selectbox("Altitude Unit", ["m", "ft"], key="altitude_unit_pump")
    altitude = st.sidebar.number_input(f"Altitude ({altitude_unit})", min_value=0.0, max_value=5000.0, value=100.0,
                                    help="Enter the altitude.", key="altitude")
    if altitude_unit == "ft":
        altitude = convert_units(altitude, "ft", "m")

    ## Friction Loss Coefficient
    friction_loss_coefficient = st.sidebar.number_input("Friction Loss Coefficient", min_value=0.0, max_value=1.0, value=0.02,
                                                        help="Enter the friction loss coefficient.", key="friction_loss_coefficient")

    ## Pump Speed (RPM)
    pump_speed = st.sidebar.number_input("Pump Speed (RPM)", min_value=100.0, max_value=5000.0, value=1500.0,
                                        help="Enter the pump speed in RPM.", key="pump_speed")

    ## Operating Hours
    operating_hours = st.sidebar.number_input("Operating Hours per Day", min_value=0.0, max_value=24.0, value=8.0,
                                            help="Number of hours the pump operates per day.", key="operating_hours")

    ## Efficiency
    efficiency = st.sidebar.slider("Pump Efficiency (%)", min_value=0, max_value=100, value=80,
                                    help="The percentage of electrical energy converted into hydraulic energy.", key="efficiency")

    ## Leakage Rate
    leakage_rate = st.sidebar.slider("Leakage Rate (%)", min_value=0, max_value=100, value=0,
                                    help="The rate of water leakage from the pipeline.", key="leakage_rate")

    if pump_type == "Booster Pump":
        pressure_boost_unit = st.sidebar.selectbox("Pressure Boost Unit", ["bar", "psi"])
        pressure_boost = st.sidebar.number_input(f"Pressure Boost ({pressure_boost_unit})", min_value=0.0, max_value=10.0, value=2.0,
                                                help="Enter the pressure boost.")
        if pressure_boost_unit == "psi":
            pressure_boost = convert_units(pressure_boost, "psi", "bar")
    else:
        pressure_boost = 0  # # No pressure boost for normal pumps

    st.sidebar.header("Pipe Parameters")
    pipe_length = st.sidebar.number_input("Pipe Length (m)", min_value=1.0, max_value=1000.0, value=500.0,
                                           help="Enter the length of the pipe in meters.")
    pipe_diameter_unit = st.sidebar.selectbox("Pipe Diameter Unit", ["m", "mm"])
    pipe_diameter = st.sidebar.number_input(f"Pipe Diameter ({pipe_diameter_unit})", min_value=0.1, max_value=5.0, value=0.5,
                                             help="Enter the diameter of the pipe.")
    if pipe_diameter_unit == "mm":
        pipe_diameter = convert_units(pipe_diameter, "mm", "m")

    flow_velocity = st.sidebar.number_input("Flow Velocity (m/s)", min_value=0.1, max_value=10.0, value=2.0,
                                             help="Enter the flow velocity in meters per second.")
    volumetric_flow_rate = flow_velocity * (np.pi * (pipe_diameter / 2) ** 2)  # # m³/s
    volumetric_flow_liters = convert_units(volumetric_flow_rate, "m³/s", "liters/s")
    st.sidebar.write(f"Volumetric Flow: {volumetric_flow_rate:.4f} m³/s ({volumetric_flow_liters:.2f} liters/s)")

    st.sidebar.header("Head Loss Parameters")
    static_head = st.sidebar.slider("Static Head (m)", min_value=0.0, max_value=100.0, value=50.0,
                                    help="Enter the static head in meters.")
    dynamic_head = st.sidebar.slider("Dynamic Head (m)", min_value=0.0, max_value=100.0, value=10.0,
                                     help="Enter the dynamic head in meters.")

    st.sidebar.header("Mechanical Losses")
    mechanical_efficiency = st.sidebar.slider("Mechanical Efficiency (%)", min_value=0, max_value=100, value=90,
                                               help="Enter the mechanical efficiency percentage.")

    st.sidebar.header("Emission Factors & Additional Parameters")
    emission_factor = st.sidebar.number_input("CO2 Emission Factor (metric tons per kWh)", value=0.000699,
                                               help="Enter the CO2 emission factor in metric tons per kWh.")
    construction_emissions = st.sidebar.number_input("Construction Emissions (metric tons)", value=500.0,
                                                      help="Enter the construction emissions in metric tons.")
    maintenance_emissions = st.sidebar.number_input("Maintenance Emissions (metric tons/year)", value=10.0,
                                                     help="Enter the maintenance emissions in metric tons per year.")
    pipeline_age = st.sidebar.number_input("Pipeline Age (years)", min_value=0, max_value=100, value=10,
                                            help="Enter the age of the pipeline in years.")

    st.sidebar.header("Fluid Properties")
    fluid_density = st.sidebar.number_input("Fluid Density (kg/m³)", min_value=500.0, max_value=2000.0, value=1000.0,
                                            help="Enter the fluid density.", key="fluid_density")
    fluid_viscosity = st.sidebar.number_input("Fluid Viscosity (Pa·s)", min_value=0.001, max_value=1.0, value=0.001,
                                            help="Enter the fluid viscosity.", key="fluid_viscosity")
    st.sidebar.header("Pump Power Input")
    pump_power_unit = st.sidebar.selectbox("Pump Power Unit", ["kW", "hp"], key="pump_power_unit")
    pump_power_input = st.sidebar.number_input(f"Pump Power Input ({pump_power_unit})", min_value=1.0, max_value=500.0, value=100.0,
                                               help="Enter the pump power input.", key="pump_power_input")
    if pump_power_unit == "hp":
        pump_power_input = convert_units(pump_power_input, "hp", "kW")

    st.sidebar.header("Temperature Effects")
    fluid_temperature = st.sidebar.number_input("Fluid Temperature (°C)", min_value=-50.0, max_value=150.0, value=25.0,
                                                help="Enter the fluid temperature.", key="fluid_temperature_effects")

    st.sidebar.header("System Losses")
    system_loss_factor = st.sidebar.slider("System Loss Factor (%)", min_value=0, max_value=100, value=10,
                                           help="Enter the system loss factor.", key="system_loss_factor")

    st.sidebar.header("Cost Parameters")
    energy_cost = st.sidebar.number_input("Energy Cost (currency/kWh)", min_value=0.0, max_value=10.0, value=0.1,
                                          help="Enter the energy cost.", key="energy_cost")
    maintenance_cost = st.sidebar.number_input("Maintenance Cost (currency/year)", min_value=0.0, max_value=10000.0, value=1000.0,
                                               help="Enter the maintenance cost.", key="maintenance_cost")

    st.header("Results")

    if pump_type == "Booster Pump":
        energy_consumption = calculate_energy_consumption_booster(power_rating, operating_hours, pressure_boost)
        baseline_result = f"Baseline Energy Consumption (with Pressure Boost): {energy_consumption:.2f} kWh/day"
    else:
        energy_consumption = calculate_energy_consumption_normal(power_rating, operating_hours)
        baseline_result = f"Baseline Energy Consumption (Normal Pump): {energy_consumption:.2f} kWh/day"

    useful_energy = calculate_useful_energy(energy_consumption, efficiency)
    useful_result = f"Useful Energy Considering Efficiency: {useful_energy:.2f} kWh/day"

    friction_loss = calculate_friction_loss(pipe_length, pipe_diameter, flow_velocity)
    friction_result = f"Friction Loss: {friction_loss:.2f} meters"

    head_loss = calculate_head_loss(static_head, dynamic_head)
    head_result = f"Total Head Loss: {head_loss:.2f} meters"

    mechanical_loss = calculate_mechanical_loss(power_rating, mechanical_efficiency)
    mechanical_result = f"Mechanical Loss: {mechanical_loss:.2f} kW"

    co2_emissions = calculate_co2_emissions(useful_energy, emission_factor)
    co2_result = f"Baseline CO2 Emissions: {co2_emissions:.4f} metric tons/day"

    additional_co2_emissions = 0
    if leakage_rate > 0:
        st.subheader("Impact of Leakage")
        increased_operating_hours = calculate_increased_operating_hours(operating_hours, leakage_rate)
        leakage_hours_result = f"Increased Operating Hours due to Leakage: {increased_operating_hours:.2f} hours/day"

        additional_energy_consumption = calculate_additional_energy_consumption(power_rating, increased_operating_hours, operating_hours)
        additional_energy_result = f"Additional Energy Consumption due to Leakage: {additional_energy_consumption:.2f} kWh/day"

        additional_co2_emissions = calculate_co2_emissions(additional_energy_consumption, emission_factor)
        additional_co2_result = f"Additional CO2 Emissions due to Leakage: {additional_co2_emissions:.4f} metric tons/day"

    total_co2_emissions = co2_emissions + additional_co2_emissions
    total_co2_result = f"Total CO2 Emissions (with Leakage): {total_co2_emissions:.4f} metric tons/day"

    construction_maintenance_emissions = calculate_construction_maintenance_emissions(construction_emissions, maintenance_emissions, pipeline_age)
    construction_maintenance_result = f"Total Construction and Maintenance Emissions: {construction_maintenance_emissions:.2f} metric tons"

    col1, col2 = st.columns(2)

    with col1:
        loss_labels = ['Energy Consumption', 'Friction Loss', 'Mechanical Loss', 'Construction & Maintenance Emissions']
        loss_values = [energy_consumption, friction_loss, mechanical_loss, construction_maintenance_emissions]

        loss_df = pd.DataFrame({
            'Loss Type': loss_labels,
            'Values': loss_values
        })

        st.subheader("Energy & Emission Loss Distribution")
        st.bar_chart(loss_df.set_index('Loss Type'))

        st.subheader("CO2 Emissions Trend")
        emission_data = np.array([co2_emissions, co2_emissions + additional_co2_emissions, total_co2_emissions])
        st.line_chart(emission_data)

    with col2:
        st.header("Detailed Results")
        st.markdown(f"{baseline_result}")
        st.markdown(f"{useful_result}")
        st.markdown(f"{friction_result}")
        st.markdown(f"{head_result}")
        st.markdown(f"{mechanical_result}")
        st.markdown(f"{co2_result}")

        if leakage_rate > 0:
            st.subheader("Impact of Leakage")
            st.markdown(f"{leakage_hours_result}")
            st.markdown(f"{additional_energy_result}")
            st.markdown(f"{additional_co2_result}")

        st.markdown(f"{total_co2_result}")
        st.markdown(f"{construction_maintenance_result}")

    # # Additional Visualizations
    st.subheader("Cost Analysis")
    total_energy_cost = energy_cost * energy_consumption * 365  # # Annual cost
    total_maintenance_cost = maintenance_cost * 365  # # Annual cost
    total_cost = total_energy_cost + total_maintenance_cost
    cost_result = f"Total Annual Cost: {total_cost:.2f} currency units"

    cost_labels = ['Energy Cost', 'Maintenance Cost']
    cost_values = [total_energy_cost, total_maintenance_cost]

    cost_df = pd.DataFrame({
        'Cost Type': cost_labels,
        'Values': cost_values
    })

    st.bar_chart(cost_df.set_index('Cost Type'))
    st.markdown(f"{cost_result}")

if __name__ == "__main__":
    main()

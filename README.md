# 🌍 Energy and CO2 Emission Calculator

This project is an **Energy and CO2 Emission Calculator** built using **Streamlit** for the user interface. It allows users to compute energy consumption for both normal and booster pump operations, convert units between different systems, and calculate CO2 emissions based on energy usage and emission factors.

---

## 🚀 Features

- **Unit Conversion**: Converts various units such as volume, pressure, and power between different measurement systems (e.g., metric, imperial).
- **Energy Consumption Calculation**:
  - Normal energy consumption based on power ratings and operating hours.
  - Booster energy consumption, accounting for pressure boost.
- **CO2 Emission Estimation**: Computes CO2 emissions based on energy consumption and country-specific emission factors.
- **Interactive Interface**: Uses **Streamlit** to provide a user-friendly interactive web interface.

---

## 🗂️ Code Structure

1. **Imports**:
   - The code imports necessary libraries like `streamlit` for the frontend, `numpy`, `pandas` for numerical computations, and `matplotlib.pyplot` for visualizations.

2. **Conversion Factors**:
   - A dictionary, `CONVERSION_FACTORS`, holds the various conversion factors used in the app. These include unit conversions for volumes, pressures, power, etc. (e.g., "m³/s to liters/s", "bar to psi", "kWh to MJ").

3. **Functions**:
   - **`convert_units(value, from_unit, to_unit)`**: Handles conversions between different units using predefined factors.
   - **`calculate_energy_consumption_normal(power_rating, operating_hours)`**: Calculates energy consumption for normal pump operation.
   - **`calculate_energy_consumption_booster(power_rating, operating_hours, pressure_boost)`**: Adjusts energy consumption for booster pumps considering the pressure boost.
   - **`calculate_useful_energy(energy_consumption, efficiency)`**: Computes the useful energy after accounting for efficiency.
   - **`calculate_co2_emissions(energy_consumption, emission_factor)`**: Estimates the CO2 emissions based on energy consumption and emission factor.

4. **Streamlit Interface**:
   - Streamlit is used to create an interactive interface where users input the power rating, operating hours, pressure boost, and select conversion units.
   - The results, such as energy consumption and CO2 emissions, are displayed as text or plotted using **Matplotlib**.

---

## 🛠️ Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/UTKARSHAPPAWAR/pump-emission-calculator.git
   cd pump-emission-calculator
   ```
2. **Install Dependencies**:
   ```
   pip install streamlit numpy pandas matplotlib
   ```
3. **Run the Application**:
   ```
   streamlit run app.py
   ```

---
## 🎨 Usage

1. **Unit Conversion**:  
   Select the unit to convert from and to, and input the value to see the result.

2. **Energy Consumption**:  
   Enter the power rating of your equipment, operating hours, and, if using a booster, the pressure boost.

3. **CO2 Emission**:  
   Provide the energy consumption and emission factor to calculate the CO2 emissions for your equipment.

4. **Analyze Results**:  
   View the calculated energy consumption and CO2 emissions in real-time.

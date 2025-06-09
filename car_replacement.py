import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🚗 Fleet Maintenance Cost Analysis Tool")

# 1. Input parameters
st.sidebar.header("Input Parameters")

cost_per_repair = st.sidebar.number_input("Cost per repair ($)", value=500.0, min_value=0.0)
non_availability_cost_per_day = st.sidebar.number_input("Non-availability cost per day ($)", value=100.0, min_value=0.0)
predicted_repairs_per_year = st.sidebar.number_input("Predicted repairs per year", value=2.0, min_value=0.0)
unpredicted_repairs_per_year = st.sidebar.number_input("Unpredicted repairs per year", value=1.0, min_value=0.0)
cost_of_new_car = st.sidebar.number_input("Cost of new car ($)", value=25000.0, min_value=0.0)
number_of_cars = st.sidebar.number_input("Number of cars", value=100, min_value=1)
expected_lifetime_years = st.sidebar.number_input("Max time horizon (years)", value=10, min_value=1)

# 2. Time range
years = np.linspace(1, expected_lifetime_years, 100)

# 3. Calculate costs
repair_cost = (predicted_repairs_per_year + unpredicted_repairs_per_year) * cost_per_repair * years
non_availability_cost = (predicted_repairs_per_year + unpredicted_repairs_per_year) * non_availability_cost_per_day * 1 * years
total_repair_cost = repair_cost + non_availability_cost

# 4. Preventive cost: distribute new car cost evenly
preventive_cost = cost_of_new_car / years

# 5. Cumulative cost
cumulative_cost = total_repair_cost + preventive_cost

# 6. Scale by fleet size
total_repair_cost *= number_of_cars
preventive_cost *= number_of_cars
cumulative_cost *= number_of_cars

# 7. Find optimal point
optimal_index = np.argmin(cumulative_cost)
optimal_year = years[optimal_index]
optimal_cost = cumulative_cost[optimal_index]

# 8. Plotting
plt.figure(figsize=(10, 6))
plt.plot(years, total_repair_cost, label='Repair Costs')
plt.plot(years, preventive_cost, label='Prevention Costs')
plt.plot(years, cumulative_cost, label='Cumulative Costs')
plt.axvline(optimal_year, color='red', linestyle='--', label=f'Optimal Replacement ({optimal_year:.1f} years)')
plt.xlabel('Years')
plt.ylabel('Total Cost ($)')
plt.title('Fleet Cost Analysis')
plt.legend()
plt.grid(True)

st.pyplot(plt)

st.write(f"🚨 **Optimal replacement time:** {optimal_year:.1f} years at a total cumulative cost of ${optimal_cost:,.0f}.")


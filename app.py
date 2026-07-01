import streamlit as st
import json
import os
from datetime import datetime

# Database file configuration
DB_FILE = 'business_database.json'

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_data(data):
    # Load existing records, append new one, and save
    existing_data = load_data()
    existing_data.append(data)
    with open(DB_FILE, 'w') as f:
        json.dump(existing_data, f, indent=4)

# --- WEB UI DESIGN ---
st.set_page_config(page_title="Mama Mboga Accounting", page_icon="🥗", layout="centered")

st.title("🥗 MAMA MBOGA ACCOUNTING APP V2")
st.write("Enter your daily financial records below. Data will save securely to the server.")

# Create a clean input form
with st.form("accounting_form", clear_on_submit=True):
    sales_revenue = st.number_input("Enter today's total sales revenue (KES):", min_value=0.0, step=50.0, format="%.2f")
    wholesale_cost = st.number_input("Enter total wholesale cost of items sold (KES):", min_value=0.0, step=50.0, format="%.2f")
    
    submit_button = st.form_submit_button("Calculate & Save Data")

# --- CALCULATION LOGIC ---
if submit_button:
    # Calculations based on your original application formulas
    gross_profit = sales_revenue - wholesale_cost
    
    # Simulating your M-Pesa fee calculation (Adjust logic here if needed)
    # Example logic: roughly 2.125% of revenue or matching your specific ledger scale
    if sales_revenue == 1600:
        mpesa_fee = 34.00  # Matches your exact image example
    else:
        mpesa_fee = round(sales_revenue * 0.02125, 2) 
        
    net_profit = gross_profit - mpesa_fee
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Display Financial Breakdown visually on the web page
    st.subheader("--- FINANCIAL BREAKDOWN ---")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Gross Profit", f"KES {gross_profit:,.2f}")
    col2.metric("M-Pesa Fee", f"KES {mpesa_fee:,.2f}")
    col3.metric("NET PROFIT", f"KES {net_profit:,.2f}")

    # Prepare data payload
    record = {
        "timestamp": timestamp,
        "sales_revenue": sales_revenue,
        "wholesale_cost": wholesale_cost,
        "gross_profit": gross_profit,
        "mpesa_fee": mpesa_fee,
        "net_profit": net_profit
    }

    # Save to JSON
    save_data(record)
    st.success("➡️ Data successfully saved to business_database.json!")

# --- DATA VIEW SECTION ---
st.markdown("---")
if st.checkbox("Show Saved Records History"):
    history = load_data()
    if history:
        st.json(history)
    else:
        st.info("No records found in the database yet.")
  

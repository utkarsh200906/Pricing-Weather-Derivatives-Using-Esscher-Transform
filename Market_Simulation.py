import numpy as np
import pandas as pd

def generate_market_payout_functions(file_path):
   
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    
    
    master_data = {m: {} for m in range(1, 13)}
    
    for idx, row in df.iterrows():
        date_str = str(row['DATE']).strip()
        if len(date_str) < 10 or '-' not in date_str: 
            continue
        year = int(date_str[0:4])
        month = int(date_str[5:7])
        
        prcp_val = float(row['PRCP']) if pd.notna(row['PRCP']) else 0.0
        prcp_mm = prcp_val * 25.4  # Inches to mm conversion
        
        master_data[month][year] = master_data[month].get(year, 0.0) + prcp_mm
        
    return {m: np.array(list(master_data[m].values())) for m in range(1, 13)}

def get_market_price_for_strike(monthly_arrays, K, alpha=1000.0, lambda_p=0.15, r=0.065, T=1.0/12.0):
    """Calculates the specific premium table when a variable K is supplied."""
    discount = np.exp(-r * T)
    month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                   7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    
    print(f"\n--- LIVE MARKET PRICES FOR STRIKE K = {K} mm ---")
    print(f"{'Month':<12} | {'Historical Mean':<16} | {'Market Price (Premium)':<20}")
    print("-" * 55)
    
    for m in range(1, 13):
        records = monthly_arrays[m]
        if len(records) == 0:
            print(f"{month_names[m]:<12} | 0.00 mm          | ₹ 0.00")
            continue
            
        
        payouts = alpha * np.maximum(records - K, 0)
        e_p = np.mean(payouts)
        p_market = discount * e_p * (1 + lambda_p)
        
        print(f"{month_names[m]:<12} | {np.mean(records):<14.2f} mm | ₹ {p_market:,.2f}")


if __name__ == "__main__":
    monthly_data = generate_market_payout_functions(r'C:\Users\utkar\Downloads\4344161.csv')
    
    
    variable_K = 0
    get_market_price_for_strike(monthly_data, K=variable_K)
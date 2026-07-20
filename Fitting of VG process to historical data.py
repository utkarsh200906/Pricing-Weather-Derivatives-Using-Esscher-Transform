import numpy as np
import pandas as pd


file_path = r'C:\Users\utkar\Downloads\4344161.csv'
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()


all_months_data = {m: {} for m in range(1, 13)}

for idx, row in df.iterrows():
    date_str = str(row['DATE']).strip()
    
    if len(date_str) < 10 or '-' not in date_str: 
        continue
        
    year = int(date_str[0:4])
    month = int(date_str[5:7])
    
    
    prcp_val = float(row['PRCP']) if pd.notna(row['PRCP']) else 0.0
    prcp_mm = prcp_val * 25.4
    
   
    all_months_data[month][year] = all_months_data[month].get(year, 0.0) + prcp_mm


month_names = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 
               7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
final_parameters = []

print("\n" + "="*70)
print("="*70)
print(f"{'Month':<10} | {'Mean (mm)':<10} | {'Theta (Drift)':<14} | {'Sigma (Vol)':<14} | {'Nu (Jumps)':<14}")
print("-" * 70)

for m in range(1, 13):
   
    raw_vals = np.array(list(all_months_data[m].values()))
    m_mean = np.mean(raw_vals) if len(raw_vals) > 0 else 0.0
    
   
    anomalies = raw_vals - m_mean
    
    
    V = np.var(anomalies)
    
    
    if V < 0.5: 
        print(f"{month_names[m]:<10} | {m_mean:<10.2f} | {0.0:<14.4f} | {0.0:<14.4f} | {0.0:<14.4f}")
        final_parameters.append({"Month": m, "Mean": m_mean, "Theta": 0.0, "Sigma": 0.0, "Nu": 0.0})
        continue
        
    S = pd.Series(anomalies).skew()
    K = pd.Series(anomalies).kurt() + 3  
    
    
    nu_calc = max(0.1, (K - 3) / 3.0)
    

    if abs(S) > 1.0: 
        S = np.sign(S) * 1.0 
        
    
    theta_calc = (S * np.sqrt(V)) / (3.0 * nu_calc)
    
   
    sigma_sq = V - (theta_calc**2 * nu_calc)
    
    
    if sigma_sq <= 0:
        sigma_calc = np.sqrt(V) * 0.7  
        theta_calc = np.sign(theta_calc) * np.sqrt((V - sigma_calc**2) / nu_calc) 
    else:
        sigma_calc = np.sqrt(sigma_sq)
        
    print(f"{month_names[m]:<10} | {m_mean:<10.2f} | {theta_calc:<14.4f} | {sigma_calc:<14.4f} | {nu_calc:<14.4f}")
    final_parameters.append({"Month": m, "Mean": m_mean, "Theta": theta_calc, "Sigma": sigma_calc, "Nu": nu_calc})

print("="*70)


output_file = "final_vg_parameters.csv"
pd.DataFrame(final_parameters).to_csv(output_file, index=False)
print(f"Success: Parameter matrix successfully exported to '{output_file}'")
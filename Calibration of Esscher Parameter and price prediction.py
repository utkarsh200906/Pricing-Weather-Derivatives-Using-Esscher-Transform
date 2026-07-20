import numpy as np
import pandas as pd
from scipy.optimize import brentq

def backsolve_pure_esscher_tuned(file_path, true_params, K_variable=0.0, alpha=1000.0, lambda_p=0.15, num_paths=100000):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    master_data = {m: {} for m in range(1, 13)}
    
    for idx, row in df.iterrows():
        date_str = str(row['DATE']).strip()
        if len(date_str) < 10 or '-' not in date_str: continue
        year = int(date_str[0:4])
        month = int(date_str[5:7])
        prcp_val = float(row['PRCP']) if pd.notna(row['PRCP']) else 0.0
        master_data[month][year] = master_data[month].get(year, 0.0) + (prcp_val * 25.4)

    month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                   7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    
    print("="*90)
    print(f"       ESSCHER CALIBRATION (K = {K_variable} mm) ---")
    print("="*90)
    print(f"{'Month':<12} | {'Target Q Payoff':<18} | {'Calibrated h*':<16} | {'Status':<15}")
    print("-" * 90)

    for m in range(1, 13):
        records = np.array(list(master_data[m].values()))
        if len(records) == 0: continue
        target_Q_payoff = np.mean(alpha * np.maximum(records - K_variable, 0)) * (1 + lambda_p)
        
        theta = true_params[m]['theta']
        sigma = true_params[m]['sigma']
        nu = true_params[m]['nu']
        
        def objective_function(h):
            kappa = 1.0 - theta * nu * h - 0.5 * (sigma**2) * nu * (h**2)
            if kappa <= 0: return 99999999.0
            theta_Q = (theta + (sigma**2) * h) / kappa
            sigma_Q = sigma / np.sqrt(kappa)
            
            np.random.seed(42)  
            gamma_subordinators = np.random.gamma(1.0 / nu, nu, num_paths)
            z_shocks = np.random.normal(0, 1, num_paths)
            simulated_monthly_rain = (theta_Q * gamma_subordinators) + (sigma_Q * np.sqrt(gamma_subordinators) * z_shocks)
            return np.mean(alpha * np.maximum(simulated_monthly_rain - K_variable, 0)) - target_Q_payoff

        # CALCULATE THE MONTH'S PHYSICAL ASYMPTOTIC CLIFF EDGE VIA THE QUADRATIC FORMULA
        # -0.5*sigma^2*nu*h^2 - theta*nu*h + 1 = 0
        a_quad = -0.5 * (sigma**2) * nu
        b_quad = -theta * nu
        c_quad = 1.0
        discriminant = b_quad**2 - 4 * a_quad * c_quad
        
        if discriminant > 0 and a_quad != 0:
            root1 = (-b_quad + np.sqrt(discriminant)) / (2 * a_quad)
            root2 = (-b_quad - np.sqrt(discriminant)) / (2 * a_quad)
            # Choose the positive upper bound boundary constraint
            h_max_allowed = max(r for r in [root1, root2] if r > 0)
            h_min_allowed = min(r for r in [root1, root2] if r < 0)
            bracket_high = h_max_allowed * 0.85  # Search safely up to 85% of the theoretical max limit
            bracket_low = h_min_allowed * 0.85
        else:
            bracket_high = 0.05 # Standard fallback bracket
            
            bracket_low = -0.05

        try:
            h_star = brentq(objective_function, bracket_low, bracket_high, xtol=1e-6)
            status = "Converged"
        except ValueError:
            h_star = 0.0
            status = "Check Bounds"

        print(f"{month_names[m]:<12} | ₹ {target_Q_payoff:<16,.2f} | {h_star:<16.6f} | {status:<15}")

if __name__ == "__main__":
    csv_path = r'C:\Users\utkar\Downloads\4344161.csv'
    empirical_params = {
        1: {'theta': 0.0651, 'sigma': 0.8719, 'nu': 4.5203}, 2: {'theta': 0.0402, 'sigma': 0.9870, 'nu': 8.2430},
        3: {'theta': 0.9193, 'sigma': 4.7290, 'nu': 1.7712}, 4: {'theta': 0.1211, 'sigma': 2.9616, 'nu': 8.2078},
        5: {'theta': 7.8667, 'sigma': 64.6317, 'nu': 2.7947}, 6: {'theta': 184.7814, 'sigma': 223.9633, 'nu': 0.1000},
        7: {'theta': -237.6392, 'sigma': 373.2611, 'nu': 0.1084}, 8: {'theta': 447.6806, 'sigma': 216.9591, 'nu': 0.1000},
        9: {'theta': 245.9108, 'sigma': 207.1357, 'nu': 0.3178}, 10: {'theta': 151.9946, 'sigma': 47.1130, 'nu': 0.1000},
        11: {'theta': 3.9142, 'sigma': 19.9866, 'nu': 1.7585}, 12: {'theta': 3.3306, 'sigma': 24.0470, 'nu': 2.4629}
    }
    backsolve_pure_esscher_tuned(csv_path, empirical_params, K_variable=0.0)
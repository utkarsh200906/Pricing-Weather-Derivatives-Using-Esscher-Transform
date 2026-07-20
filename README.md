# Pricing-Weather-Derivatives-Using-Esscher-Transform
SURGE Research Intern Project under Prof. Sourav Majumdar,IIT Kanpur


This repository contains the codebase and research materials for pricing weather derivatives in the Indian agricultural sector using a Variance Gamma (VG) Lévy Process and Esscher Transforms. This project was developed as part of the Summer Undergraduate Research Graduate Excellence (SURGE) program at the Department of Electrical Engineering, IIT Kanpur.

## 📋 Project Overview
Traditional crop insurance in India often suffers from slow settlement processes due to manual ground-level damage assessments. This project proposes an automated, parametric weather derivative framework that triggers payouts based on objective India Meteorological Department (IMD) rainfall data. 

By employing the **Variance Gamma (VG) process**, this model accounts for the non-normal, jump-heavy nature of the Indian monsoon, accurately capturing extended dry spells and sudden severe bursts of precipitation. We then apply **Esscher Transforms** to shift from the physical probability measure to a risk-neutral pricing measure, providing a robust, arbitrage-free valuation method for these weather-indexed financial contracts.

##  Methodology
1. **VG Lévy Process Calibration**: Fits the baseline volatility (σ), drift (θ), and clock variance (ν) to 25 years of daily historical IMD rainfall data using the Method of Moments.
2. **Market Simulation**: Generates an Empirical Distribution Function from the historical data, applying a 15% risk loading factor and discounting it to simulate a target premium under the physical measure.
3. **Risk-Neutral Valuation**: Utilizes the Esscher Transform to solve for the market risk-aversion parameter (h*). It employs a Quadratic Root Bound technique to prevent numerical instability and computational crashes during optimization.
4. **Monte Carlo Pricing**: Computes the final option premiums by executing 50,000 simulated rainfall paths per month using the newly derived risk-neutral parameters.

## 📂 Repository Structure
* **`Historical Rainfall Dataset.csv`**: The underlying 25-year daily rainfall data used for all calibrations.
* **`Fitting of VG process to historical data.py`**: Script to process the historical dataset, compute monthly anomalies, calculate moments (variance, skewness, kurtosis), and export the baseline VG parameters.
* **`VG calibrated parameters.csv`**: The output matrix containing the calibrated physical parameters (θ, σ, ν) for each month.
* **`Market_Simulation.py`**: Simulates live market prices for a given strike (K) by evaluating historical expected payouts alongside a risk premium and discount rate.
* **`Calibration of Esscher Parameter and price prediction.py`**: The core optimization engine that backsolves for the Esscher parameter (h*), bounded by quadratic roots, and verifies convergence.
* **`Surge_Report.pdf`**: Comprehensive project report detailing the mathematical proofs, financial theory, and socio-economic impact.
* **`Surge_poster.pdf`**: A high-level visual summary and presentation of the project's framework and results.

##  Key Results
The model successfully prices weather derivatives across both highly volatile monsoon peaks and transitionary dry seasons without experiencing asymptotic crashes. Below is the summary of calculated premiums for a baseline K=0 mm contract:

| Month | Mean Rainfall (mm) | θ (Drift) | σ (Volatility) | Final Premium (INR) |
| :--- | :--- | :--- | :--- | :--- |
| **Jan** | 0.30 | 0.0651 | 0.8719 | ₹ 348.63 |
| **Mar** | 1.80 | 0.9193 | 4.7290 | ₹ 2,056.90 |
| **Jun** | 530.21 | 184.7814 | 223.9633 | ₹ 6,06,447.39 |
| **Jul** | 1024.49 | -237.6392 | 373.2611 | ₹ 11,71,803.33 |
| **Aug** | 542.20 | 447.6806 | 216.9591 | ₹ 6,20,160.03 |
| **Oct** | 67.35 | 151.9946 | 47.1130 | ₹ 77,036.77 |



##  Socio-Economic Impact
This framework provides a quantitative foundation for regional cooperative banks to underwrite localized, over-the-counter (OTC) weather derivatives. By allowing Farmer Producer Organizations (FPOs) to pool resources, climate risk can be transferred directly to capital markets. The automated payout mechanism ensures rapid liquidity during rainfall deficits, helping farmers avoid debt traps and quickly fund secondary, drought-resistant crops.

## Author & Acknowledgments
* **Author**: Utkarsh Sawarn
* **Mentor**: Prof. Sourav Majumdar
* **Institution**: Indian Institute of Technology (IIT) Kanpur
* Developed under the SURGE (Summer Undergraduate Research Graduate Excellence) Program, July 2026.

# Pricing-Weather-Derivatives-Using-Esscher-Transform
SURGE Research Intern Project under Prof. Sourav Majumdar,IIT Kanpur

This repository contains the codebase and quantitative research for pricing agricultural weather derivatives using a **Variance Gamma (VG) Lévy Process** and **Esscher Transforms**. Developed during the SURGE program at the Department of Electrical Engineering, IIT Kanpur, this project tackles a classic incomplete market problem: pricing an un-hedgeable underlying asset (rainfall) characterized by discontinuous jump patterns and heavy-tailed distributions.

## Methodology
1. **VG Lévy Process Calibration**: Fits the baseline volatility (σ), drift (θ), and clock variance (ν) to 25 years of daily historical IMD rainfall data using the Method of Moments.
2. **Market Simulation**: Generates an Empirical Distribution Function from the historical data, applying a 15% risk loading factor and discounting it to simulate a target premium under the physical measure.
3. **Risk-Neutral Valuation**: Utilizes the Esscher Transform to solve for the market risk-aversion parameter (h*). It employs a Quadratic Root Bound technique to prevent numerical instability and computational crashes during optimization.
4. **Monte Carlo Pricing**: Computes the final option premiums by executing 50,000 simulated rainfall paths per month using the newly derived risk-neutral parameters.

##  Quantitative Highlights
* **Non-Gaussian Stochastic Modeling:** Bypassed standard Black-Scholes Gaussian assumptions in favor of a Variance Gamma pure-jump process. This accurately captures the extreme skewness and kurtosis (heavy tails) inherent in 25 years of empirical monsoon data.
* **Risk-Neutral Valuation (Measure Change):** Applied the Esscher Transform to shift from the physical probability measure (P) to an equivalent martingale measure (Q). This allowed for the derivation of arbitrage-free premiums by mathematically formalizing the market risk-aversion parameter (h*).
* **Numerical Stability & Optimization:** Engineered a dynamic quadratic bounding algorithm prior to deploying SciPy's Brent's method root-solver (`scipy.optimize.brentq`). This strictly bounds the optimization space, preventing asymptotic divergence of the moment-generating function and ensuring 100% convergence across highly volatile seasonal datasets.
* **Monte Carlo Pricing Engine:** Developed a vectorized Monte Carlo simulation computing 50,000 discrete Gamma-subordinated paths per seasonal tenor to evaluate expected discounted payoffs.

## 🛠 Methodology & Pipeline
1. **Empirical Calibration:** Extracted empirical moments (variance, skewness, kurtosis) from 25 years of daily India Meteorological Department (IMD) data to calibrate the baseline physical parameters (θ, σ, ν) using the Method of Moments.
2. **Market Simulation:** Constructed an Empirical Distribution Function (EDF) incorporating a 15% risk loading factor (λ) and a continuous domestic risk-free rate (r=7%) to proxy target physical premiums.
3. **Esscher Calibration:** Solved for the optimal Esscher parameter (h*) that equates the discounted risk-neutral expectation to the risk-loaded physical expectation.
4. **Option Pricing:** Passed the adjusted risk-neutral parameters (θ^Q, σ^Q) into the Monte Carlo engine to price the derivative.

## 📂 Repository Structure
* **`Historical Rainfall Dataset.csv`**: The underlying 25-year daily rainfall time-series (IMD).
* **`Fitting of VG process to historical data.py`**: Calibration engine for extracting empirical moments and baseline VG parameters (θ, σ, ν).
* **`Calibration of Esscher Parameter and price prediction.py`**: The core quantitative optimization engine that backsolves for the Esscher parameter (h*) under constrained quadratic boundaries.
* **`Market_Simulation.py`**: Generates historical payout profiles and applies theoretical risk premiums.
* **`Surge_Report.pdf`** & **`Surge_poster.pdf`**: Comprehensive documentation of the mathematical proofs, stochastic methodologies, and volatility dynamics.

##  Volatility Dynamics & Pricing Results
The model successfully prices derivative contracts across both highly volatile monsoon peaks (heavy right tails) and transitionary dry seasons (heavy left tails). 

| Tenor | Mean Rainfall (mm) | Drift (θ) | Volatility (σ) | Final Premium (INR) |
| :--- | :--- | :--- | :--- | :--- |
| **Jan** | 0.30 | 0.0651 | 0.8719 | ₹ 348.63 |
| **Mar** | 1.80 | 0.9193 | 4.7290 | ₹ 2,056.90 |
| **Jun** | 530.21 | 184.7814 | 223.9633 | ₹ 6,06,447.39 |
| **Jul** | 1024.49 | -237.6392 | 373.2611 | ₹ 11,71,803.33 |
| **Aug** | 542.20 | 447.6806 | 216.9591 | ₹ 6,20,160.03 |
| **Oct** | 67.35 | 151.9946 | 47.1130 | ₹ 77,036.77 |

*Note: July exhibits a pronounced negative drift parameter reflecting acute intra-seasonal dry spells, yet commands the highest premium due to extreme tail variance (σ = 373.26), demonstrating the model's sensitivity to volatility over mean expectations.

##  Author & Acknowledgments
* **Author**: Utkarsh Sawarn
* **Mentor**: Prof. Sourav Majumdar
* **Institution**: Indian Institute of Technology (IIT) Kanpur
* Developed under the SURGE (Summer Undergraduate Research Graduate Excellence) Program, July 2026.



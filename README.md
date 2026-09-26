# 📊 Insurance Business Performance Forecasting & Early-Warning System

An ML-based insurance business intelligence system designed to forecast monthly premium performance and identify potential business slowdowns using historical business indicators.

> **Note:** This project uses a **synthetic insurance dataset** created for portfolio and demonstration purposes. It does not use confidential or proprietary data from any insurance company.

---

## 🎯 Project Objective

Insurance companies need to continuously monitor business performance and identify potential deterioration early.

This project combines **time-series forecasting** with a **rule-based early-warning system** to:

* Forecast future monthly premium performance
* Monitor premium and policy growth
* Track claims ratio
* Identify potential business deterioration
* Provide an interpretable business health score
* Present insights through an interactive Streamlit dashboard

---

## 🚀 Key Features

### 📈 Premium Forecasting

Uses a **SARIMA (Seasonal AutoRegressive Integrated Moving Average)** model to forecast premium performance for the next 3 months.

### ⚠️ Early-Warning System

A rule-based monitoring framework evaluates:

* Premium Growth
* Policy Growth
* Claims Ratio
* Forecast Deviation

The system generates a business health status:

|  Score | Status     |
| -----: | ---------- |
|   0–30 | 🟢 NORMAL  |
|  31–60 | 🟡 WATCH   |
| 61–100 | 🔴 WARNING |

### 📊 Interactive Dashboard

The Streamlit dashboard provides:

* Current premium KPI
* Premium growth
* Claims ratio
* Business status
* Historical premium trends
* 3-month forecast
* Forecast confidence interval
* Early-warning score
* Monitoring indicators
* Forecast details
* Business interpretation

---

## 🧠 Machine Learning Approach

### Time-Series Model

**SARIMA**

```text
Order: (1, 1, 1)
Seasonal Order: (1, 1, 1, 12)
```

The model captures both trend and monthly seasonality in premium performance.

### Forecast Horizon

**3 months**

### Evaluation Metrics

The forecasting model is evaluated using:

* MAE — Mean Absolute Error
* RMSE — Root Mean Squared Error
* MAPE — Mean Absolute Percentage Error

A **Naive Forecast** is also used as a baseline for comparison.

---

## 📌 Business Indicators

The system monitors several important insurance business indicators.

| Indicator          | Description                    |
| ------------------ | ------------------------------ |
| Premium            | Monthly premium volume         |
| Premium Growth     | Month-to-month premium change  |
| Policies           | Number of active policies      |
| Policy Growth      | Month-to-month policy change   |
| Customers          | Number of customers            |
| Customer Growth    | Month-to-month customer change |
| Claims Ratio       | Claims divided by premium      |
| Premium per Policy | Average premium per policy     |

---

## ⚠️ Early-Warning Logic

The system assigns points when business indicators deteriorate.

### Premium Growth

* Below -10% → 30 points
* Below -5% → 15 points

### Policy Growth

* Below -10% → 25 points
* Below -5% → 12 points

### Claims Ratio

* Above 70% → 25 points
* Above 65% → 12 points

### Forecast Deviation

* Below -10% → 20 points
* Below -5% → 10 points

The resulting score determines the business health status.

---

## 🏗️ Project Architecture

```text
Insurance-business-forecasting/
│
├── data/
│   ├── raw/
│   │   └── insurance_business.csv
│   │
│   └── processed/
│       ├── model_results.csv
│       └── future_forecast.csv
│
├── models/
│   └── sarima_model.pkl
│
├── notebooks/
│   └── insurance_forecasting.ipynb
│
├── src/
│   ├── create_dataset.py
│   ├── early_warning.py
│   └── forecasting.py
│
├── screenshots/
│   ├── dashboard.png
│   ├── forecast.png
│   └── early-warning.png
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🖥️ Dashboard Preview

### Main Dashboard

![Insurance Dashboard](screenshots/dashboard.png)

### Premium Forecast

![Premium Forecast](screenshots/forecast.png)

### Early-Warning System

![Early Warning System](screenshots/early-warning.png)

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Statsmodels
* Plotly
* Streamlit
* Matplotlib
* Seaborn
* Jupyter Notebook
* Git & GitHub

---

## 📂 Dataset

The dataset contains monthly synthetic insurance business observations including:

* Date
* Premium
* Claims
* Policies
* Customers
* Premium Growth
* Policy Growth
* Customer Growth
* Claims Ratio
* Premium per Policy

The dataset covers monthly observations from **2021 to 2026**.

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/SamadhiGamagedara-sg/Insurance-business-forecasting.git
```

### 2. Navigate to the project

```bash
cd Insurance-business-forecasting
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Streamlit application

```bash
streamlit run app.py
```

---

## 💼 Business Value

The project demonstrates how machine learning and business analytics can support insurance decision-making by combining:

**Historical Data → Forecasting → KPI Monitoring → Early Warning → Business Insight**

Potential applications include:

* Premium performance monitoring
* Business growth monitoring
* Portfolio risk monitoring
* Management dashboards
* Early identification of performance deterioration
* Data-driven business planning

---

## 🔮 Future Improvements

P

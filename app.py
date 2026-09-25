import sys
import os

sys.path.append(os.path.abspath("."))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from statsmodels.tsa.statespace.sarimax import SARIMAX

from src.early_warning import calculate_warning_status


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Insurance Business Intelligence",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title(
    "📊 Insurance Business Performance Forecasting"
)

st.subheader(
    "ML-Based Forecasting & Early-Warning System"
)

st.write(
    "An analytics system for monitoring insurance business "
    "performance, forecasting premium trends, and identifying "
    "potential business slowdowns."
)


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    "data/raw/insurance_business.csv"
)

df["Date"] = pd.to_datetime(
    df["Date"]
)

df = df.sort_values("Date")


# =========================================================
# FORECASTING MODEL
# =========================================================

model = SARIMAX(
    df["Premium_Million"],
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12),
    enforce_stationarity=False,
    enforce_invertibility=False
)

result = model.fit(
    disp=False
)

forecast = result.get_forecast(
    steps=3
)

forecast_values = forecast.predicted_mean

confidence = forecast.conf_int()


future_dates = pd.date_range(
    start=df["Date"].max() + pd.DateOffset(months=1),
    periods=3,
    freq="MS"
)


# =========================================================
# CURRENT BUSINESS KPIs
# =========================================================

latest = df.iloc[-1]

current_premium = latest["Premium_Million"]

premium_growth = latest["Premium_Growth"]

claims_ratio = latest["Claims_Ratio"]

policy_growth = latest["Policy_Growth"]

customer_growth = latest["Customer_Growth"]


# =========================================================
# FORECAST DEVIATION
# =========================================================

latest_forecast = forecast_values.iloc[0]

forecast_deviation = (
    current_premium - latest_forecast
) / latest_forecast


# =========================================================
# EARLY WARNING SCORE
# =========================================================

score, status = calculate_warning_status(
    premium_growth,
    policy_growth,
    claims_ratio,
    forecast_deviation
)


# =========================================================
# KPI CARDS
# =========================================================

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Current Premium",
        f"Rs. {current_premium:.2f}M"
    )


with col2:

    st.metric(
        "Premium Growth",
        f"{premium_growth * 100:.2f}%"
    )


with col3:

    st.metric(
        "Claims Ratio",
        f"{claims_ratio * 100:.2f}%"
    )


with col4:

    if status == "NORMAL":

        icon = "🟢"

    elif status == "WATCH":

        icon = "🟡"

    else:

        icon = "🔴"

    st.metric(
        "Business Status",
        f"{icon} {status}"
    )


# =========================================================
# HISTORICAL PERFORMANCE
# =========================================================

st.divider()

st.header(
    "📈 Historical Premium Performance"
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Premium_Million"],
        mode="lines",
        name="Premium"
    )
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Premium (Million)",
    hovermode="x unified",
    height=450
)

st.plotly_chart(
    fig,
    width="stretch"
)


# =========================================================
# FORECAST
# =========================================================

st.divider()

st.header(
    "🔮 3-Month Premium Forecast"
)

forecast_fig = go.Figure()

# Historical data
forecast_fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Premium_Million"],
        mode="lines",
        name="Historical Premium"
    )
)

# Forecast
forecast_fig.add_trace(
    go.Scatter(
        x=future_dates,
        y=forecast_values,
        mode="lines+markers",
        name="Forecast"
    )
)

# Confidence interval
forecast_fig.add_trace(
    go.Scatter(
        x=list(future_dates)
        + list(future_dates[::-1]),

        y=list(confidence.iloc[:, 1])
        + list(confidence.iloc[:, 0][::-1]),

        fill="toself",

        fillcolor="rgba(100,100,200,0.15)",

        line=dict(
            color="rgba(255,255,255,0)"
        ),

        name="Confidence Interval"
    )
)

forecast_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Premium (Million)",
    hovermode="x unified",
    height=450
)

st.plotly_chart(
    forecast_fig,
    width="stretch"
)


# =========================================================
# EARLY WARNING SYSTEM
# =========================================================

st.divider()

st.header(
    "⚠️ Early-Warning System"
)

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# LEFT SIDE
# ---------------------------------------------------------

with col1:

    st.subheader(
        "Business Health"
    )

    st.metric(
        "Health Score",
        f"{score}/100"
    )

    if status == "NORMAL":

        st.success(
            "🟢 NORMAL\n\n"
            "Current indicators remain within "
            "the defined monitoring thresholds."
        )

    elif status == "WATCH":

        st.warning(
            "🟡 WATCH\n\n"
            "Some business indicators show "
            "moderate deterioration."
        )

    else:

        st.error(
            "🔴 WARNING\n\n"
            "Multiple indicators have crossed "
            "the defined warning thresholds."
        )


# ---------------------------------------------------------
# RIGHT SIDE
# ---------------------------------------------------------

with col2:

    st.subheader(
        "Monitoring Indicators"
    )

    st.write(
        f"**Premium Growth**  \n"
        f"{premium_growth * 100:.2f}%"
    )

    st.write(
        f"**Policy Growth**  \n"
        f"{policy_growth * 100:.2f}%"
    )

    st.write(
        f"**Customer Growth**  \n"
        f"{customer_growth * 100:.2f}%"
    )

    st.write(
        f"**Claims Ratio**  \n"
        f"{claims_ratio * 100:.2f}%"
    )

    st.write(
        f"**Forecast Deviation**  \n"
        f"{forecast_deviation * 100:.2f}%"
    )


# =========================================================
# FORECAST TABLE
# =========================================================

st.divider()

st.header(
    "📋 Forecast Details"
)

forecast_table = pd.DataFrame({

    "Month":
        future_dates.strftime("%Y-%m"),

    "Forecast Premium (M)":
        forecast_values.values.round(2),

    "Lower Bound (M)":
        confidence.iloc[:, 0].values.round(2),

    "Upper Bound (M)":
        confidence.iloc[:, 1].values.round(2)

})

st.dataframe(
    forecast_table,
    width="stretch"
)


# =========================================================
# BUSINESS INTERPRETATION
# =========================================================

st.divider()

st.header(
    "💡 Business Interpretation"
)

if status == "NORMAL":

    st.success(
        "Current business indicators remain within "
        "the defined monitoring thresholds."
    )

elif status == "WATCH":

    st.warning(
        "Recent business indicators show moderate "
        "deterioration and should be monitored."
    )

else:

    st.error(
        "Multiple indicators have crossed the defined "
        "early-warning thresholds and require further "
        "management attention."
    )


# =========================================================
# PROJECT INFORMATION
# =========================================================

st.divider()

st.header(
    "ℹ️ Project Information"
)

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:

    st.write(
        "**Forecasting Model**"
    )

    st.write(
        "SARIMA"
    )

with info_col2:

    st.write(
        "**Forecast Horizon**"
    )

    st.write(
        "3 Months"
    )

with info_col3:

    st.write(
        "**Monitoring Framework**"
    )

    st.write(
        "Rule-Based Early Warning"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Insurance Business Performance Forecasting & "
    "Early-Warning System | Machine Learning Portfolio Project"
)
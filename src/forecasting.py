import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


def train_forecast_model(data_path):

    df = pd.read_csv(data_path)

    df["Date"] = pd.to_datetime(df["Date"])

    df = df.sort_values("Date")

    model = SARIMAX(
        df["Premium_Million"],
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 12),
        enforce_stationarity=False,
        enforce_invertibility=False
    )

    result = model.fit(disp=False)

    forecast = result.get_forecast(steps=3)

    forecast_values = forecast.predicted_mean

    confidence = forecast.conf_int()

    future_dates = pd.date_range(
        start=df["Date"].max() + pd.DateOffset(months=1),
        periods=3,
        freq="MS"
    )

    forecast_df = pd.DataFrame({
        "Date": future_dates,
        "Forecast_Premium": forecast_values.values,
        "Lower_CI": confidence.iloc[:, 0].values,
        "Upper_CI": confidence.iloc[:, 1].values
    })

    return forecast_df
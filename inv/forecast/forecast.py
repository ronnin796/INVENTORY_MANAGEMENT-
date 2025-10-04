import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings

def forecast_sales(sales_qs, steps=7):
    """
    Run ARIMA forecast on sales queryset. Returns dict with results.
    """
    if sales_qs.count() < 2:
        return {"error": "Not enough data to forecast."}

    df = pd.DataFrame.from_records(sales_qs.values("order_date", "quantity"))
    df = df.sort_values("order_date").reset_index(drop=True)
    df["day"] = range(len(df))
    df = df.set_index("day")

    actual_sales = list(df["quantity"])

    # Validation checks
    if df["quantity"].sum() == 0 or df["quantity"].isnull().all():
        return {"error": "Sales data contains only zeros or nulls. Unable to forecast."}
    if np.ndim(df["quantity"].values) == 0:
        return {"error": "Sales data format is invalid for forecasting."}
    if len(df["quantity"].dropna()) < 3:
        return {"error": "Not enough valid data points to forecast."}

    # Forecasting
    model = ARIMA(df["quantity"], order=(1, 1, 1))
    model_fit = model.fit()
    forecast_result = model_fit.forecast(steps=steps)
    forecast_data = [max(0, val) for val in forecast_result]

    return {
        "actual_sales": actual_sales,
        "forecast_data": forecast_data,
        "forecast_labels": [f"Day {i+1}" for i in range(len(actual_sales) + len(forecast_data))],




    }




def forecast_sales_safe(sales_qs, steps=7):
    """
    Run ARIMA forecast safely. Returns empty list if not enough data.
    """
    import warnings
    import pandas as pd
    from statsmodels.tsa.arima.model import ARIMA

    df = pd.DataFrame.from_records(sales_qs.values("order_date", "quantity"))
    # Early exit if not enough data
    if df.empty or len(df) < 2 or df['quantity'].sum() == 0 or df['quantity'].isnull().all():
        return {"forecast_data": []}  # treat as safe

    df = df.sort_values("order_date").reset_index(drop=True)
    df['day'] = range(len(df))
    df = df.set_index('day')

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")  # suppress statsmodels warnings
        try:
            model = ARIMA(df['quantity'], order=(1, 1, 1))
            model_fit = model.fit()
            forecast_result = model_fit.forecast(steps=steps)
            forecast_data = [max(0, val) for val in forecast_result]
        except Exception:
            # Fallback if ARIMA fails for some reason
            forecast_data = []

    return {"forecast_data": forecast_data}

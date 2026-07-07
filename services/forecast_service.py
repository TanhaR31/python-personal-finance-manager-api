from collections import defaultdict
from datetime import date, datetime
import numpy as np
import pandas as pd

try:
    from sklearn.linear_model import LinearRegression
    SKLEARN = True
except Exception:
    SKLEARN = False

def month_key(d: date):
    return d.strftime("%Y-%m")

def add_month(d: date):
    y = d.year + (d.month // 12)
    m = d.month % 12 + 1
    return date(y, m, 1)

def forecast_income(incomes, n_months=3):
    if not incomes:
        return {"history": [], "forecast": []}

    monthly = defaultdict(float)
    for inc in incomes:
        monthly[month_key(inc.date)] += inc.amount

    months_sorted = sorted(monthly.keys())
    df = pd.DataFrame({"month": months_sorted, "income": [monthly[m] for m in months_sorted]})
    X = np.arange(len(df)).reshape(-1, 1)
    y = np.array(df["income"], dtype=float).reshape(-1, 1)

    if len(X) >= 2:
        if SKLEARN:
            model = LinearRegression()
            model.fit(X, y)
            predict = lambda x: float(model.predict(np.array([[x]]))[0, 0])
        else:
            slope, intercept = np.polyfit(X.flatten(), y.flatten(), 1)
            predict = lambda x: float(slope * x + intercept)
    else:
        last_val = float(y[-1, 0])
        predict = lambda x: last_val

    history = [{"month": row["month"], "income": float(row["income"])} for _, row in df.iterrows()]

    last_index = len(df) - 1
    last_month_dt = datetime.strptime(df["month"].iloc[-1] + "-01", "%Y-%m-%d").date()

    forecast = []
    current = add_month(last_month_dt)
    for i in range(1, n_months + 1):
        x_index = last_index + i
        pred = max(0.0, float(predict(x_index)))
        forecast.append({"month": current.strftime("%Y-%m"), "predicted_income": pred})
        current = add_month(current)

    return {"history": history, "forecast": forecast}

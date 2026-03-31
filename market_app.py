import streamlit as st
import pandas as pd
import yfinance as yf
import datetime as dt

st.title("Market Snapshot Tool 📊")

# -------------------
# USER INPUTS
# -------------------
date_input = st.date_input("Select Date", value=dt.date(2026, 3, 24))

tickers_input = st.text_area(
    "Paste tickers (space or comma separated)",
    "AAPL AMZN MSFT GOOG GOOGL JNJ"
)

run = st.button("Run Report")

# -------------------
# PROCESS
# -------------------
if run:
    tickers = [t.strip().upper() for t in tickers_input.replace(",", " ").split()]

    start = date_input - dt.timedelta(days=5)
    end = date_input + dt.timedelta(days=1)

    data = yf.download(
        tickers,
        start=start,
        end=end,
        group_by="ticker",
        auto_adjust=False,
        threads=True
    )

    rows = []

    for t in tickers:
        try:
            if t not in data.columns.levels[0]:
                continue

            df = data[t].dropna()
            df.index = pd.to_datetime(df.index)

            day = df[df.index.date == date_input]

            if day.empty:
                continue

            r = day.iloc[0]

            rows.append({
                "Ticker": t,
                "High/NAV": r.get("High", r.get("Close")),
                "Low": r.get("Low"),
                "Close": r.get("Close")
            })

        except:
            continue

    df_out = pd.DataFrame(rows)

    st.dataframe(df_out)

    file_name = "market_snapshot.xlsx"
    df_out.to_excel(file_name, index=False)

    with open(file_name, "rb") as f:
        st.download_button(
            "Download Excel",
            f,
            file_name=file_name
        )
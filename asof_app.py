"""A small FRED/ALFRED point-in-time viewer for Lab 17.

Run from this folder with: streamlit run asof_app.py
"""

from __future__ import annotations

from datetime import date
from io import StringIO

import altair as alt
import pandas as pd
import requests
import streamlit as st


FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
ALFRED_URL = "https://alfred.stlouisfed.org/graph/alfredgraph.csv"
DEFAULT_SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}


def _read_series_csv(response_text: str, series_id: str) -> pd.DataFrame:
    """Convert a FRED-style CSV to a clean date/value table.

    A period (.) is FRED's marker for an observation that is not available.
    """
    raw = pd.read_csv(StringIO(response_text), na_values=".")
    date_column = next(
        (column for column in raw.columns if column.strip().lower() in {"date", "observation_date"}),
        None,
    )
    if raw.empty or date_column is None:
        raise ValueError("FRED did not return a usable DATE column.")

    value_column = series_id.upper() if series_id.upper() in raw.columns else None
    if value_column is None:
        candidates = [column for column in raw.columns if column != date_column]
        if len(candidates) != 1:
            raise ValueError("FRED did not return a usable value column.")
        value_column = candidates[0]

    result = raw.loc[:, [date_column, value_column]].rename(
        columns={date_column: "DATE", value_column: "value"}
    )
    result["DATE"] = pd.to_datetime(result["DATE"], errors="coerce")
    result["value"] = pd.to_numeric(result["value"], errors="coerce")
    result = result.dropna(subset=["DATE", "value"]).sort_values("DATE")
    return result.reset_index(drop=True)


@st.cache_data(ttl=3600, show_spinner=False)
def download_today(series_id: str) -> pd.DataFrame:
    """Download the current FRED values for one series."""
    response = requests.get(FRED_URL, params={"id": series_id}, timeout=30)
    response.raise_for_status()
    return _read_series_csv(response.text, series_id)


@st.cache_data(ttl=3600, show_spinner=False)
def download_as_known_on(series_id: str, vintage_date: str) -> pd.DataFrame:
    """Download the ALFRED vintage that was available on ``vintage_date``."""
    response = requests.get(
        ALFRED_URL,
        params={"id": series_id, "vintage_date": vintage_date},
        timeout=30,
    )
    response.raise_for_status()
    return _read_series_csv(response.text, series_id)


def last_observation(frame: pd.DataFrame) -> pd.Series:
    """Return the latest non-missing observation in a clean series table."""
    return frame.iloc[-1]


def display_date(value: date | pd.Timestamp) -> str:
    """Format a date without platform-specific ``strftime`` flags."""
    stamp = pd.Timestamp(value)
    return f"{stamp:%B} {stamp.day}, {stamp.year}"


def point_in_time_row(
    series_id: str, vintage: pd.DataFrame, current: pd.DataFrame
) -> dict[str, object]:
    """Summarize publication lag and revisions for the results table."""
    known_last = last_observation(vintage)
    current_last = last_observation(current)
    known_date = pd.Timestamp(known_last["DATE"])

    current_after_known = int((current["DATE"] > known_date).sum())
    matched = vintage.merge(current, on="DATE", how="inner", suffixes=("_then", "_today"))
    revised = int((matched["value_then"] != matched["value_today"]).sum())

    return {
        "Series ID": f"https://fred.stlouisfed.org/series/{series_id}",
        "Last date known then": known_date.date(),
        "Value known then": float(known_last["value"]),
        "Last date measured today": pd.Timestamp(current_last["DATE"]).date(),
        "Value today": float(current_last["value"]),
        "Today's values after then": current_after_known,
        "Revised shared dates": revised,
    }


def main() -> None:
    st.set_page_config(page_title="Point-in-Time Rates", layout="wide")
    st.title("Point-in-Time Rates")
    st.caption(
        "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, "
        f"downloaded {display_date(date.today())}; built with AI help, a learning "
        "demonstration, not investment advice."
    )

    st.sidebar.header("Controls")
    selected = st.sidebar.multiselect(
        "Series IDs",
        options=list(DEFAULT_SERIES),
        default=list(DEFAULT_SERIES),
        format_func=lambda item: f"{item} — {DEFAULT_SERIES[item]}",
    )
    extra = st.sidebar.text_input("Add another FRED series ID", placeholder="Example: PAYEMS")
    if extra.strip():
        selected.append(extra.strip().upper())
    # Preserve choice order while avoiding a duplicate download.
    selected = list(dict.fromkeys(selected))

    start_date = st.sidebar.date_input("Start date", value=date(2020, 1, 1))
    as_known_on = st.sidebar.date_input("As known on", value=date.today())
    comparison_type = st.sidebar.selectbox(
        "Combined comparison chart", options=["Line chart", "Bar chart"]
    )
    vintage_date = as_known_on.isoformat()

    if not selected:
        st.info("Select a series or add a FRED series ID in the sidebar.")
        return

    rows: list[dict[str, object]] = []
    comparison_frames: list[pd.DataFrame] = []
    for series_id in selected:
        try:
            current = download_today(series_id)
            vintage = download_as_known_on(series_id, vintage_date)
            current_from_start = current.loc[current["DATE"].dt.date >= start_date]

            st.subheader(series_id if series_id not in DEFAULT_SERIES else f"{series_id} — {DEFAULT_SERIES[series_id]}")
            if current_from_start.empty:
                st.warning(f"{series_id}: no current observations on or after {start_date}.")
            else:
                st.line_chart(current_from_start.set_index("DATE")["value"], use_container_width=True)
                comparison_frames.append(
                    current_from_start.assign(series_id=series_id).loc[:, ["DATE", "series_id", "value"]]
                )
            known_last = last_observation(vintage)
            st.caption(
                f"Last date in data known on {display_date(as_known_on)}: "
                f"{display_date(known_last['DATE'])} — {known_last['value']:,.3f}"
            )
            rows.append(point_in_time_row(series_id, vintage, current))
        except (requests.RequestException, ValueError, pd.errors.ParserError, IndexError) as error:
            st.error(f"{series_id}: {error}")

    if rows:
        table = pd.DataFrame(rows)
        st.subheader("Point-in-time audit")
        st.dataframe(
            table,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Series ID": st.column_config.LinkColumn(
                    "Series ID", display_text=r".*/series/(.*)$"
                ),
                "Value known then": st.column_config.NumberColumn(format="%.3f"),
                "Value today": st.column_config.NumberColumn(format="%.3f"),
            },
        )

    if comparison_frames:
        comparison = pd.concat(comparison_frames, ignore_index=True).pivot(
            index="DATE", columns="series_id", values="value"
        )
        comparison_long = (
            comparison.rename_axis("DATE")
            .reset_index()
            .melt(id_vars="DATE", var_name="Series", value_name="Value")
            .dropna(subset=["Value"])
        )
        series_order = list(comparison.columns)
        color_scale = alt.Scale(domain=series_order, scheme="tableau10")
        tooltip = [
            alt.Tooltip("DATE:T", title="Date", format="%b %d, %Y"),
            alt.Tooltip("Series:N", title="Series"),
            alt.Tooltip("Value:Q", title="Value", format=".3f"),
        ]
        st.subheader("Combined rate comparison")
        st.caption(
            "All successfully downloaded selected series, using today’s FRED values from the start date. "
            "Compare levels carefully because the series have different frequencies and definitions."
        )
        if comparison_type == "Line chart":
            chart = (
                alt.Chart(comparison_long)
                .mark_line(point=True)
                .encode(
                    x=alt.X("DATE:T", title="Date"),
                    y=alt.Y("Value:Q", title="Rate / value"),
                    color=alt.Color("Series:N", scale=color_scale, legend=alt.Legend(title="Series")),
                    tooltip=tooltip,
                )
                .properties(height=420)
                .interactive()
            )
        else:
            # DGS10 is daily while the other defaults are monthly or weekly.
            # Keep the last available value for each series/month so the bar
            # chart is a readable set of four side-by-side bars, not a dense
            # band of daily bars.
            bar_data = (
                comparison_long.assign(Month=comparison_long["DATE"].dt.to_period("M"))
                .sort_values("DATE")
                .groupby(["Month", "Series"], as_index=False)
                .last()
            )
            bar_data["Month"] = bar_data["Month"].dt.to_timestamp()
            bar_data["Month label"] = bar_data["Month"].astype(str)
            chart = (
                alt.Chart(bar_data)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "Month label:N",
                        title="Month (last available observation)",
                        sort=alt.EncodingSortField(field="Month", order="ascending"),
                    ),
                    xOffset=alt.XOffset("Series:N", sort=series_order),
                    y=alt.Y("Value:Q", title="Rate / value"),
                    color=alt.Color("Series:N", scale=color_scale, legend=alt.Legend(title="Series")),
                    tooltip=[
                        alt.Tooltip("Month label:N", title="Month"),
                        alt.Tooltip("Series:N", title="Series"),
                        alt.Tooltip("Value:Q", title="Last value", format=".3f"),
                    ],
                )
                .properties(height=420)
                .interactive()
            )
        st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    main()

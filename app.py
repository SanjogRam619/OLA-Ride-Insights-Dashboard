import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="OLA Ride Insights Dashboard",
    page_icon="🚖",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
.main{
    background-color:#F5F7FA;
}
[data-testid="stSidebar"]{
    background-color:#111827;
}
[data-testid="stSidebar"] *{
    color:white;
}
h1{
    color:#111827;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("ola.xlsx", sheet_name="July")

df = load_data()

# ---------------------------------------------------
# CLEAN DATA
# ---------------------------------------------------
df["Booking_Status"] = df["Booking_Status"].fillna("").astype(str).str.strip()
df["Payment_Method"] = df["Payment_Method"].fillna("").astype(str).str.strip()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.image("ola image.jpeg", width=180)
st.sidebar.title("🔍 Dashboard Filters")

vehicle = st.sidebar.multiselect(
    "🚗 Vehicle Type",
    options=sorted(df["Vehicle_Type"].dropna().unique()),
    default=sorted(df["Vehicle_Type"].dropna().unique())
)

status = st.sidebar.multiselect(
    "📋 Booking Status",
    options=sorted(df["Booking_Status"].dropna().unique()),
    default=sorted(df["Booking_Status"].dropna().unique())
)

payment = st.sidebar.multiselect(
    "💳 Payment Method",
    options=["Cash", "UPI", "Credit Card", "Debit Card"],
    default=["Cash", "UPI", "Credit Card", "Debit Card"]
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------
filtered_df = df[
    (df["Vehicle_Type"].isin(vehicle)) &
    (df["Booking_Status"].isin(status))
]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
logo_col, title_col = st.columns([1,5])

with logo_col:
    st.image("ola image.jpeg", width=140)

with title_col:
    st.markdown(
        "<h1 style='padding-top:15px;'>OLA Ride Insights Dashboard</h1>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
total_bookings = len(filtered_df)
revenue = filtered_df["Booking_Value"].sum()
avg_distance = filtered_df["Ride_Distance"].mean()
avg_rating = filtered_df["Customer_Rating"].mean()

k1, k2, k3, k4 = st.columns(4)

k1.metric("🚖 Total Bookings", f"{total_bookings:,}")
k2.metric("💰 Revenue", f"₹{revenue:,.0f}")
k3.metric("📍 Avg Distance", f"{avg_distance:.2f} km")
k4.metric("⭐ Avg Rating", f"{avg_rating:.2f}")

st.markdown("---")

# ---------------------------------------------------
# CHART ROW 1
# ---------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    booking_chart = px.pie(
        filtered_df,
        names="Booking_Status",
        hole=0.55,
        title="Booking Status Distribution",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(booking_chart, use_container_width=True)

with c2:
    vehicle_revenue = (
        filtered_df.groupby("Vehicle_Type")["Booking_Value"]
        .sum()
        .reset_index()
    )

    vehicle_chart = px.bar(
        vehicle_revenue,
        x="Vehicle_Type",
        y="Booking_Value",
        color="Vehicle_Type",
        title="Revenue by Vehicle Type",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    st.plotly_chart(vehicle_chart, use_container_width=True)

# ---------------------------------------------------
# CHART ROW 2
# ---------------------------------------------------
c3, c4 = st.columns(2)

with c3:
    pickup = (
        filtered_df["Pickup_Location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    pickup.columns = ["Location", "Count"]

    pickup_chart = px.bar(
        pickup,
        x="Count",
        y="Location",
        orientation="h",
        title="Top 10 Pickup Locations",
        color="Count"
    )

    st.plotly_chart(pickup_chart, use_container_width=True)

with c4:
    drop = (
        filtered_df["Drop_Location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    drop.columns = ["Location", "Count"]

    drop_chart = px.bar(
        drop,
        x="Count",
        y="Location",
        orientation="h",
        title="Top 10 Drop Locations",
        color="Count"
    )

    st.plotly_chart(drop_chart, use_container_width=True)

# ---------------------------------------------------
# CHART ROW 3
# ---------------------------------------------------
c5, c6 = st.columns(2)

with c5:
    cancel_df = filtered_df[
        filtered_df["Booking_Status"] != "Success"
    ]

    cancel_chart = px.pie(
        cancel_df,
        names="Booking_Status",
        title="Ride Cancellation Analysis",
        color_discrete_sequence=px.colors.qualitative.Dark24
    )

    st.plotly_chart(cancel_chart, use_container_width=True)

with c6:
    payment_df = filtered_df[
        filtered_df["Payment_Method"].isin(
            ["Cash", "UPI", "Credit Card", "Debit Card"]
        )
    ]

    payment_chart = px.pie(
        payment_df,
        names="Payment_Method",
        hole=0.65,
        title="Payment Method Distribution",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    st.plotly_chart(payment_chart, use_container_width=True)

# ---------------------------------------------------
# KEY INSIGHTS
# ---------------------------------------------------
st.markdown("---")
st.subheader("📈 Key Business Insights")

try:
    top_vehicle = (
        filtered_df.groupby("Vehicle_Type")["Booking_Value"]
        .sum()
        .idxmax()
    )

    top_pickup = (
        filtered_df["Pickup_Location"]
        .value_counts()
        .idxmax()
    )

    top_payment = (
        payment_df["Payment_Method"]
        .value_counts()
        .idxmax()
    )

    st.success(f"🚗 Highest Revenue Vehicle Type: {top_vehicle}")
    st.info(f"📍 Most Popular Pickup Location: {top_pickup}")
    st.info(f"💳 Most Preferred Payment Method: {top_payment}")

except:
    st.warning("No data available for selected filters.")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")

st.markdown("""
<div style='text-align:center;padding:20px;font-size:16px;color:gray;'>
🚖 OLA Ride Insights Dashboard
<br><br>
Built by <b>Sanjog Ram</b>
<br><br>
SQL • Power BI • Python • Streamlit • Plotly
</div>
""", unsafe_allow_html=True)

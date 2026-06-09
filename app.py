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

.kpi-box{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.15);
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
# SIDEBAR
# ---------------------------------------------------
st.sidebar.image("ola image.jpeg", width=180)
st.sidebar.title("Dashboard Filters")

vehicle = st.sidebar.multiselect(
    "Vehicle Type",
    options=sorted(df["Vehicle_Type"].dropna().unique()),
    default=sorted(df["Vehicle_Type"].dropna().unique())
)

status = st.sidebar.multiselect(
    "Booking Status",
    options=sorted(df["Booking_Status"].dropna().unique()),
    default=sorted(df["Booking_Status"].dropna().unique())
)

payment = st.sidebar.multiselect(
    "Payment Method",
    options=sorted(df["Payment_Method"].dropna().unique()),
    default=sorted(df["Payment_Method"].dropna().unique())
)

filtered_df = df[
    (df["Vehicle_Type"].isin(vehicle)) &
    (df["Booking_Status"].isin(status)) &
    (df["Payment_Method"].isin(payment))
]

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
logo_col, title_col = st.columns([1,5])

with logo_col:
    st.image("ola image.jpeg", width=140)

with title_col:
    st.markdown("""
    <h1 style='padding-top:15px;'>
    OLA Ride Insights Dashboard
    </h1>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# KPIs
# ---------------------------------------------------
total_bookings = len(filtered_df)

revenue = filtered_df["Booking_Value"].sum()

avg_distance = filtered_df["Ride_Distance"].mean()

avg_rating = filtered_df["Customer_Rating"].mean()

success_rate = (
filtered_df["Booking_Status"]
.eq("Success")
.mean() * 100
)

cancel_rate = 100 - success_rate

k1,k2,k3,k4 = st.columns(4)

k1.metric("🚖 Total Bookings", f"{total_bookings:,}")
k2.metric("💰 Revenue", f"₹{revenue:,.0f}")
k3.metric("📍 Avg Distance", f"{avg_distance:.2f} km")
k4.metric("⭐ Avg Rating", f"{avg_rating:.2f}")

k5,k6 = st.columns(2)

k5.metric("✅ Success Rate", f"{success_rate:.2f}%")
k6.metric("❌ Cancellation Rate", f"{cancel_rate:.2f}%")

st.markdown("---")

# ---------------------------------------------------
# CHART ROW 1
# ---------------------------------------------------
c1,c2 = st.columns(2)

with c1:

    booking_chart = px.pie(
        filtered_df,
        names="Booking_Status",
        hole=0.55,
        title="Booking Status Distribution",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    st.plotly_chart(
        booking_chart,
        use_container_width=True
    )

with c2:

    vehicle_revenue = (
        filtered_df
        .groupby("Vehicle_Type")["Booking_Value"]
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

    st.plotly_chart(
        vehicle_chart,
        use_container_width=True
    )

# ---------------------------------------------------
# CHART ROW 2
# ---------------------------------------------------
c3,c4 = st.columns(2)

with c3:

    pickup = (
        filtered_df["Pickup_Location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    pickup.columns = ["Location","Count"]

    pickup_chart = px.bar(
        pickup,
        x="Count",
        y="Location",
        orientation="h",
        title="Top 10 Pickup Locations",
        color="Count"
    )

    st.plotly_chart(
        pickup_chart,
        use_container_width=True
    )

with c4:

    drop = (
        filtered_df["Drop_Location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    drop.columns = ["Location","Count"]

    drop_chart = px.bar(
        drop,
        x="Count",
        y="Location",
        orientation="h",
        title="Top 10 Drop Locations",
        color="Count"
    )

    st.plotly_chart(
        drop_chart,
        use_container_width=True
    )

# ---------------------------------------------------
# CHART ROW 3
# ---------------------------------------------------
c5,c6 = st.columns(2)

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

    st.plotly_chart(
        cancel_chart,
        use_container_width=True
    )

with c6:

    payment_chart = px.pie(
        filtered_df,
        names="Payment_Method",
        hole=0.65,
        title="Payment Method Distribution",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    st.plotly_chart(
        payment_chart,
        use_container_width=True
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")

st.markdown(
"""
<center>

### 🚖 OLA Ride Insights Dashboard

Built using Streamlit • Python • Plotly

</center>
""",
unsafe_allow_html=True
)

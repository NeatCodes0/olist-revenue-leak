import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Olist Revenue Leak Analysis", layout="wide")

# --- Custom CSS for a cleaner look (Works in Light & Dark mode) ---
st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    h1 {color: #1E3A8A; font-size: 2.5rem; font-weight: 700;}
    h3 {color: #4B5563; font-size: 1.2rem; font-weight: 500;}
    /* Professional KPI styling */
    div[data-testid="stMetric"] {
        background-color: rgba(30, 58, 138, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.5rem solid #1E3A8A;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Olist Revenue Leak Analysis")
st.markdown("### Quantifying the impact of poor first experiences on customer retention and revenue")

# --- Database Connection ---
@st.cache_data
def get_data():
    con = duckdb.connect("data/olist.duckdb", read_only=True)
    
    # 1. Headline KPIs (FIXED: Added the review logic back in)
    kpi_query = """
        WITH customer_orders AS (
            SELECT c.customer_unique_id, o.order_id,
                CASE WHEN DATEDIFF('day', o.order_estimated_delivery_date, o.order_delivered_customer_date) > 0 THEN 1 ELSE 0 END AS was_late,
                ROW_NUMBER() OVER (PARTITION BY c.customer_unique_id ORDER BY o.order_purchase_timestamp ASC) AS order_seq
            FROM raw_orders o
            JOIN raw_customers c ON o.customer_id = c.customer_id
            WHERE o.order_status = 'delivered'
        ),
        customer_summary AS (
            SELECT co.customer_unique_id, COUNT(co.order_id) AS total_orders,
                MAX(CASE WHEN co.order_seq = 1 THEN co.was_late ELSE 0 END) AS first_was_late,
                MAX(CASE WHEN co.order_seq = 1 THEN r.review_score ELSE NULL END) AS first_review,
                MAX(CASE WHEN co.order_seq = 1 THEN co.order_id ELSE NULL END) AS first_order_id
            FROM customer_orders co
            LEFT JOIN raw_order_reviews r ON co.order_id = r.order_id
            GROUP BY 1
        ),
        order_revenue AS (
            SELECT order_id, SUM(payment_value) AS order_value FROM raw_order_payments GROUP BY 1
        )
        SELECT 
            COUNT(cs.customer_unique_id) AS lost_customers,
            ROUND(SUM(orv.order_value), 2) AS revenue_at_risk,
            (SELECT COUNT(DISTINCT customer_unique_id) FROM raw_customers) AS total_customers
        FROM customer_summary cs
        LEFT JOIN order_revenue orv ON cs.first_order_id = orv.order_id
        WHERE cs.total_orders = 1 
          AND (cs.first_was_late = 1 OR cs.first_review = 1);
    """
    kpi_df = con.execute(kpi_query).fetchdf()
    
    # 2. Review Scores (Late vs On-time)
    review_query = """
        WITH delivered_orders AS (
            SELECT order_id, DATEDIFF('day', order_estimated_delivery_date, order_delivered_customer_date) AS delay_days
            FROM raw_orders WHERE order_status = 'delivered' AND order_delivered_customer_date IS NOT NULL
        )
        SELECT 
            CASE WHEN delay_days > 0 THEN 'Late' ELSE 'On Time' END AS "Delivery Status",
            ROUND(AVG(r.review_score), 2) AS "Average Review Score"
        FROM delivered_orders o
        LEFT JOIN raw_order_reviews r ON o.order_id = r.order_id
        GROUP BY 1
    """
    review_df = con.execute(review_query).fetchdf()
    
    # 3. Retention Rates (Late vs On-time)
    retention_query = """
        WITH customer_orders AS (
            SELECT c.customer_unique_id, o.order_id,
                CASE WHEN DATEDIFF('day', o.order_estimated_delivery_date, o.order_delivered_customer_date) > 0 THEN 1 ELSE 0 END AS was_late,
                ROW_NUMBER() OVER (PARTITION BY c.customer_unique_id ORDER BY o.order_purchase_timestamp ASC) AS order_seq
            FROM raw_orders o
            JOIN raw_customers c ON o.customer_id = c.customer_id
            WHERE o.order_status = 'delivered'
        ),
        customer_summary AS (
            SELECT customer_unique_id, COUNT(order_id) AS total_orders,
                MAX(CASE WHEN order_seq = 1 THEN was_late ELSE 0 END) AS first_was_late
            FROM customer_orders GROUP BY 1
        )
        SELECT 
            CASE WHEN first_was_late = 1 THEN 'Late' ELSE 'On Time' END AS "First Order Status",
            ROUND(100.0 * SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END) / COUNT(customer_unique_id), 2) AS "Repeat Purchase Rate (%)"
        FROM customer_summary
        GROUP BY 1
    """
    retention_df = con.execute(retention_query).fetchdf()
    
    con.close()
    return kpi_df, review_df, retention_df

# --- Load Data ---
kpi_df, review_df, retention_df = get_data()

# --- Layout: KPIs ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Customers Analyzed", value=f"{int(kpi_df['total_customers'][0]):,}")
with col2:
    st.metric(label="Lost Customers (Bad First Experience)", value=f"{int(kpi_df['lost_customers'][0]):,}")
with col3:
    st.metric(label="Revenue at Risk (BRL)", value=f"R$ {kpi_df['revenue_at_risk'][0]:,.2f}")

st.divider()

# --- Layout: Charts ---
st.markdown("### Operational Impact")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("**Impact of Late Delivery on Review Scores**")
    fig1 = px.bar(
        review_df, 
        x="Delivery Status", 
        y="Average Review Score",
        color="Delivery Status",
        color_discrete_map={"On Time": "#10B981", "Late": "#EF4444"},
        text_auto=True
    )
    fig1.update_layout(showlegend=False, yaxis_range=[0, 5], margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    st.markdown("**Impact of Late Delivery on Retention**")
    fig2 = px.bar(
        retention_df, 
        x="First Order Status", 
        y="Repeat Purchase Rate (%)",
        color="First Order Status",
        color_discrete_map={"On Time": "#10B981", "Late": "#EF4444"},
        text_auto=True
    )
    fig2.update_layout(showlegend=False, margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- Executive Summary ---
st.markdown("### Executive Summary")
st.info("""
**The Problem:** 
While 97% of orders are successfully delivered, the overall repeat purchase rate is severely low (~3%). 

**The Driver:** 
A late delivery crushes the customer experience. On-time orders average a 4.29 review score, but late orders crash to a 2.27, with over 52% of late orders receiving a 1-star review. 

**The Financial Impact:** 
We estimate that **11,735 customers** churned because their first experience was late or received a 1-star review. The total revenue at risk from these lost customers is **R$ 2,210,179.89**.
""")
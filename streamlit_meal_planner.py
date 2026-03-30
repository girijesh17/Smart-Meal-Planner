import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Page Configuration ---
st.set_page_config(
    page_title="Meal Planner",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }

    .day-card {
        background: rgba(255,255,255,0.85);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
        border-left: 5px solid #4CAF50;
        box-shadow: 2px 4px 12px rgba(0,0,0,0.08);
    }
    .day-card.nonveg { border-left-color: #e74c3c; }

    .meal-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #888;
    }
    .meal-name { font-size: 15px; font-weight: 700; color: #2c3e50; }
    .meal-meta { font-size: 12px; color: #999; margin-top: 2px; }

    h1 { color: #2c3e50; font-weight: 700; text-align: center; }

    .stDownloadButton>button {
        background: linear-gradient(135deg, #4CAF50, #2196F3);
        color: white; border: none; border-radius: 8px;
        padding: 8px 20px; font-weight: 600;
        transition: all 0.3s ease;
    }
    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(76,175,80,0.4);
    }
    </style>
""", unsafe_allow_html=True)


# --- Load Dataset ---
@st.cache_data
def load_data():
    for v in ["food_dataset_v6.csv", "food_dataset_v5.csv", "food_dataset_v4.csv"]:
        try:
            return pd.read_csv(v)
        except FileNotFoundError:
            continue
    return pd.DataFrame()

df = load_data()


# --- Scoring helper ---
def score_and_plan(df_raw, meal_type, diet_type, preference, budget, week_seed):
    if diet_type == "Both (Veg + Non-Veg)":
        df_f = df_raw[df_raw["MealType"]==meal_type].copy()
    else:
        df_f = df_raw[(df_raw["MealType"]==meal_type) & (df_raw["DietType"]==diet_type)].copy()
    if df_f.empty:
        return pd.DataFrame()

    df_f["Calories_norm"] = df_f["Calories"] / df_f["Calories"].max()
    df_f["Protein_norm"]  = df_f["Protein"]  / df_f["Protein"].max()
    df_f["Price_norm"]    = df_f["Price"]     / df_f["Price"].max()

    if preference == "Healthy":
        df_f["Score"] = 0.5*df_f["Protein_norm"] + 0.3*(1-df_f["Calories_norm"]) + 0.2*(1-df_f["Price_norm"])
    elif preference == "Cheap":
        df_f["Score"] = 0.6*(1-df_f["Price_norm"]) + 0.2*df_f["Protein_norm"] + 0.2*(1-df_f["Calories_norm"])
    else:
        df_f["Score"] = 0.6*df_f["Protein_norm"] + 0.2*(1-df_f["Price_norm"]) + 0.2*(1-df_f["Calories_norm"])

    df_scored = df_f.sort_values("Score", ascending=False)
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    plan, used, rem_budget = [], set(), budget

    for day in days:
        suitable = df_scored[~df_scored['Food'].isin(used)]
        found = False
        for _, row in suitable.iterrows():
            if rem_budget - row['Price'] >= 0:
                entry = row.to_dict()
                entry['Day'] = day
                plan.append(entry)
                used.add(row['Food'])
                rem_budget -= row['Price']
                found = True
                break
        if not found:
            cheapest = df_f.sort_values("Price").iloc[0].to_dict()
            cheapest['Day'] = day
            plan.append(cheapest)

    return pd.DataFrame(plan)


def download_df(plan_df, label="Meal Plan"):
    cols = ["Day","Food","Calories","Protein","Fat","Price"]
    available = [c for c in cols if c in plan_df.columns]
    return plan_df[available].to_csv(index=False).encode('utf-8')


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/000000/restaurant.png", width=70)
    st.header("Plan Your Week")

    with st.expander("🍽️ Meal Settings", expanded=True):
        view_mode = st.radio("View Mode", ["📅 Single Category", "🗓️ Overall Day View (All Meals)"], index=0)
        meal_type = "Breakfast"
        if "Single" in view_mode:
            meal_type = st.selectbox("Meal Category", ["Breakfast","Lunch","Dinner","Snacks","Fast Food"])
        diet_type = st.radio("Diet Preference", ["Veg", "Non-Veg", "Both (Veg + Non-Veg)"], horizontal=False)
        preference = st.segmented_control("Goal", ["Healthy","Cheap","High Protein"], selection_mode="single", default="Healthy")

    with st.expander("💰 Budget & Week", expanded=True):
        budget = st.slider("Weekly Budget (₹)", 300, 10000, 3000, step=100)
        week_number = st.selectbox("Planning for", ["Week 1","Week 2","Week 3","Week 4"])

    st.info("💡 Enjaayungal! Try **Overall Day View** to see your Breakfast, Lunch & Dinner together!")

week_seed = int(week_number.split()[1])
days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

# ============================================================
# MAIN CONTENT
# ============================================================
st.markdown("<h1>🍛 Meal Planner</h1>", unsafe_allow_html=True)

# ====== OVERALL DAY VIEW ======
if "Overall" in view_mode:
    st.write("")
    budget_per_meal = budget // 3

    plan_b = score_and_plan(df, "Breakfast", diet_type, preference, budget_per_meal, week_seed)
    plan_l = score_and_plan(df, "Lunch",     diet_type, preference, budget_per_meal, week_seed+1)
    plan_d = score_and_plan(df, "Dinner",    diet_type, preference, budget_per_meal, week_seed+2)

    all_plan = pd.DataFrame()
    if not plan_b.empty:
        plan_b["Meal"] = "Breakfast"
    if not plan_l.empty:
        plan_l["Meal"] = "Lunch"
    if not plan_d.empty:
        plan_d["Meal"] = "Dinner"
    all_plan = pd.concat([plan_b, plan_l, plan_d], ignore_index=True)

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Total Weekly Cost", f"₹{all_plan['Price'].sum()}")
    with m2: st.metric("Total Calories",    f"{all_plan['Calories'].sum()} kcal")
    with m3: st.metric("Total Protein",     f"{all_plan['Protein'].sum()}g")
    with m4:
        csv_all = download_df(all_plan, "All Meals")
        st.download_button("📥 Download Full Plan", data=csv_all,
                           file_name=f"full_meal_plan_{week_number}.csv", mime="text/csv")

    st.markdown("---")

    # Day-by-day view
    for day in days:
        st.markdown(f"### 📆 {day}")
        d_b = plan_b[plan_b["Day"]==day].iloc[0] if not plan_b.empty and day in plan_b["Day"].values else None
        d_l = plan_l[plan_l["Day"]==day].iloc[0] if not plan_l.empty and day in plan_l["Day"].values else None
        d_d = plan_d[plan_d["Day"]==day].iloc[0] if not plan_d.empty and day in plan_d["Day"].values else None

        c1, c2, c3 = st.columns(3)

        def render_card(col, label, row, emoji):
            with col:
                if row is not None:
                    card_class = "day-card" if row.get("DietType","Veg")=="Veg" else "day-card nonveg"
                    st.markdown(f"""
                    <div class="{card_class}">
                        <div class="meal-label">{emoji} {label}</div>
                        <div class="meal-name">{row['Food']}</div>
                        <div class="meal-meta">🔥 {row['Calories']} kcal &nbsp;|&nbsp; 🥩 {row['Protein']}g protein &nbsp;|&nbsp; 💰 ₹{row['Price']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='day-card'><div class='meal-label'>{emoji} {label}</div><div class='meal-name'>—</div></div>", unsafe_allow_html=True)

        render_card(c1, "Breakfast", d_b, "☀️")
        render_card(c2, "Lunch",     d_l, "🌤️")
        render_card(c3, "Dinner",    d_d, "🌙")

    # Summary table
    with st.expander("📋 Full Data Table", expanded=False):
        st.dataframe(all_plan[["Day","Meal","Food","Calories","Protein","Fat","Price"]],
                     use_container_width=True, hide_index=True)

# ====== SINGLE CATEGORY VIEW ======
else:
    plan_df = score_and_plan(df, meal_type, diet_type, preference, budget, week_seed)

    if plan_df.empty:
        st.error("No foods found for the selected combination. Please try different filters.")
        st.stop()

    tab1, tab2, tab3 = st.tabs(["📅 Weekly Schedule", "📊 Nutritional Analysis", "🍪 Extra Treats"])

    with tab1:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 📋 {meal_type} Plan — {week_number}")
        with col2:
            csv = download_df(plan_df, meal_type)
            st.download_button(label="📥 Download Chart", data=csv,
                               file_name=f'meal_plan_{meal_type}_{week_number}.csv', mime='text/csv')

        m1,m2,m3,m4 = st.columns(4)
        with m1: st.metric("Total Cost",    f"₹{plan_df['Price'].sum()}")
        with m2: st.metric("Total Calories",f"{plan_df['Calories'].sum()} kcal")
        with m3: st.metric("Total Protein", f"{plan_df['Protein'].sum()}g")
        with m4: st.metric("Budget Left",   f"₹{max(0, budget - plan_df['Price'].sum())}")

        st.dataframe(
            plan_df[["Day","Food","Calories","Protein","Fat","Price"]],
            use_container_width=True, hide_index=True,
            column_config={
                "Price":   st.column_config.NumberColumn(format="₹%d"),
                "Protein": st.column_config.NumberColumn(format="%d g"),
                "Calories":st.column_config.NumberColumn(format="%d kcal"),
            }
        )
        if plan_df['Price'].sum() > budget:
            st.warning(f"⚠️ Your selections slightly exceed the budget by ₹{plan_df['Price'].sum() - budget}.")

    with tab2:
        st.markdown("### 📈 Nutrient Distribution")
        cA, cB = st.columns(2)
        with cA:
            fig, ax = plt.subplots(figsize=(8,5))
            ax.bar(plan_df["Day"], plan_df["Calories"], color="#FF9800", alpha=0.85)
            ax.set_title("Daily Calories", fontsize=14, fontweight='bold')
            ax.set_ylabel("kcal"); plt.xticks(rotation=45)
            st.pyplot(fig)
        with cB:
            fig, ax = plt.subplots(figsize=(8,5))
            ax.bar(plan_df["Day"], plan_df["Protein"], color="#2196F3", alpha=0.85)
            ax.set_title("Daily Protein Intake", fontsize=14, fontweight='bold')
            ax.set_ylabel("grams"); plt.xticks(rotation=45)
            st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(16, 4))
        ax.plot(plan_df["Day"], plan_df["Price"], marker='o', linestyle='-', color="#4CAF50", linewidth=3)
        ax.fill_between(plan_df["Day"], plan_df["Price"], color="#4CAF50", alpha=0.2)
        ax.set_title("Cost Trend for the Week", fontsize=14, fontweight='bold')
        ax.set_ylabel("Price (₹)")
        st.pyplot(fig)

    with tab3:
        st.markdown("### 🍿 Snacks & Fast Food Picks")
        s1, s2 = st.columns(2)
        with s1:
            st.subheader("🍪 Indian Snacks")
            snacks = df[df["MealType"]=="Snacks"]
            if not snacks.empty:
                for _, r in snacks.sample(min(6, len(snacks))).iterrows():
                    tag = "🟢" if r["DietType"]=="Veg" else "🔴"
                    st.write(f"{tag} **{r['Food']}** — {r['Calories']} kcal | ₹{r['Price']}")
        with s2:
            st.subheader("🍕 Fast Food")
            fast = df[df["MealType"]=="Fast Food"]
            if not fast.empty:
                for _, r in fast.sample(min(6, len(fast))).iterrows():
                    tag = "🟢" if r["DietType"]=="Veg" else "🔴"
                    st.write(f"{tag} **{r['Food']}** — {r['Calories']} kcal | ₹{r['Price']}")

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align:center; color:grey;'>© 2026 Tamil Nadu Meal Planner | Idly, Dosai, Biryani & More! | Powered by Streamlit</p>", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from core import FERTILIZERS, CROPS, UNITS, CATEGORIES, compute_all_strategies, scale_npk

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Fertilizer Calculator",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        background: linear-gradient(90deg, #1a5c1a, #2d8a2d);
        color: white;
        padding: 20px 28px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .winner-box {
        background: #e8f5e9;
        border: 2px solid #2d8a2d;
        border-left: 6px solid #1a5c1a;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .strategy-box {
        background: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }
    .sulphur-tag {
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 14px;
        margin-top: 8px;
        display: inline-block;
    }
    .metric-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    .stSelectbox label, .stNumberInput label { font-weight: 600; }
    div[data-testid="stExpander"] { border: 1px solid #ddd; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div class="main-title">
    <h2 style="margin:0">🌱 Smart Fertilizer Calculator</h2>
    <p style="margin:4px 0 0 0; opacity:0.9; font-size:15px">
        ICAR / SAU Recommendations &nbsp;|&nbsp; IFFCO Prices Jan 2025 &nbsp;|&nbsp;
        All combinations ranked by cost
    </p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar — Inputs ─────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Input Settings")
    st.markdown("---")

    # Category filter
    category = st.selectbox("📂 Crop Category", CATEGORIES)

    # Crop list filtered by category
    crops_in_cat = {name: data for name, data in CROPS.items() if data["cat"] == category}
    crop_options = list(crops_in_cat.keys()) + ["Custom"]
    crop_name = st.selectbox("🌾 Select Crop", crop_options)

    # Show ICAR note
    if crop_name != "Custom":
        crop_data = CROPS[crop_name].copy()
        st.info(f"**Source:** {crop_data['note']}\n\n"
                f"**Season:** {crop_data['season']}\n\n"
                f"**Std. Dose:** N={crop_data['N']} | P={crop_data['P']} | K={crop_data['K']} kg/ha")
    else:
        st.markdown("**Enter custom NPK (kg/hectare):**")
        cN = st.number_input("N - Nitrogen",   min_value=0, max_value=500, value=80,  step=5)
        cP = st.number_input("P - Phosphorus", min_value=0, max_value=500, value=40,  step=5)
        cK = st.number_input("K - Potassium",  min_value=0, max_value=500, value=40,  step=5)
        cS = st.checkbox("Sulphur important for this crop?")
        crop_data = {"N": cN, "P": cP, "K": cK, "S": cS,
                     "name": "Custom", "note": "User defined", "season": "-"}

    st.markdown("---")

    # Area inputs
    unit_name = st.selectbox("📐 Area Unit", list(UNITS.keys()))
    area      = st.number_input(f"Area ({unit_name})", min_value=0.1,
                                 max_value=10000.0, value=1.0, step=0.5)

    st.markdown("---")
    calculate = st.button("🔍 Calculate Now", type="primary", use_container_width=True)

# ── Main Panel ───────────────────────────────────────────────
if calculate or "strategies" in st.session_state:

    if calculate:
        N, P, K = scale_npk(crop_data, area, unit_name)
        strategies = compute_all_strategies(N, P, K)
        st.session_state["strategies"] = strategies
        st.session_state["N"] = N
        st.session_state["P"] = P
        st.session_state["K"] = K
        st.session_state["crop_data"] = crop_data
        st.session_state["crop_name"] = crop_name
        st.session_state["area"] = area
        st.session_state["unit_name"] = unit_name

    strategies = st.session_state["strategies"]
    N          = st.session_state["N"]
    P          = st.session_state["P"]
    K          = st.session_state["K"]
    crop_data  = st.session_state["crop_data"]
    crop_name  = st.session_state["crop_name"]
    area       = st.session_state["area"]
    unit_name  = st.session_state["unit_name"]
    cheapest   = strategies[0]["total_cost"]
    sulphur    = crop_data["S"]

    # ── NPK Summary cards ────────────────────────────────────
    st.subheader(f"📊 NPK Required — {crop_name}  |  {area} {unit_name}")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🌿 Nitrogen (N)", f"{N:.1f} kg")
    with c2:
        st.metric("💧 Phosphorus (P₂O₅)", f"{P:.1f} kg")
    with c3:
        st.metric("🔥 Potassium (K₂O)", f"{K:.1f} kg")
    with c4:
        st.metric("💰 Cheapest Cost", f"Rs. {int(cheapest):,}")

    if sulphur:
        st.warning("⚠️ **Sulphur Alert:** This crop benefits from Sulphur (30 kg S/ha recommended). "
                   "Prefer combos that supply Sulphur (SSP or NPS).")

    st.markdown("---")

    # ── Comparison Table ─────────────────────────────────────
    st.subheader("📋 All Combinations — Ranked by Cost")

    table_rows = []
    for i, s in enumerate(strategies, 1):
        saving  = s["total_cost"] - cheapest
        s_tag   = f" [S={s['s_supplied']} kg]" if s["s_supplied"] > 0 else ""
        rank    = "🥇 CHEAPEST" if i == 1 else (f"+Rs. {int(saving):,}")
        table_rows.append({
            "Rank":       i,
            "Strategy":   s["name"] + s_tag,
            "Total kg":   round(s["total_kg"], 1),
            "Total Cost": f"Rs. {int(s['total_cost']):,}",
            "Extra Cost": rank,
            "Tip":        s["tag"],
        })

    df = pd.DataFrame(table_rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank":       st.column_config.NumberColumn(width="small"),
            "Strategy":   st.column_config.TextColumn(width="large"),
            "Total kg":   st.column_config.NumberColumn(width="small"),
            "Total Cost": st.column_config.TextColumn(width="medium"),
            "Extra Cost": st.column_config.TextColumn(width="medium"),
            "Tip":        st.column_config.TextColumn(width="large"),
        }
    )

    st.markdown("---")

    # ── Detailed Breakdown ───────────────────────────────────
    st.subheader("🔍 Detailed Breakdown per Strategy")

    for i, s in enumerate(strategies, 1):
        saving   = s["total_cost"] - cheapest
        medal    = "🥇" if i == 1 else ("🥈" if i == 2 else ("🥉" if i == 3 else f"#{i}"))
        box_cls  = "winner-box" if i == 1 else "strategy-box"
        label    = f"{medal} {s['name']}"
        if s["s_supplied"] > 0:
            label += f"  •  Sulphur supplied: {s['s_supplied']} kg"
        save_txt = "CHEAPEST OPTION 🏆" if i == 1 else f"+Rs. {int(saving):,} vs cheapest"

        with st.expander(label + f"   |   Rs. {int(s['total_cost']):,}   ({save_txt})",
                         expanded=(i == 1)):
            st.caption(f"💡 {s['tag']}")
            if sulphur and s["s_supplied"] > 0:
                st.success(f"✅ Sulphur supplied: {s['s_supplied']} kg — good for this crop!")
            elif sulphur and s["s_supplied"] == 0:
                st.info("ℹ️ No Sulphur in this combo — consider adding separately.")

            # Build detail table
            rows = []
            for fk, qty in s["combo"]:
                f    = FERTILIZERS[fk]
                cost = (qty / 50.0) * f["price"]
                rows.append({
                    "Fertilizer":   f["name"],
                    "Qty (kg)":     round(qty, 1),
                    "Bags (50 kg)": round(qty / 50, 2),
                    "Cost (Rs.)":   int(cost),
                })
            rows.append({
                "Fertilizer":   "TOTAL",
                "Qty (kg)":     round(s["total_kg"], 1),
                "Bags (50 kg)": round(s["total_kg"] / 50, 2),
                "Cost (Rs.)":   int(s["total_cost"]),
            })

            dfd = pd.DataFrame(rows)
            st.dataframe(dfd, use_container_width=True, hide_index=True)

    # ── Fertilizer Price Reference ───────────────────────────
    st.markdown("---")
    with st.expander("📦 Fertilizer Price Reference (IFFCO Jan 2025)"):
        fref = []
        for fk, f in FERTILIZERS.items():
            fref.append({
                "Fertilizer": f["name"],
                "N%": f["N"], "P%": f["P"], "K%": f["K"], "S%": f["S"],
                "Price/50kg bag": f"Rs. {f['price']}",
                "Bag size": f"{f['bag_kg']} kg",
            })
        st.dataframe(pd.DataFrame(fref), use_container_width=True, hide_index=True)

    st.caption("📞 Kisan Call Centre: 1800-180-1551 (Free)  |  "
               "Source: ICAR, SAU, DRMR, CRRI, IISS Bhopal  |  Prices: IFFCO MRP Jan 2025")

else:
    # Landing state
    st.info("👈 **Select your crop and area from the sidebar, then click Calculate Now.**")

    st.markdown("### How it works")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**1. Select Crop**\n\nChoose from 28 crops across "
                    "Cereals, Oilseeds, Pulses, Commercial & Vegetables. "
                    "NPK dose auto-filled from ICAR / SAU recommendations.")
    with col2:
        st.markdown("**2. Enter Area**\n\nSupports Hectare, Bigha, Acre and Katha. "
                    "Calculator scales the NPK requirement to your exact land size.")
    with col3:
        st.markdown("**3. Get Results**\n\nAll 9 fertilizer combinations ranked by cost. "
                    "See exactly how many kg and bags to buy — and how much you save.")

    st.markdown("---")
    st.markdown("**Fertilizers covered:** Urea · DAP · MOP · SSP · NPK 10-26-26 · "
                "NPK 12-32-16 · NPS 20-20-0-13 · NPK 15-15-15 · NP 28-28-0")

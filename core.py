# core.py  —  Pure calculation logic (no print/input)
# Used by both app.py (Streamlit) and original CLI script

FERTILIZERS = {
    "urea":       {"name": "Urea (46%N)",        "N": 46, "P": 0,  "K": 0,  "S": 0,  "price": 266.50, "bag_kg": 45},
    "dap":        {"name": "DAP (18-46-0)",       "N": 18, "P": 46, "K": 0,  "S": 0,  "price": 1350,   "bag_kg": 50},
    "mop":        {"name": "MOP (0-0-60)",        "N": 0,  "P": 0,  "K": 60, "S": 0,  "price": 1700,   "bag_kg": 50},
    "ssp":        {"name": "SSP (0-16-0+S)",      "N": 0,  "P": 16, "K": 0,  "S": 11, "price": 440,    "bag_kg": 50},
    "npk_102626": {"name": "NPK 10-26-26",        "N": 10, "P": 26, "K": 26, "S": 0,  "price": 1720,   "bag_kg": 50},
    "npk_123216": {"name": "NPK 12-32-16",        "N": 12, "P": 32, "K": 16, "S": 0,  "price": 1720,   "bag_kg": 50},
    "nps_202013": {"name": "NPS 20-20-0-13",      "N": 20, "P": 20, "K": 0,  "S": 13, "price": 1300,   "bag_kg": 50},
    "npk_151515": {"name": "NPK 15-15-15",        "N": 15, "P": 15, "K": 15, "S": 0,  "price": 1250,   "bag_kg": 50},
    "np_2828":    {"name": "NP 28-28-0",          "N": 28, "P": 28, "K": 0,  "S": 0,  "price": 1750,   "bag_kg": 50},
}

CROPS = {
    # CEREALS
    "Wheat":              {"N": 120, "P": 60, "K": 40,  "S": False, "season": "Rabi",        "cat": "Cereals",    "note": "IISS Bhopal: 120:60:40 kg NPK/ha"},
    "Rice (Rabi)":        {"N": 80,  "P": 40, "K": 40,  "S": False, "season": "Rabi",        "cat": "Cereals",    "note": "CRRI: Rabi irrigated 80:40:40"},
    "Rice (Kharif HYV)":  {"N": 100, "P": 60, "K": 60,  "S": False, "season": "Kharif",      "cat": "Cereals",    "note": "CRRI: Kharif irrigated 100:60:60"},
    "Rice (Hybrid)":      {"N": 100, "P": 60, "K": 60,  "S": False, "season": "Kharif",      "cat": "Cereals",    "note": "CRRI: Hybrid rice 100:60:60"},
    "Maize":              {"N": 120, "P": 60, "K": 40,  "S": False, "season": "Kharif/Rabi", "cat": "Cereals",    "note": "ICAR: 120:60:40 irrigated"},
    "Pearl Millet":       {"N": 60,  "P": 30, "K": 30,  "S": False, "season": "Kharif",      "cat": "Cereals",    "note": "SAU: 60:30:30 kg NPK/ha"},
    "Sorghum":            {"N": 80,  "P": 40, "K": 40,  "S": False, "season": "Kharif/Rabi", "cat": "Cereals",    "note": "SAU: 80:40:40 kg NPK/ha"},
    "Barley":             {"N": 60,  "P": 30, "K": 20,  "S": False, "season": "Rabi",        "cat": "Cereals",    "note": "SAU: 60:30:20 kg NPK/ha"},
    # OILSEEDS
    "Mustard":            {"N": 80,  "P": 40, "K": 40,  "S": True,  "season": "Rabi",        "cat": "Oilseeds",   "note": "DRMR Bharatpur: 80:40:40 + 30 kg S/ha"},
    "Groundnut":          {"N": 25,  "P": 50, "K": 25,  "S": True,  "season": "Kharif",      "cat": "Oilseeds",   "note": "ICAR: 25:50:25 + gypsum for Ca+S"},
    "Soybean":            {"N": 20,  "P": 60, "K": 20,  "S": False, "season": "Kharif",      "cat": "Oilseeds",   "note": "IISS Bhopal: 20:60:20 kg NPK/ha"},
    "Sunflower":          {"N": 60,  "P": 60, "K": 60,  "S": True,  "season": "Rabi/Kharif", "cat": "Oilseeds",   "note": "SAU: 60:60:60 + Sulphur beneficial"},
    "Linseed":            {"N": 30,  "P": 20, "K": 20,  "S": False, "season": "Rabi",        "cat": "Oilseeds",   "note": "SAU: 30:20:20 kg NPK/ha"},
    # PULSES
    "Chickpea":           {"N": 20,  "P": 40, "K": 20,  "S": False, "season": "Rabi",        "cat": "Pulses",     "note": "ICAR: 20:40:20 (BNF reduces N need)"},
    "Lentil":             {"N": 20,  "P": 40, "K": 20,  "S": False, "season": "Rabi",        "cat": "Pulses",     "note": "SAU: 20:40:20 kg NPK/ha"},
    "Pigeonpea (Arhar)":  {"N": 20,  "P": 50, "K": 30,  "S": False, "season": "Kharif",      "cat": "Pulses",     "note": "ICAR: 20:50:30 kg NPK/ha"},
    "Mungbean (Moong)":   {"N": 20,  "P": 40, "K": 20,  "S": False, "season": "Kharif",      "cat": "Pulses",     "note": "SAU: 20:40:20 kg NPK/ha"},
    "Urdbean (Urad)":     {"N": 20,  "P": 40, "K": 20,  "S": False, "season": "Kharif",      "cat": "Pulses",     "note": "SAU: 20:40:20 kg NPK/ha"},
    # COMMERCIAL
    "Sugarcane":          {"N": 150, "P": 60, "K": 60,  "S": False, "season": "Annual",      "cat": "Commercial", "note": "ICAR: 150:60:60 kg NPK/ha"},
    "Cotton":             {"N": 100, "P": 50, "K": 50,  "S": False, "season": "Kharif",      "cat": "Commercial", "note": "ICAR-CICR: 100:50:50 kg NPK/ha"},
    "Jute":               {"N": 60,  "P": 30, "K": 30,  "S": False, "season": "Kharif",      "cat": "Commercial", "note": "SAU: 60:30:30 kg NPK/ha"},
    # VEGETABLES
    "Potato":             {"N": 120, "P": 80, "K": 100, "S": False, "season": "Rabi",        "cat": "Vegetables", "note": "ICAR: 120:80:100 kg NPK/ha"},
    "Onion":              {"N": 100, "P": 50, "K": 100, "S": True,  "season": "Rabi",        "cat": "Vegetables", "note": "SAU: 100:50:100 kg NPK/ha + Sulphur"},
    "Tomato":             {"N": 120, "P": 75, "K": 75,  "S": False, "season": "Rabi/Kharif", "cat": "Vegetables", "note": "AAU: 120:75:75 kg NPK/ha"},
    "Brinjal":            {"N": 100, "P": 50, "K": 50,  "S": False, "season": "All",         "cat": "Vegetables", "note": "SAU: 100:50:50 kg NPK/ha"},
    "Cabbage/Cauliflower":{"N": 100, "P": 60, "K": 60,  "S": False, "season": "Rabi",        "cat": "Vegetables", "note": "SAU: 100:60:60 kg NPK/ha"},
    "Okra (Bhindi)":      {"N": 60,  "P": 40, "K": 40,  "S": False, "season": "Kharif",      "cat": "Vegetables", "note": "SAU: 60:40:40 kg NPK/ha"},
    "Turmeric":           {"N": 135, "P": 90, "K": 90,  "S": False, "season": "Kharif",      "cat": "Vegetables", "note": "ICAR-CRIDA: 135:90:90 kg NPK/ha"},
}

UNITS = {
    "Hectare": 1.0,
    "Bigha":   7.5,
    "Acre":    2.47,
    "Katha":   30.0,
}

CATEGORIES = ["Cereals", "Oilseeds", "Pulses", "Commercial", "Vegetables"]


def fert_kg(nutrient_kg, pct):
    return (100.0 * nutrient_kg / pct) if pct > 0 else 0.0

def cost_of(fert_key, qty_kg):
    return (qty_kg / 50.0) * FERTILIZERS[fert_key]["price"]

def scale_npk(crop_data, area, unit_name):
    factor = UNITS[unit_name]
    return (
        (crop_data["N"] / factor) * area,
        (crop_data["P"] / factor) * area,
        (crop_data["K"] / factor) * area,
    )

def compute_all_strategies(N, P, K):
    strategies = []

    # 1. Urea + DAP + MOP
    dap   = fert_kg(P, FERTILIZERS["dap"]["P"])
    n_dap = dap * FERTILIZERS["dap"]["N"] / 100.0
    urea  = fert_kg(max(0, N - n_dap), FERTILIZERS["urea"]["N"])
    mop   = fert_kg(K, FERTILIZERS["mop"]["K"])
    strategies.append({"name": "Urea + DAP + MOP",
        "combo": [("urea", urea), ("dap", dap), ("mop", mop)],
        "s_supplied": 0,
        "tag": "Classic combo - widely available everywhere"})

    # 2. Urea + SSP + MOP
    ssp   = fert_kg(P, FERTILIZERS["ssp"]["P"])
    urea  = fert_kg(N, FERTILIZERS["urea"]["N"])
    mop   = fert_kg(K, FERTILIZERS["mop"]["K"])
    s_ssp = (ssp * FERTILIZERS["ssp"]["S"]) / 100.0
    strategies.append({"name": "Urea + SSP + MOP",
        "combo": [("urea", urea), ("ssp", ssp), ("mop", mop)],
        "s_supplied": round(s_ssp, 1),
        "tag": "Cheapest P source; SSP adds Sulphur - great for mustard/oilseeds"})

    # 3. Urea + SSP only (low-K crops)
    if K < 5:
        ssp  = fert_kg(P, FERTILIZERS["ssp"]["P"])
        urea = fert_kg(N, FERTILIZERS["urea"]["N"])
        s_ssp= (ssp * FERTILIZERS["ssp"]["S"]) / 100.0
        strategies.append({"name": "Urea + SSP (No MOP)",
            "combo": [("urea", urea), ("ssp", ssp)],
            "s_supplied": round(s_ssp, 1),
            "tag": "For low-K crops (pulses) - saves MOP cost"})

    # 4. NPK 10-26-26 + Urea
    npk1   = fert_kg(P, FERTILIZERS["npk_102626"]["P"])
    n_npk1 = npk1 * FERTILIZERS["npk_102626"]["N"] / 100.0
    k_npk1 = npk1 * FERTILIZERS["npk_102626"]["K"] / 100.0
    urea   = fert_kg(max(0, N - n_npk1), FERTILIZERS["urea"]["N"])
    mop    = fert_kg(max(0, K - k_npk1), FERTILIZERS["mop"]["K"])
    combo4 = [("npk_102626", npk1), ("urea", urea)]
    if mop > 0.5: combo4.append(("mop", mop))
    strategies.append({"name": "NPK 10-26-26 + Urea" + (" + MOP" if mop > 0.5 else ""),
        "combo": combo4, "s_supplied": 0,
        "tag": "P+K in one bag - less handling, good for equal P:K crops"})

    # 5. NPK 12-32-16 + Urea
    npk2   = fert_kg(P, FERTILIZERS["npk_123216"]["P"])
    n_npk2 = npk2 * FERTILIZERS["npk_123216"]["N"] / 100.0
    k_npk2 = npk2 * FERTILIZERS["npk_123216"]["K"] / 100.0
    urea   = fert_kg(max(0, N - n_npk2), FERTILIZERS["urea"]["N"])
    mop    = fert_kg(max(0, K - k_npk2), FERTILIZERS["mop"]["K"])
    combo5 = [("npk_123216", npk2), ("urea", urea)]
    if mop > 0.5: combo5.append(("mop", mop))
    strategies.append({"name": "NPK 12-32-16 + Urea" + (" + MOP" if mop > 0.5 else ""),
        "combo": combo5, "s_supplied": 0,
        "tag": "High P% - fewer bags for P-heavy crops (soybean, potato)"})

    # 6. NPS 20-20-0-13 + Urea + MOP
    nps   = fert_kg(P, FERTILIZERS["nps_202013"]["P"])
    n_nps = nps * FERTILIZERS["nps_202013"]["N"] / 100.0
    s_nps = (nps * FERTILIZERS["nps_202013"]["S"]) / 100.0
    urea  = fert_kg(max(0, N - n_nps), FERTILIZERS["urea"]["N"])
    mop   = fert_kg(K, FERTILIZERS["mop"]["K"])
    strategies.append({"name": "NPS 20-20-0-13 + Urea + MOP",
        "combo": [("nps_202013", nps), ("urea", urea), ("mop", mop)],
        "s_supplied": round(s_nps, 1),
        "tag": "Best for mustard/oilseeds - NPS adds Sulphur, boosts oil content"})

    # 7. NPK 15-15-15 + Urea
    npk15  = fert_kg(P, FERTILIZERS["npk_151515"]["P"])
    n15    = npk15 * FERTILIZERS["npk_151515"]["N"] / 100.0
    k15    = npk15 * FERTILIZERS["npk_151515"]["K"] / 100.0
    urea   = fert_kg(max(0, N - n15), FERTILIZERS["urea"]["N"])
    mop    = fert_kg(max(0, K - k15), FERTILIZERS["mop"]["K"])
    combo7 = [("npk_151515", npk15), ("urea", urea)]
    if mop > 0.5: combo7.append(("mop", mop))
    strategies.append({"name": "NPK 15-15-15 + Urea" + (" + MOP" if mop > 0.5 else ""),
        "combo": combo7, "s_supplied": 0,
        "tag": "Simple balanced formula - easy for small farmers"})

    # 8. NP 28-28-0 + Urea + MOP
    np28  = fert_kg(P, FERTILIZERS["np_2828"]["P"])
    n28   = np28 * FERTILIZERS["np_2828"]["N"] / 100.0
    urea  = fert_kg(max(0, N - n28), FERTILIZERS["urea"]["N"])
    mop   = fert_kg(K, FERTILIZERS["mop"]["K"])
    strategies.append({"name": "NP 28-28-0 + Urea + MOP",
        "combo": [("np_2828", np28), ("urea", urea), ("mop", mop)],
        "s_supplied": 0,
        "tag": "Highly concentrated N+P - fewer bags, good for large farms"})

    # 9. DAP + MOP only (for low-N pulses)
    dap   = fert_kg(P, FERTILIZERS["dap"]["P"])
    n_dap = dap * FERTILIZERS["dap"]["N"] / 100.0
    mop   = fert_kg(K, FERTILIZERS["mop"]["K"])
    if n_dap >= N * 0.85:
        strategies.append({"name": "DAP + MOP (DAP meets N)",
            "combo": [("dap", dap), ("mop", mop)],
            "s_supplied": 0,
            "tag": "Only for low-N crops where DAP N is sufficient (pulses)"})

    for s in strategies:
        s["total_cost"] = sum(cost_of(fk, qty) for fk, qty in s["combo"])
        s["total_kg"]   = sum(qty for _, qty in s["combo"])

    return sorted(strategies, key=lambda x: x["total_cost"])

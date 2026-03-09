import streamlit as st
import pandas as pd  # Nový import pro práci s CSV tabulkou

# Nastavení vzhledu stránky
st.set_page_config(page_title="Výpočet optimálního a aktuálního zatížení", layout="centered")

st.title("🏃‍♂️ Výpočet optimálního a aktuálního zatížení")
st.markdown(
    "Tato aplikace využívá **$VO_2max$** pro přesný výpočet optimálního %ZC. Navíc umožňuje porovnat toto optimální zatížení s aktuálním tréninkem.")

# --- Postranní panel pro zadávání vstupů ---
st.sidebar.header("Vstupní údaje sportovce")

# Výběr pohlaví
pohlavi = st.sidebar.radio("Pohlaví:", ("Muž", "Žena"))

vek = st.sidebar.number_input("Věk (roky):", min_value=10, max_value=100, value=20)
sf_klid = st.sidebar.number_input("Klidová tepová frekvence (tepy/min):", min_value=30, max_value=120, value=57)

# Zátěžový test
zatezak_znamy = st.sidebar.checkbox("Znám SFmax ze zátěžového testu", value=False)
if zatezak_znamy:
    sf_max = st.sidebar.number_input("Zadejte naměřenou SFmax:", min_value=100, max_value=250, value=200)
else:
    # Zpřesněný výpočet podle pohlaví
    if pohlavi == "Žena":
        sf_max = 209 - (0.9 * vek)
    else:
        sf_max = 214 - (0.8 * vek)
    st.sidebar.info(f"Odhadovaná SFmax ({pohlavi}): {sf_max:.1f} tepů/min")

# Hodnota VO2max
vo2max = st.sidebar.number_input("Hodnota VO2max (ml/kg/min):", min_value=10.0, max_value=90.0, value=53.9, step=0.1)

# Kategorie populace
skupina = st.sidebar.selectbox(
    "Kategorie populace (pro finální korekci pásma):",
    ("Oslabená populace (obezita, hypokineze)", "Běžná populace", "Zdatná a aktivní populace"),
    index=2
)

st.sidebar.markdown("---")
st.sidebar.subheader("Aktuální trénink (pro porovnání)")
sf_zateze = st.sidebar.number_input("Průměrná tepovka při tréninku (ponechte 0, pokud neznáte):", min_value=0,
                                    max_value=250, value=168)

# --- HLAVNÍ ČÁST - VÝPOČTY ---

mtr = sf_max - sf_klid
optimalni_zc_pct = 60 + (vo2max / 3.5)
sf_cilova = sf_klid + (mtr * (optimalni_zc_pct / 100))

if "Oslabená" in skupina:
    spodni_hranice = sf_cilova - 20
    horni_hranice = sf_cilova - 5
elif "Běžná" in skupina:
    spodni_hranice = sf_cilova - 10
    horni_hranice = sf_cilova
else:  # Zdatná
    spodni_hranice = sf_cilova - 5
    horni_hranice = sf_cilova + 5

aktualni_zc_pct = 0
if sf_zateze > 0:
    aktualni_zc_pct = ((sf_zateze - sf_klid) / mtr) * 100

# --- ZOBRAZENÍ VÝSLEDKŮ ---
st.header("📊 Mezivýpočty")
col1, col2, col3 = st.columns(3)
col1.metric("Maximální TF", f"{sf_max:.1f} tepů")
col2.metric("MTR (Rezerva)", f"{mtr:.1f} tepů")
col3.metric("Optimální %ZC", f"{optimalni_zc_pct:.1f} %")

st.markdown("---")

# 5. Blok pro vyhodnocení aktuálního tréninku
if sf_zateze > 0:
    st.subheader("⚖️ Porovnání aktuálního a optimálního zatížení")

    col_akt, col_opt = st.columns(2)
    col_akt.metric("Aktuální zatížení v tréninku", f"{aktualni_zc_pct:.1f} %")
    col_opt.metric("Optimální zatížení z VO2max", f"{optimalni_zc_pct:.1f} %")

    rozdil = aktualni_zc_pct - optimalni_zc_pct
    if abs(rozdil) <= 3:
        st.success(f"✅ Aktuální zatížení je téměř ideální. Rozdíl od optima je pouze {abs(rozdil):.1f} %.")
    elif rozdil > 3:
        st.warning(
            f"⚠️ Aktuální zatížení ({aktualni_zc_pct:.1f} %) je **lehce nad optimem** ({optimalni_zc_pct:.1f} %).")
    else:
        st.info(f"🔽 Aktuální zatížení ({aktualni_zc_pct:.1f} %) je **nižší než optimální** ({optimalni_zc_pct:.1f} %).")
    st.markdown("---")

st.subheader("🎯 Výsledek: Hranice optimálního pásma")
st.write(f"Vypočítaná cílová tepová frekvence (před korekcí): **{sf_cilova:.0f} tepů/min**")
st.success(f"### Doporučené tréninkové pásmo:\n# {int(spodni_hranice)} – {int(horni_hranice)} tepů / min")

# Vysvětlení postupu pro kontrolu
st.markdown("### 📝 Postup výpočtu krok za krokem:")

# Dynamický text pro vzorec SFmax v taháku
if zatezak_znamy:
    sf_max_text = f"**{sf_max}** (Zadána naměřená hodnota ze zátěžového testu)"
else:
    if pohlavi == "Žena":
        sf_max_text = f"209 - (0.9 × {vek}) = **{sf_max:.1f}** (Odhad dle pohlaví a věku)"
    else:
        sf_max_text = f"214 - (0.8 × {vek}) = **{sf_max:.1f}** (Odhad dle pohlaví a věku)"

if sf_zateze > 0:
    st.markdown(f"""
    1. **SFmax:** {sf_max_text}
    2. **MTR:** {sf_max:.1f} (SFmax) - {sf_klid} (SFklid) = **{mtr:.1f} tepů**.
    3. **Aktuální %ZC:** Vzorec `((SF_zátěže - SF_klid) / MTR) * 100`. Po dosazení `(({sf_zateze} - {sf_klid}) / {mtr:.1f}) * 100` = **{aktualni_zc_pct:.1f} %**.
    4. **Optimální %ZC:** Vzorec `60 + (VO2max / 3,5)`. Po dosazení `60 + ({vo2max} / 3,5)` = **{optimalni_zc_pct:.1f} %**.
    5. **Cílová SF:** {sf_klid} + ({mtr:.1f} × {optimalni_zc_pct / 100:.3f}) = **{sf_cilova:.1f} tepů/min**.
    6. **Korekce pásma:** (Zdatná a aktivní populace $\pm$ 5 tepů) = **{int(spodni_hranice)} až {int(horni_hranice)} tepů**.
    """)
else:
    st.markdown(f"""
    1. **SFmax:** {sf_max_text}
    2. **MTR:** {sf_max:.1f} (SFmax) - {sf_klid} (SFklid) = **{mtr:.1f} tepů**.
    3. **Optimální %ZC:** Vzorec `60 + (VO2max / 3,5)`. Po dosazení `60 + ({vo2max} / 3,5)` = **{optimalni_zc_pct:.1f} %**.
    4. **Cílová SF:** {sf_klid} + ({mtr:.1f} × {optimalni_zc_pct / 100:.3f}) = **{sf_cilova:.1f} tepů/min**.
    5. **Korekce pásma:** Hranice upraveny dle vybrané kategorie populace = **{int(spodni_hranice)} až {int(horni_hranice)} tepů**.
    """)

# --- EXPORT DAT (NOVÁ ČÁST) ---
st.markdown("---")
st.header("💾 Export výsledků")

# 1. Příprava dat pro CSV
data_export = {
    "Pohlavi": [pohlavi],
    "Vek": [vek],
    "Klidova_SF": [sf_klid],
    "Max_SF": [round(sf_max, 1)],
    "Zatezovy_test": ["Ano" if zatezak_znamy else "Ne (odhad)"],
    "VO2max": [vo2max],
    "Kategorie": [skupina],
    "SF_trening": [sf_zateze if sf_zateze > 0 else "Nezadano"],
    "MTR": [round(mtr, 1)],
    "Optimalni_ZC_pct": [round(optimalni_zc_pct, 1)],
    "Aktualni_ZC_pct": [round(aktualni_zc_pct, 1) if sf_zateze > 0 else "N/A"],
    "Spodni_hranice": [int(spodni_hranice)],
    "Horni_hranice": [int(horni_hranice)]
}
df_export = pd.DataFrame(data_export)
csv_data = df_export.to_csv(index=False).encode('utf-8')

# 2. Příprava dat pro Textový report (.txt)
report_text = f"""--- ZPRÁVA O PRESKRIPCI POHYBOVÉ AKTIVITY ---

VSTUPNÍ ÚDAJE:
- Klient: {pohlavi}, {vek} let
- Kategorie: {skupina}
- Klidová SF: {sf_klid} tepů/min
- Maximální SF: {sf_max:.1f} tepů/min ({'naměřeno testem' if zatezak_znamy else 'odhad dle věku'})
- VO2max: {vo2max} ml/kg/min
- Aktuální SF v tréninku: {sf_zateze if sf_zateze > 0 else 'Nezadáno'}

MEZIVÝPOČTY:
- MTR (Rezerva): {mtr:.1f} tepů
- Optimální zatížení dle VO2max: {optimalni_zc_pct:.1f} %
"""
if sf_zateze > 0:
    report_text += f"- Aktuální zatížení v tréninku: {aktualni_zc_pct:.1f} %\n"

report_text += f"""
VÝSLEDEK PRESKRIPCE:
Doporučené tréninkové pásmo: {int(spodni_hranice)} – {int(horni_hranice)} tepů / min.
---------------------------------------------
"""

# Tlačítka pro stažení vedle sebe
col_csv, col_txt = st.columns(2)
with col_csv:
    st.download_button(
        label="📥 Stáhnout tabulku (CSV)",
        data=csv_data,
        file_name='vysledky_klienta.csv',
        mime='text/csv',
    )
with col_txt:
    st.download_button(
        label="📄 Stáhnout report (TXT)",
        data=report_text,
        file_name='report_klienta.txt',
        mime='text/plain',
    )

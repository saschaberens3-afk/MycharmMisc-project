#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# ---------- Hilfsfunktion ----------
def lin(x, m, b):
    return m * x + b

# ---------- 1. Daten laden ----------
df = pd.read_excel(
    "Kalorimetrie-test.xlsx",   # Dateiname ggf. anpassen
    sheet_name="Tabelle1",      # Blattname ggf. anpassen
    engine="openpyxl",
    header=1
)

# ---------- 2. Beschreibung aller Messreihen ----------
bereiche = {
    "1. Messung":  ("Zeit",   "Temp",    800, 860),
    "2. Messung":  ("Zeit.1", "Temp.1",  400, 450),
    "3. Messung":  ("Zeit.2", "Temp.2",  390, 430),

    "4. Messung":  ("Zeit.3", "Temp.3",  250, 300),
    "5. Messung":  ("Zeit.4", "Temp.4",  250, 300),
    "6. Messung":  ("Zeit.5", "Temp.5",  250, 300),

    "7. Messung":  ("Zeit.6", "Temp.6",  220, 280),
    "8. Messung":  ("Zeit.7", "Temp.7",  220, 280),
    "9. Messung":  ("Zeit.8", "Temp.8",  220, 280),

    "10. Messung": ("Zeit.9", "Temp.9",  200, 260),
}

results = []

# ---------- 3. Schleife über jede definierte Messreihe ----------
for mess_name, (zeit_col, temp_col, t_min, t_max) in bereiche.items():
    print(f"\n=== Bearbeite: {mess_name} ===")

    # Prüfen, ob Spalten überhaupt existieren
    if zeit_col not in df.columns or temp_col not in df.columns:
        print(f"   -> Spalten {zeit_col}/{temp_col} nicht gefunden. Überspringe.")
        continue

    # Rohdaten holen
    x_raw = pd.to_numeric(df[zeit_col], errors="coerce").values
    y_raw = pd.to_numeric(df[temp_col], errors="coerce").values

    # NaN rauswerfen
    valid_mask = ~np.isnan(x_raw) & ~np.isnan(y_raw)
    x = x_raw[valid_mask]
    y = y_raw[valid_mask]

    if len(x) < 10:
        print("   -> Zu wenige Datenpunkte. Überspringe.")
        continue

    # ---------- Fit-Bereich anwenden ----------
    fit_mask = (x >= t_min) & (x <= t_max)

    # Prüfen, ob überhaupt Punkte im Bereich liegen
    if not np.any(fit_mask):
        print(f"   -> Kein Fitbereich {t_min}-{t_max}s in den Daten. Überspringe.")
        continue

    # Punkte für den Fit
    x_tan = x[fit_mask]
    y_tan = y[fit_mask]

    # Falls zu wenige Punkte im Fitbereich, überspringen
    if len(x_tan) < 3:
        print(f"   -> Zu wenige Punkte ({len(x_tan)}) im Fit-Bereich {t_min}-{t_max}s. Überspringe.")
        continue

    # ---------- Lineare Regression (Tangente) ----------
    popt, pcov = curve_fit(lin, x_tan, y_tan)
    m, b = popt
    σ_m, σ_b = np.sqrt(np.diag(pcov))
    cov_mb = pcov[0, 1]

    # ---------- R² ----------
    y_pred = lin(x_tan, *popt)
    ss_res = np.sum((y_tan - y_pred) ** 2)
    ss_tot = np.sum((y_tan - np.mean(y_tan)) ** 2)
    r2 = 1 - ss_res / ss_tot

    # ---------- Tangente über alle Zeiten berechnen ----------
    y_tangente = lin(x, *popt)

    # ---------- Schnittpunkt Messkurve / Tangente ----------
    # Wir suchen die erste Stelle, wo Messkurve y und Tangente y_tangente auseinanderlaufen:
    delta = y - y_tangente
    wechsel = np.where(np.diff(np.sign(delta)))[0]

    if len(wechsel) == 0:
        print("   -> Kein Schnittpunkt gefunden. Überspringe.")
        continue

    idx = wechsel[0]
    x_schnitt = x[idx]
    y_schnitt = y_tangente[idx]

    # ---------- Fehlerfortpflanzung für den y-Wert am Schnittpunkt ----------
    σ_T = np.sqrt(
        x_schnitt**2 * σ_m**2 +
        σ_b**2 +
        2 * x_schnitt * cov_mb
    )

    # ---------- Plot ----------
    plt.figure(figsize=(8, 6))
    # Messkurve
    plt.plot(x, y, lw=2, label="Messwerte")

    # Tangente von x=0 bis zum Schnittpunkt
    x_tan_plot = np.linspace(0, x_schnitt, 200)
    y_tan_plot = lin(x_tan_plot, m, b)
    plt.plot(x_tan_plot, y_tan_plot, "r--", lw=2,
             label=f"Tangente: y = {m:.4f}x + {b:.2f}")

    # Markierung des Schnittpunkts
    plt.plot(x_schnitt, y_schnitt, "wo", markeredgecolor="k", label="Schnittpunkt")

    # horizontale Linie auf Höhe des Schnittpunkts (optional)
    plt.hlines(y_schnitt, 0, x_schnitt,
               linestyle=":", lw=2, color="green",
               label=f"Tgef ≈ {y_schnitt:.2f} ± {σ_T:.2f} °C")

    # Achsen, Titel, usw.
    plt.xlabel("Zeit / s")
    plt.ylabel("Temperatur / °C")
    plt.title(mess_name)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ---------- Ergebnisse speichern ----------
    results.append({
        "Messreihe": mess_name,
        "Fit_von_s": t_min,
        "Fit_bis_s": t_max,
        "Gefrierpunkt_C": y_schnitt,
        "Fehler_C_1sigma": σ_T,
        "R2": r2,
        "m": m,
        "σ_m": σ_m,
        "b": b,
        "σ_b": σ_b,
    })

# ---------- Zusammenfassung ----------
if results:
    summary_df = pd.DataFrame(results)
    print("\n===== Zusammenfassung =====")
    print(summary_df)


# In[ ]:





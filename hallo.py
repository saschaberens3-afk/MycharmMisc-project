#!/usr/bin/env python
# coding: utf-8

# In[5]:


£
# -*- coding: utf-8 -*-
monTexte = "Heureusement que les variables existent"
print(monTexte)
print(monTexte)
input("Tapez ENTREE")



# In[ ]:


#!/usr/bin/env python
# -*- coding: utf-8 -*-
monTexte = "Heureusement que la boucle FOR existe"
for compteur in range(5) :
    print(monTexte)


# In[6]:


monTexte = "Heureusement que la boucle FOR existe"

for compteur in range(5):
    print(monTexte)


# In[7]:


#!/usr/bin/env python
# -*- coding: utf-8 -*-
monTexte = "Heureusement que la boucle FOR existe"
for compteur in range(5) :
    print(compteur)
    print(monTexte)
input("Tapez sur ENTREE")


# In[9]:


monTexte = "Un peu de patience !"
for compteur in range(500) :
    print(compteur, "   ", monTexte)
input("Tapez sur ENTREE")


# In[13]:


# -*- coding: utf-8 -*-

R = int(input("Valeur de R en Ohm ? "))
print("U(V)\tI(A)")

for I in range(11):   # von 0 bis 10 inklusive
    U = R * I
    print(U, "\t", I)

input("Tapez sur ENTREE")


# In[14]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# ======================================
# Excel-Datei laden
# ======================================
df = pd.read_excel("Reines Wasser.xlsx", engine="openpyxl",
                   usecols="A,B", skiprows=3, nrows=589)
df.columns = ["Zeit", "Temperatur"]

# ======================================
# Lineare Regression im Bereich 520–590 s
# ======================================
fit_mask = (df["Zeit"] >= 520) & (df["Zeit"] <= 590)
x_tan = df.loc[fit_mask, "Zeit"].values
y_tan = df.loc[fit_mask, "Temperatur"].values

def lin(x, m, b):
    return m * x + b

# Curve Fit mit Kovarianzmatrix
popt, pcov = curve_fit(lin, x_tan, y_tan)
m, b = popt
σ_m, σ_b = np.sqrt(np.diag(pcov))
cov_mb = pcov[0, 1]

# ======================================
# Bestimmtheitsmaß R²
# ======================================
y_pred = lin(x_tan, *popt)
ss_res = np.sum((y_tan - y_pred) ** 2)
ss_tot = np.sum((y_tan - np.mean(y_tan)) ** 2)
r2 = 1 - ss_res / ss_tot

# ======================================
# Schnittpunkt mit Abkühlkurve finden
# ======================================
df["Tangente"] = lin(df["Zeit"], *popt)
df["Delta"] = df["Temperatur"] - df["Tangente"]
wechsel_idx = np.where(np.diff(np.sign(df["Delta"])))[0][0]
x_schnitt = df["Zeit"].iloc[wechsel_idx]
y_schnitt = df["Tangente"].iloc[wechsel_idx]

# ======================================
# Standardfehler des Gefrierpunkts
# ======================================
σ_T = np.sqrt(x_schnitt**2 * σ_m**2 + σ_b**2 + 2 * x_schnitt * cov_mb)

# ======================================
# Plot
# ======================================
plt.figure(figsize=(8, 6))

# Messwerte (blau)
plt.plot(df["Zeit"], df["Temperatur"], color="blue", lw=2, label="Messwerte")

# Tangente (rot, gestrichelt)
plt.plot(df["Zeit"], df["Tangente"], color="red", linestyle="--", lw=2,
         label=f"Tangente: y = {m:.3f}x + {b:.2f}")

# Horizontale Linie am Schnittpunkt (grün, gepunktet)
plt.hlines(y_schnitt, 0, x_schnitt, color="green", linestyle=":", lw=2,
           label=fr"$T_{{\mathrm{{Gefrierpunkt}}}} = {y_schnitt:.2f} \pm {σ_T:.2f}\,^{{\circ}}\mathrm{{C}}$")

# Gefrierpunkt markieren
plt.plot(x_schnitt, y_schnitt, "ko", label="Gefrierpunkt")

# Achsenbeschriftung, Titel, Legende
plt.xlabel("Zeit / s")
plt.ylabel("Temperatur / °C")
plt.title("Graph 1: Abkühlkurve mit Gefrierpunkt")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show()

# ======================================
# Ausgaben
# ======================================
print(f"R² der Tangente           : {r2:.4f}")
print(f"Gefrierpunkt              : {y_schnitt:.2f} °C")
print(f"Standardfehler (1 σ)      : ±{σ_T:.2f} °C")
print(f"Fit-Parameter m, b        : {m:.5f} ± {σ_m:.5f},  {b:.2f} ± {σ_b:.2f}")


# In[18]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# ======================================
# Hilfsfunktion: lineare Funktion
# ======================================
def lin(x, m, b):
    return m * x + b


# ======================================
# Excel einlesen
# ======================================
df = pd.read_excel("Exp 4 KryoskopieTest.xlsx", sheet_name="Tabelle1", engine="openpyxl")

# Die erste Spalte ist die Zeit (wenn das bei dir so ist!)
zeit = df.iloc[:, 0].values

# Alle anderen Spalten enthalten Temperaturen verschiedener Messungen
spalten = df.columns[1:]  # alle außer der Zeitspalte

# ======================================
# Loop über alle Messreihen
# ======================================
for name in spalten:
    # Spalte in Zahlen umwandeln (Text → NaN)
    temperatur = pd.to_numeric(df[name], errors='coerce').values

    # Nur Zeilen mit gültigen Werten
    mask = ~np.isnan(temperatur)
    x = zeit[mask]
    y = temperatur[mask]

    # Überspringen, wenn Spalte komplett leer oder unbrauchbar ist
    if len(y) < 10:
        continue

    # Fit-Bereich
    fit_mask = (x >= 520) & (x <= 590)
    if not np.any(fit_mask):
        continue

    x_tan = x[fit_mask]
    y_tan = y[fit_mask]

    popt, pcov = curve_fit(lin, x_tan, y_tan)
    m, b = popt
    σ_m, σ_b = np.sqrt(np.diag(pcov))
    cov_mb = pcov[0, 1]

    y_pred = lin(x_tan, *popt)
    ss_res = np.sum((y_tan - y_pred) ** 2)
    ss_tot = np.sum((y_tan - np.mean(y_tan)) ** 2)
    r2 = 1 - ss_res / ss_tot

    # Schnittpunkt
    y_tangente = lin(x, *popt)
    delta = y - y_tangente
    wechsel = np.where(np.diff(np.sign(delta)))[0]
    if len(wechsel) == 0:
        continue
    idx = wechsel[0]
    x_schnitt = x[idx]
    y_schnitt = y_tangente[idx]
    σ_T = np.sqrt(x_schnitt**2 * σ_m**2 + σ_b**2 + 2 * x_schnitt * cov_mb)

    # Plot
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label="Messwerte")
    plt.plot(x, y_tangente, "r--", label="Tangente")
    plt.hlines(y_schnitt, 0, x_schnitt, "g", linestyle=":")
    plt.plot(x_schnitt, y_schnitt, "ko", label="Gefrierpunkt")
    plt.title(name)
    plt.legend()
    plt.grid(True)
    plt.show()

    print(f"{name}: Gefrierpunkt {y_schnitt:.2f} °C, R²={r2:.4f}")

    # ======================================
    # Plot für diese Messung
    # ======================================
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, color="blue", lw=2, label="Messwerte")
    plt.plot(x, y_tangente, "r--", lw=2, label=f"Tangente: y = {m:.3f}x + {b:.2f}")
    plt.hlines(y_schnitt, 0, x_schnitt, color="green", linestyle=":", lw=2,
               label=fr"$T_{{Gefrierpunkt}} = {y_schnitt:.2f} \pm {σ_T:.2f}\,^{{\circ}}\mathrm{{C}}$")
    plt.plot(x_schnitt, y_schnitt, "ko", label="Gefrierpunkt")

    plt.xlabel("Zeit / s")
    plt.ylabel("Temperatur / °C")
    plt.title(f"{name}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # ======================================
    # Ausgabe in Konsole
    # ======================================
    print("=====================================")
    print(f"Messreihe                : {name}")
    print(f"R² der Tangente          : {r2:.4f}")
    print(f"Gefrierpunkt             : {y_schnitt:.2f} °C")
    print(f"Standardfehler (1 σ)     : ±{σ_T:.2f} °C")
    print(f"Fit-Parameter m, b       : {m:.5f} ± {σ_m:.5f},  {b:.2f} ± {σ_b:.2f}")
    print("=====================================\n")


# In[35]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# ---------- Hilfsfunktion ----------
def lin(x, m, b):
    return m * x + b

# ---------- 1. Daten laden ----------
df = pd.read_excel(
    "Exp 4 KryoskopieTest.xlsx",   # <-- hier dein Dateiname
    sheet_name="Tabelle1",         # <-- hier dein Tabellenblatt-Name
    engine="openpyxl",
    header=3
)

# Wir nehmen an: erste Spalte = Zeit
zeit = pd.to_numeric(df.iloc[:, 0], errors='coerce').values

# Alle restlichen Spalten = Temperaturkurven
spalten = df.columns[1:]  # überspringt Zeitspalte


# ---------- 2. Fit-Bereiche für jede Messung definieren ----------
# Schlüssel = Spaltenname in Excel
# Wert = (t_min, t_max) Bereich, der linear (~Tangente vorm Schnitt) ist
bereiche = {
    ("Reines Wasser 1",   "Zeit",    "Temp",    520, 590),
    ("Reines Wasser 2",   "Zeit.1",  "Temp.1",  520, 590),
    ("Reines Wasser 3",   "Zeit.2",  "Temp.2",  520, 590),

    ("2.5 wt% 1",         "Zeit.3",  "Temp.3",  250, 300),
    ("2.5 wt% 2",         "Zeit.4",  "Temp.4",  250, 300),
    ("2.5 wt% 3",         "Zeit.5",  "Temp.5",  250, 300),

    ("5 wt% 1",           "Zeit.6",  "Temp.6",  220, 280),
    ("5 wt% 2",           "Zeit.7",  "Temp.7",  220, 280),
    ("5 wt% 3",           "Zeit.8",  "Temp.8",  220, 280),

    ("7.5 wt% 1",         "Zeit.9",   "Temp.9",   200, 260),
    ("7.5 wt% 2",         "Zeit.10",  "Temp.10",  200, 260),
    ("7.5 wt% 3",         "Zeit.11",  "Temp.11",  200, 260),

    ("10 wt% 1",          "Zeit.12", "Temp.12",  180, 240),
    ("10 wt% 2",          "Zeit.13", "Temp.13",  180, 240),
    ("10 wt% 3",          "Zeit.14", "Temp.14",  180, 240)}

# ---------- 3. Schleife über jede Messreihe ----------
results = []  # sammeln für späteren Export, falls du willst

for name in spalten:
    print(f"\n=== Bearbeite: {name} ===")

    # Prüfen, ob wir wissen, welchen Fitbereich wir für diese Messreihe nehmen sollen
    if name not in bereiche:
        print(f"   -> Kein Fit-Bereich für '{name}' definiert. Überspringe.")
        continue

    t_min, t_max = bereiche[name]

    # Temperaturspalte in Zahlen wandeln (Text -> NaN)
    temperatur = pd.to_numeric(df[name], errors='coerce').values

    # Nur gültige Werte (keine NaNs)
    valid_mask = ~np.isnan(temperatur)
    x = zeit[valid_mask]
    y = temperatur[valid_mask]

    # Prüfen: Haben wir überhaupt Daten?
    if len(y) < 10:
        print("   -> Zu wenige Datenpunkte, überspringe.")
        continue

    # Fit-Bereich anwenden (z. B. 520-590 s oder 200-260 s, je nach Messung)
    fit_mask = (x >= t_min) & (x <= t_max)

    if not np.any(fit_mask):
        print(f"   -> In '{name}' gibt es keine Daten zwischen {t_min}s und {t_max}s. Überspringe.")
        continue

    x_tan = x[fit_mask]
    y_tan = y[fit_mask]

    # Lineare Regression in dem definierten Bereich
    popt, pcov = curve_fit(lin, x_tan, y_tan)
    m, b = popt
    σ_m, σ_b = np.sqrt(np.diag(pcov))
    cov_mb = pcov[0, 1]

    # Bestimmtheitsmaß R²
    y_pred = lin(x_tan, *popt)
    ss_res = np.sum((y_tan - y_pred) ** 2)
    ss_tot = np.sum((y_tan - np.mean(y_tan)) ** 2)
    r2 = 1 - ss_res / ss_tot

    # Tangente über gesamten Zeitbereich
    y_tangente = lin(x, *popt)

    # Schnittpunkt: Stelle, wo Messkurve und Tangente sich schneiden
    delta = y - y_tangente
    wechsel = np.where(np.diff(np.sign(delta)))[0]
    if len(wechsel) == 0:
        print("   -> Kein Schnittpunkt gefunden, überspringe.")
        continue

    idx = wechsel[0]
    x_schnitt = x[idx]
    y_schnitt = y_tangente[idx]

    # Fehlerfortpflanzung für T_Gefrierpunkt
    σ_T = np.sqrt(
        x_schnitt**2 * σ_m**2 +
        σ_b**2 +
        2 * x_schnitt * cov_mb
    )

    # ---------- Plot ----------
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, lw=2, label="Messwerte")
    plt.plot(x, y_tangente, "r--", lw=2,
             label=f"Tangente: y = {m:.3f}x + {b:.2f}")
    plt.hlines(y_schnitt, x.min(), x_schnitt, "g", linestyle=":",
               lw=2,
               label=fr"$T_{{Gefrierpunkt}} = {y_schnitt:.2f} \pm {σ_T:.2f}$ °C")
    plt.plot(x_schnitt, y_schnitt, "ko", label="Gefrierpunkt")

    plt.xlabel("Zeit / s")
    plt.ylabel("Temperatur / °C")
    plt.title(f"{name}  (Fit: {t_min}–{t_max} s)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ---------- Konsole-Output ----------
    print(f"   Gefrierpunkt           : {y_schnitt:.2f} °C")
    print(f"   Unsicherheit (1σ)      : ±{σ_T:.2f} °C")
    print(f"   R² des Fits            : {r2:.4f}")
    print(f"   m, b                   : {m:.5f} ± {σ_m:.5f},  {b:.2f} ± {σ_b:.2f}")
    print(f"   verwendeter Fit-Bereich: {t_min}s – {t_max}s")

    # ---------- Ergebnis merken ----------
    results.append({
        "Messreihe": name,
        "Fit von [s]": t_min,
        "Fit bis [s]": t_max,
        "Gefrierpunkt [°C]": y_schnitt,
        "Fehler [°C]": σ_T,
        "R²": r2,
        "m": m,
        "σ_m": σ_m,
        "b": b,
        "σ_b": σ_b
    })

# Optional: Am Ende eine Tabelle aller Ergebnisse anzeigen
if results:
    summary_df = pd.DataFrame(results)
    print("\n===== Zusammenfassung aller Messreihen =====")
    print(summary_df)


# In[36]:


print(df.columns)


# In[50]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# ---------- Hilfsfunktion ----------
def lin(x, m, b):
    return m * x + b

# ---------- 1. Daten laden ----------
df = pd.read_excel(
    "Exp 4 KryoskopieTest.xlsx",   # Dateiname ggf. anpassen
    sheet_name="Tabelle1",         # Blattname ggf. anpassen
    engine="openpyxl",
    header=3                       # hast du ja schon so gewählt
)

# ---------- 2. Beschreibung aller Messreihen ----------
# Key = wie die Messreihe heißen soll (für Plot/Tabelle)
# Value = (Zeitspalte, Temperaturspalte, t_min, t_max)
bereiche = {
    "Reines Wasser 1": ("Zeit",   "Temp",    520, 590),
    "Reines Wasser 2": ("Zeit.1", "Temp.1",  400, 450),
    "Reines Wasser 3": ("Zeit.2", "Temp.2",  520, 590),

    "2.5 wt% 1":       ("Zeit.3", "Temp.3",  250, 300),
    "2.5 wt% 2":       ("Zeit.4", "Temp.4",  250, 300),
    "2.5 wt% 3":       ("Zeit.5", "Temp.5",  250, 300),

    "5 wt% 1":         ("Zeit.6", "Temp.6",  220, 280),
    "5 wt% 2":         ("Zeit.7", "Temp.7",  220, 280),
    "5 wt% 3":         ("Zeit.8", "Temp.8",  220, 280),

    "7.5 wt% 1":       ("Zeit.9",  "Temp.9",  200, 260),
    "7.5 wt% 2":       ("Zeit.10", "Temp.10", 200, 260),
    "7.5 wt% 3":       ("Zeit.11", "Temp.11", 150, 190),

    "10 wt% 1":        ("Zeit.12", "Temp.12", 300, 360),
    "10 wt% 2":        ("Zeit.13", "Temp.13", 180, 240),
    "10 wt% 3":        ("Zeit.14", "Temp.14", 180, 240),
}

results = []

# ---------- 3. Schleife über jede definierte Messreihe ----------
for mess_name, (zeit_col, temp_col, t_min, t_max) in bereiche.items():
    print(f"\n=== Bearbeite: {mess_name} ===")

    # Prüfen ob Spalten überhaupt existieren (z. B. falls leere Messung)
    if zeit_col not in df.columns or temp_col not in df.columns:
        print(f"   -> Spalten {zeit_col}/{temp_col} nicht gefunden. Überspringe.")
        continue

    # Rohdaten aus dieser Messung holen und in Zahlen umwandeln
    x_raw = pd.to_numeric(df[zeit_col], errors="coerce").values
    y_raw = pd.to_numeric(df[temp_col], errors="coerce").values

    # NaN rauswerfen
    valid_mask = ~np.isnan(x_raw) & ~np.isnan(y_raw)
    x = x_raw[valid_mask]
    y = y_raw[valid_mask]

    if len(x) < 10:
        print("   -> Zu wenige Datenpunkte. Überspringe.")
        continue

    # Fit-Bereich anwenden
    fit_mask = (x >= t_min) & (x <= t_max)
    x_tan = x[fit_mask]
    y_tan = y[fit_mask]

# Fit-Bereich anwenden (z. B. 520–590 s)
fit_mask = (x >= t_min) & (x <= t_max)

# Prüfen, ob überhaupt Punkte im Bereich liegen
if not np.any(fit_mask):
    print(f"   -> Kein Fitbereich {t_min}-{t_max}s in den Daten. Überspringe.")
    continue

# Fit-Daten extrahieren
x_tan = x[fit_mask]
y_tan = y[fit_mask]

# Falls zu wenige Punkte im Fitbereich, überspringen
if len(x_tan) < 3:
    print(f"   -> Zu wenige Punkte ({len(x_tan)}) im Fit-Bereich {t_min}-{t_max}s. Überspringe.")
    continue

    # Lineare Regression (Tangente)
    popt, pcov = curve_fit(lin, x_tan, y_tan)
    m, b = popt
    σ_m, σ_b = np.sqrt(np.diag(pcov))
    cov_mb = pcov[0, 1]

    # R²
    y_pred = lin(x_tan, *popt)
    ss_res = np.sum((y_tan - y_pred) ** 2)
    ss_tot = np.sum((y_tan - np.mean(y_tan)) ** 2)
    r2 = 1 - ss_res / ss_tot

    # Tangente über alle Zeiten
    y_tangente = lin(x, *popt)

    # Schnittpunkt Messkurve vs. Tangente
    delta = y - y_tangente
    wechsel = np.where(np.diff(np.sign(delta)))[0]
    if len(wechsel) == 0:
        print("   -> Kein Schnittpunkt gefunden. Überspringe.")
        continue

    idx = wechsel[0]
    x_schnitt = x[idx]
    y_schnitt = y_tangente[idx]

    # Fehlerfortpflanzung für T_Gefrierpunkt
    σ_T = np.sqrt(
        x_schnitt**2 * σ_m**2 +
        σ_b**2 +
        2 * x_schnitt * cov_mb
    )

    # Plot für diese Messreihe
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, lw=2, label="Messwerte")
    # Tangente nur bis kurz nach dem Schnittpunkt zeichnen
    x_tan_plot = x[(x >= x_schnitt - 40) & (x <= x.max())]   # +10 Sekunden nach dem Schnittpunkt (optional)
    y_tan_plot = lin(x_tan_plot, m, b)
    plt.plot(x_tan_plot, y_tan_plot, "r--", lw=2,
         label=f"Tangente (Fit bis Schnittpunkt): y = {m:.3f}x + {b:.2f}")
    plt.hlines(y_schnitt, x.min(), x_schnitt,
               linestyle=":", lw=2, color="green",
               label=f"Tgef = {y_schnitt:.2f} ± {σ_T:.2f} °C")
    plt.plot(x_schnitt, y_schnitt, "ko", label="Gefrierpunkt")

    plt.xlabel("Zeit / s")
    plt.ylabel("Temperatur / °C")
    plt.title(f"{mess_name}  (Fit {t_min}–{t_max} s)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Ergebnisse merken
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

# Zusammenfassung am Ende
if results:
    summary_df = pd.DataFrame(results)
    print("\n===== Zusammenfassung =====")
    print(summary_df)


# In[55]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# ---------- Hilfsfunktion ----------
def lin(x, m, b):
    return m * x + b

# ---------- 1. Daten laden ----------
df = pd.read_excel(
    "Exp 4 KryoskopieTest.xlsx",   # Dateiname ggf. anpassen
    sheet_name="Tabelle1",         # Blattname ggf. anpassen
    engine="openpyxl",
    header=3                       # hast du ja schon so gewählt
)

# ---------- 2. Beschreibung aller Messreihen ----------
bereiche = {
    "Reines Wasser 1": ("Zeit",   "Temp",    520, 590),
    "Reines Wasser 2": ("Zeit.1", "Temp.1",  400, 450),
    "Reines Wasser 3": ("Zeit.2", "Temp.2",  390, 430),

    "2.5 wt% 1":       ("Zeit.3", "Temp.3",  250, 300),
    "2.5 wt% 2":       ("Zeit.4", "Temp.4",  250, 300),
    "2.5 wt% 3":       ("Zeit.5", "Temp.5",  250, 300),

    "5 wt% 1":         ("Zeit.6", "Temp.6",  220, 280),
    "5 wt% 2":         ("Zeit.7", "Temp.7",  220, 280),
    "5 wt% 3":         ("Zeit.8", "Temp.8",  220, 280),

    "7.5 wt% 1":       ("Zeit.9",  "Temp.9",  200, 260),
    "7.5 wt% 2":       ("Zeit.10", "Temp.10", 200, 260),
    "7.5 wt% 3":       ("Zeit.11", "Temp.11", 150, 190),

    "10 wt% 1":        ("Zeit.12", "Temp.12", 300, 360),
    "10 wt% 2":        ("Zeit.13", "Temp.13", 180, 240),
    "10 wt% 3":        ("Zeit.14", "Temp.14", 180, 240),
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

    # 1️⃣ Prüfen, ob überhaupt Punkte im Bereich liegen
    if not np.any(fit_mask):
        print(f"   -> Kein Fitbereich {t_min}-{t_max}s in den Daten. Überspringe.")
        continue

    # 2️⃣ Daten im Fitbereich holen
    x_tan = x[fit_mask]
    y_tan = y[fit_mask]

    # 3️⃣ Falls zu wenige Punkte im Fitbereich, überspringen
    if len(x_tan) < 3:
        print(f"   -> Zu wenige Punkte ({len(x_tan)}) im Fit-Bereich {t_min}-{t_max}s. Überspringe.")
        continue

    # ---------- Lineare Regression (Tangente) ----------
    popt, pcov = curve_fit(lin, x_tan, y_tan)
    m, b = popt
    σ_m, σ_b = np.sqrt(np.diag(pcov))
    cov_mb = pcov[0, 1]

    # Bestimmtheitsmaß R²
    y_pred = lin(x_tan, *popt)
    ss_res = np.sum((y_tan - y_pred) ** 2)
    ss_tot = np.sum((y_tan - np.mean(y_tan)) ** 2)
    r2 = 1 - ss_res / ss_tot

    # Tangente über alle Zeiten
    y_tangente = lin(x, *popt)

    # ---------- Schnittpunkt bestimmen ----------
    delta = y - y_tangente
    wechsel = np.where(np.diff(np.sign(delta)))[0]
    if len(wechsel) == 0:
        print("   -> Kein Schnittpunkt gefunden. Überspringe.")
        continue

    idx = wechsel[0]
    x_schnitt = x[idx]
    y_schnitt = y_tangente[idx]

    # ---------- Fehlerfortpflanzung ----------
    σ_T = np.sqrt(
        x_schnitt**2 * σ_m**2 +
        σ_b**2 +
        2 * x_schnitt * cov_mb
    )

    # ---------- Plot ----------
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, lw=2, label="Messwerte")

    # Tangente nur bis kurz nach dem Schnittpunkt zeichnen
    x_tan_plot = x[(x >= x_schnitt - 40) & (x <= x.max())]
    y_tan_plot = lin(x_tan_plot, m, b)
    plt.plot(x_tan_plot, y_tan_plot, "r--", lw=2,
             label=f"Tangente (endet am Schnittpunkt): y = {m:.3f}x + {b:.2f}")

    # Horizontale Linie am Schnittpunkt
    plt.hlines(y_schnitt, x.min(), x_schnitt,
               linestyle=":", lw=2, color="green",
               label=f"Tgef = {y_schnitt:.2f} ± {σ_T:.2f} °C")

    plt.plot(x_schnitt, y_schnitt, "ko", label="Gefrierpunkt")

    plt.xlabel("Zeit / s")
    plt.ylabel("Temperatur / °C")
    plt.title(f"{mess_name}")
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





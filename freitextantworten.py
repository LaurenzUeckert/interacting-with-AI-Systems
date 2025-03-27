import pandas as pd
from textwrap import fill

# Daten einlesen
with_sources = pd.read_csv('final_data/with_sources_ati.csv')
without_sources = pd.read_csv('final_data/without_sources_ati.csv')

# Funktion zur Bereinigung und Formatierung der Freitextantworten
def clean_text(text):
    if pd.isna(text):
        return "Keine Angabe"
    text = str(text).strip()
    if text == "":
        return "Keine Angabe"
    return text

# Funktion zur Analyse und Ausgabe der Freitextantworten
def analyze_free_text(df, group_name):
    print(f"\n{'='*80}")
    print(f"FREITEXTANTWORTEN - GRUPPE: {group_name.upper()}")
    print(f"{'='*80}\n")
    
    # Alle relevanten Freitextspalten identifizieren
    text_columns = [
        'Was hat Sie dazu gebracht der Antwort zu Vertrauen oder nicht zu Vertrauen? (optional)',
        'Haben Sie Vorschläge, wie man die Antworten & deren Glaubwürdigkeit verbessern könnte?',
        'Begründen Sie Ihre Antworten (optional)'
    ]
    
    # Für jede Freitextspalte die Antworten ausgeben
    for col in text_columns:
        if col in df.columns:
            print(f"\n{'#'*40}")
            print(f"THEMA: {col.upper()}")
            print(f"{'#'*40}\n")
            
            # Nicht-leere Antworten filtern und nummeriert ausgeben
            responses = df[col].apply(clean_text)
            non_empty = responses[responses != "Keine Angabe"]
            
            if len(non_empty) > 0:
                for i, (idx, response) in enumerate(non_empty.items(), 1):
                    print(f"Antwort {i}:")
                    print(fill(response, width=80))
                    print("-"*80)
            else:
                print("Keine Freitextantworten in dieser Kategorie")
            print("\n")

# Freitextanalyse für beide Gruppen durchführen
analyze_free_text(with_sources, "Mit Quellen")
analyze_free_text(without_sources, "Ohne Quellen")

# Zusätzlich: ATI-Score Vergleich zwischen den Gruppen
print(f"\n{'='*80}")
print("VERGLEICH ATI-SCORES")
print(f"{'='*80}\n")

print("Durchschnittlicher ATI-Score:")
print(f"- Mit Quellen: {with_sources['ATI_Score'].mean():.2f}")
print(f"- Ohne Quellen: {without_sources['ATI_Score'].mean():.2f}")

# Statistische Signifikanzprüfung
t_stat, p_value = stats.ttest_ind(
    with_sources['ATI_Score'].dropna(),
    without_sources['ATI_Score'].dropna()
)
print(f"\nT-Test Ergebnis: t = {t_stat:.3f}, p = {p_value:.4f}")
if p_value < 0.05:
    print("Der Unterschied ist statistisch signifikant (p < 0.05)")
else:
    print("Der Unterschied ist nicht statistisch signifikant (p ≥ 0.05)")
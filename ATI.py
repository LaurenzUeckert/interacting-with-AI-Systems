import pandas as pd

# Funktion zur Berechnung der Technikaffinität
def calculate_ati_score(row):
    # Kodierung der Antworten
    coding = {
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6
    }
    
    # Umkehrung der negativ formulierten Items (3, 6, 8)
    inverted_items = {
        3: lambda x: 7 - x,  # 6=1, 5=2, 4=3, 3=4, 2=5, 1=6
        6: lambda x: 7 - x,
        8: lambda x: 7 - x
    }
    
    # Extrahiere die Antworten zu den ATI-Fragen
    ati_questions = [
        'Ich beschäftige mich gern genauer mit technischen Systemen.',
        'Ich probiere gern die Funktionen neuer technischer Systeme aus.',
        'In erster Linie beschäftige ich mich mit technischen Systemen, weil ich muss.',
        'Wenn ich ein neues technisches System vor mir habe, probiere ich es intensiv aus.',
        'Ich verbringe sehr gern Zeit mit dem Kennenlernen eines neuen technischen Systems.',
        'Es genügt mir, dass ein technisches System funktioniert, mir ist es egal, wie oder warum.',
        'Ich versuche zu verstehen, wie ein technisches System genau funktioniert.',
        'Es genügt mir, die Grundfunktionen eines technischen Systems zu kennen.',
        'Ich versuche, die Möglichkeiten eines technischen Systems vollständig auszunutzen.'
    ]
    
    scores = []
    for i, question in enumerate(ati_questions, start=1):
        try:
            if i in inverted_items:
                # Invertiere die Antwort für die negativ formulierten Items
                scores.append(inverted_items[i](coding[row[question]]))
            else:
                scores.append(coding[row[question]])
        except KeyError:
            print(f"Fehler: Die Spalte '{question}' wurde nicht gefunden. Bitte überprüfen Sie die Spaltennamen in der CSV-Datei.")
            return None
    
    # Berechne den Mittelwert über alle Items
    return sum(scores) / len(scores)

# Laden der Daten
with_sources = pd.read_csv('formatted_data/with_sources.csv')
without_sources = pd.read_csv('formatted_data/without_sources.csv')

# Überprüfen der Spaltennamen
print("Spalten in with_sources:", with_sources.columns.tolist())
print("Spalten in without_sources:", without_sources.columns.tolist())

# Berechnung der ATI-Scores für beide Datensätze
with_sources['ATI_Score'] = with_sources.apply(calculate_ati_score, axis=1)
without_sources['ATI_Score'] = without_sources.apply(calculate_ati_score, axis=1)

# Entfernen der ATI-Fragen aus den Daten
ati_questions = [
    'Ich beschäftige mich gern genauer mit technischen Systemen.',
    'Ich probiere gern die Funktionen neuer technischer Systeme aus.',
    'In erster Linie beschäftige ich mich mit technischen Systemen, weil ich muss.',
    'Wenn ich ein neues technisches System vor mir habe, probiere ich es intensiv aus.',
    'Ich verbringe sehr gern Zeit mit dem Kennenlernen eines neuen technischen Systems.',
    'Es genügt mir, dass ein technisches System funktioniert, mir ist es egal, wie oder warum.',
    'Ich versuche zu verstehen, wie ein technisches System genau funktioniert.',
    'Es genügt mir, die Grundfunktionen eines technischen Systems zu kennen.',
    'Ich versuche, die Möglichkeiten eines technischen Systems vollständig auszunutzen.'
]

with_sources = with_sources.drop(columns=ati_questions, errors='ignore')
without_sources = without_sources.drop(columns=ati_questions, errors='ignore')

# Speichern der neuen CSV-Dateien
with_sources.to_csv('final_data/with_sources_ati.csv', index=False)
without_sources.to_csv('final_data/without_sources_ati.csv', index=False)

print("ATI-Scores wurden berechnet und die neuen CSV-Dateien wurden gespeichert.")
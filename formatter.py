import os
import pandas as pd
import re

# Ordnerpfad mit den CSV-Dateien
folder_path = 'data'

# Liste aller CSV-Dateien im Ordner abrufen
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Dictionary für die DataFrames erstellen
dataframes_dict = {}

# Alle CSV-Dateien einlesen
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    try:
        df = pd.read_csv(file_path)
        df_name = os.path.splitext(file)[0]
        dataframes_dict[df_name] = df
    except Exception as e:
        print(f"Fehler beim Einlesen von {file}: {e}")

# Standard-Themenreihenfolge (für beide Gruppen gleich)
standard_order = ["CIA", "Wirtschaft", "Gesundheit", "Physik"]

# Basisspaltennamen (die 9 Fragen)
base_questions = [
    "Wie viel Vorwissen haben Sie zu dem Thema des Textes?",
    "Wie Glaubwürdig fanden Sie die Antwort?",
    "Wie klar und verständlich war die Antwort?",
    "Wie sachlich fanden Sie die Antwort?",
    "Wie sehr vertrauen Sie den in der Antwort präsentierten Informationen?",
    "Wie wahrscheinlich ist es, dass die Antwort missverstanden werden könnte?",
    "Wie ausführlich fanden Sie die Antwort?",
    "Wie sicher sind Sie, dass die Antwort korrekt ist?",
    "Begründen Sie ihre Antworten (optional)"
]

def process_group(dfs, group_order):
    # Liste für restrukturierte DataFrames
    restructured_dfs = []
    
    for df in dfs:
        # Dictionary für die restrukturierten Daten
        restructured_data = {}
        
        # Mapping zwischen Gruppenreihenfolge und Standardreihenfolge erstellen
        topic_mapping = {topic: idx for idx, topic in enumerate(group_order)}
        
        # 1. Verarbeite die 4x9 Fragen (nach Standardreihenfolge ordnen)
        for topic in standard_order:
            # Finde den ursprünglichen Index dieses Themas in der Gruppenreihenfolge
            original_idx = topic_mapping.get(topic, 0)
            
            for question in base_questions:
                # Spaltenname im Original-DataFrame
                col_name = f"{question}.{original_idx+1}" if original_idx > 0 else question
                if col_name not in df.columns:
                    col_name = question  # Fallback für erste Frage ohne Suffix
                
                # Neuer Spaltenname (immer nach Standardreihenfolge)
                new_col = f"{topic} - {question}"
                restructured_data[new_col] = df[col_name]
        
        # 2. Füge die restlichen Spalten unverändert hinzu (nicht den Themen zuordnen)
        other_columns = []
        for col in df.columns:
            is_base_question = False
            for q in base_questions:
                if col.startswith(q.split('?')[0]):
                    is_base_question = True
                    break
            if not is_base_question:
                other_columns.append(col)
        
        for col in other_columns:
            restructured_data[col] = df[col]
        
        restructured_dfs.append(pd.DataFrame(restructured_data))
    
    return pd.concat(restructured_dfs, ignore_index=True)

# Daten für Gruppe A verarbeiten (mit Standardreihenfolge)
group_a_dfs = [dataframes_dict[name] for name in ["A1", "A2", "A3", "A4"] if name in dataframes_dict]
with_sources = process_group(group_a_dfs, ["CIA", "Wirtschaft", "Gesundheit", "Physik"])

# Daten für Gruppe B verarbeiten (mit Standardreihenfolge)
group_b_dfs = [dataframes_dict[name] for name in ["B1", "B2", "B3", "B4"] if name in dataframes_dict]
without_sources = process_group(group_b_dfs, ["Wirtschaft", "Physik", "CIA", "Gesundheit"])

# Ausgabeordner erstellen
output_folder = os.path.join(folder_path, "formatted_data")
os.makedirs(output_folder, exist_ok=True)

# Als CSV speichern
with_sources.to_csv(os.path.join(output_folder, "with_sources.csv"), index=False)
without_sources.to_csv(os.path.join(output_folder, "without_sources.csv"), index=False)

print("Daten erfolgreich verarbeitet und gespeichert in:", output_folder)
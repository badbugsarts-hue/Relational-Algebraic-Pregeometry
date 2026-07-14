#!/usr/bin/env python3
import os
import sys

def main():
    src_dir = os.path.join(os.path.dirname(__file__), '..', 'antigravit2', 'src')
    forbidden_words = ['Ramsey', 'Erdős', 'AlphaProof']
    
    found_leakage = False
    
    for root, _, files in os.walk(src_dir):
        for file in files:
            if not file.endswith('.lean'):
                continue
                
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except Exception as e:
                print(f"Fehler beim Lesen von {filepath}: {e}")
                continue
                
            for i, line in enumerate(lines, 1):
                for word in forbidden_words:
                    if word.lower() in line.lower():
                        print(f"ONTOLOGY LEAKAGE DETECTED in {os.path.relpath(filepath, src_dir)}:{i}")
                        print(f"  Verbotenes Wort gefunden: '{word}'")
                        print(f"  In Zeile: {line.strip()}")
                        found_leakage = True

    if found_leakage:
        print("\nERROR: Hard Firewall verletzt. Lean-Code darf keine Stratum-III-Ontologie-Begriffe enthalten.")
        sys.exit(1)
    else:
        print("OK: Firewall-Check bestanden. Keine Ontologie-Leakage im Lean-Kern gefunden.")
        sys.exit(0)

if __name__ == "__main__":
    main()

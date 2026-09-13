import re
import json
import os

def extract_claims(tex_file, output_json):
    if not os.path.exists(tex_file):
        print(f"Error: {tex_file} not found.")
        return

    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find all claims tables
    # Tables often look like:
    # \begin{table}
    # \begin{tabular}...
    # G-01 & Description \catmark{A} & ... \\
    # \end{tabular}
    # \end{table}

    # First, let's just extract every occurrence of a claim identifier followed by its class.
    # We will look for anything that looks like an ID (e.g. K-01, G-02, L12, ONT-01) and has a \catmark near it.
    
    # A simple fallback: Extract all lines containing \catmark
    catmark_lines = [line.strip() for line in content.split('\n') if r'\catmark' in line]
    
    claims = []
    for line in catmark_lines:
        # Clean up line
        clean_line = re.sub(r'\s+', ' ', line)
        # Extract catmarks
        marks = re.findall(r'\\catmark\{([^}]+)\}', clean_line)
        if marks:
            claims.append({
                "context": clean_line,
                "evidence_class": marks[0]
            })

    # Output to JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump({
            "repository": "Relational-Algebraic Pregeometry",
            "version": "4.0",
            "total_claims": len(claims),
            "claims": claims
        }, f, indent=4)
        
    print(f"Successfully extracted {len(claims)} claims into {output_json}")

if __name__ == "__main__":
    tex_path = os.path.join("manuscript", "Relational_Algebraic_Pregeometry_v4_0.tex")
    out_path = "claims.json"
    extract_claims(tex_path, out_path)

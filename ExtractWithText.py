import streamlit as st

def parse_mrz_3lines(lines):
    data = {}
    line1 = lines[0]
    # Extraction brute (10 caractères à partir de la pos 13)
    id_raw = line1[13:23]
    # Nettoyer les '<', garder alphanumérique
    identification = ''.join(ch for ch in id_raw if ch.isalnum())

    # Supprimer 1er caractère s'il est un chiffre (ex : '5WA20353' -> 'WA20353')
    if identification and identification[0].isdigit():
        identification = identification[1:]

    data['Identification'] = identification

    # Date de naissance
    line2 = lines[1]
    date_naissance_raw = line2[0:6]
    yy = int(date_naissance_raw[0:2])
    mm = date_naissance_raw[2:4]
    dd = date_naissance_raw[4:6]
    year_prefix = 2000 if yy <= 24 else 1900
    data['Date de naissance'] = f"{dd}/{mm}/{year_prefix + yy}"

    # Nom / Prénom
    line3 = lines[2]
    noms_prenom = line3.split("<<")
    data['Nom'] = noms_prenom[0].replace('<', ' ').strip()
    data['Prénom'] = noms_prenom[1].replace('<', ' ').strip() if len(noms_prenom) > 1 else ""

    return data

st.title("Extraction Nom, Prénom, Identification, Date de naissance depuis MRZ")

mrz_input = st.text_area("Colle la MRZ (3 lignes)", height=150)

if st.button("Extraire"):
    lines = [l.strip() for l in mrz_input.split('\n') if l.strip()]
    if len(lines) != 3:
        st.error("La MRZ doit contenir exactement 3 lignes.")
    else:
        data = parse_mrz_3lines(lines)
        st.write("Données extraites :")
        st.write(f"**Nom :** {data['Nom']}")
        st.write(f"**Prénom :** {data['Prénom']}")
        st.write(f"**Identification :** {data['Identification']}")
        st.write(f"**Date de naissance :** {data['Date de naissance']}")

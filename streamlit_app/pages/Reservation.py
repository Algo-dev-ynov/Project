import streamlit as st
from datetime import date

st.set_page_config(page_title="Réservation", layout="centered", page_icon="🏠")

st.markdown("""
    <style>
        header { visibility: hidden; }
        .recap-card { background:#f9f9f9; border-radius:12px; padding:16px; margin-bottom:20px; }
        .recap-item { font-size:0.9rem; margin-bottom:6px; }
    </style>
""", unsafe_allow_html=True)

if st.button("← Retour"):
    st.switch_page("pages/Detail.py")

uuid = st.session_state.get('selected_uuid')
place_name = st.session_state.get('place_name', 'Hébergement')
checkin = st.session_state.get('checkin', date.today())
checkout = st.session_state.get('checkout', date.today())
price = st.session_state.get('price', 0)
index = st.session_state.get('selected_index', 1)

nights = (checkout - checkin).days if checkout > checkin else 0

st.markdown("### Réservation")
st.image(f"https://picsum.photos/seed/{index+1}/700/200", use_container_width=True)

st.markdown("### Vos informations")
col1, col2 = st.columns(2)
with col1:
    nom = st.text_input("Nom")
with col2:
    prenom = st.text_input("Prénom")

nb_personnes = st.number_input("Nombre de personnes", min_value=1, max_value=20, value=1)
total = nights * (price or 0) * nb_personnes

st.markdown(f"""
    <div class="recap-card">
        <div class="recap-item">🏠 <b>{place_name}</b></div>
        <div class="recap-item">📅 Arrivée : <b>{checkin}</b></div>
        <div class="recap-item">📅 Départ : <b>{checkout}</b></div>
        <div class="recap-item">👥 {nb_personnes} personne(s)</div>
        <div class="recap-item">🌙 {nights} nuit(s) × {price} € × {nb_personnes} = <b style="color:#FF385C;">{total} €</b></div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

if st.button("Confirmer la réservation", use_container_width=True, type="primary"):
    if nom and prenom:
        st.markdown(f"""
            <div style="background:#d4edda; border-radius:12px; padding:24px; text-align:center; margin-top:16px;">
                <h3 style="color:#155724;">✅ Réservation confirmée !</h3>
                <p style="color:#155724;">Merci <b>{prenom} {nom}</b>, votre réservation pour <b>{place_name}</b> du <b>{checkin}</b> au <b>{checkout}</b> pour <b>{nb_personnes} personne(s)</b> est bien enregistrée.</p>
                <p style="color:#155724; font-size:1.1rem; font-weight:700;">Total : {total} €</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Veuillez remplir votre nom et prénom.")

st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#717171; font-size:0.8rem; padding:16px 0;">
        © 2024 TourismeAir — Données ouvertes <a href="https://datatourisme.fr" style="color:#FF385C;">datatourisme.fr</a>
    </div>
""", unsafe_allow_html=True)
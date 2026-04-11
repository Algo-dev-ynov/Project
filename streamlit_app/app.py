import streamlit as st
import requests

API_URL = "https://flask-api-tourisme.onrender.com"

st.set_page_config(page_title="TourismeAir", layout="wide", page_icon="🏠")

st.markdown("""
    <style>
        .card { border:1px solid #eee; border-radius:12px; overflow:hidden; margin-bottom:12px; }
        .card img { width:100%; height:120px; object-fit:cover; }
        .card-body { padding:8px 10px; }
        .card-body h4 { color:#222; margin:0 0 2px 0; font-size:0.85rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
        .card-body .city { color:#717171; font-size:0.75rem; margin:0 0 4px 0; }
        .card-body .price { font-weight:700; color:#FF385C; margin-top:4px; font-size:0.85rem; }
        .card-body .rating { font-size:0.75rem; color:#222; margin-top:2px; }
        header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='color:#FF385C; margin-bottom:0;'>🏠 TourismeAir</h2>", unsafe_allow_html=True)

cities = requests.get(f"{API_URL}/places/cities").json()
types = requests.get(f"{API_URL}/places/types").json()

col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
with col1:
    search = st.text_input("", placeholder="Rechercher une ville, un lieu...", label_visibility="collapsed")
with col2:
    city = st.selectbox("Ville", ["Toutes"] + sorted([c for c in cities if c]), label_visibility="collapsed")
with col3:
    type_ = st.selectbox("Type", ["Tous"] + sorted([t for t in types if t]), label_visibility="collapsed")
with col4:
    st.button("Rechercher", use_container_width=True)

params = {}
if city != "Toutes":
    params['city'] = city
if type_ != "Tous":
    params['type'] = type_

if search:
    places = requests.get(f"{API_URL}/places/search", params={'label': search}).json()
else:
    places = requests.get(f"{API_URL}/places", params=params).json()

def get_avg_rating(uuid):
    try:
        ratings = requests.get(f"{API_URL}/ratings/{uuid}").json()
        if isinstance(ratings, list) and len(ratings) > 0:
            avg = sum(r.get('rating', 0) for r in ratings) / len(ratings)
            return round(avg, 1)
    except:
        pass
    return None

st.write(f"**{len(places)} lieux disponibles**")

cols = st.columns(4)
for i, place in enumerate(places):
    uuid = place.get('uuid', '')
    avg = get_avg_rating(uuid)
    stars = f"⭐ {avg}/5" if avg else "Pas de note"

    with cols[i % 4]:
        st.markdown(f"""
            <div class="card">
                <img src="https://picsum.photos/seed/{i+1}/400/150" />
                <div class="card-body">
                    <h4>{place.get('label', 'Sans nom')}</h4>
                    <p class="city">{place.get('address', {}).get('addressLocality', '')} {place.get('address', {}).get('postalCode', '')}</p>
                    <p class="rating">{stars}</p>
                    <p class="price">{place.get('price', 'N/A')} €</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Voir", key=f"btn_{uuid}"):
            st.session_state['selected_uuid'] = uuid
            st.session_state['selected_index'] = i
            st.switch_page("pages/Detail.py")


st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#717171; font-size:0.8rem; padding:20px 0;">
        © 2024 TourismeAir — Données ouvertes <a href="https://datatourisme.fr" style="color:#FF385C;">datatourisme.fr</a>
    </div>
""", unsafe_allow_html=True)
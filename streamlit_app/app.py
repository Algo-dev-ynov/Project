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
    st.markdown("**Région**")
    city = st.selectbox("Ville", ["Toutes"] + sorted([c for c in cities if c]), label_visibility="collapsed")
with col3:
    st.markdown("**Type d'hébergement**")
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
                <img src="{place.get('image_url') or f'https://picsum.photos/seed/{i+1}/400/150'}" />
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
            st.switch_page("pages/Detail.py")




# ------------------------------- caht bot ---------------------------------------------------------

st.markdown("---")
st.markdown("### 🤖 Assistant TourismeAir")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ex: 'hotel à Paris', 'je veux réserver un camping'...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    user_lower = user_input.lower()
    
    # Détection intention réservation
    reserve_keywords = ["réserver", "reserver", "réservation", "reservation", "booker", "book"]
    # Détection intention recherche
    search_keywords = ["cherche", "recherche", "trouver", "trouve", "voir", "montrer", "afficher"]
    # Types d'hébergement
    type_keywords = {
        "hotel": "Hotel",
        "hôtel": "Hotel", 
        "camping": "Camping",
        "gite": "SelfCateringAccommodation",
        "gîte": "SelfCateringAccommodation",
        "chambre": "BedAndBreakfast",
        "appartement": "RentalAccommodation",
    }

    intent = None
    detected_type = None
    detected_city = None

    # Détection type
    for kw, val in type_keywords.items():
        if kw in user_lower:
            detected_type = val
            break

    # Détection ville — cherche mot après "à", "a", "en", "sur"
    import re
    city_match = re.search(r'\b(?:à|a|en|sur|près de|pres de)\s+([a-zA-ZÀ-ÿ\-]+)', user_lower)
    if city_match:
        detected_city = city_match.group(1).capitalize()

    # Détection intention
    if any(kw in user_lower for kw in reserve_keywords):
        intent = "reserve"
    elif any(kw in user_lower for kw in search_keywords) or detected_type or detected_city:
        intent = "search"


    # Réponse et action
    if intent == "search":
        params = {}
        if detected_city:
            params["city"] = detected_city
        if detected_type:
            params["type"] = detected_type
        
        results = requests.get(f"{API_URL}/places", params=params).json()
        
        reply = f"Bien reçu ! 🙏 J'ai enregistré votre demande et j'ai trouvé **{len(results)} hébergement(s)**"
        if detected_city:
            reply += f" à **{detected_city}**"
        if detected_type:
            reply += f" de type **{detected_type}**"
        reply += ". Voici les résultats ci-dessous !"
        
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state["chatbot_results"] = results

    elif intent == "reserve":
        reserve_match = re.search(
            r'(?:réserver|reserver|booker|book)\s+(?:l\'|le|la|les|un|une)?\s*(?:hotel|hôtel|camping|gite|gîte|chambre|appartement)?\s*([a-zA-ZÀ-ÿ\s\-]+)',
            user_lower
        )
        label = reserve_match.group(1).strip() if reserve_match else user_input

        search_results = requests.get(f"{API_URL}/places/search", params={"label": label}).json()
        
        if search_results:
            reply = f"Parfait ! 🙏 Merci pour votre demande, je vous redirige vers **{search_results[0].get('label')}** pour finaliser la réservation."
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state["selected_uuid"] = search_results[0].get("uuid")
            st.rerun()
        else:
            reply = "Merci pour votre demande ! 🙏 Pourriez-vous préciser le nom de l'hébergement que vous souhaitez réserver ?"
            st.session_state.messages.append({"role": "assistant", "content": reply})
        
    else:
        reply = "Merci pour votre message ! 🙏 Essayez par exemple : *'je cherche un hôtel à Lyon'* ou *'je veux réserver un camping'*."
        st.session_state.messages.append({"role": "assistant", "content": reply})
    
    st.rerun()

# Affiche les résultats du chatbot si présents
if "chatbot_results" in st.session_state and st.session_state["chatbot_results"]:
    st.markdown("**Résultats de votre recherche :**")
    chat_cols = st.columns(4)
    for i, place in enumerate(st.session_state["chatbot_results"][:8]):
        uuid = place.get('uuid', '')
        with chat_cols[i % 4]:
            st.markdown(f"""
                <div class="card">
                    <img src="{place.get('image_url') or f'https://picsum.photos/seed/{i+50}/400/150'}" />
                    <div class="card-body">
                        <h4>{place.get('label', 'Sans nom')}</h4>
                        <p class="city">{place.get('address', {}).get('addressLocality', '')}</p>
                        <p class="price">{place.get('price', 'N/A')} €</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Voir", key=f"chat_btn_{uuid}_{i}"):
                st.session_state['selected_uuid'] = uuid
                st.switch_page("pages/Detail.py")












st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#717171; font-size:0.8rem; padding:20px 0;">
        © 2024 TourismeAir — Données ouvertes <a href="https://datatourisme.fr" style="color:#FF385C;">datatourisme.fr</a>
    </div>
""", unsafe_allow_html=True)
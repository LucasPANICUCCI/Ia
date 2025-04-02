import streamlit as st
import openai
import re

# Clé API récupérée depuis les secrets (à configurer sur Streamlit Cloud)
openai.api_key = st.secrets["OPENAI_API_KEY"]

def detect_emotion(text):
    text = text.lower()
    if any(word in text for word in ["triste", "vide", "perdu", "manque"]):
        return "tristesse"
    elif any(word in text for word in ["joie", "heureux", "rire", "sourire"]):
        return "joie"
    elif any(word in text for word in ["colère", "énervé", "rage", "fâché"]):
        return "colère"
    elif any(word in text for word in ["solitude", "seul", "isolé", "abandonné"]):
        return "solitude"
    else:
        return "nostalgie"

emotion_prompts = {
    "joie": "a colorful garden full of happy people, sunshine, vibrant flowers",
    "tristesse": "a rainy city street at night, a lone figure under an umbrella, melancholic mood",
    "colère": "a stormy sky above a broken landscape, raw dramatic atmosphere",
    "solitude": "a person sitting alone on a bench, foggy morning, peaceful yet lonely",
    "nostalgie": "a vintage room with faded photographs and sunlight through old curtains"
}

def generate_dalle_image(prompt):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        return response['data'][0]['url']
    except Exception as e:
        st.error(f"Erreur : {e}")
        return None

st.title("🖋️ Exprime ton histoire & 🎨 Illustre ton émotion")
st.markdown("Écris ton histoire (max 2000 mots), nous détectons l’émotion et générons une image avec DALL·E.")
consent = st.checkbox("✅ J’accepte que mon texte soit analysé pour générer une image.")

story = st.text_area("✍️ Ton histoire ici :", height=300, max_chars=15000)
word_count = len(re.findall(r'\b\w+\b', story))
st.write(f"**{word_count} / 2000 mots**")

if st.button("🎨 Générer une image"):
    if not consent:
        st.error("Merci de cocher la case RGPD.")
    elif word_count > 2000:
        st.warning("Le texte dépasse 2000 mots.")
    elif word_count < 10:
        st.warning("Le texte est trop court.")
    else:
        emotion = detect_emotion(story)
        prompt = emotion_prompts.get(emotion, "an abstract emotional scene")
        image_url = generate_dalle_image(prompt)

        st.success(f"Émotion détectée : **{emotion.upper()}**")
        st.markdown(f"**Prompt utilisé :** _{prompt}_")
        if image_url:
            st.image(image_url, caption=f"Image générée par DALL·E (émotion : {emotion})")

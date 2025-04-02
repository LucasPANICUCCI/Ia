import streamlit as st
import openai
import re

# Clé API récupérée depuis les secrets
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
    "joie": "abstract painting evoking joy, vibrant colors, dynamic shapes",
    "tristesse": "abstract art representing sadness, dark tones, flowing forms",
    "colère": "abstract expressionist painting of anger, intense red and black, chaotic strokes",
    "solitude": "abstract painting showing isolation, cool blue palette, empty space",
    "nostalgie": "abstract art of nostalgia, faded tones, memory-like textures"
}

def generate_dalle_image(prompt):
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        st.error(f"Erreur : {e}")
        return None

st.title("🖋️ Exprime ton histoire & 🎨 Illustre ton émotion")
st.markdown("Écris ton histoire (max 2000 mots). Nous détectons l’émotion dominante et générons une **image abstraite** qui l’évoque.")

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
        with st.spinner("Analyse de l’émotion et génération de l’image..."):
            emotion = detect_emotion(story)
            prompt = emotion_prompts.get(emotion, "abstract art representing raw human emotion")
            image_url = generate_dalle_image(prompt)

            st.success(f"Émotion détectée : **{emotion.upper()}**")
            st.markdown(f"**Prompt utilisé :** _{prompt}_")
            if image_url:
                st.image(image_url, caption=f"Image abstraite générée (émotion : {emotion})", use_column_width=True)

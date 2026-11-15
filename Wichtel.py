import random
import streamlit as st

st.set_page_config(page_title="Geheimes Wichteln", page_icon="🎄", layout="centered")

# Schönes Styling für die Buttons
st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🎄 Das geheime Wichteln")
st.write("Willkommen beim diesjährigen Familien-Wichteln! 🎁")

# Original-Teilnehmer (hier gibst du Andre und Andrea ein)
teilnehmer_raw = ["Shirin", "Andre", "Mika", "Andrea"]

# Mapping: Wer zu wem umbenannt wird
name_mapping = {"Andre": "Papi", "Andrea": "Mami"}

# Funktion, um den Namen direkt hübsch anzuzeigen
def get_anzeigename(name):
  return name_mapping.get(name, name)

# Wichtel-Zuordnung im Hintergrund initialisieren
if "wichtel_dict" not in st.session_state:
  gelost_raw = teilnehmer_raw.copy()
  while True:
    random.shuffle(gelost_raw)
    # Prüfen, dass sich niemand selbst zieht (auch mit Mapping geprüft)
    valid = True
    for i in range(len(teilnehmer_raw)):
      u_mapped = get_anzeigename(teilnehmer_raw[i])
      p_mapped = get_anzeigename(gelost_raw[i])
      if u_mapped == p_mapped:
        valid = False
        break
    if valid:
      break

  # Wörterbuch: Gespeichert mit den schönen Anzeigenamen (Papi, Mami, etc.)
  st.session_state.wichtel_dict = {
      get_anzeigename(teilnehmer_raw[i]): get_anzeigename(gelost_raw[i])
      for i in range(len(teilnehmer_raw))
  }
  # Alle erlaubten Eingaben (sowohl echtes Wort als auch Anzeigename)
  st.session_state.erlaubte_namen = [
      t for t in teilnehmer_raw
  ] + list(name_mapping.values())
  st.session_state.bereits_gezogen = []
  st.session_state.aktueller_schritt = "login"

# --- ZUSTAND 1: LOGIN / ZIEHUNG ---
if st.session_state.aktueller_schritt == "login":
  st.markdown("---")
  input_text = st.text_input("Wer bist du? (Deinen Namen eingeben)").strip().capitalize()

  if st.button("Wichtel-Partner enthüllen 🎁", type="primary"):
    if not input_text:
      st.warning("⚠️ Bitte gib deinen Namen ein.")
    elif input_text not in st.session_state.erlaubte_namen:
      st.error("❌ Diesen Namen gibt es nicht in der Wichtel-Liste!")
    else:
      # Einheitlich auf den Anzeigenamen mappen (z.B. Andrea -> Mami)
      standard_name = name_mapping.get(input_text, input_text)

      if standard_name in st.session_state.bereits_gezogen:
        st.warning(
            f"⚠️ Hallo {standard_name}, du hast deinen Wichtel-Partner schon"
            " erfahren! Kein Schummeln! 😉"
        )
      else:
        st.session_state.current_user = standard_name
        st.session_state.current_partner = st.session_state.wichtel_dict[
            standard_name
        ]
        st.session_state.bereits_gezogen.append(standard_name)
        st.session_state.aktueller_schritt = "ergebnis"
        st.rerun()

# --- ZUSTAND 2: ERGEBNIS ANZEIGEN ---
elif st.session_state.aktueller_schritt == "ergebnis":
  st.success(f"🎉 Hallo {st.session_state.current_user}!")
  st.balloons()

  st.markdown(
      f"""
    <div style="padding: 20px; border-radius: 10px; background-color: #f0f2f6; text-align: center; border: 2px solid #ff4b4b;">
        <h3 style="color: #31333F; margin: 0;">Dein geheimer Wichtel-Partner ist:</h3>
        <h1 style="color: #ff4b4b; margin: 10px 0 0 0;">🤫 {st.session_state.current_partner}</h1>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.write("")
  if st.button("🔄 Nächste Person / Bildschirm übergeben", type="primary"):
    # Prüfen, ob alle 4 Personen durch sind
    anzeigenamen_liste = [
        get_anzeigename(t) for t in teilnehmer_raw
    ]
    if len(st.session_state.bereits_gezogen) == len(anzeigenamen_liste):
      st.session_state.aktueller_schritt = "ende"
    else:
      st.session_state.aktueller_schritt = "login"
    st.rerun()

# --- ZUSTAND 3: ENDE / ÜBERSICHT ---
elif st.session_state.aktueller_schritt == "ende":
  st.balloons()
  st.markdown("---")
  st.header("✨ Alle Wichtel wurden erfolgreich zugewiesen! 🎄")
  st.write(
      "Falls jemand vergessen hat, wen er gezogen hat, wähle hier den Namen"
      " aus:"
  )

  anzeigenamen_liste = [get_anzeigename(t) for t in teilnehmer_raw]
  selected_person = st.selectbox(
      "Namen auswählen:", ["--- Bitte wählen ---"] + anzeigenamen_liste
  )

  if selected_person != "--- Bitte wählen ---":
    partner_reveal = st.session_state.wichtel_dict[selected_person]
    st.info(f"🤫 **{selected_person}**, du beschenkst: **{partner_reveal}**")

  st.markdown("---")
  if st.button("🔄 Spiel zurücksetzen / Neu starten"):
    for key in list(st.session_state.keys()):
      del st.session_state[key]
    st.rerun()
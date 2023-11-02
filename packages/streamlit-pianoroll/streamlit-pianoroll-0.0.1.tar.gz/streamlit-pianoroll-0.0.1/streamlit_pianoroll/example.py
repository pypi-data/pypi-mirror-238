import streamlit as st

from streamlit_pianoroll import pianoroll

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/example.py`

st.subheader("Component with Piano Rolls!")

# Create an instance of our component with a constant `name` arg, and
# print its output value.

notes = []
for it in range(20):
    end_time = it * 0.25 + 0.1
    note = {
        "pitch": 50 + it,
        "startTime": it * 0.25,
        "endTime": end_time,
        "velocity": 60 + 3 * it,
    }
    notes.append(note)

TWINKLE_TWINKLE = {
    "totalTime": end_time,
    "notes": notes,
}

for jt in range(2):
    st.markdown(f"### Another one {jt}")
    num_clicks = pianoroll(note_sequence=TWINKLE_TWINKLE, key=jt)
st.markdown("You've clicked %s times!" % int(num_clicks))

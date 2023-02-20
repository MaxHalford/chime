"""A soundboard made with streamlit."""

import chime
import streamlit as st

"""
# `chime` soundboard 🎶

This soundboard allows you to listen to the sounds available for each theme in the Python
[`chime`](https://github.com/MaxHalford/chime/) package. Feel welcome to
[open a pull request](https://github.com/MaxHalford/chime/compare) if you wish to contribute a new
theme. 🤗
"""

for i, theme in enumerate(chime.themes()):
    if i:
        st.markdown('---')
    st.header(theme)

    for event in ['success', 'warning', 'error', 'info']:
        st.subheader(event)
        with open(chime.themes_dir().joinpath(f'{theme}/{event}.wav'), 'rb') as wav:
            st.audio(wav.read())

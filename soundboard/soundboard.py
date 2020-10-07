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

for theme in chime.themes():
    st.header(theme)

    for event in ['success', 'warning', 'error', 'info']:
        if st.button(event, key=f'{theme}/{event}'):
            chime.theme(theme)
            try:
                eval(f'chime.{event}(sync=True)')
            except Exception as e:
                st.write(e)

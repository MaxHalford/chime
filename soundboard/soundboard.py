"""A soundboard made with streamlit."""

import chime
import streamlit as st

st.title('`chime` soundboard')

st.markdown('This soundboard allows you to listen to each sound available in the [`chime`](https://github.com/MaxHalford/chime/) package. Feel welcome to [open a pull request](https://github.com/MaxHalford/chime/compare) if you wish to contribute a new theme.')

for theme in chime.themes():
    st.header(theme)

    for event in ['success', 'warning', 'error', 'info']:
        if st.button(event, key=f'{theme}/{event}'):
            chime.theme(theme)
            eval(f'chime.{event}()')

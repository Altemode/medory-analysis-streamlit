import pandas as pd 
import streamlit as st
import gettext
_ = gettext.gettext

from os import system, path



from streamlit_metrics import metric, metric_row
from streamlit_ace import st_ace

import pandas as pd
import numpy as np
import altair as alt

language = st.sidebar.selectbox('', ['eng', 'gr'])
try:
  localizator = gettext.translation('base', localedir='locales', languages=[language])
  localizator.install()
  _ = localizator.gettext 
except:
    pass



POT = st.sidebar.button(('POT generate'))
MO = st.sidebar.button('MO generate')
if POT:
    system(f'cd {path.dirname(path.realpath(__file__))} & /usr/lib/python3.10/Tools/i18n/pygettext.py -d base -o locales/base.pot Introduction.py pages/2_Insert_User.py pages/3_Insert_Medical_Data.py')
    system(f'cd {path.dirname(path.realpath(__file__))} && cp locales/base.pot locales/eng/LC_MESSAGES/base.po')

if MO:
    system(f'cd {path.dirname(path.realpath(__file__))} && msgfmt -o locales/eng/LC_MESSAGES/base.mo locales/eng/LC_MESSAGES/base')


st.title(_("Αρχική σελίδα - περιγραφή εφαρμογής!"))

st.sidebar.title(":memo: Editor settings")

THEMES = [
    "ambiance", "chaos", "chrome", "clouds", "clouds_midnight", "cobalt", "crimson_editor", "dawn",
    "dracula", "dreamweaver", "eclipse", "github", "gob", "gruvbox", "idle_fingers", "iplastic",
    "katzenmilch", "kr_theme", "kuroir", "merbivore", "merbivore_soft", "mono_industrial", "monokai",
    "nord_dark", "pastel_on_dark", "solarized_dark", "solarized_light", "sqlserver", "terminal",
    "textmate", "tomorrow", "tomorrow_night", "tomorrow_night_blue", "tomorrow_night_bright",
    "tomorrow_night_eighties", "twilight", "vibrant_ink", "xcode"
]

KEYBINDINGS = ["emacs", "sublime", "vim", "vscode"]

display, editor = st.columns((2, 1))

INITIAL_CODE = """st.header("Streamlit Sandbox")
st.write("Play with Streamlit live in the browser!")
table_data = {'Column 1': [1, 2], 'Column 2': [3, 4]}
st.write(pd.DataFrame(data=table_data))
"""

with editor:
    st.write('### Code editor')
    code = st_ace(
        value=INITIAL_CODE,
        language="python",
        placeholder="st.header('Hello world!')",
        theme=st.sidebar.selectbox("Theme", options=THEMES, index=26),
        keybinding=st.sidebar.selectbox("Keybinding mode", options=KEYBINDINGS, index=3),
        font_size=st.sidebar.slider("Font size", 5, 24, 14),
        tab_size=st.sidebar.slider("Tab size", 1, 8, 4),
        wrap=st.sidebar.checkbox("Wrap lines", value=False),
        show_gutter=True,
        show_print_margin=True,
        auto_update=False,
        readonly=False,
        key="ace-editor"
    )
    st.write('Hit `CTRL+ENTER` to refresh')
    st.write('*Remember to save your code separately!*')

with display:
    exec(code)

with st.sidebar:
    libraries_available = st.expander('Available Libraries')
    with libraries_available:
        st.write("""
        * Pandas (pd)
        * Numpy (np)
        * Altair (alt)
        * Bokeh
        * Plotly
        [Need something else?](https://github.com/samdobson/streamlit-sandbox/issues/new)
        """)
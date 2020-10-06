# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% slideshow={"slide_type": "slide"} hideCode=false hidePrompt=false hideOutput=true
# project name: code-bol-2019
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

# %% hidePrompt=false hideCode=false hide_input=false slideshow={"slide_type": "slide"} hideOutput=true
from useful_scit.imps import *
import prototipo_elecciones_bol.visualizacion_interactiva_2019.visualizacion_interactiva_2019_lfc as lfc
from prototipo_elecciones_bol.\
    visualizacion_interactiva_2019.\
    visualizacion_interactiva_2019_lfc import _f
import bokeh
import bokeh.plotting
import bokeh.io
import bokeh.models
import bokeh.palettes



from sqlalchemy import create_engine
# %% hideCode=false hidePrompt=false slideshow={"slide_type": "skip"} hideOutput=true
# def main():
# %% hideCode=false hidePrompt=false slideshow={"slide_type": "skip"} hideOutput=true
engine = lfc.get_engine()
df_rec = lfc.get_df_rec(engine)
ds = lfc.get_ds(df_rec)
ops = {'df':df_rec,'ds':ds}
# %% hideCode=false hidePrompt=false slideshow={"slide_type": "skip"} hideOutput=true hide_input=false
# %% [markdown] hidePrompt=false hideCode=false
# # Diferencia MAS - CC 

# %% slideshow={"slide_type": "slide"} tags=["to_remove"] hideCode=false hideOutput=false hidePrompt=false
_f('MAS-CC',ops)

# %% [markdown] hidePrompt=false hideCode=false
# # Votos MAS

# %% slideshow={"slide_type": "skip"} hideCode=false hidePrompt=false hide_input=false
_f("MAS",ops)
# %% [markdown] hideCode=false hidePrompt=false
# # Votos CC

# %% hideCode=false hidePrompt=false
_f("CC",ops)

# %% [markdown] hideCode=false hidePrompt=false
# # Votos PDC

# %% hideCode=false hidePrompt=false
_f('PDC',ops)

# %% [markdown] hideCode=false hidePrompt=false
# # Exportar

# %% hideCode=false hidePrompt=false slideshow={"slide_type": "skip"} hide_input=false
# !jupyter nbconvert --to hide_code_html visualizacion_interactiva_2019.ipynb
# # !jupyter nbconvert --TagRemovePreprocessor.remove_input_tags={\"to_remove\"} --to html visualizacion_interactiva_2019.ipynb
# # !open visualizacion_interactiva_2019.slides.html
# !open visualizacion_interactiva_2019.html
# %% hideCode=false hidePrompt=false hide_input=false
# !jupyter nbconvert --to slides --reveal-prefix reveal.js visualizacion_interactiva_2019.ipynb
# !open visualizacion_interactiva_2019.slides.html
# %% hideCode=false hidePrompt=false
# %% hideCode=false hidePrompt=false
# %% hideCode=false hidePrompt=false
# %% hideCode=false hidePrompt=false
# %% hideCode=false hidePrompt=false
# %% hideCode=false hidePrompt=false
# %% hideCode=false hidePrompt=false
# %% hideCode=false hidePrompt=false



# %% hideCode=false hidePrompt=false































# %% hideCode=false hidePrompt=false



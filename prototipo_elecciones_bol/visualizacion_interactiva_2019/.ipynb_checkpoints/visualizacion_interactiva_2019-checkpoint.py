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

# %%
# project name: code-bol-2019
# created by diego aliaga daliaga_at_chacaltaya.edu.bo

# %%
from useful_scit.imps import *
import visualizacion_interactiva_2019.visualizacion_interactiva_2019_lfc as lfc
import bokeh
import bokeh.plotting
import bokeh.io
import bokeh.models
import bokeh.palettes



from sqlalchemy import create_engine
# %%
# def main():
# %%
engine = lfc.get_engine()
df_rec = lfc.get_df_rec(engine)
# %%
ds = lfc.get_ds(df_rec)
# %%
# %%

bokeh.io.output_notebook()
cdf = bokeh.models.ColumnDataSource(df_rec)
plt_size = 500

var = 'MAS-CC'
f,f1 = lfc.get_double_plot(var,df_rec,ds,cdf)
gp = bokeh.plotting.gridplot([[f,f1]], plot_height=plt_size, plot_width=plt_size)

var = 'MAS'
f,f1 = lfc.get_double_plot(var,df_rec,ds,cdf)
gp1 = bokeh.plotting.gridplot([[f,f1]], plot_height=plt_size, plot_width=plt_size)

var = 'CC'
f,f1 = lfc.get_double_plot(var,df_rec,ds,cdf)
gp2 = bokeh.plotting.gridplot([[f,f1]], plot_height=plt_size, plot_width=plt_size)

var = 'PDC'
f,f1 = lfc.get_double_plot(var,df_rec,ds,cdf)

gp3 = bokeh.plotting.gridplot([[f,f1]], plot_height=plt_size, plot_width=plt_size)

bokeh.plotting.show(bokeh.plotting.Column(gp,gp1,gp2,gp3))
# bokeh.plotting.show(f1)
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%



# %%



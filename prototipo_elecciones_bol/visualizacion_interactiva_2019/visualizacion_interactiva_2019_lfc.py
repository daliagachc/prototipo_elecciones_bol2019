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
from useful_scit.imps import *
from sqlalchemy import create_engine
import bokeh
import bokeh.transform
import bokeh.models
import bokeh.plotting
import bokeh.tile_providers
import bokeh.palettes

# noinspection PyStatementEffect,PyTrailingSemicolon
plt;
# %%

LOCS = ['CC', 'MAS', 'PDC', 'MAS-CC']

def get_borders(ds):
    delta_x = (ds['x'][2] - ds['x'][1]).item() / 2
    delta_y = (ds['y'][2] - ds['y'][1]).item() / 2
    x__min = ds['x'].min().item() - delta_x
    y__min = ds['y'].min().item() - delta_y
    x__max = ds['x'].max().item() + delta_x
    y__max = ds['y'].max().item() + delta_y
    return x__max, x__min, y__max, y__min


# noinspection PyUnresolvedReferences
var_dic = {
    'MAS': {
        'pal':bokeh.palettes.YlGnBu[9][::-1],
        'min':0,
        'max':100,
        'col':'MAS'

    },
    'CC': {
        'pal': bokeh.palettes.YlOrRd[9][::-1],
        'min': 0,
        'max': 100,
        'col':'CC'

    },
    'PDC': {
        'pal': bokeh.palettes.YlGn[9][::-1],
        'min': 0,
        'max': 40,
        'col': 'PDC'

    },
    'MAS-CC': {
        'pal': bokeh.palettes.RdYlBu[11][::-1],
        'min': -100,
        'max': 100,
        'col': 'mmc'

    }
}

def get_engine():
    engine = create_engine(
        'mysql+mysqlconnector://root:1045@127.0.0.1/db_bol_19')
    return engine


def get_df_rec(engine):
    sql = """# noinspection SqlNoDataSourceInspectionForFile

        # noinspection SqlNoDataSourceInspection

select t1.*, x ,y,density,latitud,longitud
    from (select *
          from zz100_comp_4466
          where País='Bolivia' and `Votos Válidos`>0 and valid=1
          # group by id_rec
         ) t1
             join estad_nac t2 on t1.id_rec = t2.id_rec"""
    df = pd.read_sql(sql, engine)
    df = df.rename({'MAS - IPSP': 'MAS', 'dmcp': 'MAS-CC'}, axis=1)
    vv = 'Votos Válidos'
    mas = 'MAS'
    cc = 'CC'
    pdc = 'PDC'
    # noinspection PyUnusedLocal
    mmc = 'MAS-CC'

    parties = [mas, cc, pdc]
    for p in parties:
        df[p] = df[p] / df[vv] * 100

    res = ll_to_cart(df)
    df['gx'] = res[0]
    df['gy'] = res[1]

    _locs = LOCS
    locs = ['x', 'y', 'density', 'latitud', 'longitud', 'gx', 'gy']
    names = ['Departamento', 'Provincia', 'Municipio', 'Localidad', 'Recinto']
    cols = ['id_rec', *names, *_locs, *locs]

    dfg = df.groupby('id_rec')
    df_rec = dfg[_locs].mean()
    df_rec[locs] = dfg[locs].mean()
    df_rec[names] = dfg[names].first()
    df_rec = df_rec.sort_values('density')
    df_rec['mmc'] = df_rec['MAS-CC']

    return df_rec


def ll_to_cart(df):
    from pyproj import Transformer
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857",
                                       always_xy=True)
    res = transformer.transform(
        df['longitud'].values, df['latitud'].values
    )
    return res


def get_ds(df_rec):
    ds = df_rec[['x', 'y', *LOCS]].copy()
    _r = 1
    ds['xr'] = myround(ds['x'], _r)
    ds['yr'] = myround(ds['y'], _r)
    ds = ds.groupby(['xr', 'yr']).mean()
    xm, ym = ds.reset_index()[['xr', 'yr']].min()
    xM, yM = ds.reset_index()[['xr', 'yr']].max()
    xx = np.arange(xm, xM, _r)
    yy = np.arange(ym, yM, _r)
    dx, dy = np.meshgrid(xx, yy)
    # %%
    from scipy.interpolate import griddata
    da_list = []
    for l in LOCS:
        res = griddata(
            ds.reset_index()[['xr', 'yr']].values,
            ds[l].values,
            (dx, dy)
        )
        # %%

        # noinspection PyTypeChecker
        da = xr.DataArray(res, coords=[yy, xx], dims=['y', 'x'], name=l)

        da = da.coarsen(x=10, y=10, boundary='trim').mean()
        da.name = l
        da_list.append(da)
    # %%
    ds = xr.merge(da_list)
    x__max, x__min, y__max, y__min = get_borders(ds)
    ds['xmax'] = x__max
    ds['xmin'] = x__min
    ds['ymax'] = y__max
    ds['ymin'] = y__min
    return ds


def get_double_plot(var,df_rec,ds, cdf):
    dic = var_dic[var]
    # cdf = bokeh.models.ColumnDataSource(df_rec)
    cm = bokeh.transform.linear_cmap(var,
                                     palette=dic['pal'],
                                     low=dic['min'], high=dic['max'])

    TOOLS = "pan,wheel_zoom," \
            "box_zoom," \
            "reset,box_select,"

    hover = bokeh.models.tools.HoverTool(
        tooltips=[
            # ("Name", "@density"),
            # ("Gender", "@latitud"),
            ("Mun:", "@Municipio"),
            ('Loc:', "@Localidad"),
            ('Rec:', "@Recinto"),
            (f"{var}", f"@{dic['col']}"),
            ("density", "@density")
        ],
        names=['smap', 'scarto']

    )

    pst = bokeh.models.tools.LassoSelectTool(names=['smap', 'scarto'])
    # plot 1
    f = map_var(TOOLS, cm, cdf, pst, hover, var)
    f1 = cart_var(TOOLS, cm, cdf, pst, hover, var, ds)
    return f,f1

def myround(x, base=5):
    return base * round(x / base)

def map_var(TOOLS,cm,cdf,pst,hover,var):
    f = bokeh.plotting.figure(
        tools=TOOLS,
        x_axis_type='mercator',
        y_axis_type='mercator',
        output_backend="webgl"
    )
    # noinspection PyUnresolvedReferences
    tile_provider = bokeh.tile_providers.get_provider(
        bokeh.tile_providers.Vendors.CARTODBPOSITRON)
    f.add_tile(tile_provider)
    f.scatter('gx', 'gy',
              # radius='rad',
              size=7,
              fill_color=cm,
              # fill_alpha=0.6,
              source=cdf,
              line_alpha=0.1,
              line_color="black",
              name='smap'
              )
    f.add_tools(pst)

    color_bar = bokeh.models.ColorBar(
        color_mapper=cm['transform'],
        # width=40,
        # location=(0, 0),
        title=var,
        # ticker=bokeh.models.ContinuousTicker(),
        title_standoff=10,
        orientation='horizontal'
    )

    f.add_layout(color_bar, 'center')
    f.add_tools(hover)
    return f

def cart_var(TOOLS, cm, cdf, pst, hover, var, ds):
    f1 = bokeh.plotting.figure(
        tools=TOOLS,
        output_backend="webgl"
    )
    f1.add_tools(pst)

    f1.image(
        image=[ds[var].values],
        x=ds['xmin'].item(),
        y=ds['ymin'].item(),
        dw=(ds['xmax'] - ds['xmin']).item(),
        dh=(ds['ymax'] - ds['ymin']).item(),
        color_mapper=cm['transform']
    )

    f1.scatter(x='x', y='y', source=cdf,
               size=6,
               fill_color=cm,
               line_alpha=0.5,
               line_color="black",
               name='scarto'
               )

    f1.add_tools(hover)



    return f1

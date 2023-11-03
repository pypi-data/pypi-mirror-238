import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

from interpretable.ml.classify import get_test_scores
from interpretable.ml.io import read_models

## evaluate metrics
def plot_metrics(
    data,
    inputs,
    estimators,
    plot: bool=False,
    ) -> pd.DataFrame:
    """Plot performance metrics.

    Args:
        plot (bool, optional): make plots. Defaults to False.

    Returns:
        pd.DataFrame: output data.
    """
        
    df2=get_test_scores(estimators)
    df2.loc[(df2['variable']=='average precision'),'value reference']=sum(data[inputs['coly']])/len(data[inputs['coly']])
    if plot:
        from roux.lib.str import linebreaker
        df3=df2.assign(model=lambda df: df['model'].apply(lambda x : linebreaker(x,60,)))
        
        _,ax=plt.subplots(figsize=[3,3])
        sns.pointplot(
            data=df3,
            y='variable',
            x='value',
            hue='model',
            join=False,
            dodge=0.2,
            ax=ax,
            )
        ax.axvline(0.5,linestyle=":",
                   color='k',
                  label='reference: accuracy')
        ax.axvline(sum(data[inputs['coly']])/len(data[inputs['coly']]),linestyle=":",
                   color='b',
                  label='reference: precision')
        ax.legend(bbox_to_anchor=[1,1])
        ax.set(xlim=[-0.1,1.1])
        sns.despine(trim=False)
        ax.grid(axis='y',color='lightgray',lw=0.25)
    return df2

# interpret 
def plot_feature_predictive_power(
    df3: pd.DataFrame,
    ax: plt.Axes=None,
    figsize: list=[3,3],
    **kws,
    ) -> plt.Axes:
    """Plot feature-wise predictive power.

    Args:
        df3 (pd.DataFrame): input data.
        ax (plt.Axes, optional): axes object. Defaults to None.
        figsize (list, optional): figure size. Defaults to [3,3].

    Returns:
        plt.Axes: output.
    """

    df4=df3.rd.filter_rows({'variable':'ROC AUC'}).rd.groupby_sort_values(col_groupby='feature',
                     col_sortby='value',
                     ascending=False)
    if ax is None:
        _,ax=plt.subplots(figsize=figsize)
    sns.pointplot(data=df3,
                 y='feature',
                 x='value',
                 hue='variable',
                  order=df4['feature'].unique(),
                 join=False,
                  ax=ax,
                 )
    ax.legend(bbox_to_anchor=[1,1])
    ax.axvline(0.5, linestyle=':', color='lightgray')
    return ax

def plot_feature_ranks(
    df2: pd.DataFrame,
    ):
    fig,ax=plt.subplots(figsize=[2,2])
    for c in df2.filter(like=" rank"):    
        sns.scatterplot(
            data=df2,
            x=c.replace(' rank',' rescaled'),
            y=c,
            label=c.replace(' rank',''),
            ax=ax,
        )
    ax.legend(bbox_to_anchor=[1.5,1])
    ax.set(
        xlabel='Rescaled score',
        ylabel='Rank',
        )
    ## annotations
    colvalue='median(|SHAP value|)'
    from roux.viz.annot import annot_side
    ax=annot_side(ax=ax,
               df1=df2.sort_values(f'{colvalue} rank').head(5),
               colx=f'{colvalue} rescaled',coly=f'{colvalue} rank',cols='feature',length_axhline=1.3)
    ax.invert_yaxis() 
    sns.despine(trim=False)
    return ax

def plot_feature_contributions(
    data,
    kws_plot,
    vmax=0.2,
    vmin=-0.2,
    figsize=[4,4],
    ):
    data[kws_plot['swarmplot']['x']]=data[kws_plot['swarmplot']['x']].round(12)
    from roux.viz.colors import get_val2color,make_cmap,get_colors_default
    cs,cmap_=get_val2color(data[kws_plot['colcolor']],vmin=vmin, vmax=vmax, cmap=make_cmap(get_colors_default()[:3][::-1]))
    cmap_={f"{k:.1f}":cmap_[k] for k in sorted(cmap_.keys())[::-1]}
    data['color']=data[kws_plot['colcolor']].map(cs)
    # data.head(1)

    fig,ax=plt.subplots(figsize=figsize)
    sns.swarmplot(
        data=data,
        dodge=True,
        alpha=0.1,
        s=12,
        ec='none',
        ax=ax,
        **kws_plot['swarmplot'],
    )
    data1=data.copy()
    from roux.viz.ax_ import get_ticklabel_position
    data1['y']=data1[kws_plot['swarmplot']['y']].map(get_ticklabel_position(ax,'y'))
    df_=pd.concat({s:pd.DataFrame(ax.collections[i].get_offsets(),columns=['x swarm','y swarm']) for i,s in enumerate(kws_plot['swarmplot']['order'])},
                  axis=0,
                  names=[kws_plot['swarmplot']['y']],
                 ).reset_index(0)
    df_['y']=df_['y swarm'].apply(round)
    df_[kws_plot['swarmplot']['x']]=df_['x swarm'].round(12)
    data1=df_.log.merge(right=data1,
                  on=['y',
                      kws_plot['swarmplot']['y'],
                      kws_plot['swarmplot']['x']],
                  how='inner',
    #               validate="1:1",
                  )
    assert(len(data1)==len(df_))
    _=data1.apply(lambda x: ax.scatter([x[kws_plot['swarmplot']['x']]],
                                  [x['y swarm']],
                                  color=x['color'],
                                  s=200,
                                  ),axis=1)
    _=data1.sort_values('feature').apply(lambda x: ax.text(x[kws_plot['swarmplot']['x']],
                                  x['y swarm'],
                                  s=x['feature'],ha='center',va='center',
                                  ),axis=1)
    from roux.viz.ax_ import set_legend_custom
    ax=set_legend_custom(
        ax=ax.twinx(),
        legend2param=cmap_,
        param='color',
        lw=1,
        marker='o',
        markerfacecolor=True,
        size=12,
        loc='lower left',
        bbox_to_anchor=[1,0],
        title=f" feat. contri. ({kws_plot['colcolor']})",
        title_ha='left',
    )
    ax.set(
        xlabel='Feature Z-score',
        ylabel=None,)
    sns.despine(trim=False)
    ax.grid(axis='y',color='lightgray',lw=0.25)
    plt.axis('off')
    return ax
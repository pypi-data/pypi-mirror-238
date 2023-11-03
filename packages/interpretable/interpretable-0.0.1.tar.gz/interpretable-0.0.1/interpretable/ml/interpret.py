## logging
from tqdm import tqdm
## data
import pandas as pd
import numpy as np
## visualizations
import matplotlib.pyplot as plt
import seaborn as sns

import roux.lib.df as rd
from roux.lib.io import to_table

def get_feature_predictive_power(
    d0: dict,
    df01: pd.DataFrame,
    n_splits: int=5, 
    n_repeats: int=10,
    random_state: int=None,
    plot: bool=False,
    drop_na: bool=False,
    **kws,
    ) -> pd.DataFrame:
    """get_feature_predictive_power _summary_

    Notes: 
        x-values should be scale and sign agnostic.

    Args:
        d0 (dict): input dictionary.
        df01 (pd.DataFrame): input data, 
        n_splits (int, optional): number of splits. Defaults to 5.
        n_repeats (int, optional): number of repeats. Defaults to 10.
        random_state (int, optional): random state. Defaults to None.
        plot (bool, optional): plot. Defaults to False.
        drop_na (bool, optional): drop missing values. Defaults to False.

    Returns:
        pd.DataFrame: output data.
    """
    if random_state is None: logging.warning(f"random_state is None")
    from sklearn.metrics import average_precision_score,roc_auc_score
    from sklearn.model_selection import StratifiedKFold,RepeatedStratifiedKFold

    d2={}
    for colx in tqdm(d0['cols_x']):
        df1=df01.loc[:,[d0['coly'],colx]]
        if drop_na:
            df1=df1.dropna() 
        if df1[d0['coly']].nunique()==1: continue
        if sum(df1[d0['coly']]==True)<5: continue
        if sum(df1[d0['coly']]==False)<5: continue        
        # if perc(df1[d0['coly']])>90: continue
        # if perc(df1[d0['coly']])<10: continue
        if df1[colx].nunique()==1: continue
        cv = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=random_state,**kws)
        d1={i: ids for i,(_, ids) in enumerate(cv.split(df1[colx], df1[d0['coly']]))}
        df2=pd.DataFrame({'cv #':range(cv.get_n_splits())})
        if roc_auc_score(df1[d0['coly']], df1[colx])<roc_auc_score(df1[d0['coly']], -df1[colx]):
#             df1[d0['coly']]=~df1[d0['coly']]
            df1[colx]=-df1[colx]
        try:
            df2['ROC AUC']=df2['cv #'].apply(lambda x: roc_auc_score(df1.iloc[d1[x],:][d0['coly']],
                                                                     df1.iloc[d1[x],:][colx]))
            df2['average precision']=df2['cv #'].apply(lambda x: average_precision_score(df1.iloc[d1[x],:][d0['coly']],
                                                                                         df1.iloc[d1[x],:][colx]))
        except:
            print(df1)
        d2[colx]=df2.melt(id_vars='cv #',value_vars=['ROC AUC','average precision'])

    df3=pd.concat(d2,axis=0,names=['feature']).reset_index(0)
    if plot:
        from interpretable.viz.ml import plot_feature_predictive_power
        plot_feature_predictive_power(df3)
    return df3

def get_feature_importances(
    estimatorn2grid_search: dict,
    X: pd.DataFrame,
    y: pd.Series,
    scoring: str='roc_auc',
    n_repeats: int=20,
    n_jobs: int=6,
    random_state: int=None,
    plot: bool=False,
    test: bool=False,
   **kws) -> pd.DataFrame:
    """Feature importances.

    Args:
        estimatorn2grid_search (dict): map between estimator name and grid search object. 
        X (pd.DataFrame): X matrix.
        y (pd.Series): y vector.
        scoring (str, optional): scoring type. Defaults to 'roc_auc'.
        n_repeats (int, optional): number of repeats. Defaults to 20.
        n_jobs (int, optional): number of cores. Defaults to 6.
        random_state (int, optional): random state. Defaults to None.
        plot (bool, optional): plot. Defaults to False.
        test (bool, optional): test mode. Defaults to False.

    Returns:
        pd.DataFrame: output data.
    """
    if random_state is None: logging.warning(f"random_state is None")    
    def plot_(df,ax=None):
        if ax is None:
            fig,ax=plt.subplots(figsize=[4,(df['estimator'].nunique()*0.5)+2])
        dplot=df.rd.groupby_sort_values(
             col_groupby=['estimator','feature'],
             col_sortby='importance',
             func='mean', ascending=False
            )
        dplot=dplot.loc[(dplot['importance']!=0),:]

        sns.pointplot(data=dplot,
              x='importance',
              y='feature',
              hue='estimator',
             linestyles=' ',
              markers='o',
              # alpha=0.1,
              dodge=True,
              # scatter_kws = {'facecolors':'none'},
              ax=ax
             )
        return ax
    
    dn2df={}
    for k in tqdm(estimatorn2grid_search.keys()):
        from sklearn.inspection import permutation_importance
        r = permutation_importance(estimator=estimatorn2grid_search[k].best_estimator_, 
                                   X=X, y=y,
                                   scoring=scoring,
                                   n_repeats=n_repeats,
                                   n_jobs=n_jobs,
                                   random_state=random_state,
                                   **kws,
                                  )
        df=pd.DataFrame(r.importances)
        df['feature']=X.columns
        dn2df[k]=df.melt(id_vars=['feature'],value_vars=range(n_repeats),
            var_name='permutation #',
            value_name='importance',
           )
    df2=pd.concat(dn2df,axis=0,names=['estimator']).reset_index(0)
    if plot:
        plot_(df2)
    return df2

def get_partial_dependence(
    estimatorn2grid_search: dict,
    X: pd.DataFrame,
    y: pd.Series,
    test:bool=False,
    ) -> pd.DataFrame:
    """Partial dependence.

    Args:
        estimatorn2grid_search (dict): map between estimator name and grid search object.
        X (pd.DataFrame): X matrix.
        y (pd.Series): y vector.

    Returns:
        pd.DataFrame: output data.
    """
    df3=pd.DataFrame({'feature #':range(len(X.columns)),
                     'feature':X.columns})

    def apply_(featuren,featurei,estimatorn2grid_search):
        from sklearn.inspection import partial_dependence
        dn2df={}
        for k in estimatorn2grid_search:
            t=partial_dependence(estimator=estimatorn2grid_search[k].best_estimator_,
                                 X=X,
                                 features=[featurei],
                                 response_method='predict_proba',
                                 method='brute',
                                 kind='average',
                                 percentiles=[0,1],
                                 grid_resolution=100,
                                 )
            dn2df[k]=pd.DataFrame({k:v[0] for k,v in t.items()})
        df1=pd.concat(dn2df,axis=0,names=['estimator']).reset_index()
        df1['feature']=featuren
        return df1.rd.clean()
    if test: print(df3)
    df4=df3.groupby(['feature','feature #',],as_index=False).apply(lambda df:apply_(featuren=df.name[0],
                                                                                featurei=df.name[1],
                                                                                estimatorn2grid_search=estimatorn2grid_search)).reset_index(drop=True)
    
    return df4

def interpret(
    input_dir_path,
    output_dir_path,
    keys=['predictive power','feature importances','partial dependence','feature contributions'],
    random_state=None,
    plot=False,
    test=False,
    ):
    from interpretable.ml.io import read_models
    inputs,estimators,data=read_models(
        input_dir_path,
        keys=['inputs','estimators','data'],
        ).values()

    kws=dict(random_state=random_state)
    dn2df={}
    ## predictive_power
    if 'predictive power' in keys:
        dn2df['predictive power']=get_feature_predictive_power(
            inputs,
            data,
            plot=plot,
            **kws,
        )
    if 'feature importances' in keys:
        ## ensemble
        # d3={}
        # for scoring in ['roc_auc','average_precision']:
        # d3[scoring]=
        dn2df['feature importances']=get_feature_importances(
            estimators,
            X=data.loc[:,inputs['cols_x']],
            y=data.loc[:,inputs['coly']],
            # scoring=scoring,
            n_repeats=10,
            n_jobs=6,
            random_state=random_state,test=False,
            plot=plot,
        #   **kws,
            )
        # dn2df['feature importances']=pd.concat(d3,axis=0,names=['score type']).reset_index(0)
        
    if 'partial dependence' in keys:
        dn2df['partial dependence']=get_partial_dependence(
            estimators,
            X=data.loc[:,inputs['cols_x']],
            y=data.loc[:,inputs['coly']],
            # **kws,
       )
        
    if 'feature contributions' in keys:
        ## get SHAP
        predictions=data.copy()
        import shap
        d4={}
        for k in tqdm(estimators):
            explainer = shap.TreeExplainer(
                estimators[k].best_estimator_,
                feature_perturbation="tree_path_dependent",
        #       feature_names=inputs['cols_x'],
                )
            l1 = explainer.shap_values(predictions[inputs['cols_x']])
            if len(l1)==2:
                l2=l1[1]
            else:
                l2=l1
            if test: info(l2.shape)
            # print('Expected value:', explainer.expected_value[1])
            df3=pd.concat(
                [predictions.loc[:,inputs['colindex']],pd.DataFrame(l2, columns=inputs['cols_x'])],
                axis=1,
                )
            if test: info(df3.shape)
            df4=df3.melt(
                id_vars=inputs['colindex'],
                value_vars=inputs['cols_x'],
                var_name='feature',
                value_name='SHAP value',
                )
            d4[k]=df4
        df3=pd.concat(d4,axis=0,names=['estimator']).reset_index(0)

        from roux.stat.transform import rescale_divergent
        df4=pd.concat(
            {k:rescale_divergent(df,col='SHAP value') for k,df in df3.groupby(['estimator']+inputs['colindex'])},
            axis=0).reset_index(drop=True)
        dn2df['feature contributions']=df4.copy()

    for k in dn2df.keys():
        to_table(dn2df[k],f"{output_dir_path}/interpret/{k}.pqt")
    df1=pd.concat(
        {k:dn2df[k].melt(id_vars=['feature','estimator']) if k!='predictive power' else dn2df[k] for k in dn2df},
        axis=0,
        names=['interpretation']
    ).reset_index(0)
    df1.head(1)

    to_table(df1,f"{output_dir_path}/interpret/combined.tsv")      
    return dn2df

def agg_predictive_power(df):
    from roux.stat.transform import rescale
    return (df
        .groupby(['feature','variable'])['value']
            .agg([np.median,np.std]).unstack(1).swaplevel(axis=1).reset_index().rd.flatten_columns()
        .rd.drop_constants()
        .assign(
        **{
            'ROC AUC median rescaled':lambda df: rescale(df['ROC AUC median']),
            'ROC AUC median rank':lambda df: len(df)-df['ROC AUC median'].rank(),
            'average precision median rescaled':lambda df: rescale(df['average precision median']),
            'average precision median rank':lambda df: len(df)-df['average precision median'].rank(),
        }
        )
        )

def agg_feature_importances(
    df,
    ):
    from roux.stat.transform import rescale
    return (df
        .groupby(
            ['estimator','feature'],
            )
        .agg(**{
            'importance median':('importance',lambda x: np.median(x)),
            'importance std':('importance',lambda x: np.std(x)),
        })
        .reset_index()
        .assign(
        **{
            'importance rescaled':lambda df: rescale(df['importance median']),
            'importance rank':lambda df: len(df)-df['importance median'].rank(),
        }
        )
        .rd.drop_constants()
    )
def agg_feature_contributions(
    df4,
    ):
    df5=(df4
        .groupby(['estimator','feature'],as_index=False)
        .agg({'SHAP value': lambda x: np.median(abs(x))})
        )
    from roux.stat.transform import rescale_divergent
    return (
        pd.concat(
            {k:rescale_divergent(df,'SHAP value') for k,df in df5.groupby('estimator')},
            axis=0,
        )
        .reset_index(drop=True)
        .rd.renameby_replace(
            {'SHAP value':'median(|SHAP_value|)',
            'SHAP_value':'SHAP value'})
        .rd.drop_constants()
        )

def agg_feature_interpretations(
    interprets: dict,
    ):
    from roux.lib.dfs import merge_dfs
    return merge_dfs(
        [
            agg_predictive_power(interprets['predictive power']),
            agg_feature_importances(interprets['feature importances']),
            agg_feature_contributions(interprets['feature contributions']),
        ],
        how='inner',
        on='feature',
    )
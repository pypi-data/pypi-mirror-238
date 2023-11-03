"""For classification."""
## logging
import logging
from tqdm import tqdm
## data
import numpy as np
import pandas as pd
## viz
import matplotlib.pyplot as plt
import seaborn as sns

## internal
import roux.lib.dfs as rd
from roux.lib.df import groupby_sort_values
from roux.lib.io import (read_dict, to_dict, read_table, to_table)

# search estimator
def get_grid_search(modeln: str,
                    X: np.array,
                    y: np.array,
                    param_grid: dict={},
                    cv: int=5,
                    n_jobs: int=6,
                    random_state: int=None,
                    scoring: str='balanced_accuracy',
                    **kws,
                   ) -> object:
    """Grid search.

    Args:
        modeln (str): name of the model.
        X (np.array): X matrix.
        y (np.array): y vector.
        param_grid (dict, optional): parameter grid. Defaults to {}.
        cv (int, optional): cross-validations. Defaults to 5.
        n_jobs (int, optional): number of cores. Defaults to 6.
        random_state (int, optional): random state. Defaults to None.
        scoring (str, optional): scoring system. Defaults to 'balanced_accuracy'.

    Keyword arguments:
        kws: parameters provided to the `GridSearchCV` function.

    Returns:
        object: `grid_search`.

    References: 
        1. https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html
        2. https://scikit-learn.org/stable/modules/model_evaluation.html
    """
    if random_state is None: logging.warning(f"random_state is None")
    from sklearn.model_selection import GridSearchCV
    from sklearn import ensemble
    estimator = getattr(ensemble,modeln)(random_state=random_state)
    grid_search = GridSearchCV(estimator, 
                               param_grid,
                               cv=cv,
                               n_jobs=n_jobs,
                               scoring=scoring,
                               **kws)
    grid_search.fit(X, y)
    logging.info(modeln,grid_search.best_params_)
    logging.info(f"{modeln}.best_score_=a{grid_search.best_score_}")
    return grid_search

def get_estimatorn2grid_search(estimatorn2param_grid: dict,
                                X: pd.DataFrame,
                                y: pd.Series,
                                **kws
                                ) -> dict:
    """Estimator-wise grid search.

    Args:
        estimatorn2param_grid (dict): estimator name to the grid search map.
        X (pd.DataFrame): X matrix.
        y (pd.Series): y vector.

    Returns:
        dict: output.
    """
    estimatorn2grid_search={}
    for k in tqdm(estimatorn2param_grid.keys()):
        estimatorn2grid_search[k]=get_grid_search(modeln=k,
                        X=X,y=y,
                        param_grid=estimatorn2param_grid[k],
                        cv=5,
                        n_jobs=6,
                        **kws,
                       )
#     info({k:estimatorn2grid_search[k].best_params_ for k in estimatorn2grid_search})
    return estimatorn2grid_search

def get_test_scores(d1: dict) -> pd.DataFrame:
    """Test scores.

    Args:
        d1 (dict): dictionary with objects.

    Returns:
        pd.DataFrame: output.

    TODOs: 
        Get best param index.
    """
    from roux.lib.str import dict2str
    import re
    d2={}
    for k1 in d1:
#             info(k1,dict2str(d1[k1].best_params_))
        l1=list(d1[k1].cv_results_.keys())
        l1=[k2 for k2 in l1 if not re.match("^split[0-9]_test_.*",k2) is None]
        d2[k1+"\n("+dict2str(d1[k1].best_params_,sep='\n')+")"]={k2: d1[k1].cv_results_[k2] for k2 in l1}
    df1=pd.DataFrame(d2).applymap(lambda x: x[0] if (len(x)==1) else max(x)).reset_index()
    df1['variable']=df1['index'].str.split('_test_',expand=True)[1].str.replace('_',' ')
    df1['cv #']=df1['index'].str.split('_test_',expand=True)[0].str.replace('split','').apply(int)
    df1=df1.rd.clean()
    return df1.melt(id_vars=['variable','cv #'],
                   value_vars=d2.keys(),
                   var_name='model',
                   )

def run_grid_search(
    df,
    cols_x,
    coly,
    colindex,
    n_estimators: int=None,
    qcut: float=None,
    evaluations: list=[
        'prediction',
        'feature importances',
        'partial dependence',
    ],
    estimatorn2param_grid: dict=None,
    output_dir_path: str=None,
    test: bool=False,
    **kws, ## grid search
    ) -> dict:
    """Run grid search.

    Args:
        n_estimators (int): number of estimators.
        qcut (float, optional): quantile cut-off. Defaults to None.
        evaluations (list, optional): evaluations types. Defaults to ['prediction','feature importances', 'partial dependence', ].
        estimatorn2param_grid (dict, optional): estimator to the parameter grid map. Defaults to None.
        output_dir_path (str, optional): output_dir_pathut path. Defaults to None.
        test (bool, optional): test mode. Defaults to False.

    Keyword arguments:
        kws: parameters provided to `get_estimatorn2grid_search`.

    Returns:
        dict: estimator to grid search map.
    """
    assert('random_state' in kws)
    if kws['random_state'] is None: logging.warning(f"random_state is None")
    
    if estimatorn2param_grid is None: 
        from sklearn import ensemble
        estimatorn2param_grid={k:getattr(ensemble,k)().get_params() for k in estimatorn2param_grid}
        if test=='estimatorn2param_grid':
            return estimatorn2param_grid
    #     info(estimatorn2param_grid)
        for k in estimatorn2param_grid:
            if 'n_estimators' not in estimatorn2param_grid[k]:
                estimatorn2param_grid[k]['n_estimators']=[n_estimators]
        if test: logging.info(estimatorn2param_grid)
        d={}
        for k1 in estimatorn2param_grid:
            d[k1]={}
            for k2 in estimatorn2param_grid[k1]:
                if isinstance(estimatorn2param_grid[k1][k2],list):
                    d[k1][k2]=estimatorn2param_grid[k1][k2]
        estimatorn2param_grid=d
    if test: logging.info(estimatorn2param_grid)
    
    X,y=df.loc[:,cols_x].to_numpy(),df[coly].to_numpy()

    dn2df={}
    dn2df['input']=df.copy()
    estimatorn2grid_search=get_estimatorn2grid_search(
        estimatorn2param_grid,
        X=X,
        y=y,
        **kws)
#     to_dict({k:estimatorn2grid_search[k].cv_results_ for k in estimatorn2grid_search},
#            f'{output_dir_path}/estimatorn2grid_search_results.json')
    if not output_dir_path is None:
        to_dict(estimatorn2grid_search,f'{output_dir_path}/estimatorn2grid_search.pickle')
        to_dict(estimatorn2grid_search,f'{output_dir_path}/estimatorn2grid_search.joblib')
        d1=dict(
            cols_x=cols_x,
            coly=coly,
            colindex=colindex,
        ) # cols
        d1['estimatorns']=list(estimatorn2param_grid.keys())
        d1['evaluations']=evaluations
        to_table(dn2df['input'],f'{output_dir_path}/input.pqt')
        to_dict(d1,f'{output_dir_path}/input.json')
    return estimatorn2grid_search

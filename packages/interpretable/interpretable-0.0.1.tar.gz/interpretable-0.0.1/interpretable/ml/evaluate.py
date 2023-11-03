## logging
import logging
from tqdm import tqdm
## data
import pandas as pd
import numpy as np
## visualizations
import matplotlib.pyplot as plt
import seaborn as sns

def get_probability(
    estimatorn2grid_search: dict,
    X: np.array,
    y: np.array,
    colindex: str,
    coff: float=0.5,
    test: bool=False,
    ) -> pd.DataFrame:
    """Classification probability.

    Args:
        estimatorn2grid_search (dict): estimator to the grid search map.
        X (np.array): X matrix.
        y (np.array): y vector.
        colindex (str): index column. 
        coff (float, optional): cut-off. Defaults to 0.5.
        test (bool, optional): test mode. Defaults to False.

    Returns:
        pd.DataFrame: output.
    """
    assert(all(X.index==y.index))
    df0=y.to_frame('actual').reset_index()
    ## predictions
    df1=pd.DataFrame({k:estimatorn2grid_search[k].best_estimator_.predict(X) for k in estimatorn2grid_search})#.add_prefix('prediction ')
    df1.index=X.index
    df1=df1.melt(ignore_index=False,
            var_name='estimator',
            value_name='prediction').reset_index()
    ## prediction probabilities
    df2=pd.DataFrame({k:estimatorn2grid_search[k].best_estimator_.predict_proba(X)[:,1] for k in estimatorn2grid_search})#.add_prefix('prediction probability ')
    df2.index=X.index
    df2=df2.melt(ignore_index=False,
            var_name='estimator',
            value_name='prediction probability').reset_index()

    df3=df1.log.merge(right=df2,
                  on=['estimator',colindex],
                 how='inner',
                 validate="1:1")\
           .log.merge(right=df0,
                  on=[colindex],
                 how='inner',
    #              validate="1:1",
                )
    ## predicted correctly
    df3['TP']=df3.loc[:,['prediction','actual']].all(axis=1)
    if test:
        def plot_(df5):
            assert len(df5)==4, df5
            df6=df5.pivot(index='prediction',columns='actual',values='count').sort_index(axis=0,ascending=False).sort_index(axis=1,ascending=False)
            df6.columns=[str(c) for c in df6]
            df6.index  =[str(c) for c in df6.index]
            from roux.viz.heatmap import plot_crosstab
            ax=plot_crosstab(
                df6,
                order_x=['True','False'],
                order_y=['True','False'],
                # order_x=[True,False],
                # order_y=[True,False],
                show_pval=False,
                confusion=False,
            )
            df6.columns=[c=='True' for c in df6]
            df6.index  =[c=='True' for c in df6.index]
            from interpretable.viz.annot import annot_confusion_matrix
            annot_confusion_matrix(
                df6,
                ax=ax,
                off=0.5
                )
            ax.set_title(df5.name,loc='left')
        df4=df3.groupby('estimator').apply(lambda df: pd.crosstab(df['prediction'],df['actual']).melt(ignore_index=False,value_name='count')).reset_index()
        df4.groupby('estimator').apply(plot_)
    return df3

def get_auc_cv(
    estimator,
    X,
    y,
    cv=5,
    test=False,
    fitted=False,
    random_state=None,
    ):
    """
    TODO: just predict_probs as inputs
    TODO: resolve duplication of stat.binary.auc
    TODO: add more metrics in ds1 in addition to auc
    """
    def plot(df1,df2,ax=None):
        params={'label':'Mean ROC\n(AUC=%0.2f$\pm$%0.2f)' % (df1['AUC'].mean(), df1['AUC'].std()),}
        ax=plt.subplot() if ax is None else ax
        sns.lineplot(x="FPR", y="TPR", data=df2,
                     errorbar='sd',
                     label=params['label'],
                     ax=ax,
                    )
        ax.plot([0, 1], [0, 1], linestyle=':', lw=2, color='lightgray',)
        ax.set(xlim=[0, 1], ylim=[0, 1],)
        return ax
    from roux.stat.preprocess import get_cvsplits
    cv2Xy=get_cvsplits(
        X,
        y,
        cv=cv,
        random_state=random_state,
        )
    mean_fpr = np.linspace(0, 1, 100)
    from sklearn.metrics import roc_curve,auc
    dn2df={}
    d={}
    for i in tqdm(cv2Xy.keys()):
        if not fitted:
            estimator.fit(cv2Xy[i]['train']['X'], cv2Xy[i]['train']['y'])
        tpr,fpr,thresholds = roc_curve(cv2Xy[i]['test']['y'],
                                       estimator.predict_proba(cv2Xy[i]['test']['X'])[:,0],
                                      )
        interp_tpr = np.interp(mean_fpr, fpr, tpr)
        interp_tpr[0] = 0.0
        dn2df[i]=pd.DataFrame({'FPR':mean_fpr,
                               'TPR':interp_tpr,
                              })
        d[i]=auc(fpr,tpr)        
    ds1=pd.Series(d)
    ds1.name='AUC'
    df1=pd.DataFrame(ds1)
    df1.index.name='cv #'
    df2=pd.concat(dn2df,axis=0,names=['cv #']).reset_index().rd.clean()
    if test:
        plt.figure(figsize=[3,3])
        plot(df1,df2,ax=None)
    return df1,df2

def get_roc_auc(
    true,
    test,
    outmore=False,
    ):
    from sklearn.metrics import roc_curve, auc
    fpr, tpr, thresholds = roc_curve(true,test)
    a=auc(fpr, tpr)
    if not outmore:
        return a
    else:
        return fpr, tpr, thresholds,a
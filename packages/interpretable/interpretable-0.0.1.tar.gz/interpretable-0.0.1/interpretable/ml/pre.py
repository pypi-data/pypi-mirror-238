import pandas as pd

def get_Xy(
    df01,
    columns,
    y_kind,
    ):
    """
    Get the columns for a kind of model
    """
    from roux.lib.set import flatten,list2str
    return dict(
        cols_x=flatten(list(columns['cols_x'].values())),
        coly=list2str(columns['cols_y'][y_kind]),
        colindex=columns['cols_index'],
    )

def get_Xy_for_classification(
    df1: pd.DataFrame,
    coly: str,
    qcut: float=None,
    # low_complexity filters
    drop_xs_low_complexity: bool=False,
    min_nunique: int=5,
    max_inflation: float=0.5,
    **kws,
    ) -> dict:
    """Get X matrix and y vector. 
    
    Args:
        df1 (pd.DataFrame): input data, should be indexed.
        coly (str): column with y values, bool if qcut is None else float/int
        qcut (float, optional): quantile cut-off. Defaults to None.
        drop_xs_low_complexity (bool, optional): to drop columns with <5 unique values. Defaults to False.
        min_nunique (int, optional): minimum unique values in the column. Defaults to 5.
        max_inflation (float, optional): maximum inflation. Defaults to 0.5.

    Keyword arguments:
        kws: parameters provided to `drop_low_complexity`.

    Returns:
        dict: output.
    """
    df1=df1.rd.clean(drop_constants=True)
    cols_X=[c for c in df1 if c!=coly]
    if not qcut is None:
        if qcut>0.5:
            logging.error('qcut should be <=0.5')
            return 
        lims=[df1[coly].quantile(1-qcut),df1[coly].quantile(qcut)]
        df1[coly]=df1.apply(lambda x: True if x[coly]>=lims[0] else False if x[coly]<lims[1] else np.nan,axis=1)
        df1=df1.log.dropna()
    df1[coly]=df1[coly].apply(bool)
    logging.info(df1[coly].value_counts())
    y=df1[coly]
    X=df1.loc[:,cols_X]
    # remove low complexity features
    X=X.rd.clean(drop_constants=True)
    from roux.stat.preprocess import drop_low_complexity
    X=drop_low_complexity(
        X,
        cols=None,
        min_nunique=min_nunique,
        max_inflation=max_inflation,
        test=False if drop_xs_low_complexity else True,
        **kws,
        )
    return {'X':X,'y':y}

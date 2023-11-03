import pandas as pd
## visualizations
import matplotlib.pyplot as plt

def annot_confusion_matrix(
    df_: pd.DataFrame,
    ax: plt.Axes=None,
    off: float=0.5
    ) -> plt.Axes:
    """Annotate a confusion matrix.

    Args:
        df_ (pd.DataFrame): input data.
        ax (plt.Axes, optional): `plt.Axes` object. Defaults to None.
        off (float, optional): offset. Defaults to 0.5.

    Returns:
        plt.Axes: `plt.Axes` object.
    """
    from roux.stat.binary import get_stats_confusion_matrix
    df1=get_stats_confusion_matrix(df_)
    df2=pd.DataFrame({
                    'TP': [0,0],
                    'TN': [1,1],
                    'FP': [0,1],
                    'FN': [1,0],
                    'TPR':[0,2],
                    'TNR': [1,2],
                    'PPV': [2,0],
                    'NPV': [2,1],
                    'FPR': [1,3],
                    'FNR': [0,3],
                    'FDR': [3,0],
                    'ACC': [2,2],
                    },
                     index=['x','y']).T
    df2.index.name='variable'
    df2=df2.reset_index()
    df3=df1.merge(df2,
              on='variable',
              how='inner',
              validate="1:1")
    
    _=df3.loc[(df3['variable'].isin(['TP','TN','FP','FN'])),:].apply(lambda x: ax.text(x['x']+off,
                                                                                       x['y']+(off*2),
    #                               f"{x['variable']}\n{x['value']:.0f}",
                                  x['variable'],
    #                               f"({x['T|F']+x['P|N']})",
                                ha='center',va='bottom',
                               ),axis=1)
    _=df3.loc[~(df3['variable'].isin(['TP','TN','FP','FN'])),:].apply(lambda x: ax.text(x['x']+off,
                                                                                        x['y']+(off*2),
                                  f"{x['variable']}\n{x['value']:.2f}",
    #                               f"({x['T|F']+x['P|N']})",
                                ha='center',va='bottom',
                               ),axis=1)
    return ax

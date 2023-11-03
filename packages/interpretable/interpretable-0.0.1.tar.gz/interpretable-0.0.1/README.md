<!-- PROJECT SHIELDS -->
<div align="center">
  
<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url] -->
<a href="">[![PyPI](https://img.shields.io/pypi/v/interpretable?style=for-the-badge)![Python](https://img.shields.io/pypi/pyversions/interpretable?style=for-the-badge)](https://pypi.org/project/interpretable)</a>
<a href="">[![build](https://img.shields.io/github/actions/workflow/status/rraadd88/interpretable/build.yml?style=for-the-badge)](https://github.com/rraadd88/interpretable/actions/workflows/build.yml)</a>
<a href="">[![Issues](https://img.shields.io/github/issues/rraadd88/interpretable.svg?style=for-the-badge)](https://github.com/rraadd88/interpretable/issues)</a>
<br />
<a href="">[![Downloads](https://img.shields.io/pypi/dm/interpretable?style=for-the-badge)](https://pepy.tech/project/interpretable)</a>
<a href="">[![GNU License](https://img.shields.io/github/license/rraadd88/interpretable.svg?style=for-the-badge)](https://github.com/rraadd88/interpretable/blob/master/LICENSE)</a>
</div>
  
<!-- PROJECT LOGO -->
<div align="center">
  <img src="https://github.com/rraadd88/rraadd88/assets/9945034/e29db6d6-9a2e-4459-9c7b-dae2da416bf3" alt="logo" />
  <h1 align="center">interpretable</h1>
  <p align="center">
    Interpretable machine learning toolbox.
    <br />
    <a href="https://github.com/rraadd88/interpretable#examples">Examples</a>
    ·
    <a href="https://github.com/rraadd88/interpretable#api">Explore the API</a>
  </p>
</div> 
  
# Examples
[🕸️ Graph Neural Network based auto-encoder](https://github.com/rraadd88/interpretable/blob/master/examples/dev_graph_autoencoder_train_node_predict_edge.ipynb)  
[🛠️ Preprocessing.](https://github.com/rraadd88/interpretable/blob/master/examples/interpretable_01_preprocess.ipynb)  
[📦 Learning.](https://github.com/rraadd88/interpretable/blob/master/examples/interpretable_02_learn.ipynb)  
[🧪 Evaluation.](https://github.com/rraadd88/interpretable/blob/master/examples/interpretable_03_evaluate.ipynb)  
[🔢 Interpretation.](https://github.com/rraadd88/interpretable/blob/master/examples/interpretable_04_interpret.ipynb)  
  
![image](https://github.com/rraadd88/rraadd88/assets/9945034/bdef5971-f776-41ae-876e-3afac8626d3b)  
# Installation
    
```
pip install interpretable              # with basic dependencies  
```
With additional dependencies as required:
```
pip install interpretable[ml]          # for machine learning applications using scikit-learn
pip install interpretable[dl]          # for deep learning based applications using pytorch 
pip install interpretable[gnn]         # for graph neural network based applications using pytorch geometric 
pip install interpretable[dev]         # for local testing
```
# How to cite?
Please cite it using the metadata given in [this file](https://github.com/rraadd88/interpretable/blob/main/CITATION.cff). 
For more information about citation, please see 'Cite this repository' section on the github page of the repository.  
# Future directions, for which contributions are welcome:  
- [ ] Support for classification models other than RFC and GBC.
- [ ] Support for regression models.
- [ ] More examples of GNNs.
# Similar projects:
- https://github.com/EpistasisLab/tpot
- https://github.com/oegedijk/explainerdashboard
# API
<!-- markdownlint-disable -->

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/gnn.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>module</kbd> `interpretable.gnn.layers`





---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/gnn/layers.py#L3"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_channels`

```python
get_channels(start, end, scale, kind)
```






---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/gnn/layers.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_layers`

```python
get_layers(
    model_name,
    num_node_features,
    hidden_channels,
    kind,
    scale,
    **kws_model
)
```

Get the layers for encoding or decoding. 


---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/gnn/layers.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_coder`

```python
get_coder(
    model_name,
    num_node_features,
    hidden_channels,
    kind,
    scale,
    **kws_model
)
```

Get a stack of layers for encoding or decoding  


<!-- markdownlint-disable -->

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/gnn"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>module</kbd> `interpretable.gnn`






<!-- markdownlint-disable -->

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>module</kbd> `interpretable.ml.classify`
For classification. 


---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/classify.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_grid_search`

```python
get_grid_search(
    modeln: str,
    X: <built-in function array>,
    y: <built-in function array>,
    param_grid: dict = {},
    cv: int = 5,
    n_jobs: int = 6,
    random_state: int = None,
    scoring: str = 'balanced_accuracy',
    **kws
) → object
```

Grid search. 



**Args:**
 
 - <b>`modeln`</b> (str):  name of the model. 
 - <b>`X`</b> (np.array):  X matrix. 
 - <b>`y`</b> (np.array):  y vector. 
 - <b>`param_grid`</b> (dict, optional):  parameter grid. Defaults to {}. 
 - <b>`cv`</b> (int, optional):  cross-validations. Defaults to 5. 
 - <b>`n_jobs`</b> (int, optional):  number of cores. Defaults to 6. 
 - <b>`random_state`</b> (int, optional):  random state. Defaults to None. 
 - <b>`scoring`</b> (str, optional):  scoring system. Defaults to 'balanced_accuracy'. 

Keyword arguments: 
 - <b>`kws`</b>:  parameters provided to the `GridSearchCV` function. 



**Returns:**
 
 - <b>`object`</b>:  `grid_search`. 

References:  
 - <b>`1. https`</b>: //scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html 
 - <b>`2. https`</b>: //scikit-learn.org/stable/modules/model_evaluation.html 


---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/classify.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_estimatorn2grid_search`

```python
get_estimatorn2grid_search(
    estimatorn2param_grid: dict,
    X: DataFrame,
    y: Series,
    **kws
) → dict
```

Estimator-wise grid search. 



**Args:**
 
 - <b>`estimatorn2param_grid`</b> (dict):  estimator name to the grid search map. 
 - <b>`X`</b> (pd.DataFrame):  X matrix. 
 - <b>`y`</b> (pd.Series):  y vector. 



**Returns:**
 
 - <b>`dict`</b>:  output. 


---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/classify.py#L92"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_test_scores`

```python
get_test_scores(d1: dict) → DataFrame
```

Test scores. 



**Args:**
 
 - <b>`d1`</b> (dict):  dictionary with objects. 



**Returns:**
 
 - <b>`pd.DataFrame`</b>:  output. 

TODOs:  Get best param index. 


---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/classify.py#L121"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `run_grid_search`

```python
run_grid_search(
    df,
    cols_x,
    coly,
    colindex,
    n_estimators: int = None,
    qcut: float = None,
    evaluations: list = ['prediction', 'feature importances', 'partial dependence'],
    estimatorn2param_grid: dict = None,
    output_dir_path: str = None,
    test: bool = False,
    **kws
) → dict
```

Run grid search. 



**Args:**
 
 - <b>`n_estimators`</b> (int):  number of estimators. 
 - <b>`qcut`</b> (float, optional):  quantile cut-off. Defaults to None. 
 - <b>`evaluations`</b> (list, optional):  evaluations types. Defaults to ['prediction','feature importances', 'partial dependence', ]. 
 - <b>`estimatorn2param_grid`</b> (dict, optional):  estimator to the parameter grid map. Defaults to None. 
 - <b>`output_dir_path`</b> (str, optional):  output_dir_pathut path. Defaults to None. 
 - <b>`test`</b> (bool, optional):  test mode. Defaults to False. 

Keyword arguments: 
 - <b>`kws`</b>:  parameters provided to `get_estimatorn2grid_search`. 



**Returns:**
 
 - <b>`dict`</b>:  estimator to grid search map. 


<!-- markdownlint-disable -->

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>module</kbd> `interpretable.ml.evaluate`





---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/evaluate.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_probability`

```python
get_probability(
    estimatorn2grid_search: dict,
    X: <built-in function array>,
    y: <built-in function array>,
    colindex: str,
    coff: float = 0.5,
    test: bool = False
) → DataFrame
```

Classification probability. 



**Args:**
 
 - <b>`estimatorn2grid_search`</b> (dict):  estimator to the grid search map. 
 - <b>`X`</b> (np.array):  X matrix. 
 - <b>`y`</b> (np.array):  y vector. 
 - <b>`colindex`</b> (str):  index column.  
 - <b>`coff`</b> (float, optional):  cut-off. Defaults to 0.5. 
 - <b>`test`</b> (bool, optional):  test mode. Defaults to False. 



**Returns:**
 
 - <b>`pd.DataFrame`</b>:  output. 


---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/evaluate.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_auc_cv`

```python
get_auc_cv(estimator, X, y, cv=5, test=False, fitted=False, random_state=None)
```

TODO: just predict_probs as inputs TODO: resolve duplication of stat.binary.auc TODO: add more metrics in ds1 in addition to auc 


---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/evaluate.py#L145"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_roc_auc`

```python
get_roc_auc(true, test, outmore=False)
```






<!-- markdownlint-disable -->

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>module</kbd> `interpretable.ml.interpret`





---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/interpret.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_feature_predictive_power`

```python
get_feature_predictive_power(
    d0: dict,
    df01: DataFrame,
    n_splits: int = 5,
    n_repeats: int = 10,
    random_state: int = None,
    plot: bool = False,
    drop_na: bool = False,
    **kws
) → DataFrame
```

get_feature_predictive_power _summary_ 



**Notes:**

> x-values should be scale and sign agnostic. 
>

**Args:**
 
 - <b>`d0`</b> (dict):  input dictionary. 
 - <b>`df01`</b> (pd.DataFrame):  input data,  
 - <b>`n_splits`</b> (int, optional):  number of splits. Defaults to 5. 
 - <b>`n_repeats`</b> (int, optional):  number of repeats. Defaults to 10. 
 - <b>`random_state`</b> (int, optional):  random state. Defaults to None. 
 - <b>`plot`</b> (bool, optional):  plot. Defaults to False. 
 - <b>`drop_na`</b> (bool, optional):  drop missing values. Defaults to False. 



**Returns:**
 
 - <b>`pd.DataFrame`</b>:  output data. 


---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/interpret.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_feature_importances`

```python
get_feature_importances(
    estimatorn2grid_search: dict,
    X: DataFrame,
    y: Series,
    scoring: str = 'roc_auc',
    n_repeats: int = 20,
    n_jobs: int = 6,
    random_state: int = None,
    plot: bool = False,
    test: bool = False,
    **kws
) → DataFrame
```

Feature importances. 



**Args:**
 
 - <b>`estimatorn2grid_search`</b> (dict):  map between estimator name and grid search object.  
 - <b>`X`</b> (pd.DataFrame):  X matrix. 
 - <b>`y`</b> (pd.Series):  y vector. 
 - <b>`scoring`</b> (str, optional):  scoring type. Defaults to 'roc_auc'. 
 - <b>`n_repeats`</b> (int, optional):  number of repeats. Defaults to 20. 
 - <b>`n_jobs`</b> (int, optional):  number of cores. Defaults to 6. 
 - <b>`random_state`</b> (int, optional):  random state. Defaults to None. 
 - <b>`plot`</b> (bool, optional):  plot. Defaults to False. 
 - <b>`test`</b> (bool, optional):  test mode. Defaults to False. 



**Returns:**
 
 - <b>`pd.DataFrame`</b>:  output data. 


---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/interpret.py#L149"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_partial_dependence`

```python
get_partial_dependence(
    estimatorn2grid_search: dict,
    X: DataFrame,
    y: Series,
    test: bool = False
) → DataFrame
```

Partial dependence. 



**Args:**
 
 - <b>`estimatorn2grid_search`</b> (dict):  map between estimator name and grid search object. 
 - <b>`X`</b> (pd.DataFrame):  X matrix. 
 - <b>`y`</b> (pd.Series):  y vector. 



**Returns:**
 
 - <b>`pd.DataFrame`</b>:  output data. 


---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/interpret.py#L192"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `interpret`

```python
interpret(
    input_dir_path,
    output_dir_path,
    keys=['predictive power', 'feature importances', 'partial dependence', 'feature contributions'],
    random_state=None,
    plot=False,
    test=False
)
```






---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/interpret.py#L292"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `agg_predictive_power`

```python
agg_predictive_power(df)
```






---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/interpret.py#L308"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `agg_feature_importances`

```python
agg_feature_importances(df)
```






---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/interpret.py#L329"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `agg_feature_contributions`

```python
agg_feature_contributions(df4)
```






---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/interpret.py#L349"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `agg_feature_interpretations`

```python
agg_feature_interpretations(interprets: dict)
```






<!-- markdownlint-disable -->

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>module</kbd> `interpretable.ml.io`





---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/io.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `read_models`

```python
read_models(
    output_dir_path,
    keys=None,
    filenames={'inputs': 'input.json', 'data': 'input.pqt', 'estimators': 'estimatorn2grid_search.pickle', 'predictions': 'prediction.pqt'}
)
```






<!-- markdownlint-disable -->

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>module</kbd> `interpretable.ml`






<!-- markdownlint-disable -->

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>module</kbd> `interpretable.ml.pre`





---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/pre.py#L3"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_Xy`

```python
get_Xy(df01, columns, y_kind)
```

Get the columns for a kind of model 


---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/ml/pre.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_Xy_for_classification`

```python
get_Xy_for_classification(
    df1: DataFrame,
    coly: str,
    qcut: float = None,
    drop_xs_low_complexity: bool = False,
    min_nunique: int = 5,
    max_inflation: float = 0.5,
    **kws
) → dict
```

Get X matrix and y vector.  



**Args:**
 
 - <b>`df1`</b> (pd.DataFrame):  input data, should be indexed. 
 - <b>`coly`</b> (str):  column with y values, bool if qcut is None else float/int 
 - <b>`qcut`</b> (float, optional):  quantile cut-off. Defaults to None. 
 - <b>`drop_xs_low_complexity`</b> (bool, optional):  to drop columns with <5 unique values. Defaults to False. 
 - <b>`min_nunique`</b> (int, optional):  minimum unique values in the column. Defaults to 5. 
 - <b>`max_inflation`</b> (float, optional):  maximum inflation. Defaults to 0.5. 

Keyword arguments: 
 - <b>`kws`</b>:  parameters provided to `drop_low_complexity`. 



**Returns:**
 
 - <b>`dict`</b>:  output. 


<!-- markdownlint-disable -->

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/viz.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>module</kbd> `interpretable.viz.annot`





---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/viz/annot.py#L5"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `annot_confusion_matrix`

```python
annot_confusion_matrix(df_: DataFrame, ax: Axes = None, off: float = 0.5) → Axes
```

Annotate a confusion matrix. 



**Args:**
 
 - <b>`df_`</b> (pd.DataFrame):  input data. 
 - <b>`ax`</b> (plt.Axes, optional):  `plt.Axes` object. Defaults to None. 
 - <b>`off`</b> (float, optional):  offset. Defaults to 0.5. 



**Returns:**
 
 - <b>`plt.Axes`</b>:  `plt.Axes` object. 


<!-- markdownlint-disable -->

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/viz.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>module</kbd> `interpretable.viz.gnn`





---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/viz/gnn.py#L3"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `lines_metricsby_epochs`

```python
lines_metricsby_epochs(data, figsize=[3, 3])
```



**Args:**
 
 - <b>`data`</b>:  table containing the epoch and other metrics. 


<!-- markdownlint-disable -->

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/viz"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>module</kbd> `interpretable.viz`






<!-- markdownlint-disable -->

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/viz.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>module</kbd> `interpretable.viz.ml`





---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/viz/ml.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `plot_metrics`

```python
plot_metrics(data, inputs, estimators, plot: bool = False) → DataFrame
```

Plot performance metrics. 



**Args:**
 
 - <b>`plot`</b> (bool, optional):  make plots. Defaults to False. 



**Returns:**
 
 - <b>`pd.DataFrame`</b>:  output data. 


---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/viz/ml.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `plot_feature_predictive_power`

```python
plot_feature_predictive_power(
    df3: DataFrame,
    ax: Axes = None,
    figsize: list = [3, 3],
    **kws
) → Axes
```

Plot feature-wise predictive power. 



**Args:**
 
 - <b>`df3`</b> (pd.DataFrame):  input data. 
 - <b>`ax`</b> (plt.Axes, optional):  axes object. Defaults to None. 
 - <b>`figsize`</b> (list, optional):  figure size. Defaults to [3,3]. 



**Returns:**
 
 - <b>`plt.Axes`</b>:  output. 


---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/viz/ml.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `plot_feature_ranks`

```python
plot_feature_ranks(df2: DataFrame)
```






---

<a href="https://github.com/rraadd88/interpretable/blob/master/interpretable/viz/ml.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `plot_feature_contributions`

```python
plot_feature_contributions(data, kws_plot, vmax=0.2, vmin=-0.2, figsize=[4, 4])
```







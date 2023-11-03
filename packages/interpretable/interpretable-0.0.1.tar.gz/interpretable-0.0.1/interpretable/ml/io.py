from os.path import exists
from roux.lib.io import is_dict

def read_models(
    output_dir_path,
    keys=None,
    filenames=dict(
        inputs='input.json',
        data='input.pqt',
        estimators='estimatorn2grid_search.pickle',
        predictions='prediction.pqt',
        ),
    ):
    from roux.lib.io import read_dict,read_table
    if not keys is None:
        ## filter files
        filenames={k:filenames[k] for k in keys}
    
    d0={}
    for k,v in filenames.items():
        path=f'{output_dir_path}/{v}'
        if exists(path):
            if is_dict(path):
                d0[k]=read_dict(path) 
            else:
                d0[k]=read_table(path) 
    return d0
import pandas as pd
import numpy as np
import logging

def get_overlap(
    genes_set,
    genes_test,
    output_format='list',
    ):
    """
    Get overlapping genes as a string.
    """
    overlap=sorted(list(set(genes_set) & set(genes_test)))
    if output_format == 'list':
        return overlap
    elif output_format == 'str':
        return ';'.join(overlap)
    else:
        raise ValueError(output_format)

def get_overlap_size(
    **kws,
    ):
    kws['output_format']='list'
    return len(get_overlap(**kws))

def get_perc_overlap(
    genes_set,
    genes_test,
    ):
    """
    """
    overlap_size=get_overlap_size(genes_set=genes_set,
                    genes_test=genes_test,
                    output_format='list',
                    )
    return 100*(overlap_size/len(set(genes_set) | set(genes_test)))

def get_overlap_size_by_gene_test(
    genes_set,
    genes_test,
    ):
    """
    numerator of the fold change.
    """
    overlap_size=get_overlap_size(genes_set=genes_set,
                    genes_test=genes_test,
                    output_format='list',
                    )
    return overlap_size/len(set(genes_test))

def get_gene_set_size_by_background(
    genes_set,
    background,
    ):
    """
    denominator of the fold change.
    """
    return (len(set(genes_set))/background)

def get_fold_change(
    genes_set,
    genes_test,
    background,
    ):
    """
    Get fold change.

        fc = (intersection/(test genes))/((genes in the gene set)/background)

    Notes:
        Added by RD on 20220611
    """
    return get_overlap_size_by_gene_test(genes_set,genes_test)/get_gene_set_size_by_background(genes_set,background)

def get_hypergeom_pval(
    genes_set,
    genes_test,
    background,
    ):
    """
    Calculate hypergeometric P-values.
    """ 
    from scipy.stats import hypergeom
    return hypergeom.sf(
        k=get_overlap_size(genes_test=genes_test,genes_set=genes_set)-1,
        # len(set(genes_test) & set(genes_set))-1, # size of the intersection
        M=background, # background
        n=len(set(genes_test)), # size of set1
        N=len(set(genes_set)), # size of set2
        )
def get_contigency_table(
    genes_set,
    genes_test,
    background,
    ):
    """
    Generate a contingency table required for the Fisher's test.

    Notes:

                                    within gene (/referenece) set:
                                    True            False
            within test gene: True  intersection    True False
                            False   False False     total-size of union           
    """
    genes_set,genes_test=set(genes_set),set(genes_test)
    table=[[
             len((genes_set) & (genes_test)), # intersection size
             len((genes_test) - (genes_set))],# in one set not the other (genes in test but not set )
             [len((genes_set) - (genes_test)),# in one set not the other (genes in set and not test)
             background-len((genes_set) | (genes_test))] # genes that are not in my background or the test or set                               
             # not in either set
             ]
    assert sum(table[0])+sum(table[1]) == background
    return table

def get_odds_ratio(
    genes_set,
    genes_test,
    background,
    ):
    """
    Calculate Odds ratio and P-values using Fisher's exact test.
    """
    from scipy.stats import fisher_exact
    return fisher_exact(get_contigency_table(genes_set,genes_test, background),
                              alternative='two-sided'
                              )

from roux.

def get_enrichment(
    df1: pd.DataFrame, # containing genes to test
    df2: pd.DataFrame, # containing gene set
    background: int,
    colid: str, ## gene id
    colref: str, ## 
    coltest: str, ## 
    # colrefname: str='gene set name',
    # colreftype: str='gene set type',
    ):
    """
    Calculate the enrichments.
    """
    ## calculate the background for the Fisher's test that is compatible with the contigency tables
    background_fisher_test = len(set(df1[colid].tolist()+df2[colid].tolist()))
    df3=(df1
        .groupby(coltest) # iterate over the groups of genes to test
        .apply(lambda df1_: (df2.groupby(colref) # iterate over the groups of gene sets
                            .apply(lambda df2_: pd.Series(
                            {
        '% overlap':get_perc_overlap(
            genes_test=df1_[colid].tolist(),
            genes_set =df2_[colid].tolist(),
                            ),
        'P (hypergeom. test)':get_hypergeom_pval(
            genes_test=df1_[colid].tolist(),
            genes_set= df2_[colid].tolist(),
            background=background),
        'contingency table':get_contigency_table(
            genes_test=df1_[colid].tolist(),
            genes_set= df2_[colid].tolist(), 
            background=background_fisher_test,
            ),
        'Odds ratio':get_odds_ratio(
            genes_test=df1_[colid].tolist(),
            genes_set= df2_[colid].tolist(), 
            background=background_fisher_test,
            )[0], #commented out before
        "P (Fisher's exact)":get_odds_ratio(
            genes_test=df1_[colid].tolist(),
            genes_set= df2_[colid].tolist(), 
            background=background_fisher_test,
            )[1], #commented out before
        "overlapping genes":get_overlap_size(
            genes_test=df1_[colid].tolist(),
            genes_set= df2_[colid].tolist(),
            ),
        #'fold change ([0,1])':get_fold_change_no_background(df1_[colid].tolist(),df2_[colid].tolist()), # VP added this 20220603, RD changed the column name to 'fold change ([0,1])' because these fold-change values scale between 0 and 1. 
        'fold change':get_fold_change(
            genes_test=df1_[colid].tolist(),
            genes_set=df2_[colid].tolist(),
            background=background,
            ), # RD added this 20220611
        'overlap/gene test':get_overlap_size_by_gene_test(
            genes_test=df1_[colid].tolist(),
            genes_set=df2_[colid].tolist(),
            ),
        'gene set/background':get_gene_set_size_by_background(
            genes_set=df2_[colid].tolist(),
            background=background,
            ),
        },
        ))))
         
        
    ).reset_index()
    def get_q(df):
        ## Multiple test correction. Calculate adjusted P values i.e. Q values
        from statsmodels.stats.multitest import fdrcorrection
        for col in df.filter(regex='^P.*'):
            df[col.replace('P','Q')]=fdrcorrection(pvals=df[col], alpha=0.05, method='indep', is_sorted=False)[1]
        return df
    df4=(df3
        .groupby(coltest) # iterate over the groups of genes to test
        .apply(get_q)
        )
    return df4
    
import matplotlib.pyplot as plt

def lines_metricsby_epochs(
    data,
    figsize=[3,3],
    ):
    """
    
    Args:
        data: table containing the epoch and other metrics.
    
    """
    fig, ax = plt.subplots(figsize=figsize)

    for y in data.filter(regex="^((?!(loss|epoch)).)*$"):
        data.plot(x='epoch',y=y,ax=ax)
    ax.set_ylabel("Performance Metric")

    plt.legend(
        # handles=[p2, p3],
         bbox_to_anchor=[1,1], title='Performance Metric',
    )

    ax2 = ax.twinx()
    ax2.spines["left"].set_position(("axes", -0.3))
    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)
    make_patch_spines_invisible(ax2)
    ax2.spines["left"].set_visible(True)
    ax2.yaxis.set_label_position('left')
    ax2.yaxis.set_ticks_position('left')
    # Second, show the right spine.
    ax2.spines["left"].set_visible(True)

    # p1, = ax2.plot(losses, "b-", label="training loss")
    for y in data.filter(like='loss'):
        color_loss='gray'
        data.plot(x='epoch',y=y,color=color_loss,ax=ax2, legend=False,alpha=0.5)
        ax2.yaxis.label.set_color(color_loss)
        ax2.tick_params(axis='y', colors=color_loss)
        ax2.set_ylabel("Loss")
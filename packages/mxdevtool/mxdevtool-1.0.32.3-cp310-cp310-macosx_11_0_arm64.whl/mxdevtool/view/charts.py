import mxdevtool as mx

def graph(name, xdata, ydata_d, **kwargs):

    try:
        import matplotlib.pyplot as plt
    except:
        raise Exception('matplotlib is required')

    # plot the data
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for k, y in ydata_d.items():
        ax.plot(xdata, y, 'o-', color='tab:blue')

    ax.set_title(name)
    if kwargs.get('show') is True:
        plt.show()

    return ax
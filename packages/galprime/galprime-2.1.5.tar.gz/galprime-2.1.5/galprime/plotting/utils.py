import matplotlib as mpl

def load_pyplot_style(xtick_major=6, xtick_minor=2, ytick_major=6, ytick_minor=4, 
fontsize=20, tickfontsize=18):
    """ Load the style used for galprime plotting 
    Notably has a thicker border and tick marks 
    """
    mpl.rc('text', usetex=True)

    mpl.rcParams['xtick.major.size'] = xtick_major
    mpl.rcParams['xtick.major.width'] = xtick_major / 3
    mpl.rcParams['xtick.minor.size'] = xtick_minor
    mpl.rcParams['xtick.minor.width'] = xtick_minor / 4
    mpl.rcParams['ytick.major.size'] = ytick_major
    mpl.rcParams['ytick.major.width'] = ytick_major / 3
    mpl.rcParams['ytick.minor.size'] = ytick_minor
    mpl.rcParams['ytick.minor.width'] = ytick_minor / 4
    mpl.rcParams['axes.linewidth'] = 1.5

    mpl.rc('xtick', labelsize=fontsize)
    mpl.rc('ytick', labelsize=fontsize)

    mpl.rcParams['text.latex.preamble'] = [r'\boldmath']

    font = {'family' : 'serif',
        'weight': 'bold',
        'size': fontsize}

    mpl.rc('font', **font)




import seaborn as sns
import matplotlib.pyplot as plt


def visualisation(df, x_axis='tfactor', y_axis='value', track='channel'):
    """
        Track visualisation
       :param df: Pandas Dataframe
       :param x_axis: str,
            column to plot on x-axis
       :param y_axis: str,
            column to plot on y-axis
       :param track: str,
            column name containing the different channel,
                default 'channel'
       :return: matplotlib object
       """
    sns.set_theme(style="ticks")

    # Initialize the figure with a logarithmic x-axis
    ax = plt.figure(figsize=(10, 6))

    # Assuming df has a column 'track' -> 1 color to each track cat
    sns.scatterplot(data=df,
                    x=x_axis,
                    y=y_axis,
                    hue=track,
                    # marker='o',
                    size='duration'
                    )
    # add the arg

    # Put the legend out of the figure
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)

    # Tweak the visual presentation
    #plt.ylabel('Frequency [Hz]')
    #plt.xlabel('Time [sec]')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title("Visualisation")
    plt.tight_layout()

    #plt.savefig("SodaMidi.png", format='png', dpi=150)
    plt.show()
    return ax
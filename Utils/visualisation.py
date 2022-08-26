import seaborn as sns
import matplotlib.pyplot as plt


def visualisation(df, x_axis, y_axis):
    """
    Track visualisation
    :param df:
    :param x_axis:
    :param y_axis:
    :return:
    """
    sns.set_theme(style="ticks")

    # Initialize the figure with a logarithmic x-axis
    plt.figure(figsize=(10, 6))

    # Assuming df has a column 'track' -> 1 color to each track cat
    sns.scatterplot(data=df,
                    x=x_axis,
                    y=y_axis,
                    hue='track',
                    markers='-'
                    )
    # Put the legend out of the figure
    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)

    # Tweak the visual presentation
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    # plt.xlabel(x_axis)
    # plt.ylabel(y_axis)
    plt.title("Visualisation")
    plt.tight_layout()

    plt.savefig("SodaMidi.png",
                format='png',
                dpi=150)
    plt.show()
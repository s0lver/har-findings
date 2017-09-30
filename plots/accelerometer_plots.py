from typing import List, Dict
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from entities.AccelerometerSample import AccelerometerSample
from preprocessing.tools import calculate_magnitude_vector


def plot_activity_data(samples: List[AccelerometerSample], label, path_to_save=None):
    plt.style.use('bmh')

    plt.rcParams['font.family'] = 'Gotham XNarrow'
    plt.rcParams['font.serif'] = 'Gotham XNarrow'
    plt.rcParams['font.monospace'] = 'Monaco'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'normal'
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    # plt.rcParams['legend.fontsize'] = 11
    plt.rcParams['legend.fontsize'] = 7
    plt.rcParams['figure.titlesize'] = 13
    plt.rcParams['legend.fontsize'] = 9

    fig, axes = plt.subplots(4, sharex=True)
    fig.suptitle(label)

    xs = list(map(lambda x: x.timestamp, samples))
    ys = list(map(lambda x: x.x, samples))
    axes[0].plot(ys, label='X axis', linewidth='1')
    axes[0].set_ylabel('Acc (Earth G off)')
    axes[0].legend()

    ys = list(map(lambda x: x.y, samples))
    axes[1].plot(ys, label='Y axis', linewidth='1')
    axes[1].set_ylabel('Acc (Earth G off)')
    axes[1].legend()

    ys = list(map(lambda x: x.z, samples))
    axes[2].plot(ys, label='Z axis', linewidth='1')
    axes[2].set_ylabel('Acc (Earth G off)')
    axes[2].legend()

    ys = calculate_magnitude_vector(samples)
    axes[3].plot(ys, label='Magnitude vector', linewidth='1')
    axes[3].set_ylabel('Magnitude vector')
    axes[3].legend()

    axes[3].set_xlabel('Time')

    if path_to_save is not None:
        plt.savefig(path_to_save, format='pdf', bbox_inches='tight')


def plot_all_activities_data(samples_static: List[AccelerometerSample], samples_walking: List[AccelerometerSample],
                             samples_running: List[AccelerometerSample], samples_vehicle: List[AccelerometerSample],
                             path_to_save=None):
    plt.style.use('bmh')

    plt.rcParams['font.family'] = 'Gotham XNarrow'
    plt.rcParams['font.serif'] = 'Gotham XNarrow'
    plt.rcParams['font.monospace'] = 'Monaco'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'normal'
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    # plt.rcParams['legend.fontsize'] = 11
    plt.rcParams['legend.fontsize'] = 7
    plt.rcParams['figure.titlesize'] = 13
    plt.rcParams['legend.fontsize'] = 9

    # fig, axes = plt.subplots(4, 4, sharex=True)
    fig, axes = plt.subplots(4, 4)
    above_title = '-'
    shown_y_label = False

    for i in range(0, 4):
        if i == 0:
            samples = samples_static
            above_title = 'Static'
        if i == 1:
            samples = samples_walking
            above_title = 'Walking'
        if i == 2:
            samples = samples_running
            above_title = 'Running'
        if i == 3:
            samples = samples_vehicle
            above_title = 'Vehicle'

        xs = list(map(lambda x: x.timestamp, samples))
        ys = list(map(lambda x: x.x, samples))
        axes[0][i].plot(xs, ys, label='X axis', linewidth='1')
        axes[0][i].legend()
        axes[0][i].set_title(above_title)

        ys = list(map(lambda x: x.y, samples))
        axes[1][i].plot(xs, ys, label='Y axis', linewidth='1')
        axes[1][i].legend()

        ys = list(map(lambda x: x.z, samples))
        axes[2][i].plot(xs, ys, label='Z axis', linewidth='1')
        axes[2][i].legend()

        ys = calculate_magnitude_vector(samples)
        axes[3][i].plot(xs, ys, label='Magnitude vector', linewidth='1')
        axes[3][i].legend()

        axes[3][i].set_xlabel('Time')

        if not shown_y_label:
            axes[0][i].set_ylabel('Acc (Earth G off)')
            axes[1][i].set_ylabel('Acc (Earth G off)')
            axes[2][i].set_ylabel('Acc (Earth G off)')
            axes[3][i].set_ylabel('Magnitude vector')
            shown_y_label = True

    # plt.tight_layout()
    # axis.zaxis.labelpad = 15

    if path_to_save is not None:
        plt.savefig(path_to_save, format='pdf', bbox_inches='tight')


def plot_some_activities_data(samples_list, activities_string):
    plt.style.use('bmh')

    plt.rcParams['font.family'] = 'Gotham XNarrow'
    plt.rcParams['font.serif'] = 'Gotham XNarrow'
    plt.rcParams['font.monospace'] = 'Monaco'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'normal'
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 7
    plt.rcParams['figure.titlesize'] = 13
    plt.rcParams['legend.fontsize'] = 9

    fig, axes = plt.subplots(4, len(activities_string))
    shown_y_label = False

    for i in range(0, len(activities_string)):
        samples = samples_list[i]

        xs = list(map(lambda x: x.timestamp, samples))
        ys = list(map(lambda x: x.x, samples))
        axes[0][i].plot(xs, ys, label='X axis', linewidth='1')
        axes[0][i].legend()
        axes[0][i].set_title(activities_string[i])

        ys = list(map(lambda x: x.y, samples))
        axes[1][i].plot(xs, ys, label='Y axis', linewidth='1')
        axes[1][i].legend()

        ys = list(map(lambda x: x.z, samples))
        axes[2][i].plot(xs, ys, label='Z axis', linewidth='1')
        axes[2][i].legend()

        ys = calculate_magnitude_vector(samples)
        axes[3][i].plot(xs, ys, label='Magnitude vector', linewidth='1')
        axes[3][i].legend()

        axes[3][i].set_xlabel('Time')

        if not shown_y_label:
            axes[0][i].set_ylabel('Acc (Earth G off)')
            axes[1][i].set_ylabel('Acc (Earth G off)')
            axes[2][i].set_ylabel('Acc (Earth G off)')
            axes[3][i].set_ylabel('Magnitude vector')
            shown_y_label = True


def plot_statistics(statistics: List[List[Dict]], attributes_to_plot: List[str], actitivy_labels, path_to_save=None):
    plt.style.use('bmh')

    plt.rcParams['font.family'] = 'Gotham XNarrow'
    plt.rcParams['font.serif'] = 'Gotham XNarrow'
    plt.rcParams['font.monospace'] = 'Monaco'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'normal'
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    # plt.rcParams['legend.fontsize'] = 11
    plt.rcParams['legend.fontsize'] = 9
    plt.rcParams['figure.titlesize'] = 14

    fig = plt.figure()
    axis = fig.gca()

    i = 0
    for stats in statistics:
        xs = list(map(lambda x: x[attributes_to_plot[0]], stats))
        ys = list(map(lambda x: x[attributes_to_plot[1]], stats))
        # axis.scatter(x=xs, y=ys, label='Walking')
        axis.scatter(x=xs, y=ys, label=actitivy_labels[i])
        i+=1

    axis.set_xlabel(attributes_to_plot[0])
    axis.set_ylabel(attributes_to_plot[1])

    axis.legend()

    if path_to_save is not None:
        plt.savefig(path_to_save, format='pdf', bbox_inches='tight')


def plot_magnitude_vectors(magnitude_vector_lists, activity_strings):
    plt.style.use('bmh')

    plt.rcParams['font.family'] = 'Gotham XNarrow'
    plt.rcParams['font.serif'] = 'Gotham XNarrow'
    plt.rcParams['font.monospace'] = 'Monaco'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'normal'
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 7
    plt.rcParams['figure.titlesize'] = 13
    plt.rcParams['legend.fontsize'] = 9

    fig = plt.figure()
    axis = fig.gca()

    for i in range(0, len(activity_strings)):
        samples = magnitude_vector_lists[i]

        axis.plot(samples, linewidth='1', label=activity_strings[i])

    axis.legend()


def plot_magnitude_vectors_per_alpha(magnitude_vector_lists, timestamps, alpha_values, single=False):
    plt.style.use('bmh')

    plt.rcParams['font.family'] = 'Gotham XNarrow'
    plt.rcParams['font.serif'] = 'Gotham XNarrow'
    plt.rcParams['font.monospace'] = 'Monaco'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'normal'
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 7
    plt.rcParams['figure.titlesize'] = 13
    plt.rcParams['legend.fontsize'] = 9

    # xs = timestamps

    if single:
        fig = plt.figure()
        ax = fig.gca()
        for index in range(0, len(alpha_values)):
            ys = magnitude_vector_lists[index]
            ax.plot(ys, label='alpha-{}'.format(alpha_values[index]), linewidth='1')
            # ax.plot(xs, ys, label='alpha-{}'.format(alpha_values[index]), linewidth='1')

        ax.set_title('mv with respect of alphas')
        ax.legend()

    else:
        fig, axes = plt.subplots(len(alpha_values))

        for index in range(0, len(alpha_values)):
            ys = magnitude_vector_lists[index]
            axes[index].plot(ys, label='alpha-{}'.format(alpha_values[index]), linewidth='1')
            axes[index].set_title('alpha {}'.format(alpha_values[index]))


def plot_accelerations_and_mag_vectors(samples_list: List[List[AccelerometerSample]], activity_labels):
    plt.style.use('bmh')

    plt.rcParams['font.family'] = 'Gotham XNarrow'
    plt.rcParams['font.serif'] = 'Gotham XNarrow'
    plt.rcParams['font.monospace'] = 'Monaco'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'normal'
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 7
    plt.rcParams['figure.titlesize'] = 13
    plt.rcParams['legend.fontsize'] = 9

    fig, axes = plt.subplots(4)

    i = 0
    for samples in samples_list:
        xs = list(map(lambda x: x.timestamp, samples))
        ys = list(map(lambda x: x.x, samples))
        axes[0].plot(xs, ys, label='{}'.format(activity_labels[i]), linewidth='1')

        ys = list(map(lambda x: x.y, samples))
        axes[1].plot(xs, ys, label='{}'.format(activity_labels[i]), linewidth='1')

        ys = list(map(lambda x: x.z, samples))
        axes[2].plot(xs, ys, label='{}'.format(activity_labels[i]), linewidth='1')

        mv = calculate_magnitude_vector(samples)
        axes[3].plot(xs, mv, label='MV {}'.format(activity_labels[i]), linewidth='1')

        i += 1

    axes[0].legend()
    axes[1].legend()
    axes[2].legend()
    axes[3].legend()


def plot_three_dimensions(statistics: List[Dict], activity_labels: List[str], attributes_to_plot: List[str]):
    plt.style.use('bmh')

    plt.rcParams['font.family'] = 'Gotham XNarrow'
    plt.rcParams['font.serif'] = 'Gotham XNarrow'
    plt.rcParams['font.monospace'] = 'Monaco'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'normal'
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 7
    plt.rcParams['figure.titlesize'] = 13
    plt.rcParams['legend.fontsize'] = 9

    fig = plt.figure()
    axis = fig.gca(projection='3d')

    i = 0
    for stats in statistics:
        xs = list(map(lambda x: x[attributes_to_plot[0]], stats))
        ys = list(map(lambda y: y[attributes_to_plot[1]], stats))
        zs = list(map(lambda z: z[attributes_to_plot[2]], stats))

        # axis.plot(xs=xs, ys=ys, zs=zs, label=activity_labels[i])
        axis.scatter(xs=xs, ys=ys, zs=zs, label=activity_labels[i])
        i += 1

    axis.set_xlabel(attributes_to_plot[0])
    axis.set_ylabel(attributes_to_plot[1])
    axis.set_zlabel(attributes_to_plot[2])

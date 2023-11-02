import copy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
from peegy.layouts.layouts import Layout
from peegy.plot import eeg_plot_tools as eegpt
from peegy.definitions.channel_definitions import Domain
from matplotlib import ticker
from astropy import units as u

__author__ = 'jundurraga'


def plot_time_frequency_responses(dataframe: pd.DataFrame = None,
                                  rows_by: str = None,
                                  cols_by: str = None,
                                  sub_average_time_buffer_size: int = None,
                                  blend_subcategories: bool = False,
                                  time_xlim: [float, float] = None,
                                  time_ylim: [float, float] = None,
                                  freq_xlim: [float, float] = None,
                                  freq_ylim: [float, float] = None,
                                  time_vmarkers: np.array = None,
                                  freq_vmarkers: np.array = None,
                                  freq_vmarkers_style: str = None,
                                  show_individual_waveforms: bool = True,
                                  individual_waveforms_alpha: float = 0.1,
                                  show_sem: bool = False,
                                  sem_alpha: float = 0.2,
                                  show_sd: bool = True,
                                  sd_alpha: float = 0.2,
                                  show_legend: bool = True,
                                  title_by: str = 'row',
                                  title_v_offset: float = 0.0,
                                  ylabel: str = None,
                                  y_unit_to: u.Unit = None,
                                  x_unit_to: u.Unit = None,
                                  fontsize: float = 6,
                                  ) -> plt.figure:
    """
    This function will plot the waveforms contained in a pandas dataframe read using the sqlite_waveforms_to_pandas
    function of pEEGy.
    The rows and columns of the output plot are specified by the factors of the dataframe.
    The output will show the data for each of those factors (both individual and average data).
    :param dataframe: a pandas dataframe returned by sqlite_waveforms_to_pandas function of pEEGy
    :param rows_by: name of the factor in the dataframe for which the rows in the plot will be split
    :param cols_by: name of the factor in the dataframe for which the columns in the plot will be split
    :param sub_average_time_buffer_size: This is a parameter used to sub_average time_domain data. For example, if each
    of your data have 10000 points, and you want to show the average having a length of 1000 samples, you could specify
    sub_average_time_buffer_size = 1000. This will averaged the 10000 points by splitting the data into blocks of 1000
    samples
    :param blend_subcategories: if true, any subcategory present in each column and row will be pull together as
    belonging to the same category
    :param time_xlim: x axis limis for the time-domain panels
    :param time_ylim: y axis limis for the time-domain panels
    :param freq_xlim: x axis limis for the frequency-domain panels
    :param freq_ylim: y axis limis for the frequency-domain panels
    :param time_vmarkers: array with x values to add a vertical marker in the time-domain panels
    :param freq_vmarkers: array with x values to add a vertical marker in the frequency-domain panels
    :param show_individual_waveforms: if true, individual waveforms will be shown.
    :param individual_waveforms_alpha: value between 0 and 1 indicating the alpha level of individual waveforms
    :param show_sem: if true, the standard error of the mean will be shown
    :param sem_alpha: value between 0 and 1 indicating the alpha level of the sem
    :param show_sd: if true, the standard deviation of the mean will be shown
    :param sd_alpha: value between 0 and 1 indicating the alpha level of the standard deviation
    :param show_legend: if True, the legend for any other category present in the dataframe will be shown
    :param title_by: string specifying from which factor you want to show the titles in each panel. This can be: "row",
    "col", or "both"
    :param title_v_offset: float specifying the vertical offset of the title
    :param freq_vmarkers_style: style of the marker in the frequency-domain. If not passed, vertical lines are used.
    :param ylabel: Label to put in the vertical axis. If empty, the Amplitude and unit of it are used.
    :param y_unit_to: Specify the units in which the vertical axis will be displayed
    :param x_unit_to: Specify the units in which the horizontal axis will be displayed
    :param fontsize: the font size
    :return:
    """
    df = copy.copy(dataframe)
    df.reset_index(inplace=True, drop=True)
    _rows_and_cols = []
    # n_rows = 1
    # n_cols = 1
    row_conditions = np.array([1])
    col_conditions = np.array([1])
    unique_row_domains = True
    # unique_col_domains = True
    row_domains = Domain.time
    # col_domains = Domain.time
    if rows_by is not None:
        _rows_and_cols.append(rows_by)
        row_conditions = df[rows_by].astype("category").cat.categories
        row_domains = df.iloc[df[rows_by].index]['domain'].unique()
        unique_row_domains = row_domains.size == 1
        n_rows = row_conditions.size
    else:
        df.loc[:, 'dummy_row'] = 1
        _rows_and_cols.append('dummy_row')
        # row_domains = df['domain']
        n_rows = 1
    idx_rows = np.arange(row_conditions.size)
    if cols_by is not None:
        _rows_and_cols.append(cols_by)
        col_conditions = df[cols_by].astype("category").cat.categories
        # col_domains = df.iloc[df[cols_by].index]['domain'].unique()
        # unique_col_domains = col_domains.size == 1
        # col_domains = df.iloc[df[cols_by].index.values]['domain']
        n_cols = col_conditions.size
    else:
        df.loc[:, 'dummy_col'] = 1
        _rows_and_cols.append('dummy_col')
        n_cols = 1
        # col_domains = df['domain']
    idx_cols = np.arange(col_conditions.size)

    # common_x_axis = np.unique(col_conditions).size == 1
    groups = df.groupby(_rows_and_cols, observed=False)
    fig_out, ax = plt.subplots(n_rows, n_cols)
    gs = gridspec.GridSpec(n_rows, n_cols)
    all_ax_row_label = []
    for _id, ((_current_row_group, _current_col_group), _group) in enumerate(groups):
        _current_group = _group
        _colors = plt.cm.get_cmap('viridis', _current_group.shape[0])
        if blend_subcategories:
            _current_group = _group.iloc[[0]].copy().reset_index()
            if _current_group['y'].shape[0] > 1:
                _current_group['y'] = _current_group['y'].apply(lambda x: np.vstack(_group.y).T)
            # _colors = plt.cm.get_cmap('viridis', 1)
        _idx_row = idx_rows[_current_row_group == row_conditions].squeeze()
        _idx_col = idx_cols[_current_col_group == col_conditions].squeeze()
        _columns_legends = []

        _y_unit_to = y_unit_to
        _x_unit_to = x_unit_to
        for _col in _current_group:
            if _col in ['x', 'y']:
                continue
            if len(_current_group[_col].unique()) > 1:
                _columns_legends.append(_col)

        for _i, (_, _row) in enumerate(_current_group.iterrows()):
            _group_label = []
            for _ic, _col in enumerate(_columns_legends):
                _group_label.append(str(_row[_col]))
            _group_label = '/'.join(_group_label)
            y_unit = u.Quantity(1, _row['y_unit'])
            x_unit = u.Quantity(1, _row['x_unit'])
            if _y_unit_to is None:
                _y_unit_to = y_unit.unit
            if _x_unit_to is None:
                _x_unit_to = x_unit.unit
            y = (_row['y'] * y_unit).to(_y_unit_to)
            x = (_row['x'] * x_unit).to(_x_unit_to)
            fs = _row['x_fs']

            _domain = _row['domain']
            if y.ndim == 1:
                y = y.reshape([-1, 1])
            y_single_responses = y

            if _domain == 'time' and sub_average_time_buffer_size is not None:
                fs = 1 / np.mean(np.diff(x))
                used_samples = int(np.floor(y.shape[0] // sub_average_time_buffer_size) * sub_average_time_buffer_size)
                y_f = y[0: used_samples, :]
                y_f = np.transpose(np.reshape(y_f, (sub_average_time_buffer_size, -1, y_f.shape[1]), order='F'),
                                   [0, 2, 1])
                # demean
                y_f = np.mean(y_f, axis=2)
                x = np.arange(0, sub_average_time_buffer_size) / fs
                y_single_responses = y_f - np.mean(y_f, axis=0)

            ax = plt.subplot(gs[_idx_row, _idx_col])
            title = ''
            if title_by == 'row':
                title = '{:}'.format(_current_row_group)

            if title_by == 'col':
                title = '{:}'.format(_current_col_group)

            if title_by == 'both':
                title = '{:} / {:}'.format(_current_row_group, _current_col_group)

            if title_by == 'col':
                if _idx_row == 0:
                    ax.set_title(title, y=1 + title_v_offset, size=fontsize)
            else:
                ax.set_title(title, y=1 + title_v_offset, size=fontsize)

            if _domain == 'time':
                y_mean = np.mean(y_single_responses, axis=1)
                y_sd = np.std(y_single_responses, axis=1)
                y_sem = y_sd / np.sqrt(y_single_responses.shape[1])
                if show_individual_waveforms:
                    ax.plot(x, y_single_responses,
                            linewidth=0.5,
                            alpha=individual_waveforms_alpha,
                            color=_colors(_i)
                            )
            if _domain == 'frequency':
                y_mean = np.mean(np.abs(y_single_responses), axis=1)
                y_sd = np.std(np.abs(y_single_responses), axis=1)
                y_sem = y_sd / np.sqrt(y_single_responses.shape[1])
                if show_individual_waveforms:
                    ax.plot(x, np.abs(y_single_responses),
                            linewidth=0.5,
                            alpha=individual_waveforms_alpha,
                            color=_colors(_i))

            ax.plot(x, y_mean,
                    color=_colors(_i),
                    linewidth=0.8,
                    label=_group_label)
            if ylabel is None:
                ax.set_ylabel('Amplitude [{:}]'.format(y_mean.unit), size=fontsize)
            if show_sem:
                ax.fill_between(x.value,
                                (y_mean - y_sem).value,
                                (y_mean + y_sem).value,
                                alpha=sem_alpha,
                                edgecolor="none",
                                facecolor=_colors(_i))
            if show_sd:
                ax.fill_between(x.value,
                                (y_mean - y_sd).value,
                                (y_mean + y_sd).value,
                                alpha=sd_alpha,
                                edgecolor="none",
                                facecolor=_colors(_i))

            _last_col_ax = plt.subplot(gs[_idx_row, n_cols - 1])
            ax_row_label = _last_col_ax.twinx()
            ax_row_label.set_ylabel(_current_row_group, size=fontsize)
            ax_row_label.set_yticklabels([])
            ax_row_label.tick_params(
                axis='y',  # changes apply to the x-axis
                which='both',  # both major and minor ticks are affected
                right=False,  # ticks along the bottom edge are off
                left=False,  # ticks along the top edge are off
                labelleft=True)
            all_ax_row_label.append(ax_row_label)

            if _domain == 'time':
                if time_xlim is not None:
                    ax.set_xlim(time_xlim)
                if time_ylim is not None:
                    ax.set_ylim(time_ylim)
                if time_vmarkers is not None:
                    [ax.axvline(_t, color='k', linestyle=':', linewidth=0.5) for _t in time_vmarkers]
                ax.set_xlabel('Time [{:}]'.format(x.unit), size=fontsize)

            if _domain == 'frequency':
                if freq_xlim is not None:
                    ax.set_xlim(freq_xlim)
                if freq_ylim is not None:
                    ax.set_ylim(freq_ylim)
                if freq_vmarkers is not None:
                    if freq_vmarkers_style is None:
                        [ax.axvline(_f, color='k', linestyle=':', linewidth=0.5) for _f in freq_vmarkers]
                    else:
                        y_min, y_max = ax.get_ylim()
                        [ax.plot(_f, y_max * 0.93,
                                 color='g',
                                 marker=freq_vmarkers_style,
                                 markersize=3) for _f in freq_vmarkers]
                ax.set_xlabel('Frequency [{:}]'.format(x.unit), size=fontsize)
            handles, labels = ax.get_legend_handles_labels()
            if len(labels) > 1 and show_legend:
                ax.legend(handles,
                          labels,
                          loc='upper center',
                          fontsize=8,
                          frameon=False,
                          ncol=len(labels))

    all_axes = fig_out.get_axes()
    all_axis_with_data = np.all([ax.has_data() for ax in all_axes if ax not in all_ax_row_label])

    if ylabel is None:
        if y_unit_to is not None:
            fig_out.supylabel('Amplitude [{:}]'.format(y_unit_to), size=fontsize)
    else:
        fig_out.supylabel(ylabel, size=fontsize)
    if unique_row_domains and all_axis_with_data and np.all(row_domains == 'time') and n_cols > 1:
        fig_out.supxlabel('Time [{:}]'.format(_x_unit_to), size=fontsize)
    if unique_row_domains and all_axis_with_data and np.all(row_domains == 'frequency') and n_cols > 1:
        fig_out.supxlabel('Frequency [{:}]'.format(_x_unit_to), size=fontsize)

    for ax in all_axes:
        if not ax.has_data() and ax not in all_ax_row_label:
            ax.get_xaxis().set_visible(False)
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_xlabel('')
            continue
        ax.spines['top'].set_visible(False)
        if unique_row_domains and all_axis_with_data:
            if not ax.get_subplotspec().is_last_row():
                ax.set_xticklabels([])
                ax.set_xlabel('')
            if n_cols > 1:
                ax.set_xlabel('')
        ax.spines['left'].set_visible(True)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=6)

    inch = 2.54
    fig_out.set_size_inches(12.0 / inch, 2.25 * len(row_conditions) / inch)
    fig_out.subplots_adjust(top=0.98, bottom=0.08, hspace=0.0, left=0.15, right=0.95)
    return fig_out


def plot_topographic_maps(dataframe: pd.DataFrame = None,
                          rows_by: str = None,
                          cols_by: str = None,
                          subject_id_column: str = 'subject_id',
                          normalize_by: str = 'subject_id',
                          channels_column: str = 'channel',
                          title: str = '',
                          topographic_value: str = None,
                          layout: str = None,
                          title_by: str = 'row',
                          title_v_offset: float = 0.0,
                          fontsize: float = 6,
                          grid_size: np.complex_ = 600j,
                          color_map_label: str = None,
                          normalize: bool = False,
                          show_sensors: bool = True,
                          show_sensor_label: bool = False,
                          n_contour_levels: int = 35,
                          max_topographic_value: float = None,
                          min_topographic_value: float = None,
                          contour_line_width: float = 0.1,
                          apply_function: object = lambda x: np.mean(x, axis=2),
                          fun_args: dict = {}
                          ) -> plt.figure:
    """
    This function will plot the waveforms contained in a pandas dataframe read using the sqlite_waveforms_to_pandas
    function of pEEGy.
    The rows and columns of the output plot are specified by the factors of the dataframe.
    The output will show the data for each of those factors (both individual and average data)
    :param dataframe: a pandas dataframe returned by sqlite_waveforms_to_pandas function of pEEGy
    :param rows_by: name of the factor in the dataframe for which the rows in the plot will be split
    :param cols_by: name of the factor in the dataframe for which the columns in the plot will be split
    :param subject_id_column: string indicating the column name with subject ids
    :param normalize_by: string indicating the column that will be used to normalized the data
    :param channels_column: name of column containing channel labels
    :param title: title of the figure
    :param topographic_value: name of column containing the value to be shown by the topographic map
    :param layout: path or name of the layout to be used
    :param title_by: string specifying from which factor you want to show the titles in each panel. This can be: "row",
    "col", or "both"
    :param title_v_offset: float specifying the vertical offset of the title
    :param fontsize: the fontsize
    :param grid_size: complex number indicating the size of the grid,
    :param color_map_label: string with the label that would be use of the colourmap. If empty, the default value will
    be the topographic_value
    :param normalize: if True, topographic maps will be normalized within normalize_by
    :param show_sensors: if True, the position of the sensors will be shown
    :param show_sensor_label: if True, the label of the sensor will be shown
    :param n_contour_levels: number of contour lines to plot
    :param min_topographic_value: if given, the colour scale will be restricted to have this value as maximum, otherwise
    it will be determined from the data.
    :param max_topographic_value: if given, the colour scale will be restricted to have this value as minimum, otherwise
    it will be determined from the data.
    :param contour_line_width: float indicating the with (in points) of the contour lines
    :param apply_function: function to be applied to each subgroup
    :param fun_args: extra arguments to be used by apply_function. This is a dictionary with the desired parameters
    :return:
    """
    df = copy.copy(dataframe)
    _rows_and_cols = []
    row_conditions = np.array([1])
    col_conditions = np.array([1])
    if rows_by is not None:
        _rows_and_cols.append(rows_by)
        row_conditions = df[rows_by].astype("category").cat.categories
        n_rows = row_conditions.size
    else:
        df.loc[:, 'dummy_row'] = 1
        _rows_and_cols.append('dummy_row')
        n_rows = 1
    idx_rows = np.arange(row_conditions.size)

    if cols_by is not None:
        _rows_and_cols.append(cols_by)
        col_conditions = df[cols_by].astype("category").cat.categories
        n_cols = col_conditions.size
    else:
        df.loc[:, 'dummy_col'] = 1
        _rows_and_cols.append('dummy_col')
        n_cols = 1
    idx_cols = np.arange(col_conditions.size)

    if not len(_rows_and_cols):
        df['dummy_row'] = 1
        df['dummy_col'] = 1
        _rows_and_cols = ['dummy_row', 'dummy_col']
    # check if input dataframe already contains the potentials. If not, then we extract them
    if 'potentials' in df.keys():
        if normalize:
            if normalize_by is not None:
                df = df.assign(
                    potentials=df.groupby(
                        normalize_by)['potentials'].transform(
                        lambda x: x / np.ma.max(np.abs(np.ma.dstack([_val for _val in x])))))
            else:
                df = df.assign(
                    potentials=df.groupby(
                        [True] * len(df))['potentials'].transform(
                        lambda x: x / np.ma.max(np.abs(np.ma.dstack([_val for _val in x])))))
        sub_groups = df
    else:
        df['topo_value'] = df[topographic_value]
        if normalize:
            df = df.assign(
                topo_value=df.groupby(
                    [normalize_by])[topographic_value].transform(lambda x: x / np.max(np.abs(x))))
        sub_groups = get_topographic_maps_as_df(dataframe=df,
                                                subject_id_column=subject_id_column,
                                                group_by=_rows_and_cols,
                                                channels_column='channel',
                                                topographic_value='topo_value',
                                                layout=layout,
                                                apply_function=apply_function,
                                                fun_args=fun_args
                                                )
    if color_map_label is None:
        color_map_label = topographic_value
    groups = sub_groups.groupby(_rows_and_cols)
    fig_out = plt.figure(constrained_layout=True)
    widths = [1.0] * n_cols
    heights = [1.0] * n_rows
    heights.append(0.1)
    widths.append(0.01)
    gs = fig_out.add_gridspec(ncols=n_cols + 1, nrows=n_rows + 1,
                              width_ratios=widths,
                              height_ratios=heights)
    if max_topographic_value is None:
        max_sub_groups = sub_groups[sub_groups.potentials.apply(lambda x: np.size(x) > 1)]
        max_sub = max_sub_groups.potentials.apply(
            lambda x: np.ma.dstack([_val for _val in x]).max()).max()
    else:
        max_sub = max_topographic_value

    if min_topographic_value is None:
        min_sub_groups = sub_groups[sub_groups.potentials.apply(lambda x: np.size(x) > 1)]
        min_sub = min_sub_groups.potentials.apply(
            lambda x: np.ma.dstack([_val for _val in x]).min()).min()
    else:
        min_sub = min_topographic_value
    max_distance = sub_groups.max_distance.max()
    all_ax_row_label = []
    for _id, ((_current_row_group, _current_col_group), _group) in enumerate(groups):
        if _group.shape[0] == 0 or np.all(np.isnan(_group.potentials.values[0])):
            continue
        _idx_row = idx_rows[_current_row_group == row_conditions].squeeze()
        _idx_col = idx_cols[_current_col_group == col_conditions].squeeze()
        ax = plt.subplot(gs[_idx_row, _idx_col])
        panel_title = ''
        if title_by == 'row':
            panel_title = '{:}'.format(_current_row_group)
        if title_by == 'col':
            panel_title = '{:}'.format(_current_col_group)

        if title_by == 'both':
            panel_title = '{:} / {:}'.format(_current_row_group, _current_col_group)

        ax.set_title(panel_title, y=1 + title_v_offset, size=fontsize)
        if _group.potentials.values.size > 1:
            std_average = _group.potentials.apply(
                lambda x: apply_function(np.ma.dstack([_val for _val in x]), *fun_args)).values[0]
        else:
            std_average = _group.potentials.values[0]
        ax_im = ax.imshow(std_average.T, origin='lower',
                          extent=(-max_distance, max_distance, -max_distance, max_distance),
                          vmin=min_sub,
                          vmax=max_sub,
                          aspect=1.0)
        ax_im.set_cmap('nipy_spectral')

        levels = np.linspace(min_sub, max_sub, n_contour_levels)
        ax.contour(std_average.T,
                   levels,
                   origin='lower',
                   extent=(-max_distance, max_distance, -max_distance, max_distance),
                   linewidths=contour_line_width,
                   colors='k',
                   linestyles='solid')
        ax.autoscale(enable=False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        _last_col_ax = plt.subplot(gs[_idx_row, n_cols])
        _last_col_ax.set_xticks([])
        _last_col_ax.set_yticks([])
        _last_col_ax.axis('off')
        ax_row_label = _last_col_ax.twinx()
        ax_row_label.autoscale(enable=False)
        ax_row_label.set_ylabel(_current_row_group, size=fontsize)
        ax_row_label.set_yticklabels([])
        ax_row_label.tick_params(
            axis='y',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            right=False,  # ticks along the bottom edge are off
            left=False,  # ticks along the top edge are off
            labelleft=True)
        ax_row_label.spines['left'].set_visible(False)
        ax_row_label.spines['right'].set_visible(False)
        ax_row_label.spines['top'].set_visible(False)
        ax_row_label.spines['bottom'].set_visible(False)
        ax_row_label.set_xticks([])
        ax_row_label.set_yticks([])
        all_ax_row_label.append(ax_row_label)
        # plot color bar

        if _id == 0:
            c_bar_ax = plt.subplot(gs[-1, :])
            c_bar = fig_out.colorbar(ax_im, cax=c_bar_ax, orientation='horizontal', format='%.1f')
            c_bar.set_label(color_map_label, fontsize=fontsize)
            tick_locator = ticker.MaxNLocator(nbins=3)
            c_bar.locator = tick_locator
            c_bar.update_ticks()
            c_bar.ax.tick_params(labelsize=fontsize)
        channels = _group.channels.values[0]
        channel_labels = [ch['label'] for ch in channels]
        ax.plot(0, max_distance * 1.0, '|', markersize=8, color='k')
        if show_sensors:
            _lay = Layout()
            _layout = _lay.get_layout(file_name=layout)
            _layout = np.array([_l for _l in _layout if _l.label not in ['COMNT', 'SCALE']])
            for i, lay in enumerate(_layout):
                if lay.label in channel_labels:
                    ax.plot(lay.x, lay.y, 'o', color='b', markersize=0.2)
                else:
                    ax.plot(lay.x, lay.y, 'o', color='grey', markersize=0.2)
                if show_sensor_label:
                    ax.text(lay.x, lay.y, s=lay.label, fontsize=6)

    all_axes = fig_out.get_axes()
    for ax in all_axes:
        if ax == c_bar.ax:
            continue
        ax.spines['top'].set_visible(False)
        ax.set_xticklabels([])
        ax.set_xlabel('')
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
    inch = 2.54
    fig_out.suptitle(title)
    fig_out.set_size_inches(3.2 * len(col_conditions) / inch, h=3.2 * len(row_conditions) / inch)
    return fig_out


def get_topographic_maps(df,
                         subject_id_column: str = 'subject_id',
                         channels_column: str = 'channel',
                         topographic_value: str = None,
                         layout: str = None,
                         grid_size: np.complex_ = 600j,
                         apply_function: object = None,
                         fun_args: dict = {}):
    _lay = Layout()
    _layout = _lay.get_layout(file_name=layout)
    _layout = np.array([_l for _l in _layout if _l.label not in ['COMNT', 'SCALE']])
    _single_responses = np.array([])

    _subject_groups = df.groupby(subject_id_column)
    for _, (_id_sub, _sub_group) in enumerate(_subject_groups):
        x = []
        y = []
        z = []
        channels = []
        max_potential = -np.inf
        print('Using {:} data points to generate topographic map'.format(_sub_group.shape[0]))
        for _i, (_, _row) in enumerate(_sub_group.iterrows()):
            ch = _row[channels_column]
            amp = _row[topographic_value]
            for _l in _layout:
                if _l.label == ch:
                    x.append(_l.x)
                    y.append(_l.y)
                    z.append(amp)
            channels.append({'label': ch})

        _potentials, max_distance = eegpt.interpolate_potential_fields(x=np.array(x).reshape(-1, 1),
                                                                       y=np.array(y).reshape(-1, 1),
                                                                       z=np.array(z).reshape(-1, 1),
                                                                       grid=grid_size)
        max_potential
        if not _single_responses.size:
            _single_responses = _potentials[:, :, None]
        else:
            _single_responses = np.ma.dstack((_single_responses, _potentials))
    if apply_function is not None:
        _single_responses = apply_function(_single_responses, **fun_args)
    out = pd.Series(data={'potentials': _single_responses,
                          'max_distance': max_distance,
                          'channels': channels})
    return out


def get_topographic_maps_as_df(dataframe: pd.DataFrame = None,
                               group_by: [str] = None,
                               subject_id_column: str = 'subject_id',
                               channels_column: str = 'channel',
                               topographic_value: str = None,
                               layout: str = None,
                               grid_size: np.complex_ = 600j,
                               apply_function: object = np.mean,
                               fun_args: dict = {}
                               ) -> pd.DataFrame:
    """
    This function will plot the waveforms contained in a pandas dataframe read using the sqlite_waveforms_to_pandas
    function of pEEGy.
    The rows and columns of the output plot are specified by the factors of the dataframe.
    The output will show the data for each of those factors (both individual and average data).
    :param dataframe: a pandas dataframe returned by sqlite_waveforms_to_pandas function of pEEGy.
    :param group_by: name of factors to group and obtain potentials.
    :param subject_id_column: string indicating the column name with subject ids
    :param channels_column: name of column containing channel labels
    :param topographic_value: name of column containing the value to be shown by the topographic map
    :param layout: path or name of the layout to be used
    :param grid_size: complex number indicating the size of the grid,
    :return:
    """
    df = copy.copy(dataframe)
    df['topo_value'] = df[topographic_value]
    group_by = [True] * len(df) if group_by is None else group_by
    sub_groups = df.groupby(group_by, group_keys=False).apply(
        lambda x: get_topographic_maps(x,
                                       subject_id_column=subject_id_column,
                                       layout=layout,
                                       channels_column=channels_column,
                                       topographic_value='topo_value',
                                       grid_size=grid_size,
                                       apply_function=apply_function,
                                       fun_args=fun_args)).reset_index()
    return sub_groups

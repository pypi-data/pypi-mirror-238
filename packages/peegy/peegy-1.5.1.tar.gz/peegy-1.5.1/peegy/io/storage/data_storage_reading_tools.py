import numpy as np
import pandas as pd
from peegy.definitions.channel_definitions import Domain
import sqlite3
from scipy.interpolate import interp1d
import io

__author__ = 'jundurraga-ucl'


class PandasDataPages(dict):
    """This class manages pandas dataframes appended to it.
    When data frames are appended the PandasDataPages specific dataframe can be called by its name
    """

    def __init__(self):
        super(PandasDataPages, self).__init__()

    def __setitem__(self, name, dataframe: pd.DataFrame = None):
        # optional processing here
        assert isinstance(dataframe, pd.DataFrame)
        name = self.ensure_unique_name(label=name)
        super(PandasDataPages, self).__setitem__(name, dataframe)
        # we add the new item as class variable
        setattr(self, name, dataframe)

    def append(self, item: object, name=None):
        if name is None:
            name = type(item).__name__
        self[name] = item

    def ensure_unique_name(self, label: str = None):
        all_names = [_key for _key in self.keys()]
        _label = label
        count = 0
        while _label in all_names:
            _label = label + '_' + str(count)
            count = count + 1
        if count > 0:
            print('PandasDataPages item "{:}" already exists. Renamed to "{:}"'.format(label, _label))
        return _label

    def __getitem__(self, key):
        return super(PandasDataPages, self).__getitem__(key)


def sqlite_tables_to_pandas(database_path: str = None,
                            tables: [str] = None) -> pd.DataFrame:
    """
    This function will return a pandas dataframe containing the desired tables from a pEEGy .sqlite database.
    A pEEGy database will always contain a table 'subjects', 'measurement_info' , 'stimuli', 'recording'.
    Each subject will be linked to measurement by their id. Similarly, each measurement will be linked to each stimulus
    by its id.
    Any other table, for example, recording, waveforms, hotelling_t2_time, hotelling_t2_freq, f_test_time, f_test_freq,
    or other tables created by the user, will be uniquely related to each subject, measurement, recording, and stimuli
    by id_subject, id_measurement, id_recording, and _id_stimuli, respectively.
    This function will provide a user-friendly pandas dataframe by pooling together this information by indexing the
    corresponding ids to their respective values.
    :param database_path: path to the database from which we will read the tables
    :param tables: a list of strings containing the tables want to read. Make sure these tables are present in the
    database
    :return: a pandas dataframe with the respective tables.
    """
    out = PandasDataPages()
    db = sqlite3.connect(database_path)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables = [_tables[0] for _tables in cursor.fetchall()]
    extra_tables = ''
    extra_outputs = ''
    extra_join = ''
    if 'recording' in all_tables:
        extra_tables = extra_tables.join('JOIN recording REC ON REC.id_measurement = MES.id ')
        extra_outputs = extra_outputs.join('{:}.*, '.format('REC'))
        extra_join = 'and  TAB.id_recording == REC.id'

    for _table in tables:
        df = pd.read_sql_query('SELECT SUB.*, '
                               'MES.*, '
                               'STI.*, '
                               '{:}'
                               'TAB.* '
                               'FROM subjects as SUB '
                               'JOIN measurement_info MES ON (MES.id_subject = SUB.id) '
                               'JOIN stimuli STI ON STI.id_measurement = MES.id '
                               '{:}'
                               'JOIN {:} as TAB ON TAB.id_stimuli == STI.id {:}'.format(extra_outputs,
                                                                                        extra_tables,
                                                                                        _table,
                                                                                        extra_join),
                               db)
        out[_table] = df
    return out


def sqlite_waveforms_to_pandas(database_path: str = None,
                               group_factors: [str] = None,
                               user_query: [str] = None,
                               tables: [str] = None,
                               channels: [str] = None,
                               simuli_columns: list[str] = None,
                               ) -> pd.DataFrame:
    """
    This function will return a pandas dataframe containing the waveforms for the specified group_factors.
    The data is assumed to come from a pEEGy .sqlite database.
    A pEEGy database will always contain a table 'subjects', 'measurement_info' , 'stimuli', 'recording'.
    Each subject will be linked to measurement by their id. Similarly, each measurement will be linked to each stimulus
    by its id.
    Any other table, for example, recording, waveforms, hotelling_t2_time, hotelling_t2_freq, f_test_time, f_test_freq,
    or other tables created by the user, will be uniquely related to each subject, measurement, recording, and stimuli
    by id_subject, id_measurement, id_recording, and _id_stimuli, respectively.
    This function will provide a user-friendly pandas dataframe by pooling together this information with the waveforms.
    For each grouping factor, the waveforms will be pooling together in a ndim numpy array.
    If data have not consistent number of samples, then the x axis of the first waveform for a given domain (time or
    frequency) will be used as the reference. All the rest will be interpolated and sampled to that initial x axis.
    In this way a single matrix will be returned with the data for each grouping factor.
    To avoid this last step, you should make sure that all data stored in the database are epoched having the same
    length (fixed pre_stimulus_interval and post_stimulus_interval).
    :param database_path: path to the database from which we will read the tables
    :param group_factors: a list of strings containing the groups for which you want to pool the data. For example,
    if you want to group all the waveforms from a given stimulus parameter in the stimuli table of the database (e.g.
    Amplitude and Frequency; both of which are columns in the table stimuli) you could define the group factors as
    group_factors = ['Amplitude', 'Frequency']. The returned output will then contain rows grouped by each level within
    each factor whilst the waveforms (x and y columns) will contain the data for grouped for each of these levels
    :param user_query: This parameter can be used to include or exclude data based on a logical condition, e.g.
    'subject_id != "S1"'
    :param tables: list of strings indicating the names of other generated tables that will be join to the output
    dataframe. The tables should contain 'subjects', 'measurement_info' , 'stimuli', 'recording' columns so they can
    be joined.
    :param channels: list of string specifying for which channels you want to extract the waveforms. If empty, all
    channels will be returned.
    :param simuli_columns: if not None, then it should indicate which columns to read (it can include an alias for the
     specific columns to read. For example ['channel as ch', 'subject_id as subject'] or ['channel']
    :return: a pandas dataframe with the data grouped by group_factors.
    """
    db = sqlite3.connect(database_path)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables = [_tables[0] for _tables in cursor.fetchall()]

    if channels is not None:
        channels_str = ','.join(['"{:}"'.format(_ch) for _ch in channels])
        channels_str = 'WAVE.channel IN ({:}) and'.format(channels_str)
    extra_tables = ''
    extra_outputs = ''
    if 'recording' in all_tables:
        extra_tables = extra_tables.join('JOIN recording REC ON REC.id_measurement = MES.id ')
        extra_outputs = extra_outputs.join('{:}.*, '.format('REC'))

    if tables is not None:
        extra_tables = extra_tables.join(['JOIN {:} ON {:}.id_stimuli = STI.id '.format(_tab, _tab) for
                                          _tab in tables])
        extra_outputs = extra_outputs.join(['{:}.*, '.format(_tab) for
                                            _tab in tables])
    if simuli_columns is None:
        sim_query = 'STI.*, '
    else:
        sim_query = ''.join(['STI.{:}, '.format(_acro) for _acro in simuli_columns])

    df = pd.read_sql_query(
        'SELECT SUB.*, '
        'MES.*, '
        '{:}'
        '{:}'
        'WAVE.* '
        'FROM subjects as SUB '
        'JOIN measurement_info MES ON MES.id_subject = SUB.id '
        'JOIN stimuli STI ON STI.id_measurement = MES.id '
        '{:}'
        'INNER JOIN waveforms WAVE ON ({:} '
        'WAVE.id_stimuli = STI.id) '.format(sim_query,
                                            extra_outputs,
                                            extra_tables,
                                            channels_str),
        db)
    df = df.loc[:, ~df.columns.duplicated()]
    if user_query is not None:
        df = df.query(user_query)
    out_pd = pd.DataFrame()
    if group_factors is None:
        group_factors = ['domain']
    else:
        group_factors = list(set.union(set(group_factors), set(['domain'])))

    groups = df.groupby(group_factors)
    n_s_time = None
    x_time = None
    n_s_freq = None
    x_freq = None
    for _group_value, _group in groups:
        y = np.array([])
        x = np.array([])
        for index, row in _group.iterrows():
            try:
                x_data = np.load(io.BytesIO(row['x']))
                y_data = np.load(io.BytesIO(row['y']))
            except ValueError:
                x_data = np.frombuffer(io.BytesIO(row['x']).read())
                y_data = np.frombuffer(io.BytesIO(row['y']).read())
            except ValueError:
                print("Could not read data from database")

            x_unit = row['x_unit']
            y_unit = row['y_unit']
            if row['domain'] == Domain.time and n_s_time is None:
                n_s_time = x_data.size
                x_time = x_data
            if row['domain'] == Domain.frequency and n_s_freq is None:
                n_s_freq = x_data.size
                x_freq = x_data
            if row['domain'] == Domain.time and n_s_time != x_data.size:
                f = interp1d(x_data, y_data, fill_value="extrapolate")
                y_data = f(x_time)
                x_data = x_time
            if row['domain'] == Domain.frequency and n_s_freq != x_data.size:
                f = interp1d(x_data, y_data, fill_value="extrapolate")
                y_data = f(x_freq)
                x_data = x_freq
            if y.size == 0:
                y = y_data
                x = x_data
            else:
                y = np.vstack((y, y_data))
            if row['domain'] == Domain.time:
                if 'fs' in row.index:
                    fs = row['fs']
                else:
                    fs = 1 / np.mean(np.diff(x))
            if row['domain'] == Domain.frequency:
                # the fs here is a guess assuming the rfft has all samples
                n = y_data.shape[0]
                if np.mod(n, 2) == 1:
                    time_size = 2 * (n - 1)
                else:
                    time_size = 2 * n + 1
                if 'fs' in row.index:
                    fs = row['fs']
                else:
                    fs = time_size / (1 / np.mean(np.diff(x)))
        if len(group_factors) == 1:
            pars = dict(list(zip(group_factors, [_group_value])))
        else:
            pars = dict(list(zip(group_factors, _group_value)))
        out_pd = pd.concat([out_pd, pd.DataFrame([dict(pars, **{'x': x,
                                                                'y': y.T,
                                                                'x_fs': fs,
                                                                'x_unit': x_unit,
                                                                'y_unit': y_unit
                                                                })])],
                           ignore_index=True)
    return out_pd

import astropy.units as u
import pandas as pd


def parse_eclipse_data(
        file_name: str = None):
    """
    This function will read and return the data from Eclipse .xls files
    :param file_name: path to the file
    """
    # get information about recording
    header = pd.read_csv(file_name, nrows=1, header=0, delimiter='\t', lineterminator='\n')
    header = header.loc[:, ~header.columns.str.contains('^Unnamed')]
    header = header.iloc[0]
    n_bits = 16
    voltage_range = header['Volt/bit(nV)'] * 2 ** n_bits * u.nV
    print(voltage_range)
    # extract data in all buffers
    _data = pd.read_csv(file_name, skiprows=2, delimiter='\t', lineterminator='\n', index_col=0)
    _data_buffer_a = _data[_data.index.isin(['(A-buffer)'])]
    _data_buffer_b = _data[_data.index.isin(['(B-buffer)'])]
    # organize and scale data
    data = _data.to_numpy().T * header['Volt/bit(nV)'] * u.nV
    data = data[:, None, :].to(u.uV)

    data_buffer_a = _data_buffer_a.to_numpy().T * header['Volt/bit(nV)'] * u.nV
    data_buffer_a = data_buffer_a[:, None, :].to(u.uV)

    data_buffer_b = _data_buffer_b.to_numpy().T * header['Volt/bit(nV)'] * u.nV
    data_buffer_b = data_buffer_b[:, None, :].to(u.uV)
    return header, data, data_buffer_a, data_buffer_b

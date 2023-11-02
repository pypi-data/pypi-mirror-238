import peegy.io.xml_tools as x_tools
import numpy as np
import os
from os import path
import json
import zipfile as zip_f
import glob


def get_measurement_info_from_zip(zip_file_name):
    with zip_f.ZipFile(zip_file_name, 'r') as my_zip:
        files = my_zip.infolist()
        m_file = my_zip.open(files[0].filename, 'r')
        content = m_file.readlines()
        _, _extension = path.splitext(files[0].filename)
        if _extension == '.xml':
            measurement_info = x_tools.xml_string_to_dict(''.join(content))
        if _extension == '.json':
            measurement_info = json.loads(str.replace(content[0].decode("utf-8"), 'Inf', '''100000'''))
        return measurement_info


def get_extsys_parameters(parameter_files=['']):
    parameters = []
    for i, _file_name in enumerate(parameter_files):
        parameters.append(get_measurement_info_from_zip(_file_name))
    dates = [par['Measurement']['MeasurementModule']['Date'] for x, par in enumerate(parameters)]
    idx_par = [i[0] for i in sorted(enumerate(dates), key=lambda xx: xx[1])]
    sorted_parameters = np.array(parameters)[idx_par]
    sorted_parameter_files = np.array(parameter_files)[idx_par]
    return sorted_parameters, sorted_parameter_files, dates, idx_par


def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in list(d.items()))
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d


def merge_parameters_by_condition(parameters=[{}], **kwargs):
    merge_conditions_by = kwargs.get('merge_conditions_by', [''])
    merge_stimulus_index = kwargs.get('merge_stimulus_index', 0)

    for _p in parameters:
        assert merge_stimulus_index < len(_p['Measurement']['StimuliModule']['Stimulus'])
        _par = _p['Measurement']['StimuliModule']['Stimulus'][merge_stimulus_index]['Parameters']

    _m_items = []
    for i_p, _p in enumerate(parameters):
        _par = _p['Measurement']['StimuliModule']['Stimulus'][merge_stimulus_index]['Parameters']
        _temp = []
        for _cond in merge_conditions_by:
            _temp.append(_par[_cond])
        _m_items.append(_temp)

    (conditions, index, inverse, counts) = np.unique(_m_items,
                                                     axis=0,
                                                     return_counts=True,
                                                     return_inverse=True,
                                                     return_index=True)
    sorted_parameters = parameters[index]
    return sorted_parameters, index, inverse


def anonymize(directory: str = None,
              subjects_original_id: [str] = None,
              subjects_new_codes: [str] = None):
    """
    This function will replace the original subject id in each .extsys file found within the directory and
    subdirectories. The old files will be renamed with their own name + '_old'.
    :param directory: root directory where .extsys files will be searched from.
    :param subjects_original_id: list of existing IDs
    :param subjects_new_codes: list of new codes use to replace the exiting IDs
    :return: None
    """
    assert len(subjects_original_id) == len(subjects_new_codes)
    assert np.unique(subjects_original_id).size == np.unique(subjects_new_codes).size
    files = glob.glob(directory + '**/*.extsys', recursive=True)
    for _file in files:
        zip_file_name = _file

        with zip_f.ZipFile(zip_file_name, 'r') as my_zip:
            files = my_zip.infolist()
            m_file = my_zip.open(files[0].filename, 'r')
            content = m_file.readlines()
            measurement_info = json.loads(content[0].decode("utf-8"))
        _subject = measurement_info['Measurement']['MeasurementModule']['Subject']
        _idx_subject = np.argwhere(np.array(subjects_original_id) == _subject)
        if _idx_subject.size:
            _subject_code = subjects_new_codes[int(_idx_subject.squeeze())]
            measurement_info['Measurement']['MeasurementModule']['Subject'] = _subject_code
            os.rename(zip_file_name, zip_file_name + '_old')
            _file_path, _file_name = path.split(zip_file_name)
            _new_json_file = _file_path + os.sep + files[0].filename
            with open(_new_json_file, "x") as f:
                json.dump(measurement_info, f)
                f.close()
            new_zip_file_name = _file_path + os.path.sep + _file_name.replace(_subject, _subject_code)
            zipObj = zip_f.ZipFile(new_zip_file_name, 'w')
            zipObj.write(filename=_new_json_file, arcname=files[0].filename)
            zipObj.close()
            os.remove(_new_json_file)
        else:
            print('Subject {:} not found in subject codes'.format(_subject))

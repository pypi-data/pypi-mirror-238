# -*- coding: utf-8 -*-
"""
@author: jundurraga-ucl
"""
from peegy.io.elipse_tools import parse_eclipse_data
from peegy.processing.pipe.io import EclipseReader
import os
# Enable below for interactive backend
# import matplotlib
# if 'Qt5Agg' in matplotlib.rcsetup.all_backends:
#    matplotlib.use('Qt5Agg')


_path = os.path.abspath(os.path.dirname(__file__))
file_path = ('/media/jundurraga/90720477720463F61/Measurements/IRU/Measurements/IRU_Soton_Manchester/'
             'Infant aided CAEP Eclipse log data/B001_S01/20160630 10-05-47_B001_S01_Block1_run1_sig1_65.txt')
data1 = parse_eclipse_data(file_name=file_path)
buffer_a = EclipseReader(data_path=file_path, buffer='A')
buffer_b = EclipseReader(data_path=file_path, buffer='B')
buffer_all = EclipseReader(data_path=file_path)
buffer_a.run()
buffer_a.plot()
buffer_b.run()
buffer_b.plot()
buffer_all.run()
buffer_all.plot()

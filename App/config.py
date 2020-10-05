import os
import sys
file_path = os.path.join(os.path.dirname(__file__), '..')
file_dir = os.path.abspath(file_path)
sys.path.insert(0, os.path.abspath(file_path))
data_dir = file_dir + '/Data/'

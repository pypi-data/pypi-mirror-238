"""Nanosurf nhf-file reader implementation for studio data
Copyright (C) Nanosurf AG - All Rights Reserved (2023)
License - MIT"""

import typing
import pathlib 
import numpy as np
import h5py

class NHFDataset():
    def __init__(self, dataset:h5py.Dataset) -> None:
        self.attribute = get_attributes(dataset)
        # type hint is only correct after scale_dataset_to_physical_units() is called at data read time
        self.dataset:np.ndarray = dataset

    def scale_dataset_to_physical_units(self) -> None:
        """ If scaling information are provided in the Dataset, apply them.
        Converts the bit pattern of the saved raw data to the value of the given datatype saved in the attributes
        and scales it with the given calibration values.

        Attention: 
            dataset is read from file in this process, which can last long depending on array size.
            Also dataset is converted from h5py dataset into numpy.ndarray
        """
        try:
            base_calibration_min = self.attribute['base_calibration_min']
            base_calibration_max = self.attribute['base_calibration_max']
            type_min = self.attribute['type_min']
            type_max = self.attribute['type_max']
        except:
            raise ValueError("self.dataset do not contain scaling information")
        
        calibration_factor = (base_calibration_max -
                            base_calibration_min) / (type_max-type_min)
        self.dataset = (self.dataset[:]-type_min) * calibration_factor + base_calibration_min

class NHFSegment():
    def __init__(self, name: str, file_hdl: 'NHFFileReader') -> None:
        self.name = name
        self._file_hdl = file_hdl
        self.channel: dict[str, NHFDataset] = {}
        
    def read_channel(self, ch:typing.Union[str, int]) -> NHFDataset:
        nhf_dataset = None
        if isinstance(ch, str):
            nhf_dataset = self.channel[ch]
        elif isinstance(ch, int):
            nhf_dataset = list(self.channel.values())[ch]
        else:
            raise TypeError("Parameter 'ch' has not supported data type")
        
        assert isinstance(nhf_dataset, NHFDataset), ""
        self._file_hdl.print_verbose(f"Reading channel '{ch}'")
        nhf_dataset.scale_dataset_to_physical_units()
        return nhf_dataset
    
    def channel_name(self, key: int) -> str:
        return list(self.channel.keys())[key]
    
    def channel_count(self) -> int:
        return len(self.channel)
    
class NHFMeasurement(NHFSegment):
    def __init__(self, name: str, file_hdl: 'NHFFileReader') -> None:
        super().__init__(name, file_hdl)
        self.attribute: dict[str] = {}
        self.segment: dict[str, NHFSegment] = {}

    def segment_name(self, key: int) -> str:
        return list(self.segment.keys())[key]
    
    def segment_count(self) -> int:
        return len(self.segment)
    

def default_verbose_output_handler(msg:str):
    print(msg)

def get_attributes(instance: typing.Union[h5py.File,h5py.Group,h5py.Dataset]) -> dict[str]:
    """ Iterates over the attributes of the given instance and puts them to a dictionary.
    If the attribute for the data type is available, data type specific information is stored.

    Parameters
    ----------

        instance: h5py.File | h5py.Group | h5py.Dataset
            Instance within the .nhf file to be read.

    Return
    ------
        attributes_dict: dict
            Contains the attributes of the analyzed instance.

    """
    if not isinstance(instance, (h5py.File, h5py.Group, h5py.Dataset)):
        raise TypeError("Not supported type of instance provided")
    
    attributes_dict: dict = {}
    for attributes_key, attributes_val in instance.attrs.items():
        attributes_dict[attributes_key] = attributes_val
        try:
            element_type = attributes_dict['dataset_element_type']
            attributes_dict['type_min'] = NHFFileReader.dataset_element_type[element_type][0]
            attributes_dict['type_max'] = NHFFileReader.dataset_element_type[element_type][1]
            attributes_dict['type']     = NHFFileReader.dataset_element_type[element_type][2]
        except:
            pass
    return attributes_dict


class NHFFileReader():
    """ Main class to access nhf-files """
    dataset_element_type: dict = {
        0: [-(2.0**31), 2.0**31, 'dt_int32' ],
        1: [-(2.0**8) , 2.0**8 , 'dt_uint8' ],
        2: [-(2.0**16), 2.0**16, 'dt_uint16'],
        3: [-(2.0**32), 2.0**32, 'dt_uint32'],
        4: [-(2.0**64), 2.0**64, 'dt_uint64'],
        5: [-(2.0**15), 2.0**15, 'dt_int16' ],
        6: [-(2.0**64), 2.0**64, 'dt_int64' ],
        7: [       0.0, 0.0    , 'dt_double']
    }
    
    def __init__(self, filename: pathlib.Path=None, verbose=False, verbose_handler=None):
        """ Provide a nhf-file path directly at creating of the class or call later read() with filename
         
        Parameters
        ----------
            verbose: bool
                Set this to True if messages during reading or accessing is desired
            
            verbose_handler: func(msg:str)
                Define an own message handler functions to redirect the messages 
                A None is provided the default message handler print the message to console
        """
        self.measurement: dict[str, NHFMeasurement] = {}
        self.attribute: dict[str, typing.Any] = {}
        self._filename = filename
        self._file_id = None
        self._verbose = verbose
        self._verbose_output_handler = verbose_handler if verbose_handler else default_verbose_output_handler
        if self._filename:
            if self.read() == False:
                raise IOError(f"Could not read structure of file: '{self._filename}'")
            
    def version(self) -> typing.Tuple[int, int]:
        """ returns file version information in form of (major, minor) version number. If not accessible it returns (0,0)"""
        try: 
            major = int(self.attribute['nsf_file_version_major'])
            minor = int(self.attribute['nsf_file_version_minor'])
            return (major, minor)
        except:
            return (0,0)

    def read(self, filename: pathlib.Path=None) -> bool:
        """ Open the nid-file with given path for read access. 
        """
        self._clear_data()
        if filename is not None:
            self._filename = filename
        try:
            self._file_id = h5py.File(self._filename, 'r')
            self.attribute = get_attributes(self._file_id)
            measurement_names = self._get_segment_names(self._file_id)
            if measurement_names:
                self._read_file_structure(measurement_names)
            return True
        except:
            if self._file_id is not None: 
                self._file_id.close()
            self._file_id = None
            self._clear_data()
            self.print_verbose(f"Could not read structure of file: '{self._filename}'")
            return False

    def measurement_name(self, key: int) -> str:
        return list(self.measurement.keys())[key]
    
    def measurement_count(self) -> int:
        return len(self.measurement)
    
    def print_verbose(self, msg:str):
        if self._verbose:
            self._verbose_output_handler(msg)

    # internal functions, not for user access
    
    def _read_file_structure(self, measurement_names:dict[str, str]):        
        self.print_verbose(f"Available measurements in file:\n{measurement_names.values()}")
        for measurement_id in measurement_names:
            measurement_name = measurement_names[measurement_id]
            self.measurement[measurement_name] = NHFMeasurement(measurement_name, self)
            self.measurement[measurement_name].attribute = get_attributes(self._file_id[measurement_id])
            
            segment_names = self._get_segment_names(self._file_id[measurement_id])
            if segment_names:
                self.print_verbose(f"Available segments in {measurement_name}:\n{segment_names.values()}")
                for segment_id in segment_names:
                    segment_name = segment_names[segment_id]
                    segment_data = self._file_id[measurement_id][segment_id]
                    if isinstance(segment_data, h5py.Group):
                        self.measurement[measurement_name].segment[segment_name] = NHFSegment(segment_name, self)
                        dataset_names = self._get_segment_names(segment_data)
                        if dataset_names:
                            self.print_verbose(f"Available datasets in {segment_name}:\n{dataset_names.values()}")
                            for dataset_id in dataset_names:
                                dataset_name = dataset_names[dataset_id]
                                dataset_data = segment_data[dataset_id]
                                self.measurement[measurement_name].segment[segment_name].channel[dataset_name] = NHFDataset(dataset_data)
                    elif isinstance(segment_data, h5py.Dataset):
                        self.measurement[measurement_name].channel[segment_name] = NHFDataset(segment_data)
        
    def _get_segment_names(self, instance: typing.Union[h5py.File,h5py.Group]) -> dict:
        """ Reads the names of the subsegments of the given instance and puts them to a dict, where key - segment id, value- segment name

        Parameters
        ----------

            instance: h5py.File | h5py.Group | h5py.Dataset
                Instance within the .nhf file to be read.

        Return
        ------
            item_names: dict
                Contains the names to the given instance.
                key - segment id, value- segment name

        """
        if isinstance(instance, h5py.File) or isinstance(instance, h5py.Group):
            item_names: dict[str, str] = {}
            for seg_key in instance.keys():
                item_names[seg_key] = instance[seg_key].attrs['name']
            return item_names
        else:
            return None

    def __del__(self):
        if self._file_id:
            self._file_id.close()
        self._file_id = None

    def _clear_data(self):
        self.measurement: dict[str, NHFMeasurement] = {}
        self.attribute: dict[str, typing.Any] = {}

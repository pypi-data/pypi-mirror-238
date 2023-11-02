import pandas as pd
import numpy as np
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Ephemeris:
    epoch_j2000: str
    epoch: datetime
    position: np.array
    speed: np.array
    corr_values: np.array

    def to_dict(self):
        return {
            'epoch': self.epoch,
            'X': self.position[0],
            'Y': self.position[1],
            'Z': self.position[2],
            'VX': self.speed[0],
            'VY': self.speed[1],
            'VZ': self.speed[2],
            'CorrMatrix': self.corr_values
        }

    def __init__(self, data_raw) -> None:
        assert len(data_raw) == 4
        lines = list(map(lambda x: x.strip().split(), data_raw))
        
        self.epoch_j2000 = lines[0][0]
        self.epoch = datetime.strptime(lines[0][0], '%Y%j%H%M%S.%f')

        first_line_nums = np.array(list(map(float, lines[0][1:])))
        self.position = first_line_nums[:3]
        self.speed = first_line_nums[3:6]

        self.corr_values = np.array([list(map(float, line)) for line in lines[1:]])

@dataclass
class EphemerisMetadata:
    ephemeris_start: datetime
    ephemeris_stop: datetime
    step_size: int
    ephemeris_source: str
    reference: str

    def __init__(self, file_meta: list[str]) -> None:
        assert len(file_meta) >= 4
        
        ephemeris_info_str = file_meta[1] \
            .replace('ephemeris_start:', '') \
            .replace('ephemeris_stop:', '') \
            .replace('step_size:', '') \
            .replace('UTC', '') \
            .strip() \
            .split('  ')

        self.ephemeris_start = datetime.strptime(ephemeris_info_str[0], '%Y-%m-%d %H:%M:%S')
        self.ephemeris_stop = datetime.strptime(ephemeris_info_str[1], '%Y-%m-%d %H:%M:%S')
        self.step_size = int(ephemeris_info_str[2])

        self.ephemeris_source = file_meta[2] \
            .replace('ephemeris_source:', '') \
            .strip()
        
        self.reference = file_meta[3].strip()

class EphemerisFile:
    norad_id: int
    sat_name: str
    operational_status: str
    classified_status: str
    file_created: datetime
    meta: EphemerisMetadata
    ephemeris: list[Ephemeris]

    def __init__(self, filename: str) -> None:
        filename_arr = filename.split('_')
        self.norad_id = filename_arr[1]
        self.sat_name = filename_arr[2]
        self.operational_status = filename_arr[3]
        self.classified_status = filename_arr[4]

        with open(filename) as f:
            lines = f.readlines()
        
        assert len(lines) % 4 == 0

        file_created_str = lines[0] \
            .replace('created:', '') \
            .replace('UTC', '') \
            .strip()
        self.date = datetime.strptime(file_created_str, '%Y-%m-%d %H:%M:%S')

        self.meta = EphemerisMetadata(lines[:4])
        self.ephemeris = []
        for i in range(4, len(lines), 4):
            ephemeris = Ephemeris(lines[i:i + 4])
            self.ephemeris.append(ephemeris)

    def to_dataframe(self):
        return pd.DataFrame.from_records(
            [eph.to_dict() for eph in self.ephemeris]
        )
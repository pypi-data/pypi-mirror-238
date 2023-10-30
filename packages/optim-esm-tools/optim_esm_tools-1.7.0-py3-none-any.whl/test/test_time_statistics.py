import os
import tempfile
import unittest

import numpy as np
import xarray as xr

import optim_esm_tools as oet
import optim_esm_tools._test_utils
from optim_esm_tools._test_utils import get_path_for_ds
from optim_esm_tools.analyze import region_finding
from optim_esm_tools.analyze.cmip_handler import read_ds


class Work(unittest.TestCase):
    """Note of caution!

    cache=True can lead to funky behavior!
    """

    @classmethod
    def setUpClass(cls):
        _ = get_path_for_ds('piControl')
        path = get_path_for_ds('ssp585')
        head, tail = os.path.split(path)
        ds = oet.read_ds(head, _file_name=tail)
        cls.data_set = ds

    def test_raises(self):
        with self.assertRaises(ValueError):
            oet.analyze.time_statistics.TimeStatistics(
                self.data_set,
                calculation_kwargs=dict(bad=True),
            )

    def test_get_statistics(self, use_field_for_mask='cell_area'):
        ds = self.data_set.copy()
        x, y = ds[use_field_for_mask].shape
        mask = np.zeros((x, y), dtype=np.bool_)
        # let's mask the upper left corner of the data
        mask[x // 2 :, y // 2 :] = True
        da_mask = xr.DataArray(mask, dims=ds[use_field_for_mask].dims)
        ds_masked = oet.analyze.xarray_tools.mask_to_reduced_dataset(ds, da_mask)
        hist_file_name = os.path.split(get_path_for_ds('piControl', refresh=False))[-1]
        stat = oet.analyze.time_statistics.TimeStatistics(
            ds_masked,
            calculation_kwargs=dict(
                n_breaks=dict(penalty=1),
                max_jump=dict(_file_name=hist_file_name),
                max_jump_yearly=dict(_file_name=hist_file_name),
            ),
        )
        result = stat.calculate_statistics()
        for k, v in result.items():
            print(k, v)
            assert v, f'{k}={v} is not True from {result}'

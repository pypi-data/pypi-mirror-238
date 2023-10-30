import typing as ty
from functools import wraps

import numpy as np
import xarray as xr

from optim_esm_tools.config import config


def _native_date_fmt(time_array: np.ndarray, date: ty.Tuple[int, int, int]):
    """Create date object using the date formatting from the time-array."""

    if isinstance(time_array, xr.DataArray):  # pragma: no cover
        return _native_date_fmt(time_array=time_array.values, date=date)

    if not len(time_array):  # pragma: no cover
        raise ValueError('No values in dataset?')

    # Support cftime.DatetimeJulian, cftime.DatetimeGregorian, cftime.DatetimeNoLeap and similar
    _time_class = time_array[0].__class__
    return _time_class(*date)


def apply_abs(apply=True, add_abs_to_name=True, _disable_kw='apply_abs'):
    """Apply np.max() to output of function (if apply=True) Disable in the
    function kwargs by using the _disable_kw argument.

    Example:
        ```
        @apply_abs(apply=True, add_abs_to_name=False)
        def bla(a=1, **kw):
            print(a, kw)
            return a
        assert bla(-1, apply_abs=True) == 1
        assert bla(-1, apply_abs=False) == -1
        assert bla(1) == 1
        assert bla(1, apply_abs=False) == 1
        ```
    Args:
        apply (bool, optional): apply np.abs. Defaults to True.
        _disable_kw (str, optional): disable with this kw in the function. Defaults to 'apply_abs'.
    """

    def somedec_outer(fn):
        @wraps(fn)
        def somedec_inner(*args, **kwargs):
            response = fn(*args, **kwargs)
            do_abs = kwargs.get(_disable_kw)
            if do_abs or (do_abs is None and apply):
                if add_abs_to_name and isinstance(getattr(response, 'name'), str):
                    response.name = f'Abs. {response.name}'
                return np.abs(response)
            return response  # pragma: no cover

        return somedec_inner

    return somedec_outer


def _remove_any_none_times(da, time_dim, drop=True):
    data_var = da.copy()
    time_null = data_var.isnull().all(dim=set(data_var.dims) - {time_dim})
    if np.all(time_null):
        # If we take a running mean of 10 (the default), and the array is shorter than
        # 10 years we will run into issues here because a the window is longer than the
        # array. Perhaps we should raise higher up.
        raise ValueError(
            f'This array only has NaN values, perhaps array too short ({len(time_null)} < 10)?',
        )  # pragma: no cover

    if np.any(time_null):
        try:
            # For some reason only alt_calc seems to work even if it should be equivalent to the data_var
            # I think there is some fishy indexing going on in pandas <-> dask
            # Maybe worth raising an issue?
            alt_calc = xr.where(~time_null, da, np.nan)
            if drop:
                alt_calc = alt_calc.dropna(time_dim)
            data_var = data_var.load().where(~time_null, drop=drop)
            assert np.all((alt_calc == data_var).values)
        except IndexError as e:  # pragma: no cover
            from optim_esm_tools.config import get_logger

            get_logger().error(e)
            if 'alt_calc' in locals():
                return alt_calc  # type: ignore
            raise e
    return data_var


def mask_xr_ds(data_set, da_mask, masked_dims=None, drop=False):
    # Modify the ds in place - make a copy!
    data_set = data_set.copy()
    if masked_dims is None:
        masked_dims = config['analyze']['lon_lat_dim'].split(',')

    ds_start = data_set.copy()
    func_by_drop = {True: _drop_by_mask, False: _mask_xr_ds}[drop]
    data_set = func_by_drop(data_set, masked_dims, ds_start, da_mask)
    data_set = data_set.assign_attrs(ds_start.attrs)
    return data_set


def reverse_name_mask_coords(da_mask: xr.DataArray, rename_dict=None) -> xr.DataArray:
    rename_dict = rename_dict or {
        v: k for k, v in default_rename_mask_dims_dict().items()
    }
    return rename_mask_coords(da_mask, rename_dict=rename_dict)


def rename_mask_coords(
    da_mask: xr.DataArray,
    rename_dict: ty.Optional[ty.Mapping] = None,
) -> xr.DataArray:
    """Get a boolean DataArray with renamed dimensionality. For some
    applications, we want to prune a dataset of nan values along a given
    lon/lat mask. Removing data along a given mask can greatly reduce file-size
    and speed up data-set handling. This however makes it somewhat cumbersome
    to later re-apply said mask (to other data) since it's shape will be
    inconsistent with other (non-masked) data. To this end, we want to store
    the mask separately in a dataset. To avoid dimension clashes between masked
    data and the masked information, we rename the dimensions of the mask.

    Args:
        da_mask (xr.DataArray): Mask to be renamed.
        rename_dict (ty.Mapping, optional): Mapping from the dims in da_mask to renamed dims.

    Returns:
        xr.DataArray: da_mask with renamed dims.
    """
    rename_dict = rename_dict or default_rename_mask_dims_dict()
    if any(dim not in da_mask.dims for dim in rename_dict.keys()):
        raise KeyError(
            f'Trying to rename {rename_dict}, but this DataArray has {da_mask.dims}',
        )  # pragma: no cover
    mask = da_mask.copy().rename(rename_dict)
    message = (
        'Full global mask with full lat/lon dimensionality in order to be save the masked '
        'time series with all nan values dropped (to conserve disk space)'
    )
    mask.attrs.update(dict(info=message))
    return mask


def mask_to_reduced_dataset(
    data_set: xr.Dataset,
    mask: ty.Union[xr.DataArray, np.ndarray],
    add_global_mask: bool = True,
) -> xr.Dataset:
    """Reduce data_set by dropping all data where mask is False. This greatly
    reduces the size (which is absolutely required for exporting time series
    from global data).

    Args:
        data_set (xr.Dataset): data set to mask by mask
        mask (ty.Union[xr.DataArray, np.ndarray]): boolean array to mask
        add_global_mask (bool, optional): Add global mask with full dimensionality (see
            rename_mask_coords for more info). Defaults to True.

    Raises:
        ValueError: If mask has a wrong shape

    Returns:
        xr.Dataset: Original dataset where mask is True
    """
    if isinstance(mask, xr.DataArray):
        mask = mask.values
    if mask.shape != (expected := data_set['cell_area'].shape):
        raise ValueError(
            f'Inconsistent dimensionality, expected {expected}, got {mask.shape}',
        )  # pragma: no cover

    # Mask twice, "mask" is a np.ndarray, whereas ds.where needs a xr.DataArray.
    # While we could make this more efficient (and only use the second step), the first step
    # does only take ~10 ms
    ds_masked = mask_xr_ds(data_set.copy(), mask)
    bool_mask_data_array = ~ds_masked['cell_area'].isnull()
    ds_masked = mask_xr_ds(ds_masked, bool_mask_data_array, drop=True)
    if add_global_mask:
        ds_masked = add_mask_renamed(ds_masked, bool_mask_data_array)
    return ds_masked


def default_rename_mask_dims_dict():
    return {k: f'{k}_mask' for k in config['analyze']['lon_lat_dim'].split(',')}


def add_mask_renamed(data_set, da_mask, mask_name='global_mask', **kw):
    data_set[mask_name] = rename_mask_coords(da_mask, **kw)
    return data_set


def _drop_by_mask(data_set, masked_dims, ds_start, da_mask):
    """Drop values with masked_dims dimensions.

    Unfortunately, data_set.where(da_mask, drop=True) sometimes leads to
    bad results, for example for time_bnds (time, bnds) being dropped by
    (lon, lat). So we have to do some funny bookkeeping of which data
    vars we can drop with data_set.where.
    """

    dropped = [
        k
        for k, data_array in data_set.data_vars.items()
        if any(dim not in list(data_array.dims) for dim in masked_dims)
    ]
    data_set = data_set.drop_vars(dropped)

    data_set = data_set.where(da_mask.compute(), drop=True)

    # Restore ignored variables and attributes
    for k in dropped:  # pragma: no cover
        data_set[k] = ds_start[k]
    return data_set


def _mask_xr_ds(data_set, masked_dims, ds_start, da_mask):
    """Rebuild data_set for each variable that has all masked_dims."""
    for k, data_array in data_set.data_vars.items():
        if all(dim in list(data_array.dims) for dim in masked_dims):
            lat_lon = config['analyze']['lon_lat_dim'].split(',')[::-1]
            dim_incorrect = tuple(data_array.dims) not in [
                ('time', *lat_lon),
                (*lat_lon,),
            ]
            shape_incorrect = data_array.shape != data_array.T.shape
            if dim_incorrect and shape_incorrect:  # pragma: no cover
                message = f'Please make "{k}" {lat_lon}, now "{data_array.dims}"'
                raise ValueError(message)
            da = data_set[k].where(da_mask, drop=False)
            da = da.assign_attrs(ds_start[k].attrs)
            data_set[k] = da

    return data_set


def extend_indexes(mask_array, coord, cyclic=False, round_at=5):
    """Temporary fix for making extended region masks rounded at 5 deg.

    resolution
    """
    assert len(mask_array) == len(coord), (len(mask_array), len(coord))
    for i, m in enumerate(mask_array):
        idx_left = np.mod(i - 1, len(coord)) if cyclic else max(i - 1, 0)
        idx_right = np.mod(i + 1, len(coord)) if cyclic else min(i + 1, len(coord) - 1)
        goes_left = m != mask_array[idx_left]
        goes_right = m != mask_array[idx_right]
        if goes_left or goes_right:
            prev_i = i
            iterator = (
                range(idx_left, 0, -1) if goes_left else range(idx_right, len(coord))
            )
            for next_i in iterator:
                n = (
                    np.ceil(coord[prev_i] / round_at)
                    if goes_right
                    else np.floor(coord[prev_i] / round_at)
                )

                remain = coord[prev_i] - round_at * n
                next_remain = coord[next_i] - round_at * n
                if abs(remain) <= abs(next_remain):
                    break
                mask_array[next_i] = True
                prev_i = next_i
    return mask_array


def extract_extended_mask(da_mask):
    mask = da_mask.values.copy()
    inx_lat = extend_indexes(np.any(mask, axis=1), da_mask['lat_mask'])
    inx_lon = extend_indexes(np.any(mask, axis=0), da_mask['lon_mask'], cyclic=True)
    a, b = np.meshgrid(inx_lon, inx_lat)
    return a & b


def add_extended_mask(ds):
    values = extract_extended_mask(ds['global_mask'])
    ds['extended_mask'] = xr.DataArray(values, dims=ds['global_mask'].dims)

import operator
import os
import typing as ty
from functools import partial

import numpy as np
import xarray as xr

import optim_esm_tools as oet


class TimeStatistics:
    calculation_kwargs: ty.Optional[ty.Mapping] = None

    def __init__(self, data_set: xr.Dataset, calculation_kwargs=None) -> None:
        # sourcery skip: dict-literal
        self.data_set = data_set
        self.calculation_kwargs = calculation_kwargs or {}
        self.functions = self.default_calculations()
        if any(k not in self.functions for k in self.calculation_kwargs):
            bad = set(self.calculation_kwargs.keys()) - set(self.functions.keys())
            message = f'One or more of {bad} are not used by any function'
            raise ValueError(message)

    def default_calculations(self) -> ty.Mapping:
        return dict(
            max_jump=calculate_max_jump_in_std_history,
            max_jump_yearly=calculate_max_jump_in_std_history_yearly,
            p_dip=calculate_dip_test,
            p_skewness=calculate_skewtest,
            p_symmetry=calculate_symmetry_test,
            n_breaks=calculate_n_breaks,
            n_std_global=n_times_global_std,
        )

    def calculate_statistics(self) -> ty.Dict[str, ty.Optional[float]]:
        """
        For a given dataset calculate the statistical properties of the dataset based on these
        tests:
            1. The max 10-year jump w.r.t. the standard deviation of the piControl (running means).
            2. Same as 1. but based on yearly means.
            3. The p-value of the "dip test" [1]
            4. The p-value of the Skewness test [2]
            5. The p-value of the symmetry test [3]
            6. The number of breaks in the time series [4]
            7. The fraction of the selected regions standard-deviation w.r.t. to the standard
                deviation of the global average standard-deviation. Yearly means

        Citations:
            [1]:
                Hartigan, P. M. (1985). Computation of the Dip Statistic to Test for Unimodality.
                Journal of the Royal Statistical Society. Series C (Applied Statistics), 34(3),
                320-325.
                Code from:
                https://pypi.org/project/diptest/
            [2]:
                R. B. D'Agostino, A. J. Belanger and R. B. D'Agostino Jr., "A suggestion for using
                powerful and informative tests of normality", American Statistician 44, pp.
                316-321, 1990.
                Code from:
                https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skewtest.html
            [3]:
                Mira A (1999) Distribution-free test for symmetry based on Bonferroni's measure.
                J Appl Stat 26(8):959–972. https://doi.org/10.1080/02664769921963
                Code from:
                https://cran.r-project.org/web/packages/symmetry
                Code at:
                https://github.com/JoranAngevaare/rpy_symmetry
            [4]:
                C. Truong, L. Oudre, N. Vayatis. Selective review of offline change point detection
                methods. Signal Processing, 167:107299, 2020.
                Code from:
                https://centre-borelli.github.io/ruptures-docs/

        Returns:
            ty.Dict[ty.Optional[float]]: Mapping of test to result value
        """
        return {
            k: partial(f, **self.calculation_kwargs.get(k, {}))(self.data_set)  # type: ignore
            for k, f in self.functions.items()
        }


def default_thresholds(
    max_jump=None,
    p_dip=None,
    p_symmetry=None,
    n_breaks=None,
    n_std_global=None,
):
    return dict(
        max_jump=(
            operator.ge,
            max_jump or float(oet.config.config['tipping_thresholds']['max_jump']),
        ),
        p_dip=(
            operator.le,
            p_dip or float(oet.config.config['tipping_thresholds']['p_dip']),
        ),
        p_symmetry=(
            operator.le,
            p_symmetry or float(oet.config.config['tipping_thresholds']['p_symmetry']),
        ),
        n_breaks=(
            operator.ge,
            n_breaks or float(oet.config.config['tipping_thresholds']['n_breaks']),
        ),
        n_std_global=(
            operator.ge,
            n_std_global
            or float(oet.config.config['tipping_thresholds']['n_std_global']),
        ),
    )


def _get_ds_global(ds, **read_kw):
    path = ds.attrs['file']
    if os.path.exists(path):
        result = oet.load_glob(path)
        assert result is not None, path
        return result
    else:  # pragma: no cover
        oet.get_logger().warning(f'fallback for {path}')
        return oet.read_ds(os.path.split(path)[0], **read_kw)


def n_times_global_std(
    ds,
    average_over=None,
    criterion='std detrended',
    _ds_global=None,
    **read_kw,
):
    average_over = average_over or oet.config.config['analyze']['lon_lat_dim'].split(
        ',',
    )
    ds_global = _ds_global or _get_ds_global(ds, **read_kw)
    variable = ds.attrs['variable_id']
    crit = _get_tip_criterion(criterion)(variable=variable)
    val = float(crit.calculate(ds.mean(average_over)))
    assert isinstance(
        ds_global,
        xr.Dataset,
    ), f'Got type {type(_ds_global)} expected xr.Dataset. ({read_kw})'
    val_global = float(crit.calculate(ds_global.mean(average_over)))
    return val / val_global if val_global else np.inf


def get_historical_ds(ds, match_to='piControl', _file_name=None, **kw):
    # sourcery skip: inline-immediately-returned-variable
    find = oet.analyze.find_matches.associate_historical
    find_kw = oet.utils.filter_keyword_arguments(kw, find, allow_varkw=False)  # type: ignore
    read_kw = oet.utils.filter_keyword_arguments(kw, oet.read_ds, allow_varkw=False)  # type: ignore
    if _file_name is not None:
        find_kw['search_kw'] = dict(required_file=_file_name)
        read_kw['_file_name'] = _file_name
    try:
        hist_path = oet.analyze.find_matches.associate_historical(
            path=ds.attrs['path'],
            match_to=match_to,
            **find_kw,
        )
    except RuntimeError as e:  # pragma: no cover
        print(e)
        return
    read_kw.setdefault('max_time', None)
    read_kw.setdefault('min_time', None)
    hist_ds = oet.read_ds(hist_path[0], **read_kw)  # type: ignore
    return hist_ds


def get_values_from_data_set(ds, field, add=''):
    if field is None:
        field = ds.attrs['variable_id'] + add
    da = ds[field]
    da = da.mean(set(da.dims) - {'time'})
    return da.values


def calculate_dip_test(ds, field=None, nan_policy='omit'):
    import diptest

    values = get_values_from_data_set(ds, field, add='')
    if nan_policy == 'omit':
        values = values[~np.isnan(values)]
    else:
        raise NotImplementedError(
            'Not sure how to deal with nans other than omit',
        )  # pragma: no cover
    if len(values) < 3:  # pragma: no cover
        # At least 3 samples are needed
        oet.config.get_logger().error('Dataset too short for diptest')
        return None
    _, pval = diptest.diptest(values, boot_pval=False)
    return pval


def calculate_skewtest(ds, field=None, nan_policy='omit'):
    import scipy

    values = get_values_from_data_set(ds, field, add='')
    if sum(~np.isnan(values)) < 8:  # pragma: no cover
        # At least 8 samples are needed
        oet.config.get_logger().error('Dataset too short for skewtest')
        return None
    return scipy.stats.skewtest(values, nan_policy=nan_policy).pvalue


def calculate_symmetry_test(
    ds: xr.Dataset,
    field: ty.Optional[str] = None,
    nan_policy: str = 'omit',
    test_statistic: str = 'MI',
    n_repeat: int = int(oet.config.config['analyze']['n_repeat_sym_test']),
    **kw,
) -> np.float64:
    """The function `calculate_symmetry_test` calculates the symmetry test
    statistic for a given dataset and field using the R package `rpy_symmetry`.

    :param ds: An xarray Dataset containing the data
    :type ds: xr.Dataset
    :param field: The `field` parameter is an optional string that specifies the field or variable from
    the dataset (`ds`) that you want to calculate symmetry test for. If `field` is not provided, the
    function will calculate the symmetry test for all variables in the dataset
    :type field: ty.Optional[str]
    :param nan_policy: The `nan_policy` parameter determines how to handle missing values (NaNs) in the
    data. The default value is 'omit', which means that any NaN values will be excluded from the
    calculation, defaults to omit
    :type nan_policy: str (optional)
    :param test_statistic: The `test_statistic` parameter is a string that specifies the test statistic
    to be used in the symmetry test. It determines how the symmetry of the data will be measured,
    defaults to MI
    :type test_statistic: str (optional)
    :param n_repeat: The parameter `n_repeat` specifies the number of times the symmetry test should be
    repeated. The symmetry test in R does give non-deterministic results. As such repeat a test this
    many times and take the average
    :type n_repeat: int
    :return: The function `calculate_symmetry_test` returns a `np.float64` value.
    """
    import rpy_symmetry as rsym

    values = get_values_from_data_set(ds, field, add='')
    if nan_policy == 'omit':
        values = values[~np.isnan(values)]
    else:  # pragma: no cover
        message = 'Not sure how to deal with nans other than omit'
        raise NotImplementedError(message)
    return np.mean(
        [
            rsym.p_symmetry(values, test_statistic=test_statistic, **kw)
            for _ in range(n_repeat)
        ],
    )


def _get_tip_criterion(short_description):
    for mod in oet.analyze.tipping_criteria.__dict__.values():  # type: ignore
        if not isinstance(mod, type):
            continue
        if not issubclass(mod, oet.analyze.tipping_criteria._Condition):  # type: ignore
            continue
        if getattr(mod, 'short_description', None) == short_description:
            return mod
    raise ValueError(
        f'No tipping criterion associated to {short_description}',
    )  # pragma: no cover


def calculate_max_jump_in_std_history_yearly(ds, **kw):
    kw.setdefault('field', 'max jump yearly')
    kw.setdefault('field_pi_control', 'std detrended yearly')
    return calculate_max_jump_in_std_history(ds, **kw)


def calculate_n_breaks(
    ds,
    penalty=None,
    min_size=None,
    jump=None,
    model=None,
    field=None,
    nan_policy='omit',
    method=None,
):
    import ruptures as rpt

    values = get_values_from_data_set(ds, field=field, add='')

    if nan_policy == 'omit':
        values = values[~np.isnan(values)]
    else:  # pragma: no cover
        message = 'Not sure how to deal with nans other than omit'
        raise NotImplementedError(message)

    penalty = penalty or float(oet.config.config['analyze']['rpt_penalty'])
    min_size = min_size or int(oet.config.config['analyze']['rpt_min_size'])
    jump = jump or int(oet.config.config['analyze']['rpt_jump'])
    model = model or oet.config.config['analyze']['rpt_model']
    method = method or oet.config.config['analyze']['rpt_method']

    if len(values) < min_size:  # pragma: no cover
        return None

    algorithm = getattr(rpt, method)(model=model, min_size=min_size, jump=jump)
    fit = algorithm.fit(values)

    return len(fit.predict(pen=penalty)) - 1


def calculate_max_jump_in_std_history(
    ds,
    field='max jump',
    field_pi_control='std detrended',
    _ds_hist=None,
    mask=None,
    **kw,
):
    ds_hist = _ds_hist or get_historical_ds(ds, **kw)
    if ds_hist is None:
        return None  # pragma: no cover
    _get_mask = oet.analyze.xarray_tools.reverse_name_mask_coords
    mask = _get_mask(ds['global_mask']) if mask is None else mask
    ds_hist_masked = oet.analyze.xarray_tools.mask_xr_ds(ds_hist, mask, drop=True)
    _coord = oet.config.config['analyze']['lon_lat_dim'].split(',')
    variable = ds.attrs['variable_id']
    ds = ds.mean(_coord)
    ds_hist = ds_hist_masked.mean(_coord)
    crit_scen = _get_tip_criterion(field)
    crit_hist = _get_tip_criterion(field_pi_control)
    max_jump = float(crit_scen(variable=variable).calculate(ds))
    std_year = float(crit_hist(variable=variable).calculate(ds_hist))

    return max_jump / std_year if std_year else np.inf

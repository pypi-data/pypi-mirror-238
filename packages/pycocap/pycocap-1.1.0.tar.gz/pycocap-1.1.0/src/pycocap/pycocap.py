# -*- coding: utf-8 -*-

import warnings
from functools import reduce
from datetime import date
from typing import Any, List, Optional, Union
import requests
import numpy as np
import pandas as pd


API_URL = 'https://web.app.ufz.de/cocap/'


def cut_at_dates(
    df: pd.DataFrame,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> pd.DataFrame:
    """Cut a DataFrame at given dates."""
    if (start_date is not None or end_date is not None) and start_date == end_date:
        raise ValueError('start_date and end_date cannot be equal')
    mask = None
    if start_date is not None:
        start_date = pd.to_datetime(start_date)
        mask = df['date'] >= start_date
    if end_date is not None:
        end_date = pd.to_datetime(end_date)
        if start_date is not None:
            mask &= df['date'] < end_date
        else:
            mask = df['date'] < end_date
    if mask is not None:
        df = df[mask]
    return df

def regularize_timeseries(
    df: pd.DataFrame,
    fill_value: Optional[Union[float, str]] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> pd.DataFrame:
    """Fill missing data with NaNs, or fill_value to get a regular timeseries"""
    # TODO can all this be done cleaner?!
    sd = start_date if start_date is not None else df['date'].iloc[0]
    ed = end_date if end_date is not None else df['date'].iloc[-1]
    idx = pd.date_range(sd, ed, freq='D', inclusive='left')
    df = df.set_index('date')
    df = df.reindex(idx)
    df['date'] = df.index
    df = df.reset_index(drop=True)
    # put 'date' at position 0 again
    cols = df.columns.tolist()
    cols.insert(0, cols.pop())
    df = df[cols]
    if fill_value is not None:
        if fill_value == 'interpolate':
            # interpolate does not like dates...
            df.loc[:, df.columns!='date'] = (
                df.loc[:, df.columns!='date'].interpolate()
            )
        else:
            df = df.fillna(fill_value)
    return df

def _convert_json_to_df(
    json,
    rename_cols: Optional[dict] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    date_format: Optional[str] = None,
) -> pd.DataFrame:
    df = pd.DataFrame(json)
    if rename_cols is not None:
        df = df.rename(columns=rename_cols)
    try:
        df['date'] = pd.to_datetime(df['date'], format=date_format)
    except KeyError:
        ...
    df = cut_at_dates(df, start_date, end_date)
    return df


def reports(
    country: str,
    report_type: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    params: Optional[dict] = None,
    fill_value: Union[float, str] = np.nan,
    return_population: bool = False,
) -> Any:
    """Get cases or deaths timeseries as a DataFrame from the db.

    Parameters
    ----------
    country
        The country name for which to get the reports
    report_type
        Can either be "cases" or "death"
    start_date : optional
        The date at which the timeseries will start
    end_date : optional
        The date at which the timeseries will end
    fill_value : optional
        decide what to do with missing values, can be

        * np.nan: fill with NaNs, to optain regular timeseries
        * a number: fill with constant value, e.g. 0
        * 'drop': drop missing values
        * 'interpolate' : linear interpolation over gaps

    return_population : bool, optional
        Convenience flag: return tuple of (DataFrame, N)

    Returns
    -------
    df
        A DataFrame consisting of the columns "date" and `report_type`
    N, optional
        The population of `country`
    """
    response = requests.get(API_URL + f'{country}/{report_type}', params=params)
    if response.status_code == 200:
        r_json = response.json()
        if len(r_json['report']) == 0:
            warnings.warn(
                f'Empty response for country {country} and report type '
                f'{report_type}, with params {params}'
            )
            return None
        N = int(r_json['population'])
        df = _convert_json_to_df(
            r_json['report'],
            {'count': report_type},
            start_date,
            end_date,
        )
        if fill_value != 'drop':
            df = regularize_timeseries(
                df,
                fill_value,
                start_date,
                end_date,
            )
    else:
        print(f'Response code: {response.status_code}')
        df = None
        N = None
    r = df
    if return_population:
        r = (df, N)
    return r

def cases(
    country: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    params: Optional[dict] = None,
    fill_value: Union[float, str] = np.nan,
    return_population: bool = False,
) -> Any :
    """Get cases timeseries as a DataFrame from the db.

    Parameters
    ----------
    country
        The country name for which to get the reports
    start_date : optional
        The date at which the timeseries will start
    end_date : optional
        The date at which the timeseries will end
    params : optional
        optional query parameters

        * "source_name"

    fill_value : optional
        decide what to do with missing values, can be

        * np.nan: fill with NaNs, to optain regular timeseries
        * a number: fill with constant value, e.g. 0
        * 'drop': drop missing values
        * 'interpolate' : linear interpolation over gaps

    return_population : bool, optional
        Convenience flag: return tuple of (DataFrame, N)

    Returns
    -------
    df
        A DataFrame consisting of the columns "date" and "cases"
    N, optional
        The population of `country`
    """
    return reports(
        country,
        'cases',
        start_date,
        end_date,
        params,
        fill_value,
        return_population,
    )

def deaths(
    country: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    params: Optional[dict] = None,
    fill_value: Union[float, str] = np.nan,
    return_population: bool = False,
) -> Any:
    """Get death timeseries as a DataFrame from the db.

    Parameters
    ----------
    country
        The country name for which to get the reports
    start_date : optional
        The date at which the timeseries will start
    end_date : optional
        The date at which the timeseries will end
    params : optional
        optional query parameters

        * "source_name"

    fill_value : optional
        decide what to do with missing values, can be

        * np.nan: fill with NaNs, to optain regular timeseries
        * a number: fill with constant value, e.g. 0
        * 'drop': drop missing values
        * 'interpolate' : linear interpolation over gaps

    return_population : bool, optional
        Convenience flag: return tuple of (DataFrame, N)

    Returns
    -------
    df
        A DataFrame consisting of the columns "date" and "death"
    N, optional
        The population of `country`
    """
    return reports(
        country,
        'death',
        start_date,
        end_date,
        params,
        fill_value,
        return_population,
    )

def _report_nuts3(
    country: str,
    county_id: int,
    report_type: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    params: Optional[dict] = None,
) -> Optional[pd.DataFrame]:
    """Get cummulative reports as a DataFrame from for a county.

    Parameters
    ----------
    country
        The country name for which to get the reports, has to be "Germany"
    county_id
        The ID of the county of interest
    report_type
        Can either be "cases", "death", or "recovered"
    start_date : optional
        The date at which the timeseries will start
    end_date : optional
        The date at which the timeseries will end

    Returns
    -------
    df
        A DataFrame consisting of the columns "date", `report_type`, ...
    """
    if country != 'Germany':
        raise ValueError("Local data only available for country = 'Germany'")
    response = requests.get(
        API_URL + f'nuts3/{country}/{county_id}/{report_type}', params=params
    )
    if response.status_code == 200:
        r_json = response.json()
        if len(r_json['report']) == 0:
            warnings.warn(
                f'Empty response for {country=}, {county_id=}, '
                f' and {report_type=}, with {params=}'
            )
            df = None
        df = _convert_json_to_df(
            r_json['report'],
            {'count': report_type},
            start_date,
            end_date,
        )
    else:
        print(f'Response code: {response.status_code}')
        df = None
    return df

def reports_nuts3(
    country: str,
    county_id: Union[List[int], int],
    report_types: Optional[Union[List[str], str]] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    params: Optional[dict] = None,
) -> Optional[pd.DataFrame]:
    """Get multiple cummulative reports as a DataFrame for a county.

    Parameters
    ----------
    country
        The country name for which to get the reports, has to be "Germany"
    county_id
        The ID or IDs of the county or counties of interest
    report_types : optional
        the report types, if `none`, returns all. can be

        * none (default)
        * "cases"
        * "death"
        * "recovered"
    start_date : optional
        The date at which the timeseries will start
    end_date : optional
        The date at which the timeseries will end

    Returns
    -------
    df
        A DataFrame consisting of the columns "date", `report_types`, ...
    """
    _county_id = county_id
    if not isinstance(_county_id, list):
        _county_id = [_county_id]
    # values checks for Germany only
    # TODO this could be more fine grained by checking if values are all in
    # defaultDict dict
    if country == 'Germany':
        if min(_county_id) < 1001 or max(_county_id) > 16077:
            raise ValueError('German NUTS3 county IDs are > 1000 and <= 16077')
    _report_types = report_types
    if not isinstance(_report_types, list):
        _report_types = [_report_types]
    if report_types is None:
        _report_types = [
            'cases',
            'deaths',
            'recovered',
        ]

    dfs = []
    for c_id in _county_id:
        dfs_tmp = [
            _report_nuts3(
                country,
                c_id,
                report_type,  # pyright: ignore
                start_date,
                end_date,
                params,
                ) for report_type in _report_types  # pyright: ignore
        ]
        try:
            dfs.append(reduce(lambda df1, df2: pd.merge(df1, df2, on='date'), dfs_tmp))  # pyright: ignore
        except KeyError:
            ...
        if len(_county_id) > 1:
            dfs[-1]['county_id'] = c_id
    dfs = pd.concat(dfs)
    return dfs

def _report_nuts1(
    country: str,
    region_id: int,
    report_type: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    params: Optional[dict] = None,
) -> Optional[pd.DataFrame]:
    """Get cummulative reports as a DataFrame from for a county.

    Parameters
    ----------
    country
        The country name for which to get the reports, has to be "Germany"
    region_id
        The ID of the region (Federal State in DE) of interest
    report_type
        Can either be "cases", "death", or "recovered"
    start_date : optional
        The date at which the timeseries will start
    end_date : optional
        The date at which the timeseries will end

    Returns
    -------
    df
        A DataFrame consisting of the columns "date", `report_type`, ...
    """
    if country != 'Germany':
        raise ValueError("Subnational data only available for country = 'Germany'")
    response = requests.get(
        API_URL + f'nuts1/{country}/{region_id}/{report_type}', params=params
    )
    if response.status_code == 200:
        r_json = response.json()
        if len(r_json['report']) == 0:
            warnings.warn('Empty response')
            df = None
        df = _convert_json_to_df(
            r_json['report'],
            {'count': report_type},
            start_date,
            end_date,
        )
    else:
        print(f'Response code: {response.status_code}')
        df = None
    return df

def reports_nuts1(
    country: str,
    region_id: Union[List[int], int],
    report_types: Optional[Union[List[str], str]] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    params: Optional[dict] = None,
) -> Optional[pd.DataFrame]:
    """Get multiple cummulative reports as a DataFrame for a region.

    Parameters
    ----------
    country
        The country name for which to get the reports, has to be "Germany"
    region_id
        The ID or IDs of the region (state in DE) or counties of interest
    report_types : optional
        the report types, if `none`, returns all. can be

        * none (default)
        * "cases"
        * "death"
        * "recovered"
    start_date : optional
        The date at which the timeseries will start
    end_date : optional
        The date at which the timeseries will end

    Returns
    -------
    df
        A DataFrame consisting of the columns "date", `report_types`, ...
    """
    if country != 'Germany':
        raise ValueError("Subnational data only available for country = 'Germany'")
    _region_id = region_id
    if not isinstance(_region_id, list):
        _region_id = [_region_id]
    # values checks for Germany only
    if country == 'Germany':
        if min(_region_id) < 1 or max(_region_id) > 16:
            raise ValueError('German NUTS1 region IDs are > 0 and <= 16')
    _report_types = report_types
    if not isinstance(_report_types, list):
        _report_types = [_report_types]
    if report_types is None:
        _report_types = [
            'cases',
            'deaths',
            'recovered',
        ]

    dfs = []
    for r_id in _region_id:
        dfs_tmp = [
            _report_nuts1(
                country,
                r_id,
                report_type,  # pyright: ignore
                start_date,
                end_date,
                params,
                ) for report_type in _report_types  # pyright: ignore
        ]
        dfs.append(reduce(lambda df1, df2: pd.merge(df1, df2, on='date'), dfs_tmp))  # pyright: ignore
        if len(_region_id) > 1:
            dfs[-1]['region_id'] = r_id
    dfs = pd.concat(dfs)
    return dfs

def timeseries(
    country: str,
    report_type: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    params: Optional[dict] = None,
    fill_value: Union[float, str] = np.nan,
) -> Optional[pd.DataFrame]:
    """Get a timeseries as a DataFrame from the db.

    Parameters
    ----------
    country
        The country name for which to get the timeseries
    report_type
        Can be

        * "hospital_daily_occupation"
        * "hospital_weekly_admissions"
        * "icu_daily_occupation"
        * "icu_weekly_admission"
        * "R"
        * "vaccinations_daily"
        * "vaccinations_people"
        * "vaccinations_people_fully"
        * "vaccinations_total"
        * "vaccinations_total_booster"

    start_date : optional
        The date at which the timeseries will start
    end_date : optional
        The date at which the timeseries will end
    params : optional
        optional query parameters

        * "source_name"

    fill_value : optional
        decide what to do with missing values, can be

        * np.nan: fill with NaNs, to optain regular timeseries
        * a number: fill with constant value, e.g. 0
        * 'drop': drop missing values
        * 'interpolate' : linear interpolation over gaps

    Returns
    -------
    df
        A DataFrame consisting of the columns "date" and the given timeseries
    """
    valid_types = (
        'hospital_daily_occupation',
        'hospital_weekly_admissions',
        'icu_daily_occupation',
        'icu_weekly_admissions',
        'R',
        'vaccinations_daily',
        'vaccinations_people',
        'vaccinations_peoplefully',
        'vaccinations_total',
        'vaccinations_total_booster',
    )
    if report_type is not None and report_type not in valid_types:
        raise ValueError(f'report_type can only be one of {valid_types}')
    response = requests.get(API_URL + f'{country}/timeseries/{report_type}', params=params)
    req_name = 'timeseries'
    if response.status_code == 200:
        r_json = response.json()
        if len(r_json[req_name]) == 0:
            warnings.warn('Empty response')
            return None
        df = _convert_json_to_df(
            r_json[req_name],
            {'value': report_type},
            start_date,
            end_date,
        )
        if fill_value != 'drop':
            df = regularize_timeseries(
                df,
                fill_value,
                start_date,
                end_date,
            )
    else:
        print(f'Response code: {response.status_code}')
        df = None
    return df

def nfc(
    country: str,
    nfc_type: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    params: Optional[dict] = None,
) -> Optional[pd.DataFrame]:
    """Get National Framework Conditions as a DataFrame from db.

    Parameters
    ----------
    country
        The country name for which to get the timeseries
    nfc_type
        the type of data

        * "age"
        * "air_pollution_pm2.5"
        * "gender_equality"
        * "health_expenditure"
        * "immunization_dpt"
        * "life_expectancy_at_birth"
        * "literacy_rate_adult"
        * "malaria"
        * "obesity"
        * "open_defaction"
        * "population"
        * "population_density"
        * "rtd_expenditure"
        * "social_insurance_coverage"
        * "tobacco_use"
        * "tourist_departures"
        * "urban_population"

    start_date : optional
        The date at which the timeseries will start
    end_date : optional
        The date at which the timeseries will end
    params : optional
        optional query parameters

        * "source_name"

    Returns
    -------
    df
        A DataFrame consisting of the columns "date" and `nfc_type`
    """
    response = requests.get(API_URL + f'{country}/nfc/{nfc_type}', params=params)
    if response.status_code == 200:
        r_json = response.json()
        if len(r_json['nfc']) == 0:
            warnings.warn('Empty response')
            return None
        df = _convert_json_to_df(
            r_json['nfc'],
            {'year': 'date', 'value': nfc_type},
            start_date,
            end_date,
            date_format='%Y',
        )
        # TODO implement regularization for yearly timesteps
        # if fill_value != 'drop':
            # df = regularize_timeseries(
                # df,
                # fill_value,
                # start_date,
                # end_date,
                # frequency='Y',
            # )
    else:
        print(f'Response code: {response.status_code}')
        df = None
    return df

def npi(
    country: str,
    npi_type: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    params: Optional[dict] = None,
    fill_value: Union[float, str] = np.nan,
) -> Optional[pd.DataFrame]:
    """Get NPI timeseries as a DataFrame from the db.

    Parameters
    ----------
    country
        The country name for which to get the reports
    npi_type
        choose the npi type from

        * "stringency"
        * "school closing"
        * "workplace closing"
        * "cancel public events"
        * "restrictions on gatherings"
        * "close public transport"
        * "stay at home requirements"
        * "restrictions on internal movement"
        * "international travel controls"
        * "income support"
        * "dept relief"
        * "public information campaigns"
        * "testing policy"
        * "contact tracing"
        * "facial coverings"
        * "vaccination policy"
        * "protection of elderly people"

    start_date : optional
        The date at which the timeseries will start
    end_date : optional
        The date at which the timeseries will end
    params : optional
        optional query parameters

        * "source_name"

    fill_value : optional
        decide what to do with missing values, can be

        * np.nan: fill with NaNs, to optain regular timeseries
        * a number: fill with constant value, e.g. 0
        * 'drop': drop missing values
        * 'interpolate' : linear interpolation over gaps

    Returns
    -------
    df
        A DataFrame consisting of the columns "date" and `npi_type`
    """
    response = requests.get(API_URL + f'{country}/npi/{npi_type}', params=params)
    if response.status_code == 200:
        r_json = response.json()
        if len(r_json['policies']) == 0:
            warnings.warn('Empty response')
            return None
        df = _convert_json_to_df(
            r_json['policies'],
            {'value': npi_type, 'flag': npi_type+'_flag'},
            start_date,
            end_date,
        )
        if fill_value != 'drop':
            df = regularize_timeseries(
                df,
                fill_value,
                start_date,
                end_date,
            )
    else:
        print(f'Response code: {response.status_code}')
        df = None
    return df

def npis(
    country: str,
    npi_types: Optional[Union[List, str]] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    params: Optional[dict] = None,
    fill_value: Union[float, str] = np.nan,
) -> Optional[pd.DataFrame]:
    """Get multiple NPI timeseries as a DataFrame from the db.

    Parameters
    ----------
    country
        The country name for which to get the reports
    npi_types : optional
        the npi types, if `None`, returns all. Can be

        * None (default)
        * "stringency"
        * "school closing"
        * "workplace closing"
        * "cancel public events"
        * "restrictions on gatherings"
        * "close public transport"
        * "stay at home requirements"
        * "restrictions on internal movement"
        * "international travel controls"
        * "income support"
        * "debt relief"
        * "public information campaigns"
        * "testing policy"
        * "contact tracing"
        * "facial coverings"
        * "vaccination policy"
        * "protection of elderly people"

    start_date : optional
        The date at which the timeseries will start
    end_date : optional
        The date at which the timeseries will end
    params : optional
        optional query parameters

        * "source_name"

    fill_value : optional
        decide what to do with missing values, can be

        * np.nan: fill with NaNs, to optain regular timeseries
        * a number: fill with constant value, e.g. 0
        * 'drop': drop missing values
        * 'interpolate' : linear interpolation over gaps

    Returns
    -------
    df
        A DataFrame consisting of the columns "date" and `npi_type`
    """
    _npi_types = npi_types
    if npi_types is None:
        _npi_types = [
            'stringency',
            'school closing',
            'workplace closing',
            'cancel public events',
            'restrictions on gatherings',
            'close public transport',
            'stay at home requirements',
            'restrictions on internal movement',
            'international travel controls',
            'income support',
            'debt relief',
            'public information campaigns',
            'testing policy',
            'contact tracing',
            'facial coverings',
            'vaccination policy',
            'protection of elderly people',
        ]

    dfs = [
        npi(
            country,
            npi_type,
            start_date,
            end_date,
            params,
            fill_value,
            ) for npi_type in _npi_types  # pyright: ignore
    ]
    dfs = reduce(lambda df1, df2: pd.merge(df1, df2, on='date'), dfs)
    return dfs

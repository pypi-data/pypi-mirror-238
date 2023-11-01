# Copyright 2016 Enzo Busseti, Stephen Boyd, Steven Diamond, BlackRock Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib

import numpy as np
import pandas as pd

TRUNCATE_REPR_HASH = 10  # probability of conflict is 1e-16


__all__ = ['periods_per_year_from_datetime_index', 'resample_returns',
           'flatten_heterogeneous_list', 'repr_numpy_pandas',
           'average_periods_per_year']


def average_periods_per_year(num_periods, first_time, last_time):
    """Average periods per year, rounded to int."""
    return int(np.round(num_periods / ((last_time - first_time) /
                                    pd.Timedelta('365.24d'))))

def periods_per_year_from_datetime_index(idx):
    """Average periods per year of a datetime index, rounded to int."""
    return average_periods_per_year(
        num_periods=len(idx), first_time=idx[0], last_time=idx[-1])


def resample_returns(returns, periods):
    """Resample returns expressed over number of periods to single period."""
    return np.exp(np.log(1 + returns) / periods) - 1


def flatten_heterogeneous_list(li):
    """[1, 2, 3, [4, 5]] -> [1, 2, 3, 4, 5]."""
    return sum(([el] if not hasattr(el, '__iter__')
                else el for el in li), [])


def hash_(array_like):
    """Hash np.array."""
    return hashlib.sha256(
        bytes(str(list(array_like.flatten())), 'utf-8')).hexdigest()[
            :TRUNCATE_REPR_HASH]


def repr_numpy_pandas(nppd):
    """Unique repr of a numpy or pandas object."""
    if isinstance(nppd, np.ndarray):
        return f'np.array(hash={hash_(nppd)})'
    # if isinstance(nppd, np.matrix):
    #     return f'np.array(hash={hash_(nppd.A)})'
    if isinstance(nppd, pd.Series):
        return f'pd.Series(hash_values={hash_(nppd.values)}, '\
            + f'hash_index={hash_(nppd.index.to_numpy())})'
    if isinstance(nppd, pd.DataFrame):
        return f'pd.DataFrame(hash_values={hash_(nppd.values)}, '\
            + f'hash_index={hash_(nppd.index.to_numpy())}, '\
            + f'hash_columns={hash_(nppd.columns.to_numpy())})'
    raise NotImplementedError('The provided data type is not supported.')

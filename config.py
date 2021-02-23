#
# Copyright (c) 2021 Be The Match.
#
# This file is part of DPB1 Prediction
# (see https://github.com/nmdp-bioinformatics/dpb1-prediction).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
class Config(object):
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False
    IMPUTATION_URL = "https://dev1/ImputeService"
    HAP_FREQS_DIR = "data/frequencies"

class DevConfig(Config):
    DEBUG = True
    IMPUTATION_URL = "https://dev1/ImputeService"


class QAConfig(Config):
    IMPUTATION_URL = "https://qa1/ImputeService"


class PreProdConfig(Config):
    IMPUTATION_URL = "https://preprod1/ImputeService"


class ProdConfig(Config):
    IMPUTATION_URL = "https://prod/ImputeService"


class LocalConfig(Config):
    DEBUG = True
    TESTING = True
    HAP_FREQS_DIR = "tests/data/frequencies"

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
import requests
import json
import pandas as pd

class TCE_map(object):

    def __init__(self,
            path='data/tce_assignments.txt', ard=None):
        self.path = path
        self.tce_assignments = self._get_tce_assignments()
        print(self.tce_assignments)
        self.ard = ard

    def _get_tce_assignments(self):
        """
        Obtains TCE assignments from a hard-coded from IMGT.
        :return: Dictionary of alleles to TCE groups (3, 2, 1, 0).
        :rtype: Dict[str, str]
        """
        with open(self.path, 'r') as f:
            tce_map = json.loads(f.readline())

        allele_header = 'Allele'
        tce_header = 'V2_Assignment'
        url = 'https://raw.githubusercontent.com/ANHIG/IMGTHLA/Latest/tce/dpb_tce.csv'
        tce_df = pd.read_csv(url, comment='#')
        tce_df.replace({'\$' : '', 'a' : ''}, regex=True, inplace=True)
        tce_df = tce_df[[allele_header, tce_header]]
        tce_df = tce_df[~tce_df[tce_header].isnull()]
        tce_df.set_index(allele_header, inplace=True)
        tce_map_updated = tce_df.to_dict()[tce_header]
        tce_map.update(tce_map_updated)
        return tce_map
    
    def assign_tce(self, dpb1_allele):
        if dpb1_allele not in self.tce_assignments:
            if self.ard:
                dpb1_allele = self.ard.redux_gl(dpb1_allele, 'lgx')
            else:
                raise InvalidTceError(dpb1_allele, 'The TCE group for this DPB1 allele is unknown. '
                                                   'Try enabling pyARD to perform reduction to the antigen-recognition domain level.')
        if dpb1_allele not in self.tce_assignments:
            # print("Check the %s allele. The TCE group is unable to be determined." % dpb1_allele)
            return '0'
        return str(self.tce_assignments[dpb1_allele])

class TCE_SLUG(object):

    def __init__(self, tce_name, dpb1_slug_list=None, probability=None):
        self.name = tce_name
        self.dpb1_slugs = dpb1_slug_list
        self.min_tce = self._calculate_min_tce()
        self.probability = probability or self._calculate_probability()
    
    def _calculate_probability(self):
        if self.dpb1_slugs:
            return sum([dpb1_slug.probability for dpb1_slug in self.dpb1_slugs if dpb1_slug.probability])
        else:
            return None
    
    def _calculate_min_tce(self):
        """
        Obtains the numerically minimum TCE group between the TCE pairs. However,
        0s are disregarded, unless they're the only option.
        """
        tces = [tce for tce in self.name.split('+') if tce != '0']
        if not tces:
            return '0'
        return min(tces)

    def __repr__(self):
        return str({'tce_groups' : str(self.name),
                'probability' : self.probability and str(round(self.probability, 3))})

    def serialize(self):
        serialized = {}
        serialized['tce_groups'] = self.name
        if self.probability != None:
            serialized['probability'] = float(self.probability)
        return serialized


class TCE(object):
    def __init__(self, min_tce : int):
        self.name = min_tce
        self.probability = None
    
    def add_probability(self, probability : float):
        if probability:
            if not self.probability:
                self.probability = 0
            self.probability += probability
    
    def __repr__(self):
        return str({'tce_group' : str(self.name),
                    'probability' : self.probability and str(round(self.probability, 3))})

    def serialize(self):
        serialized = {'tce_group' : self.name}
        if self.probability != None:
            serialized['probability'] = float(self.probability)
        return serialized

class InvalidTceError(Exception):

    def __init__(self, allele, message):
        self.allele = allele
        self.message = message
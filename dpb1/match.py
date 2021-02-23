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
from sigfig import round
import numpy as np

class Matches(object):
    """
    Takes in recipient and donor subjects and aggregates
    all the possible matches on a DPB1 allele and TCE group level.
    """
    def __init__(self, subject_recip=None, subject_donor=None):
        """
        :param Subject subject_recip: Subject object representing the recipient.
                                      Needs to contain TCE groups.
        :param Subject subject_donor: Subject object representing the donor.
                                      Needs to contain TCE groups.
        """
        self.subject_recip = subject_recip
        self.subject_donor = subject_donor
        self.match_grades = None

    def get_tce_match_grades(self):
        """
        Iteratives over TCE genotype pairs (between recipient and donor) to
        create MatchGrades (nonpermissive [graft-versus-host], nonpermissive [host-versus-graft],
        permissive). 
        :return: List of MatchGrade objects
        """
        match_grades = {}
        for tce_geno_recip in self.subject_recip.tce_genotypes:
            for tce_geno_donor in self.subject_donor.tce_genotypes:
                match_grade = MatchGrade([tce_geno_recip, tce_geno_donor])
                if match_grade.name not in match_grades:
                    match_grades[match_grade.name] = match_grade
                else:
                    if match_grade.probability:
                        match_grades[match_grade.name].probability = match_grades[match_grade.name].probability + match_grade.probability
        match_grades = list(match_grades.values())
        self._order_by_probability(match_grades)

        # If only one MatchGrade was calculated and a DPB1 typing was provided but
        # without any successful predictions, then assign it with a probability of 1
        if len(match_grades) == 1 and match_grades[0].probability == 0:
            match_grades[0].probability = 1

        self.match_grades = match_grades
        return self.match_grades

    def _order_by_probability(self, match_grades):
        """
        Orders the match grades by probability, descending.
        :return: None
        """
        match_grades.sort(key=lambda match_grade: match_grade.probability, reverse=True)

    def __repr__(self):
        return str(self.match_grades)


class MatchGrade(object):

    def __init__(self, tce_slugs, name=None, probability=None):
        self.tce_slugs = tce_slugs
        self.name = name or self._calculate_match_grade()
        self.probability = probability and probability or self._calculate_probability()
        
    def _calculate_match_grade(self):
        """
        Calculates the TCE match grade between two TCE_SLUGs.
        :return: Match grade name string
        """
        tce_slug_recip, tce_slug_donor = self.tce_slugs
        if (tce_slug_recip.min_tce == tce_slug_donor.min_tce):
            return 'PERMISSIVE'
        elif (tce_slug_recip.min_tce < tce_slug_donor.min_tce):
            return 'GVH_NONPERMISSIVE'
        else:
            return 'HVG_NONPERMISSIVE'

    def _calculate_probability(self):
        """
        Calculates the probability of the match grade by multiplying
        the product of the TCE_SLUG probabilities
        :return: probability float calculation
        """
        return float(np.prod([tce_slug.probability or 0
                        for tce_slug in self.tce_slugs]))

    def __repr__(self):
        return str({'name' : self.name,
                    'probability' : self.probability and round(self.probability, 3)})

    def serialize(self):
        return {'category' : self.name,
                'probability' : self.probability}

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
import xml.etree.ElementTree as ET
from .allele import Allele
from .haplotype import Haplotype
from .genotype import Genotype
from config import Config

# For unverified requests warning suppression
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Imputation(object):
    """
    Represents a group of possible Genotypes for an individual.

    Ultimately, each Genotype should have a pair of haplotypes,
    populations, and frequencies.

    :param genotypes: List of Genotype objects
    """

    def __init__(self, glstring=None, population=None, locus_order=['A', 'C', 'B', 'DRB1', 'DQB1'],
                 genotypes=[], imputation=None, imputation_url=None):
        self.glstring = glstring
        self.population = population
        self.locus_order = locus_order
        self.genotypes = genotypes
        self.ref_freq_path = None
        self.imputation_url = imputation_url or Config().IMPUTATION_URL
        if imputation:
            self.set_imputation(imputation)

    def set_imputation(self, imputation):
        genotypes = []
        for hap_pop_freq in imputation:
            hpf_pair = []
            for index in ['1', '2']:
                hpf_pair.append(Haplotype(name=hap_pop_freq['haplotype' + index],
                                          population=hap_pop_freq['population' + index],
                                          frequency=float(hap_pop_freq['frequency' + index])))
            genotypes.append(Genotype(hpf_pair))
        self.genotypes = genotypes

    def impute(self):
        raise InvalidImputationError(self.glstring, "6locus Imputation call Unimplemented")

    def __repr__(self):
        return str(self.genotypes)


class InvalidImputationError(Exception):

    def __init__(self, imputation, message):
        self.imputation = imputation
        self.message = message

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
import re
from .allele import Allele
import dpb1.haplotype
from sigfig import round
import requests
import json
import operator
import toolz
from mpmath import mpf

class DPB1s(object):
    """
    Represents a genotype list of possible DPB1 alleles
    """
    def __init__(self, glstring, ard=None, tce_map=None):
        self.glstring = glstring
        self.ard = ard
        self.tce_map = tce_map
        self.potential_SLGs = self._get_potential_DPB1_SLGs(glstring)
    
    def _get_potential_DPB1_SLGs(self, glstring):
        """
        Organizes potential DPB1 SLGs through lists.
        Outer list (3) - items represent possible SLGs 
        List (2) - items are up to two lists of possible alleles

        Ex: x/y/z+a/b/c|x+a -> [[[x,y,z],[a,b,c]], [[x],[a]]]
        """
        potential_dpb1_SLGs = []
        for dpb1_SLGs in glstring.split('|'):
            haplotypes = dpb1_SLGs.split('+')
            if len(haplotypes) == 1:
                haplotypes = haplotypes * 2
            if len(haplotypes) > 2:
                raise InvalidDpb1Error("There are more than two DPB1 allotypes. "
                                       "Check the number of successive '+' symbols.")
            dpb1_haplos = []
            for haplotype in haplotypes:
                dpb1_haplo = dpb1.haplotype.Haplotype()
                alleles = haplotype.split('/')
                if len(alleles) == 1:
                    alleles = DPB1(alleles[0]).get_potential_DPB1s(self.ard)
                dpb1_haplo.dpb1_alleles = alleles
                dpb1_haplos.append(dpb1_haplo)
            potential_dpb1_SLGs += [sorted([dpb1_1, dpb1_2]) 
                                        for dpb1_1 in dpb1_haplos[0].dpb1_alleles
                                        for dpb1_2 in dpb1_haplos[1].dpb1_alleles]

        potential_dpb1_SLGs = [DPB1_SLUG(potential_dpb1_SLG, ard=self.ard, frequency=None) 
                                for potential_dpb1_SLG in potential_dpb1_SLGs]
        # Remove duplicate lists
        potential_dpb1_SLGs = list(toolz.unique(potential_dpb1_SLGs, key=lambda s: s.name))
        # Sort
        potential_dpb1_SLGs.sort(key=operator.attrgetter('name'))
        for slg in potential_dpb1_SLGs:
            slg.assign_TCE_groups(self.tce_map)
        return potential_dpb1_SLGs

    def unambiguous_tce_pair(self):
        """
        Returns boolean on whether the TCE groups of possible
        known DPB1 alleles are unambiguous (only once TCE group)
        :return: boolean
        """
        tce_pairs = set()
        for slg in self.potential_SLGs:
            tce_pairs.add(slg.get_sorted_TCEs())
        return len(tce_pairs) == 1

    def get_known_dpb1_SLG(self):
        """
        Formats known high resolution DPB1 genotype in a list
        return: list of DPB1 objects
        """
        dpb1_slug = self.potential_SLGs[0]
        dpb1_slug.probability = 1.0
        return dpb1_slug

    def __repr__(self):
        return str(self.potential_SLGs)

class DPB1(Allele):
    """
    A subclass of the Allele class specifically designated for the DPB1 allele,
    which contains associated 7-locus haplotypes from the population frequencies.
    Its frequency is calculated by multiplying the sum of the frequencies from these
    haplotypes by the parent 5-locus haplotype.
    """
    def __init__(self, allele_name, haplotypes=[]):
        self.haplotypes = haplotypes
        super().__init__(allele_name)
        self.frequency = None
        self.tce = None

    def calculate_frequency(self, parent_haplotype):
        self.frequency = (mpf(parent_haplotype.frequency) * 
                          mpf(sum([haplotype.frequency 
                              for haplotype in self.haplotypes])))
    
    def get_potential_DPB1s(self, ard):
        """
        Retrieves potential reduced, high-resolution DPB1 alleles.
        :return: list of str
        """
        if self.resolution == "high":
            if ard:
                return [ard.redux_gl(self.name, 'lgx')]
            else:
                return [self.name]
        elif self.resolution == "intermediate":
            return self._get_potential_alleles(ard)

    def _get_potential_alleles(self, ard):
        """
        Returns the potential high-resolution alleles.
        If typing is intermediate, expands the alleles via a MAC service.
        :return: list of alleles (str)
        """
        url = "https://hml.nmdp.org/mac/api/expand?typing="
        try:
            response = requests.get(url + 'HLA-' + self.name)
            data = json.loads(response.content)
            expanded_list = [result['expanded'].replace('HLA-','') for result in data]
            if ard:
                reduced_alleles = [ard.redux_gl(allele, 'lgx') for allele in expanded_list]
                expanded_list = list(dict.fromkeys(reduced_alleles))
            return [allele for allele in expanded_list if allele]
        except Exception as e:
            raise e

    def __repr__(self):
        return str({'name' : str(self.name),
                   'frequency' : str(self.frequency)})

class DPB1_SLUG(object):
    """
    A DPB1 single-locus unambiguous genotype (SLUG) is a pair of DPB1 alleles.
    Its frequency is calculated as the product of those alleles' frequencies.
    That product is doubled if the genotype is homozygous, according to the
    Hardy-Weinberg principle.
    """

    def __init__(self, alleles=None, name=None, frequency=None, probability=None,
                 population=None, tceg=None, ard=None):
        self.alleles = alleles and self._sort(alleles) or []
        self.ard = ard
        if self.ard:
            self._reduce_alleles()
        self.name = name and name or '+'.join([allele.name for allele in self.alleles])
        self.frequency = frequency and frequency or alleles and self._calculate_frequency() or None
        self.probability = probability
        self.tce_name = tceg
        self.population = population
    
    def _reduce_alleles(self):
        """
        Reduces both DPB1 alleles using the py-ard library.
        """
        alleles = []
        for allele in self.alleles:
            try:
                alleles.append(Allele(self.ard.redux_gl(allele.name, 'lgx')))
            except:
                raise InvalidDpb1Error(allele, "%s is not able to be reduced via the antigen-recognition domain." % allele.name)
        self.alleles = alleles
    
    def _sort(self, alleles):
        """
        Sorts the two DPB1 Alleles based on a numeric sorting of the fields, with
        priority on the first (left-most) field.
        Returns the sorted list of allotypes.

        Empty fields have lower priority over populated, numeric fields.

        :param Alleles: Two-element list of two DPB1 Alleles
        :type allotypes: list of DPB1 Alleles
        """
        if not all([isinstance(allele, Allele) or isinstance(allele, DPB1) for allele in alleles]):
            alleles = [DPB1(allele) for allele in alleles]
            self.alleles = alleles
        dpb1_one, dpb1_two = alleles
        fields_a, fields_b = dpb1_one.fields, dpb1_two.fields
        i = 0
        reversed = False
        while len(fields_a) > i and len(fields_b) > i and not reversed:
            if re.match('\d+$', fields_a[i] + fields_b[i]):
                if int(fields_a[i]) > int(fields_b[i]):
                    reversed = True
                elif int(fields_a[i]) < int(fields_b[i]):
                    break
            else:
                if str(fields_a[i]) > str(fields_b[i]):
                    reversed = True
                elif str(fields_a[i]) < str(fields_b[i]):
                    break
            i += 1
        if reversed or len(fields_a) < len(fields_b):
            alleles.reverse()
        return alleles

    def _calculate_frequency(self):
        """
        Calculates the frequency of a DPB1 SLUG by multiplying
        the frequencies of both DPB1 Alleles.
        This value is doubled when the SLUG is heterozygous,
        according to the Hardy-Weinberg principle.
        """
        zygosity_index = (self.alleles[0].name == self.alleles[1].name and
                          1 or 2)
        frequency = ((self.alleles[0].frequency or 0) *
                (self.alleles[1].frequency or 0) *
                zygosity_index)
        return frequency if frequency else 0

    def assign_TCE_groups(self, tce_map):
        for dpb1 in self.alleles:
            dpb1.tce = tce_map.assign_tce(dpb1.name)
    
    def get_sorted_TCEs(self):
        tce_groups = [dpb1.tce for dpb1 in self.alleles]
        tce_groups.sort()
        self.tce_name = '+'.join(tce_groups)
        return self.tce_name

    def contains_DPB1(self, potential_dpb1_SLGs):
        """
        Detects if SLUG contains a DPB1 from potential DPB1 lists.
        :param potential_DPB1s: list of DPB1_SLUGs
        :return: boolean
        """
        pot_dpb1_SLG_names = [dpb1_SLG.name for dpb1_SLG in potential_dpb1_SLGs]
        return self.name in pot_dpb1_SLG_names
    
    def __repr__(self):
        return str({'name' : str(self.name),
                'probability' : str(round(float(self.probability), 3)) if self.probability else 0})

    def serialize(self):
        output = {'genotype' : self.name}
        if self.tce_name:
            output['tce_groups'] = self.tce_name
        if self.frequency:
            output['probability'] = float(self.probability) if self.probability else 0
        return output

class InvalidDpb1Error(Exception):

    def __init__(self, dpb1, message):
        self.dpb1 = dpb1
        self.meesage = message
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
from dpb1.allele import Allele
try:
    from dpb1.dpb1 import DPB1
except:
    import dpb1
from sigfig import round

class Haplotype(object):
    """
    Represents a set of alleles inherited from one parent.
    Here, a haplotype is built from the following loci:

    A~C~B~DRB1~DRB3/4/5~DQB1~DPB1

    The allele names are separated by '~' from one another
    to indicate they occur on the same phase, and thus the same
    haplotype.

    :param name: The haplotype name, str
    """

    def __init__(self, name=None, population=None, frequency=None):
        self.name = name
        self.alleles = name and self._get_alleles(name)
        self.dpb1_alleles = []
        self.population = population
        self.frequency = frequency
        self.ref_haplotypes = None
        self.locus_order = self._get_locus_order()

    def remove_alleles(self, loci):
        """
        Removes alleles from supplied loci
        :param loci: list of loci (str)
        :return: None
        """
        for locus in loci:
            self.alleles.pop(locus)
        self.name = '~'.join(self.alleles)

    def extract_DPB1_alleles(self, reference_frequencies):
        """
        Takes in PopulationFrequencies and extracts the possible DPB1
        alleles according to this haplotype's name.
        :param population_freqs: PopulationFrequencies
        :return: None
        """
        #print('Extracting DPB1 allele from', self.name)
        ref_haplotypes = reference_frequencies.get_possible_haplotypes(self)
        #print('Obtained', len(ref_haplotypes), 'haplotypes')
        self.ref_haplotypes = ref_haplotypes
        self._set_possible_DPB1s(ref_haplotypes)

    def _set_possible_DPB1s(self, ref_haplotypes):
        """
        Takes in a set of reference 7-locus haplotypes and generates
        DPB1 objects for each unique DPB1 allele. Each DPB1 object will
        also be initiated with a list of associated haplotypes.
        :param ref_haplotypes: list of 7-locus Haplotypes
        :return: None
        """
        dpb1_haplotypes = {}
        for ref_haplotype in ref_haplotypes:
            dpb1_name = ref_haplotype.alleles["DPB1"].name
            if dpb1_name in dpb1_haplotypes:
                dpb1_haplotypes[dpb1_name].append(ref_haplotype)
            else:
                dpb1_haplotypes[dpb1_name] = [ref_haplotype]
        for dpb1_name, ref_haplotypes in dpb1_haplotypes.items():
            try:
                dpb1 = DPB1(dpb1_name, haplotypes = ref_haplotypes)
            except:
                import dpb1
                dpb1 = dpb1.DPB1(dpb1_name, haplotypes = ref_haplotypes)
            dpb1.calculate_frequency(self)
            self.dpb1_alleles.append(dpb1)
    
    def _get_locus_order(self):
        """
        Return ordered list of allele names (str) for this haplotype.
        """
        if not self.alleles:
            return []
        return list(self.alleles.keys())

    def formatted_name(self, loci, drbx=None):
        """
        Takes in a list of loci, denoting the order of
        how the alleles in the haplotype should be displayed.
        Resulting name is returned.
        :param loci: list of str e.g., ['A', 'C', 'B', 'DRB1', 'DQB1']
        :param drbx: Substitutes a provided wildcard string in for DRBX
        :return name: formatted haplotype name (str)
        """
        alleles = []
        for locus in loci:
            if locus == 'DRBX' and drbx:
                alleles += [drbx]
            else:
                alleles += [self.alleles[locus].name]
        return '~'.join(alleles)
            
    def _get_alleles(self, haplotype_name):
        """
        Ensures that appropriate Alleles are accepted.

        :param haplotype_name: A haplotype name (str)
        :return alleles: List of Allele objects
        """
        alleles = {}
        for allele_name in haplotype_name.split('~'):
            if allele_name:
                allele = Allele(allele_name)
                if allele.locus in alleles:
                    raise InvalidHaplotypeError(haplotype_name,
                        "The haplotype contains duplicate loci.")
                else:
                    locus = (allele.locus in ["DRB3", "DRB4", "DRB5"] and
                             "DRBX" or allele.locus)
                    alleles[locus] = allele
            else:
                raise InvalidHaplotypeError(haplotype_name,
                        "The haplotype contains a non-Allele value.")

        if not alleles:
            raise InvalidHaplotypeError(haplotype_name,
                    "No valid alleles were supplied through this haplotype.")

        return alleles

    def __repr__(self):
        return ','.join([self.name or '',
                        self.population or '',
                        str(round(self.frequency, 3)) if self.frequency else '0'])

class InvalidHaplotypeError(Exception):

    def __init__(self, haplotype_name, message):
        self.name = haplotype_name
        self.message = message

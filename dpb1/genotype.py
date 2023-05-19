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
import dpb1.haplotype
from .dpb1 import DPB1_SLUG

class Genotype(object):
    """
    Represents a pair of haplotypes built from these loci:

    A~C~B~DRB1~DRB3/4/5~DQB1~DPB1

    The haplotypes are separated by a '+'.

    :param name: A list of two Haplotype objects or a genotype name (str)
    """

    def __init__(self, haplotypes, index : int = None, prob : float = None):
        self.index = index
        self.prob = prob
        self.SLUGs = None
        if isinstance(haplotypes, str):
            self.name = haplotypes
            self.haplotypes = self._get_haplotypes(haplotypes)
        elif (len(haplotypes) == 2):
                self.name = haplotypes[0].name + '+' + haplotypes[1].name
                self.haplotypes = haplotypes
        else:
            raise InvalidGenotypeError(haplotypes,
                    "Please provide a genotype name or two-element list of valid Haplotype objects")

    def _get_haplotypes(self, genotype_name):
        """
        Ensures that appropriate Haplotypes are accepted.

        :param genotype_name: A genotype name (str)
        :return haplotype_one, haplotype_two: Tuple of Haplotype objects
        """
        haplotype_names = genotype_name.split('+')
        if len(haplotype_names) != 2:
            raise InvalidGenotypeError(genotype_name,
                        "The genotype does not contain only two haplotypes.")
        haplotypes = []
        for haplotype_name in haplotype_names:
            if haplotype_name:
                haplotype = dpb1.haplotype.Haplotype(name=haplotype_name)
                haplotypes.append(haplotype)
            else:
                raise InvalidGenotypeError(genotype_name,
                        "The genotype contains a non-haplotype value.")
        return haplotypes

    def extract_DPB1_alleles(self, population_freqs):
        for haplotype in self.haplotypes:
            haplotype.extract_DPB1_alleles(population_freqs)

    def generate_SLUGs(self):
        """
        Generates SLUGs based on all the possible combinations of possible DPB1 alleles
        from both haplotypes
        :return: None
        """
        population = self._remove_duplicates([haplotype.population for haplotype in self.haplotypes])

        if len(population) == 1:
            population = population[0]
        else:
            raise InvalidGenotypeError(self.name, 'Imputed haplotypes contained different populations')

        self.SLUGs = [DPB1_SLUG(alleles=[dpb1_1, dpb1_2], population=population)
                      for dpb1_1 in self.haplotypes[0].dpb1_alleles
                      for dpb1_2 in self.haplotypes[1].dpb1_alleles 
                      if dpb1_1.frequency and dpb1_2.frequency]
        return self.SLUGs
    
    def _remove_duplicates(self, alist):
        return list(dict.fromkeys(alist))

    def __repr__(self):
        return str(self.haplotypes)

class InvalidGenotypeError(Exception):

    def __init__(self, genotype_name, message):
        self.name = genotype_name
        self.message = message

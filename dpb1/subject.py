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
from .allele import Allele
from .haplotype import Haplotype
from .genotype import Genotype, InvalidGenotypeError
from .imputation import Imputation
from .tce import TCE_SLUG, TCE
from .dpb1 import DPB1s, DPB1, DPB1_SLUG
from .frequencies import PopulationHaplotypeFreqs
from .population import Population
import operator

class Subject(object):

    def __init__(self, glstring=None, id=None, population=None, imputation=None, ard=None, tce_map=None,
                       locus_order=['A', 'C', 'B', 'DRBX', 'DRB1', 'DQB1'], ref_freqs=None, subject_type=None,
                       imputation_url=None):            
        """
        Represents an individual patient or donor including:
        :param str glstring: HLA typing through a Genotype List string (GL string)
        :param str id: Identifier string
        :param str population: Self-identified race and ethnicity code
        :param list imputation: List of dictionaries with the following format:
                                ({"haplotype1", "population1", frequency1",
                                "haplotype2", "population2", frequency2"})
        :param ARD ard: pyard.ARD object
        :param TCE_map tce_map: dpb1.tce.TCE_map object
        :param list locus_order: List of str loci for defining the first-stage imputation (without DPB1)
        :param PopulationHaplotypeFreqs ref_freqs: dpb1.frequencies.PopulationHaplotypeFreqs object for the given population
        :param str subject_type: A label indicating the subject type (patient or donor, for example)
        """
        self.ard = ard
        self.tce_map = tce_map
        self.glstring, self.dpb1 = self._split_dpb1(glstring)
        self.id = id
        self.locus_order = locus_order 
        self.population = population and Population(population).code or None
        if not imputation and not self.dpb1 or (self.dpb1 and not self.dpb1.unambiguous_tce_pair()):
            self.imputation = self._impute(imputation_url=imputation_url)
        else:
            self.imputation = imputation
        self.ref_freqs = ref_freqs or PopulationHaplotypeFreqs(self.population)
        self.subject_type = subject_type
        self.epsilon = 0.01
        self.SLUGs = []
        self.tce_genotypes = []
        self.tce_groups = []
        self.non_dpb1_haplotypes = []

    def _split_dpb1(self, glstring):
        """
        Splits the DPB1 locus off of a GL string.
        :param str glstring: Genotype List string of HLA
        :return glstring, dpb1: str, list of DPB1 classes
        """
        if not glstring:
            return None, None
        loci_names = glstring.split('^')
        dpb1_loci = [locus for locus in loci_names if 'DPB1' in locus]
        other_loci = [locus for locus in loci_names if 'DPB1' not in locus]
        if len(dpb1_loci) > 1:
            raise InvalidSubjectError(self.id,  "GLString (%s) contains more than one DPB1 locus."
                                                " Ensure that when splitting using the '^' character,"
                                                " there are unique locus groups." % glstring)
        glstring = '^'.join(other_loci)
        dpb1_gl = len(dpb1_loci) and dpb1_loci[0] or []
        dpb1 = (dpb1_loci and DPB1s(dpb1_gl, ard=self.ard, tce_map=self.tce_map)
                          or None)
        return glstring, dpb1

    def _format_typing(self, glstring):
        """
        Takes a GLstring (Genotype List string) and 
        creates an organized dictionary of locus strings
        to two-element Allele lists
        :param allele_names: list of str
        :return typing: Dict of str, list of Allele
        """
        allele_names = [typing for locus_typings in glstring.split('^') 
                               for typing in locus_typings.split('+')]
        alleles = ['DPB1' in allele_name and DPB1(allele_name) or Allele(allele_name)
                   for allele_name in allele_names]
        typing = {}
        for allele in alleles:
            if allele.locus in typing:
                typing[allele.locus].append(allele)
            else:
                typing[allele.locus] = [allele]
        return typing

    def generate_dpb1_slugs(self):
        """
        :return: List of DPB1 single-locus unambiguous genotypes (SLUGs)
        """
        SLUG_map = {}
        if (not self.imputation and
            self.dpb1 and len(self.dpb1.potential_SLGs) == 1): # Due to unambiguous TCE or empty imputation
                if not self.dpb1.unambiguous_tce_pair():
                    raise InvalidSubjectError("No available imputation and contains ambiguous DPB1 TCE groups.")
                dpb1_SLG = self.dpb1.get_known_dpb1_SLG()
                dpb1_SLG.assign_TCE_groups(self.tce_map)
                self.SLUGs = [dpb1_SLG]
                return self.SLUGs
        if self.imputation:
            for i, genotype in enumerate(self.imputation.genotypes):
                for haplotype in genotype.haplotypes:
                    haplotype.extract_DPB1_alleles(self.ref_freqs)
                    if not haplotype.ref_haplotypes:
                        self.non_dpb1_haplotypes.append(haplotype)
                slugs = genotype.generate_SLUGs()
                for slug in slugs:
                    if not self.dpb1 or slug.contains_DPB1(self.dpb1.potential_SLGs):
                        if slug.name in SLUG_map:
                            SLUG_map[slug.name].frequency += slug.frequency
                        else:
                            SLUG_map[slug.name] = slug
            self.SLUGs = list(SLUG_map.values())
            self._normalize_SLUGs()
            self._order_by_probability(self.SLUGs)
        if not self.SLUGs and self.dpb1 and self.dpb1.potential_SLGs:
            self.SLUGs = self.dpb1.potential_SLGs
        return self.SLUGs

    def no_imputed_slgs(self):
        """
        Returns boolean on whether any DPB1 single-locus genotypes (SLGs) were 
        imputed.
        """
        return len([slg for slg in self.SLUGs if slg.frequency != None]) == 0

    def generate_tce_genotypes(self):
        tce_slug_map = {}
        if self.dpb1:
            if self.dpb1.unambiguous_tce_pair():
                self.tce_genotypes = [TCE_SLUG(self.dpb1.potential_SLGs[0].get_sorted_TCEs(), 
                                          dpb1_slug_list=self.SLUGs, probability=1.0)]
                self._generate_tce_groups()
                return self.tce_genotypes
            elif ((not self.SLUGs or
                   self.no_imputed_slgs())
                    and self.dpb1.potential_SLGs):
                tce_pairs = set([slg.get_sorted_TCEs() for slg in self.dpb1.potential_SLGs])
                self.tce_genotypes = [TCE_SLUG(tce_pair, probability=None) for tce_pair in tce_pairs]
                self.tce_genotypes.sort(key=operator.attrgetter('name'))
                self._generate_tce_groups()
                return self.tce_genotypes
        # TCE Genotypes
        for dpb1_slug in self.SLUGs:
            dpb1_slug.assign_TCE_groups(self.tce_map)
            sorted_tce_name = dpb1_slug.get_sorted_TCEs()
            if sorted_tce_name in tce_slug_map:
                tce_slug_map[sorted_tce_name].append(dpb1_slug)
            else:
                tce_slug_map[sorted_tce_name] = [dpb1_slug]
        self.tce_genotypes = []
        for tce_name, dpb1_slug_list in tce_slug_map.items():
            self.tce_genotypes.append(TCE_SLUG(tce_name, dpb1_slug_list=dpb1_slug_list))
        self._order_by_probability(self.tce_genotypes)
        self._generate_tce_groups()
        return self.tce_genotypes

    def _generate_tce_groups(self):
        tce_groups = {}
        for tce_genotype in self.tce_genotypes:
            min_tce = tce_genotype.min_tce
            if min_tce not in tce_groups:
                tce_groups[min_tce] = TCE(min_tce)
            tce_groups[min_tce].add_probability(tce_genotype.probability)
        self.tce_groups = list(tce_groups.values())
        self._order_by_probability(self.tce_groups)


    def _impute(self, imputation_url=None):
        """
        Creates an Imputation object and tells it to obtain
        the imputed (potential) genotypes for this subject's typing.
        :return: Imputation object
        """
        imputation = Imputation(glstring=self.glstring, 
                                population=self.population, 
                                locus_order=self.locus_order,
                                imputation_url=imputation_url)
        imputation.impute()
        return imputation

    def _normalize_SLUGs(self):
        """
        Normalizes the SLUGs by calculating the sum of all their frequencies
        and dividing each SLUG's frequency by that sum.
        :return: None
        """
        dpb1_sum = sum([SLUG.frequency for SLUG in self.SLUGs])
        for SLUG in self.SLUGs:
            SLUG.probability = SLUG.frequency / dpb1_sum
        
    def _order_by_probability(self, slug_list):
        """
        Orders the SLUGs (DPB1 alleles or TCE groups) by probability, descending.
        :return: None
        """
        if slug_list and slug_list[0].probability:
            slug_list.sort(key=lambda SLUG: SLUG.probability, reverse=True)

    def _filter_epsilon(self, SLGs):
        """
        Returns the list of SLGs with probabilities higher than the
        epsilon value.
        :return: List of SLGs objects
        """
        return [SLG for SLG in SLGs 
                if SLG.probability == None or 
                   SLG.probability > self.epsilon]
    
    def filter_SLGs(self):
        """
        Filters DPB1 SLGs and TCE groups based on epsilon.
        """
        self.SLUGs = self._filter_epsilon(self.SLUGs)
        self.tce_groups = self._filter_epsilon(self.tce_groups)
        self.tce_genotypes = self._filter_epsilon(self.tce_genotypes)

    def serialize(self):
        self.filter_SLGs()
        output = {}
        if self.id:
            output['id'] = self.id
        output['dpb1_tce_groups'] = [tce.serialize() for tce in self.tce_groups]
        output['dpb1_tce_genotypes'] = [tce_genotype.serialize() for tce_genotype in self.tce_genotypes]
        output['dpb1_genotypes'] = [slg.serialize() for slg in self.SLUGs]
        if self.non_dpb1_haplotypes:
            output['non_dpb1_haplotypes'] = [haplo.name for haplo in self.non_dpb1_haplotypes]
        return output


class InvalidSubjectError(Exception):

    def __init__(self, id, message):
        self.id = id
        self.message = message

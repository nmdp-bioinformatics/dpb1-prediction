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
import os
import csv
from .population import Population
from .allele import Allele
import dpb1.haplotype
import dpb1.genotype
from .dpb1 import DPB1, DPB1_SLUG
import time
import gzip
import re

class PopulationHaplotypeFreqs(object):

    def __init__(self, population, file_path=None, locus_order=None, directory=None):
        self.population = Population(population).get_code()
        self.directory = directory or 'data/frequencies'
        self.file_path = file_path
        self.headers = self._get_headers()
        self.locus_order = locus_order or ['A', 'C', 'B', 'DRB1', 'DQB1']
        self.haplotypes = self._load_haplotypes()

    def _load_haplotypes(self):
        """
        Loads haplotypes from the population's frequency file.
        :return: dict of key haplotype (str) and value DPB1 haplotype (Haplotype)
        """
        haplotypes = {}
        with gzip.open(self.file_path, 'rt') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for row in csv_reader:
                haplotype_name = row[self.headers.index("Haplo")]
                frequency = float(row[self.headers.index("Freq")])
                haplo_key, haplo_value = self._split_haplotype(haplotype_name)
                # sub_haplo = dpb1.haplotype.Haplotype(haplo_value, 
                #                 population=self.population, 
                #                 frequency=frequency)
                sub_haplo = (haplo_value, frequency)
                if haplo_key in haplotypes:
                    haplotypes[haplo_key].append(sub_haplo)
                else:
                    haplotypes[haplo_key] = [sub_haplo]
        return haplotypes

    def _split_haplotype(self, haplotype_name):
        """
        Splits a haplotype string and partitions it based on
        locus order.
        :param haplotype_name: Haplotype name (str)
        :return: haplotype name without DPB1 (str), haplotype name with DPB1 (str)
        """
        haplo_key = []
        haplo_value = []
        locus_order = self.locus_order.copy()
        if 'DRBX' in self.locus_order:
            locus_order += ['DRB3', 'DRB4', 'DRB5']
        for allele in haplotype_name.split('~'):
            locus = allele.split('*')[0]
            if locus in locus_order:
                haplo_key.append(allele)
            else:
                haplo_value.append(allele)
        sorted_haplo = dpb1.haplotype.Haplotype('~'.join(haplo_key)).formatted_name(self.locus_order)
        dpb1_haplo = '~'.join(haplo_value)
        return sorted_haplo, dpb1_haplo

    def get_possible_haplotypes(self, haplotype):
        """
        Obtains possible DPB1-containing haplotypes that contain the same 5 loci of self.haplotype.
        Generates a regex for self.haplotype's name.
        :param haplotype: dpb1.haplotype.Haplotype
        """
        # if 'DRBX' in self.locus_order:
        #     hap_key = haplotype.formatted_name(self.locus_order, drbx='DRBX*NNNN')
        #     # print(haplotype)
        #     if hap_key in self.haplotypes:
        #         hap_freqs += self.haplotypes[hap_key]
        hap_freqs = []
        for with_drbx in [True, False]:
            if (with_drbx and ('DRBX' not in self.locus_order or
                               'DRBX' not in haplotype.locus_order)):
                continue
            hap_key = haplotype.formatted_name(self.locus_order,
                                                drbx=None if with_drbx else 'DRBX*NNNN')
            if hap_key in self.haplotypes:
                hap_freqs += self.haplotypes[hap_key]
        return [dpb1.haplotype.Haplotype(name=hap_freq[0], 
                population=self.population, 
                frequency=hap_freq[1]) 
                for hap_freq in hap_freqs]

    def _get_filepath(self):
        """
        Obtains the filepath for the relevant population.
        :param population: str
        :return: str
        """
        return '%s/%s.freqs.gz' % (self.directory, self.population)

    def _get_headers(self):
        """
        Reads the first comma-delimited line of this object's filepath
        and assigns the elements as a header attribute
        Ex: Haplo,Count,Freq,D
        :return: list of str or None
        """
        try:
            with gzip.open(self.file_path, mode='rt') as f:
                reader = csv.reader(f)
                headers = next(reader)
                return headers
        except:
            message = 'Haplotype frequency files are not present in ' + self.directory 
            raise InvalidFrequenciesError(self.file_path, message)

class HaplotypeFreqs(object):

    def __init__(self, 
            directory="data/frequencies", 
            locus_order=['A', 'C', 'B', 'DRB1', 'DQB1'],
            populations=[]):
        self.directory = directory
        self.locus_order = locus_order
        self.populations = self._init_pop_freqs(populations=populations)

    def _init_pop_freqs(self, populations=[]):
        """
        Initiates the population haplotype frequencies in a directory.
        dict of population code (str), PopulationHaplotypeFreqs
        """
        freq_files = os.listdir(self.directory)
        pop_freqs = {}
        print("Initializing population frequencies")
        n = 1
        for freq_file in freq_files:
            pop_cde = freq_file.split('.freqs')[0]
            pop_cde_match = re.search('[A-Z]+', freq_file)
            if pop_cde_match:
                pop_cde = pop_cde_match.group()
                population = Population(pop_cde)
                file_path = self.directory + '/' + freq_file
                if population.valid and (not populations or pop_cde in populations):
                    start_time = time.time()
                    pop_freqs[population.code] = PopulationHaplotypeFreqs(pop_cde,
                                                    locus_order=self.locus_order,
                                                    directory=self.directory,
                                                    file_path=file_path)
                    print('%s/%s - %s - %s sec' % 
                            (n,
                            len(populations) if populations else len(freq_files),
                            pop_cde, round(time.time() - start_time, 3)))
                    n += 1
        return pop_freqs
    
    def get_pop_freqs(self, population):
        pop_code = Population(population).get_code()
        if pop_code == "NAMER" and "NAMER" not in self.populations:
            pop_code = "EURCAU"
        if pop_code in self.populations:
            return self.populations[pop_code]
        else:
            raise InvalidFrequenciesError(self.directory, 'The %s population was not properly loaded.' % pop_code)

class InvalidFrequenciesError(Exception):

    def __init__(self, filepath, message):
        self.filepath = filepath
        self.message = message

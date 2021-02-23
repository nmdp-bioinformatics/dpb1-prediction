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
class Population(object):

    def __init__(self, population):
        self.code = self._set_population(population)
        self.valid = self._set_validity()

    def get_code(self):
        return self.code

    def _set_population(self, population):
        pop_map = {"MAFA" : "AFA", "NAMB" : "AFA",
                    "MAPI" : "API",
                    "EEURO" : "CAU", "EURWRC" : "CAU", "MCAU" : "CAU", "MEDIT" : "CAU", "MIDEAS" : "CAU",
                    "NCAFRI" : "CAU", "NEURO" : "CAU", "WCARIB" : "CAU", "WEURO" : "CAU", "WSCA" : "CAU",
                    "DEC" : "DEC",
                    "GUAMAN" : "HAWI", "HAWAII" : "HAWI", "MHAW" : "HAWI", "OPI" : "HAWI", "SAMOAN" : "HAWI",
                    "MHIS" : "HIS",
                    "MULTI" : "MULTI",
                    "MNAM" : "NAM"}
        return population in pop_map and pop_map[population] or population

    def _set_validity(self):
        populations = ["AAFA", "CARHIS", "MSWHIS", "AFA", "CARIBI",
                       "NAM", "AFB", "CAU", "NAMER", "AINDI", "FILII",
                       "NCHI", "AISC", "HAWI", "SCAHIS", "ALANAM", "HIS",
                       "SCAMB", "AMIND", "JAPI", "SCSEAI", "API", "KORI",
                       "VIET", "CARB", "MENAFC", "MULTI", "UNK", "OTH", "EURCAU"]
        return self.code in populations
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

class Allele(object):
    """
    Represents an HLA allele, which is a variation of a gene.
    These loci are considered in this microservice: A, C, B, DRB1, DRB3/4/5, DQB1, DPB1.

    Alleles are formatted with the locus name, followed by an asterisk
    and a list of fields (integers) delimited by colons.
    
    :param allele_name: A string, the allele name
    """
    def __init__(self, allele_name, frequency=None):
        self.name = allele_name
        self.locus, self.fields, self.resolution, self.is_null = self._get_info()
        self.frequency = frequency

    def _get_info(self):
        """
        Extracts the locus name, a list of fields (integers),
        and the resolution level of the allele.
        Raises error if format is invalid.

        :return: type (str), fields (list)
        """
        locus_regex = '[ACB]|(?:DRB[X1345])|(?:DQB1)|(?:DPB1)'
        if '+' in self.name:
            raise InvalidAlleleError(self.name, "Allele cannot contain a '+'")
        low_res_match = re.match('(%s)(\d+)' % (locus_regex), self.name)
        resolution = None
        if low_res_match:
            locus, fields = low_res_match.group(1,2)
            resolution = 'low'
        else:
            try:
                locus, fields = self.name.split('*')
            except:
                raise InvalidAlleleError(self.name, "Allele needs to contain exactly one asterisk '*'.")
        if not re.match(locus_regex + '$', locus):
            raise InvalidAlleleError(self.name, "The allele's locus is not supported. "
                                            "Please use A, C, B, DRB1, DRB3, DRB4, DRB5, DQB1, or DPB1.")

        if not re.match('[\dN]+(\:[A-Z\d]+)*[A-Z]?$', fields):
            raise InvalidAlleleError(self.name, "The fields are incorrectly formatted. "
                                            "Please include at least one field (integers). "
                                            "Additional fields are appended with a preceding semicolon ':'. "
                                            "For example, A*01:01 is a valid format but A*01:01: is not.")
        
        var_expression = (re.search('\d+[A-Z]$', self.name) and
                          fields[-1] or None)
        if var_expression: fields = fields[:-1]

        if not resolution:
            if re.match('N+', fields):
                fields = [None]
                resolution = None
            else:
                fields = fields.split(':')
                resolution = (re.match('^[A-Z]+$', fields[1]) and 'intermediate' or
                            re.match('^[0-9]+$', fields[1]) and 'high' or None)
                if not resolution:
                    raise InvalidAlleleError(self.name, "The level of typing resolution cannot be determined.")
        else:
            fields = [fields]
        return locus, fields, resolution, var_expression == 'N'

    def __repr__(self):
        return str({'name' : str(self.name), 
                    'freq' : str(self.frequency)})

class InvalidAlleleError(Exception):

    def __init__(self, allotype_name, message):
        self.name = allotype_name
        self.message = message
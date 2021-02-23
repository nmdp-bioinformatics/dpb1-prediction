Feature: Define Allele
    An allele is an alternative version of a gene.
    In the context of the DPB1 microservice, only HLA alleles are
    considered, specifically these loci:

    A, C, B, DRB1, DRB3/4/5, DQB1, DPB1
    
    Scenario Outline: Allele names

        Given the allele name is <Allele Name>
        When evaluating the allele
        Then the allele name is found to be <Validity>
        And the field list is found to be <Fields>
        And the level of resolution is found to be <Resolution>

        Examples: Valid examples of alleles
            | Allele Name | Validity | Fields     | Resolution   |
            | A7          |  valid   | 7          | low          |
            | B35         |  valid   | 35         | low          |
            | DQB15       |  valid   | 5          | low          |
            | C*40:05     |  valid   | 40, 05     | high         |
            | DRB3*07:112 |  valid   | 07, 112    | high         |
            | B*07:68:03  |  valid   | 07, 68, 03 | high         |
            | B*07:68:03  |  valid   | 07, 68, 03 | high         |
            | A*03:ANKG   |  valid   | 03, ANKG   | intermediate |
            | DRB4*03:01N |  valid   | 03, 01     | high         |
            | DRBX*NNNN   |  valid   | NA         | NA           |

        Examples: Invalid examples of alleles
            | Allele Name | Validity | Fields  | Resolution |
            | B*:07:68:03 | invalid  | invalid | invalid    |
            | B*07::68:03 | invalid  | invalid | invalid    |
            | B*07:68:03: | invalid  | invalid | invalid    |
            | HLA-C*01:01 | invalid  | invalid | invalid    |
            | 😄          | invalid  | invalid | invalid    |
            | DRB2*01:01  | invalid  | invalid | invalid    |
            | B7+B8       | invalid  | invalid | invalid    |
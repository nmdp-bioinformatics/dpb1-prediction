Feature: Define Subject

    A subject represents a donor or recipient.

    To impute their DPB1 alleles, we need to have their typing available (intermediate or high).

    It is preferred to have five loci (A, C, B, DRB1, DQB1) if possible.

    Most importantly, the imputation in this service is based off of population frequencies,
    so a population code is needed.

    Scenario: Allele typings

        Given this set of typings
            | Typing 1      | Typing 2      |
            | A*11:01:01:01 | A*24:02:01:01 |
            | C*02:02:02    | C*04:01:01    |
            | B*44:05:01    | B*35:01:01    |
            | DRB1*11:03:01 | DRB1*03:01:01 |
            | DQB1*03:01:01 | DQB1*05:01    |
            | DPB1*03:01:01 | |
        And the subject's population code as 'MCAU'
        And these relevant reference haplotype frequencies for that population
        And the resulting donor subject
        When checking the DPB1 alleles
        Then the alleles are found to be "DPB1*03:01+DPB1*03:01"
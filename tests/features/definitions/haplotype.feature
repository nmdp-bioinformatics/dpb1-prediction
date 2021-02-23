Feature: Define Haplotype

    A haplotype represents the allele set inherited from one parent.
    Humans normally have two haplotypes from both parents.
    In this microservice, a haplotype is built from the following loci:

    A~C~B~DRB1~DRB3/4/5~DQB1~DPB1

    '~' denotes that the alleles on either side are on the same phase.

    Scenario Outline: Haplotype names

        Given the haplotype name as <Haplotype>
        When evaluating the validity of the haplotype name
        Then the haplotype name is found to be <Validity>

        Examples: Valid examples of alleles
            | Haplotype                                                           | Validity |
            | A*02:01~C*07:02~B*08:02~DRB1*15:01~DQB1*06:02                       |  valid   |
            | A*30:01~C*17:01~B*42:01~DRB3*01:01~DRB1*03:02~DQB1*04:02~DPB1*01:01 |  valid   |

        Examples: Invalid examples of alleles
            | Haplotype                                                           | Validity |
            | A*02:01~A*07:02~B*08:02~DRB1*15:01~DQB1*06:02                       | invalid  |
            | A*02:01+C*07:02~B*08:02+DRB1*15:01~DQB1*06:02                       | invalid  |
            | 😄                                                                  | invalid  |

    # Scenario: Selecting alleles from a haplotype

    #     Given the haplotype as "A*02:01~C*07:02~B*08:02~DRB1*15:01~DQB1*06:02"
    #     When selecting specific allele names
    #     Then the allele <Locus> is found to be <Name>
    #         | Locus | Name       |
    #         | A     | A*02:01    |
    #         | C     | A*07:02    |
    #         | B     | A*08:02    |
    #         | DRB1  | DRB1*15:01 |
    #         | DQB1  | DQB1*06:02 |
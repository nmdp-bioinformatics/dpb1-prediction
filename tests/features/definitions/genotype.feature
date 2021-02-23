Feature: Define Genotype

    A genotype consists of two haplotypes: one from each of an
    individual's parents. If both haplotypes are the same, then
    the genotype is said to be homozygous. If they are different,
    then the genotype is heterozygous.

    A genotype can be represented via two haplotype names joined
    by a '+'.

    Scenario Outline: Genotype names

        Given the genotype name as <Genotype>
        When evaluating the validity of the genotype name
        Then the genotype name is found to be <Validity>

        Examples: Valid examples of genotypes
            | Genotype                                                                                    | Validity |
            | A*02:01~C*07:02~B*08:02~DRB1*15:01~DQB1*06:02+A*02:01~C*07:02~B*08:02~DRB1*15:01~DQB1*06:02 |  valid   |
            | A*02:01~C*07:02~B*07:02~DRB1*15:01~DQB1*06:02+A*02:01~C*07:02~B*07:02~DRB1*15:01~DQB1*06:03 |  valid   |

        Examples: Invalid examples of genotypes
            | Genotype                                                           | Validity |
            | A*30:01~C*17:01~B*42:01~DRB3*01:01~DRB1*03:02~DQB1*04:02~DPB1*01:01 | invalid  |
            | 🧬+🧬                                                               | invalid  |
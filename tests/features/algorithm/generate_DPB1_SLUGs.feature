Feature: Generating DPB1 SLUGs

    **Imputation**
    After defining the subject, the 5-locus HLA typing (A, C, B, DRB1, DQB1)
    is submitted to an imputation service that determines possible haplotypes
    and population-dependent frequencies.

    **Reference Frequency Preparation**
    These imputed 5-locus haplotype pairs (genotypes) are then compared to
    population-stratified 7-locus frequencies (A, C, B, DRB1, DQB1, DRB3/4/5, and DPB1)
    filled out through an Expectation Maximization (EM) algorithm. These haplotype frequencies
    are sorted in this order to facilitate fast look up: A, C, B, DRB1, DQB1, DRB3/4/5, DPB1.

    **DPB1 Allele Extraction**
    Using these reference 7-locus frequencies, the possible DPB1 alleles and frequencies are obtained.
    Programmatically, the 7-locus set of haplotypes associated with a DPB1 allele are stored within
    each unique DPB1 allele, which is a subclass of the Allele class.
    To calculate each DPB1 allele's frequency, the frequencies from the allele's 7-locus set are added
    together and multipled by the frequency of the parent 5-locus haplotype.

    **DPB1 SLUG Generation
    After obtaining the DPB1 alleles for each imputed haplotype, the possible DPB1 single-locus unambiguous
    genotypes (SLUGs) need to be generated. This is accomplished by taking two DPB1 lists from both haplotypes
    in an imputed genotype and iterating through each possible DPB1 pair to create SLUGs and with genotype frequencies.
    These frequencies are just the product of the DPB1 allele frequencies, unless it is a homozygous
    genotype. In that case, the resulting frequency is further doubled in accordance with the Heidy-Weinberg
    principle.

    These process is repeated for each imputed genotype for a subject. Upon completion,
    the SLUGs are normalized by dividing each genotype frequency by the total sum of all the frequencies from
    each generated SLUG.

    Background: Subject Preparation

        Given this set of typings
            | Typing 1 | Typing 2 |
            | A*02:05:01 | A*33:01:01 |
            | C*07:01:01 | C*08:02:01 |
            | B*14:02:01:01 | B*41:01:01:01 |
            | DRB1*13:02:01 | DRB1*13:02:01 |
            | DQB1*06:04:01 | DQB1*06:04:01 |
        And the subject's population code as 'CAU'
        And these relevant reference haplotype frequencies for that population
        And the resulting donor subject

    Scenario: Retrieve Imputation

        Given these expected imputed genotypes
            | Haplotype 1                                   | Freq 1   | Haplotype 2                                   | Freq 2   |
            | A*33:01~C*08:02~B*14:02~DRB1*13:02~DRB3*03:01~DQB1*06:04 | 4.80e-05 | A*02:05~C*07:01~B*41:01~DRB1*13:02~DRB3*03:01~DQB1*06:04 | 3.14e-06 |
        When obtaining the imputed genotypes
        Then the expected versus obtained genotypes are found to be equal
    
    Scenario: Reference Frequency Preparation
        
        Given these expected sorted reference frequencies for "A*02:05~C*07:01~B*41:01~DRB1*13:02~DQB1*06:04"
            | Haplotype 			| Freq	 |
            | DRB3*03:01~DPB1*02:01 | 3.924e-7 |
            | DRB3*03:01~DPB1*03:01 | 1.021e-6 |
            | DRB3*03:01~DPB1*04:01 | 9.322e-7 |
            | DRB3*03:01~DPB1*04:02 | 1.685e-7 |
            | DRB3*03:01~DPB1*14:01 | 1.714e-6 |
            | DRB3*03:01~DPB1*19:01 | 6.541e-7 |
            | DRB3*03:01~DPB1*34:01 | 3.330e-7 |
        When obtaining the imputed genotypes
        And focusing on the haplotype "A*02:05~C*07:01~B*41:01~DRB1*13:02~DRB3*03:01~DQB1*06:04"
        And obtaining the sorted reference haplotype frequencies for that haplotype
        Then the expected and obtained sorted reference haplotype frequencies are the same

    Scenario: DPB1 Allele Extraction

        When obtaining the imputed genotypes
        And focusing on the haplotype "A*02:05~C*07:01~B*41:01~DRB1*13:02~DRB3*03:01~DQB1*06:04"
        And obtaining the sorted reference haplotype frequencies for that haplotype

        And obtaining the possible DPB1 alleles and frequencies for that haplotype
        Then the possible DPB1 alleles for that haplotype are "DPB1*02:01,DPB1*03:01,DPB1*04:01,DPB1*04:02,DPB1*14:01,DPB1*19:01,DPB1*34:01"
        And the frequencies of those DPB1 alleles for that haplotype are "1.23e-12,3.2e-12,2.93e-12,5.29e-13,5.38e-12,2.05e-12,1.05e-12"

    Scenario: DPB1 SLUG Generation

        Given these expected SLUGs
            | SLUG                  | Probability |
            | DPB1*02:01+DPB1*14:01 | 0.142  |
            | DPB1*02:01+DPB1*03:01 | 0.0958 |
            | DPB1*02:01+DPB1*04:01 | 0.0897 |
            | DPB1*03:01+DPB1*04:01 | 0.0638 |
            | DPB1*04:01+DPB1*14:01 | 0.0629 |
            | DPB1*03:01+DPB1*14:01 | 0.0586 |
            | DPB1*02:01+DPB1*19:01 | 0.0536 |
            | DPB1*04:02+DPB1*14:01 | 0.0349 |
            | DPB1*02:01+DPB1*34:01 | 0.0273 |
            | DPB1*03:01+DPB1*04:02 | 0.0256 |
            | DPB1*04:01+DPB1*04:02 | 0.0243 |
            | DPB1*04:01+DPB1*19:01 | 0.0223 |
            | DPB1*02:01+DPB1*04:02 | 0.0216 |
            | DPB1*03:01+DPB1*19:01 | 0.0204 |
            | DPB1*01:01+DPB1*14:01 | 0.0188 |
            | DPB1*02:01+DPB1*02:01 | 0.0161 |
            | DPB1*03:01+DPB1*03:01 | 0.0159 |
            | DPB1*04:01+DPB1*04:01 | 0.0159 |
            | DPB1*04:02+DPB1*19:01 | 0.013  |
            | DPB1*04:01+DPB1*34:01 | 0.0113 |
            | DPB1*01:01+DPB1*03:01 | 0.0112 |
            | DPB1*03:01+DPB1*34:01 | 0.0104 |
            | DPB1*01:01+DPB1*04:01 | 0.0102 |
        When obtaining the imputed genotypes
        And focusing on the imputed genotype "A*33:01~C*08:02~B*14:02~DRB1*13:02~DQB1*06:04+A*02:05~C*07:01~B*41:01~DRB1*13:02~DQB1*06:04"
        And generating all DPB1 SLUGs with a probability greater than 0.01 for the donor
        Then the expected and observed DPB1 SLUGs are found to be the same
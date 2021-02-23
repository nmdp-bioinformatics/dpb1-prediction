Feature: TCE Groups 
    
    DPB1 alleles belong to one of three t-cell epitope (TCE) groups.

    Permissive and non-permissive matching can arise from these groups.

    Scenario: Generate TCE Groups from SLUGs

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
        And these expected SLUGs
            |   SLUG                    | Probability | Expected TCE Group |
            |	DPB1*02:01+DPB1*14:01	|	0.142	|	2+3	|
            |	DPB1*02:01+DPB1*03:01	|	0.0958	|	3+2	|
            |	DPB1*02:01+DPB1*04:01	|	0.0897	|	3+3	|
            |	DPB1*03:01+DPB1*04:01	|	0.0638	|	2+3	|
            |	DPB1*04:01+DPB1*14:01	|	0.0629	|	3+2	|
            |	DPB1*03:01+DPB1*14:01	|	0.0586	|	2+2	|
            |	DPB1*02:01+DPB1*19:01	|	0.0536	|	3+2	|
            |	DPB1*04:02+DPB1*14:01	|	0.0349	|	3+2	|
            |	DPB1*02:01+DPB1*34:01	|	0.0273	|	3+3	|
            |	DPB1*03:01+DPB1*04:02	|	0.0256	|	2+3	|
            |	DPB1*04:01+DPB1*04:02	|	0.0243	|	3+3	|
            |	DPB1*04:01+DPB1*19:01	|	0.0223	|	3+2	|
            |	DPB1*02:01+DPB1*04:02	|	0.0216	|	3+3	|
            |	DPB1*03:01+DPB1*19:01	|	0.0204	|	2+2	|
            |	DPB1*01:01+DPB1*14:01	|	0.0188	|	3+2	|
            |	DPB1*02:01+DPB1*02:01	|	0.0161	|	3+3	|
            |	DPB1*03:01+DPB1*03:01	|	0.0159	|	2+2	|
            |	DPB1*04:01+DPB1*04:01	|	0.0159	|	3+3	|
            |	DPB1*04:02+DPB1*19:01	|	0.013	|	3+2	|
            |	DPB1*04:01+DPB1*34:01	|	0.0113	|	3+3	|
            |	DPB1*01:01+DPB1*03:01	|	0.0112	|	3+2	|
            |	DPB1*03:01+DPB1*34:01	|	0.0104	|	2+3	|
            |	DPB1*01:01+DPB1*04:01	|	0.0102	|	3+3	|
        And these expected TCE SLUGs
            | TCE SLUG | Probability | 
            | 2+3      | 0.621     |
            | 3+3      | 0.261     |
            | 2+2      | 0.117     |
        When generating the DPB1 SLUGs and TCE groups for the donor
        Then the expected and observed DPB1 SLUGs are found to be the same
        And the expected and observed TCE groups are the same

    Scenario: DPB1 is known (high res)

        Given this set of typings
            | Typing 1 | Typing 2 |
            | A*02:05:01 | A*33:01:01 |
            | C*07:01:01 | C*08:02:01 |
            | B*14:02:01:01 | B*41:01:01:01 |
            | DRB1*13:02:01 | DRB1*13:02:01 |
            | DQB1*06:04:01 | DQB1*06:04:01 |
            | DPB1*02:01:02 | |
        And the subject's population code as 'CAU'
        And these relevant reference haplotype frequencies for that population
        And the resulting donor subject
        And these expected SLUGs
            |   SLUG                    | Probability | Expected TCE Group |
            |	DPB1*02:01+DPB1*02:01	|	1.0	|	3+3	|
        And these expected TCE SLUGs
            | TCE SLUG | Probability | 
            | 3+3      | 1.0     |
        When generating the DPB1 SLUGs and TCE groups for the donor
        Then the expected and observed DPB1 SLUGs are found to be the same
        And the expected and observed TCE groups are the same

    Scenario: One DPB1 is known (intermediate res)

        Given this set of typings
            | Typing 1 | Typing 2 |
            | A*02:05:01 | A*33:01:01 |
            | C*07:01:01 | C*08:02:01 |
            | B*14:02:01:01 | B*41:01:01:01 |
            | DRB1*13:02:01 | DRB1*13:02:01 |
            | DQB1*06:04:01 | DQB1*06:04:01 |
            | DPB1*03:CXD | |
        And the subject's population code as 'CAU'
        And these relevant reference haplotype frequencies for that population
        And the resulting donor subject
        And these expected SLUGs
            |   SLUG                    | Probability | Expected TCE Group |
            |	DPB1*03:01+DPB1*03:01	|	None	|	2+2	|
            |	DPB1*03:01+DPB1*78:01	|	None	|	2+2	|
            |	DPB1*78:01+DPB1*78:01	|	None	|	2+2	|
        And these expected TCE SLUGs
            | TCE SLUG | Probability | 
            | 2+2      | 1.0     |
        When generating the DPB1 SLUGs and TCE groups for the donor
        Then the expected and observed DPB1 SLUGs are found to be the same
        And the expected and observed TCE groups are the same

    Scenario: Both DPB1 are known (intermediate res)

        Given this set of typings
            | Typing 1 | Typing 2 |
            | A*02:05:01 | A*33:01:01 |
            | C*07:01:01 | C*08:02:01 |
            | B*14:02:01:01 | B*41:01:01:01 |
            | DRB1*13:02:01 | DRB1*13:02:01 |
            | DQB1*06:04:01 | DQB1*06:04:01 |
            | DPB1*03:CXD | DPB1*04:KXGS | 
            # https://hml.nmdp.org/mac/api/expand?typing=DPB1*04:KXGS
        And the subject's population code as 'CAU'
        And these relevant reference haplotype frequencies for that population
        And the resulting donor subject
        And these expected SLUGs
            |   SLUG                    | Probability | Expected TCE Group |
            |	DPB1*03:01+DPB1*04:01	|	0.8	    |	2+3	|
            |	DPB1*03:01+DPB1*03:01	|	0.2	    |	2+2	|
        And these expected TCE SLUGs
            | TCE SLUG | Probability | 
            | 2+3      | 0.8      |
            | 2+2      | 0.2      |
        When generating the DPB1 SLUGs and TCE groups for the donor
        Then the expected and observed DPB1 SLUGs are found to be the same
        And the expected and observed TCE groups are the same
Feature: TCE Groups 
    
    Matching between TCE groups is obtained from a service (http://p1haplostats-s1:48080/doc/#!/Matches/getMatches)
    that determines if two DPB1 SLUGs are a match, permissive, or non-permissive (GvH and HvG).

    Scenario: Patient and Donor are missing DPB1

        Given this set of typings
            | Typing 1 | Typing 2 |
            | A*03:01 | A*24:02 |
            | C*04:01 | C*07:02 |
            | B*07:02 | B*40:01 |
            | DRB1*09:YYCS | DRB1*11:YYCT |
            | DQB1*03:01 | DQB1*03:03 |
        And the subject's population code as 'OPI'
        And these relevant reference haplotype frequencies for that population
        And the resulting recipient subject
        And these expected SLUGs
            | SLUG				    | Probability | TCEG |
            | DPB1*04:02+DPB1*05:01 | 0.850     | 3+3  |
            | DPB1*04:01+DPB1*04:02 | 0.0597    | 3+3  |
            | DPB1*02:01+DPB1*04:02 | 0.0579    | 3+3  |
        And these expected TCE SLUGs
            | TCE SLUG | Probability | 
            | 3+3      | 0.987     |
            | 2+3      | 0.01     |
        When generating the DPB1 SLUGs and TCE groups for the recipient
        Then the expected and observed TCE groups are the same

        Given this set of typings
            | Typing 1 | Typing 2 |
            | A*01:01 | A*02:06 | 
            | C*07:ACSZV | C*15:ACHSJ | 
            | B*08:01 | B*51:01 | 
            | DRB1*03:JV | DRB1*14:UADX | 
            | DQB1*02:01 | DQB1*05:03 |
        And the subject's population code as 'CAU'
        And these relevant reference haplotype frequencies for that population
        And the resulting donor subject
        And these expected SLUGs
            | SLUG					| Probability | TCEG |
            | DPB1*02:01+DPB1*04:01 | 0.39219   | 3+3  |
            | DPB1*01:01+DPB1*02:01 | 0.32001   | 3+3  |
            | DPB1*02:01+DPB1*03:01 | 0.08958   | 2+3  |
            | DPB1*02:01+DPB1*04:02 | 0.08485   | 3+3  |
            | DPB1*02:01+DPB1*02:01 | 0.04186   | 3+3  |
            | DPB1*02:01+DPB1*09:01 | 0.016745  | 1+3  |
        And these expected TCE SLUGs
            | TCE SLUG | Probability | 
            | 3+3      | 0.872     |
            | 2+3      | 0.102     |
            | 1+3      | 0.026     |
        When generating the DPB1 SLUGs and TCE groups for the donor
        Then the expected and observed TCE groups are the same

        
        Given these expected match categories and probabilities
            | Match category   | Probability |
            | PERMISSIVE        | 0.861     |
            | HVG_NONPERMISSIVE | 0.127     |
            | GVH_NONPERMISSIVE | 0.012     |
        When generating the DPB1 SLUGs and TCE groups for the recipient/donor
        And obtaining the TCE match categories between the recipient and donor
        Then the expected and observed TCE match categories are the same

    Scenario: Patient has high-level DPB1 already but donor has no DPB1 typed

        Given this set of typings
            | Typing 1 | Typing 2 |
            | A*11:01 | A*29:02 | 
            | C*15:02 | C*16:01 | 
            | B*51:01 | B*44:03 | 
            | DRB1*04:01 | DRB1*07:01 | 
            | DQB1*03:02 | DQB1*02:01 | 
            | DPB1*04:01 | DPB1*03:01 |
        And the subject's population code as 'CAU'
        And these relevant reference haplotype frequencies for that population
        And the resulting recipient subject
        And these expected TCE SLUGs
            | TCE SLUG | Probability | 
            | 2+3      | 1         |
        When generating the DPB1 SLUGs and TCE groups for the recipient
        Then the expected and observed TCE groups are the same

        Given this set of typings
            | Typing 1 | Typing 2 |
            | A*11:DHVB | A*29:DHVF |
            | C*15:BDJR | C*16:AB |
            | B*44:CYY | B*51:EKEK |
            | DRB1*04:01 | DRB1*07:01 |
            | DQB1*02:01 | DQB1*03:02 |
        And the subject's population code as 'NAMER'
        And these relevant reference haplotype frequencies for that population
        And the resulting donor subject
        And these expected TCE SLUGs
            | TCE SLUG | Probability | 
            | 3+3      | 0.846     |
            | 2+3      | 0.134     |
            | 1+3      | 0.015     |
        When generating the DPB1 SLUGs and TCE groups for the donor
        Then the expected and observed TCE groups are the same

        Given these expected match categories and probabilities
            | Match category   | Probability |
            | GVH_NONPERMISSIVE | 0.846     |
            | PERMISSIVE        | 0.137     |
            | HVG_NONPERMISSIVE | 0.0167    |
        When generating the DPB1 SLUGs and TCE groups for the recipient/donor
        And obtaining the TCE match categories between the recipient and donor
        Then the expected and observed TCE match categories are the same

    Scenario: Patient has one known DPB1 allele but donor has no DPB1 typed

        Given this set of typings
            | Typing 1 | Typing 2 |
            | A*11:DHVB | A*29:DHVF |
            | C*15:BDJR | C*16:AB |
            | B*44:CYY | B*51:EKEK |
            | DRB1*04:01 | DRB1*07:01 |
            | DQB1*02:01 | DQB1*03:02 |
            | DPB1*04:01 |  |
        And the subject's population code as 'CAU'
        And these relevant reference haplotype frequencies for that population
        And the resulting recipient subject
        And these expected TCE SLUGs
            | TCE SLUG | Probability | 
            | 3+3      | 1.0     |
        When generating the DPB1 SLUGs and TCE groups for the recipient
        Then the expected and observed TCE groups are the same

        Given this set of typings
            | Typing 1 | Typing 2 |
            | A*11:DHVB | A*29:DHVF |
            | C*15:BDJR | C*16:AB |
            | B*44:CYY | B*51:EKEK |
            | DRB1*04:01 | DRB1*07:01 |
            | DQB1*02:01 | DQB1*03:02 |
        And the subject's population code as 'NAMER'
        And these relevant reference haplotype frequencies for that population
        And the resulting donor subject
        And these expected TCE SLUGs
            | TCE SLUG | Probability | 
            | 3+3      | 0.846     |
            | 2+3      | 0.134     |
            | 1+3      | 0.015     |
        When generating the DPB1 SLUGs and TCE groups for the donor
        Then the expected and observed TCE groups are the same

        Given these expected match categories and probabilities
            | Match category    | Probability |
            | PERMISSIVE        | 0.846     |
            | HVG_NONPERMISSIVE | 0.154     |
        When generating the DPB1 SLUGs and TCE groups for the recipient/donor
        And obtaining the TCE match categories between the recipient and donor
        Then the expected and observed TCE match categories are the same
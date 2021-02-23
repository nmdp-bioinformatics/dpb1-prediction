Feature: Classify TCE group matching 
    
    Matching between TCE groups is obtained from a service (http://p1haplostats-s1:48080/doc/#!/Matches/getMatches)
    that determines if two DPB1 SLUGs are a match, permissive, or non-permissive (GvH and HvG).

    Scenario: 0+0 Recipient TCE Groups

        Given these TCE group pairs and expected match categories
            | Recipient TCE | Donor TCE | Match Categories  |
            | 0+0 | 0+0 | PERMISSIVE |
            | 0+0 | 0+1 | GVH_NONPERMISSIVE |
            | 0+0 | 0+2 | GVH_NONPERMISSIVE |
            | 0+0 | 0+3 | GVH_NONPERMISSIVE |
            | 0+0 | 1+1 | GVH_NONPERMISSIVE |
            | 0+0 | 1+2 | GVH_NONPERMISSIVE |
            | 0+0 | 1+3 | GVH_NONPERMISSIVE |
            | 0+0 | 2+2 | GVH_NONPERMISSIVE |
            | 0+0 | 2+3 | GVH_NONPERMISSIVE |
            | 0+0 | 3+3 | GVH_NONPERMISSIVE |
        When classifying their match categories
        Then their expected and classified categories are the same
    
    Scenario: 0+1 Recipient TCE Groups

        Given these TCE group pairs and expected match categories
            | Recipient TCE | Donor TCE | Match Categories  |
            | 0+1 | 0+0 | HVG_NONPERMISSIVE |
            | 0+1 | 0+1 | PERMISSIVE |
            | 0+1 | 0+2 | GVH_NONPERMISSIVE |
            | 0+1 | 0+3 | GVH_NONPERMISSIVE |
            | 0+1 | 1+1 | PERMISSIVE |
            | 0+1 | 1+2 | PERMISSIVE |
            | 0+1 | 1+3 | PERMISSIVE |
            | 0+1 | 2+2 | GVH_NONPERMISSIVE |
            | 0+1 | 2+3 | GVH_NONPERMISSIVE |
            | 0+1 | 3+3 | GVH_NONPERMISSIVE |
        When classifying their match categories
        Then their expected and classified categories are the same

    Scenario: 0+2 Recipient TCE Groups

        Given these TCE group pairs and expected match categories
            | Recipient TCE | Donor TCE | Match Categories  |
            | 0+2 | 0+0 | HVG_NONPERMISSIVE |
            | 0+2 | 0+1 | HVG_NONPERMISSIVE |
            | 0+2 | 0+2 | PERMISSIVE |
            | 0+2 | 0+3 | GVH_NONPERMISSIVE |
            | 0+2 | 1+1 | HVG_NONPERMISSIVE |
            | 0+2 | 1+2 | HVG_NONPERMISSIVE |
            | 0+2 | 1+3 | HVG_NONPERMISSIVE |
            | 0+2 | 2+2 | PERMISSIVE |
            | 0+2 | 2+3 | PERMISSIVE |
            | 0+2 | 3+3 | GVH_NONPERMISSIVE |
        When classifying their match categories
        Then their expected and classified categories are the same

    Scenario: 0+3 Recipient TCE Groups

        Given these TCE group pairs and expected match categories
            | Recipient TCE | Donor TCE | Match Categories  |
            | 0+3 | 0+0 | HVG_NONPERMISSIVE |
            | 0+3 | 0+1 | HVG_NONPERMISSIVE |
            | 0+3 | 0+2 | HVG_NONPERMISSIVE |
            | 0+3 | 0+3 | PERMISSIVE |
            | 0+3 | 1+1 | HVG_NONPERMISSIVE |
            | 0+3 | 1+2 | HVG_NONPERMISSIVE |
            | 0+3 | 1+3 | HVG_NONPERMISSIVE |
            | 0+3 | 2+2 | HVG_NONPERMISSIVE |
            | 0+3 | 2+3 | HVG_NONPERMISSIVE |
            | 0+3 | 3+3 | PERMISSIVE |
        When classifying their match categories
        Then their expected and classified categories are the same

    Scenario: 1+1 Recipient TCE Groups

        Given these TCE group pairs and expected match categories
            | Recipient TCE | Donor TCE | Match Categories  |
            | 1+1 | 0+0 | HVG_NONPERMISSIVE |
            | 1+1 | 0+1 | PERMISSIVE |
            | 1+1 | 0+2 | GVH_NONPERMISSIVE |
            | 1+1 | 0+3 | GVH_NONPERMISSIVE |
            | 1+1 | 1+1 | PERMISSIVE |
            | 1+1 | 1+2 | PERMISSIVE |
            | 1+1 | 1+3 | PERMISSIVE |
            | 1+1 | 2+2 | GVH_NONPERMISSIVE |
            | 1+1 | 2+3 | GVH_NONPERMISSIVE |
            | 1+1 | 3+3 | GVH_NONPERMISSIVE |
        When classifying their match categories
        Then their expected and classified categories are the same

    Scenario: 1+2 Recipient TCE Groups

        Given these TCE group pairs and expected match categories
            | Recipient TCE | Donor TCE | Match Categories  |
            | 1+2 | 0+0 | HVG_NONPERMISSIVE |
            | 1+2 | 0+1 | PERMISSIVE |
            | 1+2 | 0+2 | GVH_NONPERMISSIVE |
            | 1+2 | 0+3 | GVH_NONPERMISSIVE |
            | 1+2 | 1+1 | PERMISSIVE |
            | 1+2 | 1+2 | PERMISSIVE |
            | 1+2 | 1+3 | PERMISSIVE |
            | 1+2 | 2+2 | GVH_NONPERMISSIVE |
            | 1+2 | 2+3 | GVH_NONPERMISSIVE |
            | 1+2 | 3+3 | GVH_NONPERMISSIVE |
        When classifying their match categories
        Then their expected and classified categories are the same

    Scenario: 1+3 Recipient TCE Groups

        Given these TCE group pairs and expected match categories
            | Recipient TCE | Donor TCE | Match Categories  |
            | 1+3 | 0+0 | HVG_NONPERMISSIVE |
            | 1+3 | 0+1 | PERMISSIVE |
            | 1+3 | 0+2 | GVH_NONPERMISSIVE |
            | 1+3 | 0+3 | GVH_NONPERMISSIVE |
            | 1+3 | 1+1 | PERMISSIVE |
            | 1+3 | 1+2 | PERMISSIVE |
            | 1+3 | 1+3 | PERMISSIVE |
            | 1+3 | 2+2 | GVH_NONPERMISSIVE |
            | 1+3 | 2+3 | GVH_NONPERMISSIVE |
            | 1+3 | 3+3 | GVH_NONPERMISSIVE |
        When classifying their match categories
        Then their expected and classified categories are the same

    Scenario: 2+2 Recipient TCE Groups

        Given these TCE group pairs and expected match categories
            | Recipient TCE | Donor TCE | Match Categories  |
            | 2+2 | 0+0 | HVG_NONPERMISSIVE |
            | 2+2 | 0+1 | HVG_NONPERMISSIVE |
            | 2+2 | 0+2 | PERMISSIVE |
            | 2+2 | 0+3 | GVH_NONPERMISSIVE |
            | 2+2 | 1+1 | HVG_NONPERMISSIVE |
            | 2+2 | 1+2 | HVG_NONPERMISSIVE |
            | 2+2 | 1+3 | HVG_NONPERMISSIVE |
            | 2+2 | 2+2 | PERMISSIVE |
            | 2+2 | 2+3 | PERMISSIVE |
            | 2+2 | 3+3 | GVH_NONPERMISSIVE |
        When classifying their match categories
        Then their expected and classified categories are the same

    Scenario: 2+3 Recipient TCE Groups

        Given these TCE group pairs and expected match categories
            | Recipient TCE | Donor TCE | Match Categories  |
            | 2+3 | 0+0 | HVG_NONPERMISSIVE |
            | 2+3 | 0+1 | HVG_NONPERMISSIVE |
            | 2+3 | 0+2 | PERMISSIVE |
            | 2+3 | 0+3 | GVH_NONPERMISSIVE |
            | 2+3 | 1+1 | HVG_NONPERMISSIVE |
            | 2+3 | 1+2 | HVG_NONPERMISSIVE |
            | 2+3 | 1+3 | HVG_NONPERMISSIVE |
            | 2+3 | 2+2 | PERMISSIVE |
            | 2+3 | 2+3 | PERMISSIVE |
            | 2+3 | 3+3 | GVH_NONPERMISSIVE |
        When classifying their match categories
        Then their expected and classified categories are the same

    Scenario: 3+3 Recipient TCE Groups

        Given these TCE group pairs and expected match categories
            | Recipient TCE | Donor TCE | Match Categories  |
            | 3+3 | 0+0 | HVG_NONPERMISSIVE |
            | 3+3 | 0+1 | HVG_NONPERMISSIVE |
            | 3+3 | 0+2 | HVG_NONPERMISSIVE |
            | 3+3 | 0+3 | PERMISSIVE |
            | 3+3 | 1+1 | HVG_NONPERMISSIVE |
            | 3+3 | 1+2 | HVG_NONPERMISSIVE |
            | 3+3 | 1+3 | HVG_NONPERMISSIVE |
            | 3+3 | 2+2 | HVG_NONPERMISSIVE |
            | 3+3 | 2+3 | HVG_NONPERMISSIVE |
            | 3+3 | 3+3 | PERMISSIVE |
        When classifying their match categories
        Then their expected and classified categories are the same
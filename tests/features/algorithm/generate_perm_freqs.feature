Feature: Generating DPB1 Permissiveness Frequencies

    @full_service
    Scenario Outline:
        Given a row (#<Row Index>) in "validation/dataframes/curated/df_haplogic.csv"
        When generating the predicted permissive frequencies
        Then the expected <Permissive Frequency> and predicted frequencies are the same

        Examples:
            | Row Index | Permissive Frequency |
            | 0 | 0.171 |
            | 1 | 0.98  |
            | 2 | 0.664 |
            | 3 | 1.0 |            
            | 4 | 0.137 |
            | 5 | 0.814 |
            | 6 | 0.532 |
            | 7 | 0.532 |
            | 8 | 0.656 |
            | 9 | 0.864 |
            | 10 | 0.761  |
            | 11 | 0.761  |
            | 12 | 0.741  |
            | 13 | 0.0623 |
            | 14 | 0.57 |
            | 15 | 0.852 |
            | 16 | 0.49 |
            | 17 | 0.498 |
            | 18 | 0.526 |
            | 19 | 0.133 |
            | 20 | 0.185 |
            | 21 | 0.263 |
            | 22 | 0.308 |
            | 23 | 0.717 |
            | 24 | 0.58 |
            | 25 | 0.543 |
            | 26 | 0.764 |
            | 27 | 0.446 |
            | 28 | 0.329 |
            | 29 | 0.781 |
            | 30 | 0.887 |
            | 31 | 0.807 |
            | 32 | 0.641 |
            | 33 | 0.823 |
            | 34 | 0.823 |
            | 35 | 0.661 |
            | 36 | 0.571 |
            | 37 | 0.435 |
            | 38 | 0.249 |
            | 39 | 0.245 |
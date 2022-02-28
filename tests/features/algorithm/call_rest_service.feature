@rest_service
Feature: Call REST Service

    Scenario: Imputation input - Haplotype not in frequencies

        Given an input payload as
            """
            {"subjects" :
            [{"id": "123456789",
                "imputation":[{"haplotype1": "A*99:01~C*07:01~B*08:01~DRB1*03:01~DQB1*02:01",
                                "population1": "CAU",
                                "frequency1": "0.0598117681949288",
                                "haplotype2": "A*99:01~B*08:01~C*07:01~DRB1*03:01~DQB1*02:01",
                                "population2": "CAU",
                                "frequency2": "0.0598117681949288"}]}]}
            """
        When submitting the subject's information to and retrieving results from 'dpb1-imputation/tce-groups'
        Then the output is found to be
            """
                {
                    "data": [
                        {
                         "id" : "123456789",
                         "dpb1_tce_groups": [],
                         "dpb1_tce_genotypes": [],
                         "dpb1_genotypes": [],
                         "non_dpb1_haplotypes" : ["A*99:01~C*07:01~B*08:01~DRB1*03:01~DQB1*02:01", 
                                                 "A*99:01~B*08:01~C*07:01~DRB1*03:01~DQB1*02:01"]
                        }
                    ]
                }
            """ 

    Scenario: TCE Groups

        Given an input payload as
            """
            {"population": "CAU",
            "typing": "A*02:05:01+A*33:01:01^C*07:01:01+C*08:02:01^B*14:02:01:01+B*41:01:01:01^DRB1*13:02:01+DRB1*13:02:01^DQB1*06:04:01+DQB1*06:04:01"}
            """
        When submitting the subject's information to and retrieving results from 'dpb1-prediction/tce-groups'
        Then the output is found to be
            """
                {
                    "data": {
                        "dpb1_tce_groups": [
                        {
                            "tce_group": "2",
                            "probability": 0.7378272033563958
                        },
                        {
                            "tce_group": "3",
                            "probability": 0.2612652222015426
                        }
                        ],
                        "dpb1_tce_genotypes": [
                        {
                            "tce_groups": "2+3",
                            "probability": 0.6209973820941405
                        },
                        {
                            "tce_groups": "3+3",
                            "probability": 0.2612652222015426
                        },
                        {
                            "tce_groups": "2+2",
                            "probability": 0.11682982126225543
                        }
                        ],
                        "dpb1_genotypes": [
                        {
                            "genotype": "DPB1*02:01+DPB1*14:01",
                            "tce_groups": "2+3",
                            "probability": 0.14232503675544764
                        },
                        {
                            "genotype": "DPB1*02:01+DPB1*03:01",
                            "tce_groups": "2+3",
                            "probability": 0.09583364795525025
                        },
                        {
                            "genotype": "DPB1*02:01+DPB1*04:01",
                            "tce_groups": "3+3",
                            "probability": 0.08969578509174583
                        },
                        {
                            "genotype": "DPB1*03:01+DPB1*04:01",
                            "tce_groups": "2+3",
                            "probability": 0.06383042807255217
                        },
                        {
                            "genotype": "DPB1*04:01+DPB1*14:01",
                            "tce_groups": "2+3",
                            "probability": 0.06293940944525436
                        },
                        {
                            "genotype": "DPB1*03:01+DPB1*14:01",
                            "tce_groups": "2+2",
                            "probability": 0.058591329345672405
                        },
                        {
                            "genotype": "DPB1*02:01+DPB1*19:01",
                            "tce_groups": "2+3",
                            "probability": 0.0535651878821646
                        },
                        {
                            "genotype": "DPB1*04:02+DPB1*14:01",
                            "tce_groups": "2+3",
                            "probability": 0.03491395758113173
                        },
                        {
                            "genotype": "DPB1*02:01+DPB1*34:01",
                            "tce_groups": "3+3",
                            "probability": 0.027275152649170686
                        },
                        {
                            "genotype": "DPB1*03:01+DPB1*04:02",
                            "tce_groups": "2+3",
                            "probability": 0.02555197447165764
                        },
                        {
                            "genotype": "DPB1*04:01+DPB1*04:02",
                            "tce_groups": "3+3",
                            "probability": 0.024266537146250593
                        },
                        {
                            "genotype": "DPB1*04:01+DPB1*19:01",
                            "tce_groups": "2+3",
                            "probability": 0.02225095277208434
                        },
                        {
                            "genotype": "DPB1*02:01+DPB1*04:02",
                            "tce_groups": "3+3",
                            "probability": 0.02160191003207413
                        },
                        {
                            "genotype": "DPB1*03:01+DPB1*19:01",
                            "tce_groups": "2+2",
                            "probability": 0.020424548488760515
                        },
                        {
                            "genotype": "DPB1*01:01+DPB1*14:01",
                            "tce_groups": "2+3",
                            "probability": 0.018799812024928336
                        },
                        {
                            "genotype": "DPB1*02:01+DPB1*02:01",
                            "tce_groups": "3+3",
                            "probability": 0.016067735882560497
                        },
                        {
                            "genotype": "DPB1*03:01+DPB1*03:01",
                            "tce_groups": "2+2",
                            "probability": 0.01593469661939092
                        },
                        {
                            "genotype": "DPB1*04:01+DPB1*04:01",
                            "tce_groups": "3+3",
                            "probability": 0.01585719624159696
                        },
                        {
                            "genotype": "DPB1*04:02+DPB1*19:01",
                            "tce_groups": "2+3",
                            "probability": 0.013003315595921513
                        },
                        {
                            "genotype": "DPB1*04:01+DPB1*34:01",
                            "tce_groups": "3+3",
                            "probability": 0.011330085031777973
                        },
                        {
                            "genotype": "DPB1*01:01+DPB1*03:01",
                            "tce_groups": "2+3",
                            "probability": 0.011193336842481581
                        },
                        {
                            "genotype": "DPB1*03:01+DPB1*34:01",
                            "tce_groups": "2+3",
                            "probability": 0.010400088188747329
                        },
                        {
                            "genotype": "DPB1*01:01+DPB1*04:01",
                            "tce_groups": "3+3",
                            "probability": 0.010224592952021624
                        }
                        ]
                    }
                    }
            """

    Scenario: No haplotypes, one high-res DPB1 SLG

        Given an input payload as
            """
            {"population": "CAU",
            "typing": "A*24:03+A*33:03^B*51:06+B*58:01^C*03:02+C*12:04^DQB1*03:02+DQB1*05:01^DRB1*04:03+DRB1*15:02^DPB1*02:01"}
            """
        When submitting the subject's information to and retrieving results from 'dpb1-prediction/tce-groups'
        Then the output is found to be
            """
                {
                    "data": {
                        "dpb1_tce_groups": [
                        {
                            "tce_group": "3",
                            "probability": 1
                        }
                        ],
                        "dpb1_tce_genotypes": [
                        {
                            "tce_groups": "3+3",
                            "probability": 1
                        }
                        ],
                        "dpb1_genotypes": [
                        {
                            "genotype": "DPB1*02:01+DPB1*02:01",
                            "tce_groups": "3+3"
                        }
                        ]
                    }
                    }
            """
    
    Scenario: No haplotypes, one lower-res DPB1 SLG (unambiguous TCE)

        Given an input payload as
            """
            {"population": "CAU",
            "typing": "A*24:03+A*33:03^B*51:06+B*58:01^C*03:02+C*12:04^DQB1*03:02+DQB1*05:01^DRB1*04:03+DRB1*15:02^DPB1*03:CXD"}
            """
        When submitting the subject's information to and retrieving results from 'dpb1-prediction/tce-groups'
        Then the output is found to be
            """
                {
                    "data": {
                        "dpb1_tce_groups": [
                        {
                            "tce_group": "2",
                            "probability": 1
                        }
                        ],
                        "dpb1_tce_genotypes": [
                        {
                            "tce_groups": "2+2",
                            "probability": 1
                        }
                        ],
                        "dpb1_genotypes": [
                        {
                            "genotype": "DPB1*03:01+DPB1*03:01",
                            "tce_groups": "2+2"
                        },
                        {
                            "genotype": "DPB1*03:01+DPB1*78:01",
                            "tce_groups": "2+2"
                        },
                        {
                            "genotype": "DPB1*78:01+DPB1*78:01",
                            "tce_groups": "2+2"
                        }
                        ]
                    }
                    }
            """

    Scenario: No imputation, one lower-res DPB1 SLG (ambiguous TCE)

        Given an input payload as
            """
            {"population": "CAU",
            "typing": "A*24:03+A*33:03^B*51:06+B*58:01^C*03:02+C*12:04^DQB1*03:02+DQB1*05:01^DRB1*04:03+DRB1*15:02^DPB1*04:KXGS"}
            """
        When submitting the subject's information to and retrieving results from 'dpb1-prediction/tce-groups'
        Then the output is found to be

            """
                {
                    "data": {
                        "dpb1_tce_groups": [
                        {
                            "tce_group": "2"
                        },
                        {
                            "tce_group": "3"
                        }
                        ],
                        "dpb1_tce_genotypes": [
                        {
                            "tce_groups": "2+2"
                        },
                        {
                            "tce_groups": "2+3"
                        },
                        {
                            "tce_groups": "3+3"
                        }
                        ],
                        "dpb1_genotypes": [
                        {
                            "genotype": "DPB1*03:01+DPB1*03:01",
                            "tce_groups": "2+2"
                        },
                        {
                            "genotype": "DPB1*03:01+DPB1*04:01",
                            "tce_groups": "2+3"
                        },
                        {
                            "genotype": "DPB1*03:01+DPB1*111:01",
                            "tce_groups": "2+2"
                        },
                        {
                            "genotype": "DPB1*03:01+DPB1*121:01",
                            "tce_groups": "2+3"
                        },
                        {
                            "genotype": "DPB1*04:01+DPB1*03:01",
                            "tce_groups": "2+3"
                        },
                        {
                            "genotype": "DPB1*04:01+DPB1*04:01",
                            "tce_groups": "3+3"
                        },
                        {
                            "genotype": "DPB1*04:01+DPB1*111:01",
                            "tce_groups": "2+3"
                        },
                        {
                            "genotype": "DPB1*04:01+DPB1*121:01",
                            "tce_groups": "3+3"
                        },
                        {
                            "genotype": "DPB1*111:01+DPB1*111:01",
                            "tce_groups": "2+2"
                        },
                        {
                            "genotype": "DPB1*111:01+DPB1*121:01",
                            "tce_groups": "2+3"
                        },
                        {
                            "genotype": "DPB1*121:01+DPB1*121:01",
                            "tce_groups": "3+3"
                        }
                        ]
                    }
                    }
            """

    Scenario: No imputation, >1 high-res SLG

        Given an input payload as
            """
            {"population": "CAU",
            "typing": "A*02:05:01+A*32:01:01^C*07:01:01+C*08:02:01^B*14:02:01:01+B*41:01:01:01^DRB1*13:02:01+DRB1*13:02:01^DQB1*06:04:01+DQB1*06:04:01^DPB1*02:01|DPB1*03:01"}
            """
        When submitting the subject's information to and retrieving results from 'dpb1-prediction/tce-groups'
        Then the output is found to be
            """
                {
                    "data": {
                        "dpb1_tce_groups": [
                        {
                            "tce_group": "2"
                        },
                        {
                            "tce_group": "3"
                        }
                        ],
                        "dpb1_tce_genotypes": [
                        {
                            "tce_groups": "2+2"
                        },
                        {
                            "tce_groups": "3+3"
                        }
                        ],
                        "dpb1_genotypes": [
                        {
                            "genotype": "DPB1*02:01+DPB1*02:01",
                            "tce_groups": "3+3"
                        },
                        {
                            "genotype": "DPB1*03:01+DPB1*03:01",
                            "tce_groups": "2+2"
                        }
                        ],
                        "non_dpb1_haplotypes": [
                        "A*32:01~C*08:02~B*14:02~DRB1*13:02~DRB3*03:01~DQB1*06:04"
                        ]
                    }
                    }
            """

    Scenario: No imputation, >1 lower-res SLG

        Given an input payload as
            """
            {"population": "CAU",
            "typing": "A*02:05:01+A*32:01:01^C*07:01:01+C*08:02:01^B*14:02:01:01+B*41:01:01:01^DRB1*13:02:01+DRB1*13:02:01^DQB1*06:04:01+DQB1*06:04:01^DPB1*02:01"}
            """
        When submitting the subject's information to and retrieving results from 'dpb1-prediction/tce-groups'
        Then the output is found to be
            """
                {
                    "data": {
                        "dpb1_tce_groups": [
                        {
                            "tce_group": "3",
                            "probability": 1
                        }
                        ],
                        "dpb1_tce_genotypes": [
                        {
                            "tce_groups": "3+3",
                            "probability": 1
                        }
                        ],
                        "dpb1_genotypes": [
                        {
                            "genotype": "DPB1*02:01+DPB1*02:01",
                            "tce_groups": "3+3"
                        }
                        ]
                    }
                    }
            """

    Scenario: TCE Groups with more complex GL string and known, high-res DPB1 allele

        Given an input payload as
            """
            {"population": "CAU",
            "typing": "A*01:01+A*01:01^B*07:02+B*07:02^C*04:01+C*07:02|C*07:02+C*12:03|C*07:01+C*07:02|C*06:02+C*07:02|C*03:03+C*07:02|C*07:02+C*07:02|C*07:02+C*15:02|C*07:02+C*07:04^DQB1*05:01+DQB1*05:01|DQB1*05:01+DQB1*05:04^DRB1*01:01+DRB1*01:01^DPB1*01:01"}
            """
        When submitting the subject's information to and retrieving results from 'dpb1-prediction/tce-groups'
        Then the output is found to be
            """
                {
                    "data": {
                        "dpb1_tce_groups": [
                        {
                            "tce_group": "3",
                            "probability": 1
                        }
                        ],
                        "dpb1_tce_genotypes": [
                        {
                            "tce_groups": "3+3",
                            "probability": 1
                        }
                        ],
                        "dpb1_genotypes": [
                        {
                            "genotype": "DPB1*01:01+DPB1*01:01",
                            "tce_groups": "3+3"
                        }
                        ]
                    }
                    }
            """
    
    Scenario: No imputation, TCE Matches (Unambiguous DPB1 and ambiguous DPB1)

        Given an input payload as
            """
                {
                    "subject_pairs": [
                        {
                        "donor": {
                            "typing": "A*24:02+A*02:01^C*04:01+C*05:01^B*35:17+B*44:02^DRB1*08:02+DRB1*04:01^DQB1*03:01+DQB1*04:02^DPB1*04:01+DPB1*16:01",
                            "population": "CAU"
                        },
                        "recipient": {
                            "typing": "A*02:01+A*24:02^C*04:01+C*05:01^B*35:17+B*44:02^DRB1*04:01+DRB1*08:02^DQB1*03:01+DQB1*04:02^DPB1*04:CBV+DPB1*04:BDVU",
                            "population": "CAU"
                        }
                        }
                    ]
                }
            """
        When submitting the subject's information to and retrieving results from 'dpb1-prediction/tce-matches'
        Then the output is found to be
            """
                {
                    "data": [
                        {
                        "tce_match_grades": [
                            {
                            "category": "PERMISSIVE",
                            "probability": 1
                            }
                        ],
                        "donor": {
                            "dpb1_tce_groups": [
                            {
                                "tce_group": "3",
                                "probability": 1
                            }
                            ],
                            "dpb1_tce_genotypes": [
                            {
                                "tce_groups": "3+3",
                                "probability": 1
                            }
                            ],
                            "dpb1_genotypes": [
                            {
                                "genotype": "DPB1*04:01+DPB1*16:01",
                                "tce_groups": "3+3"
                            }
                            ]
                        },
                        "recipient": {
                            "dpb1_tce_groups": [
                            {
                                "tce_group": "3",
                                "probability": 1
                            }
                            ],
                            "dpb1_tce_genotypes": [
                            {
                                "tce_groups": "3+3",
                                "probability": 1
                            }
                            ],
                            "dpb1_genotypes": [
                            {
                                "genotype": "DPB1*04:01+DPB1*04:02",
                                "tce_groups": "3+3"
                            },
                            {
                                "genotype": "DPB1*04:01+DPB1*51:01",
                                "tce_groups": "3+3"
                            },
                            {
                                "genotype": "DPB1*04:02+DPB1*23:01",
                                "tce_groups": "3+3"
                            },
                            {
                                "genotype": "DPB1*23:01+DPB1*51:01",
                                "tce_groups": "3+3"
                            }
                            ]
                        }
                        }
                    ]
                    }
            """

    
    Scenario: No imputation, TCE Matches (Unambiguous DPB1 and ambiguous DPB1)

        Given an input payload as
            """
            {
            "subject_pairs": [
                {
                "donor": {
                    "typing": "A*02:07+A*11:01^B*38:02+B*46:01^C*01:02+C*07:02^DRB1*11:06+DRB1*14:01^DQB1*03:01+DQB1*05:02^DPB1*04:01+DPB1*13:01",
                    "population": "CAU"
                },
                "recipient": {
                    "typing": "A*02:07+A*11:01^B*38:02/B*38:15+B*46:01^C*01:02+C*07:409^DRB1*11:06+DRB1*14:01^DQB1*03:01+DQB1*05:02^DPB1*02:02+DPB1*04:01/DPB1*216:01N",
                    "population": "CAU"
                }
                }
            ]
            }
            """
        When submitting the subject's information to and retrieving results from 'dpb1-prediction/tce-matches'
        Then the output is found to be
            """
            {
                    "data": [
                        {
                        "tce_match_grades": [
                            {
                            "category": "PERMISSIVE",
                            "probability": 1
                            }
                        ],
                        "donor": {
                            "dpb1_tce_groups": [
                            {
                                "tce_group": "3",
                                "probability": 1
                            }
                            ],
                            "dpb1_tce_genotypes": [
                            {
                                "tce_groups": "3+3",
                                "probability": 1
                            }
                            ],
                            "dpb1_genotypes": [
                            {
                                "genotype": "DPB1*04:01+DPB1*13:01",
                                "tce_groups": "3+3"
                            }
                            ]
                        },
                        "recipient": {
                            "dpb1_tce_groups": [
                            {
                                "tce_group": "3"
                            }
                            ],
                            "dpb1_tce_genotypes": [
                            {
                                "tce_groups": "0+3"
                            },
                            {
                                "tce_groups": "3+3"
                            }
                            ],
                            "dpb1_genotypes": [
                            {
                                "genotype": "DPB1*02:02+DPB1*04:01",
                                "tce_groups": "3+3"
                            },
                            {
                                "genotype": "DPB1*02:02+DPB1*216:01N",
                                "tce_groups": "0+3"
                            }
                            ]
                        }
                        }
                    ]
                    }
            """

    Scenario: Imputation input

        Given an input payload as
            """
            {
                "subjects": [
                    {
                    "id": "147803795",
                    "imputation": [
                        {
                        "haplotype1": "A*01:01~C*03:03~B*07:02~DRB1*01:01~DQB1*05:01",
                        "population1": "CAU",
                        "frequency1": 0.0598117681949288,
                        "haplotype2": "A*01:01~C*07:01~B*08:01~DRB1*03:01~DQB1*02:01~DRB3*01:01",
                        "population2": "CAU",
                        "frequency2": 0.0598117681949288
                        }
                    ]
                    }
                ]
            }
            """
        When submitting the subject's information to and retrieving results from 'dpb1-imputation/tce-groups'
        Then the output is found to be
            """
                {
                    "data": [
                        {
                        "id": "147803795",
                        "dpb1_tce_groups": [
                            {
                            "tce_group": "2",
                            "probability": 0.4993523191926803
                            },
                            {
                            "tce_group": "3",
                            "probability": 0.47300346872390214
                            },
                            {
                            "tce_group": "1",
                            "probability": 0.027644212083417476
                            }
                        ],
                        "dpb1_tce_genotypes": [
                            {
                            "tce_groups": "2+3",
                            "probability": 0.47361064367068606
                            },
                            {
                            "tce_groups": "3+3",
                            "probability": 0.47300346872390214
                            },
                            {
                            "tce_groups": "2+2",
                            "probability": 0.02574167552199426
                            },
                            {
                            "tce_groups": "1+3",
                            "probability": 0.016128373040307373
                            },
                            {
                            "tce_groups": "1+2",
                            "probability": 0.011515839043110102
                            }
                        ],
                        "dpb1_genotypes": [
                            {
                            "genotype": "DPB1*01:01+DPB1*04:01",
                            "tce_groups": "3+3",
                            "probability": 0.2457145099008231
                            },
                            {
                            "genotype": "DPB1*01:01+DPB1*03:01",
                            "tce_groups": "2+3",
                            "probability": 0.1997197454400491
                            },
                            {
                            "genotype": "DPB1*03:01+DPB1*04:01",
                            "tce_groups": "2+3",
                            "probability": 0.17581646051393535
                            },
                            {
                            "genotype": "DPB1*01:01+DPB1*01:01",
                            "tce_groups": "3+3",
                            "probability": 0.10036357043819456
                            },
                            {
                            "genotype": "DPB1*01:01+DPB1*04:02",
                            "tce_groups": "3+3",
                            "probability": 0.053507286963773694
                            },
                            {
                            "genotype": "DPB1*01:01+DPB1*02:01",
                            "tce_groups": "3+3",
                            "probability": 0.05236559419976468
                            },
                            {
                            "genotype": "DPB1*03:01+DPB1*04:02",
                            "tce_groups": "2+3",
                            "probability": 0.038123427673232076
                            },
                            {
                            "genotype": "DPB1*02:01+DPB1*03:01",
                            "tce_groups": "2+3",
                            "probability": 0.037476279773076174
                            },
                            {
                            "genotype": "DPB1*03:01+DPB1*03:01",
                            "tce_groups": "2+2",
                            "probability": 0.020062316890094654
                            },
                            {
                            "genotype": "DPB1*01:01+DPB1*09:01",
                            "tce_groups": "1+3",
                            "probability": 0.010510183918713717
                            }
                        ]
                        }
                    ]
                    }
            """

    Scenario: Ambiguous DPB1 GLString (One DPB1)

        Given an input payload as
            """
            {"population": "CAU",
            "typing": "A*02:05:01+A*33:01:01^C*07:01:01+C*08:02:01^B*14:02:01:01+B*41:01:01:01^DRB1*13:02:01+DRB1*13:02:01^DQB1*06:04:01+DQB1*06:04:01^DPB1*04:01/DPB1*677:01"}
            """
        When submitting the subject's information to and retrieving results from 'dpb1-prediction/tce-groups'
        Then the output is found to be
            """
                {
                    "data": {
                        "dpb1_tce_groups": [
                        {
                            "tce_group": "3",
                            "probability": 1
                        }
                        ],
                        "dpb1_tce_genotypes": [
                        {
                            "tce_groups": "3+3",
                            "probability": 1
                        }
                        ],
                        "dpb1_genotypes": [
                        {
                            "genotype": "DPB1*04:01+DPB1*04:01",
                            "tce_groups": "3+3"
                        },
                        {
                            "genotype": "DPB1*04:01+DPB1*677:01",
                            "tce_groups": "3+3"
                        },
                        {
                            "genotype": "DPB1*677:01+DPB1*677:01",
                            "tce_groups": "3+3"
                        }
                        ]
                    }
                    }
            """

    Scenario: Ambiguous DPB1 GLString (Both DPB1)

        Given an input payload as
            """
            {"population": "CAU",
            "typing": "A*02:05:01+A*33:01:01^C*07:01:01+C*08:02:01^B*14:02:01:01+B*41:01:01:01^DRB1*13:02:01+DRB1*13:02:01^DQB1*06:04:01+DQB1*06:04:01^DPB1*04:01/DPB1*677:01+DPB1*03:01/DPB1*14:01"}
            """
        When submitting the subject's information to and retrieving results from 'dpb1-prediction/tce-groups'
        Then the output is found to be
            """
                {
                    "data": {
                        "dpb1_tce_groups": [
                        {
                            "tce_group": "2",
                            "probability": 1
                        }
                        ],
                        "dpb1_tce_genotypes": [
                        {
                            "tce_groups": "2+3",
                            "probability": 1
                        }
                        ],
                        "dpb1_genotypes": [
                        {
                            "genotype": "DPB1*03:01+DPB1*04:01",
                            "tce_groups": "2+3"
                        },
                        {
                            "genotype": "DPB1*03:01+DPB1*677:01",
                            "tce_groups": "2+3"
                        },
                        {
                            "genotype": "DPB1*04:01+DPB1*14:01",
                            "tce_groups": "2+3"
                        },
                        {
                            "genotype": "DPB1*14:01+DPB1*677:01",
                            "tce_groups": "2+3"
                        }
                        ]
                    }
                    }
            """

    Scenario: Ambiguous DPB1 GLString (Both DPB1)

        Given an input payload as
            """
            {"population": "CAU",
            "typing": "A*02:05:01+A*33:01:01^C*07:01:01+C*08:02:01^B*14:02:01:01+B*41:01:01:01^DRB1*13:02:01+DRB1*13:02:01^DQB1*06:04:01+DQB1*06:04:01^DPB1*01:01+DPB1*04:01|DPB1*02:01/DPB1*03:01+DPB1*04:01"}
            """
        When submitting the subject's information to and retrieving results from 'dpb1-prediction/tce-groups'
        Then the output is found to be
            """
                {
                    "data": {
                        "dpb1_tce_groups": [
                        {
                            "tce_group": "3",
                            "probability": 0.6101977780359107
                        },
                        {
                            "tce_group": "2",
                            "probability": 0.3898022219640893
                        }
                        ],
                        "dpb1_tce_genotypes": [
                        {
                            "tce_groups": "3+3",
                            "probability": 0.6101977780359107
                        },
                        {
                            "tce_groups": "2+3",
                            "probability": 0.3898022219640893
                        }
                        ],
                        "dpb1_genotypes": [
                        {
                            "genotype": "DPB1*02:01+DPB1*04:01",
                            "tce_groups": "3+3",
                            "probability": 0.5477578231158804
                        },
                        {
                            "genotype": "DPB1*03:01+DPB1*04:01",
                            "tce_groups": "2+3",
                            "probability": 0.3898022219640893
                        },
                        {
                            "genotype": "DPB1*01:01+DPB1*04:01",
                            "tce_groups": "3+3",
                            "probability": 0.06243995492003033
                        }
                        ]
                    }
                    }
            """
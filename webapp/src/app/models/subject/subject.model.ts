// Copyright (c) 2021 Be The Match.

// This file is part of DPB1 Prediction 
// (see https://github.com/nmdp-bioinformatics/dpb1-prediction).

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.

// You should have received a copy of the GNU Lesser General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.

interface Likelihoods {
    genotype : string;
    probability : number;
    tce_groups? : string;
}

export class Subject {
    "Error"? : string;
    "Ref"? : number;
    "DPB1 TCEs"?: Likelihoods[];
    "Source ID"? : string;
    "Registry Donor ID"? : string;
    "GRID/ID"? : string;
    "GRID"? : string;
    "Previously released"? : string;
    "Prev. Donations"? : string;
    "Readiness Score"? : string;
    "Status"? : string;
    "List"? : string;
    "Country"? : string;
    "ION/DC ID"? : string;
    "ION/DC Name"? : string;
    "Age"? : string;
    "Sex"? : string;
    "A 1"? : string;
    "A 2"? : string;
    "B 1"? : string;
    "B 2"? : string;
    "C 1"? : string;
    "C 2"? : string;
    "DRB1 1"? : string;
    "DRB1 2"? : string;
    "DQB1 1"? : string;
    "DQB1 2"? : string;
    "DPB1 TCE"? : string;
    "TCE P/M Likelihood"? : number;
    "DPB1 1"? : string;
    "DPB1 2"? : string;
    "DRB3 1"? : string;
    "DRB3 2"? : string;
    "DRB4 1"? : string;
    "DRB4 2"? : string;
    "DRB5 1"? : string;
    "DRB5 2"? : string;
    "DQA1 1"? : string;
    "DQA1 2"? : string;
    "DPA1 1"? : string;
    "DPA1 2"? : string;
    "Match Category (out of 10)"? : string;
    "Match Category (out of 8)"? : string;
    "Pr (10/10) = %"? : string;
    "Pr (9/10) = %"? : string;
    "Pr (8/10) = %"? : string;
    "Pr (8/8) = %"? : string;
    "Pr (7/8) = %"? : string;
    "Pr (6/8) = %"? : string;
    "A%"? : string;
    "B%"? : string;
    "C%"? : string;
    "DRB1%"? : string;
    "DQB1%"? : string;
    "A Match Grade"? : string;
    "B Match Grade"? : string;
    "C Match Grade"? : string;
    "DRB1 Match Grade"? : string;
    "DQB1 Match Grade"? : string;
    "Race"? : string;
    "Ethnicity"? : string;
    "Last Contact Date"? : string;
    "Contact Type"? : string;
    "CMV"? : string;
    "Num Preg"? : string;
    "ABO"? : string;
    "RhD Type"? : string;
    "CCR5"? : string;
    "Weight (kg)"? : string;
    "Previous CT"? : string;
    "Repository Sample"? : string;
    "Reg Date"? : string;
    "Avail Date"? : string;
    "TCE Grp 1"? : string;
    "TCE Grp 2"? : string;
    "Population"? : string;
}

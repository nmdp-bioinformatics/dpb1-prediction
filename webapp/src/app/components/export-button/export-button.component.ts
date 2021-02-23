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

import { Input, Component, OnInit } from '@angular/core';
import * as XLSX from 'xlsx';
import { ImportService } from '../../services/import-service/import.service';
import { FilterService } from '../../services/filter-service/filter.service';
import { Subject } from '../../models/subject/subject.model';

@Component({
  selector: 'app-export-button',
  templateUrl: './export-button.component.html',
  styleUrls: ['./export-button.component.scss']
})
export class ExportButtonComponent implements OnInit {
  @Input() donors : Subject[];
  filteredDonors : Subject[];
  fileName: string = 'dpb1-prediction-output';

  constructor(private importService : ImportService,
              private filterService : FilterService) { }

  ngOnInit() {
    const component = this;
    this.importService.currentFileName.subscribe(function(fileName){
      component.fileName = fileName;
    })
    this.filterService.currentFilteredDonors.subscribe(function(filteredDonors){
      component.filteredDonors = filteredDonors;
    });
    this.filteredDonors = this.donors;
  }

  export() {
    const ws: XLSX.WorkSheet = XLSX.utils.json_to_sheet(this.filteredDonors);

    const wb: XLSX.WorkBook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Results');
    XLSX.writeFile(wb, this.fileName.split('.csv')[0] 
                              + '-tce-predicted.csv');
  }

  hasTCELikelihoods(){
    const donorsWithLoadedPredictions = this.donors.filter(d => d['TCE P/M Likelihood'] >= 0);
    return donorsWithLoadedPredictions.length;
  }

}

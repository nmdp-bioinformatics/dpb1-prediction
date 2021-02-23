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
import { Subject } from '../../models/subject/subject.model';
import { ImportService } from '../../services/import-service/import.service';
import { PredictService } from '../../services/predict-service/predict.service';

@Component({
  selector: 'app-reset-button',
  templateUrl: './reset-button.component.html',
  styleUrls: ['./reset-button.component.scss']
})
export class ResetButtonComponent implements OnInit {
  @Input() patient: Subject;
  @Input() donors: Subject[];

  constructor(private predictService : PredictService,
              private importService : ImportService) { }

  ngOnInit() {
  }

  clearAll(){
    // let emptyPatient = { "Source ID" : "", "Population" : "", 
    //                   "A 1" : "", "A 2" : "", 
    //                   "B 1" : "", "B 2" : "", 
    //                   "C 1" : "", "C 2" : "", 
    //                   "DRB1 1" : "", "DRB1 2" : "", 
    //                   "DQB1 1" : "", "DQB1 2" : "", 
    //                   "DPB1 TCE" : null,
    //                   "DPB1 1" : "", "DPB1 2" : ""};
    this.importService.updateDonors([]);
    // this.predictService.updatePatient(emptyPatient);
  }

}

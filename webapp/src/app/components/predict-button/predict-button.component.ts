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
import { MatPaginator } from '@angular/material/paginator';
import { PredictService } from '../../services/predict-service/predict.service';
import { Subject } from '../../models/subject/subject.model';

@Component({
  selector: 'app-predict-button',
  templateUrl: './predict-button.component.html',
  styleUrls: ['./predict-button.component.scss']
})
export class PredictButtonComponent implements OnInit {

  @Input() patient : Subject;
  @Input() donors : Subject[];
  pagination : MatPaginator;

  constructor(private predictService : PredictService) { }

  ngOnInit() {
    const component = this;
    this.predictService.currentPatient.subscribe(function(patient){
      component.patient = patient;
    })
    this.predictService.currentPagination.subscribe(function(pagination){
      component.pagination = pagination;
    })
  }

  predict() {
    this.predictService.predictDPB1(this.patient, this.donors[0]);
  }

  emptyDPB1s(){
    return (!this.patient['DPB1 1'].trim() && !this.patient['DPB1 2'].trim());
  }

  emptyTypings(){
    return (!this.patient['A 1'].trim() && !this.patient['A 2'].trim() &&
            !this.patient['B 1'].trim() && !this.patient['B 2'].trim() &&
            !this.patient['DRB1 1'].trim() && !this.patient['DRB1 2'].trim());
  }

  emptyPopulation(){
    return !this.patient['Population'].trim();
  }
}

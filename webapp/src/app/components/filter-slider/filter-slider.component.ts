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
import { MatSliderChange } from '@angular/material';
import { Subject } from '../../models/subject/subject.model';
import { FilterService } from '../../services/filter-service/filter.service';

@Component({
  selector: 'app-filter-slider',
  templateUrl: './filter-slider.component.html',
  styleUrls: ['./filter-slider.component.scss']
})
export class FilterSliderComponent implements OnInit {
  @Input() donors : Subject[];
  min: number = 0;
  max: number = 100;
  tickInterval: number = 1;

  constructor(private filterService : FilterService) { }

  ngOnInit() {

  }

  formatLabel(value: number) {
    return (100 - value) + '%';
  }

  onThresholdChange(event: MatSliderChange) {
    const threshold = this._convertToLikelihood(event.value);
    this.filterService.updateTceThreshold(threshold);
  }

  hasTcePredictions(){
    return this.donors.filter(d => d['TCE P/M Likelihood']).length;
  }

  _convertToLikelihood(value : number) {
    return (100 - value) / 100;
  }
}

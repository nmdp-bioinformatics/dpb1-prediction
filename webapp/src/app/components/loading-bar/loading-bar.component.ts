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

import { Input, Component, OnInit, Pipe, PipeTransform } from '@angular/core';
import { Subject } from '../../models/subject/subject.model';
// import { PercentDonorsLoadedPipe } from '../../pipes/percent-donors-loaded.pipe';

@Component({
  selector: 'app-loading-bar',
  templateUrl: './loading-bar.component.html',
  styleUrls: ['./loading-bar.component.scss']
})
export class LoadingBarComponent implements OnInit {
  @Input() donors : Subject[];

  constructor() { }

  ngOnInit() {
  }

  numberWithTCE() {
    return this.donors.
      filter(d => d['TCE P/M Likelihood'] != null &&
      !isNaN(d['TCE P/M Likelihood']) &&
      d['TCE P/M Likelihood'] != -2).length;
  }

  calculatePercDonors() {
    return this.numberWithTCE() / this.donors.length * 100;
  }

}

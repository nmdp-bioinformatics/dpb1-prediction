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

@Component({
  selector: 'app-donor-input',
  templateUrl: './donor-input.component.html',
  styleUrls: ['./donor-input.component.scss']
})
export class DonorInputComponent implements OnInit {
  @Input() patient : Subject;
  @Input() donors : Subject[];
  filename: string;

  constructor(private importService : ImportService) { }

  ngOnInit() {
    const component = this;
    this.importService.currentFileName.subscribe(function(filename){
      component.filename = filename;
    })
  }

}

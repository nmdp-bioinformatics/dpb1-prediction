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

import { Injectable } from '@angular/core';
import { Subject } from '../../models/subject/subject.model';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ImportService {
  headers  :  string[] = ["GRID/ID", "GRID",
                          "Population", "Age", "Sex",
                          "A 1", "A 2", "B 1", "B 2",
                          "C 1", "C 2", "DRB1 1", "DRB1 2",
                          "DQB1 1", "DQB1 2",
                          "DPB1 1", "DPB1 2", "DPB1 TCE"];
    
  donors : Subject[];
  fileName : string;
  
  removedChars : string[] = ['"', '='];
  private donorSource = new BehaviorSubject(this.donors);
  private fileNameSource = new BehaviorSubject(this.fileName);
  currentDonors = this.donorSource.asObservable();
  currentFileName = this.fileNameSource.asObservable();

  updateDonors(donors : Subject[]) {
    this.donorSource.next(donors);
  }

  updateFileName(fileName : string) {
    this.fileNameSource.next(fileName);
  }

  constructor() { }

  _removedSuffixColumns(): string[] {
    return this.headers.map(a => a.replace(/ [12]$/g, ''))
  }

  _addLeadingZeroToAllele(value: string){
    if (value.indexOf(':') >= 0 && value.split(':')[0].length == 1){
      value = '0' + value;
    }
    return value
  }

  _removeChars(value : string){
    while (value && this.removedChars.some(c => value.indexOf(c) > 0)){
      this.removedChars.forEach(c => {
        value = value.replace(c, '');
      })
    }
    return value ? value.replace(/(\r\n|\n|\r)/gm,"") : value;
  }

  _numberDuplicates(headers: string[]){
    let map = {};
    const count = headers.map(function(val) {
        return map[val] = (typeof map[val] === "undefined") ? 1 : map[val] + 1;
    });
    const numberedHeaders = headers.map(function(val, index) {
        return val + (map[val] != 1 ? ' ' + count[index] : '');
    });
    return numberedHeaders;
  }

  formatTextInput(lines: Array<Array<string>>) {
    let headers = lines.shift().map(a => a.trim());
    headers = this._numberDuplicates(headers);
    let line : string[];
    let rows : Subject[] = [];
    const service = this;
    for (let i = 1; i <= lines.length; i++){
      line = lines[i - 1];
      if (line.filter(v => v != '').length){
        let subject : Subject = {'Ref' : i};
        headers.forEach(function(header, index){
          let value: string | number = service._addLeadingZeroToAllele(service._removeChars(line[index]));
          if (header != 'Ref'){
            if (header == "TCE P/M Likelihood"){
              value = parseFloat(value);
              value = value < 0 || isNaN(value) ? null : value;
            }
            subject[header] = value;
          }
        })
        if (!subject["GRID/ID"] && subject["GRID"]){
          subject["GRID/ID"] = subject["GRID"];
        }
        rows.push(subject);
      }
    }
    return rows;
  }
}

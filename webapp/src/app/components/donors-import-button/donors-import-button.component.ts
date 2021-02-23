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

import { Component, OnInit, Inject } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ImportService } from '../../services/import-service/import.service';
import { PredictService } from '../../services/predict-service/predict.service';
import { Subject } from '../../models/subject/subject.model';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import {map, startWith} from 'rxjs/operators';
import { Papa } from 'ngx-papaparse';

export interface DialogData {
  donors: Subject[];
}

@Component({
  selector: 'app-donors-import-button',
  templateUrl: './donors-import-button.component.html',
  styleUrls: ['./donors-import-button.component.scss']
})
export class ImportButtonComponent implements OnInit {
  donors: Subject[];

  constructor(public dialog: MatDialog,
    private importService : ImportService,
    private predictService : PredictService) { }

  ngOnInit() {
  }

  import() {
    const dialogRef = this.dialog.open(ImportDialogComponent, {
      data: {donors : this.donors}
    });

    dialogRef.afterClosed().subscribe(donors => {
      this.importService.updateDonors(donors);
      // this.predictService.updateDonorResults(null);
    })
  }
}

@Component({
  selector: 'app-import-dialog',
  templateUrl: './import-dialog.component.html',
  styleUrls: ['./donors-import-button.component.scss']
})
export class ImportDialogComponent implements OnInit {
  file: File;
  importLimitControl = new FormControl();
  filteredOptions: Observable<number[]>;
  options : number[] =  [20, 50, 100, 200];
  numTotalDonors : number;

  constructor(
    public dialogRef: MatDialogRef<ImportDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,
    private importService: ImportService,
    private papa: Papa) { }

  ngOnInit() {
    this.filteredOptions = this.importLimitControl.valueChanges
      .pipe(
        startWith(''),
        map(value => typeof value === 'number' ? value : value.size),
        map(size => size ? this._filter(size) : this.options.slice())
      );
    this.importLimitControl.setValue(this.options[0]);
  }

  displayFn(size: number): number {
    return size && size ? size : 50;
  }

  private _filter(size: number): number[] {
    const filterValue = size.toString();
    return this.options.filter(option => option.toString().indexOf(filterValue) === 0);
  }

  handleFileInput($event) {
    const file = $event.target.files[0];
    this.importService.updateFileName(file.name);
    const reader = new FileReader();
    reader.onload = () => {
      this.papa.parse(reader.result.toString(), {
        // header : true,
        skipEmptyLines : true,
        complete: (result) => {
          let donors = this.importService.formatTextInput(result.data);
          this.numTotalDonors = donors.length;
          this.data.donors = donors;
        }
      })
    };
    reader.readAsText(file);
  }

  trim(donors: Subject[]): Subject[] | null {
    // const limit = this.importLimitControl.value.size ? this.importLimitControl.value.size :
    //   this.importLimitControl.value;
    const limit = 500;
    return donors ? donors.slice(0, limit) :
      null;
  }

  calculateTime(numTotalDonors : number) {
    return numTotalDonors * 8 / 60;
  }
}

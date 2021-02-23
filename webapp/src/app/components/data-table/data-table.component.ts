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

import { Input, Component, OnInit, ViewChild, EventEmitter, Output } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { ImportService } from '../../services/import-service/import.service';
import { FilterService } from '../../services/filter-service/filter.service';
import { PredictService } from '../../services/predict-service/predict.service';
import { Subject } from '../../models/subject/subject.model';
import { trigger, style, animate, transition } from '@angular/animations';

@Component({
  selector: 'app-data-table',
  templateUrl: './data-table.component.html',
  styleUrls: ['./data-table.component.scss'],
  animations: [
    trigger(
      'inOutAnimation', 
      [
        transition(
          ':enter', 
          [
            style({ opacity: 0 }),
            animate('1s ease-out', 
                    style({ opacity: 1 }))
          ]
        ),
        transition(
          ':leave', 
          [
            style({ opacity: 1 }),
            animate('1s ease-in', 
                    style({ opacity: 0 }))
          ]
        )
      ]
    )
  ]
})
export class DataTableComponent implements OnInit {
  @Input() subjects : Subject[];
  @Input() donors : boolean;
  editable : boolean = false;
  @Output() collapsePatient : EventEmitter<boolean> = new EventEmitter();

  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;

  patient : Subject;
  predictStatus : boolean = false;
  allDisplayedColumns : string[] = [ "DPB1", "DPB1 TCE", "Ref",
      "GRID/ID and Population", "Age and Sex",
      "A", "B", "C", "DRB1", "DQB1"];
  previousDisplayedColumns : string[];
  displayedColumns : string[];
  currentSelectedSort : string;
  currentHeaderSorted : Object = { 'header' : undefined, 'ascending' : false };
  dataSource = new MatTableDataSource<Subject>();
  unknownDPB1 : boolean = false;

  constructor(private importService : ImportService,
              private filterService : FilterService,
              private predictService : PredictService) { }

  ngOnInit() {
    this.displayedColumns = this.donors ?
      this.allDisplayedColumns :
      this.allDisplayedColumns.slice(0,1);
    this.dataSource.data = this.subjects;
    this.dataSource.paginator = this.paginator;
    
    const component = this;
    if (this.donors){
      this.importService.currentDonors.subscribe(function(donors){
        if (donors) {
          component.dataSource.data = donors;
          component.subjects = donors;
        }
      })
      this.predictService.currentPatient.subscribe(function(patient){
        component.patient = patient;
      })
      this.predictService.currentResults.subscribe(function(results){
        if (results){
          const donorInResults = component.subjects.filter(d => d['GRID/ID'] == results.donor.id).length;
          console.log(results.donor.id + ' was detected', results);
          // console.log(component.subjects, results, donorInResults);
          if (donorInResults){
            component.predictService.assignPermissiveness(results, component.subjects);
            const firstUnknownTCEDonor = component.predictService.firstUnknownTceDonor(component.subjects);
            const loadingDonors = component.subjects.filter(d => d['TCE P/M Likelihood'] == -2);
            if (firstUnknownTCEDonor && !loadingDonors.length){
              component.predictService.predictDPB1(component.patient, firstUnknownTCEDonor);
            }
          }
        }
      })
      this.dataSource.paginator.page.subscribe(p => {
        this.predictService.updateIndices(p);
      })
      this.filterService.currentTceThreshold.subscribe(function(threshold){
        if (component.subjects.filter(d => d['TCE P/M Likelihood'] >= 0).length){
          component._filterTceDonors(threshold);
        };
      })
    }
  }

  _filterTceDonors(threshold: number) {
    const filteredDonors = this.subjects
      .filter(function(donor){
        threshold = threshold == 0 ? -2 : threshold;
        return donor['TCE P/M Likelihood'] >= threshold;
      });
    this.filterService.updateFilteredDonors(filteredDonors);
    this.dataSource.data = filteredDonors;
  }

  ngAfterViewInit() {
    this.predictService.updateIndices(this.dataSource.paginator);
  }

  updateList(id : number, property: string, event: any) {
    const editField = event.target.textContent;
    this.dataSource.data[id][property] = editField;
  }

  sort(header : string) {
    const ascending = this.currentHeaderSorted['ascending'];
    this.dataSource.data = this.dataSource.data.sort((a, b) => (ascending ? a[header] - b[header] :
                                                                b[header] - a[header]))
    this.currentHeaderSorted['header'] = header;
    this.currentHeaderSorted['ascending'] = !this.currentHeaderSorted['ascending'];
  }

  changeCurrentSort(header : string) {
    this.currentSelectedSort = header;
  }

  expand(){
    this.previousDisplayedColumns = this.displayedColumns;
    this.displayedColumns = this.allDisplayedColumns;
  }

  collapse(){
    this.collapsePatient.emit(false);
    this.displayedColumns = this.previousDisplayedColumns;
  }

}

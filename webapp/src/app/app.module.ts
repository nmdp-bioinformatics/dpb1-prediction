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

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule, HAMMER_GESTURE_CONFIG } from '@angular/platform-browser';
import { GestureConfig } from '@angular/material';
import { ContenteditableModule } from '@ng-stack/contenteditable';
import { NgModule } from '@angular/core';
import { MatDialogModule, 
  MatInputModule } from '@angular/material';
  import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatPaginatorModule } from '@angular/material';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatSliderModule } from '@angular/material/slider'
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { ControlPanelComponent } from './components/control-panel/control-panel.component';
import { ImportButtonComponent, ImportDialogComponent } from './components/donors-import-button/donors-import-button.component';
import { DataTableComponent } from './components/data-table/data-table.component';
import { ContentComponent } from './components/content/content.component';
import { PatientInputComponent } from './components/patient-input/patient-input.component';
import { DonorInputComponent } from './components/donor-input/donor-input.component';
import { PredictButtonComponent } from './components/predict-button/predict-button.component';
import { LoadingBarComponent } from './components/loading-bar/loading-bar.component';
import { ExportButtonComponent } from './components/export-button/export-button.component';
import { FilterSliderComponent } from './components/filter-slider/filter-slider.component';
import { ResetButtonComponent } from './components/reset-button/reset-button.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    ControlPanelComponent,
    ImportButtonComponent,
    ImportDialogComponent,
    DataTableComponent,
    ContentComponent,
    PatientInputComponent,
    DonorInputComponent,
    PredictButtonComponent,
    LoadingBarComponent,
    ExportButtonComponent,
    FilterSliderComponent,
    ResetButtonComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    ContenteditableModule,
    HttpClientModule,
    MatDialogModule,
    MatAutocompleteModule,
    MatIconModule,
    MatInputModule,
    MatTableModule,
    MatTooltipModule,
    MatPaginatorModule,
    MatProgressBarModule,
    MatSliderModule,
    ReactiveFormsModule,
    FormsModule
  ],
  exports: [
    MatAutocompleteModule,
    MatDialogModule,
    MatInputModule,
  ],
  entryComponents: [
    ImportDialogComponent
  ],
  providers: [
    {provide: HAMMER_GESTURE_CONFIG, useClass: GestureConfig}
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

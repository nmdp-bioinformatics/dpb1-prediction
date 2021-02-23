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
import { HttpClient } from '@angular/common/http';
import { ImportService } from '../../services/import-service/import.service';
import { MatPaginator } from '@angular/material/paginator';
import { environment } from '../../../environments/environment';

interface Likelihoods {
  genotype : string;
  probability : number;
  tce_groups? : string;
}

interface MatchCategories {
  category : string;
  probability : number;
}

interface ResultSubject {
  id : string;
  dpb1_TCEs : Likelihoods[];
  dpb1_SLGs : Likelihoods[];
}

interface ResultPair {
  tce_match_grades : MatchCategories[];
  donor : ResultSubject;
  recipient : ResultSubject;
  error? : string;
}

interface Response {
  data? : ResultPair[];
}

interface Error {
  message : string;
}

@Injectable({
  providedIn: 'root'
})
export class PredictService {

  private baseURL = environment.apiUrl + "/dpb1-prediction/tce-matches";

  patient : Subject;
  results : ResultPair;
  loci : String[] = ['A', 'C', 'B', 'DRB1', 'DPB1'];
  pagination : MatPaginator;
  
  private patientSource = new BehaviorSubject(this.patient);
  private donorResults = new BehaviorSubject(this.results);
  private paginationSource = new BehaviorSubject(this.pagination);
  currentPatient = this.patientSource.asObservable();
  currentResults = this.donorResults.asObservable();
  currentPagination = this.paginationSource.asObservable();

  constructor(private httpClient: HttpClient, private importService : ImportService) { }

  firstUnknownTceDonor(donors : Subject[]) : Subject | void {
    return donors
      .sort((a, b) => a['Ref'] - b['Ref]'])
      .filter(d => d['TCE P/M Likelihood'] == null)[0];
  }

  predictDPB1(patient: Subject, donor : Subject) {
    patient['TCE P/M Likelihood'] = -2;
    donor['TCE P/M Likelihood'] = -2; // For indicating loading
    const params = this._formatParams(patient, donor);
    console.log(params.subject_pairs[0].donor.id + ' was submitted', params);
    this.httpClient.post(this.baseURL, params)
      .toPromise()
      .then((res : Response) => {
        this._assignResults(res.data[0]);
      })
      .catch((error : Error) => {
        console.log(error);
        this._assignServerError(donor, error.message);
      })
  }

  _assignServerError(donor : Subject, message : string){
    let patient = this.patientSource.value;
    if (message.indexOf('Http failure') >= 0){
      donor['TCE P/M Likelihood'] = -1;
      const error = "The server is currently down";
      donor['Error'] = error;
      patient['Error'] = error;
    }
    this.patientSource.next(patient);
  }

  _assignResults(results: ResultPair){
    this._assignPatientResults(results);
    this.donorResults.next(results);
  }

  // updateDonorResults(results: ResultPair){
  //   this.donorResults.next(results);
  // }

  _assignPatientResults(results: ResultPair){
    let patient = this.patientSource.value;
    if (results.recipient &&
        results.recipient.dpb1_TCEs &&
        results.recipient.dpb1_TCEs.length){
      const dpb1_TCEs = results.recipient.dpb1_TCEs;
      patient['TCE P/M Likelihood'] = null;
      patient['DPB1 TCEs'] = dpb1_TCEs;
    } else {
      this._assignError(patient, results, 'recipient');
    }
    this.patientSource.next(patient);
  }

  _extractErrorMessage(message : string){
    const extraction = / ?'(.*?)\.?'.? ?/.exec(message);
    return extraction ? extraction[1] : ''
  }

  _formatParams(patient: Subject, donor: Subject) {
    return {"subject_pairs" : [
              {"recipient" : this._formatSubjectParams(patient, true),
              "donor" : this._formatSubjectParams(donor)}]}
  }

  _formatSubjectParams(subject: Subject, patient: boolean = false) {
    return {'id' : patient ? 'Patient' : subject['GRID/ID'],
            'typing' : this._generateGLstring(subject),
            'population' : subject['Population'].trim() || 'CAU'};
  }

  _generateGLstring(subject: Subject) {
    const service = this; 
    let alleles = this.loci.map(function(locus){
      let indices = ['1', '2'];
      let allelePair = indices.map(function(index){
        let typing = subject[locus + ' ' + index];
        if (typing){
          typing = typing.trim();
          const g_or_p_group = /\d[GP]$/.exec(typing);
          typing = g_or_p_group ? service._keep_two_fields(typing) : typing;
          const separator = typing ? (typing.indexOf(':') > 0 ? '*' : '')
                                   : null;
          return typing ? locus + separator + typing : null;
        }
      }).filter(a => a != null && a != '');
      if (allelePair.length == 1){
        allelePair = allelePair.concat(allelePair);
      }
      return allelePair.join('+')
    })
    const GLstring = alleles.filter(a => a != null && a != '').join('^');
    return GLstring;
  }

  _keep_two_fields(typing : string){
    typing = typing.split(':').slice(0, 2).join(':');
    const g_or_p_group = /\d[GP]$/.exec(typing);
    typing = g_or_p_group ? typing.slice(0, typing.length - 1) : typing;
    return typing;
  }

  updatePatient(patient : Subject){
    this.patientSource.next(patient);
  }

  updateIndices(pagination : MatPaginator) {
    this.paginationSource.next(pagination);
  }

  assignPermissiveness(result : ResultPair, donors : Subject[]){
    if (result && result.donor){
      const donorID = result.donor.id;
      let probability = -1;
      if (result.tce_match_grades && result.tce_match_grades.length){
        const permissiveCategory = result['tce_match_grades'].filter(g => g['category'] == 'PERMISSIVE');
        probability = permissiveCategory.length ? 
                        permissiveCategory[0].probability :
                        0;
      }
      const donor = donors.filter(d => d['GRID/ID'] == donorID)[0];
      if (donor){
        if (probability == -1){
          if (result.donor &&
              result.donor.dpb1_TCEs && 
              result.donor.dpb1_TCEs.length){
            donor['DPB1 TCEs'] = result.donor.dpb1_TCEs;
          } else {
            this._assignError(donor, result, 'donor');
          }
        }
        donor['TCE P/M Likelihood'] = probability;
      }
    }
  }

  _assignError(subject: Subject, results: ResultPair, subject_type: string){
    console.log(results);
    let id = null;
    if (results.error){
      if (results.error.indexOf(',') >= 0 &&
          results.error.split('"').length >= 2) {
            const fields = results.error.split('"');
            id = this._extractErrorMessage(fields[0]);
            id = id == 'Patient' ? 'the patient' : ('donor ' + id);
            let error = fields.slice(1).join('');
            const faultStringMatch = error.match('<faultstring>(.+)</faultstring>');
            if (faultStringMatch && faultStringMatch.length > 1){
                error = faultStringMatch[1];
            } else {
              let errors = error.split(',');
              error = this._extractErrorMessage(errors[errors.length - 1]);
            }
            const invalid_allele_regex = /(?:(.+) is not able to be reduced)|(?:Type not found for locus (.+))/;
            const invalid_allele_match = error.match(invalid_allele_regex);
            if (invalid_allele_match && invalid_allele_match.length > 2) {
              error = 'Verify that the ' + (invalid_allele_match[1] || invalid_allele_match[2]) +
                        ' allele is a valid allele';
            }
            const invalid_pop_regex = /The (.+) population was not properly loaded/;
            const invalid_pop_match = error.match(invalid_pop_regex);
            if (invalid_pop_match && invalid_pop_match.length > 1){
              error = "The '" + invalid_pop_match[1] + "' population was not recognized";
            }
            subject['Error'] = error + ' for ' + id;
      } else {
        subject['Error'] = results.error;
      }
    } else if (results[subject_type].dpb1_TCEs.length){
      const dpb1_TCEs = results[subject_type].dpb1_TCEs;
      subject['TCE P/M Likelihood'] = null;
      subject['DPB1 TCEs'] = dpb1_TCEs;
    } else if (!subject['Population']) {
      subject['Error'] = "This " + (subject_type == 'recipient' ? 'patient' : subject_type) +
                          " does not have a population code, which is needed to make TCE predictions"
    } else {
      subject['TCE P/M Likelihood'] = -1;
      subject['Error'] = "This " + (subject_type == 'recipient' ? 'patient' : subject_type) +
                          " was not successfully predicted \
                          either due to alleles or haplotypes outside \
                          of the reference data. Please double check \
                          that the alleles and population are formatted correctly";
    }

    if (subject_type == 'recipient'){
      this.updatePatient(subject);
    }
  }
}

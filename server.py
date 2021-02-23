# Copyright (c) 2021 Be The Match.

# This file is part of DPB1 Prediction 
# (see https://github.com/nmdp-bioinformatics/dpb1-prediction).

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

#!venv/bin/python
import gc
import os

from flask import Flask, jsonify, request, current_app, url_for
from flask_compress import Compress
from flask_restplus import Api, Resource, fields
from pyard import ARD

import config
from dpb1.frequencies import HaplotypeFreqs
from dpb1.imputation import Imputation
from dpb1.match import Matches
from dpb1.population import Population
from dpb1.subject import Subject, InvalidSubjectError
from dpb1.tce import TCE_map

if os.environ.get('Environment'):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')
 
    Api.specs_url = specs_url

app = Flask(__name__)
Compress(app)
flask_env = os.environ.get("FLASK_ENV")
if flask_env is not None:
    if flask_env.startswith('dev'):
        app.config.from_object(config.DevConfig())
    elif flask_env.startswith('qa'):
        app.config.from_object(config.QAConfig())
    elif flask_env.startswith('preprod'):
        app.config.from_object(config.PreProdConfig())
    elif flask_env.startswith('prod'):
        app.config.from_object(config.ProdConfig())
    else:
        app.config.from_object(config.LocalConfig())
else:
    app.config.from_object(config.LocalConfig())

api = Api(app)
dpb1_prediction = api.namespace('dpb1-prediction', description="Given a subject's population and typing, this service predicts DPB1 alleles, TCE groups, and permissiveness matching.")
dpb1_imputation = api.namespace('dpb1-imputation', description="Given (a) subjects' imputed phased multi-locus unambiguous genotypes, this service predicts DPB1 alleles and TCE groups.")

locus_order = ['A', 'C', 'B', 'DRBX', 'DRB1', 'DQB1']

print("******************************Loading Frequencies Begin******************************")
populations = []
# populations = ["CAU"]
hap_freqs = HaplotypeFreqs(
                directory=app.config['HAP_FREQS_DIR'],
                populations=populations,
                locus_order=locus_order)
print("******************************Loading Frequencies Complete******************************")

ard = ARD(data_dir='data')
print("******************************Loading py-ard Complete******************************")
tce_map = TCE_map(ard=ard)

# Mark the loaded reference data as static
gc.freeze()

example_GLstring = "A*02:05:01+A*33:01:01^C*07:01:01+C*08:02:01^B*14:02:01:01+B*41:01:01:01^DRB1*13:02:01+DRB1*13:02:01^DQB1*06:04:01+DQB1*06:04:01"
subject_model_w_id = api.model('subject', {'id' : fields.String(example="123456", required=True),
                                            'typing' : fields.String(example=example_GLstring, required=True),
                                            'population' : fields.String(example="CAU", required=True)})
subject_model = api.model('subject', {'typing' : fields.String(example=example_GLstring, required=True),
                                      'population' : fields.String(example="CAU", required=True)})

@dpb1_prediction.route("/tce-groups")
class DPB1TCEs(Resource):
    
    @api.expect(subject_model)
    def post(self):
        """
        returns predicted TCE (T-cell epitope) groups (ex: 3+3, 3+2, 1+1) with calculated probabilities.
        TCE groups with less than 0.01 probability are omitted.
        """
        try:
            typing = request.json['typing']
            population = request.json['population']
            subject = Subject(glstring=typing,
                                population=population,
                                locus_order=locus_order,
                                ref_freqs=hap_freqs.get_pop_freqs(population),
                                imputation_url=current_app.config['IMPUTATION_URL'],
                                ard=ard,
                                tce_map=tce_map)
            subject.generate_dpb1_slugs()
            subject.generate_tce_genotypes()
            return jsonify({'data' : subject.serialize()})
        except Exception as e:
            print(e)
            return e.__dict__, 500

@dpb1_prediction.route("/tce-matches")
class TCEMatching(Resource):

    subject_pair_model = api.model('Subject pair',
        {'donor' : fields.Nested(subject_model_w_id),
         'recipient' : fields.Nested(subject_model_w_id)}
    )
    model = api.model('Subject pairs', 
                       {'subject_pairs': fields.List(fields.Nested(subject_pair_model))
                        }
                     )
    @api.expect(model)
    def post(self):
        """
        returns predicted TCE match categories (ex: HvG_NONPERMISSIVE, PERMISSIVE, etc) with calculated probabilities.
        Bases predictions off of TCE groups by default, but can include allele-based predictions (which includes the MATCH category).
        Match categories with less than 0.01 probability are omitted.
        """
        try:
            subject_pairs = request.json["subject_pairs"]
            ref_freqs = {}
            results = []
            for subject_pair in subject_pairs:
                try:
                    subjects = {}
                    for subject_type in ['recipient', 'donor']:
                        subject = subject_pair[subject_type]
                        sub_id = 'id' in subject and subject['id'] or None
                        try:
                            typing = subject_pair[subject_type]['typing']
                            population = Population(subject_pair[subject_type]['population']).code
                            subjects[subject_type] = Subject(glstring=typing, id=sub_id, population=population,
                                                            locus_order=locus_order, ref_freqs=hap_freqs.get_pop_freqs(population),
                                                            imputation_url=current_app.config['IMPUTATION_URL'],
                                                            ard=ard,
                                                            tce_map=tce_map)
                            subjects[subject_type].generate_dpb1_slugs()
                            subjects[subject_type].generate_tce_genotypes()
                        except Exception as e:
                            raise InvalidSubjectError(sub_id, str(e))
                    matches = Matches(subjects['recipient'], subjects['donor'])
                    tce_match_grades = matches.get_tce_match_grades()
                    results.append({'tce_match_grades' : [match_grade.serialize() for match_grade in tce_match_grades],
                                    'donor' : subjects['donor'].serialize(),
                                    'recipient' : subjects['recipient'].serialize()})
                except Exception as e:
                    recip = subject_pair['recipient']
                    donor = subject_pair['donor']
                    print(e)
                    results.append({'donor' : {'id' : 'id' in donor and donor['id'] or None},
                                    'recipient' : {'id' : 'id' in recip and recip['id'] or None},
                                    'error' : str(e)})
            return jsonify({'data' : results})
        except Exception as e:
            print(e)
            return e.__dict__, 500

@dpb1_imputation.route("/tce-groups")
class DPB1SLUGs(Resource):

    imputation_model = api.model('Imputation',
        {'haplotype1' : fields.String(example="A*01:01~C*07:01~B*08:01~DRB1*03:01~DQB1*02:01", required=True),
         'population1' : fields.String(example="CAU", required=True),
         'frequency1' : fields.Float(example=0.0598117681949288, required=True),
         'haplotype2' : fields.String(example="A*01:01~C*07:01~B*08:01~DRB1*03:01~DQB1*02:01", required=True),
         'population2' : fields.String(example="CAU", required=True),
         'frequency2' : fields.Float(example=0.0598117681949288, required=True)})
    subject_model = api.model('Subject imputation',
        {'id' : fields.String(example="147803795", required=True),
         'imputation' : fields.List(
             fields.Nested(imputation_model)
         )})
    model = api.model('Subjects', {'subjects': fields.List(fields.Nested(subject_model))})

    @api.expect(model)
    def post(self):
        """
        returns a list of predicted DPB1 Single-Locus Genotypes (SLGs) (ex: DPB1*04:01+DPB1*19:01) with calculated probabilities.
        SLGs with less than 0.01 probability are omitted.
        """
        try:
            subjects = request.json['subjects']
            results = []
            for subject in subjects:
                try:
                    sub_id = subject['id']
                    imputation = Imputation(imputation=subject['imputation'])
                    population = subject['imputation'][0]['population1']
                    subject = Subject(imputation=imputation,
                                        population=population,
                                        ref_freqs=hap_freqs.get_pop_freqs(population),
                                        ard=ard,
                                        id=sub_id,
                                        tce_map=tce_map)
                    subject.generate_dpb1_slugs()
                    subject.generate_tce_genotypes()
                    results.append(subject.serialize())
                except Exception as e:
                    print(e)
                    results.append({'id' : 'id' in subject and subject['id'] or None,
                                    'error' : str(e)})
            return jsonify({'data' : results})
        except Exception as e:
            print(e)
            return e.__dict__, 500


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run("0.0.0.0", 5010, debug=False)

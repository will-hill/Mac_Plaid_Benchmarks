from elasticsearch import Elasticsearch
import json
import os

base_dir = 'mlruns/1/'
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.delete(index='benchmarks', ignore=[400, 404])


def mapping_type(s):
    try:
        float(s)
        return 'double'
    except ValueError:
        return 'keyword'  # can be 'text' but 'keyword' is aggregatable for analysis & viz


mapping = {
    'mappings': {
        'properties': {}
    }
}

for trial in os.listdir(base_dir):
    if os.path.exists(os.path.realpath(base_dir + trial + '/artifacts/result.json')):
        mapping['mappings']['properties']['id'] = {'type': 'text'}

        # plaidbench results
        with open(base_dir + trial + '/artifacts/result.json') as result_json:
            result = json.load(result_json)
            for key, value in result.items():
                type = mapping_type(value)
                if type == 'double':
                    mapping['mappings']['properties'][key] = {'type': type, 'ignore_malformed': True}
                else:
                    mapping['mappings']['properties'][key] = {'type': type}

        del result, result_json, type, key, value
        # params
        for param in os.listdir(base_dir + trial + '/params/'):
            with open(base_dir + trial + '/params/' + param) as p:
                type = mapping_type(p.readline())
                if type == 'double':
                    mapping['mappings']['properties'][param] = {'type': type, 'ignore_malformed': True}
                else:
                    mapping['mappings']['properties'][param] = {'type': type}

        del type, param, p
        # metrics
        for metric in os.listdir(base_dir + trial + '/metrics/'):
            with open(base_dir + trial + '/metrics/' + metric) as m:
                type = mapping_type(m.readline().split()[1])
                if type == 'double':
                    mapping['mappings']['properties'][metric] = {'type': type, 'ignore_malformed': True}
                else:
                    mapping['mappings']['properties'][metric] = {'type': type}
        break

response = es.indices.create(
    index='benchmarks',
    body=mapping
)
print(response)

del mapping, m, metric, response, trial, type
# start indexing

for trial in os.listdir(base_dir):
    if os.path.exists(os.path.realpath(base_dir + trial + '/artifacts/result.json')):
        trial_result = {'id': trial}

        # plaidbench results
        with open(base_dir + trial + '/artifacts/result.json') as result_json:
            trial_result.update(json.load(result_json))

        # params
        for param in os.listdir(base_dir + trial + '/params/'):
            with open(base_dir + trial + '/params/' + param) as p:
                trial_result[param] = p.readline()

        # metrics
        for metric in os.listdir(base_dir + trial + '/metrics/'):
            with open(base_dir + trial + '/metrics/' + metric) as m:
                trial_result[metric] = m.readline().split()[1]

        res = es.index(index='benchmarks', id=trial_result['id'], body=trial_result)
        print(res)

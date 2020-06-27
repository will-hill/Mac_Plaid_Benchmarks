import mlflow
from os import path, popen, getcwd
from threading import Thread
from json import load as json_load
from time import sleep, process_time


def benchmark_t(args):
    from plaidbench import cli
    results = cli.plaidbench(args)
    print('results....  ', type(results), '   ', results)


devices = ['metal_amd', 'opencl_amd', 'metal_uhd', 'opencl_uhd', 'cpu']
small_networks = 'mobilenet|nasnet_mobile|imdb_lstm'.split('|')

for device in devices:
    for network in small_networks:
        name = f'TRIAL_{device}_{network}'
        if path.exists(getcwd() + '/' + name):
            continue
        popen(f'cp ~/{device}.json ~/.plaidml')
        with mlflow.start_run(experiment_id=1, run_name=name[6:]):
            x = Thread(target=benchmark_t, kwargs={'args': [f'--results=./{name}', 'keras', network]})
            start_time = process_time()
            x.start()
            x.join()
            mlflow.log_metric('ttl_exec_time', process_time() - start_time)
            mlflow.log_param('device', device)
            mlflow.log_param('network', network)
            sleep(2)
            mlflow.log_artifact(getcwd() + '/' + name + '/result.json')
            with open(name + '/result.json') as json_file:
                result = json_load(json_file)

                mlflow.log_param('examples', result['examples'])
                mlflow.log_param('model', result['model'])
                mlflow.log_param('batch_size', result['batch_size'])
                mlflow.log_param('backend', result['backend'])

                mlflow.log_metric('fail_ratio', result['fail_ratio'])
                mlflow.log_metric('max_abs_error', result['max_abs_error'])
                mlflow.log_metric('max_error', result['max_error'])
                mlflow.log_metric('correct', int(result['correct']))
                mlflow.log_metric('compile_duration', result['compile_duration'])
                mlflow.log_metric('duration_per_example', result['duration_per_example'])
                mlflow.log_metric('tile_duration_per_example', result['tile_duration_per_example'])

        exit(0)

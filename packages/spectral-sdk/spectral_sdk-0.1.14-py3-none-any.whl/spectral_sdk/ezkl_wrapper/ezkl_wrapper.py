import asyncio
import cloudpickle
import datetime
import ezkl
import json
import os
import requests
import torch
import zipfile

model_dir = './model'
model_onnx_path = model_dir + '/model.onnx'
model_compiled_onnx_path = model_dir + '/compiled_model.onnx'
model_settings_path = model_dir + '/settings.json'
model_witness_path = model_dir + '/witness.json'
model_vk_path = model_dir + '/model_vk.vk'
model_pk_path = model_dir + '/model_pk.pk'
model_srs_path = model_dir + '/kzg.srs'
model_proof_path = model_dir + '/zkml_hashed_proof.pf'
model_cal_path = model_dir + '/cal_data.json'
# cmd line args
pickle_model_path = './model/cloudpickle-model.pkl'
model_input_path = './model/input.json'
pickle_model_path = './model.pkl'
model_input_path = './input.json'

ipfs_node = 'https://plumber.dev.spectral.finance'

zip_name = 'model.zip'

def zip_files(files, zip_name='model.zip'):
    zip_file = zipfile.ZipFile(zip_name, 'w')
    path = os.path.basename(zip_name)
    with zip_file:
        for file in files:
            zip_file.write(file, path)
    print("Zipping [33] DONE " + str(datetime.datetime.now()))
    return path


def read_and_report(file, chunk_size=1024):
    total_size = os.path.getsize(file_path)
    bytes_read = 0
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        bytes_read += len(data)
        print(f"Uploaded {bytes_read}/{total_size} bytes ({bytes_read * 100 / total_size:.2f}%)", end='\r')
        yield data
        
def upload_file_to_service(file_path, url, auth_token):
    with open(file_path, 'rb') as file:
        files = {'file': (file_path, read_and_report(file))}
        response = requests.post(url, files=files, headers={'Authorization': f'Bearer {auth_token}'})

    json_response = json.loads(response.text)
    return json_response['Hash']


def dump_model(onnx_model_path, input_json_path):
    run_args = ezkl.PyRunArgs()
    run_args.input_visibility = 'public'
    run_args.param_visibility = 'public'
    run_args.output_visibility = 'public'
    model_onnx_path = onnx_model_path
     #run_args.batch_size = 1
    try:
        res = ezkl.gen_settings(model_onnx_path, model_settings_path, py_run_args=run_args)
        if res:
            print('Settings successfully generated')
    except Exception as e:
        print(f'An error occurred: {e}')

    # cal_data = {'input_data': input.detach().cpu().numpy().tolist()}
    # save as json file
    # with open(model_cal_path, "w") as f:
    #     json.dump(cal_data, f)
    #     f.flush()
    # calibrate the settings file

        async def f():
            res = await ezkl.calibrate_settings(input_path, model_onnx_path, model_settings_path,
                                                'resources')
            if res:
                print('Settings successfully calibrated')
            else:
                print('Settings calibration failed')
        asyncio.run(f())

    print("Calibration DONE " + str(datetime.datetime.now()))
    # get the SRS string

    try:
        res = ezkl.compile_circuit(
            model_onnx_path, model_compiled_onnx_path, model_settings_path)
        if res:
            print('Model successfully compiled')
    except Exception as e:
        print(f'An error occurred: {e}')

    res = ezkl.get_srs(model_srs_path, model_settings_path)
    print("SRS fetched " + str(datetime.datetime.now()))
    # try:
    #     res = ezkl.gen_witness(
    #         model_input_path, model_compiled_onnx_path, model_witness_path)
    #     if res:
    #         print('Witness file successfully generated')
    # except Exception as e:
    #     print(f'An error occurred: {e}')
    # print("Witness generated " + str(datetime.datetime.now()))

    # mock proof for sanity check
    # try:
    #     res = ezkl.mock(model_witness_path,
    #                     model_compiled_onnx_path)
    #     if res:
    #         print('Mock proof run was successfull')
    # except Exception as e:
    #     print(f'An error occurred: {e}')
    # print("In [29] DONE " + str(datetime.datetime.now()))
    # ezkl setup - to generate PK and VK
    try:
        res = ezkl.setup(model_compiled_onnx_path, model_vk_path,
                        model_pk_path, model_srs_path)
        if res:
            print('Setup was successful')
    except Exception as e:
        print(f'An error occurred: {e}')
    print("In [30] DONE " + str(datetime.datetime.now()))
    # generate proof
    # try:
    #     res = ezkl.prove(model_witness_path, model_compiled_onnx_path, model_pk_path, model_proof_path, model_srs_path,
    #                     'poseidon',  # 'evm' if proof required to be deployed onchain, 'poseidon' otherwise
    #                     'single')
    #     if res:
    #         print('Proof was successfully generated')
    # except Exception as e:
    #     print(f'An error occurred: {e}')
    # print("In [31] DONE " + str(datetime.datetime.now()))


    # try:
    #     res = ezkl.verify(model_proof_path, model_settings_path,
    #                     model_vk_path, model_srs_path)
    #     if res:
    #         print('Proof was successfully verified')
    # except Exception as e:
    #     print(f'An error occurred: {e}')
    # print("In [32] DONE " + str(datetime.datetime.now()))

    print([model_srs_path, model_vk_path, model_settings_path, input_json_path])
    path = zip_files([model_srs_path, model_vk_path, model_settings_path, input_json_path])
    # Usage example

    service_url = 'https://plumber.dev.spectral.finance:4000/api/v1/ipfs'
    auth_token = 'SFMyNTY.g2gDbQAAACQ4ZGJkNjQwMi0xMzgyLTRjYjAtOGI3MC05NTczNGEwMDk0OGJuBgCNBN6FiwFiAAFRgA.CwfkB1Nst3xGzd48okCKcBjn0bAAg1KKQr_7iMo662k'

    hash = upload_file_to_service(path, service_url, auth_token)
    return hash
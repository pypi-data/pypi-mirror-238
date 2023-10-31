import tarfile
import io
import os
import time
import random
from tqdm import tqdm
import os
import yaml

"""
support functions to help in automatic_analysis tasks
"""

"""
Make tar files of inputted model folders and Upload tar files for Datalake collection automatic_analysis_models collection and return the stored location information
@param source_dir: path of the model folder which needed to be uploaded
@param model_id:id/name of the model which is registered in the datalake
@param _datalake_client: datalake_client instance in order to acquire datalake SDK s inside this function
"""


def make_tarfile_in_memory(source_dir, model_id, _datalake_client):
    client = _datalake_client
    tar_stream = io.BytesIO()
    print("Started compressing...")
    total_files = sum([len(files) for _, _, files in os.walk(source_dir)])
    with tarfile.open(fileobj=tar_stream, mode='w:gz') as tar:
        cwd = os.getcwd()
        os.chdir(source_dir)
        pbar = tqdm(total=total_files, desc="Compressing..",
                    dynamic_ncols=True)
        for root, dirs, files in os.walk('.'):
            for file_ in files:
                file_path = os.path.join(root, file_)
                tar.add(file_path, arcname=file_path)
                pbar.update(1)
        pbar.close()
        os.chdir(cwd)
    tar_stream.seek(0)
    print("Compressing Completed")
    temp_path = f"./{model_id}.tar.gz"
    with open(temp_path, 'wb') as f:
        f.write(tar_stream.read())
    result = client.file_upload(temp_path, 7, "automatic_analysis_models", meta_data_object={
    }, meta_data_override=False, storage_prefix_path=None)
    client.wait_for_job_complete(result['job_id'])
    datalake_unique_name = result["unique_name"]
    path_details = client.get_item_details(
        datalake_unique_name, {"storagePath": True, "bucketName": True})
    storage_url = path_details['url']
    bucket_name = path_details['bucketName']
    object_key = path_details['storagePath']
    with open(f"{source_dir}/label_list.yaml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            label_list = data['label_list']
        except yaml.YAMLError as exc:
            print(exc)
    files = os.listdir(source_dir)
    pt_files = [f for f in files if f.endswith('.pt')]
    if pt_files:
        model_name = pt_files[0]
        print(f"The pytorch file is: {model_name}")
    else:
        model_name = 'test.pt'
        print("No pytorch files found")
    os.remove(temp_path)
    return storage_url, bucket_name, object_key, label_list, model_name


"""
Generate a unique ID based on the time the instance is initiated and return that ID in order to support status reporting
"""


def generate_unique_id():
    timestamp = int(time.time() * 1000)
    random_part = random.randint(0, 9999)

    unique_id = f"{timestamp:013d}{random_part:04d}"
    return unique_id

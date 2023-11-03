from typing import List
from loguru import logger

import pyarrow as pa
import pyarrow.parquet as pq
from object_storage_client import ObjectStorageClient


def get_bucket_from_step_name(step_name: str, list_buckets: List[dict]):
    for bucket in list_buckets:
        if bucket["step_name"] == step_name:
            return bucket


def get_dataset_path_from_step_name(step_name: str, list_parquets: List[dict]):
    for parquet in list_parquets:
        if parquet["step_name"] == step_name:
            return parquet["bucket_name"], parquet["object_name"]


def get_artefacts_path_from_registry_name(registry_name: str, list_registries: List[dict]):
    for registry in list_registries:
        if registry["registry_name"] == registry_name:
            return registry


def list_bucket_objects(bucket_name: str, list_buckets: List[dict], client, prefix: str = "", recursive: bool = True):
    logger.info(f"Getting list of objects on bucket '{bucket_name}'...")
    try:
        bucket_config = get_bucket_from_step_name(bucket_name, list_buckets)
        bucket_name = bucket_config["bucket_name"]
        object_storage_client = ObjectStorageClient(bucket_config, client)
        return object_storage_client.list_bucket_objects(bucket_name, prefix, recursive)
    except Exception as ex:
        error = f"Not able to list objects on bucket '{bucket_name}': {str(ex)}"
        logger.info(error)
        raise Exception(error)


def read_from_bucket_to_file(bucket_name: str, object_name: str, list_buckets: List[dict], client):
    logger.info(f"Reading file '{object_name}' from bucket '{bucket_name}'...")
    try:
        bucket_config = get_bucket_from_step_name(bucket_name, list_buckets)
        bucket_name = bucket_config["bucket_name"]
        object_storage_client = ObjectStorageClient(bucket_config, client)
        return object_storage_client.read_from_bucket_to_file(bucket_name, object_name)
    except Exception as ex:
        error = f"Not able to read the object '{object_name}' from bucket '{bucket_name}': {str(ex)}"
        logger.info(error)
        raise Exception(error)


def write_file_in_bucket(bucket_name: str, file_name: str, data, list_buckets: List[dict], client):
    logger.info(f"Writing new file '{file_name}' on bucket '{bucket_name}'...")
    try:
        bucket_config = get_bucket_from_step_name(bucket_name, list_buckets)
        bucket_name = bucket_config["bucket_name"]
        object_storage_client = ObjectStorageClient(bucket_config, client)
        object_storage_client.write_file_in_bucket(bucket_name, file_name, data)
    except Exception as ex:
        error = f"Not able to write the file {file_name} on bucket {bucket_name}: {str(ex)}"
        logger.info(error)
        raise Exception(error)


def import_dataset(dataset_name: str, list_parquets: List[dict], client, s3):
    logger.info(f"Importing dataset '{dataset_name}' from flow...")
    try:
        bucket_name, path = get_dataset_path_from_step_name(dataset_name, list_parquets)
        bucket = client.bucket_exists(bucket_name)
        if bucket:
            df = pq.ParquetDataset(f"{bucket_name}/{path}", filesystem=s3).read_pandas().to_pandas()
            return df
        else:
            raise Exception("Bucket" + bucket_name + "does not exist")
    except Exception as ex:
        error = f"Not able to import dataset {dataset_name} from minio bucket: {str(ex)}"
        logger.info(error)
        raise Exception(error)


def export_dataset(dataset, dataset_step_name, list_parquets, client, s3):
    logger.info(f"Exporting output dataset on the flow with name '{dataset_step_name}'...")
    try:
        bucket_name, path = get_dataset_path_from_step_name(dataset_step_name, list_parquets)
        bucket = client.bucket_exists(bucket_name)
        if bucket:
            table = pa.Table.from_pandas(dataset, preserve_index=False)
            pq.write_table(table, f"{bucket_name}/{path}", filesystem=s3, compression="snappy")
            return True
        else:
            raise Exception(f"Bucket {bucket_name} does not exist.")
    except Exception as ex:
        error = f"Not able to save dataset {dataset_step_name} into minio bucket: {str(ex)}"
        logger.info(error)
        raise Exception(error)


def get_model_artefact(registry_name: str, artefact_path: str, registries_inputs: List[dict], client, run_id: str = None):
    logger.info(
        f"Reading model artefact '{artefact_path}' related to " +
        (f"run '{run_id}' from registry '{registry_name}'..." if run_id else f"activated run on registry '{registry_name}'...")
    )
    try:
        registry = get_artefacts_path_from_registry_name(registry_name, registries_inputs)
        artefacts_folder = registry['artefacts_path']
        if run_id:
            artefacts_folder = "/".join(artefacts_folder.split("/")[:-1]) + "/" + run_id
        return client.read_from_bucket_to_file(registry["bucket_name"], f"{artefacts_folder}/{artefact_path}")
    except Exception as ex:
        error = f"Not able to read the artefact {artefact_path} of registry {registry_name}: {str(ex)}"
        logger.info(error)
        raise Exception(error)


def save_model_artefact(registry_name: str, artefact_path: str, data, registries_inputs: List[dict], client, run_id: str = None):
    logger.info(
        f"Saving model artefact '{artefact_path}' related to " +
        (f"run '{run_id}' from registry '{registry_name}'..." if run_id else f"activated run on registry '{registry_name}'...")
    )
    try:
        registry = get_artefacts_path_from_registry_name(registry_name, registries_inputs)
        artefacts_folder = registry['artefacts_path']
        if run_id:
            artefacts_folder = "/".join(artefacts_folder.split("/")[:-1]) + "/" + run_id
        client.write_file_in_bucket(registry["bucket_name"], f"{artefacts_folder}/{artefact_path}", data)
    except Exception as ex:
        error = f"Not able to write the artefact {artefact_path}: {str(ex)}"
        logger.info(error)
        raise Exception(error)

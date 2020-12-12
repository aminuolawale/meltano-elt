from google.cloud import bigquery
import os


def upload_to_bigquery(client, dataset, entity):
    """ """
    table_id = f"{dataset}.{entity}"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
    )
    file_path = os.path.join(os.getcwd(), "output", f"{entity}.jsonl")
    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    job.result()
    table = client.get_table(table_id)
    result = "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), table_id
    )
    return result


if __name__ == "__main__":
    print("starting file watcher")
    entity = "category"
    while True:
        file_path = os.path.join(os.getcwd(), "output", f"{entity}.jsonl")
        if os.path.exists(file_path):
            print("detected json file, exporting")
            os.environ.update(
                GOOGLE_APPLICATION_CREDENTIALS="/home/aminuolawale/Downloads/green-buttress-289410-6db7a67665df.json"
            )
            client = bigquery.Client()
            dataset = "green-buttress-289410.diamantinodiamantino"
            result = upload_to_bigquery(client, dataset, entity)
            print("the result", result)
            os.remove(file_path)

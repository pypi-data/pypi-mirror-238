import os
import traceback

from google.cloud import bigquery
import logging
import pandas as pd

logging.basicConfig(format='%(name)s - %(levelname)s -%(asctime)s- %(message)s', level=logging.INFO)


class BigQuery():
    def __init__(self, credential_json: str):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_json
        self.client = bigquery.Client()

    def execute_query(self, query: str):
        query_job = self.client.query(query)
        results_df = query_job.result().to_dataframe()  # Waits for job to complete.
        return results_df

    def dump_dataframe_to_bq_table(self, dataframe: pd.DataFrame, schema_cols_type: dict, table_id: str, mode: str):
        """Send a Slack message to a channel via a webhook.

        Args:
            dataframe(pandas dataframe): for dataframe to be dumped to bigquery
            schema_cols_type: {"date_start":"date", "id": "integer", "name": "string"}

            table_id (list): table_id in which dataframe need to be inserted e.g project_id.dataset.table_name = table_id
            mode(str): To append or replace the table - e.g mode = "append"  or mode="replace"
        Returns:
            returns as success message with number of inserted rows and table name
        """
        schema = []
        for col, col_type in schema_cols_type.items():
            if col_type == "date":
                schema.append(
                    bigquery.SchemaField(col, bigquery.enums.SqlTypeNames.DATE)
                )
            elif col_type=="integer":
                schema.append(
                    bigquery.SchemaField(col, bigquery.enums.SqlTypeNames.INTEGER)
                )
            elif col_type == "string":
                schema.append(
                    bigquery.SchemaField(col, bigquery.enums.SqlTypeNames.STRING)
                )
            elif col_type == "datetime":
                schema.append(
                    bigquery.SchemaField(col, bigquery.enums.SqlTypeNames.DATETIME)
                )

        if mode == "replace":
            write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        else:
            write_disposition = bigquery.WriteDisposition.WRITE_APPEND
        job_config = bigquery.LoadJobConfig(
            # Specify a (partial) schema. All columns are always written to the
            # table. The schema is used to assist in data type definitions.
            schema=schema,
            # Optionally, set the write disposition. BigQuery appends loaded rows
            # to an existing table by default, but with WRITE_TRUNCATE write
            # disposition it replaces the table with the loaded data.
            write_disposition=write_disposition,
        )

        job_config.schema_update_options = [
            bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
        ]

        load_job = None
        retry_count = 0
        exception = None
        while load_job is None and retry_count < 5:
            try:
                load_job = self.client.load_table_from_dataframe(
                    dataframe, table_id, job_config=job_config
                )  # Make an API request.
                load_job.result()  # Wait for the job to complete.

                table = self.client.get_table(table_id)  # Make an API request.
                message = "Loaded {} rows and {} columns to {} ".format(load_job.output_rows,
                                                                        len(table.schema),
                                                                        table_id)
                logging.info(message)
                return message
            except Exception as e:
                exception = e
                retry_count += 1
                print(traceback.format_exc())
        raise Exception(f"BigQuery load job given exception in all the {retry_count} retries:  {exception}")

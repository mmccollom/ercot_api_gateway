import json
import pyarrow.parquet as pq


def execute(delivery_date: str) -> str:
    """
    Get data from s3 and return a json string with the data
    :param delivery_date:
    :return:str
    """

    filters = [('delivery_date', '=', delivery_date),]

    s3_path = 's3://ercot-62841215/sced_lmp/'
    dataset = pq.ParquetDataset(s3_path, filters=filters)

    df = dataset.read().to_pandas()
    return json.loads(df.to_json(orient='records'))


# api gateway lambda handler
def lambda_handler(event, context):
    print(event)
    delivery_date = event['delivery_date']
    return execute(delivery_date)


# for local testing
if __name__ == '__main__':
    print (lambda_handler({'delivery_date': '2023-05-20'}, None))

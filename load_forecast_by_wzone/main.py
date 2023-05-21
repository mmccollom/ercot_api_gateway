import json
import pyarrow.parquet as pq


def execute(publish_date: str, publish_hour: int, delivery_date: str = None) -> str:
    """
    Get data from s3 and return a json string with the data
    :param publish_date:
    :param publish_hour:
    :param delivery_date:
    :return:str
    """

    if delivery_date:
        filters = [('publish_date', '=', publish_date),
                   ('publish_hour', '=', publish_hour),
                   ('delivery_date', '=', delivery_date)]
    else:
        filters = [('publish_date', '=', publish_date),
                   ('publish_hour', '=', publish_hour)]

    s3_path = 's3://ercot-62841215/load_forecast_by_weather_zone/'
    dataset = pq.ParquetDataset(s3_path, filters=filters)

    df = dataset.read().to_pandas()
    return json.loads(df.to_json(orient='records'))


# api gateway lambda handler
def lambda_handler(event, context):
    print(event)
    publish_date = event['publish_date']
    publish_hour = int(event['publish_hour'])
    delivery_date = event['delivery_date']
    return execute(publish_date, publish_hour, delivery_date)


# for local testing
if __name__ == '__main__':
    lambda_handler({'publish_date': '2023-05-20', 'publish_hour': 16, 'delivery_date': ''}, None)

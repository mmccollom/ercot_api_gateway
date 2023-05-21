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

    # convert effective_to and effective_from to string from datetime with format YYYY-MM-DD HH:MM:SS
    df['effective_to'] = df['effective_to'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['effective_from'] = df['effective_from'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # move column effective_to to the start of the dataframe
    cols = list(df.columns)
    cols.insert(0, cols.pop(cols.index('effective_to')))
    df = df[cols]

    # move column effective_from to the start of the dataframe
    cols = list(df.columns)
    cols.insert(0, cols.pop(cols.index('effective_from')))
    df = df[cols]

    # move column delivery_date to the start of the dataframe
    cols = list(df.columns)
    cols.insert(0, cols.pop(cols.index('delivery_date')))
    df = df[cols]

    print(df.head())

    return json.loads(df.to_json(orient='records'))


# api gateway lambda handler
def lambda_handler(event, context):
    print(event)
    delivery_date = event['delivery_date']
    return execute(delivery_date)


# for local testing
if __name__ == '__main__':
    lambda_handler({'delivery_date': '2023-05-20'}, None)

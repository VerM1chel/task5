from DataPreparator import DataPreparator
import mongo_pipelines


from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
import pymongo


if __name__=='__main__':
    def main():
        dp = DataPreparator('tiktok_google_play_reviews.csv')
        dp.prepare_data()
        dp.clean_text()
        dp.save_to_csv('mongo_data.csv')

        client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
        db = client['local']
        tiktok_coll = db['TikTok']
        coll = db['best_comments']
        coll.insert_many(tiktok_coll.aggregate(mongo_pipelines.best_comments_pipeline))
        coll = db['short_content']
        coll.insert_many(tiktok_coll.aggregate(mongo_pipelines.short_content_pipeline))
        coll = db['day_rating']
        coll.insert_many(tiktok_coll.aggregate(mongo_pipelines.day_rating_pipeline))


with DAG(
    dag_id='daily_report',
    default_args={
        'retries': 1,
        'retry_delay': timedelta(minutes=20)
    },
    default_view='graph',
    catchup=False,
    schedule_interval='0 0 * * *',
    start_date=datetime(2022, 8, 27),
) as dag:
    t1 = PythonOperator(
        task_id='daily',
        python_callable=main,
        depends_on_past=False,
        retries=0
    )
t1

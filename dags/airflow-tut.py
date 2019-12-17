"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# it is discouraged to use current dtg for start_date, but we are just testing
cur_dtg = datetime.now()
default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': cur_dtg,
    'email': ['xxxxxxx@minerkasch.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(cur_dtg.year, cur_dtg.month, cur_dtg.day),
}

# dag = DAG('airflow-tutorial', default_args=default_args, schedule_interval=timedelta(minutes=2), dagrun_timeout=timedelta(minutes=1))
dag = DAG('airflow-tutorial', default_args=default_args, schedule_interval=timedelta(minutes=1), catchup=False)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 1',
    retries=3,
    dag=dag)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag)

t2.set_upstream(t1)
t3.set_upstream(t1)


from airflow import DAG
from airflow.operators.subdag_operator import SubDagOperator
from airflow.operators.python_operator import PythonOperator


class DatalabQA(object):
    def __init__(self, main_dag, config_name, source):
        self.main_dag = main_dag
        self.dag_id = main_dag.dag_id
        self.default_args = self.main_dag.default_args
        self.config_name = config_name
        self.source = source

    def _subdag(self, parent_dag_name, child_dag_name, args):
        return DAG(
            dag_id='%s.%s' % (parent_dag_name, child_dag_name),
            default_args=args,
            schedule_interval="@daily",
        )

    def attach_checks(self):
        # create a subdag ( which is acctually a regular dag)
        subdag = self._subdag(self.dag_id, self.config_name, self.default_args)
        # loop through the checks and add them to the subdag
        # for i, check in enumerate(self.config_name.get('checks')):
        from datalab_qa import checks as registered_checks
        dag_name_mod = __import__(registered_checks.self.dag_id)
        check = dag_name_mod.get('')
        PythonOperator(task_id="check_{}".format(self.config_name),
            provide_context=True,
            python_callable=check,
            op_kwargs={'source':self.source},
            dag=subdag)
        # finally add the subdag to the main dag and return the subdag
        checks = SubDagOperator(
            task_id=self.config_name + '_' + self.source,
            subdag=subdag,
            default_args=self.default_args,
            dag=self.main_dag,
        )
        return checks

    # def _attach_checks(self, main_dag, check, source):
    #     operator = self._build_operator(check, source)
    #     self._attach_to_main_dag(main_dag, operator)
    #
    # def _build_operator(self, check, source):
    #     return PythonOperator()
    #
    # def _attach_main_dag(self, main_dag, parsed_config):
    #     return self.main_dag


# DAG_NAME = 'example_subdag_operator'
#
# args = {
#     'owner': 'airflow',
#     'astart_date': airflow.utils.dates.days_ago(2),
# }

# dag = DAG(
#     dag_id=DAG_NAME,
#     default_args=args,
#     schedule_interval="@once",
# )
#
# start = DummyOperator(
#     task_id='start',
#     default_args=args,
#     dag=dag,
# )
#
# section_1 = SubDagOperator(
#     task_id='section-1',
#     subdag=subdag(DAG_NAME, 'section-1', args),
#     default_args=args,
#     dag=dag,
# )
#
# some_other_task = DummyOperator(
#     task_id='some-other-task',
#     default_args=args,
#     dag=dag,
# )
#
# section_2 = SubDagOperator(
#     task_id='section-2',
#     subdag=subdag(DAG_NAME, 'section-2', args),
#     default_args=args,
#     dag=dag,
# )
#
# end = DummyOperator(
#     task_id='end',
#     default_args=args,
#     dag=dag,
# )
#
# start.set_downstream(section_1)
# section_1.set_downstream(some_other_task)
# some_other_task.set_downstream(section_2)
# section_2.set_downstream(end)

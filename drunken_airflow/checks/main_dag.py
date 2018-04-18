# import spark
# from pyddq.core import Check

from drunken_airflow.checks.base_check import BaseCheck

class ConfigName(BaseCheck):
    def __init__(self):
        super(ConfigName).__init__()

    def checks(self, source):
        # df = spark.createDataFrame(source)
        # check = Check(df)
        # check.hasUniqueKey("column1").isNeverNull("column2").run()
        print 'checking df'


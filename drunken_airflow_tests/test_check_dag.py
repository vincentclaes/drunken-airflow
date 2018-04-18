import unittest

from drunken_airflow.subdag_qc import SubdagQC


class MockDag(object):
    def __init__(self):
        self.dag_id = 'main_dag'
        self.default_args = {}


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mdag = MockDag()
        dlqa = SubdagQC(mdag, 'ConfigName', 'my_file')
        dlqa.attach_checks()

    def test_something(self):
        self.assertEqual(True, False)

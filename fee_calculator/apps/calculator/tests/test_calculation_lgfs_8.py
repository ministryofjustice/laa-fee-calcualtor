# -*- coding: utf-8 -*-
import csv
from decimal import Decimal
import os

from rest_framework import status

from calculator.tests.lib.utils import scenario_clf_to_id
from calculator.tests.calculation_utils import (
    CalculatorTestCase, get_test_name, make_test
)


LGFS_CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    'data/test_dataset_lgfs.csv'
)


class Lgfs8CalculatorTestCase(CalculatorTestCase):
    scheme_id = 2

    def assertRowValuesCorrect(self, row):
        """
        Assert row values equal calculated values
        """
        data = {
            'scheme': self.scheme_id,
            'fee_type_code': row['BILL_SUB_TYPE'],
            'scenario': scenario_clf_to_id(row['SCENARIO']),
            'offence_class': row['OFFENCE_CATEGORY'],
            'day': int(row['TRIAL_LENGTH']) if row['TRIAL_LENGTH'] else 0,
            'ppe': int(row['EVIDENCE_PAGES']) if row['EVIDENCE_PAGES'] else 0
        }

        if row['NO_DEFENDANTS']:
            data['NUMBER_OF_DEFENDANTS'] = int(row['NO_DEFENDANTS'])

        resp = self.client.get(self.endpoint(), data=data)
        self.assertEqual(
            resp.status_code, status.HTTP_200_OK, resp.content
        )

        self.assertEqual(
            resp.data['amount'],
            Decimal(row['CALC_FEE_EXC_VAT']),
            data
        )


def create_tests():
    """
    Insert test methods into the TestCase for each case in the spreadsheet
    """

    with open(LGFS_CSV_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            setattr(
                Lgfs8CalculatorTestCase,
                get_test_name('lgfs', row, i+2),
                make_test(row, i+2)
            )


create_tests()

# -*- coding: utf-8 -*-
import csv
from datetime import datetime
from decimal import Decimal
from math import floor
import os

from django.conf import settings
from django.test import TestCase
from rest_framework import status

from calculator.models import Price, FeeType
from .lib.utils import scenario_ccr_to_id


CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    'data/test_dataset.csv'
)


class CalculatorTestCase(TestCase):
    fixtures = [
        'advocatetype', 'feetype', 'offenceclass', 'price', 'scenario',
        'scheme', 'unit', 'modifiertype', 'modifier',
    ]

    def endpoint(self, scheme_id):
        return '/api/{version}/fee-schemes/{scheme_id}/calculate/'.format(
            version=settings.API_VERSION, scheme_id=scheme_id
        )

    def assertRowValuesCorrect(self, row):
        """
        Assert row values equal calculated values
        """
        calc_date_str = row['REP_ORD_DATE']
        if calc_date_str:
            if len(calc_date_str) > 10:
                calc_date_str = calc_date_str[:-9]
            calculation_date = datetime.strptime(
                calc_date_str, '%d/%m/%Y'
            ).date()
        else:
            calculation_date = datetime.now().date()

        is_basic = row['BILL_SUB_TYPE'] == 'AGFS_FEE'

        # get scheme for date
        scheme_resp = self.client.get(
            '/api/{version}/fee-schemes/'.format(version=settings.API_VERSION),
            data=dict(supplier_type='advocate', case_date=calculation_date)
        )
        self.assertEqual(
            scheme_resp.status_code, status.HTTP_200_OK, scheme_resp.content
        )
        self.assertEqual(scheme_resp.json()['count'], 1)
        scheme_id = scheme_resp.json()['results'][0]['id']

        data = {
            'scheme': scheme_id,
            'fee_type_code': row['BILL_SUB_TYPE'],
            'scenario': scenario_ccr_to_id(
                row['BILL_SCENARIO_ID'], row['THIRD_CRACKED'] or 3),
            'advocate_type': row['PERSON_TYPE'],
            'offence_class': row['OFFENCE_CATEGORY'],
        }

        unit = 'DAY'
        if not is_basic:
            # get unit for fee type
            unit_resp = self.client.get(
                '/api/{version}/fee-schemes/{scheme_id}/units/'.format(
                    version=settings.API_VERSION, scheme_id=scheme_id),
                data=data
            )
            self.assertEqual(
                unit_resp.status_code, status.HTTP_200_OK, unit_resp.content
            )
            self.assertEqual(unit_resp.json()['count'], 1, data)
            unit = unit_resp.json()['results'][0]['id']

        data['unit'] = unit
        data['unit_count'] = (
            Decimal(row['NUM_ATTENDANCE_DAYS'])
            if row['BILL_TYPE'] == 'AGFS_FEE'
            else Decimal(row['QUANTITY'])
        ) or 1,

        if row['NUM_OF_CASES']:
            data['modifier_1'] = int(row['NUM_OF_CASES'])
        if row['NO_DEFENDANTS']:
            data['modifier_2'] = int(row['NO_DEFENDANTS'])
        if row['TRIAL_LENGTH']:
            data['modifier_3'] = int(row['TRIAL_LENGTH'])
        if row['PPE']:
            data['modifier_4'] = int(row['PPE'])
        if row['MONTHS']:
            data['modifier_5'] = floor(abs(Decimal(row['MONTHS'])))

        fees = {}

        resp = self.client.get(self.endpoint(scheme_id), data=data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.content)
        fees['basic'] = resp.data['amount']

        if is_basic:
            if row['PPE']:
                data['unit'] = 'PPE'
                data['unit_count'] = int(row['PPE'])

                resp = self.client.get(self.endpoint(scheme_id), data=data)
                self.assertEqual(
                    resp.status_code, status.HTTP_200_OK, resp.content
                )
                fees['ppe'] = resp.data['amount']

            if row['NUM_OF_WITNESSES']:
                data['unit'] = 'PW'
                data['unit_count'] = int(row['NUM_OF_WITNESSES'])

                resp = self.client.get(self.endpoint(scheme_id), data=data)
                self.assertEqual(
                    resp.status_code, status.HTTP_200_OK, resp.content
                )
                fees['pw'] = resp.data['amount']

        total = sum(fees.values())
        self.assertEqual(
            total,
            Decimal(row['CALC_FEE_EXC_VAT']),
            '%s %s' % (fees, data,)
        )


def test_name(row, line_number):
    """
    Generate the method name for the test
    """
    return 'test_{0}_{1}'.format(
        line_number,
        row.get('CASE_ID')
    )


test_name.__test__ = False


def make_test(row, line_number):
    """
    Generate a test method
    """
    def row_test(self):
        self.assertRowValuesCorrect(row)
    row_test.__doc__ = str(line_number) + ': ' + str(row.get('CASE_ID'))
    return row_test


make_test.__test__ = False


def create_tests():
    """
    Insert test methods into the TestCase for each case in the spreadsheet
    """
    with open(CSV_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        priced_fees = FeeType.objects.filter(
            id__in=Price.objects.all().values_list('fee_type_id', flat=True).distinct()
        ).values_list('code', flat=True).distinct()
        for i, row in enumerate(reader):
            if row['BILL_SUB_TYPE'] in priced_fees:
                setattr(CalculatorTestCase, test_name(row, i+2), make_test(row, i+2))


create_tests.__test__ = False

create_tests()

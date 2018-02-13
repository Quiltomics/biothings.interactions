# -*- coding: utf-8 -*-
"""
Test classes for parsing protein interaction files.

Author:  Greg Taylor (greg.k.taylor@gmail.com)
"""
import os
import unittest
import tempfile

from hub.dataload.sources.ctdchemgene.parser import CTDChemGeneParser


class TestParserMethods(unittest.TestCase):
    """
    Test class for CTD parser functions.

    The datasets were extracted from a debugging screen query, results were pruned down to one entry
    and results were manually validated.
    """

    ctdFile = os.path.join(os.path.dirname(__file__), 'test_data/CTD_chem_gene_ixns.tsv')

    def test_ctdchemgene_parse(self):
        """
        Parse a test hint file, gather statistics, and assess results
        :return:
        """
        # Write the contents of the test ConsenesusPathDB file to a temporary file object
        test_file = open(TestParserMethods.ctdFile, mode="r")
        ctd = []
        for record in CTDChemGeneParser.parse_tsv_file(test_file):
            ctd.append(record)

        ########################################################
        # Gather some useful statistics of the resulting dataset
        ########################################################

        self.assertGreater(self._list_average(ctd, 'pubmedids'), 1.5)
        self.assertGreater(self._list_average(ctd, 'interactionactions'), 2)

    def _num_values(self, records, field):
        """
        Compute the total number of non NoneType values for a field in a given record.
        :param records:
        :param field:
        :return:
        """
        # Number of records with non-null values
        total = 0
        for _r in records:
            for _f in _r['biogrid']:
                if field in _f.keys():
                    total = total + 1
        return total

    def _total(self, records, field):
        """
        Compute the sum total over the test dataset for a given record field.
        :param records:
        :param field:
        :return:
        """
        # Number of records with non-null values
        total = 0
        for _r in records:
            for _f in _r['hint']:
                if _f[field]:
                    total = total + _f[field]
        return total

    def _list_count(self, records, field):
        """
        Compute the count of list elements over the test dataset for a given record field.
        :param records:
        :param field:
        :return:
        """
        count = 0
        for _r in records:
            for _f in _r['ctd']:
                if field in _f:
                    count = count + len(_f[field])
        return count

    def _list_average(self, cpd, field):
        """
        Compute the average number of list elements over the test dataset for a given record field.
        :param cpd:
        :param field:
        :return:
        """
        count = self._list_count(cpd, field)
        return count / len(cpd)

    def _record_average(self, records, field1, field2):
        """
        Compute the average number of list elements over the test dataset for a given record field.
        :param cpd:
        :param field:
        :return:
        """
        count = 0
        for _r in records:
            if field1 in _r.keys() and field2 in _r[field1].keys():
                count = count + len(_r[field1][field2])
        return count / len(records)

    def _find20(self, records, field):
        """

        :param records:
        :param field:
        :return:
        """
        i = 0
        for r in records:
            if r[field]:
                print("%s:%s" % (field, r[field]))
                i = i + 1
            if i >= 20:
                break
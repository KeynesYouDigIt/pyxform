"""
Tests by file. Runs through a list of *.xls files, and expects that the output for a *.xml
with a matching prefix before the . is as expected. Possibly risky: all tests in this file
are defined according to matching files. 
"""

from lxml import etree
from formencode.doctest_xml_compare import xml_compare
from unittest import TestCase
import pyxform
from pyxform import xls2json
import os
from pyxform.tests import utils
import codecs
import sys


class MainTest(TestCase):
    
    def runTest(self):
        files_to_test = ["instance_xmlns_test.xls"]
        for file_to_test in files_to_test:
            path_to_excel_file = utils.path_to_text_fixture(file_to_test)
            
            # Get the xform output path:
            directory, filename = os.path.split(path_to_excel_file)
            root_filename, ext = os.path.splitext(filename)
            path_to_output_xform = os.path.join(
                directory, root_filename + "_output.xml")
            path_to_expected_xform = os.path.join(
                directory, root_filename + ".xml")

            # Do the conversion:
            json_survey = xls2json.parse_file_to_json(path_to_excel_file)
            survey = pyxform.create_survey_element_from_dict(json_survey)
            survey.print_xform_to_file(path_to_output_xform)
            
            # Compare with the expected output:
            with codecs.open(path_to_expected_xform, 'rb', encoding="utf-8"
                             ) as expected_file:
                expected = etree.fromstring(expected_file.read())
                result = etree.fromstring(survey.to_xml())
                reporter = lambda x: sys.stdout.write(x + "\n")
                self.assertTrue(xml_compare(
                    expected, result, reporter=reporter))
            os.remove(path_to_output_xform)

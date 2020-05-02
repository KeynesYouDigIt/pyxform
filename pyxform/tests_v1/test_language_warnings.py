# -*- coding: utf-8 -*-
"""
Test language warnings.
"""
import os
import tempfile

from pyxform.tests_v1.pyxform_test_case import PyxformTestCase


class LanguageWarningTest(PyxformTestCase):
    """
    Test language warnings.
    """

    def test_label_with_valid_subtag_should_not_warn(self):
        survey = self.md_to_pyxform_survey(
            """
            | survey |      |         |                     |
            |        | type | name    | label::English (en) |
            |        | note | my_note | My note             |
            """
        )

        warnings = []
        tmp = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
        tmp.close()
        survey.print_xform_to_file(tmp.name, warnings=warnings)

        self.assertTrue(len(warnings) == 0)
        os.unlink(tmp.name)

    def test_label_with_no_subtag_should_warn(self):
        survey = self.md_to_pyxform_survey(
            """
            | survey |      |         |                     |
            |        | type | name    | label::English      |
            |        | note | my_note | My note             |
            """
        )

        warnings = []
        tmp = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
        tmp.close()
        survey.print_xform_to_file(tmp.name, warnings=warnings)

        self.assertTrue(len(warnings) == 1)
        self.assertTrue(
            "do not contain valid machine-readable codes: English. Learn more"
            in warnings[0]
        )
        os.unlink(tmp.name)

    def test_label_with_unknown_subtag_should_warn(self):
        survey = self.md_to_pyxform_survey(
            """
            | survey |      |         |                       |
            |        | type | name    | label::English (schm) |
            |        | note | my_note | My note               |
            """
        )

        warnings = []
        tmp = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
        tmp.close()
        survey.print_xform_to_file(tmp.name, warnings=warnings)

        self.assertTrue(len(warnings) == 1)
        self.assertTrue(
            "do not contain valid machine-readable codes: English (schm). Learn more"
            in warnings[0]
        )
        os.unlink(tmp.name)

    def test_missing_translation_no_default_lang_media_has_no_language(self):
        # form should test media tag w NO default language set.
        survey = self.md_to_pyxform_survey(
            """
            | survey  |                 |         |                     |             |
            |         | type            | name    | label::English (en) | media::image|
            |         | integer         | nums    | How many nums?      | opt1.jpg    |
            """
        )

        warnings = []
        tmp = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
        tmp.close()
        survey.print_xform_to_file(tmp.name, warnings=warnings)
        self.assertTrue(len(warnings) == 2)

        # First warning explains the problem and correctly gets the 
        # language, question, and attribute.
        import ipdb; ipdb.set_trace()
        self.assertTrue("Missing translation for content" in warnings[0])
        self.assertTrue("English (en)" in warnings[0])
        self.assertTrue("nums" in warnings[0])
        self.assertTrue("image" in warnings[0])
        self.assertTrue("A `default_language` has not been set on this form." in warnings[1])

        os.unlink(tmp.name)
    
    def xtest_missing_translation_default_language_clears_warning(self):
        # form should test media tag w NO default language set.
        survey = self.md_to_pyxform_survey(
            """
            | survey  |                 |         |                     |              |
            |         | type            | name    | label::English (en) | media::image |
            |         | integer         | nums    | How many nums?      | opt1.jpg     |
            """
        )

        warnings = []
        tmp = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
        tmp.close()
        survey.print_xform_to_file(tmp.name, warnings=warnings)

        # In this survey, when 'default' s selected the label of this question will be '-'.
        # Also, when 'English (en)` is selected, the medial will be '-'
        self.assertTrue(len(warnings) == 1)
        os.unlink(tmp.name)

    def xtest_missing_translation_media(self):
        # this is most similar to situation that prompted this feature
        # 
        survey = self.md_to_pyxform_survey(
            """
            | survey   |                  |         |                     |                    |                           |
            |          | type             | name    | label::English (en) | label::French (fr) | media::image::French (fr) |
            |          | integer          | nums    | How many nums?      | Combien noms?      | opt1.jpg                  |
            | settings |                  |         |                     |                    |                           |
            |          | default_langauge |
            |          | English (en)     |
            """
        )

        warnings = []
        tmp = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
        tmp.close()
        survey.print_xform_to_file(tmp.name, warnings=warnings)
        self.assertTrue(len(warnings) == 1)
        self.assertIn(
            "Question missing translation: /pyxform_autotestname/nums", warnings[0]
        )
        self.assertIn("Column missing: image", warnings[0])
        os.unlink(tmp.name)

    def xtest_missing_translation_hint(self):
        survey = self.md_to_pyxform_survey(
            """
            | survey  |                 |         |                     |                    |                   |
            |         | type            | name    | label::English (en) | label::French (fr) | hint::French (fr) |
            |         | integer         | nums    | How many nums?      | Combien noms?      | noms est nombres  |
            """
        )

        warnings = []
        tmp = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
        tmp.close()
        survey.print_xform_to_file(tmp.name, warnings=warnings)
        self.assertTrue(len(warnings) == 1)
        self.assertIn(
            "Question missing translation: /pyxform_autotestname/nums", warnings[0]
        )
        self.assertIn("Column missing: hint", warnings[0])
        os.unlink(tmp.name)

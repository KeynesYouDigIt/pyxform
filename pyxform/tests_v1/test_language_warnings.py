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

    def test_reprod_issue_355(self):
        survey = self.md_to_pyxform_survey(
            """
            | survey  |                    |          |                     |                    |
            |         | type               | name     | label::English (en) | choice-filter      |
            |         | select_one country | country  | Country             |                    |
            |         | select_one city    | city     | City                | country=${country} |
            | choices |                    |          |                     |                    |
            |         | list_name          | name     | label               |                    |
            |         | country            | france   | France              |                    |
            |         | country            | canada   | Canada              |                    |
            |         | city               | grenoble | Grenoble            |                    |
            |         | city               | quebec   | Quebec              |                    |
            """
        )

        warnings = []
        tmp = tempfile.NamedTemporaryFile(suffix=".xml", delete=False)
        tmp.close()
        survey.print_xform_to_file(tmp.name, warnings=warnings)

        self.assertTrue(len(warnings) == 0)
        os.unlink(tmp.name)


    def test_translations_and_choice_filters(self):
        self.assertPyxformXform(
            name="translations_choice_filters",
            id_string="transl",
            md="""
            | survey  |                    |          |                     |                    |
            |         | type               | name     | label::English (en) | choice_filter      |
            |         | select_one country | country  | Country             |                    |
            |         | select_one city    | city     | City                | country=${country} |
            | choices |                    |          |                     |                    |
            |         | list_name          | name     | label               |                    |
            |         | country            | france   | France              |                    |
            |         | country            | canada   | Canada              |                    |
            |         | city               | grenoble | Grenoble            |                    |
            |         | city               | quebec   | Quebec              |                    |
            """,
            errored=False,
            debug= True
        )

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

        # In this survey, when 'default' s selected the label of this question will be '-'.
        # Also, when 'English (en)` is selected, the medial will be '-'
        self.assertTrue(len(warnings) == 2)
        os.unlink(tmp.name)


    
    def test_default_language_clears_warning(self):
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

        # In this survey, when 'default' s selected the label of this question will be '-'.
        # Also, when 'English (en)` is selected, the medial will be '-'
        self.assertTrue(len(warnings) == 2)
        os.unlink(tmp.name)

    def test_missing_translation_media(self):
        survey = self.md_to_pyxform_survey(
            """
            | survey  |                 |         |                     |                    |                          |
            |         | type            | name    | label::English (en) | label::French (fr) | media::image::French (fr)|
            |         | integer         | nums    | How many nums?      | Combien noms?      | opt1.jpg                 |
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

    def test_missing_translation_hint(self):
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

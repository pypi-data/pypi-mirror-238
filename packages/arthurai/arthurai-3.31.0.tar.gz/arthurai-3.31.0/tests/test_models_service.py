import pandas as pd

from arthurai.common.constants import ValueType
from arthurai.core.attributes import AttributeCategory
from arthurai.core.models import ArthurModel


class TestModelsServiceObject:

    def test_get_attribute_data(self):
        """
        Currently, tests that float attributes that only take on values of
        0.0 or 1.0 are converted to categorical.
        """

        value_type = ValueType.Float

        df = pd.DataFrame({
            'float_binary': [0.0, 1.0, 1.0, 1.0, 0.0],
            'true_float': [0.0, 0.2, 0.4, 0.6, 0.8]
        })

        binary_attr = ArthurModel._get_attribute_data(value_type, df.float_binary)
        float_attr = ArthurModel._get_attribute_data(value_type, df.true_float)

        assert binary_attr["categorical"] is True
        assert float_attr["categorical"] is False

    def test_unstructured_text_get_attribute_data(self):
        """
        Ensure non-unique unstructured text attributes don't get
        categories
        """
        value_type = ValueType.Unstructured_Text
        df = pd.DataFrame({
            "text": ["test", "test", "more", "things"],
            "target": [0,1,2,3]
        })

        text_attr = ArthurModel._get_attribute_data(value_type, df.text)

        assert text_attr['is_unique'] == False
        assert text_attr['categorical'] == True
        assert 'categories' not in text_attr

    def test_categories_ordering_get_attribute_data(self):
        df_float = pd.DataFrame({
            'float_binary': [0.0, 1.0, 1.0, 1.0, 0.0],
        })

        df_string = pd.DataFrame({
            'strings': ["five", "two", "six", "three", "three", "four", "four", "one", "four", "four", "five",
                        "five", "six", "five", "five", "six", "three", "six", "six", "two", "six"]
        })

        float_ordering = [AttributeCategory(value=1.0), AttributeCategory(value=0.0)]
        strings_ordering = [AttributeCategory(value="six"), AttributeCategory(value="five"),
                            AttributeCategory(value="four"), AttributeCategory(value="three"),
                            AttributeCategory(value="two"), AttributeCategory(value="one")]

        binary_attr = ArthurModel._get_attribute_data(ValueType.Float, df_float.float_binary)
        string_attr = ArthurModel._get_attribute_data(ValueType.String, df_string.strings)

        assert binary_attr["categories"] == float_ordering
        assert string_attr["categories"] == strings_ordering

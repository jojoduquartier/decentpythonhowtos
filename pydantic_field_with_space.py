from pydantic.fields import Field
from pydantic import BaseModel, BaseConfig
from pydantic.class_validators import Validator
from pydantic.error_wrappers import ValidationError


def f(string):
    if isinstance(string, str):
        return string
    raise ValidationError([], Test)


"""
Things to try:

1) instead of f which returns the data when successful, use a function like: lambda x: isinstance(x, str)
    * the data returned will be booleans instead of the actual values 
2) play with the pre, each_item etc. params of the Validator class
"""

# there is already a string validation class. look into it
string_validator = Validator(
    f,
    True,
    True,
    True,
    True
)


class Test(BaseModel):
    __fields__ = {
        'field1': Field(
            name='field1',
            type_=str,
            class_validators={'field1': string_validator},
            model_config=BaseConfig
        ),
        'field 2': Field(
            name='field 2',
            type_=str,
            class_validators=None,
            # class_validators={'field 2': string_validator},
            model_config=BaseConfig
        ),
        'field3': Field(
            name='field3',
            alias='field with space',
            type_=str,
            class_validators=None,
            model_config=BaseConfig,
            required=False
        ),
    }


# normal stuff
data = {
    'field1': 'lola',
    'field 2': 'some data',
    'field with space': 'spacy'
}

test = Test(**data)
print(test.json())
print('------')

# checking if integers are ok - this works. In fact even with a regular default BaseModel, integers are converted
# to string properly and no validation error takes place. As a result, if we actually used string_validator for
# field 2 and the `pre` param of our Validator object is False, no errors would come up. But if `pre` is True, the data
# is checked to be an instance of string first before the normal pydantic validator.
data = {
    'field1': 'lola',
    'field 2': 23
}

test = Test(**data)
print(test.json())
print('------')

# checking if the required default of True takes effect
data = {
    'field1': 'lola',
    'field 2': None
}

try:
    test = Test(**data)
    print(test.json())
except Exception as e:
    print(e)
print('------')

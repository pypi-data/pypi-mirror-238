# COPYRIGHT 2022 MONOOCLE INSIGHTS
# ALL RIGHTS RESERVED
# UNAUTHORIZED USE, REPRODUCTION, OR
# DISTRIBUTION STRICTLY PROHIBITED
#
# AUTHOR: Sean O'Malley and Raymond Deiotte
# CREATION DATE: 20230802
# LAST UPDATED: 20230821

### Import Packages/Dependencies ###

# basic

# custom
#Use for PyPi packaging
import care_query.care_query_utils as cqu

#Use for local testing
# import care_query_utils as cqu


### Field Value Data Class ###
class FieldValueData:

    def __init__(self, data):

        self.data = data

    def list_fields(self, contains = None):

        # list fields
        fields = list(self.data.keys())

        if contains != None:

            # normalize field string
            contains = cqu.stringNorm(contains)

            fields = [x for x in fields if contains in x]

        return fields

    def list_values(self, field, contains = None):

        # normalize field string
        field = cqu.stringNorm(field)

        try:

            # get corresponding values
            values = list(self.data[field])

            if contains != None:

                # normalize value_contains string
                contains = cqu.stringNorm(contains)

                values = [x for x in values if contains in x]

            return values
            
        except:
            raise ValueError(f"{field} is not an available field, please reference self.field_values.list_fields() for full list of options.")

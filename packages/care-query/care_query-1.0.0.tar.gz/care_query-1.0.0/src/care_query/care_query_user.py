# COPYRIGHT 2022 MONOOCLE INSIGHTS
# ALL RIGHTS RESERVED
# UNAUTHORIZED USE, REPRODUCTION, OR
# DISTRIBUTION STRICTLY PROHIBITED
#
# AUTHOR: Sean O'Malley and Raymond Deiotte
# CREATION DATE: 20230802
# LAST UPDATED: 20230821

### Import Packages/Dependencies ###

### Query User Class ###
class UserProfile:

    def __init__(self, email, token):

        # fill in for now, will come from API call
        # self.email = "somalley@monocleinsights.com"
        self.email = email
        self.token = token
        self.state_access = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
        self.journey_access = True
        self.supplemental_access = True
        self.aggregate_access = True
        self.pharmacy_access = True


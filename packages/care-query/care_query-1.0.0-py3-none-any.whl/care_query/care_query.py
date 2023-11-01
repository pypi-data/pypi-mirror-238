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
import json
from datetime import date, timedelta
import importlib.resources

import dateutil.parser

# custom
#Use to build the pypi package
import care_query.care_query_utils as cqu
from care_query.care_query_data import CareQueryData
from care_query.care_query_user import UserProfile
from care_query.field_value_data import FieldValueData
from care_query.glossary import DataGlossary

#Use for Local Running and testing
# import care_query_utils as cqu
# from care_query_data import CareQueryData
# from care_query_user import UserProfile
# from field_value_data import FieldValueData
# from glossary import DataGlossary



# connection

### Query Builder Class ###
class CareQuery:

    def __init__(self, email, token):

        # initialize: user profile
        self.user = UserProfile(email, token)

        # read field value json - move to CQ_Class or CQUtils
        #TODO: Use this for the pypi distro
        with importlib.resources.open_text('care_query','field-values.json') as f:
            field_values = json.load(f)

        # #TODO: Uncomment and use this for local testing
        # with open('field-values.json', 'r') as f:
        #     field_values = json.load(f)


        ### initialize: field values
        self.field_values = FieldValueData(field_values)

        # initialize: data result features
        self.glossary = DataGlossary()

    def careEncounter(self, 
                    min_date = None,
                    max_date = None,
                    gender = None,
                    age_min = None,
                    age_max = None,
                    visit_type = None,
                    payor_channel = None,
                    revenue_center_code = None,
                    place_of_service = None, 
                    drg_code = None,
                    drg_category = None,
                    drg_greedy = None,
                    diag_code = None,
                    diag_category = None,
                    diag_subcategory = None,
                    short_diag_code = None,
                    diag_greedy = None,
                    proc_code = None,
                    proc_category = None,
                    proc_subcategory = None,
                    proc_greedy = None,
                    taxonomy_code = None,
                    specialty_category = None,
                    specialty = None,
                    subspecialty = None,
                    taxonomy_greedy = None,
                    ref_npi = None,
                    npi = None,
                    state = None,
                    division = None,
                    region = None,
                    metro = None,
                    short_zip = None,
                    limit = None,
                    show = None):
        
        """
        Description:
        
            Specify encounter-based query parameters to construct a query object. From which the .execute() method on this query will return line-item level patient journey detail for healthcare encounters that meet the query criterion. We define an encoutner as a single, billiable healthcare instance of care.

        Parameters:
            min_date (str):
                Lower threshold date within the date range of interest, observational start date
                option(s): "2023-01-01" or "01/01/2023" 
                default: 90 days prior to date of query
            max_date (str):
                Upper threshold date within the date range of interest, observational end date
                option(s): "2023-01-01" or "01/01/2023" 
                default: 30 days prior to date of query
            gender (str or list(str)):
                Patient gender within the population of interest
                option(s): 'M' for Male, 'F' for Female, or ['M','F'] for both
                default(s): ['M','F']
            age_min (int):
                Minimum patient age identified within the population of interest
                option(s): 0 to 120
                default: 0
            age_max (int):
                Maximum patient age identified within the population of interest
                option(s): 0 to 120
                default: 120
            visit_type (str or list(str) or list(list(str),list(str))):
                Description of the setting of care
                option(s): Run self.field_values.list_values(field = "visit_type") to see all visit_type options
                default(s): Defaults to all visit types if left unspecified
            payor_channel (str or list(str) or list(list(str),list(str))):
                Health Insurance Payor channel-of-business or line-of-business
                option(s): Run self.field_values.list_values(field = "payor_channel") to see all payor_channel options
                default(s): Defaults to all payor channels if left unspecified
            revenue_center_code (str or list(str) or list(list(str),list(str))):
                4-digit code used to identify a specific accommodation, ancillary service, or billing calculation on a hospital bill
                option(s): Run self.field_values.list_values(field = "revenue_center_code") to see all revenue_center_code options
                default(s):  Defaults to all revenue codes if left unspecified
            place_of_service (str or list(str) or list(list(str),list(str))):
                Setting in which a healthcare service was provided by healthcare providers, insurers, and government agencies to track and bill for healthcare services
                option(s): Run self.field_values.list_values(field = "place_of_service") to see all place_of_service options
                default(s): Defaults to all places of service if left unspecified
            drg_code (str or list(str) or list(list(str),list(str))):
                Diagnosis related group (DRG) is how insurance payors categorize hospitalization costs to determine payment requirement. DRG is based on your primary and secondary diagnoses, other conditions (comorbidities), age, sex, and necessary medical procedures. 
                option(s): Run self.field_values.list_values(field = "drg_code") to see all drg options
                default(s): Defaults to all drg codes if left unspecified
            drg_category (str or list(str) or list(list(str),list(str))):
                Diagnosis related group (DRG) medical diagnosis categories help reduce request dimensionality
                option(s): Run self.field_values.list_values(field = "drg_category") to see all drg category options
                default(s): Defaults to any/all drg categories if left unspecified
            drg_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple drg parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified drg needs to be present within the returned results, False indicates all drg must be present for the returned results
                default: True
            diag_code (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis code assigned to the patient
                option(s): Run self.field_values.list_values(field = "diag_code") to see all diag_code options
                default(s): Defaults to all diagnosis codes if left unspecified
            diag_category (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis category assigned to the patient
                option(s): Run self.field_values.list_values(field = "diag_category") to see all diag_category options
                default(s): Defaults to all diagnosis categories if left unspecified
            diag_subcategory (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis subcategory assigned to the patient
                option(s): Run self.field_values.list_values(field = "diag_subcategory") to see all diag_subcategory options
                default(s): Defaults to all diagnosis subcategories if left unspecified
            short_diag_code (str or list(str) or list(list(str),list(str))):
                First three digits of ICD-10 code assigned to the patient
                option(s): Run self.field_values.list_values(field = "short_diag_code") to see all short_diag_code options
                default(s): Defaults to all short diagnosis codes if left unspecified
            diag_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple diagnosis parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified diagnosis needs to be present within the returned results, False indicates all diagnosis must be present for the returned results
                default: True
            proc_code (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural code performed
                option(s): Run self.field_values.list_values(field = "proc_code") to see all proc_code options
                default(s): Defaults to all procedure codes if left unspecified
            proc_category (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural category performed
                option(s): Run self.field_values.list_values(field = "proc_category") to see all proc_category options
                default(s): Defaults to all procedure categories if left unspecified
            proc_subcategory (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural subcategory performed
                option(s): Run self.field_values.list_values(field = "proc_subcategory") to see all proc_subcategory options
                default(s): Defaults to all procedure subcategories if left unspecified
            proc_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple procedure parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified procedure needs to be present within the returned results, False indicates all procedures within sub-lists must be present for the returned results
                default: True
            taxonomy_code (str or list(str) or list(list(str),list(str))):
                Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider
                option(s): Run self.field_values.list_values(field = "taxonomy_code") to see all taxonomy_code options
                default(s): Defaults to all taxonomy codes if left unspecified
            specialty (str or list(str) or list(list(str),list(str))):
                Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty") to see all specialty options
                default(s): Defaults to all specialties if left unspecified
            specialty_category (str or list(str) or list(list(str),list(str))):
                Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty_category") to see all specialty_category options
                default(s): Defaults to all specialty categories if left unspecified
            subspecialty (str or list(str) or list(list(str),list(str))):
                Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "subspecialty") to see all subspecialty options
                default(s): Defaults to all specialty subcategories if left unspecified
            taxonomy_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple taxonomy or specialty parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified taxonomy or specialty needs to be present within the returned results, False indicates all taxonomy or specialty must be present for the returned results
                default: True
            ref_npi (int or list(int) or list(list(int),list(int))):
                Referring provider(s) indicated by National Provider Identifiers (NPIs)
                option(s): Any valid, registered individual National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            npi (int or list(int) or list(list(int),list(int))):
                National Provider Identifier (NPI) of individual and organizational provider(s) of interest
                option(s): Any valid, registered individual or organizational National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            state (str or list(str) or list(list(str),list(str))):
                option(s): Run self.field_values.list_values(field = "state") to see all state options
                default(s): Defaults to all US States if left unspecified
            division (str or list(str) or list(list(str),list(str))):
                District residence of the query patient population. There are nine distinct US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "division") to see all division options
                default(s): Defaults to all entire US population if left unspecified
            region (str or list(str) or list(list(str),list(str))):
                Regional residence of the query patient population. There are four major US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "region") to see all region options
                default(s): Defaults to all entire US population if left unspecified
            metro (str or list(str) or list(list(str),list(str))):
                Metropolitan and micropolitan statistical areas according to the US Census Bureau
                option(s): Run self.field_values.list_values(field = "metro") to see all metro options
                default(s): Defaults to all entire US population if left unspecified
            short_zip (int or list(int) or list(list(int),list(int))):
                First three digits the zip code of the query patient population specified
                option(s): Run self.field_values.list_values(field = "short_zip") to see all short_zip options
                default(s): Defaults to all entire US population if left unspecified 
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: 10000
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: state = "NE"
                    example logic: Select data from the state of Nebraska
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: state = ["NE","CO"]
                    example logic: Select data from either Nebraska OR Colorado
                multi-selection AND: Select multiple values across multiple lists to request results that meet both conditions
                    example: short_diag_code = [["I10"],["E11"]]
                    example logic: Select data where patients have hypertension (I10) AND type-2 diabetes (E11)
            inter-parameter: Logical arguments ACROSS parameter specifications
                multi-selection AND: (default) Return data that meets both criterion
                    example: self.encounter(state = "NE", short_diag_code = ["I10"])
                    example logic: Select all hypertensive encounters in Nebraska
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if min_date == None:
            temp = date.today() - timedelta(days=30)
            min_date = temp.strftime("%Y-%m-%d")
            print(min_date)
        if max_date == None:
            temp = date.today() - timedelta(days=90)
            max_date = temp.strftime("%Y-%m-%d")
            print(max_date)
        if age_min == None:
            age_min = 0
        if age_max == None:
            age_max = 120
        if gender == None:
            gender = ["M","F"]
        if limit == None:
            limit = 10000
        elif (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"drg_category":drg_category, "gender" : gender, "visit_type" : visit_type, "payor_channel" : payor_channel, "revenue_center_code" : revenue_center_code, "place_of_service" :  place_of_service, "diag_code" : diag_code, "short_diag_code" : short_diag_code, "diag_category":diag_category, "diag_subcategory": diag_subcategory, "proc_code" : proc_code, "proc_category":proc_category, "proc_subcategory":proc_subcategory, "taxonomy_code" : taxonomy_code, "subspecialty": subspecialty, "specialty" : specialty, "specialty_category" : specialty_category, "ref_npi" : ref_npi, "npi" : npi, "state" : state, "division" : division, "region" : region, "metro" : metro, "short_zip" : short_zip}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # ensure valid date data type 
        dates = {"min_date" : min_date, "max_date" : max_date}
        for x in list(dates.items()):
            if x[1] != None:
                if type(x[1]) == str:
                    cqu.checkTypeDate(dateutil.parser.parse(x[1]).date(), x[0])
                else:
                    cqu.checkTypeDate(x[1], x[0])

        # ensure valid integer data type
        ints = {"limit" : limit, "age_min" : age_min, "age_max" : age_max}
        for x in list(ints.items()):
            if (x[1] != None):
                cqu.checkTypeInt(x[1], x[0])

        # normalize NPI output
        ref_npi = cqu.NPINorm(ref_npi)
        npi = cqu.NPINorm(npi)

        # raise error for invalid NPIs
        cqu.checkNPI(ref_npi, "ref_npi")
        cqu.checkNPI(npi, "npi")

        ### Input Quality Control ###

        # normalize code digit input
        drg_code = cqu.codeNorm(drg_code, n = 3, punct = False)
        revenue_center_code = cqu.codeNorm(revenue_center_code, n = 4, punct = False)
        short_zip = cqu.codeNorm(short_zip, n = 3, punct = False)
        short_diag_code = cqu.codeNorm(short_diag_code, n = 3, punct = False)
        diag_code = cqu.codeNorm(diag_code, punct = False)

        # normalize strings -- lowercase, trim whitespace)
        gender = cqu.stringNorm(gender)
        visit_type = cqu.stringNorm(visit_type)
        payor_channel = cqu.stringNorm(payor_channel)
        place_of_service = cqu.stringNorm(place_of_service)
        drg_category = cqu.stringNorm(drg_category)
        diag_code = cqu.stringNorm(diag_code)
        short_diag_code = cqu.stringNorm(short_diag_code)
        diag_category = cqu.stringNorm(diag_category)
        diag_subcategory = cqu.stringNorm(diag_subcategory)
        proc_code = cqu.stringNorm(proc_code)
        proc_category = cqu.stringNorm(proc_category)
        proc_subcategory = cqu.stringNorm(proc_subcategory)
        taxonomy_code = cqu.stringNorm(taxonomy_code)
        subspecialty = cqu.stringNorm(subspecialty)
        specialty = cqu.stringNorm(specialty)
        specialty_category = cqu.stringNorm(specialty_category)
        state = cqu.stringNorm(state)
        division = cqu.stringNorm(division)
        region = cqu.stringNorm(region)
        metro = cqu.stringNorm(metro)

        # ensure levels feature levels congeal
        cqu.checkLevels(visit_type, "visit_type", levels = 1)
        cqu.checkLevels(payor_channel, "payor_channel", levels = 1)
        cqu.checkLevels(place_of_service, "place_of_service", levels = 1)
        cqu.checkLevels(revenue_center_code, "revenue_center_code", levels = 1)
        cqu.checkLevels(drg_code, "drg_code", levels = 1)
        cqu.checkLevels(ref_npi, "ref_npi", levels = 1)
        cqu.checkLevels(npi, "npi", levels = 1)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(gender, self.field_values.data, "gender")
        cqu.checkFieldValues(visit_type, self.field_values.data, "visit_type")
        cqu.checkFieldValues(payor_channel, self.field_values.data, "payor_channel")
        cqu.checkFieldValues(revenue_center_code, self.field_values.data, "revenue_center_code")
        cqu.checkFieldValues(place_of_service, self.field_values.data, "place_of_service")
        cqu.checkFieldValues(drg_code, self.field_values.data, "drg_code")
        cqu.checkFieldValues(drg_category, self.field_values.data, "drg_category")
        cqu.checkFieldValues(diag_category, self.field_values.data, "diag_category")
        cqu.checkFieldValues(diag_subcategory, self.field_values.data, "diag_subcategory")
        cqu.checkFieldValues(proc_code, self.field_values.data, "proc_code")
        cqu.checkFieldValues(proc_category, self.field_values.data, "proc_category")
        cqu.checkFieldValues(proc_subcategory, self.field_values.data, "proc_subcategory")
        cqu.checkFieldValues(taxonomy_code, self.field_values.data, "taxonomy_code")
        cqu.checkFieldValues(subspecialty, self.field_values.data, "subspecialty")
        cqu.checkFieldValues(specialty, self.field_values.data, "specialty")
        cqu.checkFieldValues(specialty_category, self.field_values.data, "specialty_category")
        cqu.checkFieldValues(state, self.field_values.data, "state")
        cqu.checkFieldValues(division, self.field_values.data, "division")
        cqu.checkFieldValues(region, self.field_values.data, "region")
        cqu.checkFieldValues(metro, self.field_values.data, "metro")

        ### Input Logic & Hierarchy ###

        # place of service hierarchy logic
        place_of_service = cqu.placeOfServicePriority(place_of_service, self.field_values.data)

        # drg hierarchy logic
        drgs, drg_greedy, warnings_list0  = cqu.drgPriority(drg_code, drg_category, drg_greedy, self.field_values.data)

        # control for drg, proc or diag co-occurrance
        cqu.checkDRGConflate(drgs, proc_code, proc_subcategory, proc_category, diag_code, diag_subcategory, diag_category, short_diag_code)

        # diagnosis hierarchy logic
        diags, diag_greedy, warnings_list1 = cqu.diagnosisPriority(diag_code, short_diag_code, diag_subcategory, diag_category, diag_greedy, self.field_values.data)

        # procedure hierarchy logic
        procs, proc_greedy, warnings_list2 = cqu.procedurePriority(proc_code, proc_subcategory, proc_category, proc_greedy, self.field_values.data)

        # warning around drg and diag/proc overlap
        warnings_list3 = [] 

        # procedure hierarchy logic
        taxonomies, taxonomy_greedy, warnings_list4 = cqu.taxonomyPriority(taxonomy_code, subspecialty, specialty, specialty_category, taxonomy_greedy, self.field_values.data)
        cqu.checkLevels(taxonomies, "taxonomies", levels = 1)

        # geography hierarchy priority
        states, zips, warnings_list5 = cqu.geoPriority(state, division, region, metro, short_zip, self.field_values.data)

        # warning around taxonomy and npi overlap
        warnings_list6 = cqu.checkNPIOverlap(taxonomies, ref_npi, npi)

        # collect warnings
        warnings_list = warnings_list0 + warnings_list1 + warnings_list2 + warnings_list3 + warnings_list4 + warnings_list5 + warnings_list6

        # make it pretty for Ray's SQL
        diags = cqu.stringNorm(cqu.listWrapString(diags), stringtype = "upper")
        procs = cqu.stringNorm(cqu.listWrapString(procs), stringtype = "upper")
        states = cqu.stringNorm(cqu.listWrapString(states), stringtype = "upper")
        gender = cqu.stringNorm(gender, stringtype = "upper")
        taxonomies = cqu.stringNorm(cqu.listWrapString(taxonomies), stringtype = "upper")
        payor_channel = cqu.stringNorm(cqu.listWrapString(payor_channel), stringtype = "title")
        visit_type = cqu.stringNorm(cqu.listWrapString(visit_type), stringtype = "title")
        npi = cqu.listWrapString(npi)
        ref_npi = cqu.listWrapString(ref_npi)
        zips = cqu.listWrapString(zips)

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "encounter",
                 "min_date" : min_date,
                "max_date" : max_date,
                "gender" : gender,
                "age_min" : age_min,
                "age_max" : age_max,
                "visit_type" : visit_type,
                "payor_channel" : payor_channel,
                "revenue_center_code" : revenue_center_code,
                "place_of_service" :  place_of_service,
                "drg_code" : drgs,
                "diag_code" : diags,
                "proc_code" : procs,
                "taxonomy_code" : taxonomies,
                "ref_npi" : ref_npi,
                "npi" : npi,
                "state" : states,
                "short_zip" : zips,
                "greedy": False, # always keep false for now, implications too complicated for now
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        enc = CareQueryData(data, features = self.glossary.feature_detail("JOURNEY_TABLE"), show = show)

        return enc
    
    def careVisit(self, 
                    min_date = None,
                    max_date = None,
                    gender = None,
                    age_min = None,
                    age_max = None,
                    visit_type = None,
                    payor_channel = None,
                    revenue_center_code = None,
                    place_of_service = None, 
                    diag_code = None,
                    diag_category = None,
                    diag_subcategory = None,
                    short_diag_code = None,
                    diag_greedy = None,
                    proc_code = None,
                    proc_category = None,
                    proc_subcategory = None,
                    proc_greedy = None,
                    taxonomy_code = None,
                    specialty_category = None,
                    specialty = None,
                    subspecialty = None,
                    taxonomy_greedy = None,
                    ref_npi = None,
                    npi = None,
                    state = None,
                    division = None,
                    region = None,
                    metro = None,
                    short_zip = None,
                    limit = None,
                    show = None):
        
        """
        Description:
        
            Specify visit-based query parameters to construct a query object. From which the .execute() method on this query will return line-item level patient journey detail for healthcare visits that meet the query criterion. We define a visit as an encounter (or set of encounters) that occur within the same event of care.
       
        Parameters:
            min_date (str):
                Lower threshold date within the date range of interest, observational start date
                option(s): "2023-01-01" or "01/01/2023" 
                default: 90 days prior to date of query
            max_date (str):
                Upper threshold date within the date range of interest, observational end date
                option(s): "2023-01-01" or "01/01/2023" 
                default: 30 days prior to date of query
            gender (str or list(str)):
                Patient gender within the population of interest
                option(s): 'M' for Male, 'F' for Female, or ['M','F'] for both
                default(s): ['M','F']
            age_min (int):
                Minimum patient age identified within the population of interest
                option(s): 0 to 120
                default: 0
            age_max (int):
                Maximum patient age identified within the population of interest
                option(s): 0 to 120
                default: 120
            visit_type (str or list(str) or list(list(str),list(str))):
                Description of the setting of care
                option(s): Run self.field_values.list_values(field = "visit_type") to see all visit_type options
                default(s): Defaults to all visit types if left unspecified
            payor_channel (str or list(str) or list(list(str),list(str))):
                Health Insurance Payor channel-of-business or line-of-business
                option(s): Run self.field_values.list_values(field = "payor_channel") to see all payor_channel options
                default(s): Defaults to all payor channels if left unspecified
            revenue_center_code (str or list(str) or list(list(str),list(str))):
                4-digit code used to identify a specific accommodation, ancillary service, or billing calculation on a hospital bill
                option(s): Run self.field_values.list_values(field = "revenue_center_code") to see all revenue_center_code options
                default(s):  Defaults to all revenue codes if left unspecified
            place_of_service (str or list(str) or list(list(str),list(str))):
                Setting in which a healthcare service was provided by healthcare providers, insurers, and government agencies to track and bill for healthcare services
                option(s): Run self.field_values.list_values(field = "place_of_service") to see all place_of_service options
                default(s): Defaults to all places of service if left unspecified
            diag_code (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis code assigned to the patient
                option(s): Run self.field_values.list_values(field = "diag_code") to see all diag_code options
                default(s): Defaults to all diagnosis codes if left unspecified
            diag_category (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis category assigned to the patient
                option(s): Run self.field_values.list_values(field = "diag_category") to see all diag_category options
                default(s): Defaults to all diagnosis categories if left unspecified
            diag_subcategory (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis subcategory assigned to the patient
                option(s): Run self.field_values.list_values(field = "diag_subcategory") to see all diag_subcategory options
                default(s): Defaults to all diagnosis subcategories if left unspecified
            short_diag_code (str or list(str) or list(list(str),list(str))):
                First three digits of ICD-10 code assigned to the patient
                option(s): Run self.field_values.list_values(field = "short_diag_code") to see all short_diag_code options
                default(s): Defaults to all short diagnosis codes if left unspecified
            diag_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple diagnosis parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified diagnosis needs to be present within the returned results, False indicates all diagnosis must be present for the returned results
                default: True
            proc_code (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural code performed
                option(s): Run self.field_values.list_values(field = "proc_code") to see all proc_code options
                default(s): Defaults to all procedure codes if left unspecified
            proc_category (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural category performed
                option(s): Run self.field_values.list_values(field = "proc_category") to see all proc_category options
                default(s): Defaults to all procedure categories if left unspecified
            proc_subcategory (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural subcategory performed
                option(s): Run self.field_values.list_values(field = "proc_subcategory") to see all proc_subcategory options
                default(s): Defaults to all procedure subcategories if left unspecified
            proc_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple procedure parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified procedure needs to be present within the returned results, False indicates all procedures within sub-lists must be present for the returned results
                default: True
            taxonomy_code (str or list(str) or list(list(str),list(str))):
                Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider
                option(s): Run self.field_values.list_values(field = "taxonomy_code") to see all taxonomy_code options
                default(s): Defaults to all taxonomy codes if left unspecified
            specialty (str or list(str) or list(list(str),list(str))):
                Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty") to see all specialty options
                default(s): Defaults to all specialties if left unspecified
            specialty_category (str or list(str) or list(list(str),list(str))):
                Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty_category") to see all specialty_category options
                default(s): Defaults to all specialty categories if left unspecified
            subspecialty (str or list(str) or list(list(str),list(str))):
                Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "subspecialty") to see all subspecialty options
                default(s): Defaults to all specialty subcategories if left unspecified
            taxonomy_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple taxonomy or specialty parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified taxonomy or specialty needs to be present within the returned results, False indicates all taxonomy or specialty must be present for the returned results
                default: True
            ref_npi (int or list(int) or list(list(int),list(int))):
                Referring provider(s) indicated by National Provider Identifiers (NPIs)
                option(s): Any valid, registered individual National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            npi (int or list(int) or list(list(int),list(int))):
                National Provider Identifier (NPI) of individual and organizational provider(s) of interest
                option(s): Any valid, registered individual or organizational National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            state (str or list(str) or list(list(str),list(str))):
                option(s): Run self.field_values.list_values(field = "state") to see all state options
                default(s): Defaults to all US States if left unspecified
            division (str or list(str) or list(list(str),list(str))):
                District residence of the query patient population. There are nine distinct US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "division") to see all division options
                default(s): Defaults to all entire US population if left unspecified
            region (str or list(str) or list(list(str),list(str))):
                Regional residence of the query patient population. There are four major US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "region") to see all region options
                default(s): Defaults to all entire US population if left unspecified
            metro (str or list(str) or list(list(str),list(str))):
                Metropolitan and micropolitan statistical areas according to the US Census Bureau
                option(s): Run self.field_values.list_values(field = "metro") to see all metro options
                default(s): Defaults to all entire US population if left unspecified
            short_zip (int or list(int) or list(list(int),list(int))):
                First three digits the zip code of the query patient population specified
                option(s): Run self.field_values.list_values(field = "short_zip") to see all short_zip options
                default(s): Defaults to all entire US population if left unspecified 
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: 10000
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: state = "NE"
                    example logic: Select data from the state of Nebraska
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: state = ["NE","CO"]
                    example logic: Select data from either Nebraska OR Colorado
                multi-selection AND: Select multiple values across multiple lists to request results that meet both conditions
                    example: short_diag_code = [["I10"],["E11"]]
                    example logic: Select data where patients have hypertension (I10) AND type-2 diabetes (E11)
            inter-parameter: Logical arguments ACROSS parameter specifications
                multi-selection AND: (default) Return data that meets both criterion
                    example: self.encounter(state = "NE", short_diag_code = ["I10"])
                    example logic: Select all hypertensive encounters in Nebraska
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if min_date == None:
            temp = date.today() - timedelta(days=30)
            min_date = temp.strftime("%Y-%m-%d")
            print(min_date)
        if max_date == None:
            temp = date.today() - timedelta(days=90)
            max_date = temp.strftime("%Y-%m-%d")
            print(max_date)
        if age_min == None:
            age_min = 0
        if age_max == None:
            age_max = 120
        if gender == None:
            gender = ["M","F"]
        if limit == None:
            limit = 10000
        elif (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"gender" : gender, "visit_type" : visit_type, "payor_channel" : payor_channel, "revenue_center_code" : revenue_center_code, "place_of_service" :  place_of_service, "diag_code" : diag_code, "short_diag_code" : short_diag_code, "diag_category":diag_category, "diag_subcategory": diag_subcategory, "proc_code" : proc_code, "proc_category":proc_category, "proc_subcategory":proc_subcategory, "taxonomy_code" : taxonomy_code, "subspecialty": subspecialty, "specialty" : specialty, "specialty_category" : specialty_category, "ref_npi" : ref_npi, "npi" : npi, "state" : state, "division" : division, "region" : region, "metro" : metro, "short_zip" : short_zip}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # ensure valid date data type 
        dates = {"min_date" : min_date, "max_date" : max_date}
        for x in list(dates.items()):
            if x[1] != None:
                if type(x[1]) == str:
                    cqu.checkTypeDate(dateutil.parser.parse(x[1]).date(), x[0])
                else:
                    cqu.checkTypeDate(x[1], x[0])

        # ensure valid integer data type
        ints = {"limit" : limit, "age_min" : age_min, "age_max" : age_max}
        for x in list(ints.items()):
            if (x[1] != None):
                cqu.checkTypeInt(x[1], x[0])

        # normalize NPI output
        ref_npi = cqu.NPINorm(ref_npi)
        npi = cqu.NPINorm(npi)

        # raise error for invalid NPIs
        cqu.checkNPI(ref_npi, "ref_npi")
        cqu.checkNPI(npi, "npi")

        ### Input Quality Control ###

        # normalize code digit input
        # drg_code = cqu.codeNorm(drg_code, n = 3, punct = False)
        revenue_center_code = cqu.codeNorm(revenue_center_code, n = 4, punct = False)
        short_zip = cqu.codeNorm(short_zip, n = 3, punct = False)
        short_diag_code = cqu.codeNorm(short_diag_code, n = 3, punct = False)
        diag_code = cqu.codeNorm(diag_code, punct = False)

        # normalize strings -- lowercase, trim whitespace)
        gender = cqu.stringNorm(gender)
        visit_type = cqu.stringNorm(visit_type)
        payor_channel = cqu.stringNorm(payor_channel)
        place_of_service = cqu.stringNorm(place_of_service)
        # drg_code = cqu.stringNorm(drg_code)
        diag_code = cqu.stringNorm(diag_code)
        short_diag_code = cqu.stringNorm(short_diag_code)
        diag_category = cqu.stringNorm(diag_category)
        diag_subcategory = cqu.stringNorm(diag_subcategory)
        proc_code = cqu.stringNorm(proc_code)
        proc_category = cqu.stringNorm(proc_category)
        proc_subcategory = cqu.stringNorm(proc_subcategory)
        taxonomy_code = cqu.stringNorm(taxonomy_code)
        subspecialty = cqu.stringNorm(subspecialty)
        specialty = cqu.stringNorm(specialty)
        specialty_category = cqu.stringNorm(specialty_category)
        state = cqu.stringNorm(state)
        division = cqu.stringNorm(division)
        region = cqu.stringNorm(region)
        metro = cqu.stringNorm(metro)

        # ensure levels feature levels congeal
        cqu.checkLevels(visit_type, "visit_type", levels = 1)
        cqu.checkLevels(payor_channel, "payor_channel", levels = 1)
        cqu.checkLevels(place_of_service, "place_of_service", levels = 1)
        cqu.checkLevels(revenue_center_code, "revenue_center_code", levels = 2)
        # cqu.checkLevels(drg_code, "drg_code", levels = 2)
        cqu.checkLevels(ref_npi, "ref_npi", levels = 1)
        cqu.checkLevels(npi, "npi", levels = 2)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(gender, self.field_values.data, "gender")
        cqu.checkFieldValues(visit_type, self.field_values.data, "visit_type")
        cqu.checkFieldValues(payor_channel, self.field_values.data, "payor_channel")
        cqu.checkFieldValues(revenue_center_code, self.field_values.data, "revenue_center_code")
        cqu.checkFieldValues(place_of_service, self.field_values.data, "place_of_service")
        # cqu.checkFieldValues(drg_code, self.field_values.data, "drg_code")
        cqu.checkFieldValues(diag_category, self.field_values.data, "diag_category")
        cqu.checkFieldValues(diag_subcategory, self.field_values.data, "diag_subcategory")
        cqu.checkFieldValues(proc_code, self.field_values.data, "proc_code")
        cqu.checkFieldValues(proc_category, self.field_values.data, "proc_category")
        cqu.checkFieldValues(proc_subcategory, self.field_values.data, "proc_subcategory")
        cqu.checkFieldValues(taxonomy_code, self.field_values.data, "taxonomy_code")
        cqu.checkFieldValues(subspecialty, self.field_values.data, "subspecialty")
        cqu.checkFieldValues(specialty, self.field_values.data, "specialty")
        cqu.checkFieldValues(specialty_category, self.field_values.data, "specialty_category")
        cqu.checkFieldValues(state, self.field_values.data, "state")
        cqu.checkFieldValues(division, self.field_values.data, "division")
        cqu.checkFieldValues(region, self.field_values.data, "region")
        cqu.checkFieldValues(metro, self.field_values.data, "metro")

        ### Input Logic & Hierarchy ###

        # place of service hierarchy logic
        place_of_service = cqu.placeOfServicePriority(place_of_service, self.field_values.data)

        # diagnosis hierarchy logic
        diags, diag_greedy, warnings_list1 = cqu.diagnosisPriority(diag_code, short_diag_code, diag_subcategory, diag_category, diag_greedy, self.field_values.data)

        # procedure hierarchy logic
        procs, proc_greedy, warnings_list2 = cqu.procedurePriority(proc_code, proc_subcategory, proc_category, proc_greedy, self.field_values.data)

        # warning around drg and diag/proc overlap
        warnings_list3 = [] # cqu.checkDRGOverlap(drg_code, diags, procs)

        # procedure hierarchy logic
        taxonomies, taxonomy_greedy, warnings_list4 = cqu.taxonomyPriority(taxonomy_code, subspecialty, specialty, specialty_category, taxonomy_greedy, self.field_values.data)
        cqu.checkLevels(taxonomies, "taxonomies", levels = 2)

        # geography hierarchy priority
        states, zips, warnings_list5 = cqu.geoPriority(state, division, region, metro, short_zip, self.field_values.data)

        # warning around taxonomy and npi overlap
        warnings_list6 = cqu.checkNPIOverlap(taxonomies, ref_npi, npi)

        # collect warnings
        warnings_list = warnings_list1 + warnings_list2 + warnings_list3 + warnings_list4 + warnings_list5 + warnings_list6

        # make it pretty for Ray's SQL
        diags = cqu.stringNorm(cqu.listWrapString(diags), stringtype = "upper")
        procs = cqu.stringNorm(cqu.listWrapString(procs), stringtype = "upper")
        states = cqu.stringNorm(cqu.listWrapString(states), stringtype = "upper")
        gender = cqu.stringNorm(gender, stringtype = "upper")
        taxonomies = cqu.stringNorm(cqu.listWrapString(taxonomies), stringtype = "upper")
        payor_channel = cqu.stringNorm(cqu.listWrapString(payor_channel), stringtype = "title")
        visit_type = cqu.stringNorm(cqu.listWrapString(visit_type), stringtype = "title")
        npi = cqu.listWrapString(npi)
        ref_npi = cqu.listWrapString(ref_npi)
        zips = cqu.listWrapString(zips)

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "visit",
                 "min_date" : min_date,
                "max_date" : max_date,
                "gender" : gender,
                "age_min" : age_min,
                "age_max" : age_max,
                "visit_type" : visit_type,
                "payor_channel" : payor_channel,
                "revenue_center_code" : revenue_center_code,
                "place_of_service" :  place_of_service,
                "drg_code" : None,
                "diag_code" : diags,
                "proc_code" : procs,
                "taxonomy_code" : taxonomies,
                "ref_npi" : ref_npi,
                "npi" : npi,
                "state" : states,
                "short_zip" : zips,
                "greedy": False, # always keep false for now, implications too complicated for now
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        visit = CareQueryData(data, features = self.table_features.feature_detail("JOURNEY_TABLE"),show = show)

        return visit

    def careEpisode(self, 
                    min_date = None,
                    max_date = None,
                    gender = None,
                    age_min = None,
                    age_max = None,
                    visit_type = None,
                    payor_channel = None,
                    revenue_center_code = None,
                    place_of_service = None, 
                    diag_code = None,
                    diag_category = None,
                    diag_subcategory = None,
                    short_diag_code = None,
                    diag_greedy = None,
                    proc_code = None,
                    proc_category = None,
                    proc_subcategory = None,
                    proc_greedy = None,
                    taxonomy_code = None,
                    specialty_category = None,
                    specialty = None,
                    subspecialty = None,
                    taxonomy_greedy = None,
                    ref_npi = None,
                    npi = None,
                    state = None,
                    division = None,
                    region = None,
                    metro = None,
                    short_zip = None,
                    limit = None,
                    show = None):
        
        """
        Description:
        
            Specify episode-based query parameters to construct a query object. From which the .execute() method on this query will return line-item level patient journey detail for healthcare episodes that meet the query criterion. We define an episode of care as a sequence of healthcare encounters that occur within at least 30 days of one another in succession, a definition shared by CMS.

        Parameters:
            min_date (str):
                Lower threshold date within the date range of interest, observational start date
                option(s): "2023-01-01" or "01/01/2023" 
                default: 90 days prior to date of query
            max_date (str):
                Upper threshold date within the date range of interest, observational end date
                option(s): "2023-01-01" or "01/01/2023" 
                default: 30 days prior to date of query
            gender (str or list(str)):
                Patient gender within the population of interest
                option(s): 'M' for Male, 'F' for Female, or ['M','F'] for both
                default(s): ['M','F']
            age_min (int):
                Minimum patient age identified within the population of interest
                option(s): 0 to 120
                default: 0
            age_max (int):
                Maximum patient age identified within the population of interest
                option(s): 0 to 120
                default: 120
            visit_type (str or list(str) or list(list(str),list(str))):
                Description of the setting of care
                option(s): Run self.field_values.list_values(field = "visit_type") to see all visit_type options
                default(s): Defaults to all visit types if left unspecified
            payor_channel (str or list(str) or list(list(str),list(str))):
                Health Insurance Payor channel-of-business or line-of-business
                option(s): Run self.field_values.list_values(field = "payor_channel") to see all payor_channel options
                default(s): Defaults to all payor channels if left unspecified
            revenue_center_code (str or list(str) or list(list(str),list(str))):
                4-digit code used to identify a specific accommodation, ancillary service, or billing calculation on a hospital bill
                option(s): Run self.field_values.list_values(field = "revenue_center_code") to see all revenue_center_code options
                default(s):  Defaults to all revenue codes if left unspecified
            place_of_service (str or list(str) or list(list(str),list(str))):
                Setting in which a healthcare service was provided by healthcare providers, insurers, and government agencies to track and bill for healthcare services
                option(s): Run self.field_values.list_values(field = "place_of_service") to see all place_of_service options
                default(s): Defaults to all places of service if left unspecified
            diag_code (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis code assigned to the patient
                option(s): Run self.field_values.list_values(field = "diag_code") to see all diag_code options
                default(s): Defaults to all diagnosis codes if left unspecified
            diag_category (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis category assigned to the patient
                option(s): Run self.field_values.list_values(field = "diag_category") to see all diag_category options
                default(s): Defaults to all diagnosis categories if left unspecified
            diag_subcategory (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis subcategory assigned to the patient
                option(s): Run self.field_values.list_values(field = "diag_subcategory") to see all diag_subcategory options
                default(s): Defaults to all diagnosis subcategories if left unspecified
            short_diag_code (str or list(str) or list(list(str),list(str))):
                First three digits of ICD-10 code assigned to the patient
                option(s): Run self.field_values.list_values(field = "short_diag_code") to see all short_diag_code options
                default(s): Defaults to all short diagnosis codes if left unspecified
            diag_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple diagnosis parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified diagnosis needs to be present within the returned results, False indicates all diagnosis must be present for the returned results
                default: True
            proc_code (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural code performed
                option(s): Run self.field_values.list_values(field = "proc_code") to see all proc_code options
                default(s): Defaults to all procedure codes if left unspecified
            proc_category (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural category performed
                option(s): Run self.field_values.list_values(field = "proc_category") to see all proc_category options
                default(s): Defaults to all procedure categories if left unspecified
            proc_subcategory (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural subcategory performed
                option(s): Run self.field_values.list_values(field = "proc_subcategory") to see all proc_subcategory options
                default(s): Defaults to all procedure subcategories if left unspecified
            proc_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple procedure parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified procedure needs to be present within the returned results, False indicates all procedures within sub-lists must be present for the returned results
                default: True
            taxonomy_code (str or list(str) or list(list(str),list(str))):
                Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider
                option(s): Run self.field_values.list_values(field = "taxonomy_code") to see all taxonomy_code options
                default(s): Defaults to all taxonomy codes if left unspecified
            specialty (str or list(str) or list(list(str),list(str))):
                Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty") to see all specialty options
                default(s): Defaults to all specialties if left unspecified
            specialty_category (str or list(str) or list(list(str),list(str))):
                Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty_category") to see all specialty_category options
                default(s): Defaults to all specialty categories if left unspecified
            subspecialty (str or list(str) or list(list(str),list(str))):
                Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "subspecialty") to see all subspecialty options
                default(s): Defaults to all specialty subcategories if left unspecified
            taxonomy_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple taxonomy or specialty parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified taxonomy or specialty needs to be present within the returned results, False indicates all taxonomy or specialty must be present for the returned results
                default: True
            ref_npi (int or list(int) or list(list(int),list(int))):
                Referring provider(s) indicated by National Provider Identifiers (NPIs)
                option(s): Any valid, registered individual National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            npi (int or list(int) or list(list(int),list(int))):
                National Provider Identifier (NPI) of individual and organizational provider(s) of interest
                option(s): Any valid, registered individual or organizational National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            state (str or list(str) or list(list(str),list(str))):
                option(s): Run self.field_values.list_values(field = "state") to see all state options
                default(s): Defaults to all US States if left unspecified
            division (str or list(str) or list(list(str),list(str))):
                District residence of the query patient population. There are nine distinct US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "division") to see all division options
                default(s): Defaults to all entire US population if left unspecified
            region (str or list(str) or list(list(str),list(str))):
                Regional residence of the query patient population. There are four major US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "region") to see all region options
                default(s): Defaults to all entire US population if left unspecified
            metro (str or list(str) or list(list(str),list(str))):
                Metropolitan and micropolitan statistical areas according to the US Census Bureau
                option(s): Run self.field_values.list_values(field = "metro") to see all metro options
                default(s): Defaults to all entire US population if left unspecified
            short_zip (int or list(int) or list(list(int),list(int))):
                First three digits the zip code of the query patient population specified
                option(s): Run self.field_values.list_values(field = "short_zip") to see all short_zip options
                default(s): Defaults to all entire US population if left unspecified 
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: 10000
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: state = "NE"
                    example logic: Select data from the state of Nebraska
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: state = ["NE","CO"]
                    example logic: Select data from either Nebraska OR Colorado
                multi-selection AND: Select multiple values across multiple lists to request results that meet both conditions
                    example: short_diag_code = [["I10"],["E11"]]
                    example logic: Select data where patients have hypertension (I10) AND type-2 diabetes (E11)
            inter-parameter: Logical arguments ACROSS parameter specifications
                multi-selection AND: (default) Return data that meets both criterion
                    example: self.encounter(state = "NE", short_diag_code = ["I10"])
                    example logic: Select all hypertensive encounters in Nebraska
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if min_date == None:
            temp = date.today() - timedelta(days=30)
            min_date = temp.strftime("%Y-%m-%d")
            print(min_date)
        if max_date == None:
            temp = date.today() - timedelta(days=90)
            max_date = temp.strftime("%Y-%m-%d")
            print(max_date)
        if age_min == None:
            age_min = 0
        if age_max == None:
            age_max = 120
        if gender == None:
            gender = ["M","F"]
        if limit == None:
            limit = 10000
        elif (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"gender" : gender, "visit_type" : visit_type, "payor_channel" : payor_channel, "revenue_center_code" : revenue_center_code, "place_of_service" :  place_of_service, "diag_code" : diag_code, "short_diag_code" : short_diag_code, "diag_category":diag_category, "diag_subcategory": diag_subcategory, "proc_code" : proc_code, "proc_category":proc_category, "proc_subcategory":proc_subcategory, "taxonomy_code" : taxonomy_code, "subspecialty": subspecialty, "specialty" : specialty, "specialty_category" : specialty_category, "ref_npi" : ref_npi, "npi" : npi, "state" : state, "division" : division, "region" : region, "metro" : metro, "short_zip" : short_zip}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # ensure valid date data type 
        dates = {"min_date" : min_date, "max_date" : max_date}
        for x in list(dates.items()):
            if x[1] != None:
                if type(x[1]) == str:
                    cqu.checkTypeDate(dateutil.parser.parse(x[1]).date(), x[0])
                else:
                    cqu.checkTypeDate(x[1], x[0])

        # ensure valid integer data type
        ints = {"limit" : limit, "age_min" : age_min, "age_max" : age_max}
        for x in list(ints.items()):
            if (x[1] != None):
                cqu.checkTypeInt(x[1], x[0])

        # normalize NPI output
        ref_npi = cqu.NPINorm(ref_npi)
        npi = cqu.NPINorm(npi)

        # raise error for invalid NPIs
        cqu.checkNPI(ref_npi, "ref_npi")
        cqu.checkNPI(npi, "npi")

        ### Input Quality Control ###

        # normalize code digit input
        # drg_code = cqu.codeNorm(drg_code, n = 3, punct = False)
        revenue_center_code = cqu.codeNorm(revenue_center_code, n = 4, punct = False)
        short_zip = cqu.codeNorm(short_zip, n = 3, punct = False)
        short_diag_code = cqu.codeNorm(short_diag_code, n = 3, punct = False)
        diag_code = cqu.codeNorm(diag_code, punct = False)

        # normalize strings -- lowercase, trim whitespace)
        gender = cqu.stringNorm(gender)
        visit_type = cqu.stringNorm(visit_type)
        payor_channel = cqu.stringNorm(payor_channel)
        place_of_service = cqu.stringNorm(place_of_service)
        # drg_code = cqu.stringNorm(drg_code)
        diag_code = cqu.stringNorm(diag_code)
        short_diag_code = cqu.stringNorm(short_diag_code)
        diag_category = cqu.stringNorm(diag_category)
        diag_subcategory = cqu.stringNorm(diag_subcategory)
        proc_code = cqu.stringNorm(proc_code)
        proc_category = cqu.stringNorm(proc_category)
        proc_subcategory = cqu.stringNorm(proc_subcategory)
        taxonomy_code = cqu.stringNorm(taxonomy_code)
        subspecialty = cqu.stringNorm(subspecialty)
        specialty = cqu.stringNorm(specialty)
        specialty_category = cqu.stringNorm(specialty_category)
        state = cqu.stringNorm(state)
        division = cqu.stringNorm(division)
        region = cqu.stringNorm(region)
        metro = cqu.stringNorm(metro)

        # ensure levels feature levels congeal
        cqu.checkLevels(visit_type, "visit_type", levels = 1)
        cqu.checkLevels(payor_channel, "payor_channel", levels = 1)
        cqu.checkLevels(place_of_service, "place_of_service", levels = 1)
        cqu.checkLevels(revenue_center_code, "revenue_center_code", levels = 2)
        # cqu.checkLevels(drg_code, "drg_code", levels = 2)
        cqu.checkLevels(ref_npi, "ref_npi", levels = 1)
        cqu.checkLevels(npi, "npi", levels = 2)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(gender, self.field_values.data, "gender")
        cqu.checkFieldValues(visit_type, self.field_values.data, "visit_type")
        cqu.checkFieldValues(payor_channel, self.field_values.data, "payor_channel")
        cqu.checkFieldValues(revenue_center_code, self.field_values.data, "revenue_center_code")
        cqu.checkFieldValues(place_of_service, self.field_values.data, "place_of_service")
        # cqu.checkFieldValues(drg_code, self.field_values.data, "drg_code")
        cqu.checkFieldValues(diag_category, self.field_values.data, "diag_category")
        cqu.checkFieldValues(diag_subcategory, self.field_values.data, "diag_subcategory")
        cqu.checkFieldValues(proc_code, self.field_values.data, "proc_code")
        cqu.checkFieldValues(proc_category, self.field_values.data, "proc_category")
        cqu.checkFieldValues(proc_subcategory, self.field_values.data, "proc_subcategory")
        cqu.checkFieldValues(taxonomy_code, self.field_values.data, "taxonomy_code")
        cqu.checkFieldValues(subspecialty, self.field_values.data, "subspecialty")
        cqu.checkFieldValues(specialty, self.field_values.data, "specialty")
        cqu.checkFieldValues(specialty_category, self.field_values.data, "specialty_category")
        cqu.checkFieldValues(state, self.field_values.data, "state")
        cqu.checkFieldValues(division, self.field_values.data, "division")
        cqu.checkFieldValues(region, self.field_values.data, "region")
        cqu.checkFieldValues(metro, self.field_values.data, "metro")

        ### Input Logic & Hierarchy ###

        # place of service hierarchy logic
        place_of_service = cqu.placeOfServicePriority(place_of_service, self.field_values.data)

        # diagnosis hierarchy logic
        diags, diag_greedy, warnings_list1 = cqu.diagnosisPriority(diag_code, short_diag_code, diag_subcategory, diag_category, diag_greedy, self.field_values.data)

        # procedure hierarchy logic
        procs, proc_greedy, warnings_list2 = cqu.procedurePriority(proc_code, proc_subcategory, proc_category, proc_greedy, self.field_values.data)

        # warning around drg and diag/proc overlap
        warnings_list3 = [] # cqu.checkDRGOverlap(drg_code, diags, procs)

        # procedure hierarchy logic
        taxonomies, taxonomy_greedy, warnings_list4 = cqu.taxonomyPriority(taxonomy_code, subspecialty, specialty, specialty_category, taxonomy_greedy, self.field_values.data)
        cqu.checkLevels(taxonomies, "taxonomies", levels = 2)

        # geography hierarchy priority
        states, zips, warnings_list5 = cqu.geoPriority(state, division, region, metro, short_zip, self.field_values.data)

        # warning around taxonomy and npi overlap
        warnings_list6 = cqu.checkNPIOverlap(taxonomies, ref_npi, npi)

        # collect warnings
        warnings_list = warnings_list1 + warnings_list2 + warnings_list3 + warnings_list4 + warnings_list5 + warnings_list6

        # make it pretty for Ray's SQL
        diags = cqu.stringNorm(cqu.listWrapString(diags), stringtype = "upper")
        procs = cqu.stringNorm(cqu.listWrapString(procs), stringtype = "upper")
        states = cqu.stringNorm(cqu.listWrapString(states), stringtype = "upper")
        gender = cqu.stringNorm(gender, stringtype = "upper")
        taxonomies = cqu.stringNorm(cqu.listWrapString(taxonomies), stringtype = "upper")
        payor_channel = cqu.stringNorm(cqu.listWrapString(payor_channel), stringtype = "title")
        visit_type = cqu.stringNorm(cqu.listWrapString(visit_type), stringtype = "title")
        npi = cqu.listWrapString(npi)
        ref_npi = cqu.listWrapString(ref_npi)
        zips = cqu.listWrapString(zips)

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "episode",
                 "min_date" : min_date,
                "max_date" : max_date,
                "gender" : gender,
                "age_min" : age_min,
                "age_max" : age_max,
                "visit_type" : visit_type,
                "payor_channel" : payor_channel,
                "revenue_center_code" : revenue_center_code,
                "place_of_service" :  place_of_service,
                "drg_code" : None,
                "diag_code" : diags,
                "proc_code" : procs,
                "taxonomy_code" : taxonomies,
                "ref_npi" : ref_npi,
                "npi" : npi,
                "state" : states,
                "short_zip" : zips,
                "greedy": False, # always keep false for now, implications too complicated for now
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        episode = CareQueryData(data, features = self.glossary.feature_detail("JOURNEY_TABLE"), show = show)

        return episode

    def careJourney(self, 
                    min_date = None,
                    max_date = None,
                    gender = None,
                    age_min = None,
                    age_max = None,
                    visit_type = None,
                    payor_channel = None,
                    revenue_center_code = None,
                    place_of_service = None, 
                    diag_code = None,
                    diag_category = None,
                    diag_subcategory = None,
                    short_diag_code = None,
                    diag_greedy = None,
                    proc_code = None,
                    proc_category = None,
                    proc_subcategory = None,
                    proc_greedy = None,
                    taxonomy_code = None,
                    specialty_category = None,
                    specialty = None,
                    subspecialty = None,
                    taxonomy_greedy = None,
                    ref_npi = None,
                    npi = None,
                    state = None,
                    division = None,
                    region = None,
                    metro = None,
                    short_zip = None,
                    limit = None,
                    show = None):
        
        """
        Description:
        
            Specify journey-based query parameters to construct a query object. From which the .execute() method on this query will return line-item level patient journey detail for patient journeys that meet the query criterion. We define a patient journey as all patient encounters during the specified period of time.

        Parameters:
            min_date (str):
                Lower threshold date within the date range of interest, observational start date
                option(s): "2023-01-01" or "01/01/2023" 
                default: 90 days prior to date of query
            max_date (str):
                Upper threshold date within the date range of interest, observational end date
                option(s): "2023-01-01" or "01/01/2023" 
                default: 30 days prior to date of query
            gender (str or list(str)):
                Patient gender within the population of interest
                option(s): 'M' for Male, 'F' for Female, or ['M','F'] for both
                default(s): ['M','F']
            age_min (int):
                Minimum patient age identified within the population of interest
                option(s): 0 to 120
                default: 0
            age_max (int):
                Maximum patient age identified within the population of interest
                option(s): 0 to 120
                default: 120
            visit_type (str or list(str) or list(list(str),list(str))):
                Description of the setting of care
                option(s): Run self.field_values.list_values(field = "visit_type") to see all visit_type options
                default(s): Defaults to all visit types if left unspecified
            payor_channel (str or list(str) or list(list(str),list(str))):
                Health Insurance Payor channel-of-business or line-of-business
                option(s): Run self.field_values.list_values(field = "payor_channel") to see all payor_channel options
                default(s): Defaults to all payor channels if left unspecified
            revenue_center_code (str or list(str) or list(list(str),list(str))):
                4-digit code used to identify a specific accommodation, ancillary service, or billing calculation on a hospital bill
                option(s): Run self.field_values.list_values(field = "revenue_center_code") to see all revenue_center_code options
                default(s):  Defaults to all revenue codes if left unspecified
            place_of_service (str or list(str) or list(list(str),list(str))):
                Setting in which a healthcare service was provided by healthcare providers, insurers, and government agencies to track and bill for healthcare services
                option(s): Run self.field_values.list_values(field = "place_of_service") to see all place_of_service options
                default(s): Defaults to all places of service if left unspecified
            diag_code (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis code assigned to the patient
                option(s): Run self.field_values.list_values(field = "diag_code") to see all diag_code options
                default(s): Defaults to all diagnosis codes if left unspecified
            diag_category (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis category assigned to the patient
                option(s): Run self.field_values.list_values(field = "diag_category") to see all diag_category options
                default(s): Defaults to all diagnosis categories if left unspecified
            diag_subcategory (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis subcategory assigned to the patient
                option(s): Run self.field_values.list_values(field = "diag_subcategory") to see all diag_subcategory options
                default(s): Defaults to all diagnosis subcategories if left unspecified
            short_diag_code (str or list(str) or list(list(str),list(str))):
                First three digits of ICD-10 code assigned to the patient
                option(s): Run self.field_values.list_values(field = "short_diag_code") to see all short_diag_code options
                default(s): Defaults to all short diagnosis codes if left unspecified
            diag_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple diagnosis parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified diagnosis needs to be present within the returned results, False indicates all diagnosis must be present for the returned results
                default: True
            proc_code (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural code performed
                option(s): Run self.field_values.list_values(field = "proc_code") to see all proc_code options
                default(s): Defaults to all procedure codes if left unspecified
            proc_category (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural category performed
                option(s): Run self.field_values.list_values(field = "proc_category") to see all proc_category options
                default(s): Defaults to all procedure categories if left unspecified
            proc_subcategory (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural subcategory performed
                option(s): Run self.field_values.list_values(field = "proc_subcategory") to see all proc_subcategory options
                default(s): Defaults to all procedure subcategories if left unspecified
            proc_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple procedure parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified procedure needs to be present within the returned results, False indicates all procedures within sub-lists must be present for the returned results
                default: True
            taxonomy_code (str or list(str) or list(list(str),list(str))):
                Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider
                option(s): Run self.field_values.list_values(field = "taxonomy_code") to see all taxonomy_code options
                default(s): Defaults to all taxonomy codes if left unspecified
            specialty (str or list(str) or list(list(str),list(str))):
                Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty") to see all specialty options
                default(s): Defaults to all specialties if left unspecified
            specialty_category (str or list(str) or list(list(str),list(str))):
                Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty_category") to see all specialty_category options
                default(s): Defaults to all specialty categories if left unspecified
            subspecialty (str or list(str) or list(list(str),list(str))):
                Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "subspecialty") to see all subspecialty options
                default(s): Defaults to all specialty subcategories if left unspecified
            taxonomy_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple taxonomy or specialty parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified taxonomy or specialty needs to be present within the returned results, False indicates all taxonomy or specialty must be present for the returned results
                default: True
            ref_npi (int or list(int) or list(list(int),list(int))):
                Referring provider(s) indicated by National Provider Identifiers (NPIs)
                option(s): Any valid, registered individual National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            npi (int or list(int) or list(list(int),list(int))):
                National Provider Identifier (NPI) of individual and organizational provider(s) of interest
                option(s): Any valid, registered individual or organizational National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            state (str or list(str) or list(list(str),list(str))):
                option(s): Run self.field_values.list_values(field = "state") to see all state options
                default(s): Defaults to all US States if left unspecified
            division (str or list(str) or list(list(str),list(str))):
                District residence of the query patient population. There are nine distinct US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "division") to see all division options
                default(s): Defaults to all entire US population if left unspecified
            region (str or list(str) or list(list(str),list(str))):
                Regional residence of the query patient population. There are four major US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "region") to see all region options
                default(s): Defaults to all entire US population if left unspecified
            metro (str or list(str) or list(list(str),list(str))):
                Metropolitan and micropolitan statistical areas according to the US Census Bureau
                option(s): Run self.field_values.list_values(field = "metro") to see all metro options
                default(s): Defaults to all entire US population if left unspecified
            short_zip (int or list(int) or list(list(int),list(int))):
                First three digits the zip code of the query patient population specified
                option(s): Run self.field_values.list_values(field = "short_zip") to see all short_zip options
                default(s): Defaults to all entire US population if left unspecified 
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: 10000
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: state = "NE"
                    example logic: Select data from the state of Nebraska
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: state = ["NE","CO"]
                    example logic: Select data from either Nebraska OR Colorado
                multi-selection AND: Select multiple values across multiple lists to request results that meet both conditions
                    example: short_diag_code = [["I10"],["E11"]]
                    example logic: Select data where patients have hypertension (I10) AND type-2 diabetes (E11)
            inter-parameter: Logical arguments ACROSS parameter specifications
                multi-selection AND: (default) Return data that meets both criterion
                    example: self.encounter(state = "NE", short_diag_code = ["I10"])
                    example logic: Select all hypertensive encounters in Nebraska
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if min_date == None:
            temp = date.today() - timedelta(days=30)
            min_date = temp.strftime("%Y-%m-%d")
            print(min_date)
        if max_date == None:
            temp = date.today() - timedelta(days=90)
            max_date = temp.strftime("%Y-%m-%d")
            print(max_date)
        if age_min == None:
            age_min = 0
        if age_max == None:
            age_max = 120
        if gender == None:
            gender = ["M","F"]
        if limit == None:
            limit = 10000
        elif (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"gender" : gender, "visit_type" : visit_type, "payor_channel" : payor_channel, "revenue_center_code" : revenue_center_code, "place_of_service" :  place_of_service, "diag_code" : diag_code, "short_diag_code" : short_diag_code, "diag_category":diag_category, "diag_subcategory": diag_subcategory, "proc_code" : proc_code, "proc_category":proc_category, "proc_subcategory":proc_subcategory, "taxonomy_code" : taxonomy_code, "subspecialty": subspecialty, "specialty" : specialty, "specialty_category" : specialty_category, "ref_npi" : ref_npi, "npi" : npi, "state" : state, "division" : division, "region" : region, "metro" : metro, "short_zip" : short_zip}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # ensure valid date data type 
        dates = {"min_date" : min_date, "max_date" : max_date}
        for x in list(dates.items()):
            if x[1] != None:
                if type(x[1]) == str:
                    cqu.checkTypeDate(dateutil.parser.parse(x[1]).date(), x[0])
                else:
                    cqu.checkTypeDate(x[1], x[0])

        # ensure valid integer data type
        ints = {"limit" : limit, "age_min" : age_min, "age_max" : age_max}
        for x in list(ints.items()):
            if (x[1] != None):
                cqu.checkTypeInt(x[1], x[0])

        # normalize NPI output
        ref_npi = cqu.NPINorm(ref_npi)
        npi = cqu.NPINorm(npi)

        # raise error for invalid NPIs
        cqu.checkNPI(ref_npi, "ref_npi")
        cqu.checkNPI(npi, "npi")

        ### Input Quality Control ###

        # normalize code digit input
        # drg_code = cqu.codeNorm(drg_code, n = 3, punct = False)
        revenue_center_code = cqu.codeNorm(revenue_center_code, n = 4, punct = False)
        short_zip = cqu.codeNorm(short_zip, n = 3, punct = False)
        short_diag_code = cqu.codeNorm(short_diag_code, n = 3, punct = False)
        diag_code = cqu.codeNorm(diag_code, punct = False)

        # normalize strings -- lowercase, trim whitespace)
        gender = cqu.stringNorm(gender)
        visit_type = cqu.stringNorm(visit_type)
        payor_channel = cqu.stringNorm(payor_channel)
        place_of_service = cqu.stringNorm(place_of_service)
        # drg_code = cqu.stringNorm(drg_code)
        diag_code = cqu.stringNorm(diag_code)
        short_diag_code = cqu.stringNorm(short_diag_code)
        diag_category = cqu.stringNorm(diag_category)
        diag_subcategory = cqu.stringNorm(diag_subcategory)
        proc_code = cqu.stringNorm(proc_code)
        proc_category = cqu.stringNorm(proc_category)
        proc_subcategory = cqu.stringNorm(proc_subcategory)
        taxonomy_code = cqu.stringNorm(taxonomy_code)
        subspecialty = cqu.stringNorm(subspecialty)
        specialty = cqu.stringNorm(specialty)
        specialty_category = cqu.stringNorm(specialty_category)
        state = cqu.stringNorm(state)
        division = cqu.stringNorm(division)
        region = cqu.stringNorm(region)
        metro = cqu.stringNorm(metro)

        # ensure levels feature levels congeal
        cqu.checkLevels(visit_type, "visit_type", levels = 1)
        cqu.checkLevels(payor_channel, "payor_channel", levels = 1)
        cqu.checkLevels(place_of_service, "place_of_service", levels = 1)
        cqu.checkLevels(revenue_center_code, "revenue_center_code", levels = 2)
        # cqu.checkLevels(drg_code, "drg_code", levels = 2)
        cqu.checkLevels(ref_npi, "ref_npi", levels = 2)
        cqu.checkLevels(npi, "npi", levels = 2)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(gender, self.field_values.data, "gender")
        cqu.checkFieldValues(visit_type, self.field_values.data, "visit_type")
        cqu.checkFieldValues(payor_channel, self.field_values.data, "payor_channel")
        cqu.checkFieldValues(revenue_center_code, self.field_values.data, "revenue_center_code")
        cqu.checkFieldValues(place_of_service, self.field_values.data, "place_of_service")
        # cqu.checkFieldValues(drg_code, self.field_values.data, "drg_code")
        cqu.checkFieldValues(diag_category, self.field_values.data, "diag_category")
        cqu.checkFieldValues(diag_subcategory, self.field_values.data, "diag_subcategory")
        cqu.checkFieldValues(proc_code, self.field_values.data, "proc_code")
        cqu.checkFieldValues(proc_category, self.field_values.data, "proc_category")
        cqu.checkFieldValues(proc_subcategory, self.field_values.data, "proc_subcategory")
        cqu.checkFieldValues(taxonomy_code, self.field_values.data, "taxonomy_code")
        cqu.checkFieldValues(subspecialty, self.field_values.data, "subspecialty")
        cqu.checkFieldValues(specialty, self.field_values.data, "specialty")
        cqu.checkFieldValues(specialty_category, self.field_values.data, "specialty_category")
        cqu.checkFieldValues(state, self.field_values.data, "state")
        cqu.checkFieldValues(division, self.field_values.data, "division")
        cqu.checkFieldValues(region, self.field_values.data, "region")
        cqu.checkFieldValues(metro, self.field_values.data, "metro")

        ### Input Logic & Hierarchy ###

        # place of service hierarchy logic
        place_of_service = cqu.placeOfServicePriority(place_of_service, self.field_values.data)

        # diagnosis hierarchy logic
        diags, diag_greedy, warnings_list1 = cqu.diagnosisPriority(diag_code, short_diag_code, diag_subcategory, diag_category, diag_greedy, self.field_values.data)

        # procedure hierarchy logic
        procs, proc_greedy, warnings_list2 = cqu.procedurePriority(proc_code, proc_subcategory, proc_category, proc_greedy, self.field_values.data)

        # warning around drg and diag/proc overlap
        warnings_list3 = [] # cqu.checkDRGOverlap(drg_code, diags, procs)

        # procedure hierarchy logic
        taxonomies, taxonomy_greedy, warnings_list4 = cqu.taxonomyPriority(taxonomy_code, subspecialty, specialty, specialty_category, taxonomy_greedy, self.field_values.data)
        cqu.checkLevels(taxonomies, "taxonomies", levels = 2)

        # geography hierarchy priority
        states, zips, warnings_list5 = cqu.geoPriority(state, division, region, metro, short_zip, self.field_values.data)

        # warning around taxonomy and npi overlap
        warnings_list6 = cqu.checkNPIOverlap(taxonomies, ref_npi, npi)

        # collect warnings
        warnings_list = warnings_list1 + warnings_list2 + warnings_list3 + warnings_list4 + warnings_list5 + warnings_list6

        # make it pretty for Ray's SQL
        diags = cqu.stringNorm(cqu.listWrapString(diags), stringtype = "upper")
        procs = cqu.stringNorm(cqu.listWrapString(procs), stringtype = "upper")
        states = cqu.stringNorm(cqu.listWrapString(states), stringtype = "upper")
        gender = cqu.stringNorm(gender, stringtype = "upper")
        taxonomies = cqu.stringNorm(cqu.listWrapString(taxonomies), stringtype = "upper")
        payor_channel = cqu.stringNorm(cqu.listWrapString(payor_channel), stringtype = "title")
        visit_type = cqu.stringNorm(cqu.listWrapString(visit_type), stringtype = "title")
        npi = cqu.listWrapString(npi)
        ref_npi = cqu.listWrapString(ref_npi)
        zips = cqu.listWrapString(zips)

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "journey",
                 "min_date" : min_date,
                "max_date" : max_date,
                "gender" : gender,
                "age_min" : age_min,
                "age_max" : age_max,
                "visit_type" : visit_type,
                "payor_channel" : payor_channel,
                "revenue_center_code" : revenue_center_code,
                "place_of_service" :  place_of_service,
                "drg_code" : None,
                "diag_code" : diags,
                "proc_code" : procs,
                "taxonomy_code" : taxonomies,
                "ref_npi" : ref_npi,
                "npi" : npi,
                "state" : states,
                "short_zip" : zips,
                "greedy": False, # always keep false for now, implications too complicated for now
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        journey = CareQueryData(data, features = self.glossary.feature_detail("JOURNEY_TABLE"), show = show)

        return journey

    def nppesDetail(self,
                    gender = None,
                    taxonomy_code = None,
                    specialty_category = None,
                    specialty = None,
                    subspecialty = None,
                    npi = None,
                    state = None,
                    division = None,
                    region = None,
                    short_zip = None,
                    limit = None,
                    show = None):
        
        """
        Description:
        
            Specify the NPPES (a comprehensive national provider database) query details, from which you may then run the .execute() method on this query to return the corresponding rows in NPPES_TABLE.

        Parameters:
            gender (str or list(str)):
                Patient gender within the population of interest
                option(s): 'M' for Male, 'F' for Female, or ['M','F'] for both
                default(s): ['M','F']
            taxonomy_code (str or list(str) or list(list(str),list(str))):
                Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider
                option(s): Run self.field_values.list_values(field = "taxonomy_code") to see all taxonomy_code options
                default(s): Defaults to all taxonomy codes if left unspecified
            specialty (str or list(str) or list(list(str),list(str))):
                Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty") to see all specialty options
                default(s): Defaults to all specialties if left unspecified
            specialty_category (str or list(str) or list(list(str),list(str))):
                Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty_category") to see all specialty_category options
                default(s): Defaults to all specialty categories if left unspecified
            subspecialty (str or list(str) or list(list(str),list(str))):
                Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "subspecialty") to see all subspecialty options
                default(s): Defaults to all specialty subcategories if left unspecified
            npi (int or list(int) or list(list(int),list(int))):
                National Provider Identifier (NPI) of individual and organizational provider(s) of interest
                option(s): Any valid, registered individual or organizational National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            state (str or list(str) or list(list(str),list(str))):
                US State of the provider's NPPES registered address
                option(s): Run self.field_values.list_values(field = "state") to see all state options
                default(s): Defaults to all US States if left unspecified
            division (str or list(str) or list(list(str),list(str))):
                US State Division of the provider's NPPES registered address. There are nine distinct US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "division") to see all division options
                default(s): Defaults to all entire US if left unspecified
            region (str or list(str) or list(list(str),list(str))):
                US State Region of the provider's NPPES registered address. There are four major US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "region") to see all region options
                default(s): Defaults to all entire US if left unspecified
            zip (int or list(int) or list(list(int),list(int))):
                Primary zip code of the provider
                option(s): Any valid US zip code or list of zip codes
                default(s): Defaults to all entire US if left unspecified 
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: None
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: state = "NE"
                    example logic: Select data from the state of Nebraska
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: state = ["NE","CO"]
                    example logic: Select data from either Nebraska OR Colorado
                multi-selection AND: Is not possible with nppesDetail queries
            inter-parameter: Logical arguments ACROSS parameter specifications
                multi-selection AND: (default) Return data that meets either critera
                    example: state = "NE" and npi = 1234567920
                    example logic: Selecs all nebraska providers as well as provider 1234567920
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if gender == None:
            gender = ["M","F"]

        if (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"gender" : gender, "taxonomy_code" : taxonomy_code, "subspecialty": subspecialty, "specialty" : specialty, "specialty_category" : specialty_category, "npi" : npi, "state" : state, "division" : division, "region" : region, "metro" : metro, "short_zip" : short_zip}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # ensure valid integer data type
        ints = {"limit" : limit}
        for x in list(ints.items()):
            if (x[1] != None):
                cqu.checkTypeInt(x[1], x[0])

        # normalize NPI output
        npi = cqu.NPINorm(npi)

        # raise error for invalid NPIs
        cqu.checkNPI(npi, "npi")

        ### Input Quality Control ###

        # normalize code digit input
        zip = cqu.codeNorm(zip, n = 5, punct = False)
        
        # normalize strings -- lowercase, trim whitespace)
        gender = cqu.stringNorm(gender)
        taxonomy_code = cqu.stringNorm(taxonomy_code)
        subspecialty = cqu.stringNorm(subspecialty)
        specialty = cqu.stringNorm(specialty)
        specialty_category = cqu.stringNorm(specialty_category)
        state = cqu.stringNorm(state)
        division = cqu.stringNorm(division)
        region = cqu.stringNorm(region)

        # ensure levels feature levels congeal
        cqu.checkLevels(taxonomy_code, "taxonomy_code", levels = 1)
        cqu.checkLevels(subspecialty, "subspecialty", levels = 1)
        cqu.checkLevels(specialty, "specialty", levels = 1)
        cqu.checkLevels(specialty_category, "specialty_category", levels = 1)
        cqu.checkLevels(state, "state", levels = 1)
        cqu.checkLevels(division, "division", levels = 1)
        cqu.checkLevels(region, "region", levels = 1)
        cqu.checkLevels(npi, "npi", levels = 1)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(gender, self.field_values.data, "gender")
        cqu.checkFieldValues(taxonomy_code, self.field_values.data, "taxonomy_code")
        cqu.checkFieldValues(subspecialty, self.field_values.data, "subspecialty")
        cqu.checkFieldValues(specialty, self.field_values.data, "specialty")
        cqu.checkFieldValues(specialty_category, self.field_values.data, "specialty_category")
        cqu.checkFieldValues(state, self.field_values.data, "state")
        cqu.checkFieldValues(division, self.field_values.data, "division")
        cqu.checkFieldValues(region, self.field_values.data, "region")

        ### Input Logic & Hierarchy ###

        # procedure hierarchy logic
        taxonomy_greedy = True
        taxonomies, taxonomy_greedy, warnings_list1 = cqu.taxonomyPriority(taxonomy_code, subspecialty, specialty, specialty_category, taxonomy_greedy, self.field_values.data)
        cqu.checkLevels(taxonomies, "taxonomies", levels = 1)

        # geography hierarchy priority
        metro = None
        states, zips, warnings_list2 = cqu.geoPriority(state, division, region, metro, short_zip, self.field_values.data)

        # collect warnings
        warnings_list = warnings_list1 + warnings_list2

        # make it pretty for Ray's SQL
        gender = cqu.stringNorm(gender, stringtype = "upper")
        taxonomies = cqu.stringNorm(taxonomies, stringtype = "upper")

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.    
        data = {"query": "nppes-detail",
                "gender" : gender,
                "taxonomy_code" : taxonomies,
                "npi" : npi,
                "state" : states,
                "short_zip" : zips,
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        nppes = CareQueryData(data, features = self.glossary.feature_detail("NPPES_TABLE"), show = show)

        return nppes

    def diagDetail(self,
                   diag_code = None,
                   diag_category = None,
                   diag_subcategory = None,
                   short_diag_code = None,
                   limit = None,
                   show = None):
        
        """
        Description:
        
            Specify the diagnosis parameters for which you would like additional context, categories and ties. Users may then run the .execute() method on this query to return the corresponding rows in DIAG_TABLE.
        
        Parameters:

            diag_code (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis code
                option(s): Run self.field_values.list_values(field = "diag_code") to see all diag_code options
                default(s): Defaults to all diagnosis codes if left unspecified
            diag_category (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis category
                option(s): Run self.field_values.list_values(field = "diag_category") to see all diag_category options
                default(s): Defaults to all diagnosis categories if left unspecified
            diag_subcategory (str or list(str) or list(list(str),list(str))):
                ICD-10 diagnosis subcategory
                option(s): Run self.field_values.list_values(field = "diag_subcategory") to see all diag_subcategory options
                default(s): Defaults to all diagnosis subcategories if left unspecified
            short_diag_code (str or list(str) or list(list(str),list(str))):
                First three digits of ICD-10 code
                option(s): Run self.field_values.list_values(field = "short_diag_code") to see all short_diag_code options
                default(s): Defaults to all short diagnosis codes if left unspecified
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: None
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: short_diag_code = "E51"
                    example logic: Selects diagnosis that are within the E51 category
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: short_diag_code = ["E51","I10"]
                    example logic: Selects diagnosis that are within the E51 or I10 categories
            inter-parameter: Logical arguments ACROSS parameter specifications
                multi-selection: (default) Return data that meets either criterion
                    example: diag_subcategory = "abdominal and pelvic pain" and short_diag_code = ["I10"]
                    example logic: Selects all abdominal and pelvic pain diagnoses as well as I10 diagnsoses
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"diag_code" : diag_code, "short_diag_code" : short_diag_code, "diag_category":diag_category, "diag_subcategory": diag_subcategory}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        ### Input Quality Control ###

        # normalize code digit input
        short_diag_code = cqu.codeNorm(short_diag_code, n = 3, punct = False)
        diag_code = cqu.codeNorm(diag_code, punct = False)

        # normalize strings -- lowercase, trim whitespace)
        diag_code = cqu.stringNorm(diag_code)
        short_diag_code = cqu.stringNorm(short_diag_code)
        diag_category = cqu.stringNorm(diag_category)
        diag_subcategory = cqu.stringNorm(diag_subcategory)

        # ensure levels feature levels congeal
        cqu.checkLevels(diag_code, "diag_code", levels = 1)
        cqu.checkLevels(short_diag_code, "short_diag_code", levels = 1)
        cqu.checkLevels(diag_category, "diag_category", levels = 1)
        cqu.checkLevels(diag_subcategory, "diag_subcategory", levels = 1)
        
        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(diag_category, self.field_values.data, "diag_category")
        cqu.checkFieldValues(diag_subcategory, self.field_values.data, "diag_subcategory")

        ### Input Logic & Hierarchy ###

        # diagnosis hierarchy logic
        diag_greedy = True
        diags, diag_greedy, warnings_list = cqu.diagnosisPriority(diag_code, short_diag_code, diag_subcategory, diag_category, diag_greedy, self.field_values.data)

        # make it pretty for Ray's SQL
        diags = cqu.stringNorm(diags, stringtype = "upper")

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "diag-detail",
                "diag_code" : diags,
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        diag_detail = CareQueryData(data, features = self.glossary.feature_detail("DIAG_TABLE"), show = show)

        return diag_detail

    def procDetail(self,
                   proc_code = None,
                   proc_category = None,
                   proc_subcategory = None,
                   limit = None,
                   show = None):
        
        """
        Description:
        
            Specify the procedure parameters for which you would like additional context, categories and ties. Users may then run the .execute() method on this query to return the corresponding rows in PROC_TABLE.

        Parameters:
            
            proc_code (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural code performed
                option(s): Run self.field_values.list_values(field = "proc_code") to see all proc_code options
                default(s): Defaults to all procedure codes if left unspecified
            proc_category (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural category performed
                option(s): Run self.field_values.list_values(field = "proc_category") to see all proc_category options
                default(s): Defaults to all procedure categories if left unspecified
            proc_subcategory (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural subcategory performed
                option(s): Run self.field_values.list_values(field = "proc_subcategory") to see all proc_subcategory options
                default(s): Defaults to all procedure subcategories if left unspecified
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: None
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: state = "NE"
                    example logic: Select data from the state of Nebraska
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: state = ["NE","CO"]
                    example logic: Select data from either Nebraska OR Colorado
                multi-selection AND: Select multiple values across multiple lists to request results that meet both conditions
                    example: short_diag_code = [["I10"],["E11"]]
                    example logic: Select data where patients have hypertension (I10) AND type-2 diabetes (E11)
            inter-parameter: Logical arguments ACROSS parameter specifications
                multi-selection: (default) Return data that meets either criterion
                    example: proc_subcategory = "surgery - cardiovascular system" and short_diag_code = ["A9520"]
                    example logic: Selects all surgery - cardiovascular system procedures as well as A9520 procedure code
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"proc_code" : proc_code, "proc_category":proc_category, "proc_subcategory":proc_subcategory}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # ensure valid integer data type
        ints = {"limit" : limit}
        for x in list(ints.items()):
            if (x[1] != None):
                cqu.checkTypeInt(x[1], x[0])

        ### Input Quality Control ###

        # normalize strings -- lowercase, trim whitespace)
        proc_code = cqu.stringNorm(proc_code)
        proc_category = cqu.stringNorm(proc_category)
        proc_subcategory = cqu.stringNorm(proc_subcategory)

        # ensure levels feature levels congeal
        cqu.checkLevels(proc_code, "proc_code", levels = 1)
        cqu.checkLevels(proc_category, "proc_category", levels = 1)
        cqu.checkLevels(proc_subcategory, "proc_subcategory", levels = 1)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(proc_code, self.field_values.data, "proc_code")
        cqu.checkFieldValues(proc_category, self.field_values.data, "proc_category")
        cqu.checkFieldValues(proc_subcategory, self.field_values.data, "proc_subcategory")

        ### Input Logic & Hierarchy ###

        # procedure hierarchy logic
        proc_greedy = True
        procs, proc_greedy, warnings_list = cqu.procedurePriority(proc_code, proc_subcategory, proc_category, proc_greedy, self.field_values.data)

        # make it pretty for Ray's SQL
        procs = cqu.stringNorm(procs, stringtype = "upper")
        
        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "proc-detail",
                "proc_code" : procs,
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        proc_detail = CareQueryData(data, features = self.glossary.feature_detail("PROC_TABLE"), show = show)

        return proc_detail

    def specialtyDetail(self, 
                        taxonomy_code = None,
                        specialty_category = None,
                        specialty = None,
                        subspecialty = None,
                        limit = None,
                        show = None):
        
        """
        Description:
        
            Specify the specialty/taxonomy parameters for which you would like additional context, categories and ties. Users may then run the .execute() method on this query to return the corresponding rows in SPEC_TABLE.

        Parameters:

            taxonomy_code (str or list(str) or list(list(str),list(str))):
                Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider
                option(s): Run self.field_values.list_values(field = "taxonomy_code") to see all taxonomy_code options
                default(s): Defaults to all taxonomy codes if left unspecified
            specialty (str or list(str) or list(list(str),list(str))):
                Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty") to see all specialty options
                default(s): Defaults to all specialties if left unspecified
            specialty_category (str or list(str) or list(list(str),list(str))):
                Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty_category") to see all specialty_category options
                default(s): Defaults to all specialty categories if left unspecified
            subspecialty (str or list(str) or list(list(str),list(str))):
                Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "subspecialty") to see all subspecialty options
                default(s): Defaults to all specialty subcategories if left unspecified
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: 10000
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: state = "NE"
                    example logic: Select data from the state of Nebraska
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: state = ["NE","CO"]
                    example logic: Select data from either Nebraska OR Colorado
                multi-selection AND: Select multiple values across multiple lists to request results that meet both conditions
                    example: short_diag_code = [["I10"],["E11"]]
                    example logic: Select data where patients have hypertension (I10) AND type-2 diabetes (E11)
            inter-parameter: Logical arguments ACROSS parameter specifications
                multi-selection: Returns data that meets either criteria
                    example: spec_category = 'physician assistants & advanced practice nursing providers' and specialty = 'allergy & immunology'
                    example logic: Selects any/all taxonomies related to either physician assistants & advanced practice nursing providers or allergy & immunology
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"taxonomy_code" : taxonomy_code, "subspecialty": subspecialty, "specialty" : specialty, "specialty_category" : specialty_category}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # ensure valid integer data type
        ints = {"limit" : limit}
        for x in list(ints.items()):
            if (x[1] != None):
                cqu.checkTypeInt(x[1], x[0])

        ### Input Quality Control ###

        # normalize strings -- lowercase, trim whitespace)
        taxonomy_code = cqu.stringNorm(taxonomy_code)
        subspecialty = cqu.stringNorm(subspecialty)
        specialty = cqu.stringNorm(specialty)
        specialty_category = cqu.stringNorm(specialty_category)

        # ensure levels feature levels congeal
        cqu.checkLevels(taxonomy_code, "taxonomy_code", levels = 1)
        cqu.checkLevels(subspecialty, "subspecialty", levels = 1)
        cqu.checkLevels(specialty, "specialty", levels = 1)
        cqu.checkLevels(specialty_category, "specialty_category", levels = 1)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(taxonomy_code, self.field_values.data, "taxonomy_code")
        cqu.checkFieldValues(subspecialty, self.field_values.data, "subspecialty")
        cqu.checkFieldValues(specialty, self.field_values.data, "specialty")
        cqu.checkFieldValues(specialty_category, self.field_values.data, "specialty_category")

        ### Input Logic & Hierarchy ###

        # procedure hierarchy logic
        taxonomy_greedy = True
        taxonomies, taxonomy_greedy, warnings_list = cqu.taxonomyPriority(taxonomy_code, subspecialty, specialty, specialty_category, taxonomy_greedy, self.field_values.data)
        cqu.checkLevels(taxonomies, "taxonomies", levels = 1)

        # make it pretty for Ray's SQL
        taxonomies = cqu.stringNorm(taxonomies, stringtype = "upper")

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "spec-detail",
                "taxonomy_code" : taxonomies,
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        spec_detail = CareQueryData(data, features = self.glossary.feature_detail("SPEC_TABLE"), show = show)

        return spec_detail

    def mipsDetail(self,
                      npi = None,
                      limit = None,
                      show = None):
        
        """
        Description:
        
            Query to request Merit-based Incentive Payment System (MIPS) performance information for specified providers.
        
        Parameters:
            
            npi (int or list(int) or list(list(int),list(int))):
                National Provider Identifier (NPI) of individual and organizational provider(s) of interest
                option(s): Any valid, registered individual or organizational National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: 10000
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: state = "NE"
                    example logic: Select data from the state of Nebraska
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: state = ["NE","CO"]
                    example logic: Select data from either Nebraska OR Colorado
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"npi" : npi}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # ensure valid integer data type
        ints = {"limit" : limit}
        for x in list(ints.items()):
            if (x[1] != None):
                cqu.checkTypeInt(x[1], x[0])

        # normalize NPI output
        npi = cqu.NPINorm(npi)

        # raise error for invalid NPIs
        cqu.checkNPI(npi, "npi")

        ### Input Quality Control ###

        # ensure levels feature levels congeal
        cqu.checkLevels(npi, "npi", levels = 1)

        ### Construct Final JSON ###

        #Define the API request data elements.
        data = {"query": "mips-detail",
                "npi" : npi,
                "limit" : None,
                "warnings": None,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        mips = CareQueryData(data, features = self.glossary.feature_detail("MIPS_TABLE"), show = show)

        return mips

    def geoDetail(self,
                  short_zip = None,
                  state = None,
                  division = None,
                  region = None,
                  metro = None,
                  limit = None,
                  show = None):
        
        """
        Description:
        
            Query to specify geographic detail around zip, county, metro, state or region - including US Census population statistics at each level.

        Parameters:
            
            short_zip (int or list(int) or list(list(int),list(int))):
                First three digits the zip code of the query patient population specified
                option(s): Run self.field_values.list_values(field = "short_zip") to see all short_zip options
                default(s): Defaults to all entire US population if left unspecified
            metro (str or list(str) or list(list(str),list(str))):
                Metropolitan and micropolitan statistical areas according to the US Census Bureau
                option(s): Run self.field_values.list_values(field = "metro") to see all metro options
                default(s): Defaults to all entire US population if left unspecified
            state (str or list(str) or list(list(str),list(str))):
                option(s): Run self.field_values.list_values(field = "state") to see all state options
                default(s): Defaults to all US States if left unspecified
            division (str or list(str) or list(list(str),list(str))):
                District residence of the query patient population. There are nine distinct US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "division") to see all division options
                default(s): Defaults to all entire US population if left unspecified
            region (str or list(str) or list(list(str),list(str))):
                Regional residence of the query patient population. There are four major US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "region") to see all region options
                default(s): Defaults to all entire US population if left unspecified 
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: 10000
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"state" : state, "division" : division, "region" : region, "metro" : metro, "short_zip" : short_zip}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # ensure valid integer data type
        ints = {"limit" : limit}
        for x in list(ints.items()):
            if (x[1] != None):
                cqu.checkTypeInt(x[1], x[0])

        ### Input Quality Control ###

        # normalize code digit input
        short_zip = cqu.codeNorm(short_zip, n = 3, punct = False)

        # normalize strings -- lowercase, trim whitespace)
        state = cqu.stringNorm(state)
        division = cqu.stringNorm(division)
        region = cqu.stringNorm(region)
        metro = cqu.stringNorm(metro)

        # ensure levels feature levels congeal
        cqu.checkLevels(state, "state", levels = 1)
        cqu.checkLevels(division, "division", levels = 1)
        cqu.checkLevels(region, "region", levels = 1)
        cqu.checkLevels(metro, "metro", levels = 1)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(state, self.field_values.data, "state")
        cqu.checkFieldValues(division, self.field_values.data, "division")
        cqu.checkFieldValues(region, self.field_values.data, "region")
        cqu.checkFieldValues(metro, self.field_values.data, "metro")

        ### Input Logic & Hierarchy ###

        # geography hierarchy priority
        states, zips, warnings_list = cqu.geoPriority(state, division, region, metro, short_zip, self.field_values.data)

        # make it pretty for Ray's SQL
        states = cqu.stringNorm(states, stringtype = "upper")

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "geo-detail",
                "state" : states,
                "short_zip" : zips,
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        geo = CareQueryData(data, features = self.glossary.feature_detail("GEO_TABLE"), show = show)

        return geo
    
    def execOutreach(self,
                     hospital = None,
                     exec_level = None,
                     department = None,
                     state = None,
                     division = None,
                     region = None,
                     short_zip = None,
                     npi = None,
                     limit = None,
                     show = None):
        
        """
        Description:
        
            Query to specify executive email, phone and address data - including context around their role and seniority.
        
        Parameters:
            
            hospital (str or list(str) or list(list(str),list(str))):
                Primary hospital affiliated with the executive record
                option(s): Run self.field_values.list_values(field = "hospital") to see all hospital options
                default(s): Defaults to all hospital if left unspecified
            exec_level (str or list(str) or list(list(str),list(str))):
                Adiministrative level associated with the executive's role
                option(s): Run self.field_values.list_values(field = "exec_level") to see all exec_level options
                default(s): Defaults to all exec_level if left unspecified
            department (str or list(str) or list(list(str),list(str))):
                Functional department associated with the executive's role
                option(s): Run self.field_values.list_values(field = "department") to see all department options
                default(s): Defaults to all department if left unspecified
            npi (int or list(int) or list(list(int),list(int))):
                National Provider Identifier (NPI) of individual and organizational provider(s) of interest
                option(s): Any valid, registered individual or organizational National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            state (str or list(str) or list(list(str),list(str))):
                US State code of the individual provider record
                option(s): Run self.field_values.list_values(field = "state") to see all state options
                default(s): Defaults to all US States if left unspecified
            division (str or list(str) or list(list(str),list(str))):
                District residence of the query patient population. There are nine distinct US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "division") to see all division options
                default(s): Defaults to all entire US population if left unspecified
            region (str or list(str) or list(list(str),list(str))):
                Regional residence of the query patient population. There are four major US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "region") to see all region options
                default(s): Defaults to all entire US population if left unspecified
            metro (str or list(str) or list(list(str),list(str))):
                Metropolitan and micropolitan statistical areas according to the US Census Bureau
                option(s): Run self.field_values.list_values(field = "metro") to see all metro options
                default(s): Defaults to all entire US population if left unspecified
            short_zip (int or list(int) or list(list(int),list(int))):
                First three digits the zip code of the query patient population specified
                option(s): Run self.field_values.list_values(field = "short_zip") to see all short_zip options
                default(s): Defaults to all entire US population if left unspecified 
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: No Limit
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"npi" : npi, "state" : state, "division" : division, "region" : region, "short_zip" : short_zip, "metro":metro}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # normalize NPI output
        npi = cqu.NPINorm(npi)

        # raise error for invalid NPIs
        cqu.checkNPI(npi, "npi")

        ### Input Quality Control ###

        # normalize code digit input
        short_zip = cqu.codeNorm(short_zip, n = 3, punct = False)
        
        # normalize strings -- lowercase, trim whitespace)
        metro = cqu.stringNorm(metro)
        state = cqu.stringNorm(state)
        division = cqu.stringNorm(division)
        region = cqu.stringNorm(region)

        # ensure levels feature levels congeal
        cqu.checkLevels(hospital, "hospital", levels = 1)
        cqu.checkLevels(exec_level, "exec_level", levels = 1)
        cqu.checkLevels(department, "department", levels = 1)
        cqu.checkLevels(state, "state", levels = 1)
        cqu.checkLevels(division, "division", levels = 1)
        cqu.checkLevels(region, "region", levels = 1)
        cqu.checkLevels(short_zip, "short_zip", levels = 1)
        cqu.checkLevels(npi, "npi", levels = 1)
        cqu.checkLevels(metro, "metro", levels = 1)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(hospital, self.field_values.data, "hospital")
        cqu.checkFieldValues(exec_level, self.field_values.data, "exec_level")
        cqu.checkFieldValues(department, self.field_values.data, "department")
        cqu.checkFieldValues(state, self.field_values.data, "state")
        cqu.checkFieldValues(division, self.field_values.data, "division")
        cqu.checkFieldValues(region, self.field_values.data, "region")
        cqu.checkFieldValues(metro, self.field_values.data, "metro")

        ### Input Logic & Hierarchy ###

        # geography hierarchy priority
        states, zips, warnings_list = cqu.geoPriority(state, division, region, metro, short_zip, self.field_values.data)

        # make it pretty for Ray's SQL
        states = cqu.stringNorm(states, stringtype = "upper")

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "exec-outreach",
                "hospital":hospital,
                "exec_level":exec_level,
                "department":department,
                "npi" : npi,
                "state" : states,
                "short_zip" : zips,
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        exec = CareQueryData(data, features = self.glossary.feature_detail("EXEC_OUTREACH_TABLE"), show = show)

        return exec

    def providerOutreach(self,
                         taxonomy_code = None,
                         subspecialty = None,
                         specialty_category = None,
                         specialty = None,
                         npi = None,
                         state = None,
                         division = None,
                         region = None,
                         metro = None,
                         short_zip = None,
                         limit = None,
                         show = None):
        
        """
        Description:
        
            Query to specify data request for individual healthcare providers and their accompanying contact information, including email, phone and fax.

        Parameters:
            
            taxonomy_code (str or list(str) or list(list(str),list(str))):
                Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider
                option(s): Run self.field_values.list_values(field = "taxonomy_code") to see all taxonomy_code options
                default(s): Defaults to all taxonomy codes if left unspecified
            subspecialty (str or list(str) or list(list(str),list(str))):
                Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "subspecialty") to see all subspecialty options
                default(s): Defaults to all specialty subcategories if left unspecified
            specialty (str or list(str) or list(list(str),list(str))):
                Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty") to see all specialty options
                default(s): Defaults to all specialties if left unspecified
            specialty_category (str or list(str) or list(list(str),list(str))):
                Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty_category") to see all specialty_category options
                default(s): Defaults to all specialty categories if left unspecified
            ref_npi (int or list(int) or list(list(int),list(int))):
                Referring provider(s) indicated by National Provider Identifiers (NPIs)
                option(s): Any valid, registered individual National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            npi (int or list(int) or list(list(int),list(int))):
                National Provider Identifier (NPI) of individual and organizational provider(s) of interest
                option(s): Any valid, registered individual or organizational National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            state (str or list(str) or list(list(str),list(str))):
                option(s): Run self.field_values.list_values(field = "state") to see all state options
                default(s): Defaults to all US States if left unspecified
            division (str or list(str) or list(list(str),list(str))):
                District residence of the query patient population. There are nine distinct US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "division") to see all division options
                default(s): Defaults to all entire US population if left unspecified
            region (str or list(str) or list(list(str),list(str))):
                Regional residence of the query patient population. There are four major US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "region") to see all region options
                default(s): Defaults to all entire US population if left unspecified
            metro (str or list(str) or list(list(str),list(str))):
                Metropolitan and micropolitan statistical areas according to the US Census Bureau
                option(s): Run self.field_values.list_values(field = "metro") to see all metro options
                default(s): Defaults to all entire US population if left unspecified
            short_zip (int or list(int) or list(list(int),list(int))):
                First three digits the zip code of the query patient population specified
                option(s): Run self.field_values.list_values(field = "short_zip") to see all short_zip options
                default(s): Defaults to all entire US population if left unspecified 
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: 10000
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"taxonomy_code" : taxonomy_code, "subspecialty": subspecialty, "specialty" : specialty, "specialty_category" : specialty_category, "npi" : npi, "state" : state, "metro" : metro, "division" : division, "region" : region, "short_zip" : short_zip}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # normalize NPI output
        npi = cqu.NPINorm(npi)

        # raise error for invalid NPIs
        cqu.checkNPI(npi, "npi")

        ### Input Quality Control ###

        # normalize code digit input
        short_zip = cqu.codeNorm(short_zip, n = 3, punct = False)
        
        # normalize strings -- lowercase, trim whitespace)
        taxonomy_code = cqu.stringNorm(taxonomy_code)
        subspecialty = cqu.stringNorm(subspecialty)
        specialty = cqu.stringNorm(specialty)
        specialty_category = cqu.stringNorm(specialty_category)
        metro = cqu.stringNorm(metro)
        state = cqu.stringNorm(state)
        division = cqu.stringNorm(division)
        region = cqu.stringNorm(region)

        # ensure levels feature levels congeal
        cqu.checkLevels(taxonomy_code, "taxonomy_code", levels = 1)
        cqu.checkLevels(subspecialty, "subspecialty", levels = 1)
        cqu.checkLevels(specialty_category, "specialty_category", levels = 1)
        cqu.checkLevels(specialty, "specialty", levels = 1)
        cqu.checkLevels(npi, "npi", levels = 1)
        cqu.checkLevels(division, "division", levels = 1)
        cqu.checkLevels(region, "region", levels = 1)
        cqu.checkLevels(metro, "metro", levels = 1)
        cqu.checkLevels(short_zip, "short_zip", levels = 1)

        # check to see if inputs are within corresponding field value space\
        cqu.checkFieldValues(taxonomy_code, self.field_values.data, "taxonomy_code")
        cqu.checkFieldValues(subspecialty, self.field_values.data, "subspecialty")
        cqu.checkFieldValues(specialty, self.field_values.data, "specialty")
        cqu.checkFieldValues(specialty_category, self.field_values.data, "specialty_category")
        cqu.checkFieldValues(state, self.field_values.data, "state")
        cqu.checkFieldValues(division, self.field_values.data, "division")
        cqu.checkFieldValues(region, self.field_values.data, "region")
        cqu.checkFieldValues(metro, self.field_values.data, "metro")

        ### Input Logic & Hierarchy ###

        # procedure hierarchy logic
        taxonomy_greedy = True
        taxonomies, taxonomy_greedy, warnings_list1 = cqu.taxonomyPriority(taxonomy_code, subspecialty, specialty, specialty_category, taxonomy_greedy, self.field_values.data)

        # geography hierarchy priority
        states, zips, warnings_list2 = cqu.geoPriority(state, division, region, metro, short_zip, self.field_values.data)

        # warning around taxonomy and npi overlap
        ref_npi = None
        warnings_list3 = cqu.checkNPIOverlap(taxonomies, ref_npi, npi)

        # collect warnings
        warnings_list = warnings_list1 + warnings_list2 + warnings_list3

        # make it pretty for Ray's SQL
        states = cqu.stringNorm(states, stringtype = "upper")
        taxonomies = cqu.stringNorm(taxonomies, stringtype = "upper")

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "prov-outreach",
                "taxonomy_code" : taxonomies,
                "npi" : npi,
                "state" : states,
                "short_zip" : zips,
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        provo = CareQueryData(data, features = self.glossary.feature_detail("PROV_OUTREACH_TABLE"), show = show)

        return provo

    def affiliationActivity(self,
                            npi = None,
                            system = None,
                            taxonomy_code = None,
                            specialty_category = None,
                            specialty = None,
                            subspecialty = None,
                            short_zip = None,
                            metro = None,
                            state = None,
                            division = None,
                            region = None,
                            lookback_period = None,
                            limit = None,
                            show = None):
        
        """
        Description:
        
            Query to specify health system provider affiliation query parameters to return nuanced affiliation data, including the actual claims activity-by-affiliation for each provider.

        Parameters:

            npi (int or list(int) or list(list(int),list(int))):
                National Provider Identifier (NPI) of individual and organizational provider(s) of interest
                option(s): Any valid, registered individual or organizational National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            Name of the system(s) with which an individual or organizational healthcare provider may be affiliated with in any way
                option(s): Please see self.glossary.list_options(parameter = "system") for all system parameter options
                default(s): Must be a single string from the designated list of system names
            taxonomy_code (str or list(str):
                Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider
                option(s): Run self.field_values.list_values(field = "taxonomy_code") to see all taxonomy_code options
                default(s): Defaults to all taxonomy codes if left unspecified
            specialty (str or list(str) or list(list(str),list(str))):
                Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty") to see all specialty options
                default(s): Defaults to all specialties if left unspecified
            specialty_category (str or list(str) or list(list(str),list(str))):
                Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty_category") to see all specialty_category options
                default(s): Defaults to all specialty categories if left unspecified
            subspecialty (str or list(str) or list(list(str),list(str))):
                Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "subspecialty") to see all subspecialty options
                default(s): Defaults to all specialty subcategories if left unspecified
            state (str or list(str) or list(list(str),list(str))):
                US State for the primary NPPES location 
                option(s): Run self.field_values.list_values(field = "state") to see all state options
                default(s): Defaults to all US States if left unspecified
            division (str or list(str) or list(list(str),list(str))):
                District residence of the query patient population. There are nine distinct US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "division") to see all division options
                default(s): Defaults to all entire US population if left unspecified
            region (str or list(str) or list(list(str),list(str))):
                Regional residence of the query patient population. There are four major US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "region") to see all region options
                default(s): Defaults to all entire US population if left unspecified
            metro (str or list(str) or list(list(str),list(str))):
                Metropolitan and micropolitan statistical areas according to the US Census Bureau
                option(s): Run self.field_values.list_values(field = "metro") to see all metro options
                default(s): Defaults to all entire US population if left unspecified
            short_zip (int or list(int) or list(list(int),list(int))):
                First three digits the zip code of the query patient population specified
                option(s): Run self.field_values.list_values(field = "short_zip") to see all short_zip options
                default(s): Defaults to all entire US population if left unspecified 
            lookback_period (str):
                String indicating the quarter and year of the provider practice affiliation behavior 1-year lookback window.
                option(s): Name the year and quarter as 'Q3-2023' of the lookback period, or specify 'current' for the most recent affiliation pattern data
                default: 'current'
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: None
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: state = "NE"
                    example logic: Select data from the state of Nebraska
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: state = ["NE","CO"]
                    example logic: Select data from either Nebraska OR Colorado
            inter-parameter: Logical arguments ACROSS parameter specifications
                multi-selection AND: (default) Return data that meets both criterion
                    example: self.encounter(state = "NE", short_diag_code = ["I10"])
                    example logic: Select all hypertensive encounters in Nebraska
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True
        if lookback_period == None:
            lookback_period = "current"

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"system":system, "lookback_period":lookback_period, "taxonomy_code" : taxonomy_code, "subspecialty": subspecialty, "specialty" : specialty, "specialty_category" : specialty_category, "npi" : npi, "state" : state, "division" : division, "region" : region, "metro" : metro, "short_zip" : short_zip}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # normalize NPI output
        npi = cqu.NPINorm(npi)

        # raise error for invalid NPIs
        cqu.checkNPI(npi, "npi")

        ### Input Quality Control ###

        # normalize code digit input
        short_zip = cqu.codeNorm(short_zip, n = 3, punct = False)
        short_diag_code = cqu.codeNorm(short_diag_code, n = 3, punct = False)
        diag_code = cqu.codeNorm(diag_code, punct = False)

        # normalize strings -- lowercase, trim whitespace)
        system = cqu.stringNorm(system)
        lookback_period = cqu.stringNorm(lookback_period)
        taxonomy_code = cqu.stringNorm(taxonomy_code)
        subspecialty = cqu.stringNorm(subspecialty)
        specialty = cqu.stringNorm(specialty)
        specialty_category = cqu.stringNorm(specialty_category)
        state = cqu.stringNorm(state)
        division = cqu.stringNorm(division)
        region = cqu.stringNorm(region)
        metro = cqu.stringNorm(metro)

        # ensure levels feature levels congeal
        cqu.checkLevels(npi, "npi", levels = 1)
        cqu.checkLevels(system, "system", levels = 1)
        cqu.checkLevels(taxonomy_code, "taxonomy_code", levels = 1)
        cqu.checkLevels(specialty_category, "specialty_category", levels = 1)
        cqu.checkLevels(specialty, "specialty", levels = 1)
        cqu.checkLevels(subspecialty, "subspecialty", levels = 1)
        cqu.checkLevels(short_zip, "short_zip", levels = 1)
        cqu.checkLevels(metro, "metro", levels = 1)
        cqu.checkLevels(state, "state", levels = 1)
        cqu.checkLevels(division, "division", levels = 1)
        cqu.checkLevels(region, "region", levels = 1)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(system, self.field_values.data, "system")
        cqu.checkFieldValues(taxonomy_code, self.field_values.data, "taxonomy_code")
        cqu.checkFieldValues(subspecialty, self.field_values.data, "subspecialty")
        cqu.checkFieldValues(specialty, self.field_values.data, "specialty")
        cqu.checkFieldValues(specialty_category, self.field_values.data, "specialty_category")
        cqu.checkFieldValues(state, self.field_values.data, "state")
        cqu.checkFieldValues(division, self.field_values.data, "division")
        cqu.checkFieldValues(region, self.field_values.data, "region")
        cqu.checkFieldValues(metro, self.field_values.data, "metro")

        ### Input Logic & Hierarchy ###

        # procedure hierarchy logic
        taxonomy_greedy = True
        taxonomies, taxonomy_greedy, warnings_list1 = cqu.taxonomyPriority(taxonomy_code, subspecialty, specialty, specialty_category, taxonomy_greedy, self.field_values.data)

        # geography hierarchy priority
        states, zips, warnings_list2 = cqu.geoPriority(state, division, region, metro, short_zip, self.field_values.data)

        # collect warnings
        warnings_list = warnings_list1 + warnings_list2

        # make it pretty for Ray's SQL
        states = cqu.stringNorm(states, stringtype = "upper")
        taxonomies = cqu.stringNorm(taxonomies, stringtype = "upper")

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "provider-affiliation",
                "system": system,
                "taxonomy_code" : taxonomies,
                "npi" : npi,
                "state" : states,
                "short_zip" : zips,
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        affl = CareQueryData(data, features = self.glossary.feature_detail("PROV_AFFILIATION_TABLE"), show = show)

        return affl
      
    def updateAffiliation(self,
                          system = None,
                          remove_npi = None,
                          add_npi = None,
                          show = None):
        
        """
        Description:
            
            Query to update health system and provider affiliations given provider/system parameters given.

        Parameters:

            system (str):
                Name of the system an individual provider may be affiliated with in any way
                option(s): Please see self.glossary.list_options(parameter = "system") for all system parameter options
                default(s): Must be a single string from the designated list of system names
            remove_npi (int or list(int) or list(str)):
                National Provider Identifier (NPI) of individual and organizational provider(s) of interest
                option(s): Any valid, registered individual or organizational National Provider Identifier in the US
                default(s): None
            add_npi (int or list(int) or list(str)):
                National Provider Identifier(s) (NPIs) of individual and organizational provider(s) for which a user would like to remove from the designated system affiliation 
                option(s): Any valid, registered individual or organizational National Provider Identifier in the US
                default(s): None
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if (remove_npi != None) | (add_npi != None):
            raise ValueError("One must only specify a list of National Provider Identifiers (NPIs) to add or remove at any one time.")

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"remove_npi":remove_npi, "add_npi":add_npi, "system" : system}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # normalize NPI output
        add_npi = cqu.NPINorm(add_npi)
        remove_npi = cqu.NPINorm(remove_npi)

        # raise error for invalid NPIs
        cqu.checkNPI(add_npi, "npi")
        cqu.checkNPI(remove_npi, "npi")

        ### Input Quality Control ###

        # normalize strings -- lowercase, trim whitespace)
        system = cqu.stringNorm(system)

        # ensure levels feature levels congeal
        if type(system) != str:
            raise ValueError("Only one 'system' may be specified at a time and represented as a single string value, such as system = 'hca healthcare'")
        cqu.checkLevels(remove_npi, "remove_npi", levels = 1)
        cqu.checkLevels(add_npi, "add_npi", levels = 1)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(system, self.field_values.data, "system")

        #Define the API request data elements.
        data = {"query": "provider-affiliation",
                "system": system,
                "remove_npi" : remove_npi,
                "add_npi" : add_npi,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        update = CareQueryData(data, features = self.glossary.feature_detail("AFFILIATION_TABLE"), show = show)

        return update
      
    def procAllowedAvgs(self,
                       visit_type = None,
                       payor_channel = None,
                       proc_code = None,
                       proc_category = None,
                       proc_subcategory = None,
                       state = None,
                       division = None,
                       region = None,
                       lookback_period = None,
                       limit = None,
                       show = None):
        
        """
        Description:
        
            Query specify procedure-encounter-based criterion to return statistical data around healthcare claim allowed amounts.

        Parameters:
            
            visit_type (str or list(str) or list(list(str),list(str))):
                Description of the setting of care
                option(s): Run self.field_values.list_values(field = "visit_type") to see all visit_type options
                default(s): Defaults to all visit types if left unspecified
            payor_channel (str or list(str) or list(list(str),list(str))):
                Health Insurance Payor channel-of-business or line-of-business
                option(s): Run self.field_values.list_values(field = "payor_channel") to see all payor_channel options
                default(s): Defaults to all payor channels if left unspecified
            proc_code (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural code performed
                option(s): Run self.field_values.list_values(field = "proc_code") to see all proc_code options
                default(s): Defaults to all procedure codes if left unspecified
            proc_category (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural category performed
                option(s): Run self.field_values.list_values(field = "proc_category") to see all proc_category options
                default(s): Defaults to all procedure categories if left unspecified
            proc_subcategory (str or list(str) or list(list(str),list(str))):
                CPT or HCPCS procedural subcategory performed
                option(s): Run self.field_values.list_values(field = "proc_subcategory") to see all proc_subcategory options
                default(s): Defaults to all procedure subcategories if left unspecified
            state (str or list(str) or list(list(str),list(str))):
                option(s): Run self.field_values.list_values(field = "state") to see all state options
                default(s): Defaults to all US States if left unspecified
            division (str or list(str) or list(list(str),list(str))):
                District residence of the query patient population. There are nine distinct US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "division") to see all division options
                default(s): Defaults to all entire US population if left unspecified
            region (str or list(str) or list(list(str),list(str))):
                Regional residence of the query patient population. There are four major US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "region") to see all region options
                default(s): Defaults to all entire US population if left unspecified
            lookback_period (str):
                String indicating the quarter and year of the provider practice affiliation behavior 1-year lookback window.
                option(s): Name the year and quarter as 'Q3-2023' of the lookback period, or specify 'current' for the most recent affiliation pattern data
                default: 'current'
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: 10000
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"lookback_period" : lookback_period, "visit_type" : visit_type, "payor_channel" : payor_channel, "proc_code" : proc_code, "proc_category":proc_category, "proc_subcategory":proc_subcategory, "state" : state, "division" : division, "region" : region}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # normalize NPI output
        npi = cqu.NPINorm(npi)

        # raise error for invalid NPIs
        cqu.checkNPI(npi, "npi")

        ### Input Quality Control ###

        # normalize strings -- lowercase, trim whitespace)
        lookback_period = cqu.stringNorm(lookback_period)
        visit_type = cqu.stringNorm(visit_type)
        payor_channel = cqu.stringNorm(payor_channel)
        proc_code = cqu.stringNorm(proc_code)
        proc_category = cqu.stringNorm(proc_category)
        proc_subcategory = cqu.stringNorm(proc_subcategory)
        state = cqu.stringNorm(state)
        division = cqu.stringNorm(division)
        region = cqu.stringNorm(region)

        # ensure levels feature levels congeal
        cqu.checkLevels(visit_type, "visit_type", levels = 1)
        cqu.checkLevels(payor_channel, "payor_channel", levels = 1)
        cqu.checkLevels(proc_code, "proc_code", levels = 1)
        cqu.checkLevels(proc_category, "proc_category", levels = 1)
        cqu.checkLevels(proc_subcategory, "proc_subcategory", levels = 1)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(visit_type, self.field_values.data, "visit_type")
        cqu.checkFieldValues(payor_channel, self.field_values.data, "payor_channel")
        cqu.checkFieldValues(proc_code, self.field_values.data, "proc_code")
        cqu.checkFieldValues(proc_category, self.field_values.data, "proc_category")
        cqu.checkFieldValues(proc_subcategory, self.field_values.data, "proc_subcategory")
        cqu.checkFieldValues(state, self.field_values.data, "state")
        cqu.checkFieldValues(division, self.field_values.data, "division")
        cqu.checkFieldValues(region, self.field_values.data, "region")

        ### Input Logic & Hierarchy ###

        # procedure hierarchy logic
        proc_greedy = True
        procs, proc_greedy, warnings_list1 = cqu.procedurePriority(proc_code, proc_subcategory, proc_category, proc_greedy, self.field_values.data)

        # geography hierarchy priority
        metro = None
        short_zip = None
        states, zips, warnings_list2 = cqu.geoPriority(state, division, region, metro, short_zip, self.field_values.data)

        # collect warnings
        warnings_list = warnings_list1 + warnings_list2

        # make it pretty for Ray's SQL
        procs = cqu.stringNorm(procs, stringtype = "upper")
        states = cqu.stringNorm(states, stringtype = "upper")
        gender = cqu.stringNorm(gender, stringtype = "upper")
        payor_channel = cqu.stringNorm(payor_channel, stringtype = "title")
        visit_type = cqu.stringNorm(visit_type, stringtype = "title")

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "avg-allowed",
                "visit_type" : visit_type,
                "payor_channel" : payor_channel,
                "proc_code" : procs,
                "state" : states,
                "lookback_period":lookback_period,
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        allowed = CareQueryData(data, features = self.glossary.feature_detail("ALLOWED_AVGS_TABLE"), show = show)

        return allowed
    
    def scriptEncounter(self, 
                        min_date = None,
                        max_date = None,
                        gender = None,
                        age_min = None,
                        age_max = None,
                        ndc = None,
                        pharm_class = None,
                        substance = None,
                        marketing_category = None,
                        script_greedy = None,
                        taxonomy_code = None,
                        specialty_category = None,
                        specialty = None,
                        subspecialty = None,
                        taxonomy_greedy = None,
                        npi = None,
                        state = None,
                        division = None,
                        region = None,
                        metro = None,
                        short_zip = None,
                        limit = None,
                        show = None):
        
        """
        Description:
        
            Query patient prescription claims that meet the specified criterion with line item detail.
        
        Parameters:

            min_date (str):
                Lower threshold date within the date range of interest, observational start date
                option(s): "2023-01-01" or "01/01/2023" 
                default: 90 days prior to date of query
            max_date (str):
                Upper threshold date within the date range of interest, observational end date
                option(s): "2023-01-01" or "01/01/2023" 
                default: 30 days prior to date of query
            gender (str or list(str)):
                Patient gender within the population of interest
                option(s): 'M' for Male, 'F' for Female, or ['M','F'] for both
                default(s): ['M','F']
            age_min (int):
                Minimum patient age identified within the population of interest
                option(s): 0 to 120
                default: 0
            age_max (int):
                Maximum patient age identified within the population of interest
                option(s): 0 to 120
                default: 120
            ndc (str or list(str) or list(list(str),list(str))):
                FDA National Drug Code version 11 standardized code for a dispensed drug
                option(s): xxx
                default(s): Defaults to all National Drug Codes (NDCs) if left unspecified
            pharm_class (str or list(str) or list(list(str),list(str))):
                Classifications of a drug product based on its therapeutic action, or how it works in the body
                option(s): Run self.field_values.list_values(field = "pharm_class") to see all pharm_class options
                default(s): Defaults to all National Drug Code (NDC) pharmaceutical classes if left unspecified
            script_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple prescription parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified prescription needs to be present within the returned results, False indicates all prescription must be present for the returned results
                default: True
            substance (str or list(str) or list(list(str),list(str))):
                The active ingredient in a drug product
                option(s): Run self.field_values.list_values(field = "substance") to see all substance options
                default(s): Defaults to all National Drug Code Substances if left unspecified
            marketing_category (str or list(str) or list(list(str),list(str))):
                Classification of a drug product based on its regulatory status and how it is marketed
                option(s): Run self.field_values.list_values(field = "marketing_category") to see all marketing_category options
                default(s): Defaults to all National Drug Code Marketing Categories if left unspecified
            taxonomy_code (str or list(str) or list(list(str),list(str))):
                Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider
                option(s): Run self.field_values.list_values(field = "taxonomy_code") to see all taxonomy_code options
                default(s): Defaults to all taxonomy codes if left unspecified
            specialty (str or list(str) or list(list(str),list(str))):
                Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty") to see all specialty options
                default(s): Defaults to all specialties if left unspecified
            specialty_category (str or list(str) or list(list(str),list(str))):
                Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty_category") to see all specialty_category options
                default(s): Defaults to all specialty categories if left unspecified
            subspecialty (str or list(str) or list(list(str),list(str))):
                Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "subspecialty") to see all subspecialty options
                default(s): Defaults to all specialty subcategories if left unspecified
            taxonomy_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple taxonomy or specialty parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified taxonomy or specialty needs to be present within the returned results, False indicates all taxonomy or specialty must be present for the returned results
                default: True
            npi (int or list(int) or list(list(int),list(int))):
                National Provider Identifier (NPI) of individual and organizational provider(s) of interest
                option(s): Any valid, registered individual or organizational National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            state (str or list(str) or list(list(str),list(str))):
                option(s): Run self.field_values.list_values(field = "state") to see all state options
                default(s): Defaults to all US States if left unspecified
            division (str or list(str) or list(list(str),list(str))):
                District residence of the query patient population. There are nine distinct US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "division") to see all division options
                default(s): Defaults to all entire US population if left unspecified
            region (str or list(str) or list(list(str),list(str))):
                Regional residence of the query patient population. There are four major US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "region") to see all region options
                default(s): Defaults to all entire US population if left unspecified
            metro (str or list(str) or list(list(str),list(str))):
                Metropolitan and micropolitan statistical areas according to the US Census Bureau
                option(s): Run self.field_values.list_values(field = "metro") to see all metro options
                default(s): Defaults to all entire US population if left unspecified
            short_zip (int or list(int) or list(list(int),list(int))):
                First three digits the zip code of the query patient population specified
                option(s): Run self.field_values.list_values(field = "short_zip") to see all short_zip options
                default(s): Defaults to all entire US population if left unspecified 
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: 10000
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: state = "NE"
                    example logic: Select data from the state of Nebraska
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: state = ["NE","CO"]
                    example logic: Select data from either Nebraska OR Colorado
            inter-parameter: Logical arguments ACROSS parameter specifications
                multi-selection AND: (default) Return data that meets both criterion
                    example: self.encounter(state = "NE", short_diag_code = ["I10"])
                    example logic: Select all hypertensive encounters in Nebraska
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if min_date == None:
            temp = date.today() - timedelta(days=30)
            min_date = temp.strftime("%Y-%m-%d")
            print(min_date)
        if max_date == None:
            temp = date.today() - timedelta(days=90)
            max_date = temp.strftime("%Y-%m-%d")
            print(max_date)
        if age_min == None:
            age_min = 0
        if age_max == None:
            age_max = 120
        if gender == None:
            gender = ["M","F"]
        if limit == None:
            limit = 10000
        elif (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"marketing_category":marketing_category,"substance":substance,"pharm_class":pharm_class, "ndc":ndc, "gender" : gender,  "taxonomy_code" : taxonomy_code, "subspecialty": subspecialty, "specialty" : specialty, "specialty_category" : specialty_category, "npi" : npi, "state" : state, "division" : division, "region" : region, "metro" : metro, "short_zip" : short_zip}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # ensure valid date data type 
        dates = {"min_date" : min_date, "max_date" : max_date}
        for x in list(dates.items()):
            if x[1] != None:
                if type(x[1]) == str:
                    cqu.checkTypeDate(dateutil.parser.parse(x[1]).date(), x[0])
                else:
                    cqu.checkTypeDate(x[1], x[0])

        # ensure valid integer data type
        ints = {"limit" : limit, "age_min" : age_min, "age_max" : age_max}
        for x in list(ints.items()):
            if (x[1] != None):
                cqu.checkTypeInt(x[1], x[0])

        # normalize NPI output
        npi = cqu.NPINorm(npi)

        # raise error for invalid NPIs
        cqu.checkNPI(npi, "npi")

        ### Input Quality Control ###

        # normalize code digit input
        revenue_center_code = cqu.codeNorm(revenue_center_code, n = 4, punct = False)
        short_zip = cqu.codeNorm(short_zip, n = 3, punct = False)
        short_diag_code = cqu.codeNorm(short_diag_code, n = 3, punct = False)
        diag_code = cqu.codeNorm(diag_code, punct = False)

        # normalize strings -- lowercase, trim whitespace)
        ndc = cqu.stringNorm(ndc)
        pharm_class = cqu.stringNorm(pharm_class)
        substance = cqu.stringNorm(substance)
        marketing_category = cqu.stringNorm(marketing_category)
        gender = cqu.stringNorm(gender)
        taxonomy_code = cqu.stringNorm(taxonomy_code)
        subspecialty = cqu.stringNorm(subspecialty)
        specialty = cqu.stringNorm(specialty)
        specialty_category = cqu.stringNorm(specialty_category)
        state = cqu.stringNorm(state)
        division = cqu.stringNorm(division)
        region = cqu.stringNorm(region)
        metro = cqu.stringNorm(metro)

        # ensure levels feature levels congeal
        cqu.checkLevels(npi, "npi", levels = 1)
        cqu.checkLevels(ndc, "ndc", levels = 1)
        cqu.checkLevels(pharm_class, "pharm_class", levels = 1)
        cqu.checkLevels(substance, "substance", levels = 1)
        cqu.checkLevels(marketing_category, "marketing_category", levels = 1)
        cqu.checkLevels(subspecialty, "subspecialty", levels = 1)
        cqu.checkLevels(taxonomy_code, "taxonomy_code", levels = 1)
        cqu.checkLevels(specialty, "specialty", levels = 1)
        cqu.checkLevels(specialty_category, "specialty_category", levels = 1)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(pharm_class, self.field_values.data, "pharm_class")
        cqu.checkFieldValues(substance, self.field_values.data, "substance")
        cqu.checkFieldValues(marketing_category, self.field_values.data, "marketing_category")
        cqu.checkFieldValues(gender, self.field_values.data, "gender")
        cqu.checkFieldValues(taxonomy_code, self.field_values.data, "taxonomy_code")
        cqu.checkFieldValues(subspecialty, self.field_values.data, "subspecialty")
        cqu.checkFieldValues(specialty, self.field_values.data, "specialty")
        cqu.checkFieldValues(specialty_category, self.field_values.data, "specialty_category")
        cqu.checkFieldValues(state, self.field_values.data, "state")
        cqu.checkFieldValues(division, self.field_values.data, "division")
        cqu.checkFieldValues(region, self.field_values.data, "region")
        cqu.checkFieldValues(metro, self.field_values.data, "metro")

        ### Input Logic & Hierarchy ###

        # taxonomy hierarchy logic
        taxonomies, taxonomy_greedy, warnings_list1 = cqu.taxonomyPriority(taxonomy_code, subspecialty, specialty, specialty_category, taxonomy_greedy, self.field_values.data)
        cqu.checkLevels(taxonomies, "taxonomies", levels = 1)

        # prescription hierarchy logic
        ndcs, script_greedy, warnings_list2 = cqu.scriptPriority(ndc, substance, pharm_class, marketing_category, script_greedy, self.field_values.data)

        # geography hierarchy priority
        states, zips, warnings_list3 = cqu.geoPriority(state, division, region, metro, short_zip, self.field_values.data)

        # collect warnings
        warnings_list = warnings_list1 + warnings_list2 + warnings_list3

        # make it pretty for Ray's SQL
        ndcs = cqu.stringNorm(cqu.listWrapString(ndcs), stringtype = "upper")
        procs = cqu.stringNorm(cqu.listWrapString(procs), stringtype = "upper")
        states = cqu.stringNorm(cqu.listWrapString(states), stringtype = "upper")
        gender = cqu.stringNorm(gender, stringtype = "upper")
        taxonomies = cqu.stringNorm(cqu.listWrapString(taxonomies), stringtype = "upper")
        npi = cqu.listWrapString(npi)
        zips = cqu.listWrapString(zips)

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "script-encounter",
                 "min_date" : min_date,
                "max_date" : max_date,
                "gender" : gender,
                "age_min" : age_min,
                "age_max" : age_max,
                "ndc" : ndcs,
                "taxonomy_code" : taxonomies,
                "npi" : npi,
                "state" : states,
                "short_zip" : zips,
                "greedy": False, # always keep false for now, implications too complicated for now
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        senc = CareQueryData(data, features = self.glossary.feature_detail("SCRIPT_TABLE"), show = show)

        return senc
    
    def scriptJourney(self,
                      min_date = None,
                      max_date = None,
                      gender = None,
                      age_min = None,
                      age_max = None,
                      ndc = None,
                      pharm_class = None,
                      substance = None,
                      marketing_category = None,
                      script_greedy = None,
                      taxonomy_code = None,
                      specialty_category = None,
                      specialty = None,
                      subspecialty = None,
                      taxonomy_greedy = None,
                      npi = None,
                      state = None,
                      division = None,
                      region = None,
                      metro = None,
                      short_zip = None,
                      limit = None,
                      show = None):
        
        """
        Description:
        
            Query patient's full prescription claims history with line item detail, by specifying ANY and ALL prescription parameters where criterion are met across the entire journey.
        
        Parameters:

            min_date (str):
                Lower threshold date within the date range of interest, observational start date
                option(s): "2023-01-01" or "01/01/2023" 
                default: 90 days prior to date of query
            max_date (str):
                Upper threshold date within the date range of interest, observational end date
                option(s): "2023-01-01" or "01/01/2023" 
                default: 30 days prior to date of query
            gender (str or list(str)):
                Patient gender within the population of interest
                option(s): 'M' for Male, 'F' for Female, or ['M','F'] for both
                default(s): ['M','F']
            age_min (int):
                Minimum patient age identified within the population of interest
                option(s): 0 to 120
                default: 0
            age_max (int):
                Maximum patient age identified within the population of interest
                option(s): 0 to 120
                default: 120
            ndc (str or list(str) or list(list(str),list(str))):
                FDA National Drug Code version 11 standardized code for a dispensed drug
                option(s): xxx
                default(s): Defaults to all National Drug Codes (NDCs) if left unspecified
            pharm_class (str or list(str) or list(list(str),list(str))):
                Classifications of a drug product based on its therapeutic action, or how it works in the body
                option(s): Run self.field_values.list_values(field = "pharm_class") to see all pharm_class options
                default(s): Defaults to all National Drug Code (NDC) pharmaceutical classes if left unspecified
            script_greedy (bool):
                Boolean indicator for 'AND' or 'OR' when multiple prescription parameters specified - helps users offer various levels of specificity without confusing and/or logic
                option(s): True indicates that ANY specified prescription needs to be present within the returned results, False indicates all prescription must be present for the returned results
                default: True
            substance (str or list(str) or list(list(str),list(str))):
                The active ingredient in a drug product
                option(s): Run self.field_values.list_values(field = "substance") to see all substance options
                default(s): Defaults to all National Drug Code Substances if left unspecified
            marketing_category (str or list(str) or list(list(str),list(str))):
                Classification of a drug product based on its regulatory status and how it is marketed
                option(s): Run self.field_values.list_values(field = "marketing_category") to see all marketing_category options
                default(s): Defaults to all National Drug Code Marketing Categories if left unspecified
            taxonomy_code (str or list(str) or list(list(str),list(str))):
                Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider
                option(s): Run self.field_values.list_values(field = "taxonomy_code") to see all taxonomy_code options
                default(s): Defaults to all taxonomy codes if left unspecified
            specialty (str or list(str) or list(list(str),list(str))):
                Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty") to see all specialty options
                default(s): Defaults to all specialties if left unspecified
            specialty_category (str or list(str) or list(list(str),list(str))):
                Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "specialty_category") to see all specialty_category options
                default(s): Defaults to all specialty categories if left unspecified
            subspecialty (str or list(str) or list(list(str),list(str))):
                Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy
                option(s): Run self.field_values.list_values(field = "subspecialty") to see all subspecialty options
                default(s): Defaults to all specialty subcategories if left unspecified
            npi (int or list(int) or list(list(int),list(int))):
                National Provider Identifier (NPI) of individual and organizational provider(s) of interest
                option(s): Any valid, registered individual or organizational National Provider Identifier in the US
                default(s): Defaults to all National Provider Identifiers (NPIs) if left unspecified
            state (str or list(str) or list(list(str),list(str))):
                option(s): Run self.field_values.list_values(field = "state") to see all state options
                default(s): Defaults to all US States if left unspecified
            division (str or list(str) or list(list(str),list(str))):
                District residence of the query patient population. There are nine distinct US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "division") to see all division options
                default(s): Defaults to all entire US population if left unspecified
            region (str or list(str) or list(list(str),list(str))):
                Regional residence of the query patient population. There are four major US State groupings as defined by the US Census Bureau
                option(s): Run self.field_values.list_values(field = "region") to see all region options
                default(s): Defaults to all entire US population if left unspecified
            metro (str or list(str) or list(list(str),list(str))):
                Metropolitan and micropolitan statistical areas according to the US Census Bureau
                option(s): Run self.field_values.list_values(field = "metro") to see all metro options
                default(s): Defaults to all entire US population if left unspecified
            short_zip (int or list(int) or list(list(int),list(int))):
                First three digits the zip code of the query patient population specified
                option(s): Run self.field_values.list_values(field = "short_zip") to see all short_zip options
                default(s): Defaults to all entire US population if left unspecified 
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: 10000
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: state = "NE"
                    example logic: Select data from the state of Nebraska
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: state = ["NE","CO"]
                    example logic: Select data from either Nebraska OR Colorado
                multi-selection AND: Select multiple values across multiple lists to request results that meet both conditions
                    example: short_diag_code = [["I10"],["E11"]]
                    example logic: Select data where patients have hypertension (I10) AND type-2 diabetes (E11)
            inter-parameter: Logical arguments ACROSS parameter specifications
                multi-selection AND: (default) Return data that meets both criterion
                    example: self.encounter(state = "NE", short_diag_code = ["I10"])
                    example logic: Select all hypertensive encounters in Nebraska
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if min_date == None:
            temp = date.today() - timedelta(days=30)
            min_date = temp.strftime("%Y-%m-%d")
            print(min_date)
        if max_date == None:
            temp = date.today() - timedelta(days=90)
            max_date = temp.strftime("%Y-%m-%d")
            print(max_date)
        if age_min == None:
            age_min = 0
        if age_max == None:
            age_max = 120
        if gender == None:
            gender = ["M","F"]
        if limit == None:
            limit = 10000
        elif (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"marketing_category":marketing_category,"substance":substance,"pharm_class":pharm_class, "ndc":ndc, "gender" : gender,  "taxonomy_code" : taxonomy_code, "subspecialty": subspecialty, "specialty" : specialty, "specialty_category" : specialty_category, "npi" : npi, "state" : state, "division" : division, "region" : region, "metro" : metro, "short_zip" : short_zip}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # ensure valid date data type 
        dates = {"min_date" : min_date, "max_date" : max_date}
        for x in list(dates.items()):
            if x[1] != None:
                if type(x[1]) == str:
                    cqu.checkTypeDate(dateutil.parser.parse(x[1]).date(), x[0])
                else:
                    cqu.checkTypeDate(x[1], x[0])

        # ensure valid integer data type
        ints = {"limit" : limit, "age_min" : age_min, "age_max" : age_max}
        for x in list(ints.items()):
            if (x[1] != None):
                cqu.checkTypeInt(x[1], x[0])

        # normalize NPI output
        npi = cqu.NPINorm(npi)

        # raise error for invalid NPIs
        cqu.checkNPI(npi, "npi")

        ### Input Quality Control ###

        # normalize code digit input
        revenue_center_code = cqu.codeNorm(revenue_center_code, n = 4, punct = False)
        short_zip = cqu.codeNorm(short_zip, n = 3, punct = False)
        short_diag_code = cqu.codeNorm(short_diag_code, n = 3, punct = False)
        diag_code = cqu.codeNorm(diag_code, punct = False)

        # normalize strings -- lowercase, trim whitespace)
        ndc = cqu.stringNorm(ndc)
        pharm_class = cqu.stringNorm(pharm_class)
        substance = cqu.stringNorm(substance)
        marketing_category = cqu.stringNorm(marketing_category)
        gender = cqu.stringNorm(gender)
        taxonomy_code = cqu.stringNorm(taxonomy_code)
        subspecialty = cqu.stringNorm(subspecialty)
        specialty = cqu.stringNorm(specialty)
        specialty_category = cqu.stringNorm(specialty_category)
        state = cqu.stringNorm(state)
        division = cqu.stringNorm(division)
        region = cqu.stringNorm(region)
        metro = cqu.stringNorm(metro)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(pharm_class, self.field_values.data, "pharm_class")
        cqu.checkFieldValues(substance, self.field_values.data, "substance")
        cqu.checkFieldValues(marketing_category, self.field_values.data, "marketing_category")
        cqu.checkFieldValues(gender, self.field_values.data, "gender")
        cqu.checkFieldValues(taxonomy_code, self.field_values.data, "taxonomy_code")
        cqu.checkFieldValues(subspecialty, self.field_values.data, "subspecialty")
        cqu.checkFieldValues(specialty, self.field_values.data, "specialty")
        cqu.checkFieldValues(specialty_category, self.field_values.data, "specialty_category")
        cqu.checkFieldValues(state, self.field_values.data, "state")
        cqu.checkFieldValues(division, self.field_values.data, "division")
        cqu.checkFieldValues(region, self.field_values.data, "region")
        cqu.checkFieldValues(metro, self.field_values.data, "metro")

        ### Input Logic & Hierarchy ###

        # taxonomy hierarchy logic
        taxonomies, taxonomy_greedy, warnings_list1 = cqu.taxonomyPriority(taxonomy_code, subspecialty, specialty, specialty_category, taxonomy_greedy, self.field_values.data)

        # prescription hierarchy logic
        ndcs, script_greedy, warnings_list2 = cqu.scriptPriority(ndc, substance, pharm_class, marketing_category, script_greedy, self.field_values.data)

        # geography hierarchy priority
        states, zips, warnings_list3 = cqu.geoPriority(state, division, region, metro, short_zip, self.field_values.data)

        # collect warnings
        warnings_list = warnings_list1 + warnings_list2 + warnings_list3

        # make it pretty for Ray's SQL
        ndcs = cqu.stringNorm(cqu.listWrapString(ndcs), stringtype = "upper")
        procs = cqu.stringNorm(cqu.listWrapString(procs), stringtype = "upper")
        states = cqu.stringNorm(cqu.listWrapString(states), stringtype = "upper")
        gender = cqu.stringNorm(gender, stringtype = "upper")
        taxonomies = cqu.stringNorm(cqu.listWrapString(taxonomies), stringtype = "upper")
        npi = cqu.listWrapString(npi)
        zips = cqu.listWrapString(zips)

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "script-journey",
                 "min_date" : min_date,
                "max_date" : max_date,
                "gender" : gender,
                "age_min" : age_min,
                "age_max" : age_max,
                "ndc" : ndcs,
                "taxonomy_code" : taxonomies,
                "npi" : npi,
                "state" : states,
                "short_zip" : zips,
                "greedy": False, # always keep false for now, implications too complicated for now
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        sjou = CareQueryData(data, features = self.glossary.feature_detail("SCRIPT_TABLE"), show = show)

        return sjou

    def scriptDetail(self,
                     ndc = None,
                     pharm_class = None,
                     substance = None,
                     marketing_category = None,
                     limit = None,
                     show = None):
        
        """
        Description:
        
            Query prescription details such as active ingredient, company labeler, and categorical details for all FDA National Drug Codes (NDCs)
        
        Parameters:

            ndc (str or list(str) or list(list(str),list(str))):
                FDA National Drug Code version 11 standardized code for a dispensed drug
                option(s): xxx
                default(s): Defaults to all National Drug Codes (NDCs) if left unspecified
            pharm_class (str or list(str) or list(list(str),list(str))):
                Classifications of a drug product based on its therapeutic action, or how it works in the body
                option(s): Run self.field_values.list_values(field = "pharm_class") to see all pharm_class options
                default(s): Defaults to all National Drug Code (NDC) pharmaceutical classes if left unspecified
            substance (str or list(str) or list(list(str),list(str))):
                The active ingredient in a drug product
                option(s): Run self.field_values.list_values(field = "substance") to see all substance options
                default(s): Defaults to all National Drug Code Substances if left unspecified
            marketing_category (str or list(str) or list(list(str),list(str))):
                Classification of a drug product based on its regulatory status and how it is marketed
                option(s): Run self.field_values.list_values(field = "marketing_category") to see all marketing_category options
                default(s): Defaults to all National Drug Code Marketing Categories if left unspecified
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: 10000
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: state = "NE"
                    example logic: Select data from the state of Nebraska
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: state = ["NE","CO"]
                    example logic: Select data from either Nebraska OR Colorado
            inter-parameter: Logical arguments ACROSS parameter specifications
                multi-selection AND: (default) Return data that meets both criterion
                    example: self.encounter(state = "NE", short_diag_code = ["I10"])
                    example logic: Select all hypertensive encounters in Nebraska
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"marketing_category":marketing_category,"substance":substance,"pharm_class":pharm_class, "ndc":ndc}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # ensure valid integer data type
        ints = {"limit" : limit}
        for x in list(ints.items()):
            if (x[1] != None):
                cqu.checkTypeInt(x[1], x[0])

        ### Input Quality Control ###

        # normalize code digit input
        ndc = cqu.codeNorm(ndc, n = 11, punct = False)

        # normalize strings -- lowercase, trim whitespace)
        ndc = cqu.stringNorm(ndc)
        pharm_class = cqu.stringNorm(pharm_class)
        substance = cqu.stringNorm(substance)
        marketing_category = cqu.stringNorm(marketing_category)

        # ensure levels feature levels congeal
        cqu.checkLevels(ndc, "ndc", levels = 1)
        cqu.checkLevels(pharm_class, "pharm_class", levels = 1)
        cqu.checkLevels(substance, "substance", levels = 1)
        cqu.checkLevels(marketing_category, "marketing_category", levels = 1)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(pharm_class, self.field_values.data, "pharm_class")
        cqu.checkFieldValues(substance, self.field_values.data, "substance")
        cqu.checkFieldValues(marketing_category, self.field_values.data, "marketing_category")

        ### Input Logic & Hierarchy ###

        # prescription hierarchy logic
        script_greedy = True
        ndcs, script_greedy, warnings_list = cqu.scriptPriority(ndc, substance, pharm_class, marketing_category, script_greedy, self.field_values.data)

        # make it pretty for Ray's SQL
        ndcs = cqu.stringNorm(cqu.listWrapString(ndcs), stringtype = "upper")

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "script-detail",
                "ndc" : ndcs,
                "greedy": False, # always keep false for now, implications too complicated for now
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        sdet = CareQueryData(data, features = self.glossary.feature_detail("SCRIPT_DETAIL_TABLE"), show = show)

        return sdet
    
    def drgDetail(self,
                  drg_code = None,
                  drg_category = None,
                  limit = None,
                  show = None):
        
        """
        Description:
        
            Query Diagnosis Related Group (DRG) details, context and categories.

        Parameters:
            
            drg_code (str or list(str) or list(list(str),list(str))):
                Diagnosis related group (DRG) is how insurance payors categorize hospitalization costs to determine payment requirement. DRG is based on your primary and secondary diagnoses, other conditions (comorbidities), age, sex, and necessary medical procedures. 
                option(s): Run self.field_values.list_values(field = "drg_code") to see all drg options
                default(s): Defaults to all drg codes if left unspecified
            drg_category (str or list(str) or list(list(str),list(str))):
                Diagnosis related group (DRG) medical diagnosis categories help reduce request dimensionality
                option(s): Run self.field_values.list_values(field = "drg_category") to see all drg category options
                default(s): Defaults to any/all drg categories if left unspecified
            limit (int):
                Number of rows returned in the data request
                option(s): Select a specific number of rows for the API to return, or None to return all corresponding rows
                default: None
            show (bool):
                Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself.
                option(s): True indicates print, False indicates do not print
                default: True

        Logic:
            intra-parameter: Logical arguments WITHIN parameter specifications
                basic selection: Select a single value to request that value
                    example: state = "NE"
                    example logic: Select data from the state of Nebraska
                multi-selection OR: Select multiple values within a list to request any results that meet either condition
                    example: state = ["NE","CO"]
                    example logic: Select data from either Nebraska OR Colorado
        
        Raises:
            ValueError: if result cannot be recognized
            TypeError: if result data type cannot be recognized
            VolumeWarning: if result high data volume anticipated
        
        Returns:
            json: JSON query instructions to CareQuery API endpoint 

        """

        ### Basic Parameter Defaults ###

        if (limit == False) | (limit == True):
            limit = None
        if show == None:
            show = True

        ### Input Data Type Control ###

        # ensure valid mixed data type 
        mixed = {"drg_category":drg_category, "drg_code":drg_code}       
        for x in list(mixed.items()):
            if x[1] != None:
                cqu.checkTypeMixed(x[1], x[0])

        # ensure valid integer data type
        ints = {"limit" : limit}
        for x in list(ints.items()):
            if (x[1] != None):
                cqu.checkTypeInt(x[1], x[0])

        ### Input Quality Control ###

        # normalize code digit input
        drg_code = cqu.codeNorm(drg_code, n = 3, punct = False)

        # normalize strings -- lowercase, trim whitespace)
        drg_category = cqu.stringNorm(drg_category)

        # ensure levels feature levels congeal
        cqu.checkLevels(drg_category, "drg_category", levels = 1)
        cqu.checkLevels(drg_code, "drg_code", levels = 1)

        # check to see if inputs are within corresponding field value space
        cqu.checkFieldValues(drg_code, self.field_values.data, "drg_code")
        cqu.checkFieldValues(drg_category, self.field_values.data, "drg_category")

        ### Input Logic & Hierarchy ###

        # drg hierarchy logic
        drg_greedy = True
        drgs, drg_greedy, warnings_list  = cqu.drgPriority(drg_code, drg_category, drg_greedy, self.field_values.data)

        ### Construct Final JSON ###

        if len(warnings_list) > 0:
            warnings_list
        else:
            warnings_list = None

        #Define the API request data elements.
        data = {"query": "drg-detail",
                "drg_code" : drgs,
                "limit" : limit,
                "warnings": warnings_list,
                "email": self.user.email,
                "token": self.user.token,
                "mode" : None,
                "timestamp" : None}
        
        # create care query data object
        drgd = CareQueryData(data, features = self.glossary.feature_detail("DRG_TABLE"), show = show)

        return drgd
    
if __name__ == '__main__':

    ### Query Instantiation, Creation and Execution ###

    # Instantiate and Connect to CareQuery API
    cq = CareQuery(token = "a7a5c93c004b44741eab907007955d6f")

    # Constrtruct Encounter Query
    enc_query = cq.careEncounter(proc_code = ["99212", "99281", "99214", "99204","59400", "59409", "59410","59510"],
                                npi = 1932213600,
                                state = ["IL","GA"],
                                min_date = "2023-01-01",
                                max_date = "2023-03-01")

    crossers_query = cq.careJourney(proc_code=["99212", "99281", "99214", "99204", "59400", "59409", "59410", "59510"],
                                    proc_subcategory=['medicine - cardiovascular', 'surgery - cardiovascular system'],
                                    short_zip=["606"],
                                    npi=[["1497859649"], ["1932213600"]],
                                    # these are hco_npis (multi-list is implied AND)
                                    min_date="2022-01-01",
                                    max_date="2023-06-01",
                                    limit=100000)

    # execute query
    # crossers_data = crossers_query.execute()
    enc_data = enc_query.execute()
    
    # enc_data = enc_query.execute()

    print(enc_data.head())

    # explore field values object
    # print("-----")
    # print("fields")
    # print(cq.field_values.list_fields(contains = "diag"))
    # print("-----")
    # print("values")
    # print(cq.field_values.list_values(field = "region", contains = "MID"))
    #
    # # explore table values
    # print("---")
    # print("list tables:")
    # print(cq.glossary.list_tables())
    # print("---")
    # print("list methods:")
    # print(cq.glossary.list_methods())

    


    

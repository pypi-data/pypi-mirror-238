# COPYRIGHT 2022 MONOOCLE INSIGHTS
# ALL RIGHTS RESERVED
# UNAUTHORIZED USE, REPRODUCTION, OR
# DISTRIBUTION STRICTLY PROHIBITED
#
# AUTHOR: Sean O'Malley and Raymond Deiotte
# CREATION DATE: 20230821
# LAST UPDATED: 20230821

### Import Dependencies ###

import re
# basic
from datetime import date, datetime


### Data Type Helpers ###

def checkTypeMixed(x, x_name):
    if type(x) not in [int, str, list]:
        raise TypeError(f"TypeError: Datatype for '{x_name}' must be a string, int or list")
    
def checkTypeBool(x, x_name):
    if type(x) not in [bool]:
        raise TypeError(f"TypeError: Datatype for '{x_name}' must be a boolean")
    
def checkTypeInt(x, x_name):
    if type(x) not in [int]:
        raise TypeError(f"TypeError: Datatype for '{x_name}' must be a integer")
    
def checkTypeDate(x, x_name):
    if type(x) not in [date, datetime.date, datetime]:
        raise TypeError(f"TypeError: Datatype for '{x_name}' must be a date string or date object")

### Data Validation Helpers ###   

def checkNPI(param, name):
    """
    Error if NPI dimensions are invalid
    """
    if type(param) == str: # int to str
        if len(param) != 10:
            raise ValueError(f"ValueError: Invalid '{name}' length detected, must equal 10 digits and '{param}' is {len(param)}")
    elif type(param) == list: 
        if any(isinstance(el, list) for el in param): # if list of list
            naughty = list(set([item for sublist in param for item in sublist if len(item) != 10]))
            if len(naughty) > 0:
                raise ValueError(f"ValueError: Invalid '{name}' length detected, must equal 10 digits and {naughty} do not meet this criterion")
        else: # if 1d list
            naughty = list(set([x for x in param if len(x) != 10]))
            if len(naughty) > 0:
                raise ValueError(f"ValueError: Invalid '{name}' length detected, must equal 10 digits and {naughty} do not meet this criterion")

def checkDRGOverlap(drg_code, diags, procs):
    """
    Warning if DRG and procedures and/or diagnoses are present
    """
    if (drg_code != None) & (diags != None) & (procs != None):
        warnings_list = ["ValueWarning: DRG, diagnoses and procedures specified *** Diagnostic Related Groupings (DRGs) are derived from of procedure and diagnosis codes, query will return all fields relating to DRG 'OR' diagnosis and procedures."]
    elif (drg_code != None) & (procs != None):
        warnings_list = ["ValueWarning: DRG procedures specified *** Diagnostic Related Groupings (DRGs) are derived from of procedure and diagnosis codes, query will return all fields relating to DRG 'OR' procedures."]
    elif (drg_code != None) & (procs != None):
        warnings_list = ["ValueWarning: DRG and diagnoses specified *** Diagnostic Related Groupings (DRGs) are derived from of procedure and diagnosis codes, query will return all fields relating to DRG 'OR' diagnosis."]
    else:
        warnings_list = []

    return warnings_list

def checkNPIOverlap(taxonomies, ref_npi, npi):
    """
    Warning if NPI fields and taxonomies are present
    """
    if (taxonomies != None) & (ref_npi != None) & (npi != None):
        warnings_list = ["ValueWarning: Provider Specialty/Taxonomy, Referring NPI and Primary NPI Specified *** query will return all values that meet ALL criterion. For EITHER/OR criterion, set greedy = True"]
    elif (taxonomies != None) & (ref_npi != None):
        warnings_list = ["ValueWarning: Provider Specialty/Taxonomy and Referring NPI *** query will return all values that meet BOTH criterion. For EITHER/OR criterion, set greedy = True"]
    elif (taxonomies != None) & (npi != None):
        warnings_list = ["ValueWarning: Provider Specialty/Taxonomy and NPI *** query will return all values that meet BOTH criterion. For EITHER/OR criterion, set greedy = True"]
    else:
        warnings_list = []

    if (ref_npi != None) & (npi != None):
        warnings_list.append("ValueWarning: Referring NPI and Primary NPI Specified *** query will return all values that meet BOTH criterion. For EITHER/OR criterion, set greedy = True")
    
    return warnings_list

def checkLevels(param, name, levels = None):
    """
    Warning if list dimensionality is off
    """
    if (param != None) & (levels != None):
        if type(param) == list:
            if (any(isinstance(el, list) for el in param)) & (levels == 1): # if list of list
                raise ValueError(f"ValueError: List of lists implies an 'and' statement and is not allowed for '{name}' in this type of query")
            elif (any(isinstance(el, list) for el in param)) & (levels > 2):
                raise ValueError(f"ValueError: List of lists implies an 'and' statement and is not allowed beyond two lists for '{name}' in this type of query")

def checkFieldValues(param, field_values, name):
    """
    Check if param is a valid field value
    """
    if param != None:

        try:
            values = list(field_values[name].keys()) # nested dicts
        except:
            values = list(field_values[name]) # basic lists

        if (type(param) == str) & (param not in values):
            raise ValueError(f"ValueError: '{param}' is not a valid '{name}' value, please reference self.field_values.list_values(field = '{name}') for full list of options")
        elif type(param) == list:
            if any(isinstance(el, list) for el in param): # if list of list
                naughty = list(set([item for sublist in param for item in sublist if item not in values]))
                if len(naughty) > 0:
                    raise ValueError(f"ValueError: {param} are not a valid '{name}' value(s), please reference self.field_values.list_values(field = '{name}') for full list of options")
            else: # if 1d list
                naughty = list(set([x for x in param if x not in values]))
                if len(naughty) > 0:
                    raise ValueError(f"ValueError: {param} are not a valid '{name}' value(s), please reference self.field_values.list_values(field = '{name}') for full list of options")

def checkDRGConflate(drg_code, proc_code, proc_subcategory, proc_category, diag_code, diag_subcategory, diag_category, short_diag_code):
            
            if (drg_code != None) & ((proc_code != None) | (proc_subcategory != None) | (proc_category != None)):
                raise ValueError("DRG Conflation Error: DRGs cannot be specified alongside any procedure parameters because DRGs use procedures within thier computation, conflating query the output.")
            if (drg_code != None) & ((diag_code != None) | (diag_subcategory != None) | (diag_category != None) | (short_diag_code != None)):
                raise ValueError("DRG Conflation Error: DRGs cannot be specified alongside any diagnosis parameters because DRGs use diagnoses within thier computation, conflating query the output.")

### Normalization Helpers ### 

# wrap strings in list if needed
def listWrapString(x):
    if type(x) == str:
        x = [x]
    return x

# helper string type class
def stringNorm(param, stringtype = None):
    """
    Normalize string to case, whether alone, in list or list of lists
    """
    if (stringtype == None) | (stringtype == "lower"):
        if (type(param) == int) | (type(param) == str):
            param = str(param).lower().strip()
        elif type(param) == list:
            if any(isinstance(el, list) for el in param): # if list of list
                param = [[str(x).lower().strip() for x in y] if type(y) == list else [str(y).lower().strip()] for y in param]
            else: # 1d list
                param = [str(x).lower().strip() for x in param]
    elif stringtype == "upper":
        if (type(param) == int) | (type(param) == str):
            param = str(param).upper().strip()
        elif type(param) == list:
            if any(isinstance(el, list) for el in param): # if list of list
                param = [[str(x).upper().strip() for x in y] if type(y) == list else [str(y).upper().strip()] for y in param]
            else: # 1d list
                param = [str(x).upper().strip() for x in param]
    elif stringtype == "title":
        if (type(param) == int) | (type(param) == str):
            param = str(param).title().strip()
        elif type(param) == list:
            if any(isinstance(el, list) for el in param): # if list of list
                param = [[str(x).title().strip() for x in y] if type(y) == list else [str(y).title().strip()] for y in param]
            else: # 1d list
                param = [str(x).title().strip() for x in param]

    return param

# helper string code norm
def codeNorm(code, n = None, punct = None):
    """
    Normalize code to final format
    """
    # remove punctuation
    if (code != None) & (punct == False):
        if (type(code) == int) | (type(code) == str):
            code = str(re.sub('[^A-Za-z0-9]+', '', code))
        elif type(code) == list:
            if any(isinstance(el, list) for el in code): # if list of list
                code = [[re.sub('[^A-Za-z0-9]+', '', str(x)) for x in y] if type(y) == list else [re.sub('[^A-Za-z0-9]+', '', str(y))] for y in code]
            else: # if 1d list
                code = [re.sub('[^A-Za-z0-9]+', '', str(x)) for x in code]
    
    # remove punctuation
    if (code != None) & (n != None):
        if type(code) == int:
            code = str(code)
        if (type(code) == str) & (len(code) < n): # add when less
            code = code.rjust(n, '0')
        if (type(code) == str) & (len(code) > n): # cut when more
            code = code[:n]
        elif type(code) == list:
            if any(isinstance(el, list) for el in code): # if list of list
                code = [[str(x).rjust(n,'0')[:n] for x in y] if type(y) == list else [str(y).rjust(n,'0')[:n]] for y in code]
            else: # if 1d list
                code = [str(x).rjust(n,'0')[:n] for x in code]

    return code

# helper quality and npi normalization function
def NPINorm(param):
    """
    Normalize NPI values
    """
    # normalize input
    if type(param) == int: # int to str
        param = str(param).replace(".0","").strip()
    elif type(param) == list: # if a list
        if any(isinstance(el, list) for el in param): # if list of list
            param = [[str(x).replace(".0","").strip() for x in y] if type(y) == list else [str(y).replace(".0","").strip()] for y in param]
        else: # if 1d list
            param = [str(x).replace(".0","").strip() for x in param]
            
    return param

### Logical Prioritization ###

def placeOfServicePriority(place_of_service, field_values):
    """
    Extract underlying values from place of service
    """
    if place_of_service != None:
        # extract, convert to list
        if (type(place_of_service) == str) | (type(place_of_service) == int):
            place_of_service = [str(place_of_service)]
        
        # convert names to codes in lists
        if (type(place_of_service) == list) & (len(place_of_service) > 0):
            if (any(isinstance(el, list) for el in place_of_service)):
                pos = [[field_values["place_of_service"][x] for x in y] for y in place_of_service] # list of list logic 
            else:
                pos = [field_values["place_of_service"][x] for x in place_of_service] # list logic

    else:
        pos = None

    return pos

def diagnosisPriority(diag_code, short_diag_code, diag_subcategory, diag_category, diag_greedy, field_values):
    """
    Surface underlying short diagnosis codes for text and string according to diagnosis greedy policy
    """
    # control for all nones
    if (diag_code == None) & (short_diag_code == None) & (diag_subcategory == None) & (diag_category == None):
        diags = None
        warnings_list = []
    else:
        # determine if we need to be greedy at any point within diagnoses
        if (diag_code != None):
            next
            if (any(isinstance(el, list) for el in diag_code)):
                diag_greedy = False
        if (short_diag_code != None):
            next
            if (any(isinstance(el, list) for el in short_diag_code)):
                diag_greedy = False
        if (diag_subcategory != None):
            next
            if (any(isinstance(el, list) for el in diag_subcategory)):
                diag_greedy = False
        if (diag_category != None):
            next
            if (any(isinstance(el, list) for el in diag_category)):
                diag_greedy = False
        
        # set default greediness
        if diag_greedy != False:
            diag_greedy = True

        # proper warnings
        if diag_greedy == False:
            warnings_item2 = "Non-Greedy Diagnosis Priority *** this query will use 'AND' logic for diagnostic list selections, all diagnoses within sub-lists MUST be present in order to be returned."
        else:
            warnings_item2 = "Greedy Diagnosis Priority *** this query will use 'OR' logic for diagnostic selections, meaning that query will return all results where ANY diagnosis is present."

        # multiple category warning
        if len([x for x in [diag_code, short_diag_code, diag_subcategory, diag_category] if x != None]) > 1:
            warnings_item1 = f"Multiple Diagnosis Options Selected: {warnings_item2}"
            warnings_list = [warnings_item1]
        else:
            warnings_list = []

        # instantiate diags
        diags = []

        if diag_code != None:
            # if string or int, make list
            if (type(diag_code) == str) | (type(diag_code) == int):
                diag_code = [str(diag_code)]
            # if not greedy and not nested, make it so
            if (diag_greedy == False) &  (any(isinstance(el, list) for el in diag_code) == False):
                diag_code = [diag_code]
            # if list and no length, make diags
            if (type(diag_code) == list) & (len(diag_code) != 0):
                diags.extend(diag_code)

        if short_diag_code != None:
            # if string or int, make list
            if (type(short_diag_code) == str) | (type(short_diag_code) == int):
                short_diag_code = [str(short_diag_code)]
            # if not greedy and not nested, make it so
            if (diag_greedy == False) &  (any(isinstance(el, list) for el in short_diag_code) == False):
                short_diag_code = [short_diag_code]
            # if list and no length, make diags
            if (type(short_diag_code) == list) & (len(short_diag_code) != 0):
                diags.extend(short_diag_code)

        if diag_subcategory != None:

            # string or int, make list
            if (type(diag_subcategory) == str) | (type(diag_subcategory) == int):
                diag_subcategory = [str(diag_subcategory)]
            # if not greedy and not nested, make it so
            if (diag_greedy == False) &  (any(isinstance(el, list) for el in diag_subcategory) == False):
                diag_subcategory = [diag_subcategory]
            # list and no length, make diags the list specified
            if (type(diag_subcategory) == list) & (len(diags) == 0):
                diags = [x[1] for x in field_values["diag_subcategory"].items() if x[0] in diag_subcategory]
                if diag_greedy == True:
                    try:
                        diags = [item for sublist in diags for item in sublist] # unnest
                    except:
                        next

            # nested list (default non-greedy), bring up underlying codes & append list
            elif any(isinstance(el, list) for el in diag_subcategory): 
                temp2 = []
                for i in range(0,len(diag_subcategory)):
                    temp = [x[1] for x in field_values["diag_subcategory"].items() if x[0] in diag_subcategory[i]]
                    temp2.extend(temp)
                diags.extend(temp2)

            # non-greedy list, , bring up underlying codes & extend list wrapped values
            elif (type(diag_subcategory) == list) & (diag_greedy == False):
                temp = [x[1] for x in field_values["diag_subcategory"].items() if x[0] in diag_subcategory]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                diags.extend([temp])
                
            # greedy list, bring up underlying codes & extend values
            elif (type(diag_subcategory) == list) & (diag_greedy == True):
                temp = [x[1] for x in field_values["diag_subcategory"].items() if x[0] in diag_subcategory]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                diags.extend(temp)

        if diag_category != None:

            # string or int, make list
            if (type(diag_category) == str) | (type(diag_category) == int):
                diag_category = [str(diag_category)]
            # if not greedy and not nested, make it so
            if (diag_greedy == False) &  (any(isinstance(el, list) for el in diag_category) == False):
                diag_category = [diag_category]
            # list and no length, make diags the list specified
            if (type(diag_category) == list) & (len(diags) == 0):
                diags = [x[1] for x in field_values["diag_category"].items() if x[0] in diag_category]
                if diag_greedy == True:
                    try:
                        diags = [item for sublist in diags for item in sublist] # unnest
                    except:
                        next

            # nested list (default non-greedy), bring up underlying codes & append list
            elif any(isinstance(el, list) for el in diag_category): 
                temp2 = []
                for i in range(0,len(diag_category)):
                    temp = [x[1] for x in field_values["diag_category"].items() if x[0] in diag_category[i]]
                    temp2.extend(temp)
                diags.extend(temp2)

            # non-greedy list, , bring up underlying codes & extend list wrapped values
            elif (type(diag_category) == list) & (diag_greedy == False):
                temp = [x[1] for x in field_values["diag_category"].items() if x[0] in diag_category]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                diags.extend([temp])
                
            # greedy list, bring up underlying codes & extend values
            elif (type(diag_category) == list) & (diag_greedy == True):
                temp = [x[1] for x in field_values["diag_category"].items() if x[0] in diag_category]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                diags.extend(temp)

        # drop any empty lists
        diags = [x for x in diags if len(x) > 0]

        # ensure none if empty
        if len(diags) == 0:
            diags = None

        # wrap any loose items if list of lists
        if any(isinstance(el, list) for el in diags):
            diags = [[x] if type(x) != list else x for x in diags]

    return diags, diag_greedy, warnings_list

def procedurePriority(proc_code, proc_subcategory, proc_category, proc_greedy, field_values):
    """
    Surface underlying procedure codes for text and string according to procedure greedy policy
    """
    # control for all nones
    if (proc_code == None) & (proc_subcategory == None) & (proc_category == None):
        procs = None
        warnings_list = []
    else:
        # determine if we need to be greedy at any point within procedure
        if (proc_code != None):
            next
            if (any(isinstance(el, list) for el in proc_code)):
                proc_greedy = False
        if (proc_subcategory != None):
            next
            if (any(isinstance(el, list) for el in proc_subcategory)):
                proc_greedy = False
        if (proc_category != None):
            next
            if (any(isinstance(el, list) for el in proc_category)):
                proc_greedy = False
        
        # set default greediness
        if proc_greedy != False:
            proc_greedy = True

        # proper warnings
        if proc_greedy == False:
            warnings_item2 = "Non-Greedy Procedure Priority *** this query will use 'AND' logic for procedural list selections, all procedures within sub-lists MUST be present in order to be returned."
        else:
            warnings_item2 = "Greedy Procedure Priority *** this query will use 'OR' logic for procedural selections, meaning that query will return all results where ANY procedure is present."

        # multiple category warning
        if len([x for x in [proc_code, proc_subcategory, proc_category] if x != None]) > 1:
            warnings_item1 = f"Multiple Procedure Options Selected: {warnings_item2}"
            warnings_list = [warnings_item1]
        else:
            warnings_list = []

        # instantiate procs
        procs = []

        if proc_code != None:
            # make any string or int, make list
            if (type(proc_code) == str) | (type(proc_code) == int):
                proc_code = [str(proc_code)]
            # if not greedy and not nested, make it so
            if (proc_greedy == False) & (any(isinstance(el, list) for el in proc_code) == False):
                proc_code = [proc_code]
            # if list and no length, make procs
            if (type(proc_code) == list) & (len(proc_code) > 0) & (proc_greedy == True):
                procs.extend(proc_code)
            # non-greedy nested list, normal append
            elif (proc_greedy == False) & (any(isinstance(el, list) for el in proc_code)):
                procs.extend(proc_code)
            
        if proc_subcategory != None:

            # make any string or int a list
            if (type(proc_subcategory) == str) | (type(proc_subcategory) == int):
                proc_subcategory = [str(proc_subcategory)]
            # if not greedy and not nested, make it so
            if (proc_greedy == False) &  (any(isinstance(el, list) for el in proc_subcategory) == False):
                proc_subcategory = [proc_subcategory]
            # if nested list, underlying code matching doesn't matter bc values are exclusive from one another
            if (len(procs) == 0) | (any(isinstance(el, list) for el in proc_subcategory)):
                procs.extend(proc_subcategory)
            # if greedy list (most common), remove overlapping codes
            elif (type(proc_subcategory) == list):
                try:
                    underlying_procs = [x[1] for x in field_values["proc_subcategory"].items() if x[0] in proc_subcategory] # identify any codes overlapping categories from procs
                    underlying_procs = [item for sublist in underlying_procs for item in sublist] # flatten
                    procs = [x for x in procs if x not in underlying_procs] # remove overlapping procs
                except:
                    next
                procs.extend(proc_subcategory)
             
        if proc_category != None:

            # make any string or int a list
            if (type(proc_category) == str) | (type(proc_category) == int):
                proc_category = [str(proc_category)]
            # if not greedy and not nested, make it so
            if (proc_greedy == False) &  (any(isinstance(el, list) for el in proc_category) == False):
                proc_category = [proc_category]
            # if nested list or not greedy, underlying code matching doesn't matter bc values are exclusive from one another
            if (len(procs) == 0) | (any(isinstance(el, list) for el in proc_category)):
                if (any(isinstance(el, list) for el in proc_category)):
                    # nested list 
                    temp = []
                    for cat in proc_category: 
                        temp0 = [x for x in list(field_values["proc_subcategory"].keys()) if x.split(" - ")[0] in cat] # isolate subcategory list of categories for common vocab
                        temp.extend(temp0)
                    procs.append(temp)
                else:
                    # new list
                    procs = [x for x in list(field_values["proc_subcategory"].keys()) if x.split(" - ")[0] in proc_category] # isolate subcategory list of categories for common vocab

            # greedy list (most common), remove overlapping codes
            elif (type(proc_category) == list):
                temp0 = [x for x in list(field_values["proc_subcategory"].keys()) if x.split(" - ")[0] in proc_category] # isolate subcategory list of categories for common vocab
                temp0 = [x for x in temp0 if x not in procs] # remove any overlapping subcategories
                try:
                    underlying_procs = [x[1] for x in field_values["proc_subcategory"].items() if x[0] in temp0] # identify any codes overlapping categories from procs
                    underlying_procs = [item for sublist in underlying_procs for item in sublist] # flatten
                    procs = [x for x in procs if x not in underlying_procs] # remove overlapping procs
                except:
                    next
                procs.extend(temp0)

        # drop any empty lists
        procs = [x for x in procs if len(x) > 0]

        if len(procs) == 0:
            procs = None

        # wrap any loose items if list of lists
        if any(isinstance(el, list) for el in procs):
            procs = [[x] if type(x) != list else x for x in procs]

    return procs, proc_greedy, warnings_list

def taxonomyPriority(taxonomy_code, subspecialty, specialty, specialty_category, taxonomy_greedy, field_values):
    """
    Surface underlying taxonomy codes for text and string according to specialty/taxonomy greedy policy
    """
    # control for all nones
    if (taxonomy_code == None) & (subspecialty == None) & (specialty == None) & (specialty_category == None):
        taxonomies = None
        warnings_list = []
    else:    
        # determine if we need to be greedy at any point within taxonomyedure
        if (taxonomy_code != None):
            next
            if (any(isinstance(el, list) for el in taxonomy_code)):
                taxonomy_greedy = False
        if (subspecialty != None):
            next
            if (any(isinstance(el, list) for el in subspecialty)):
                taxonomy_greedy = False
        if (specialty != None):
            next
            if (any(isinstance(el, list) for el in specialty)):
                taxonomy_greedy = False
        if (specialty_category != None):
            next
            if (any(isinstance(el, list) for el in specialty_category)):
                taxonomy_greedy = False
        
        # set default greediness
        if taxonomy_greedy != False:
            taxonomy_greedy = True

        # proper warning
        if taxonomy_greedy == False:
            warnings_item2 = "Non-Greedy Taxonomy Priority *** this query will use 'AND' logic for taxonomy list selections, all taxonomies within sub-lists MUST be present in order to be returned."
        else:
            warnings_item2 = "Greedy Taxonomy Priority *** this query will use 'OR' logic for taxonomy selections, meaning that query will return all results where ANY taxonomy is present."

        # multiple category warning
        if len([x for x in [taxonomy_code, subspecialty, specialty, specialty_category] if x != None]) > 1:
            warnings_item1 = f"Multiple Specialty/Taxonmoy Options Selected: {warnings_item2}"
            warnings_list = [warnings_item1]
        else:
            warnings_list = []

        # instantiate taxonomies
        taxonomies = []

        if taxonomy_code != None:
            # if string or int, make list
            if (type(taxonomy_code) == str) | (type(taxonomy_code) == int):
                taxonomy_code = [str(taxonomy_code)]
            # if not greedy and not nested, make it so
            if (taxonomy_greedy == False) &  (any(isinstance(el, list) for el in taxonomy_code) == False):
                taxonomy_code = [taxonomy_code]
            # if list and no length, make taxonomies
            if (type(taxonomy_code) == list) & (len(taxonomy_code) > 0):
                taxonomies.extend(taxonomy_code)

        if subspecialty != None:

            # string or int, make list
            if (type(subspecialty) == str) | (type(subspecialty) == int):
                subspecialty = [str(subspecialty)]
            # if not greedy and not nested, make it so
            if (taxonomy_greedy == False) &  (any(isinstance(el, list) for el in subspecialty) == False):
                subspecialty = [subspecialty]

            # list and no length, make taxonomies the list specified
            if (type(subspecialty) == list) & (len(taxonomies) == 0):
                taxonomies = [x[1] for x in field_values["subspecialty"].items() if x[0] in subspecialty]
                if taxonomy_greedy == True:
                    try:
                        taxonomies = [item for sublist in taxonomies for item in sublist] # unnest
                    except:
                        next

            # nested list (default non-greedy), bring up underlying codes & append list
            elif any(isinstance(el, list) for el in subspecialty): 
                temp2 = []
                for i in range(0,len(subspecialty)):
                    temp = [x[1] for x in field_values["subspecialty"].items() if x[0] in subspecialty[i]]
                    temp2.extend(temp)
                taxonomies.extend(temp2)

            # non-greedy list, , bring up underlying codes & extend list wrapped values
            elif (type(subspecialty) == list) & (taxonomy_greedy == False):
                temp = [x[1] for x in field_values["subspecialty"].items() if x[0] in subspecialty]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                taxonomies.extend([temp])
                
            # greedy list, bring up underlying codes & extend values
            elif (type(subspecialty) == list) & (taxonomy_greedy == True):
                temp = [x[1] for x in field_values["subspecialty"].items() if x[0] in subspecialty]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                taxonomies.extend(temp)

        if specialty != None:

            # string or int, make list
            if (type(specialty) == str) | (type(specialty) == int):
                specialty = [str(specialty)]
            # if not greedy and not nested, make it so
            if (taxonomy_greedy == False) &  (any(isinstance(el, list) for el in specialty) == False):
                specialty = [specialty]

            # list and no length, make taxonomies the list specified
            if (type(specialty) == list) & (len(taxonomies) == 0):
                taxonomies = [x[1] for x in field_values["specialty"].items() if x[0] in specialty]
                if taxonomy_greedy == True:
                    try:
                        taxonomies = [item for sublist in taxonomies for item in sublist] # unnest
                    except:
                        next

            # nested list (default non-greedy), bring up underlying codes & append list
            elif any(isinstance(el, list) for el in specialty): 
                temp2 = []
                for i in range(0,len(specialty)):
                    temp = [x[1] for x in field_values["specialty"].items() if x[0] in specialty[i]]
                    temp2.extend(temp)
                taxonomies.extend(temp2)

            # non-greedy list, , bring up underlying codes & extend list wrapped values
            elif (type(specialty) == list) & (taxonomy_greedy == False):
                temp = [x[1] for x in field_values["specialty"].items() if x[0] in specialty]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                taxonomies.extend([temp])
                
            # greedy list, bring up underlying codes & extend values
            elif (type(specialty) == list) & (taxonomy_greedy == True):
                temp = [x[1] for x in field_values["specialty"].items() if x[0] in specialty]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                taxonomies.extend(temp)

        if specialty_category != None:

            # string or int, make list
            if (type(specialty_category) == str) | (type(specialty_category) == int):
                specialty_category = [str(specialty_category)]
            # if not greedy and not nested, make it so
            if (taxonomy_greedy == False) &  (any(isinstance(el, list) for el in specialty_category) == False):
                specialty_category = [specialty_category]

            # list and no length, make taxonomies the list specified
            if (type(specialty_category) == list) & (len(taxonomies) == 0):
                taxonomies = [x[1] for x in field_values["specialty_category"].items() if x[0] in specialty_category]
                if taxonomy_greedy == True:
                    try:
                        taxonomies = [item for sublist in taxonomies for item in sublist] # unnest
                    except:
                        next

            # nested list (default non-greedy), bring up underlying codes & append list
            elif any(isinstance(el, list) for el in specialty_category): 
                temp2 = []
                for i in range(0,len(specialty_category)):
                    temp = [x[1] for x in field_values["specialty_category"].items() if x[0] in specialty_category[i]]
                    temp2.extend(temp)
                taxonomies.extend(temp2)

            # non-greedy list, bring up underlying codes & extend list wrapped values
            elif (type(specialty_category) == list) & (taxonomy_greedy == False):
                temp = [x[1] for x in field_values["specialty_category"].items() if x[0] in specialty_category]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                taxonomies.extend([temp])
                
            # greedy list, bring up underlying codes & extend values
            elif (type(specialty_category) == list) & (taxonomy_greedy == True):
                temp = [x[1] for x in field_values["specialty_category"].items() if x[0] in specialty_category]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                taxonomies.extend(temp)

        # drop any empty lists
        taxonomies = [x for x in taxonomies if len(x) > 0]

        if len(taxonomies) == 0:
            taxonomies = None

        # wrap any loose items if list of lists
        if any(isinstance(el, list) for el in taxonomies):
            taxonomies = [[x] if type(x) != list else x for x in taxonomies]

    return taxonomies, taxonomy_greedy, warnings_list

def geoPriority(state, division, region, metro, short_zip, field_values):
    """
    Surface underlying zip and state values for text
    """
    # control for all nones
    if (state == None) & (division == None) & (region == None) & (metro == None) & (short_zip == None):
        states2 = None
        zips = None 
        warnings_list = []
    else:

        # warning and flattening of any multi-level geo lists
        warnings_list = []
        if (state != None):
            next
            if (any(isinstance(el, list) for el in state)):
                state = [item for sublist in state for item in sublist]
                warnings_list.append("*** Multi-Level lists are not allowed within geographical fields *** query will include results for ANY 'state' fields listed")
        if (division != None):
            next
            if (any(isinstance(el, list) for el in division)):
                division = [item for sublist in division for item in sublist]
                warnings_list.append("*** Multi-Level lists are not allowed within geographical fields *** query will include results for ANY 'division' fields listed")
        if (region != None):
            next
            if (any(isinstance(el, list) for el in region)):
                region = [item for sublist in region for item in sublist]
                warnings_list.append("*** Multi-Level lists are not allowed within geographical fields *** query will include results for ANY 'region' fields listed")
        if (metro != None):
            next
            if (any(isinstance(el, list) for el in metro)):
                metro = [item for sublist in metro for item in sublist]
                warnings_list.append("*** Multi-Level lists are not allowed within geographical fields *** query will collapse list to include results for ANY 'metro' fields listed")
        if (short_zip != None):
            next
            if (any(isinstance(el, list) for el in short_zip)):
                short_zip = [item for sublist in short_zip for item in sublist]
                warnings_list.append("*** Multi-Level lists are not allowed within geographical fields *** query will collapse list to include results for ANY 'metro' fields listed")

        ### state-mapped sources ###

        # state logic
        states = []
        if state != None:
            if (type(state) == str):
                state = [state]
            if (type(state) == list) & (len(state) != 0):
                states.extend(state)

        # division logic
        divisions = []
        if division != None:
            if (type(division) == str):
                state = [division]
            if (type(division) == list) & (len(division) != 0):
                temp = [x[1] for x in field_values["division"].items() if x[0] in division]
                try:
                    temp = [item for sublist in temp for item in sublist]
                except:
                    next
                divisions.extend(temp)

        # _region logic
        regions = []
        if region != None:
            if (type(region) == str):
                state = [region]
            if (type(region) == list) & (len(region) != 0):
                temp = [x[1] for x in field_values["region"].items() if x[0] in region]
                try:
                    temp = [item for sublist in temp for item in sublist]
                except:
                    next
                regions.extend(temp)

        ### zip-mapped sources ###

        # short_zip logic
        short_zips = []
        if short_zip != None:
            if (type(short_zip) == str):
                short_zip = [short_zip]
            if (type(short_zip) == list) & (len(short_zip) != 0):
                short_zips.extend(short_zip)

        # metro logic
        metros = []
        if metro != None:
            if (type(metro) == str):
                metro = [metro]
            if (type(metro) == list) & (len(metro) != 0):
                temp = [x[1] for x in field_values["metro"].items() if x[0] in metro]
                try:
                    temp = [item for sublist in temp for item in sublist]
                except:
                    next
                metros.extend(temp)

        ### Hierarchical Inclusivity Measures (in, out, both) ### 

        # intra zip priority
        if (len(short_zips) != 0) & (len(metros) != 0):
            zips = short_zips + metros
        elif (len(short_zips) != 0) & (len(metros) == 0):
            zips = short_zips
        elif (len(short_zips) == 0) & (len(metros) != 0):
            zips = metros
        else:
            zips = None

        # intra state priority
        if (len(states) != 0) & (len(divisions) != 0) & (len(regions) != 0): # all non-null
            states2 = states + divisions + regions
        elif (len(states) == 0) & (len(divisions) != 0) & (len(regions) != 0): # states non-null
            states2 = divisions + regions
        elif (len(states) != 0) & (len(divisions) != 0) & (len(regions) == 0): # regions non-null
            states2 = states + divisions
        elif (len(states) != 0) & (len(divisions) == 0) & (len(regions) != 0): # divisions non-null
            states2 = states + regions
        elif (len(states) != 0) & (len(divisions) == 0) & (len(regions) == 0): # only states
            states2 = states
        elif (len(states) == 0) & (len(divisions) == 0) & (len(regions) != 0): # only regions
            states2 = regions
        elif (len(states) == 0) & (len(divisions) != 0) & (len(regions) == 0): # only divisions
            states2 = divisions
        else:
            states2 = None

        # remove zips when overlapped with state
        if (zips != None) & (states2 != None):
            state_zips = [x[1] for x in field_values["state"].items() if x[0] in states2]
            if (any(isinstance(el, list) for el in state_zips)): 
                state_zips = [y for x in state_zips for y in x]
            overlapping_zips = [x for x in zips if x in state_zips]
            if len(overlapping_zips) > 0:
                warnings_list.append(f"Overlapping state/short_zip Selection: The following short_zip codes ({overlapping_zips}) appear within State selection(s) made, query will return state and non-overlappning short_zip results. To return excluded short_zip codes only, specify without overlapping state.")
            zips = [x for x in zips if x not in state_zips]

        ### Warnings On Multi-Selection ### 
        try:
            if (len(states) != 0) & (len(divisions) != 0) | (len(regions) != 0) & (len(divisions) != 0) | (len(states) != 0) & (len(regions) != 0) | (len(metros) != 0) & (len(zips) != 0):
                warnings_list.append("Multiple Geography Options Selected: Greedy Diagnosis Priority *** Query will return all results that corresponding to ANY of the States and/or Short Zip Codes selected.")
            elif (len(states) > 0) & (len(zips) > 0):
                warnings_list.append("Multiple Geography Options Selected: Greedy Diagnosis Priority *** Query will return all results that corresponding to ANY of the States and/or Short Zip Codes selected.")
        except:
            next
        
        if states2 != None:
            if (len(states2) == 0):
                states2 = None
        if zips != None:
            if len(zips) == 0:
                zips = None

    return states2, zips, warnings_list

def scriptPriority(ndc, substance, pharm_class, marketing_category, script_greedy, field_values):
    
    """
    Surface underlying NDCs for text and string according to script greedy policy
    """
    
    # control for all nones
    if (ndc == None) & (substance == None) & (marketing_category == None) & (pharm_class == None):
        ndcs = None
        warnings_list = []
    else:    
        # determine if we need to be greedy at any point within scripts
        if (ndc != None):
            next
            if (any(isinstance(el, list) for el in ndc)):
                script_greedy = False
        if (substance != None):
            next
            if (any(isinstance(el, list) for el in substance)):
                script_greedy = False
        if (pharm_class != None):
            next
            if (any(isinstance(el, list) for el in pharm_class)):
                script_greedy = False
        if (marketing_category != None):
            next
            if (any(isinstance(el, list) for el in marketing_category)):
                script_greedy = False
        
        # set default greediness
        if script_greedy != False:
            script_greedy = True

        # proper warning
        if script_greedy == False:
            warnings_item2 = "Non-Greedy Script Priority *** this query will use 'AND' logic for script list selections, all NDCs within sub-lists MUST be present in order to be returned."
        else:
            warnings_item2 = "Greedy Script Priority *** this query will use 'OR' logic for script selections, meaning that query will return all results where ANY NDC is present."

        # multiple category warning
        if len([x for x in [ndc, substance, pharm_class, marketing_category] if x != None]) > 1:
            warnings_item1 = f"Multiple NDC Options Selected: {warnings_item2}"
            warnings_list = [warnings_item1]
        else:
            warnings_list = []

        # instantiate ndc
        ndcs = []

        if ndc != None:
            # if string or int, make list
            if (type(ndc) == str) | (type(ndc) == int):
                ndc = [str(ndc)]
            # if not greedy and not nested, make it so
            if (script_greedy == False) &  (any(isinstance(el, list) for el in ndc) == False):
                ndc = [ndc]
            # if list and no length, make ndcs
            if (type(ndc) == list) & (len(ndc) > 0):
                ndcs.extend(ndc)

        if substance != None:

            # string or int, make list
            if (type(substance) == str) | (type(substance) == int):
                substance = [str(substance)]
            # if not greedy and not nested, make it so
            if (script_greedy == False) &  (any(isinstance(el, list) for el in substance) == False):
                substance = [substance]

            # list and no length, make ndcs the list specified
            if (type(substance) == list) & (len(ndcs) == 0):
                ndcs = [x[1] for x in field_values["substance"].items() if x[0] in substance]
                if script_greedy == True:
                    try:
                        ndcs = [item for sublist in ndcs for item in sublist] # unnest
                    except:
                        next

            # nested list (default non-greedy), bring up underlying codes & append list
            elif any(isinstance(el, list) for el in substance): 
                temp2 = []
                for i in range(0,len(substance)):
                    temp = [x[1] for x in field_values["substance"].items() if x[0] in substance[i]]
                    temp2.extend(temp)
                ndcs.extend(temp2)

            # non-greedy list, , bring up underlying codes & extend list wrapped values
            elif (type(substance) == list) & (script_greedy == False):
                temp = [x[1] for x in field_values["substance"].items() if x[0] in substance]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                ndcs.extend([temp])
                
            # greedy list, bring up underlying codes & extend values
            elif (type(substance) == list) & (script_greedy == True):
                temp = [x[1] for x in field_values["substance"].items() if x[0] in substance]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                ndcs.extend(temp)

        if pharm_class != None:

            # string or int, make list
            if (type(pharm_class) == str) | (type(pharm_class) == int):
                pharm_class = [str(pharm_class)]
            # if not greedy and not nested, make it so
            if (script_greedy == False) &  (any(isinstance(el, list) for el in pharm_class) == False):
                pharm_class = [pharm_class]

            # list and no length, make ndcs the list specified
            if (type(pharm_class) == list) & (len(ndcs) == 0):
                ndcs = [x[1] for x in field_values["pharm_class"].items() if x[0] in pharm_class]
                if script_greedy == True:
                    try:
                        ndcs = [item for sublist in ndcs for item in sublist] # unnest
                    except:
                        next

            # nested list (default non-greedy), bring up underlying codes & append list
            elif any(isinstance(el, list) for el in pharm_class): 
                temp2 = []
                for i in range(0,len(pharm_class)):
                    temp = [x[1] for x in field_values["pharm_class"].items() if x[0] in pharm_class[i]]
                    temp2.extend(temp)
                ndcs.extend(temp2)

            # non-greedy list, , bring up underlying codes & extend list wrapped values
            elif (type(pharm_class) == list) & (script_greedy == False):
                temp = [x[1] for x in field_values["pharm_class"].items() if x[0] in pharm_class]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                ndcs.extend([temp])
                
            # greedy list, bring up underlying codes & extend values
            elif (type(pharm_class) == list) & (script_greedy == True):
                temp = [x[1] for x in field_values["pharm_class"].items() if x[0] in pharm_class]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                ndcs.extend(temp)

        if marketing_category != None:

            # string or int, make list
            if (type(marketing_category) == str) | (type(marketing_category) == int):
                marketing_category = [str(marketing_category)]
            # if not greedy and not nested, make it so
            if (script_greedy == False) &  (any(isinstance(el, list) for el in marketing_category) == False):
                marketing_category = [marketing_category]

            # list and no length, make ndcs the list specified
            if (type(marketing_category) == list) & (len(ndcs) == 0):
                ndcs = [x[1] for x in field_values["marketing_category"].items() if x[0] in marketing_category]
                if script_greedy == True:
                    try:
                        ndcs = [item for sublist in ndcs for item in sublist] # unnest
                    except:
                        next

            # nested list (default non-greedy), bring up underlying codes & append list
            elif any(isinstance(el, list) for el in marketing_category): 
                temp2 = []
                for i in range(0,len(marketing_category)):
                    temp = [x[1] for x in field_values["marketing_category"].items() if x[0] in marketing_category[i]]
                    temp2.extend(temp)
                ndcs.extend(temp2)

            # non-greedy list, bring up underlying codes & extend list wrapped values
            elif (type(marketing_category) == list) & (script_greedy == False):
                temp = [x[1] for x in field_values["marketing_category"].items() if x[0] in marketing_category]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                ndcs.extend([temp])
                
            # greedy list, bring up underlying codes & extend values
            elif (type(marketing_category) == list) & (script_greedy == True):
                temp = [x[1] for x in field_values["marketing_category"].items() if x[0] in marketing_category]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                ndcs.extend(temp)

        # drop any empty lists
        ndcs = [x for x in ndcs if len(x) > 0]

        if len(ndcs) == 0:
            ndcs = None

        # wrap any loose items if list of lists
        if any(isinstance(el, list) for el in ndcs):
            ndcs = [[x] if type(x) != list else x for x in ndcs]

    return ndcs, script_greedy, warnings_list

def drgPriority(drg_code, drg_category, drg_greedy, field_values):
    """
    Surface underlying drg codes for text and string according to drg greedy policy
    """
    # control for all nones
    if (drg_code == None) & (drg_category == None):
        drgs = None
        warnings_list = []
    else:
        # determine if we need to be greedy at any point within drgs
        if (drg_code != None):
            next
            if (any(isinstance(el, list) for el in drg_code)):
                drg_greedy = False
        if (drg_category != None):
            next
            if (any(isinstance(el, list) for el in drg_category)):
                drg_greedy = False
        
        # set default greediness
        if drg_greedy != False:
            drg_greedy = True

        # proper warning
        if drg_greedy == False:
            warnings_item2 = "Non-Greedy DRG Priority *** this query will use 'AND' logic for DRG list selections, all drgs within sub-lists MUST be present in order to be returned."
        else:
            warnings_item2 = "Greedy DRG Priority *** this query will use 'OR' logic for DRG selections, meaning that query will return all results where ANY DRG is present."

        # multiple category warning
        if len([x for x in [drg_code, drg_category] if x != None]) > 1:
            warnings_item1 = f"Multiple DRG Options Selected: {warnings_item2}"
            warnings_list = [warnings_item1]
        else:
            warnings_list = []

        # instantiate drgs
        drgs = []

        if drg_code != None:
            # if string or int, make list
            if (type(drg_code) == str) | (type(drg_code) == int):
                drg_code = [str(drg_code)]
            # if not greedy and not nested, make it so
            if (drg_greedy == False) &  (any(isinstance(el, list) for el in drg_code) == False):
                drg_code = [drg_code]
            # if list and no length, make drgs
            if (type(drg_code) == list) & (len(drg_code) > 0):
                drgs.extend(drg_code)

        if drg_category != None:

            # string or int, make list
            if (type(drg_category) == str) | (type(drg_category) == int):
                drg_category = [str(drg_category)]
            # if not greedy and not nested, make it so
            if (drg_greedy == False) &  (any(isinstance(el, list) for el in drg_category) == False):
                drg_category = [drg_category]

            # list and no length, make drgs the list specified
            if (type(drg_category) == list) & (len(drg_category) == 0):
                drgs = [x[1] for x in field_values["drg_category"].items() if x[0] in drg_category]
                if drg_greedy == True:
                    try:
                        drg_greedy = [item for sublist in drg_greedy for item in sublist] # unnest
                    except:
                        next

            # nested list (default non-greedy), bring up underlying codes & append list
            elif any(isinstance(el, list) for el in drg_category): 
                temp2 = []
                for i in range(0,len(drg_category)):
                    temp = [x[1] for x in field_values["drg_category"].items() if x[0] in drg_category[i]]
                    temp2.extend(temp)
                drgs.extend(temp2)

            # non-greedy list, , bring up underlying codes & extend list wrapped values
            elif (type(drg_category) == list) & (drg_greedy == False):
                temp = [x[1] for x in field_values["drg_category"].items() if x[0] in drg_category]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                drgs.extend([temp])
                
            # greedy list, bring up underlying codes & extend values
            elif (type(drg_category) == list) & (drg_greedy == True):
                temp = [x[1] for x in field_values["drg_category"].items() if x[0] in drg_category]
                try:
                    temp = [item for sublist in temp for item in sublist] # unnest
                except:
                    next
                drgs.extend(temp)

        # drop any empty lists
        drgs = [x for x in drgs if len(x) > 0]

        if len(drgs) == 0:
            drgs = None

        # wrap any loose items if list of lists
        if any(isinstance(el, list) for el in drgs):
            drgs = [[x] if type(x) != list else x for x in drgs]

    return drgs, drg_greedy, warnings_list

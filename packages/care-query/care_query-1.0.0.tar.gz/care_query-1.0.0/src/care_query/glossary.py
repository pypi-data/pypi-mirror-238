# COPYRIGHT 2022 MONOOCLE INSIGHTS
# ALL RIGHTS RESERVED
# UNAUTHORIZED USE, REPRODUCTION, OR
# DISTRIBUTION STRICTLY PROHIBITED
#
# AUTHOR: Raymond Deiotte and Sean O'Malley
# CREATION DATE: 20230822
# LAST UPDATED: 20230822

### Import Packages ###
import json
import importlib.resources

### Data Dictionary ###

# create data table description 
tables = {"JOURNEY_TABLE":{"description":"This dataset offers comprehensive detail of longitudinal patient journeys, with line-item encounter detail, insight into payor, provider, procedure, revenue code, charges and SmartAllowedAmount®.", 
                           "queries":["careEncounter", "careVisit", "careEpisode", "careJourney"], 
                           "features":{"journey_id": "Randomly generated identifier unique to each longitudinal patient journey.",
                                        "episode_id": "Randomly generated identifier unique to each sequence of encounters with at least 30 days between visits.",
                                        "visit_id": "Randomly generated identifier unique to each set of encounters that occur within the same event of care.",
                                        "encounter_id": "Randomly generated identifier, unique to an isolated event of care.",
                                        "date": "Primary date of each encounter.",
                                        "patient_age": "Age (within 5 years) of the patient on each encounter.",
                                        "patient_state": "US State residence of the patient on each encounter.",
                                        "patient_zip3": "First three zip code digits of the patient on each encounter.",
                                        "place_of_service": "Type of facility where a encounter occurred.",
                                        "visit_type": "Description of the setting of care.",
                                        "payor": "Name of the primary payor on each encounter.",
                                        "payor_channel": "Payor channel-of-business, line-of-business, or plan type.",
                                        "ref_npi": "Referring individual provider of an encounter, identified via their National Provider Identifier (NPI).",
                                        "hcp_npi": "Primary individual provider of an encounter, identified via their National Provider Identifier (NPI).",
                                        "hcp_taxonomy": "Primary taxonomy code of the individual provider on an encounter.",
                                        "hcp_specialty": "Primary specialty of the individual provider provider on an encounter.",
                                        "hco_npi": "Organizational provider of an encounter, identified via their National Provider Identifier (NPI).",
                                        "diag_1": "Primary diagnosis listed on each encounter, can be represented as an ICD10 code.",
                                        "diag_2": "Secondary diagnosis listed on each encounter, can be represented as an ICD10 code.",
                                        "diag_3": "Tertiary diagnosis listed on each encounter, can be represented as an ICD10 code.",
                                        "diag_4": "Fourth diagnosis listed on each encounter, can be represented as an ICD10 code.",
                                        "diag_5": "Fifth diagnosis listed on each encounter, can be represented as an ICD10 code.",
                                        "proc_code": "Procedure performed within each encounter.",
                                        "proc_units": "Total number of procedure units within each encounter.",
                                        "proc_modifier": "Procedure code modifier for procedure performed within encounter.",
                                        "rev_code": "Revenue Center code designated for each encounter.",
                                        "rev_units": "Total number of days in which the revenue code was designated within the healthcare interaction.",
                                        "charge": "Line-item charge submitted to insurers. The charge is the pre-adjudicated value submitted to insurers.",
                                        "smart_allowed": "Line-item estimate of allowed amount, utilizing proprietary ML on CMS, Price Transparency and Actual Adjudicated amounts to provide estimates within an average of 5% variance from actuals."}
                            },
            "NPPES_TABLE":{"description":"This table is a cleaned, normalized and monthly-updated verions of the CMS NPPES database.", 
                           "queries":["nppesDetail"], 
                           "features":{"npi":"National Provider Identifier (NPI) of the individual/organizational provider registered with NPPES.",
                                       "name":"Full name or organizational name of the individual/organizational provider registered with NPPES.",
                                       "entity_type":"Indicator of whether the corresponding provider is an individual or organization.",
                                       "gender":"Gender of the individual provider.",
                                       "credential":"Medical credential of the individual provider.",
                                       "primary_taxonomy_code":"Primary taxonomy code of the individual/organizational provider.",
                                       "secondary_taxonomy_code":"Secondary taxonomy code of the individual/organizational provider.",
                                       "address":"Primary address of the individual/organizational provider, as reported to NPPES.",
                                       "metro":"City, State of the primary address of the individual/organizational provider, as reported to NPPES.",
                                       "state":"State of the primary address of the individual/organizational provider, as reported to NPPES.",
                                       "zip":"Zip code of the primary address of the individual/organizational provider, as reported to NPPES.",
                                       "phone":"Primary phone number of the individual/organizational provider, as reported to NPPES.",
                                       "fax":"Primary fax number of the individual/organizational provider, as reported to NPPES.",
                                       "sole_proprietor":"Binary indicator (yes, no) as to whether the provider is registered as a sole proprietor with NPPES.",
                                       "org_subpart":"Binary indicator (yes, no) as to whether the provider is registered as an organizational subpart with NPPES.",
                                       "forg_lbnax":"Legal business name of the parent organization associated with an NPI.",
                                       "update_date":"The last date in which the provider contact details have been updated"}
                            }, 
            "DIAG_TABLE":{"description":"This table provides helpful context and categories around ICD-10 diagnosis codes.", 
                           "queries":["diagDetail"], 
                           "features":{"diag_code":"ICD-10 diagnosis code",
                                       "short_diag_code":"First three characters of the ICD-10 diagnosis code, corresponding to the diagnosis subcategory",
                                       "diag_subcategory":"Name of the ICD-10 diagnosis sub-category",
                                       "diag_category":"Name of the ICD-10 diagnosis category",
                                       "diag_desc":"Description of the ICD-10 diagnosis code",
                                       "icd9_code":"ICD-9 mapping to the ICD-10 diagnosis code",
                                       "diag_severity":"CMS-designated severity score from 0 to 100"}
                            }, 
            "PROC_TABLE":{"description":"This table provides helpful context and categories around CPT/HCPCS procedure codes.", 
                           "queries":["procDetail"], 
                           "features":{"proc_code":"CPT/HCPCS procedural code",
                                       "proc_category":"Name of the CPT/HCPCS procedural category",
                                       "proc_subcategory":"Name of the CPT/HCPCS procedural sub-category",
                                       "proc_desc":"Description of the procedure code"}
                            },
            "SPECIALTY_TABLE":{"description":"This table provides helpful context and categories around taxonomy codes and specialty mappings.", 
                           "queries":["specDetail"], 
                           "features":{"taxonomy_code":"Taxonomy code classification system that identifies the specific area of practice of a healthcare provider",
                                       "subspecialty":"Sub-specialty are specific areas of focus within a healthcare specialty",
                                       "specialty":"Specialty is a branch of medicine that focuses on a specific area of the body, disease, or population",
                                       "specialty_category":"Broader categories of specialty areas of focus"}
                            },
            "MIPS_TABLE":{"description":"This table takes the monthly updates to the CMS MIPS database, cleans, normalizes and orients their output into a concise feature set built for consumption.", 
                           "queries":["mipsDetail"], 
                           "features":{"npi":"National Provider Identifier (NPI) of the individual/organizational provider registered with NPPES.",
                                       "org_pac_id":"Unique group ID assigned by PECOS to the group this individual participated in",
                                       "name":"Individual clinician's full name",
                                       "source":"Method by which the clinician achieved scores (“individual”, “group”, “virtual group”,  or “apm”); if the source is “apm”, this indicates that the MIPS APM scoring standard was applied for this set of scores",
                                       "quality_score":"Quality performance category score",
                                       "interop_score":"Promoting Interoperability (PI) performance category score",
                                       "improvement_score":"Improvement Activities (IA) performance category score",
                                       "mips_score_without_cpb":"MIPS Final Score without the Complex Patient Bonus (CPB). The CPB is part of the MIPS final score based on the overall medical complexity and social risk for one’s patients treated",
                                       "mips_score":"Final Merit-based Incentive Payment System (MIPS) score",
                                       "update_date":"The last date in which the provider contact details have been updated"}
                            },
            "GEO_TABLE":{"description":"This table allows provides a comprehensive view of every geographic area in the US, providing population and growth statistics from zip and county to geographic US regions.", 
                           "queries":["geoDetail"], 
                           "features":{"zip":"Postal Zone Improvement Plan (ZIP) code corresponding to a geographic area",
                                       "zip3":"First three digits of the zip code",
                                       "county_code":"US Government's Federal Information Processing Standards (FIPS) code for state-county combination",
                                       "county":"Name and State of the corresponding county",
                                       "county_pop":"US Census estimated population of the County population",
                                       "county_growth_rate":"US Census estimated County population growth trend",
                                       "metro":"US Census Bureau metropolitan and micropolitan statistical area",
                                       "metro_location":"Centrality of the county as it relates to the corresponding US Metro",
                                       "state_code":"Two digit code representing a US State",
                                       "state":"Full name of US State",
                                       "state_pop":"US Census estimated population of the State population",
                                       "state_growth_rate":"US Census estimated State population growth trend",
                                       "division":"Nine minor State groupings as defined by the US Census Bureau",
                                       "division_pop":"US Census estimated population of the Division population",
                                       "division_growth_rate":"US Census estimated Division population growth trend",
                                       "region":"Four major State groupings as defined by the US Census Bureau",
                                       "region_pop":"US Census estimated population of the Region population",
                                       "region_growth_rate":"US Census estimated Region population growth trend"}
                            },
            "EXEC_OUTREACH_TABLE":{"description":"This table provides methods of outreach for hospital and health system executives, including email, LinkedIn and role context.", 
                           "queries":["execOutreach"], 
                           "features":{"exec_name":"Full name of the executive record",
                                       "hospital":"Primary hospital/system associated with the executive record",
                                       "title":"Role title associated with the hospital/system executive record",
                                       "department":"Departmental affiliation with the role of the executive record",
                                       "exec_level":"Administrative level of the executive record",
                                       "email1":"Primary email address of the hospital/system executive record",
                                       "email2":"Secondary email address of the hospital/system executive record",
                                       "address":"Primary address of the hospital/system executive record",
                                       "city":"City for the primary address of the hospital/system executive record",
                                       "state":"US State code for the primary address of the hospital/system executive record",
                                       "zip":"Zip code for the primary address of the hospital/system executive record",
                                       "phone":"Primary phone number of the hospital/system executive record",
                                       "linkedin":"LinkedIn URL for the hospital/system executive record",
                                       "npi":"National Provider Identifier (NPI) if executive is an NPPES registered healthcare provider",
                                       "org_url":"Organizational website most closely associated with the executive record",
                                       "system_exec":"Biary indicator of whether the executive is at the hospital or health system administrative level",
                                       "update_date":"The last date in which the hospital executive contact details have been updated"}
                            }, 
            "PROV_OUTREACH_TABLE":{"description":"This table provides methods of outreach for individual healthcare providers, including emails, and primary locations.", 
                           "queries":["provOutreach"], 
                           "features":{"hcp_npi":"National Provider Identifier (NPI) of the individual provider registered with NPPES.",
                                       "hcp_name":"Full name of the individual provider record",
                                       "taxonomy":"Primary taxonomy for the provider record",
                                       "subspecialty":"Subspecialty name for the primary taxonomy of the provider record",
                                       "specialty":"Specialty name for the primary taxonomy of the provider record",
                                       "specialty_category":"Specialty category name for the primary taxonomy of the provider record",
                                       "email1":"Primary email address of the individual provider",
                                       "email2":"Secondary email address of the individual provider",
                                       "address":"Primary address on record of the individual provider",
                                       "city":"Primary city of address for the individual provider record",
                                       "state":"Two digit code representing a US State",
                                       "zip":"Postal Zone Improvement Plan (ZIP) code corresponding to a geographic area",
                                       "phone":"Primary phone number of the individual provider",
                                       "fax":"Primary fax number of the individual provider",
                                       "update_date":"The last date in which the provider contact details have been updated"}
                            },
            "AFFILIATION_TABLE":{"description":"This table offers comprehensive detail of individual provider affiliations through time, with particular attention to the totals of their actual clinical activity, where they practice, how those locations are affiliated with systems.", 
                           "queries":["affiliationActivity","updateAffiliation"], 
                           "features":{"hcp_npi":"National Provider Identifier (NPI) of the individual provider registered with NPPES.",
                                       "hcp_name":"Full name of the individual provider",
                                       "hcp_taxonomy":"Primary taxonomy code of the individual provider",
                                       "hcp_state":"US State code of the NPPES registered provider address",
                                       "hcp_short_zip":"Short zip code of the NPPES registered provider address",
                                       "system_affiliation":"Anticipated health system affiliation of the individual provider derived from their practice patterns and reported affiliation",
                                       "affiliation_confounded":"Binary indicator of whether provider practice patterns indicate multiple affiliations or absence of a reliable behavioral indicator of affiliation",
                                       "primary_hco_npi":"National Provider Identifier (NPI) of the facility/department where the individual provider performed the **most** encounters within one year of the indicated lookback year/quarter",
                                       "primary_hco_name":"Name of the facility/department where the individual provider performed the most encounters within one year of the indicated lookback year/quarter",
                                       "primary_hco_system":"Health system affiliation of the facility/department where the individual provider performed the most encounters within one year of the indicated lookback year/quarter",
                                       "primary_hco_encounters":"Number of encounters seen by individual provider at the primary_hco within the lookback window",
                                       "primary_hco_proportion":"Proportion of encounters seen by individual provider at the primary_hco compared to all other hco's, within the lookback window",
                                       "secondary_hco_npi":"National Provider Identifier (NPI) of the facility/department where the individual provider performed the second most encounters within one year of the indicated lookback year/quarter",
                                       "secondary_hco_name":"Name of the facility/department where the individual provider performed the second mostencounters within one year of the indicated lookback year/quarter",
                                       "secondary_hco_system":"Health system affiliation of the facility/department where the individual provider performed the second most encounters within one year of the indicated lookback year/quarter",
                                       "secondary_hco_encounters":"Number of encounters seen by individual provider at the secondary_hco within the lookback window",
                                       "secondary_hco_proportion":"Proportion of encounters seen by individual provider at the secondary_hco compared to all other hco's, within the lookback window",
                                       "tertiary_hco_npi":"National Provider Identifier (NPI) of the facility/department where the individual provider performed the third most encounters within one year of the indicated lookback year/quarter",
                                       "tertiary_hco_name":"Name of the facility/department where the individual provider performed the third most encounters within one year of the indicated lookback year/quarter",
                                       "tertiary_hco_system":"Health system affiliation of the facility/department where the individual provider performed the third most encounters within one year of the indicated lookback year/quarter",
                                       "tertiary_hco_encounters":"Number of encounters seen by individual provider at the tertiary_hco within the lookback window",
                                       "tertiary_hco_proportion":"Proportion of encounters seen by individual provider at the tertiary_hco compared to all other hco's, within the lookback window",
                                       "lookback_period":"End year-quarter value of the 1-year lookback period. Per the example, affiliation is calculated using encounters from the start of Q3-2022 to the start of Q3-2023",
                                       "current":"Binary indicator as to whether the period is the most recent recorded within CareQuery"}
                            },
            "ALLOWED_AVGS_TABLE":{"description":"This table gives users the ability to visualize the statistical shape of allowed amounts for procedure-specific claims across the US.",   
                           "queries":["procAllowedAvgs"], 
                           "features":{"proc_code": "CPT/HCPCS procedural code - used as a grouper for all corresponding statistics.",
                                       "proc_subcategory":"Sub-categorical description of the procedure code - used as a grouper for all corresponding statistics.",
                                       "state":"US State where the procedure was performed  - used as a grouper for all corresponding statistics.",
                                       "payor_channel":"Payor channel-of-business, line-of-business, or plan type  - used as a grouper for all corresponding statistics.",
                                       "visit_type": "Description of the setting of care  - used as a grouper for all corresponding statistics.",
                                       "total_encounters":"Total number of encounters corresponding to the groupers within the period and utilized in the allowed amount statistics.",
                                       "trimmed_mean_allowed_amount":"The mean allowed amount with outliers trimmed from consideration.",
                                       "mean_allowed_amount":"The mean allowed amount with all corresponding encounters considered.",
                                       "min_allowed_amount":"The minimum encounter allowed amount seen within the groupers/period.",
                                       "percentile_10":"The 10th percentile of all allowed amount values seen within the corresponding groupers/period.",
                                       "percentile_20":"The 20th percentile of all allowed amount values seen within the corresponding groupers/period.",
                                       "percentile_50":"The 50th percentile of all allowed amount values seen within the corresponding groupers/period.",
                                       "percentile_80":"The 80th percentile of all allowed amount values seen within the corresponding groupers/period.",
                                       "percentile_90":"The 90th percentile of all allowed amount values seen within the corresponding groupers/period.",
                                       "max_allowed_amount":"The maximum encounter allowed amount seen within the groupers/period.",
                                       "lookback_period":"All values are computed within an year-long lookback period on a quarterly basis. This value represents the most recent quarter-year in which a lookback has occurred.",
                                       "current":"Binary indicator as to whether the listed period is the most current.",}
                            },
            "SCRIPT_TABLE":{"description":"This table provides prescription claim with comprehensive drug and provider details, across entire longitudinal journeys.",   
                           "queries":["scriptEncounter", "scriptJourney"], 
                           "features":{"journey_id":"Randomly generated identifier unique to each longitudinal patient journey",
                                       "script_id":"Randomly generated identifier unique to each prescription claim",
                                       "group_id":"Randomly generated identifier unique to each payor plan corresponding to the prescription written",
                                       "script_date":"Date the prescription was written ",
                                       "service_date":"Date that the prescription was filled, services rendered, or the payer began coverage following Part A expiration in a long-term care setting",
                                       "patient_state":"US State residence of the patient on each encounter",
                                       "patient_short_zip":"First three digits of the patient zip code",
                                       "patient_age":"Age of the patient at the moment of each encounter",
                                       "patient_gender":"Gender/Sex of the patient",
                                       "hcp_npi":"National Provider Identifier (NPI) of the individual that wrote the prescription for the patient",
                                       "hcp_taxonomy":"Primary taxonomy code of the individual provider who wrote the prescription",
                                       "hcp_specialty":"Primary specialty of the individual provider provider wrote the prescription",
                                       "hco_npi":"National Provider Identifier (NPI) of the organization that fulfilled the prescription",
                                       "ndc":"FDA National Drug Code version 11 standardized code for a dispensed drug",
                                       "proprietary_name":"Unique brand name of a drug product as assigned by the drug manufacturer",
                                       "refills":"Maximum number of refills authorized",
                                       "quantity_prescribed":"Quantity of drug units prescribed",
                                       "quantity_dispensed":"Quantity of drug units dispensed",
                                       "fill_number":"Refill number for the current SCRIPT_ID",
                                       "days_supply":"Estimated number of days the dispensed drugs will last",
                                       "unit_of_measure":"Units of measure for the quantity_dispensed",
                                       "submitted_cost":"Pharmacy submitted cost of the claim",
                                       "patient_pay":"Patient cost responsibility as determined by payor",
                                       "copay_insurance":"Patient cost responsibility as copay or coinsurance",
                                       "plan_pay":"Payor cost responsibility",}
                            },
            "SCRIPT_DETAIL_TABLE":{"description":"This table provides ingredient, company, and categorical detail for all FDA National Drug Codes (NDCs).",   
                           "queries":["scriptDetail"], 
                           "features":{"ndc":"FDA standardized National Drug Code 11 for a dispensed drug",
                                       "labeler":"A company or organization that is a manufacturer, repackager, relabeler, or distributor of drugs",
                                       "product_type":"A classification of a drug product based on its intended use and how it is regulated by the FDA",
                                       "substance":"A substance is the active ingredient in a drug product",
                                       "substance_unit":"The unit of measurement for the active ingredient in a drug product",
                                       "dosage_form":"The type of pharmaceutical formulation, such as a tablet, capsule, liquid, or injection, that a drug product is available in",
                                       "route":"Method by which a drug product is administered to the body",
                                       "marketing_category":"A classification of a drug product based on its regulatory status and how it is marketed",
                                       "application_number":"A unique identifier for an NDC labeler's request to obtain an NDC labeler code",
                                       "pharm_classes":"A list of classifications of a drug product based on its therapeutic action, or how it works in the body",}
                            },
            "DRG_TABLE":{"description":"This table provides helpful context and categories around Diagnosis Related Groups (DRGs) for inpatient medical billing.",   
                           "queries":["drgDetail"], 
                           "features":{"drg_code":"Diagnosis related group (DRG) code. This code is based on your primary and secondary diagnoses, other conditions (comorbidities), age, sex, and necessary medical procedures",
                                       "drg_name":"Descriptive name of the DRG code",
                                       "drg_category":"Medical Diagnostic Category MDC of the DRG",
                                       "drg_type":"The type of diagnosis related group (DRG)",
                                       "drg_post_acute":"Binary indicator of whether a DRG is post acute or not",
                                       "drg_special":"Binary indicator of whether a DRG is a special condition - particularly complex or expensive conditions that  may require specialized care, longer hospital stays, and/or more expensive medications and procedures",
                                       "drg_weight":"Represents the relative resources required  to care for patients in that particular DRG. This CMS computed figure highlights a DRG's relative to the average resources used to treat cases in all other DRGs",
                                       "los_gmean":"The geometric mean length of stay corresponding to a DRG",
                                       "los_mean":"The arithmetic mean length of stay corresponding to a DRG",}
                            },
        }

queries = {"careEncounter":{"description" : "Specify encounter-based query parameters to construct a query object. From which the .execute() method on this query will return line-item level patient journey detail for healthcare encounters that meet the query criterion. We define an encoutner as a single, billiable healthcare instance of care.",
                            "parameters" : {"min_date" : "Lower threshold date within the date range of interest, observational start date",
                                            "max_date" : "Upper threshold date within the date range of interest, observational end date",
                                            "gender" : "Patient gender within the population of interest",
                                            "age_min" : "Minimum patient age identified within the population of interest",
                                            "age_max" : "Maximum patient age identified within the population of interest",
                                            "visit_type" : "Description of the setting of care",
                                            "payor_channel" : "Health Insurance Payor channel-of-business or line-of-business",
                                            "revenue_center_code" : "4-digit code used to identify a specific accommodation, ancillary service, or billing calculation on a hospital bill",
                                            "place_of_service" : "Setting in which a healthcare service was provided by healthcare providers, insurers, and government agencies to track and bill for healthcare services",
                                            "drg_code":"Diagnosis related group (DRG) code. This code is based on your primary and secondary diagnoses, other conditions (co-morbidities), age, sex, and necessary medical procedures.",
                                            "drg_category":"Medical Diagnostic Category (MDC) of the Diagnosis Related Group (DRG)",
                                            "drg_greedy":"Boolean indicator for 'AND' or 'OR' when multiple DRG parameters specified - helps users offer various levels of specificity without confusing and/or logic",
                                            "diag_code" : "ICD-10 diagnosis code assigned to the patient",
                                            "diag_category" : "ICD-10 diagnosis category assigned to the patient",
                                            "diag_subcategory" : "ICD-10 diagnosis subcategory assigned to the patient",
                                            "short_diag_code" : "First three digits of ICD-10 code assigned to the patient",
                                            "diag_greedy" : "Boolean indicator for 'AND' or 'OR' when multiple diagnosis parameters specified - helps users offer various levels of specificity without confusing and/or logic",
                                            "proc_code" : "CPT or HCPCS procedural code performed",
                                            "proc_category" : "CPT or HCPCS procedural category performed",
                                            "proc_subcategory" : "CPT or HCPCS procedural subcategory performed",
                                            "proc_greedy" : "Boolean indicator for 'AND' or 'OR' when multiple procedure parameters specified - helps users offer various levels of specificity without confusing and/or logic",
                                            "taxonomy_code" : "Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider",
                                            "specialty" : "Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy",
                                            "specialty_category" : "Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy",
                                            "subspecialty" : "Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy",
                                            "taxonomy_greedy" : "Boolean indicator for 'AND' or 'OR' when multiple taxonomy or specialty parameters specified - helps users offer various levels of specificity without confusing and/or logic",
                                            "ref_npi":"Referring provider(s) indicated by National Provider Identifiers (NPIs)",
                                            "npi":"National Provider Identifier (NPI) of individual and organizational provider(s) of interest",
                                            "state":"US State residence of the query patient population",
                                            "division":"Nine distinct US State groupings as defined by the US Census Bureau",
                                            "region":"Four major US State groupings as defined by the US Census Bureau - Northeast, Midwest, South and West",
                                            "metro":"Metropolitan and micropolitan statistical areas according to the US Census Bureau",
                                            "short_zip":"First three digits the zip code of the query patient population specified",
                                            "limit":"Number of rows returned in the data request.",
                                            "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself."}
                        },
            "careVisit":{"description" : "Visit-based query that returns line-item level patient journey detail for healthcare visits that meet the query criterion. We define a visit as group of encounters within the same event of of care.",
                            "parameters" : {"min_date" : "Lower threshold date within the date range of interest, observational start date",
                                            "max_date" : "Upper threshold date within the date range of interest, observational end date",
                                            "gender" : "Patient gender within the population of interest",
                                            "age_min" : "Minimum patient age identified within the population of interest",
                                            "age_max" : "Maximum patient age identified within the population of interest",
                                            "visit_type" : "Description of the setting of care",
                                            "payor_channel" : "Health Insurance Payor channel-of-business or line-of-business",
                                            "revenue_center_code" : "4-digit code used to identify a specific accommodation, ancillary service, or billing calculation on a hospital bill",
                                            "place_of_service" : "Setting in which a healthcare service was provided by healthcare providers, insurers, and government agencies to track and bill for healthcare services",
                                            "diag_code" : "ICD-10 diagnosis code assigned to the patient",
                                            "diag_category" : "ICD-10 diagnosis category assigned to the patient",
                                            "diag_subcategory" : "ICD-10 diagnosis subcategory assigned to the patient",
                                            "short_diag_code" : "First three digits of ICD-10 code assigned to the patient",
                                            "diag_greedy" : "Boolean indicator for 'AND' or 'OR' when multiple diagnosis parameters specified - helps users offer various levels of specificity without confusing and/or logic",
                                            "proc_code" : "CPT or HCPCS procedural code performed",
                                            "proc_category" : "CPT or HCPCS procedural category performed",
                                            "proc_subcategory" : "CPT or HCPCS procedural subcategory performed",
                                            "proc_greedy" : "Boolean indicator for 'AND' or 'OR' when multiple procedure parameters specified - helps users offer various levels of specificity without confusing and/or logic",
                                            "taxonomy_code" : "Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider",
                                            "specialty" : "Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy",
                                            "specialty_category" : "Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy",
                                            "subspecialty" : "Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy",
                                            "taxonomy_greedy" : "Boolean indicator for 'AND' or 'OR' when multiple taxonomy or specialty parameters specified - helps users offer various levels of specificity without confusing and/or logic",
                                            "ref_npi":"Referring provider(s) indicated by National Provider Identifiers (NPIs)",
                                            "npi":"National Provider Identifier (NPI) of individual and organizational provider(s) of interest",
                                            "state":"US State residence of the query patient population",
                                            "division":"Nine distinct US State groupings as defined by the US Census Bureau",
                                            "region":"Four major US State groupings as defined by the US Census Bureau - Northeast, Midwest, South and West",
                                            "metro":"Metropolitan and micropolitan statistical areas according to the US Census Bureau",
                                            "short_zip":"First three digits the zip code of the query patient population specified",
                                            "limit":"Number of rows returned in the data request.",
                                            "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself."}
                            },
            "careEpisode":{"description" : "Episode-based query that returns line-item level patient journey detail for healthcare episodes that meet the query criterion. We define an episode as sequential group of encounters that occur within the 30 days from one another, in continuation, until greater than 30 days has elapsed.",
                            "parameters" : {"min_date" : "Lower threshold date within the date range of interest, observational start date",
                                            "max_date" : "Upper threshold date within the date range of interest, observational end date",
                                            "gender" : "Patient gender within the population of interest",
                                            "age_min" : "Minimum patient age identified within the population of interest",
                                            "age_max" : "Maximum patient age identified within the population of interest",
                                            "visit_type" : "Description of the setting of care",
                                            "payor_channel" : "Health Insurance Payor channel-of-business or line-of-business",
                                            "revenue_center_code" : "4-digit code used to identify a specific accommodation, ancillary service, or billing calculation on a hospital bill",
                                            "place_of_service" : "Setting in which a healthcare service was provided by healthcare providers, insurers, and government agencies to track and bill for healthcare services",
                                            "diag_code" : "ICD-10 diagnosis code assigned to the patient",
                                            "diag_category" : "ICD-10 diagnosis category assigned to the patient",
                                            "diag_subcategory" : "ICD-10 diagnosis subcategory assigned to the patient",
                                            "short_diag_code" : "First three digits of ICD-10 code assigned to the patient",
                                            "diag_greedy" : "Boolean indicator for 'AND' or 'OR' when multiple diagnosis parameters specified - helps users offer various levels of specificity without confusing and/or logic",
                                            "proc_code" : "CPT or HCPCS procedural code performed",
                                            "proc_category" : "CPT or HCPCS procedural category performed",
                                            "proc_subcategory" : "CPT or HCPCS procedural subcategory performed",
                                            "proc_greedy" : "Boolean indicator for 'AND' or 'OR' when multiple procedure parameters specified - helps users offer various levels of specificity without confusing and/or logic",
                                            "taxonomy_code" : "Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider",
                                            "specialty" : "Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy",
                                            "specialty_category" : "Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy",
                                            "subspecialty" : "Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy",
                                            "taxonomy_greedy" : "Boolean indicator for 'AND' or 'OR' when multiple taxonomy or specialty parameters specified - helps users offer various levels of specificity without confusing and/or logic",
                                            "ref_npi":"Referring provider(s) indicated by National Provider Identifiers (NPIs)",
                                            "npi":"National Provider Identifier (NPI) of individual and organizational provider(s) of interest",
                                            "state":"US State residence of the query patient population",
                                            "division":"Nine distinct US State groupings as defined by the US Census Bureau",
                                            "region":"Four major US State groupings as defined by the US Census Bureau - Northeast, Midwest, South and West",
                                            "metro":"Metropolitan and micropolitan statistical areas according to the US Census Bureau",
                                            "short_zip":"First three digits the zip code of the query patient population specified",
                                            "limit":"Number of rows returned in the data request.",
                                            "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself."}
                        },
        "careJourney":{"description" : "Journey-based query that returns line-item level patient journey detail for healthcare patient journeys that meet the query criterion. We define a journey as a full longitudinal patient record, all encounters dating back to January 1st, 2019.",
                            "parameters" : {"min_date" : "Lower threshold date within the date range of interest, observational start date",
                                            "max_date" : "Upper threshold date within the date range of interest, observational end date",
                                            "gender" : "Patient gender within the population of interest",
                                            "age_min" : "Minimum patient age identified within the population of interest",
                                            "age_max" : "Maximum patient age identified within the population of interest",
                                            "visit_type" : "Description of the setting of care",
                                            "payor_channel" : "Health Insurance Payor channel-of-business or line-of-business",
                                            "revenue_center_code" : "4-digit code used to identify a specific accommodation, ancillary service, or billing calculation on a hospital bill",
                                            "place_of_service" : "Setting in which a healthcare service was provided by healthcare providers, insurers, and government agencies to track and bill for healthcare services",
                                            "diag_code" : "ICD-10 diagnosis code assigned to the patient",
                                            "diag_category" : "ICD-10 diagnosis category assigned to the patient",
                                            "diag_subcategory" : "ICD-10 diagnosis subcategory assigned to the patient",
                                            "short_diag_code" : "First three digits of ICD-10 code assigned to the patient",
                                            "diag_greedy" : "Boolean indicator for 'AND' or 'OR' when multiple diagnosis parameters specified - helps users offer various levels of specificity without confusing and/or logic",
                                            "proc_code" : "CPT or HCPCS procedural code performed",
                                            "proc_category" : "CPT or HCPCS procedural category performed",
                                            "proc_subcategory" : "CPT or HCPCS procedural subcategory performed",
                                            "proc_greedy" : "Boolean indicator for 'AND' or 'OR' when multiple procedure parameters specified - helps users offer various levels of specificity without confusing and/or logic",
                                            "taxonomy_code" : "Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider",
                                            "specialty" : "Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy",
                                            "specialty_category" : "Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy",
                                            "subspecialty" : "Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy",
                                            "taxonomy_greedy" : "Boolean indicator for 'AND' or 'OR' when multiple taxonomy or specialty parameters specified - helps users offer various levels of specificity without confusing and/or logic",
                                            "ref_npi":"Referring provider(s) indicated by National Provider Identifiers (NPIs)",
                                            "npi":"National Provider Identifier (NPI) of individual and organizational provider(s) of interest",
                                            "state":"US State residence of the query patient population",
                                            "division":"Nine distinct US State groupings as defined by the US Census Bureau",
                                            "region":"Four major US State groupings as defined by the US Census Bureau - Northeast, Midwest, South and West",
                                            "metro":"Metropolitan and micropolitan statistical areas according to the US Census Bureau",
                                            "short_zip":"First three digits the zip code of the query patient population specified",
                                            "limit":"Number of rows returned in the data request.",
                                            "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself."}
                        },
        "nppesDetail":{"description" : "Query to navigate the NPPES_TABLE, which sources monthly updates to the national provider database within the National Plan & Provider Enumeration System (NPPES) by CMS.",
                        "parameters" : {"npi":"National Provider Identifier (NPI) of individual and organizational provider(s) of interest",
                                        "taxonomy_code":"Taxonomy of the organization or individual providers, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider",
                                        "specialty":"Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy",
                                        "specialty_category":"Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy",
                                        "subspecialty":"Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy",
                                        "state":"US State of the provider's NPPES registered address",
                                        "division":"US State Division of the provider's NPPES registered address. There are nine distinct US State groupings as defined by the US Census Bureau",
                                        "region":"US State Region of the provider's NPPES registered address. There are four major US State groupings as defined by the US Census Bureau",
                                        "zip":"Primary zip code of the provider",
                                        "limit":"Number of rows returned in the data request",
                                        "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself."}
                        },
        "diagDetail":{"description" : "Query to specify the diagnosis parameters for additional context, categories and code ties from the DIAG_TABLE",
                        "parameters" : {"diag_code":"ICD-10 diagnosis code",
                                        "diag_category":"Name of the ICD-10 diagnosis category",
                                        "diag_subcategory":"Name of the ICD-10 diagnosis sub-category",
                                        "short_diag_code":"First three characters of the ICD-10 diagnosis code, corresponding to the diagnosis subcategory",
                                        "limit":"Number of rows returned in the data request",
                                        "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself"}
                        },
        "procDetail":{"description" : "Query to specify the procedure parameters for additional context, categories and code ties from the PROC_TABLE",
                        "parameters" : {"proc_code":"CPT/HCPCS procedural code",
                                        "proc_category":"Name of the CPT/HCPCS procedural category",
                                        "proc_subcategory":"Name of the CPT/HCPCS procedural sub-category",
                                        "limit":"Number of rows returned in the data request",
                                        "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself"}
                        },
        "specialtyDetail":{"description" : "Query to specify the taxonmy/specialty parameters for additional context, categories and code ties from the SPEC_TABLE",
                        "parameters" : {"taxonomy_code":"Taxonomy of organization or individual provider, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider",
                                        "subspecialty":"Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy",
                                        "specialty":"Specialty of organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy",
                                        "specialty_category":"Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy",
                                        "limit":"Number of rows returned in the data request",
                                        "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself"}
                        },
        "mipsDetail":{"description" : "Query to request Merit-based Incentive Payment System (MIPS) performance information for specified providers",
                        "parameters" : {"npi":"National Provider Identifier (NPI) assigned to the individual provider",
                                        "limit":"Number of rows returned in the data request",
                                        "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself"}
                        },
        "geoDetail":{"description" : "Query to specify geographic detail around zip, county, metro, state or region - including US Census population statistics at each level",
                        "parameters" : {"short_zip":"First three digits any valid ZIP code",
                                        "metro":"Metropolitan and micropolitan statistical areas according to the US Census Bureau",
                                        "state":"Two digit US State code(s)",
                                        "division":"Nine distinct US State groupings as defined by the US Census Bureau",
                                        "region":"Four major US State groupings as defined by the US Census Bureau",
                                        "limit":"Number of rows returned in the data request",
                                        "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself"}
                        },
        "execOutreach":{"description" : "Query to specify executive email, phone and address data - including context around their role and seniority.",
                        "parameters" : {"hospital":"Name of the primary hospital affiliated with the executive",
                                        "exec_level":"Adiministrative level associated with the executive's role",
                                        "department":"Functional department associated with the executive's role",
                                        "npi":"Where executive is a provider, their National Provider Identifier (NPI)",
                                        "state":"US State code of the executive record",
                                        "division":"US State Division code of the executive record",
                                        "region":"US State Region code of the executive record",
                                        "metro":"Metropolitan and micropolitan statistical areas according to the US Census Bureau",
                                        "short_zip":"First three digits of zip code for the executive record",
                                        "limit":"Number of rows returned in the data request",
                                        "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself"}
                        },
        "providerOutreach":{"description" : "Query to specify individual healthcare providers and their accompanying contact information, including email, phone and fax.",
                        "parameters" : {"npi":"National Provider Identifier (NPI) of individual and organizational provider record",
                                        "taxonomy_code":"Primary taxonomy code of the individual provider record",
                                        "subspecialty":"Subspecialty of the individual provider record",
                                        "specialty":"Specialty of the individual provider record",
                                        "specialty_category":"Specialty category of the individual provider record",
                                        "state":"US State code of the individual provider record",
                                        "division":"US State Division code of the individual provider record",
                                        "region":"US State Region code of the individual provider record",
                                        "metro":"Metropolitan and micropolitan statistical areas according to the US Census Bureau",
                                        "short_zip":"First three digits of zip code for the individual provider record",
                                        "limit":"Number of rows returned in the data request",
                                        "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself"}
                        },
         "affiliationActivity":{"description" : "Query to specify health system provider affiliation query parameters to return nuanced affiliation data, including the actual claims activity-by-affiliation for each provider",
                        "parameters" : {"npi":"National Provider Identifier (NPI) of individual and organizational provider record",
                                        "system":"Name of the system an individual provider may be affiliated with in any way - either indicated by overall affiliation, or via the system affiliation for any of the top 3 healthcare organization (hco) in which they practice at",
                                        "taxonomy_code":"Primary taxonomy code of the individual provider record",
                                        "subspecialty":"Subspecialty of the individual provider record",
                                        "specialty":"Specialty of the individual provider record",
                                        "specialty_category":"Specialty category of the individual provider record",
                                        "state":"US State code of the individual provider record",
                                        "division":"US State Division code of the individual provider record",
                                        "region":"US State Region code of the individual provider record",
                                        "lookback_period":"String indicating the quarter and year of the provider practice",
                                        "limit":"Number of rows returned in the data request",
                                        "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself"}
                        },
        "affiliationActivity":{"description" : "Query to update health system and provider affiliations given provider/system parameters given",
                        "parameters" : {"system":"Name of the system an individual provider may be affiliated with in any way - either indicated by overall affiliation, or via the system affiliation for any of the top 3 healthcare organization (hco) in which they practice at",
                                        "add_npi":"National Provider Identifier (NPI) an individual and/or organizational provider(s) with which you would like to ADD to the affiliation list of the system specified",
                                        "remove_npi":"National Provider Identifier (NPI) an individual and/or organizational provider(s) with which you would like to REMOVE from the affiliation list of the system specified",
                                        "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself"}
                        },
        "procAllowedAvgs":{"description" : "Query to specify procedure-encounter-based criterion and return statistical data around healthcare claim allowed amounts.",
                            "parameters" : {"visit_type" : "Description of the setting of care",
                                            "payor_channel" : "Health Insurance Payor channel-of-business or line-of-business",
                                            "proc_code" : "CPT or HCPCS procedural code performed",
                                            "proc_category" : "CPT or HCPCS procedural category performed",
                                            "proc_subcategory" : "CPT or HCPCS procedural subcategory performed",
                                            "state":"US State residence of the query patient population",
                                            "division":"Nine distinct US State groupings as defined by the US Census Bureau",
                                            "region":"Four major US State groupings as defined by the US Census Bureau - Northeast, Midwest, South and West",
                                            "limit":"Number of rows returned in the data request.",
                                            "show":"Binary indicator as to whether you'd like your query to be printed for review upon it's creation. Regardless, this summary may be accessed via the .summarize(show=True) method on the query object itself."}
                        },
        "scriptEncounter":{"description" : "Query patient prescription claims that meet the specified criterion with line item detail",
                            "parameters" : {"min_date":"Lower threshold date within the date range of interest, observational start date",
                                            "max_date":"Upper threshold date within the date range of interest, observational end date",
                                            "":"",
                                            "gender":"Patient gender within the population of interest",
                                            "age_min":"Minimum patient age identified within the population of interest",
                                            "age_max":"Maximum patient age identified within the population of interest",
                                            "ndc":"FDA National Drug Code version 11 standardized code for a dispensed drug",
                                            "pharm_class":"Classifications of a drug product based on its therapeutic action, or how it works in the body",
                                            "substance":"The active ingredient in a drug product",
                                            "marketing_category":"Classification of a drug product based on its regulatory status and how it is marketed",
                                            "taxonomy_code":"Taxonomy of the organization or individual provider, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider",
                                            "specialty":"Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy",
                                            "specialty_category":"Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy",
                                            "subspecialty":"Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy",
                                            "npi":"National Provider Identifier (NPI) of individual and/or organizational provider(s) that appear on the encounter",
                                            "state":"US State residence of the query patient population",
                                            "division":"Nine distinct US State groupings as defined by the US Census Bureau",
                                            "region":"Four major US State groupings as defined by the US Census Bureau",
                                            "metro":"Metropolitan and micropolitan statistical  \nareas according to the US Census Bureau",
                                            "short_zip":"First three digits the zip code of the  \nquery patient population specified",
                                            "limit":"Number of rows returned in the data request",
                                            "show":"Binary indicator as to whether you'd like  \nquery to be printed for review upon it's creation"}
                        },
        "scriptJourney":{"description" : "Query patient's full prescription claims history with line item detail, by specifying ANY and ALL prescription parameters where criterion are met across the entire journey",
                            "parameters" : {"min_date":"Lower threshold date within the date range of interest, observational start date",
                                            "max_date":"Upper threshold date within the date range of interest, observational end date",
                                            "gender":"Patient gender within the population of interest",
                                            "age_min":"Minimum patient age identified within the population of interest",
                                            "age_max":"Maximum patient age identified within the population of interest",
                                            "ndc":"FDA National Drug Code version 11 standardized code for a dispensed drug",
                                            "pharm_class":"Classifications of a drug product based on its therapeutic action, or how it works in the body",
                                            "substance":"The active ingredient in a drug product",
                                            "marketing_category":"Classification of a drug product based on its regulatory status and how it is marketed",
                                            "taxonomy_code":"Taxonomy of the organization or individual provider, 10-digit code that used to identify the type, classification, and area of specialization of an individual or organizational healthcare provider",
                                            "specialty":"Specialty of the organization or individual provider(s), specific focus of a provider by patient population, disease, skill or philosophy",
                                            "specialty_category":"Specialty category of the organization or individual provider(s), broad focus of a provider by patient population, disease, skill or philosophy",
                                            "subspecialty":"Specialty subcategory of the organization or individual provider(s), hyper-specific focus of a provider by patient population, disease, skill or philosophy",
                                            "npi":"National Provider Identifier (NPI) of individual and/or organizational provider(s) that appear on the encounter",
                                            "state":"US State residence of the query patient population",
                                            "division":"Nine distinct US State groupings as defined by the US Census Bureau",
                                            "region":"Four major US State groupings as defined by the US Census Bureau",
                                            "metro":"Metropolitan and micropolitan statistical  \nareas according to the US Census Bureau",
                                            "short_zip":"First three digits the zip code of the  \nquery patient population specified",
                                            "limit":"Number of rows returned in the data request",
                                            "show":"Binary indicator as to whether you'd like  \nquery to be printed for review upon it's creation"}
                        },
        "scriptDetail":{"description" : "Query prescription details such as active ingredient, company labeler, and categorical details for all FDA National Drug Codes (NDCs).",
                            "parameters" : {"ndc":"FDA National Drug Code version 11 standardized code for a dispensed drug",
                                            "pharm_class":"Classifications of a drug product based on its therapeutic action, or how it works in the body",
                                            "substance":"The active ingredient in a drug product",
                                            "marketing_category":"Classification of a drug product based on its regulatory status and how it is marketed",
                                            "limit":"Number of rows returned in the data request",
                                            "show":"Binary indicator as to whether you'd like  \nquery to be printed for review upon it's creation"}
                        },
        "drgDetail":{"description" : "Query to specify data request for all Diagnosis Related Group (DRG) parameters for additional context and categories.",
                            "parameters" : {"drg_code":"Diagnosis related group (DRG) code. This code is based on your primary and secondary diagnoses, other conditions (co-morbidities), age, sex, and necessary medical procedures.",
                                            "drg_category":"Medical Diagnostic Category (MDC) of the Diagnosis Related Group (DRG)",
                                            "limit":"Number of rows returned in the data request",
                                            "show":"Binary indicator as to whether you'd like  \nquery to be printed for review upon it's creation"}
                        },
        }

### Table Feature Data Class ###
class DataGlossary:

    def __init__(self):
        
        self.tables = tables
        self.queries = queries

        # read field value json - move to CQ_Class or CQUtils
        # #TODO: Uncomment and use this for local testing
        # with open('field-values.json', 'r') as f:
        #     self.parameter_options = json.load(f)

        # TODO: Use this for the pypi distro
        with importlib.resources.open_text('care_query', 'field-values.json') as f:
            self.parameter_options = json.load(f)


    def list_tables(self):

        listed = list(self.tables.keys())

        return listed
    
    def list_queries(self):

        listed = list(self.queries.keys())

        return listed
    
    def list_parameters(self, query):

        listed = self.queries[query]["parameters"]

        return listed
    
    def list_options(self, parameter, contains = None):

        try:
            if type(self.parameter_options[parameter]) == dict:
                listed = list(self.parameter_options[parameter].keys())
                if contains != None:
                    listed = [x for x in listed if contains in str(x).lower()]
            elif type(self.parameter_options[parameter]) == list:
                listed = self.parameter_options[parameter]
                if contains != None:
                    listed = [x for x in listed if contains in str(x).lower()]
            else:
                listed = []
            if (len(listed) == 0) & (contains != None):
                print("No parameter options meet the contains critera.")
        except:
            raise ValueError(f"""ValueError: {parameter} parameter Not Found. Run self.list_parameters("name of query") to see all parameter options""")

        return listed
    
    def parameter_detail(self, parameter, as_pandas = None):
        
        try:
            detail = self.parameter_options[parameter]
            # if as_pandas != False:
            #     print(pd.DataFrame.from_dict(detail))
            #     #detail.columns = ["parameter","options"]
        except:
            raise ValueError(f"""ValueError: {parameter} parameter Not Found. Run self.list_parameters("name of query") to see all parameter options""")
        
        return detail

    def table_detail(self, table):

        try:
            detail = self.tables[table]
        except:
            raise ValueError(f"ValueError: {table} table Not Found. Run self.list_tables() to see all table options")

        return detail

    def feature_detail(self, table):

        try:
            detail = self.tables[table]["features"]
        except:
            raise ValueError(f"ValueError: {table} table Not Found. Run self.list_tables() to see all table options")

        return detail

    def query_detail(self, query):

        try:
            detail = self.queries[query]
        except:
            raise ValueError(f"ValueError: {query} method Not Found. Run self.list_methods() to see all method options")

        return detail
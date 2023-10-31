from nyc_bias_audit import NYCBiasAudit

config = {
    "tenant_id": "",
    "apikey": "",
}

audit = NYCBiasAudit(config)

data_onboard_system = {
    "system_id": "",                    # left empty will create a new system, otherwise will update
    "system_info": {
        "system_name": "",
        "company_description": "",
        "system_short_description": "", # description displayed in Trust
        "system_long_description": "",  # description required for the report
        "key_information": "",
        "distribution_date": "",        # deployment date
        "system_type": "",              # CONTINUOUS or BINARY, we can probably get it from the data
        "deployment_type": "",          # {COMPANY} - for 3rd party, "JOB_TYPE", "PREDICTOR", "ASSESSMENT"
        "team_information": [{
            "name": "",
            "email": "",
            "role": ""
        }]
    }
}

system_id = audit.onboard_system(data_onboard_system)

data_run_bias_audit = {
    "system_id": "",                    # the id of the system for which you want to run teh audit
    "data_information": {
        "data_type": [],                # historical, test
        "data_region": "",              # EU, US, New York
        "data_size": 0,                 # the size of the data submitted
        "period_start": "",             # data period start
        "period_end": "",               # data period end
        "description": "",              # for data_type == historical
        "test_description": "",         # if data_type == test as well
        "protected_characteristics": [] # Gender, Ethnicity, Disability or Age
    },
    "data_options": {                   # any special operations that needs to be applied?
        "scaling": {
            "type": "",                 # NO_SCALING, STANDARD, REGRESSION
            "scaling_columns": []       # deployment_id or job_id usually
        }
    },
    "data": [{                          # If the data was a csv, then each on the following fields
        "deployment_id": "",            # will be the columns of that csv.
        "job_id": "",                   #
        "gender": "",                   # Out of the 4 (gender, ethnicity, disability, age) only the
        "ethnicity": "",                # ones marked in protected_characteristics above shoould be
        "disability": "",               # filled out.
        "age": "",
        "score": ""
    }],
    "audit_date": "",                   # if empty, it will use the current date of the run
}

audit.run_bias_audit(data_run_bias_audit)

systems = audit.get_systems()

systems_example = [
  {
    "system_id": "",
    "system_name": ""
  },
  {
    "system_id": "",
    "system_name": ""
  },
  {
    "system_id": "",
    "system_name": ""
  }
]

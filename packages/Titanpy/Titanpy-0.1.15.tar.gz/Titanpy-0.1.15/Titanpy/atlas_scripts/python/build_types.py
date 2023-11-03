# This script contains functions that Atlas uses to created different types of source datasets and initializes the database using sqlalchemy.

def Default(sql_creds_path, st_creds_path, start_date = None):
    
    from .database_tools import create_engine, run_sql
    from .titanpy_tools import titanpy_dataframe
    
    endpoint_list = [
        # 'export/inventory-bills',
        'export/invoice-items',
        'export/invoices',
        'export/payments',
        'export/bookings',
        'export/customers',
        'export/customers/contacts',
        'export/leads',
        'export/locations',
        'export/locations/contacts',
        'export/appointment-assignments',
        'export/purchase-orders',
        'export/appointments',
        'export/job-canceled-logs',
        'export/jobs',
        'export/projects',
        'export/invoice-templates',
        'export/membership-types',
        'export/memberships',
        'export/recurring-service-events',
        'export/recurring-service-types',
        'export/recurring-services',
        'export/activity-codes',
        'export/gross-pay-items',
        'export/jobs/splits',
        'export/jobs/timesheets',
        'export/payroll-adjustments',
        'export/timesheet-codes',
        'export/business-units',
        'export/employees',
        'export/tag-types',
        'export/technicians',
    ]

    engine = create_engine(sql_creds_path)

    print("\n------------------ Initializing Default Atlas Schema -------------------")
    import os
    this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, "../sql/create_atlas_schema.sql")
    run_sql(engine, DATA_PATH)
    print("\nAtlas Schema Initialized")
    print("\n------------------ Getting Servicetitan Data ---------------------------\n")
    df_dict = titanpy_dataframe(engine, endpoint_list, st_creds_path, start_date=start_date)
    print("\n------- Succesfully Created/Updated Default Atlas Source Tables! -------\n")


if __name__ == "__main__":
    Default("./credentials/postgresql_credentials.json", "./credentials/servicetitan_credentials.json", start_date='2023-11-01')

def get_request(credentials, query, url):
    
    import requests

    auth = {
        "ST-App-Key": credentials["APP_KEY"],
        "Authorization": credentials["ACCESS_TOKEN"]
    }
    print(f"(Requesting from {url})")
    default_query_parameters = {
    }
    if query != None:
        for request in query:
            default_query_parameters[request] = query[request]
    try:
        request = requests.get(url=url,params=default_query_parameters, headers=auth)
        return request
    except Exception as e:
        print(f"There was an error getting data from {url}")
        print(e)

def get(credentials, endpoint, query, id, category, *args, **kwargs):

    general_urls = {
        "url": "https://api.servicetitan.io/",
        "accounting_url_tenant": f"https://api.servicetitan.io/accounting/v2/tenant/{credentials['TENANT_ID']}/",
        "reporting_url_tenant": f"https://api.servicetitan.io/reporting/v2/tenant/{credentials['TENANT_ID']}/",
        "forms_url_tenant":f"https://api.servicetitan.io/forms/v2/tenant/{credentials['TENANT_ID']}/",
        "crm_url_tenant":f"https://api.servicetitan.io/crm/v2/tenant/{credentials['TENANT_ID']}/",
        "dispatch_url_tenant":f"https://api.servicetitan.io/dispatch/v2/tenant/{credentials['TENANT_ID']}/",
        "installed_systems_url_tenant":f"https://api.servicetitan.io/equipmentsystems/v2/tenant/{credentials['TENANT_ID']}/",
        "inventory_url_tenant":f"https://api.servicetitan.io/inventory/v2/tenant/{credentials['TENANT_ID']}/",
        "job_booking_url_tenant":f"https://api.servicetitan.io/jbce/v2/tenant/{credentials['TENANT_ID']}/",
        "job_planning_url_tenant": f"https://api.servicetitan.io/jpm/v2/tenant/{credentials['TENANT_ID']}/",
        "marketing_url_tenant": f"https://api.servicetitan.io/marketing/v2/tenant/{credentials['TENANT_ID']}/",
        "marketing_reputation_url_tenant": f"https://api.servicetitan.io/marketingreputation/v2/tenant/{credentials['TENANT_ID']}/",
        "memberships_url_tenant": f"https://api.servicetitan.io/memberships/v2/tenant/{credentials['TENANT_ID']}/",
        "payroll_url_tenant": f"https://api.servicetitan.io/payroll/v2/tenant/{credentials['TENANT_ID']}/",
        "pricebook_url_tenant": f"https://api.servicetitan.io/pricebook/v2/tenant/{credentials['TENANT_ID']}/",
        "estimates_url_tenant": f"https://api.servicetitan.io/sales/v2/tenant/{credentials['TENANT_ID']}/",
        "service_agreements_url_tenant": f"https://api.servicetitan.io/service-agreements/v2/tenant/{credentials['TENANT_ID']}/",
        "settings_url_tenant": f"https://api.servicetitan.io/settings/v2/tenant/{credentials['TENANT_ID']}/",
        "task_management_url_tenant": f"https://api.servicetitan.io/taskmanagement/v2/tenant/{credentials['TENANT_ID']}/",
        "telecom_url_tenant": f"https://api.servicetitan.io/telecom/v2/tenant/{credentials['TENANT_ID']}/",
        "telecom_url_v3_tenant": f"https://api.servicetitan.io/telecom/v3/tenant/{credentials['TENANT_ID']}/",
    }

    # --------- ENDPOINT GROUPS --------- #

    # Accounting
    accounting_endpoints = [
        'export/inventory-bills',
        'export/invoice-items',
        'export/invoices',
        'export/payments',
        'ap-credits',
        'ap-payments',
        'inventory-bills',
        'invoices',
        'journal-entries',
        'payments',
        'payment-terms',
        'tax-zones',
    ]
    accounting_id_endpoints = [
        'journal-entries-details/',
        'journal-entries-summary/',
        'payment-types/',
    ]

    # CRM
    crm_endpoints = [
        'export/bookings',
        'export/customers',
        'export/customers/contacts',
        'export/leads',
        'export/locations',
        'export/locations/contacts',
        'booking-provider-tags',
        'bookings',
        'customers',
        'customers/contacts',
        'leads',
        'locations',
        'locations/contacts',
    ]
    crm_id_endpoints = [
        'booking-provider-tags/',
        '/bookings',
        '/bookings/',
        '/bookings-contacts/',
        'bookings/',
        'bookings-contacts/',
        'customers/',
        'customers-contacts/',
        'customers-notes/',
        'leads/',
        'leads-notes/',
        'locations/',
        'locations-contacts/',
        'locations-notes/',
    ]

    # Dispatch
    dispatch_endpoints = [
        'export/appointment-assignments',
        'appointment_assignments',
        'non-job-appointments',
        'teams',
        'technician-shifts',
        'zones',
    ]
    dispatch_id_endpoints = [
        'non-job-appointments/',
        'teams/',
        'technician-shifts/',
        'zones/',
    ]

    # Installed Systems
    installed_systems_endpoints = [
        'installed-equipment',
    ]
    installed_systems_id_endpoints = [
        'installed-equipment/',
    ]

    # Forms
    forms_endpoints = [
        'forms',
        'submissions',
    ]

    # Inventory
    inventory_endpoints = [
        'export/purchase-orders',
        'adjustments',
        'purchase-orders',
        'purchase-order-markups',
        'purchase-order-types',
        'receipts',
        'returns',
        'transfers',
        'trucks',
        'vendors',
        'warehouses',
    ]
    inventory_id_endpoints = [
        'purchase-orders/',
        'purchase-order-markups/',
        'vendors/',
    ]

    # Job Booking
    job_booking_endpoints = [
        'call-reasons',
    ]

    # Job Planning and Management
    job_planning_endpoints = [
        'export/appointments',
        'export/job-canceled-logs',
        'export/jobs',
        'export/projects',
        'appointments',
        'job-cancel-reasons',
        'job-hold-reasons',
        'jobs',
        'job-types',
        'projects',
        'project-statuses',
        'project-substatuses',
    ]
    job_planning_id_endpoints = [
        'appointments/',
        'jobs-cancel-reasons//',
        'jobs/',
        'jobs-history/',
        'jobs-notes/',
        'job-types/',
        'projects/',
        'projects-notes/',
        'project-statuses/',
        'project-substatuses/',
    ]

    # Marketing
    marketing_endpoints = [
        'categories',
        'costs',
        'campaigns',
        'suppressions',
    ]
    marketing_id_endpoints = [
        'categories/',
        'costs/',
        'campaigns/',
        'campaigns-costs/',
        'suppressions/',
    ]

    # Marketing Reputation
    marketing_reputation_endpoints = [
        'reviews',
    ]

    # Memberships Endpoints
    memberships_endpoints = [
        'export/invoice-templates',
        'export/membership-types',
        'export/memberships',
        'export/recurring-service-events',
        'export/recurring-service-types',
        'export/recurring-services',
        'memberships',
        'recurring-service-events',
        'recurring-services',
        'membership-types',
        'recurring-service-types',

    ]
    memberships_id_endpoints = [
        'memberships/',
        'memberships-status-changes/',
        'invoice-templates/',
        'invoice-templates//',
        'recurring-services/',
        'membership-types/',
        'membership-types-discounts/',
        'membership-types-duration-billing-items/',
        'membership-types-recurring-service-items/',
        'recurring-service-types/',
    ]

    # Payroll
    payroll_endpoints = [
        'export/activity-codes',
        'export/gross-pay-items',
        'export/jobs/splits',
        'export/jobs/timesheets',
        'export/payroll-adjustments',
        'export/timesheet-codes',
        'activity-codes',
        'gross-pay-items',
        'jobs/splits',
        'locations/rates',
        'payroll-adjustments',
        'payrolls',
        'timesheet-codes',
        'jobs/timesheets',
        'non-job-timesheets',
    ]
    payroll_id_endpoints = [
        'activity-codes/',
        'jobs-splits/',
        'payroll-adjustments/',
        'employees-payrolls/',
        'technicians-payrolls/',
        'timesheet-codes/',
        'jobs-timesheets/',
    ]

    # Pricebook
    pricebook_endpoints = [
        'categories',
        'discounts-and-fees',
        'equipment',
        'images',
        'materials',
        'materialsmarkup',
        'services',
    ]
    pricebook_id_endpoints = [
        'categories/',
        'discounts-and-fees/',
        'equipment/',
        'materials/',
        'materialsmarkup/',
        'services/',
    ]

    # Reporting
    reporting_endpoints = [
        'report-categories',
    ]
    reporting_id_endpoints = [
        'dynamic-value-sets/',
        '/reports',
        '/reports/',
    ]

    # Sales/Estimates
    estimates_endpoints = [
        'estimates/export',
        'estimates',
        'estimates/items',
    ]
    estimates_id_endpoints = [
        'estimates/',
    ]

    # Service Agreements
    service_agreements_endpoints = [
        'export/service-agreements',
        'service-agreements',
    ]
    service_agreements_id_endpoints = [
        'service-agreements/',
    ]

    # Settings
    settings_endpoints = [
        'export/business-units',
        'export/employees',
        'export/tag-types',
        'export/technicians',
        'business_units',
        'employees',
        'tag-types',
        'technicians',
        'user-roles',
    ]
    settings_id_endpoints = [
        'business_units/',
        'employees/',
        'technicians/',
    ]

    # Task Management
    task_management_endpoints = [
        'data',
    ]

    # Telecom
    telecom_endpoints = [
        'export/calls',
    ]
    telecom_v3_endpoints = [
        'calls',
    ]
    telecom_id_endpoints = [
        'calls/',
        'calls-recording/',
        'calls-voicemail/',
    ]

    # --------- AVAILABLE ENDPOINTS --------- #

    available_endpoints = [
    ]
    available_endpoint_groups = [
        accounting_endpoints,
        accounting_id_endpoints,
        reporting_endpoints,
        reporting_id_endpoints,
        forms_endpoints,
        crm_endpoints,
        crm_id_endpoints,
        dispatch_endpoints,
        dispatch_id_endpoints,
        installed_systems_endpoints,
        installed_systems_id_endpoints,
        inventory_endpoints,
        inventory_id_endpoints,
        job_booking_endpoints,
        job_planning_endpoints,
        job_planning_id_endpoints,
        marketing_endpoints,
        marketing_id_endpoints,
        marketing_reputation_endpoints,
        memberships_endpoints,
        memberships_id_endpoints,
        payroll_endpoints,
        payroll_id_endpoints,
        pricebook_endpoints,
        pricebook_id_endpoints,
        estimates_endpoints,
        estimates_id_endpoints,
        service_agreements_endpoints,
        service_agreements_id_endpoints,
        settings_endpoints,
        settings_id_endpoints,
        task_management_endpoints,

    ]
    for group in available_endpoint_groups:
        available_endpoints.extend(group)

    # --------- ENDPOINT TESTS --------- #

    # Tests if endpoint has been manually added or not.
    if endpoint in available_endpoints:

        # Accounting Endpoints

        if endpoint in accounting_endpoints:
            url = f"{general_urls['accounting_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)

        if endpoint in accounting_id_endpoints:
            if endpoint == 'journal-entries-details/':
                if id != None:
                    url = f"{general_urls['accounting_url_tenant']}journal-entries/{id}/details"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint == 'journal-entries-summary/':
                if id != None:
                    url = f"{general_urls['accounting_url_tenant']}journal-entries/{id}/summary"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint == 'payment-types/':
                if id != None:
                    url = f"{general_urls['accounting_url_tenant']}payment-types/{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
        
        # CRM Endpoints
        
        if endpoint in crm_endpoints:
            url = f"{general_urls['crm_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)

        if endpoint in crm_id_endpoints:
            
            if endpoint in ['booking-provider-tags/', 'bookings/', 'customers/','leads/','locations/']:
                if id != None:
                    url = f"{general_urls['crm_url_tenant']}{endpoint}{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

            if endpoint in ['/bookings']:
                if category != None:
                    url = f"{general_urls['crm_url_tenant']}{category}{endpoint}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an Category in order to run. Please enter category as an arg.")
            
            if endpoint in ['/bookings/',]:
                if category != None and id != None:
                    url = f"{general_urls['crm_url_tenant']}{category}{endpoint}{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID and a Category in order to run. Please enter id and category as an arg.")

            if endpoint == '/bookings-contacts/':
                if category != None and id != None:
                    url = f"{general_urls['crm_url_tenant']}{category}/bookings/{id}/contacts"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID and a Category in order to run. Please enter id and category as an arg.")

            if endpoint == 'bookings-contacts/':
                if id != None:
                    url = f"{general_urls['crm_url_tenant']}bookings/{id}/contacts"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

            if endpoint == 'customers-contacts/':
                if id != None:
                    url = f"{general_urls['crm_url_tenant']}customers/{id}/contacts"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

            if endpoint == 'customers-notes/':
                if id != None:
                    url = f"{general_urls['crm_url_tenant']}customers/{id}/notes"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

            if endpoint == 'leads-notes/':
                if id != None:
                    url = f"{general_urls['crm_url_tenant']}leads/{id}/notes"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

            if endpoint == 'locations-contacts/':
                if id != None:
                    url = f"{general_urls['crm_url_tenant']}locations/{id}/contacts"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

            if endpoint == 'locations-notes/':
                if id != None:
                    url = f"{general_urls['crm_url_tenant']}locations/{id}/notes"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

        # Dispatch Endpoints

        if endpoint in dispatch_endpoints:
            url = f"{general_urls['dispatch_url_tenant']}{endpoint}"
            return get_request(credentials,query,url)
        
        if endpoint in ['non-job-appointments/','teams/','technician-shifts/','zones/']:
            if id != None:
                url = f"{general_urls['dispatch_url_tenant']}{endpoint}{id}"
                return get_request(credentials,query,url)
            else:
                print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

        # Installed Systems Endpoints
        
        if endpoint in installed_systems_endpoints:
            url = f"{general_urls['installed_systems_url_tenant']}{endpoint}"
            return get_request(credentials,query,url)
        
        if endpoint in ['installed-equipment/',]:
            if id != None:
                url = f"{general_urls['installed_systems_url_tenant']}{endpoint}{id}"
                return get_request(credentials,query,url)
            else:
                print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

        # Forms Endpoints
        
        if endpoint in forms_endpoints:
            url = f"{general_urls['forms_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)

        # Inventory Endpoints

        if endpoint in inventory_endpoints:
            url = f"{general_urls['inventory_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)

        if endpoint in ['purchase-orders/','purchase-order-markups/','vendors/']:
            if id != None:
                url = f"{general_urls['inventory_url_tenant']}{endpoint}{id}"
                return get_request(credentials,query,url)
            else:
                print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

        # Job Booking Endpoints

        if endpoint in job_booking_endpoints:
            url = f"{general_urls['job_booking_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)

        # Job Planning Endpoints

        if endpoint in job_planning_endpoints:
            url = f"{general_urls['job_planning_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)       

        if endpoint in job_planning_id_endpoints:
            
            if endpoint in ['appointments/','jobs/','job-types/','projects/','project-statuses/','project-substatuses/']:
                if id != None:
                    url = f"{general_urls['job_planning_url_tenant']}{endpoint}{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint in ['job-cancel-reasons//']:
                if id != None:
                    url = f"{general_urls['job_planning_url_tenant']}jobs/cancel-reasons?ids={id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires IDs in order to run. Please enter ids as an arg.")
            if endpoint in ['jobs-history/']:
                if id != None:
                    url = f"{general_urls['job_planning_url_tenant']}jobs/{id}/history"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint in ['jobs-notes/']:
                if id != None:
                    url = f"{general_urls['job_planning_url_tenant']}jobs/{id}/notes"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint in ['projects-notes/']:
                if id != None:
                    url = f"{general_urls['job_planning_url_tenant']}projects/{id}/notes"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

        # Marketing Endpoints

        if endpoint in marketing_endpoints:
            url = f"{general_urls['marketing_url_tenant']}{endpoint}"
            return get_request(credentials, query, url) 
        
        if endpoint in marketing_id_endpoints:
            if endpoint in ['categories/','costs/','campaigns/','suppressions/']:
                if id != None:
                    url = f"{general_urls['marketing_url_tenant']}{endpoint}{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg. (Email is considered and ID for suppressions/ endpoints.)")
            if endpoint in ['campaigns-costs/']:
                if id != None:
                    url = f"{general_urls['marketing_url_tenant']}campaigns/{id}/costs"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
        
        # Marketing Reputation Endpoints

        if endpoint in marketing_reputation_endpoints:
            url = f"{general_urls['marketing_reputation_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)

        # Memberships Endpoints

        if endpoint in memberships_endpoints:
            url = f"{general_urls['memberships_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)
        
        if endpoint in memberships_id_endpoints:
            if endpoint in ['memberships/', 'invoice-templates/', 'recurring-services/', 'membership-types/', 'recurring-service-types/']:
                if id != None:
                    url = f"{general_urls['memberships_url_tenant']}{endpoint}{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint in ['memberships-status-changes/']:
                if id != None:
                    url = f"{general_urls['memberships_url_tenant']}memberships/{id}/status-changes"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint in ['invoice-templates//']:
                if id != None:
                    url = f"{general_urls['memberships_url_tenant']}invoice-templates?id={id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires IDs in order to run. Please enter ids as an arg.")
            if endpoint in ['membership-types-discounts/']:
                if id != None:
                    url = f"{general_urls['memberships_url_tenant']}membership-types/{id}/discounts"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint in ['membership-types-duration-billing-items/']:
                if id != None:
                    url = f"{general_urls['memberships_url_tenant']}membership-types/{id}/duration-billing-items"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint in ['membership-types-recurring-service-items/']:
                if id != None:
                    url = f"{general_urls['memberships_url_tenant']}membership-types/{id}/recurring-service-items"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

        # Payroll Endpoints

        if endpoint in payroll_endpoints:
            url = f"{general_urls['payroll_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)
        
        if endpoint in payroll_id_endpoints:
            if endpoint in ['activity-codes/', 'payroll-adjustments/', 'timesheet-codes/',]:
                if id != None:
                    url = f"{general_urls['memberships_url_tenant']}{endpoint}{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint in ['jobs-splits/']:
                if id != None:
                    url = f"{general_urls['memberships_url_tenant']}jobs/{id}/splits"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint in ['employees-payrolls/']:
                if id != None:
                    url = f"{general_urls['memberships_url_tenant']}employees/{id}/payrolls"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint in ['technicians-payrolls/']:
                if id != None:
                    url = f"{general_urls['memberships_url_tenant']}technicians/{id}/payrolls"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint in ['jobs-timesheets/']:
                if id != None:
                    url = f"{general_urls['memberships_url_tenant']}jobs/{id}/timesheets"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

        # Pricebook Endpoints

        if endpoint in pricebook_endpoints:
            url = f"{general_urls['pricebook_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)

        if endpoint in pricebook_id_endpoints:
            if endpoint in ['categories/', 'discounts-and-fees/', 'equipment/', 'materials/', 'materialsmarkup/', 'services/',]:
                if id != None:
                    url = f"{general_urls['pricebook_url_tenant']}{endpoint}{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

        # Reporting Endpoints

        if endpoint in reporting_endpoints:
            url = f"{general_urls['reporting_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)
        
        if endpoint in reporting_id_endpoints:
            if endpoint == 'dynamic-value-sets/':
                if id != None:
                    url = f"{general_urls['reporting_url_tenant']}dynamic-value-sets/{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint == '/reports':
                if category != None:
                    url = f"{general_urls['reporting_url_tenant']}report-category/{category}/reports"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an Category in order to run. Please enter category as an arg.")
            if endpoint == '/reports/':
                if id != None and category != None:
                    url = f"{general_urls['reporting_url_tenant']}report-category/{category}/reports/{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID and a Category in order to run. Please enter id and category as an arg.")

        # Sales/Estimates Endpoints

        if endpoint in estimates_endpoints:
            url = f"{general_urls['estimates_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)
        
        if endpoint in estimates_id_endpoints:
            if endpoint in ['estimates/',]:
                if id != None:
                    url = f"{general_urls['estimates_url_tenant']}{endpoint}{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
        
        # Service Agreement Endpoints

        if endpoint in service_agreements_endpoints:
            url = f"{general_urls['service_agreements_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)
        
        if endpoint in service_agreements_id_endpoints:
            if endpoint in ['service-agreements/',]:
                if id != None:
                    url = f"{general_urls['service_agreements_url_tenant']}{endpoint}{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

        # Settings Endpoints

        if endpoint in settings_endpoints:
            url = f"{general_urls['settings_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)
        
        if endpoint in settings_id_endpoints:
            if endpoint in ['business_units/', 'employees/', 'technicians/',]:
                if id != None:
                    url = f"{general_urls['settings_url_tenant']}{endpoint}{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

        # Task Management Endpoints

        if endpoint in task_management_endpoints:
            url = f"{general_urls['task_management_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)

        # Telecom Endpoints

        if endpoint in telecom_endpoints:
            url = f"{general_urls['telecom_url_tenant']}{endpoint}"
            return get_request(credentials, query, url)
        if endpoint in telecom_v3_endpoints:
            url = f"{general_urls['telecom_url_v3_tenant']}{endpoint}"
            return get_request(credentials, query, url)
        if endpoint in telecom_id_endpoints:
            if endpoint in ['calls/',]:
                if id != None:
                    url = f"{general_urls['telecom_url_tenant']}{endpoint}{id}"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint in ['calls-recording/',]:
                if id != None:
                    url = f"{general_urls['telecom_url_tenant']}calls/{id}/recording"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")
            if endpoint in ['calls-voicemail/',]:
                if id != None:
                    url = f"{general_urls['telecom_url_tenant']}calls/{id}/voicemail"
                    return get_request(credentials,query,url)
                else:
                    print("The requested endpoint requires an ID in order to run. Please enter id as an arg.")

    # Attempts to make a request to a general endpoint if it has not been manually added
    # TO-DO AI assisted url creation
    else:
        try:
            url = f"https://api.servicetitan.io/jpm/v2/tenant/{credentials['TENANT_ID']}/{endpoint}"
            return get_request(credentials, query, url)
        except Exception as e:
            print(f"There was an error getting data from {endpoint}. The endpoint was not found in our current available\
                  endpoint list and could not be interpretted automatically. Please submit a request for this endpoint.")
            print(e)
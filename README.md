# Azure Billing App for Elastic AppSearch

## Prerequisites

`pip install requests elastic-enterprise-search xmltodict`

## How it works ?

There are 2 ways to configure the application:

   1. Modify the "config.json" file, by replacing the values.

   2. If you assign a parameter to the script, it will automatically load the configuration based on environment variables. Here is the list of the necessary environment variables:

        - SubscriptionID = Subscription id
        - BillingProfileID = Billing Profile id
        - BillingAccountID = Billing Account id
        - ApplicationID = Application id
        - TenantID = Tenant id
        - Appsecret = Application secret key
        - Elastic_endpoint = Elastic enterprise search endpoint
        - Elastic_key = Elastic enterprise search key
        - Elastic_enginename = Name of the app search engine

{{ config(materialized='view') }}

select
    *
from {{ source('staging','bank_marketing') }}
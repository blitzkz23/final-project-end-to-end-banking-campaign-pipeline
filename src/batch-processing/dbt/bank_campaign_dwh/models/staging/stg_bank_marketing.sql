{{ config(materialized='view') }}

select
    {{ dbt_utils.surrogate_key(['age', 'job']) }} as id,
    *
from {{ source('staging','bank_marketing') }}
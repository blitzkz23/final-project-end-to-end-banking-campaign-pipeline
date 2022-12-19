{{ config(materialized='view') }}

select
    {{ dbt_utils.surrogate_key(['age', 'job', 'education', 'marital', 'duration', 'month', 'day_of_week', 'housing', 'loan', 'campaign', 'cons_conf_idx', 'emp_var_rate']) }} as id,
    *
from {{ source('staging','bank_marketing') }}
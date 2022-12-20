{{ config(materialized='view') }}

select
    md5(concat(
        coalesce(cast(age as string), ''),
        '|',
        coalesce(cast(job as string), ''),
        '|',
        coalesce(cast(education as string), ''),
        '|',
        coalesce(cast(marital as string), ''),
        '|',
        coalesce(cast(duration as string), ''),
        '|',
        coalesce(cast(month as string), ''),
        '|',
        coalesce(cast(day_of_week as string), ''),
        '|',
        coalesce(cast(housing as string), ''),
        '|',
        coalesce(cast(loan as string), ''),
        '|',
        coalesce(cast(campaign as string), ''),
        '|',
        coalesce(cast(cons_conf_idx as string), ''),
        '|',
        coalesce(cast(emp_var_rate as string), '')
    )) as id,
    *
from {{ source('staging','bank_marketing') }}
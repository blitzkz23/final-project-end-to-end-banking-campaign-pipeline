select distinct
    {{ encode_credit('credit') }} as credit_id,
    credit as credit_type
from {{ ref('stg_bank_marketing') }}
order by credit_id asc
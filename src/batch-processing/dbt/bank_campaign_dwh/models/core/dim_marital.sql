select distinct
    {{ marital('marital') }} as marital_id,
    marital as marital_type
from {{ ref('stg_bank_marketing') }}
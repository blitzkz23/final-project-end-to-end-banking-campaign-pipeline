select distinct
    {{ encode_contact('contact') }} as contact_id,
    contact as contact_type
from {{ ref('stg_bank_marketing') }}
order by contact_id asc
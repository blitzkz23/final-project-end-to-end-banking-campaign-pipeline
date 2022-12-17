select distinct
    {{ contact('contact') }} as contact_id,
    contact as contact_type
from {{ ref('stg_bank_marketing') }}
where contact_id in ({{ var("contact_type_values") }})
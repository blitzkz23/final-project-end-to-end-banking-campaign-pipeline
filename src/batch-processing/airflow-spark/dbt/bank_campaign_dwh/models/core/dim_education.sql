select distinct
    {{ encode_education('education') }} as education_id,
    education as education_type
from {{ ref('stg_bank_marketing') }}
order by education_id asc
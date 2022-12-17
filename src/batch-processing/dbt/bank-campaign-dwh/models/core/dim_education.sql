select distinct
    {{ education('education') }} as education_id,
    education as education_type
from {{ ref('stg_bank_marketing') }}
where education_id in ({{ var("education_type_values") }})
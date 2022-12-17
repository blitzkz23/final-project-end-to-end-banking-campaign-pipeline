select distinct
    {{ job('job') }} as job_id,
    job as job_type
from {{ ref('stg_bank_marketing') }}
where job_id in ({{ var("job_type_values") }})
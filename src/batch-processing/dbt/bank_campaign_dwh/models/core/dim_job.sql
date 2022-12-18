select distinct
    {{ job('job') }} as job_id,
    job as job_type
from {{ ref('stg_bank_marketing') }}
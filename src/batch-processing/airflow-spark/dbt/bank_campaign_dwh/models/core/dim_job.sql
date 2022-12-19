select distinct
    {{ encode_job('job') }} as job_id,
    job as job_type
from {{ ref('stg_bank_marketing') }}
order by job_id asc
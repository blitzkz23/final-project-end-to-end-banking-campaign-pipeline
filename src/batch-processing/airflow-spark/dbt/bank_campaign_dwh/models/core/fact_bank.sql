with bank_data as (

    select * from {{ ref('stg_bank_marketing') }}

),  

final as (

    select
        --ID
        distinct id as id,
        {{ encode_job('job') }} as job_id,
        {{ encode_education('education') }} as education_id,
        {{ encode_marital('marital') }} as marital_id,
        {{ encode_contact('contact') }} as contact_id, 
        `default` as credit,
        age,
        month,
        day_of_week as day,
        housing as housing_loan,
        loan as personal_loan,
        y as subscribe,

    from bank_data
)

select * from final
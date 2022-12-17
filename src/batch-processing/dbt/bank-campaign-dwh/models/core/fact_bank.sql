with bank_data as (

    select * from {{ ref('stg_bank_marketing') }}

),  

final as (

    select
        --ID
        stg_bank_marketing.id as id,
        {{ job('job') }} as job_id,
        {{ education('education') }} as education_id,
        {{ marital('marital') }} as marital_id,
        {{ contact('contact') }} as contact_id,
        --Other
        stg_bank_marketing.age as age,
        stg_bank_marketing.month as month,
        stg_bank_marketing.day_of_week as day,
        stg_bank_marketing.default as credit,
        stg_bank_marketing.housing as housing_loan,
        stg_bank_marketing.loan as personal_loan,
        stg_bank_marketing.y as subscribe
    from bank_data
)

select * from final
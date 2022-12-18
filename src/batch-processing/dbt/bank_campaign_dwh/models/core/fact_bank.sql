with bank_data as (

    select * from {{ ref('stg_bank_marketing') }}

),  

final as (

    select
        --ID
        id as id,
        {{ job('job') }} as job_id,
        {{ education('education') }} as education_id,
        {{ marital('marital') }} as marital_id,
        {{ contact('contact') }} as contact_id, 
        education as education,
        marital as marital,
        contact as contact,
        age as age,
        month as month,
        day_of_week as day,
        `default` as credit,
        housing as housing_loan,
        loan as personal_loan,
        y as subscribe,

    from bank_data
)

select * from final
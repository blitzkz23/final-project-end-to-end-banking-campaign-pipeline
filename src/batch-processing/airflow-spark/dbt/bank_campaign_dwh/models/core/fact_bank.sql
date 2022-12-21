with bank_data as (

    select * from {{ ref('stg_bank_marketing') }}

),  

final as (

    select
        distinct id as id, 
        {{ encode_job('job') }} as job_id,
        {{ encode_education('education') }} as education_id,
        {{ encode_marital('marital') }} as marital_id,
        {{ encode_contact('contact') }} as contact_id, 
        {{ encode_credit('credit') }} as credit_id,
        age,
        concat(
            cast(extract(YEAR FROM parse_date('%Y%m', cast(month as string))) as string),"-",cast(extract(MONTH FROM parse_date('%Y%m', cast(month as string))) as STRING)
        ) as date,
        duration,
        campaign,
        housing as housing_loan,
        loan as personal_loan,
        emp_var_rate,
        cons_price_idx,
        cons_conf_idx,
        euribor3m,
        nr_employed,
        y as subscribe,

    from bank_data
)

select * from final
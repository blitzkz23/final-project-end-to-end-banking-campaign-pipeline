 {#
    This macro returns the description of the job 
#}

{% macro encode_education(column_name) -%}

    case {{ column_name }}
        when 'basic' then 1
        when 'high.school' then 2
        when 'professional.course' then 3
        when 'unknown' then 4
        when 'university.degree' then 5
        when 'illiterate' then 6
    end

{%- endmacro %}
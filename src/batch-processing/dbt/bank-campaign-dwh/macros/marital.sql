 {#
    This macro returns the description of the job 
#}

{% macro marital(column_name) -%}

    case {{ column_name }}
        when 'married' then 1
        when 'single' then 2
        when 'divorced' then 3
        when 'unknown' then 4
    end

{%- endmacro %}
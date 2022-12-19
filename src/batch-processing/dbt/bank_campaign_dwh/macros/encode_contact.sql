 {#
    This macro returns the description of the job 
#}

{% macro encode_contact(column_name) -%}

    case {{ column_name }}
        when 'telephone' then 1
        when 'cellular' then 2
    end

{%- endmacro %}
 {#
    This macro returns the description of the credit 
#}

{% macro encode_credit(column_name) -%}

    case {{ column_name }}
        when 'yes' then 1
        when 'no' then 2
        when 'unknown' then 3
    end

{%- endmacro %}
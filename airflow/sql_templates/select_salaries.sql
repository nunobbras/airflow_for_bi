SELECT  
        emp_no
      , salary
      , from_date
      , to_date
      , %(window_start_date)s
FROM
      salaries
WHERE
      from_date >= %(window_start_date)s
AND   from_date <  %(window_end_date)s


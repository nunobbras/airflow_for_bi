SELECT  
      emp_no,      
      FLOOR(RAND() * 80000) + 10000,
      %(from_date)s,
      %(to_date)s
FROM
      employees
ORDER BY RAND()
LIMIT 10

INSERT INTO `dwh`.`salaries`
(`emp_no`,
`salary`,
`from_date`,
`to_date`,
`import_data`)
VALUES
( %(emp_no),
  %(salary),
  %(from_date),
  %(to_date),
  %(import_data));

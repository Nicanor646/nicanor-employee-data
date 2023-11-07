with employees_dep_job_by_q as (
	select 
		d.department,
		j.job,
		e.id, 
		extract(year from datetime) as year, 
		extract(quarter from datetime) as Q 
	from employee e 
	inner join department d on e.department_id = d.id 
	inner join job j on e.job_id = j.id
	where extract(year from datetime) = :year
)
select 
  department,
  job,
  SUM(case when Q = 1 then 1 else 0 end) as Q1,
  SUM(case when Q = 2 then 1 else 0 end) as Q2,
  SUM(case when Q = 3 then 1 else 0 end) as Q3,
  SUM(case when Q = 4 then 1 else 0 end) as Q4
from employees_dep_job_by_q
group by department, job;
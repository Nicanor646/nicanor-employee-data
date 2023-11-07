with hires_by_department as (
	select 
		d.id,
		d.department,
		count(e.id) as num_hires 
	from department d 
	inner join employee e on d.id = e.department_id 
	where extract(year from datetime) = :year
	group by d.id, d.department 
)
, avg_hires_by_department as (
	select
		avg(num_hires) as avg_hires
	from hires_by_department
)
select 
	d.id,
	d.department, 
	num_hires
from hires_by_department d
where num_hires > (select avg_hires from avg_hires_by_department)
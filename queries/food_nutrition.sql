--- Top 5 foods by average protein
select f.food_name,
round(avg(n.protein)::numeric,2)as average_protein
from food_items f
join nutrition_data n
on f.food_id = n.food_id
group by f.food_name
order by average_protein desc
limit 5;

--- Foods whose average calories >300
select f.food_name,
round(avg(n.calories)::numeric,2)as average_calories
from food_items f
join nutrition_data n
on f.food_id = n.food_id
group by f.food_name
having avg(n.calories)>300
order by average_calories desc

--- for each food
select f.food_id,f.food_name,
round(avg(n.calories)::numeric,2)as avg_calories,
MAX(n.calories)as max_calories,
min(n.calories)as min_Calories
from food_items f
join nutrition_data n
on f.food_id = n.food_id
group by f.food_id,f.food_name
order by avg_calories desc

--- rank foods based on max protein
with cte as (
	select f.food_id,f.food_name,
	MAX(n.protein)as max_protein
	from food_items f
	join nutrition_data n 
	on f.food_id = n.food_id
	group by f.food_id,f.food_name
)
select food_name,
max_protein,
RANK()OVER(ORDER BY max_protein desc)as rank
from cte

--- Top 2 foods by calories
with cte as (
	select f.food_id,f.food_name,
	n.calories,
	DENSE_RANK()OVER(ORDER BY n.calories desc)as rank
	from food_items f
	join nutrition_data n 
	on f.food_id = n.food_id
)
select food_name,calories
from cte
where rank<=2



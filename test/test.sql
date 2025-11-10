select sales_rep, customer, sum(sales)
from sales_fact y
right join (
    select anything
    from anywhere
) x on x.anything = y.sales_rep
where sales_rep_id = '111111111'
group by sales_rep, customer
having sum(sales) > 10000
order by customer desc
limit 100
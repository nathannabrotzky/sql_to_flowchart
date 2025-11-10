select sales_rep, customer, sum(sales)
from sales_fact
left join acct_fact on sales_fact.customer = acct_fact.customer
where sales_rep_id = '111111111'
group by sales_rep, customer
having sum(sales) > 10000
union
select sales_rep, customer, sum(sales)
from sales_fact
right join (
    select customer, occupation, location
    from customer_fact
) x on sales_fact.customer = acct_fact.customer
where sales_rep_id = '222222222'
group by sales_rep, customer
having sum(sales) > 10000
order by customer desc
limit 100
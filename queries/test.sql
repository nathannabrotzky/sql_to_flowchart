select
    matthew,
    mark,
    luke,
    sum(john) as john
from
    the_acts
    left join romans on the_acts.corinthians = romans.colossians
    left join (select * from revelations) x on revelations.corinthians = the_acts.corinthians
WHERE
    matthew = gospel
    and mark = gospel
group by
    matthew, mark, luke
order by
    matthew desc;
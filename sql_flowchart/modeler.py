import re
import uuid

class SqlNode:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.content = ""
        self.parent = []
        self.children = []

def model_sql(sql:str, if_subquery: int = 0, subquery_child: str = "") -> list:
    clauses = ['select','from','where','left join','right join','inner join','cross join', 'union','group by','having','order by','limit']
    model = {}
    subqueries = []
    layer_trigger = 0
    subquery_trigger = 0
    last_id = ""
    word = ""
    subquery = ""
    for char in sql:
        if char == "(":
            layer_trigger += 1
            if layer_trigger >= 1:
                subquery = "".join([subquery,char])
            continue
        elif char == ")":
            if layer_trigger >= 1:
                subquery = "".join([subquery,char])
            layer_trigger -= 1
            if subquery_trigger == 0:
                word = "".join([word,subquery])
                subquery = ""
            if layer_trigger == 0 and subquery_trigger == 1:
                subqueries.append([last_id,subquery])
                subquery = ""
                subquery_trigger = 0
            continue
        elif layer_trigger == 0:
            word = "".join([word,char])
            for clause in clauses:
                if clause in word:
                    id = uuid.uuid4()
                    model[id] = SqlNode(
                        id=id,
                        type=clause,
                    )
                    if last_id != "":
                        model[last_id].content = word.replace(clause,"")
                    last_id = id
                    word = ""
        elif layer_trigger >= 1:
            subquery = "".join([subquery,char])
            for clause in clauses:
                if clause in subquery:
                    subquery_trigger = 1
        else:
            continue
    model[last_id].content = word.replace(";","")
    for key, val in model.items():
        if val.type == "select":
            for k, v in model.items():
                if v.type in ["from",'left join','right join','inner join','cross join']:
                    val.parent.append(k)
            for k, v in model.items():
                if v.type == "where":
                    val.children.append(k)
            if if_subquery == 1:
                for k, v in model.items():
                    check = 0
                    if v.type in ['where','union']:
                        check = 1
                if check == 0:
                    val.children.append(subquery_child)
        elif val.type == "where":
            for k, v in model.items():
                if v.type == "select":
                    val.parent.append(k)
            for k, v in model.items():
                if v.type == "union":
                    val.children.append(k)
            if if_subquery == 1:
                for k, v in model.items():
                    check = 0
                    if v.type == 'union':
                        check = 1
                if check == 0:
                    val.children.append(subquery_child)
        elif val.type == "union":
            check = 0
            for k, v in model.items():
                if v.type == "where":
                    val.parent.append(k)
                    check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "select":
                        val.parent.append(k)
                        check = 1
            if if_subquery == 1:
                val.children.append(subquery_child)
        elif val.type == "group by":
            check = 0
            for k, v in model.items():
                if v.type == "union":
                    val.parent.append(k)
                    check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "where":
                        val.parent.append(k)
                        check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "select":
                        val.parent.append(k)
                        check = 1
        elif val.type == "having":
            check = 0
            for k, v in model.items():
                if v.type == "group by":
                    val.parent.append(k)
                    check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "union":
                        val.parent.append(k)
                        check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "where":
                        val.parent.append(k)
                        check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "select":
                        val.parent.append(k)
                        check = 1
        elif val.type == "order by":
            check = 0
            for k, v in model.items():
                if v.type == "having":
                    val.parent.append(k)
                    check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "group by":
                        val.parent.append(k)
                        check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "union":
                        val.parent.append(k)
                        check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "where":
                        val.parent.append(k)
                        check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "select":
                        val.parent.append(k)
                        check = 1
        elif val.type == "limit":
            check = 0
            for k, v in model.items():
                if v.type == "order by":
                    val.parent.append(k)
                    check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "having":
                        val.parent.append(k)
                        check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "group by":
                        val.parent.append(k)
                        check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "union":
                        val.parent.append(k)
                        check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "where":
                        val.parent.append(k)
                        check = 1
            if check == 0:
                for k, v in model.items():
                    if v.type == "select":
                        val.parent.append(k)
                        check = 1
    
    for query in subqueries:
        model = model | model_sql(query[1][1:-1],1,query[0])

    return model

def modelling(sql):
    nodes = model_sql(sql)
    return nodes
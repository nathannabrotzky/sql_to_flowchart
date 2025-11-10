import uuid
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sql_flowchart.file_loader import load_sql_file
from sql_flowchart.parser import parse_sql_file

def extract_and_mask_subqueries(sql: str):
    subqueries = []
    stack = []
    sql_chars = list(sql)

    for i, char in enumerate(sql):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                start = stack.pop()
                content = sql[start + 1:i].strip()
                if content.lower().startswith('select'):
                    subqueries.append([start, sql[start + 1:i]])
                    for j in range(start + 1, i):
                        sql_chars[j] = '-'

    masked_sql = ''.join(sql_chars)
    return subqueries, masked_sql

class SqlNode:
    def __init__(self, id, index, type, content, parents, children):
        self.id = id
        self.index = index
        self.type = type
        self.content = content
        self.parents = parents
        self.children = children

def model_sql(sql: str) -> dict:
    primary_clauses = ["select", "union", "order by", "limit"]
    nodes = {}
    subqueries, sql = extract_and_mask_subqueries(sql)
    original_sql = sql
    last_id = ""

    # -------------------------------------------------------------------------
    # Assigning primary nodes
    # -------------------------------------------------------------------------
    while True:
        offset = len(original_sql) - len(sql)
        indexes = [sql.rfind(clause) for clause in primary_clauses]
        index = max(indexes)
        if index == -1:
            break
        clause_type = primary_clauses[indexes.index(index)]
        content = sql[index:]
        node_id = uuid.uuid4()
        nodes[node_id] = SqlNode(
            id=node_id,
            index=offset + index,
            type=clause_type.strip(),
            content=content.replace(clause_type, ""),
            parents=[],
            children=[] if not last_id else [last_id]
        )
        if last_id:
            nodes[last_id].parents.append(node_id)
        sql = sql[:index]
        last_id = node_id

    # -------------------------------------------------------------------------
    # Consolidate union nodes
    # -------------------------------------------------------------------------
    union_node = None
    to_delete = []

    for node_id, node in list(nodes.items()):
        if node.type == "union":
            if not union_node:
                union_node = SqlNode(
                    id=uuid.uuid4(),
                    index=-1,
                    type="union",
                    content="",
                    parents=[],
                    children=[]
                )
            if node.children:
                union_node.parents.append(node.children[0])
            to_delete.append(node_id)

    if union_node:
        for node_id in to_delete:
            del nodes[node_id]

        for node in nodes.values():
            if node.type == "select":
                if node.children and node.children[0] in nodes:
                    union_node.children.append(node.children[0])
                    nodes[node.children[0]].parents = [union_node.id]
                else:
                    union_node.parents.append(node.id)
                node.children = [union_node.id]
                node.parents = []

        nodes[union_node.id] = union_node

    # -------------------------------------------------------------------------
    # Split select nodes
    # -------------------------------------------------------------------------
    secondary_clauses = ["from","where","group by","having"]
    select_nodes = {}
    for node in nodes.values():
        if node.type == "select":
            last_id = ""
            i = 15
            while True:
                indexes = [node.content.rfind(clause) for clause in secondary_clauses]
                index = max(indexes)
                if index == -1:
                    break
                clause_type = secondary_clauses[indexes.index(index)]
                content = node.content[index:]
                node_id = uuid.uuid4()
                select_nodes[node_id] = SqlNode(
                    id=node_id,
                    index=node.index,
                    type=clause_type.strip(),
                    content=content.replace(clause_type, ""),
                    parents=[],
                    children=[node.id] if not last_id else [last_id]
                )
                if last_id:
                    select_nodes[last_id].parents.append(node_id)
                node.content = node.content[:index]
                last_id = node_id
                i += 1
    nodes.update(select_nodes)

    # -------------------------------------------------------------------------
    # Split from nodes
    # -------------------------------------------------------------------------
    tertiary_clauses = ["right join","left join","inner join","cross join"]
    from_nodes = {}
    for node in nodes.values():
        if node.type == "from":
            last_id = ""
            while True:
                indexes = [node.content.rfind(clause) for clause in tertiary_clauses]
                index = max(indexes)
                if index == -1:
                    break
                clause_type = tertiary_clauses[indexes.index(index)]
                content = node.content[index:]
                node_id = uuid.uuid4()
                from_nodes[node_id] = SqlNode(
                    id=node_id,
                    index=index,
                    type=clause_type.strip(),
                    content=content.replace(clause_type, ""),
                    parents=[],
                    children=[node.children[0]]
                )
                if last_id:
                    from_nodes[last_id].parents.append(node_id)
                node.content = node.content[:index]
    nodes.update(from_nodes)

    # -------------------------------------------------------------------------
    # Split and add subqueries (recursively)
    # -------------------------------------------------------------------------
    for sub_start, sub_sql in subqueries:
        sub_mask = "-" * len(sub_sql)
        root_id = None

        # Find the node containing the subquery mask
        for node in nodes.values():
            if sub_mask in node.content:
                root_id = node.id
                # Replace the mask with the word "subquery"
                node.content = node.content.replace("("+sub_mask+")", "subquery")
                break

        # Recursively model the subquery
        sub_nodes = model_sql(sub_sql.strip())

        # Link subquery nodes to the root node
        for node in sub_nodes.values():
            if not node.children:
                node.children = [root_id] if root_id else []
        nodes.update(sub_nodes)

    return nodes

if __name__ == "__main__":
    file = load_sql_file(os.path.abspath('test\\test.sql'))
    file = parse_sql_file(file)
    print(file)
    file = model_sql(file)
    for k, node in file.items():
        print(f"\n{node.id}\n{node.type.upper()}: {node.content}\n{node.parents}\n{node.children}")

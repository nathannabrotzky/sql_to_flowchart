from graphviz import Digraph

class SqlFlowchartGenerator:
    def __init__(self, node_map: dict, max_label_length: int = 60, rankdir: str = 'TB',
                 colors: dict = None, fontname: str = 'Arial', output_node_color: str = 'lightgray'):
        self.node_map = node_map
        self.max_label_length = max_label_length
        self.rankdir = rankdir
        self.fontname = fontname
        self.output_node_color = output_node_color

        # Default color mapping if none provided
        self.colors = colors or {
            'select': 'lightblue',
            'from': 'lightgreen',
            'where': 'yellow',
            'join': 'orange',
            'group by': 'pink',
            'order by': 'purple',
            'having': 'red',
            'union': 'gray',
            'limit': 'brown'
        }

    def link_sql_nodes(self):
        for node_id, node in self.node_map.items():
            for parent_id in node.parent:
                if parent_id in self.node_map:
                    parent_node = self.node_map[parent_id]
                    if node_id not in parent_node.children:
                        parent_node.children.append(node_id)
            for child_id in node.children:
                if child_id in self.node_map:
                    child_node = self.node_map[child_id]
                    if node_id not in child_node.parent:
                        child_node.parent.append(node_id)
        for node in self.node_map.values():
            node.parent = list(set(node.parent))
            node.children = list(set(node.children))

    def get_node_color(self, node_type: str) -> str:
        for key in self.colors:
            if key in node_type.lower():
                return self.colors[key]
        return 'white'

    def wrap_text(self, text: str) -> str:
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= self.max_label_length:
                current_line += (word + " ")
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return "\n".join(lines)

    def generate_flowchart(self, output_file='sql_flowchart'):
        self.link_sql_nodes()
        dot = Digraph(comment='SQL Flowchart', format='png')
        dot.attr(rankdir=self.rankdir, fontname=self.fontname)

        for node_id, node in self.node_map.items():
            wrapped_content = self.wrap_text(node.content)
            label = f"[{node_id}]\n{node.type.upper()}\n{wrapped_content}"
            color = self.get_node_color(node.type)
            dot.node(str(node_id), label=label, shape='box', style='filled', fillcolor=color, fontname=self.fontname)

        for node_id, node in self.node_map.items():
            for child_id in node.children:
                dot.edge(str(node_id), str(child_id))

        dot.node("OUTPUT", label="OUTPUT", shape="ellipse", style="filled", fillcolor=self.output_node_color, fontname=self.fontname)
        for node_id, node in self.node_map.items():
            if not node.children:
                dot.edge(str(node_id), "OUTPUT")

        dot.render(output_file, cleanup=True)
        print(f"Flowchart generated: {output_file}.png")
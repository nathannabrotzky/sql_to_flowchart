from graphviz import Digraph

class SqlFlowchartGenerator:
    def __init__(self, node_list: list, max_label_length: int = 60, rankdir: str = 'TB',
                 colors: dict = None, fontname: str = 'Arial', output_node_color: str = 'lightgray'):
        self.node_list = node_list
        self.max_label_length = max_label_length
        self.rankdir = rankdir
        self.fontname = fontname
        self.output_node_color = output_node_color

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

    def get_node_by_id(self, node_id):
        return next((node for k, node in self.node_list.items() if node.id == node_id), None)

    def link_sql_nodes(self):
        for k, node in self.node_list.items():
            for parent_id in node.parents:
                parent_node = self.get_node_by_id(parent_id)
                if parent_node and node.id not in parent_node.children:
                    parent_node.children.append(node.id)
            for child_id in node.children:
                child_node = self.get_node_by_id(child_id)
                if child_node and node.id not in child_node.parents:
                    child_node.parents.append(node.id)

        for k, node in self.node_list.items():
            node.parents = list(set(node.parents))
            node.children = list(set(node.children))

    def get_node_color(self, node_type: str) -> str:
        for key in self.colors:
            if key in node_type.lower():
                return self.colors[key]
        return 'white'

    def wrap_text(self, text: str) -> str:
        import re
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
        text = "\n".join(lines)
        text = re.sub(r'\s*,\s*', ',\n', text)
        text = re.sub(r'\s+\band\b\s+', '\nand ', text, flags=re.IGNORECASE)
        text = re.sub(r'\s+\bor\b\s+', '\nor ', text, flags=re.IGNORECASE)
        text = re.sub(r'\s+\bon\b\s+', '\non ', text, flags=re.IGNORECASE)
        return text

    def generate_flowchart(self, output_file='sql_flowchart'):
        self.link_sql_nodes()
        dot = Digraph(comment='SQL Flowchart', format='png')
        dot.attr(rankdir=self.rankdir, fontname=self.fontname)

        for k, node in self.node_list.items():
            wrapped_content = self.wrap_text(node.content)
            wrapped_content = wrapped_content \
                .replace('>', '&gt;') \
                .replace('<', '&lt;') \
                .replace('\n', '<br/>') \
                .replace('(', '<b>(</b>') \
                .replace(')', '<b>)</b>')

            content_rows = "\n".join(
                f'<tr><td align="center">{line.strip()}</td></tr>'
                for line in wrapped_content.split('<br/>') if line.strip()
            )

            label = f"""<
                <table border="0" cellborder="0" cellspacing="0">
                    <tr><td align="center"><b>{node.type.upper()}</b></td></tr>
                    {content_rows}
                </table>
            >"""
            color = self.get_node_color(node.type)

            try:
                dot.node(str(node.id), label=label, shape='box', style='filled', fillcolor=color, fontname=self.fontname)
            except Exception as e:
                print(f"Error creating node {node.id}: {e}")
                print("Label content:\n", label)

        for k, node in self.node_list.items():
            for child_id in node.children:
                dot.edge(str(node.id), str(child_id))

        dot.node("OUTPUT", label="OUTPUT", shape="ellipse", style="filled", fillcolor=self.output_node_color, fontname=self.fontname)
        for k, node in self.node_list.items():
            if not node.children:
                dot.edge(str(node.id), "OUTPUT")

        dot.render(output_file, cleanup=True)
        print(f"Flowchart generated: {output_file}.png")

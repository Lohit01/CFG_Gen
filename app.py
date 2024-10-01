import os
import openai
import pydot
import networkx as nx
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

def calculate_cyclomatic_complexity(dot_code):
    graph = nx.DiGraph(nx.nx_pydot.read_dot(dot_code))

    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()

    cyclomatic_complexity = num_edges - num_nodes + 2

    return {
        'Number of Nodes': num_nodes,
        'Number of Edges': num_edges,  # Updated key
        'Cyclomatic Complexity': cyclomatic_complexity
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_cfg_route():
    user_input = request.form['user_input']
    prompt = f"Create a control flow graph in DOT format for the following scenario: {user_input}. Include nodes and edges in valid DOT syntax, without additional explanations."

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    dot_code = response.choices[0].message.content.strip()
    
    # Extract the relevant DOT code
    start_index = dot_code.index("digraph")
    end_index = dot_code.rindex("}") + 1
    dot_code = dot_code[start_index:end_index]
    
    # Save the DOT code to a file
    with open("cfg_graph.dot", "w") as f:
        f.write(dot_code)

    # Calculate metrics
    metrics = calculate_cyclomatic_complexity("cfg_graph.dot")

    # Generate the graph image
    os.system("dot -Tpng cfg_graph.dot -o static/cfg_graph.png")
    
    cfg_image = url_for('static', filename='cfg_graph.png')
    
    return render_template('index.html', cfg_image=cfg_image, metrics=metrics)

if __name__ == '__main__':
    app.run(debug=True)

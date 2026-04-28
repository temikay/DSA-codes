import streamlit as st
import networkx as nx
import json
import os

students = {
    "James Adeyemi" :        [1,0,0,1,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],
    "Elizabeth Olawale" : [0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
    "Benjamin Babatunde" : [1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0],
    "Catherine Olatunji" :   [0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,0,0],
    "Samuel Okorocha" :      [0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1],
    "Victoria Akinyemi" :    [0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0],
    "Daniel Oyedele" :       [1,0,0,0,0,0,0,1,0,0,0,0,1,0,1,1,0,0,0,0],
    "Margaret Balogun" :     [0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,0,0],
    "Alexander Fadugba" :    [0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
    "Sophia Onabanjo" :      [1,0,0,0,0,0,0,0,0,1,0,0,1,0,1,1,0,0,0,0],
    "William Adebayo" :      [0,0,0,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1],
    "Charlotte Oyelowo" :    [0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,1,0,0,0,0],
    "Thomas Oshodi" :        [1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0],
    "Eleanor Adenuga" :      [0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
    "Henry Bankole" :        [0,0,0,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1],
    "Beatrice Folarin" :     [0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,0],
    "George Ogundipe" :      [1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0],
    "Florence Ajayi" :       [0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
    "Arthur Popoola" :       [0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1],
    "Lillian Jegede" :       [0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,1,0,0,0,0],
    "Oliver Soyinka" :       [1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0],
    "Amelia Abiola" :        [0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
    "Edward Otedola" :       [0,0,0,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1],
    "Grace Afolayan" :       [0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,0],
    "Frederick Akindele" :   [1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0],
    "Alice Bello" :          [0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
    "Philip Durojaiye" :     [0,0,0,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1],
    "Rose Eniola" :          [0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,1,0,0,0,0],
    "Joseph Gbadamosi" :     [1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0],
    "Clara Ishola" :         [0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
    "Richard Kolawole" :     [0,0,0,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1],
    "Martha Ladipo" :        [0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,0],
    "David Makanjuola" :     [1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0],
    "Hazel Odumosu" :        [0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
    "Robert Olaniyan" :      [0,0,0,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1],
    "Jane Onasanya" :        [0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,1,0,0,0,0],
    "Charles Sanusi" :       [1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0],
    "Evelyn Tinubu" :        [0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
    "Francis Williams-Adeola" : [0,0,0,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1],
    "Mary Yerokun" :         [0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,0],
    "George Alaba" :         [1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0],
    "Sarah Awolowo" :        [0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
    "Peter Dokpesi" :        [0,0,0,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1],
    "Anne Esho" :            [0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,1,0,0,0,0],
    "Michael Folorunsho" :   [1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0],
    "Lucy Idowu" :           [0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0],
    "Stephen Jolayemi" :     [0,0,0,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1],
    "Diana Kayode" :         [0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,0],
    "Christopher Mobolaji" : [1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0],
    "Ruby Ogunlesi" :        [0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0]
}

def load_students():
    if os.path.exists("students.json") and os.path.getsize("students.json") > 0:
        with open("students.json", "r") as f:
            data = json.load(f)
            # Ensure all keys are strings (JSON keys are always strings, but just in case)
            return {str(k): v for k, v in data.items()}
    else:
        with open("students.json", "w") as f:
            json.dump(students, f, indent=4)
        return students.copy()
    
def save_students(students):
    with open("students.json", "w") as f:
        json.dump(students, f, indent=4)

# Session State Initialization
if "students" not in st.session_state:
    st.session_state.students = load_students()
    
students = st.session_state.students

index_to_name = {i: name for i, name in enumerate(students.keys())}
name_to_index = {name: i for i, name in index_to_name.items()}

if "index_to_name" not in st.session_state:
    st.session_state.index_to_name = index_to_name.copy()
    
if "name_to_index" not in st.session_state:
    st.session_state.name_to_index = name_to_index.copy()
    
index_to_name = st.session_state.index_to_name
name_to_index = st.session_state.name_to_index

skills = [
    "Website development", "Data Science", "Data Analysis", "Embedded Systems",
    "IoT", "Machine Learning", "3D design", "Project management",
    "Research and development", "Product design", "Network Engineering",
    "Cybersecurity", "Graphic design", "Robotics", "UI/UX",
    "Digital Marketing", "Cooking", "Python", "Creative Writing",
    "Electrical Installation"
]

def get_student_skills(vector):
    return [skills[i] for i, val in enumerate(vector) if val == 1]

G = nx.Graph()

#Add nodes
for i in index_to_name:
    G.add_node(i)
    
#Add edges
# def add_edges(G, students):
names = list(students.keys())


for i in range(len(names)):
    for j in range(i + 1, len(names)):
    
        # Calculate similarity based on shared skills
        # skills1 = set(get_student_skills(students[student1]))
        # skills2 = set(get_student_skills(students[student2]))
        # shared_skills = skills1.intersection(skills2)
        
        s1 = students[names[i]]
        s2 = students[names[j]]
        
        sim = sum(1 for a, b in zip(s1, s2) if a == 1 and b == 1)  # Simple count of shared skills
        
        if sim > 0:  # Only add edge if there's at least one shared skill
            distance = 1 / (sim + 1)  # Inverse of similarity for distance
            
            G.add_edge(
                name_to_index[names[i]],
                name_to_index[names[j]],
                weight=sim, 
                distance= distance
            )
        # if shared_skills:
        #     G.add_edge(i, j, weight=len(shared_skills))

# add_edges(G, students)

st.title("Student Collaboration System")

# Add the Add_Student button
col1, col2 = st.columns([6.8, 1])
with col1:
    name = st.selectbox(
        "Select a student:", 
        list(students.keys()),
        # label_visibility="collapsed"
    )
    source = name_to_index[name]

with col2:
    st.write("")  # Empty space for alignment
    st.write("")  # Empty space for alignment
    if st.button("➕", key="add_student", help="Add a new student to the system"):
        st.session_state.show_form = True
    
if "show_form" not in st.session_state:
    st.session_state.show_form = False

if st.session_state.show_form:
    st.subheader("Add a New Student")
    
    with st.form("add_student_form"):
        new_name = st.text_input("Student Name")
        new_skills = st.multiselect("Select Skills", skills)

        submitted = st.form_submit_button("Add Student")

        if submitted:
            students = st.session_state.students
            index_to_name = st.session_state.index_to_name
            name_to_index = st.session_state.name_to_index

            if not new_name:
                st.error("Please enter a student name.")

            elif new_name in students:
                st.error("Student already exists.")

            elif not new_skills:
                st.error("Please select at least one skill.")

            else:
                # Create skill vector
                skill_vector = [1 if skill in new_skills else 0 for skill in skills]
                students[new_name] = skill_vector
                
                # Save to JSON File
                save_students(students)
                
                st.write(f"{new_name} added to the system with skills: {', '.join(new_skills)}")
                
                # Update index mappings
                
                new_index = max(index_to_name.keys()) + 1
                index_to_name[new_index] = new_name
                name_to_index[new_name] = new_index

                st.success(f"Student '{new_name}' added successfully!")
                st.session_state.show_form = False
                
                st.rerun()  # Refresh the app to show the new student

col1, col2, col3 = st.columns(3)

with col1:
    show_skills = st.button("Show Skills", key="skills_btn")
    
with col2:
    # st.button("Recommenddd", key="recommend_btn")
    recommend_btn = st.button("Recommend", key="recommend_btn")
    
with col3:
    # st.button("Show Graph", key="graph_btn")
    show_graph = st.button("Show Community Graph", key="graph_btn")


# Show Top Collaborators Window

if recommend_btn:
    if source not in G:
        st.error("Student not found in the graph.")
        st.stop()

    lengths = nx.single_source_dijkstra_path_length(G, source, weight="distance")
    ranked = sorted(lengths.items(), key=lambda x: x[1])

    source_skills = set(get_student_skills(students[name]))

    st.subheader("Top Collaborators")

    for node, dist in ranked[1:6]:  # Skip the source itself
        person = index_to_name[node]
        person_skills = set(get_student_skills(students[person]))
        shared_skills = source_skills.intersection(person_skills)

        st.write(f"**{person}** ")
        st.write(f"Score: {round(dist, 2)}")
        st.write(f"Shared Skills: {', '.join(shared_skills)}")
        st.write("---")

    selected_vector = students[name]
    selected_skills = get_student_skills(selected_vector)



# Show Collaboration grapah section

lengths = nx.single_source_dijkstra_path_length(G, name_to_index[name], weight="distance")
ranked = sorted(lengths.items(), key=lambda x: x[1])

top_nodes =  [node for node, _ in ranked[:6]]

subG = G.subgraph(top_nodes)

import matplotlib.pyplot as plt

if show_graph:
    plt.figure(figsize=(10, 6))
    
    pos = nx.spring_layout(subG, k= 0.8)
    
    node_colors = [
        "red" if node == source else "skyblue"
        for node in subG.nodes()
    ]
    
    name_labels = {node: index_to_name[node] for node in subG.nodes()}
    
    nx.draw(
        subG,
        pos,
        with_labels=True,
        labels=name_labels,
        node_color=node_colors,
        edge_color='gray',
        node_size=700,
        font_size=8
    )
    
    labels = {
        (u, v): f"{d['weight']}"
        for u, v, d in subG.edges(data=True)
    }
    
    # labels = nx.get_edge_attributes(subG, 'weight')
    nx.draw_networkx_edge_labels(
        subG,
        pos,
        edge_labels=labels,
        font_size=7
        )
    st.pyplot(plt)

# Show Skills button

if show_skills:
    st.subheader(f"Skills of {name}")
    for skill in get_student_skills(students[name]):
        st.write(f"- {skill}")

   
st.write("Total students: ", len(students))
# x = txt.endswith('.')

# print(x)

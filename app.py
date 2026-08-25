import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

from ai_engine import (
    extract_text_from_pdf,
    extract_research_knowledge
)


# =================================================
# PAGE CONFIG
# =================================================

st.set_page_config(
    page_title="ResearchNexus AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =================================================
# CUSTOM CSS
# =================================================

st.markdown("""
<style>

.stApp {
    background-color: #0b1020;
}

.main-title {
    font-size: 3.2rem;
    font-weight: 800;
    color: white;
    margin-bottom: 5px;
}

.hero-text {
    font-size: 1.2rem;
    color: #94a3b8;
    margin-bottom: 25px;
}

.badge {
    display: inline-block;
    padding: 7px 15px;
    border-radius: 20px;
    background-color: #16324f;
    color: #67e8f9;
    font-size: 0.85rem;
    font-weight: 600;
}

.insight-card {
    background-color: #151c33;
    padding: 22px;
    border-radius: 16px;
    border-left: 4px solid #38bdf8;
    margin-bottom: 15px;
    color: white;
}

.section-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: white;
    margin-top: 25px;
    margin-bottom: 15px;
}

.paper-card {
    background-color: #151c33;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #27304d;
    margin-bottom: 15px;
    color: white;
}

.library-stat {
    background-color: #151c33;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #27304d;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# =================================================
# SESSION STATE
# =================================================

if "research_data" not in st.session_state:
    st.session_state.research_data = []


# =================================================
# RELATED RESEARCH CONCEPT GROUPS
# =================================================

concept_groups = {

    "smart_agriculture": {

        "crop disease detection",
        "precision agriculture",
        "agricultural risk prediction",
        "climate adaptation",
        "smart agriculture",
        "sustainable agriculture",
        "plant pathology",
        "crop stress",
        "drought",
        "agriculture"

    },

    "artificial_intelligence": {

        "deep learning",
        "machine learning",
        "computer vision",
        "convolutional neural networks",
        "cnn",
        "vision transformer",
        "random forest",
        "artificial intelligence"

    },

    "agricultural_data": {

        "satellite imagery",
        "soil moisture",
        "weather data",
        "historical weather",
        "climate data",
        "leaf image",
        "image dataset",
        "remote sensing"

    },

    "early_warning_systems": {

        "early warning system",
        "risk prediction",
        "disease detection",
        "crop monitoring",
        "prediction"

    }

}


# =================================================
# FIND SEMANTIC RESEARCH CONCEPTS
# =================================================

def find_concept_connections(items):

    matched_concepts = set()

    for concept, keywords in concept_groups.items():

        for item in items:

            item = item.lower()

            for keyword in keywords:

                if (
                    keyword in item
                    or item in keyword
                ):

                    matched_concepts.add(
                        concept
                    )

    return matched_concepts


# =================================================
# CALCULATE CROSS-RESEARCH CONNECTION SCORE
# UPDATE 1
# =================================================

def calculate_connection_score(
    shared_entities,
    shared_topics,
    shared_concepts
):

    # Each shared item contributes equally
    connection_score = (

        len(shared_entities)
        +
        len(shared_topics)
        +
        len(shared_concepts)

    )

    if connection_score >= 5:

        connection_level = "🔥 Strong Connection"

    elif connection_score >= 3:

        connection_level = "⚡ Moderate Connection"

    elif connection_score >= 1:

        connection_level = "🔹 Emerging Connection"

    else:

        connection_level = "❌ No Connection"

    return connection_score, connection_level


# =================================================
# SIDEBAR
# =================================================

with st.sidebar:

    st.markdown("# 🧠 ResearchNexus AI")

    st.caption(
        "AI-Powered University Research Intelligence"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Research Hub",
            "📤 Ingest Research",
            "📚 Research Library",
            "🕸️ Knowledge Graph",
            "💡 AI Insights"
        ]
    )

    st.divider()

    st.success("● AI Research Engine Online")


# =================================================
# RESEARCH HUB
# =================================================

if page == "🏠 Research Hub":

    st.markdown(
        '<span class="badge">'
        '✦ UNIVERSITY RESEARCH INTELLIGENCE'
        '</span>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-title">'
        'Discover hidden connections in research.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-text">'
        'ResearchNexus AI transforms siloed university research into '
        'an intelligent, connected knowledge ecosystem.'
        '</div>',
        unsafe_allow_html=True
    )

    total_docs = len(
        st.session_state.research_data
    )

    total_entities = sum(
        len(item.get("entities", []))
        for item in st.session_state.research_data
    )

    total_relationships = sum(
        len(item.get("relationships", []))
        for item in st.session_state.research_data
    )

    total_opportunities = sum(
        len(
            item.get(
                "collaboration_opportunities",
                []
            )
        )
        for item in st.session_state.research_data
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📄 Research Documents",
            total_docs
        )

    with col2:

        st.metric(
            "🔍 Entities Discovered",
            total_entities
        )

    with col3:

        st.metric(
            "🔗 Connections",
            total_relationships
        )

    with col4:

        st.metric(
            "💡 Opportunities",
            total_opportunities
        )

    st.divider()

    st.markdown(
        '<div class="section-title">'
        'How ResearchNexus AI Works'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.info(
            "📤 **1. INGEST**\n\n"
            "Upload research PDFs or paste research content."
        )

    with col2:

        st.info(
            "🤖 **2. EXTRACT**\n\n"
            "AI identifies entities, technologies, topics and datasets."
        )

    with col3:

        st.info(
            "🕸️ **3. CONNECT**\n\n"
            "Research relationships are transformed into a unified knowledge graph."
        )

    with col4:

        st.info(
            "💡 **4. DISCOVER**\n\n"
            "Find hidden collaborations and cross-disciplinary research opportunities."
        )


# =================================================
# INGEST RESEARCH
# =================================================

elif page == "📤 Ingest Research":

    st.markdown("# 📤 Ingest Research")

    st.caption(
        "Upload university research and let AI discover "
        "its hidden knowledge."
    )

    uploaded_file = st.file_uploader(
        "Upload a Research PDF",
        type=["pdf"]
    )

    st.write("### OR")

    manual_text = st.text_area(
        "Paste Research Content",
        height=180,
        placeholder=(
            "Paste a research abstract, thesis content, "
            "markdown or research information..."
        )
    )

    analyze_button = st.button(
        "🧠 Analyze Research with AI",
        use_container_width=True
    )

    if analyze_button:

        if uploaded_file is not None:

            with st.spinner(
                "📄 Extracting research content..."
            ):

                text = extract_text_from_pdf(
                    uploaded_file
                )

            filename = uploaded_file.name

        elif manual_text.strip():

            text = manual_text

            filename = (
                f"Manual Research Paper "
                f"{len(st.session_state.research_data) + 1}"
            )

        else:

            st.warning(
                "Please upload a PDF or paste research content."
            )

            st.stop()

        if not text.strip():

            st.error(
                "No readable text was found in this research document."
            )

            st.stop()

        with st.spinner(
            "🤖 AI is extracting research entities and relationships..."
        ):

            result = extract_research_knowledge(
                text,
                filename
            )

        if "error" in result:

            st.error(
                f"AI Analysis failed: {result['error']}"
            )

        else:

            result["document"] = filename

            st.session_state.research_data.append(
                result
            )

            st.success(
                f"🎉 {filename} successfully analyzed "
                "and added to ResearchNexus!"
            )

            st.markdown(
                "## 📌 Research Summary"
            )

            st.write(
                result.get(
                    "summary",
                    "No summary generated."
                )
            )

            st.markdown(
                "## 🔍 Discovered Topics"
            )

            topics = result.get(
                "topics",
                []
            )

            if topics:

                topic_cols = st.columns(3)

                for index, topic in enumerate(topics):

                    with topic_cols[index % 3]:

                        st.success(
                            f"🏷️ {topic}"
                        )

            else:

                st.info(
                    "No topics detected."
                )

            st.markdown(
                "## 🧬 Extracted Entities"
            )

            entities = result.get(
                "entities",
                []
            )

            if entities:

                entity_df = pd.DataFrame(
                    entities
                )

                st.dataframe(
                    entity_df,
                    use_container_width=True
                )

            else:

                st.info(
                    "No entities detected."
                )

            st.markdown(
                "## 🔗 Relationships"
            )

            relationships = result.get(
                "relationships",
                []
            )

            if relationships:

                relationship_df = pd.DataFrame(
                    relationships
                )

                st.dataframe(
                    relationship_df,
                    use_container_width=True
                )

            else:

                st.info(
                    "No relationships detected."
                )


# =================================================
# RESEARCH LIBRARY
# =================================================

elif page == "📚 Research Library":

    st.markdown("# 📚 Research Library")

    st.caption(
        "Browse, search and manage all research documents "
        "analyzed by ResearchNexus AI."
    )

    if not st.session_state.research_data:

        st.info(
            "📭 Your research library is empty. "
            "Go to **Ingest Research** and analyze a document."
        )

    else:

        total_documents = len(
            st.session_state.research_data
        )

        total_entities = sum(
            len(document.get("entities", []))
            for document in st.session_state.research_data
        )

        total_topics = sum(
            len(document.get("topics", []))
            for document in st.session_state.research_data
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "📄 Total Papers",
                total_documents
            )

        with col2:

            st.metric(
                "🔍 Total Entities",
                total_entities
            )

        with col3:

            st.metric(
                "🏷️ Total Topics",
                total_topics
            )

        st.divider()

        search_query = st.text_input(
            "🔍 Search Research Library",
            placeholder=(
                "Search by paper name, topic, summary "
                "or extracted entity..."
            )
        )

        filtered_documents = []

        for index, document in enumerate(
            st.session_state.research_data
        ):

            document_name = document.get(
                "document",
                ""
            )

            summary = document.get(
                "summary",
                ""
            )

            topics = " ".join(
                document.get(
                    "topics",
                    []
                )
            )

            entities = " ".join(
                entity.get(
                    "name",
                    ""
                )
                for entity in document.get(
                    "entities",
                    []
                )
            )

            searchable_content = (
                document_name
                + " "
                + summary
                + " "
                + topics
                + " "
                + entities
            ).lower()

            if (
                not search_query
                or search_query.lower()
                in searchable_content
            ):

                filtered_documents.append(
                    (
                        index,
                        document
                    )
                )

        st.markdown(
            f"### 📂 Showing {len(filtered_documents)} "
            f"of {total_documents} Research Papers"
        )

        if not filtered_documents:

            st.warning(
                "No research papers matched your search."
            )

        else:

            for index, document in filtered_documents:

                document_name = document.get(
                    "document",
                    "Research Document"
                )

                topics = document.get(
                    "topics",
                    []
                )

                entities = document.get(
                    "entities",
                    []
                )

                relationships = document.get(
                    "relationships",
                    []
                )

                with st.expander(
                    f"📄 {document_name}",
                    expanded=False
                ):

                    col1, col2 = st.columns(
                        [4, 1]
                    )

                    with col1:

                        st.markdown(
                            "### 📌 Research Summary"
                        )

                        st.write(
                            document.get(
                                "summary",
                                "No summary generated."
                            )
                        )

                    with col2:

                        st.metric(
                            "🏷️ Topics",
                            len(topics)
                        )

                        st.metric(
                            "🧬 Entities",
                            len(entities)
                        )

                        st.metric(
                            "🔗 Relations",
                            len(relationships)
                        )

                    st.divider()

                    st.markdown(
                        "### 🏷️ Research Topics"
                    )

                    if topics:

                        topic_cols = st.columns(3)

                        for topic_index, topic in enumerate(
                            topics
                        ):

                            with topic_cols[
                                topic_index % 3
                            ]:

                                st.success(
                                    f"🏷️ {topic}"
                                )

                    else:

                        st.info(
                            "No topics detected."
                        )

                    st.divider()

                    st.markdown(
                        "### 🧬 Extracted Entities"
                    )

                    if entities:

                        entity_df = pd.DataFrame(
                            entities
                        )

                        st.dataframe(
                            entity_df,
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "No entities detected."
                        )

                    st.divider()

                    st.markdown(
                        "### 🔗 Research Relationships"
                    )

                    if relationships:

                        relationship_df = pd.DataFrame(
                            relationships
                        )

                        st.dataframe(
                            relationship_df,
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "No relationships detected."
                        )

                    st.divider()

                    delete_col1, delete_col2 = (
                        st.columns(
                            [4, 1]
                        )
                    )

                    with delete_col2:

                        if st.button(
                            "🗑️ Delete",
                            key=f"delete_{index}",
                            use_container_width=True
                        ):

                            st.session_state.research_data.pop(
                                index
                            )

                            st.rerun()

        st.divider()

        st.markdown(
            "### ⚠️ Library Management"
        )

        st.warning(
            "Clearing the research library will remove "
            "all currently analyzed research documents."
        )

        if st.button(
            "🗑️ Clear Entire Research Library",
            use_container_width=True
        ):

            st.session_state.research_data = []

            st.rerun()


# =================================================
# KNOWLEDGE GRAPH
# =================================================

elif page == "🕸️ Knowledge Graph":

    st.markdown(
        "# 🕸️ University Knowledge Graph"
    )

    st.caption(
        "Discover hidden connections between "
        "multiple research papers."
    )

    if not st.session_state.research_data:

        st.info(
            "👈 Go to **Ingest Research** and analyze "
            "at least one research document."
        )

    else:

        G = nx.Graph()

        document_entities = {}
        document_topics = {}

        for document in st.session_state.research_data:

            doc_name = document.get(
                "document",
                "Research Document"
            )

            document_entities[doc_name] = set()
            document_topics[doc_name] = set()

            G.add_node(
                doc_name,
                node_type="Document"
            )

            for topic in document.get(
                "topics",
                []
            ):

                if topic:

                    document_topics[doc_name].add(
                        topic.lower()
                    )

                    G.add_node(
                        topic,
                        node_type="Topic"
                    )

                    G.add_edge(
                        doc_name,
                        topic,
                        relationship="HAS_TOPIC"
                    )

            for entity in document.get(
                "entities",
                []
            ):

                entity_name = entity.get(
                    "name"
                )

                entity_type = entity.get(
                    "type",
                    "Entity"
                )

                if entity_name:

                    document_entities[doc_name].add(
                        entity_name.lower()
                    )

                    G.add_node(
                        entity_name,
                        node_type=entity_type
                    )

                    G.add_edge(
                        doc_name,
                        entity_name,
                        relationship="MENTIONS"
                    )

            for relation in document.get(
                "relationships",
                []
            ):

                source = relation.get(
                    "source"
                )

                target = relation.get(
                    "target"
                )

                relationship = relation.get(
                    "relationship",
                    "RELATED_TO"
                )

                if source and target:

                    if source not in G.nodes:

                        G.add_node(
                            source,
                            node_type="Entity"
                        )

                    if target not in G.nodes:

                        G.add_node(
                            target,
                            node_type="Entity"
                        )

                    G.add_edge(
                        source,
                        target,
                        relationship=relationship
                    )

        documents = list(
            document_entities.keys()
        )

        cross_connections = []

        for i in range(len(documents)):

            for j in range(
                i + 1,
                len(documents)
            ):

                doc1 = documents[i]
                doc2 = documents[j]

                shared_entities = (
                    document_entities[doc1]
                    &
                    document_entities[doc2]
                )

                shared_topics = (
                    document_topics[doc1]
                    &
                    document_topics[doc2]
                )

                paper1_items = (
                    document_entities[doc1]
                    |
                    document_topics[doc1]
                )

                paper2_items = (
                    document_entities[doc2]
                    |
                    document_topics[doc2]
                )

                concepts1 = find_concept_connections(
                    paper1_items
                )

                concepts2 = find_concept_connections(
                    paper2_items
                )

                shared_concepts = (
                    concepts1
                    &
                    concepts2
                )

                connection_score, connection_level = (
                    calculate_connection_score(
                        shared_entities,
                        shared_topics,
                        shared_concepts
                    )
                )

                if connection_score > 0:

                    G.add_edge(
                        doc1,
                        doc2,
                        relationship=
                        "CROSS_RESEARCH_CONNECTION",
                        weight=connection_score,
                        shared_concepts=list(
                            shared_concepts
                        )
                    )

                    cross_connections.append(

                        {

                            "Paper 1": doc1,

                            "Paper 2": doc2,

                            "Shared Entities":
                            len(shared_entities),

                            "Shared Topics":
                            len(shared_topics),

                            "Related Concepts":

                            ", ".join(

                                concept.replace(
                                    "_",
                                    " "
                                ).title()

                                for concept
                                in shared_concepts

                            )

                            if shared_concepts

                            else "None",

                            "Connection Score":
                            connection_score,

                            "Connection Level":
                            connection_level

                        }

                    )

        pos = nx.spring_layout(
            G,
            seed=42,
            k=2.2,
            iterations=150
        )

        normal_edge_x = []
        normal_edge_y = []

        cross_edge_x = []
        cross_edge_y = []

        for source, target, edge_data in G.edges(
            data=True
        ):

            x0, y0 = pos[source]
            x1, y1 = pos[target]

            relationship = edge_data.get(
                "relationship",
                ""
            )

            if relationship == "CROSS_RESEARCH_CONNECTION":

                cross_edge_x.extend(
                    [x0, x1, None]
                )

                cross_edge_y.extend(
                    [y0, y1, None]
                )

            else:

                normal_edge_x.extend(
                    [x0, x1, None]
                )

                normal_edge_y.extend(
                    [y0, y1, None]
                )

        edge_trace = go.Scatter(

            x=normal_edge_x,
            y=normal_edge_y,
            mode="lines",
            hoverinfo="none",

            line=dict(
                width=1,
                color="#64748b"
            ),

            name="Research Connection"

        )

        cross_trace = go.Scatter(

            x=cross_edge_x,
            y=cross_edge_y,
            mode="lines",
            hoverinfo="none",

            line=dict(
                width=4,
                color="#facc15"
            ),

            name="Cross-Research Connection"

        )

        color_map = {

            "Document": "#f59e0b",
            "Researcher": "#a855f7",
            "Department": "#ef4444",
            "Topic": "#22c55e",
            "Technology": "#3b82f6",
            "Method": "#06b6d4",
            "Dataset": "#f97316",
            "Entity": "#94a3b8"

        }

        size_map = {

            "Document": 48,
            "Researcher": 30,
            "Department": 32,
            "Topic": 30,
            "Technology": 27,
            "Method": 27,
            "Dataset": 32,
            "Entity": 25

        }

        node_types = {}

        for node in G.nodes():

            node_type = G.nodes[node].get(
                "node_type",
                "Entity"
            )

            if node_type not in node_types:

                node_types[node_type] = {

                    "x": [],
                    "y": [],
                    "text": [],
                    "hover": []

                }

            x, y = pos[node]

            node_types[node_type]["x"].append(x)

            node_types[node_type]["y"].append(y)

            node_types[node_type]["text"].append(node)

            connections = len(
                list(
                    G.neighbors(node)
                )
            )

            node_types[node_type]["hover"].append(

                f"<b>{node}</b><br>"
                f"Type: {node_type}<br>"
                f"Connections: {connections}"

            )

        traces = [
            edge_trace,
            cross_trace
        ]

        for node_type, data in node_types.items():

            color = color_map.get(
                node_type,
                "#94a3b8"
            )

            size = size_map.get(
                node_type,
                24
            )

            node_trace = go.Scatter(

                x=data["x"],
                y=data["y"],

                mode="markers+text",

                name=node_type,

                text=data["text"],

                textposition="top center",

                hovertext=data["hover"],

                hoverinfo="text",

                marker=dict(

                    size=size,

                    color=color,

                    line=dict(
                        width=2,
                        color="white"
                    )

                )

            )

            traces.append(
                node_trace
            )

        fig = go.Figure(
            data=traces
        )

        fig.update_layout(

            title=dict(

                text=
                "🧠 Unified University Research Network",

                font=dict(
                    size=24
                )

            ),

            showlegend=True,

            hovermode="closest",

            height=800,

            paper_bgcolor="#0b1020",

            plot_bgcolor="#0b1020",

            font=dict(
                color="white",
                size=13
            ),

            margin=dict(
                b=20,
                l=20,
                r=20,
                t=70
            ),

            legend=dict(

                bgcolor="rgba(20,30,50,0.9)",

                bordercolor="#475569",

                borderwidth=1

            ),

            xaxis=dict(
                showgrid=False,
                zeroline=False,
                visible=False
            ),

            yaxis=dict(
                showgrid=False,
                zeroline=False,
                visible=False
            )

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "📄 Research Papers",
                len(documents)
            )

        with col2:

            st.metric(
                "🧩 Total Nodes",
                len(G.nodes())
            )

        with col3:

            st.metric(
                "🔗 Total Connections",
                len(G.edges())
            )

        with col4:

            st.metric(
                "✨ Cross-Research Links",
                len(cross_connections)
            )

        st.divider()

        st.markdown(
            "## ✨ Hidden Cross-Research Connections"
        )

        if cross_connections:

            connection_df = pd.DataFrame(
                cross_connections
            )

            st.dataframe(
                connection_df,
                use_container_width=True
            )

        else:

            st.info(
                "No direct or semantic research "
                "connections were found yet."
            )

        st.divider()

        st.markdown(
            "### 🎯 Connection Score System"
        )

        st.info(
            """
            🔹 **1–2:** Emerging Connection

            ⚡ **3–4:** Moderate Connection

            🔥 **5+:** Strong Connection

            The score is calculated from shared entities,
            shared topics and shared semantic concepts.
            """
        )

        st.divider()

        st.markdown(
            "### 🎨 Knowledge Graph Legend"
        )

        legend_col1, legend_col2, legend_col3 = (
            st.columns(3)
        )

        with legend_col1:

            st.markdown(
                "🟠 **Research Document**"
            )

            st.markdown(
                "🟣 **Researcher**"
            )

            st.markdown(
                "🔴 **Department**"
            )

        with legend_col2:

            st.markdown(
                "🟢 **Research Topic**"
            )

            st.markdown(
                "🔵 **Technology**"
            )

            st.markdown(
                "🔷 **Method**"
            )

        with legend_col3:

            st.markdown(
                "🟠 **Dataset**"
            )

            st.markdown(
                "🟡 **Cross-Research Connection**"
            )


# =================================================
# AI INSIGHTS
# =================================================

elif page == "💡 AI Insights":

    st.markdown(
        "# 💡 AI Research Insights"
    )

    st.caption(
        "Discover hidden collaborations, research overlaps "
        "and cross-disciplinary opportunities."
    )

    if not st.session_state.research_data:

        st.info(
            "Analyze at least one research document first."
        )

    else:

        # =============================================
        # INDIVIDUAL PAPER INSIGHTS
        # =============================================

        for document in st.session_state.research_data:

            document_name = document.get(
                "document",
                "Research Document"
            )

            st.markdown(
                f"## 📄 {document_name}"
            )

            opportunities = document.get(
                "collaboration_opportunities",
                []
            )

            st.markdown(
                "### 🤝 Collaboration Opportunities"
            )

            if opportunities:

                for opportunity in opportunities:

                    st.markdown(

                        f"""
                        <div class="insight-card">

                        <h4>
                        ✨ Hidden Connection Detected
                        </h4>

                        <p>
                        {opportunity}
                        </p>

                        </div>
                        """,

                        unsafe_allow_html=True

                    )

            else:

                st.info(
                    "No collaboration opportunities detected."
                )

            redundancy = document.get(
                "redundancy_risk",
                "Unknown"
            )

            st.markdown(
                "### ⚠️ Redundancy Analysis"
            )

            if redundancy == "High":

                st.error(
                    f"High Redundancy Risk: {redundancy}"
                )

            elif redundancy == "Medium":

                st.warning(
                    f"Medium Redundancy Risk: {redundancy}"
                )

            else:

                st.success(
                    f"Redundancy Risk: {redundancy}"
                )

            topics = document.get(
                "topics",
                []
            )

            if topics:

                st.markdown(
                    "### 🧠 Research Domains"
                )

                st.write(
                    " • ".join(topics)
                )

            st.divider()


        # =============================================
        # CROSS-RESEARCH INTELLIGENCE
        # UPDATE 1
        # =============================================

        if len(
            st.session_state.research_data
        ) >= 2:

            st.markdown(
                "# 🔮 Cross-Research Intelligence"
            )

            st.caption(
                "Discovering direct and semantic relationships "
                "between multiple university research papers."
            )

            documents = (
                st.session_state.research_data
            )

            found_connections = False

            for i in range(
                len(documents)
            ):

                for j in range(
                    i + 1,
                    len(documents)
                ):

                    doc1 = documents[i]
                    doc2 = documents[j]

                    name1 = doc1.get(
                        "document",
                        "Research Paper 1"
                    )

                    name2 = doc2.get(
                        "document",
                        "Research Paper 2"
                    )

                    entities1 = {

                        entity.get(
                            "name",
                            ""
                        ).lower()

                        for entity in doc1.get(
                            "entities",
                            []
                        )

                        if entity.get(
                            "name"
                        )

                    }

                    topics1 = {

                        topic.lower()

                        for topic in doc1.get(
                            "topics",
                            []
                        )

                    }

                    entities2 = {

                        entity.get(
                            "name",
                            ""
                        ).lower()

                        for entity in doc2.get(
                            "entities",
                            []
                        )

                        if entity.get(
                            "name"
                        )

                    }

                    topics2 = {

                        topic.lower()

                        for topic in doc2.get(
                            "topics",
                            []
                        )

                    }

                    shared_entities = (
                        entities1
                        &
                        entities2
                    )

                    shared_topics = (
                        topics1
                        &
                        topics2
                    )

                    paper1_items = (
                        entities1
                        |
                        topics1
                    )

                    paper2_items = (
                        entities2
                        |
                        topics2
                    )

                    concepts1 = (
                        find_concept_connections(
                            paper1_items
                        )
                    )

                    concepts2 = (
                        find_concept_connections(
                            paper2_items
                        )
                    )

                    shared_concepts = (
                        concepts1
                        &
                        concepts2
                    )

                    connection_score, connection_level = (
                        calculate_connection_score(
                            shared_entities,
                            shared_topics,
                            shared_concepts
                        )
                    )

                    if connection_score > 0:

                        found_connections = True

                        related_concepts = (

                            ", ".join(

                                concept.replace(
                                    "_",
                                    " "
                                ).title()

                                for concept
                                in shared_concepts

                            )

                            if shared_concepts

                            else "No semantic concept overlap"

                        )

                        shared_entity_names = (

                            ", ".join(
                                sorted(shared_entities)
                            )

                            if shared_entities

                            else "None"

                        )

                        shared_topic_names = (

                            ", ".join(
                                sorted(shared_topics)
                            )

                            if shared_topics

                            else "None"

                        )

                        st.markdown(

                            f"""
                            <div class="insight-card">

                            <h3>
                            🔗 Potential Research Connection
                            </h3>

                            <p>
                            <b>{name1}</b>
                            ↔
                            <b>{name2}</b>
                            </p>

                            <hr>

                            <p>
                            <b>🧬 Shared Entities:</b>
                            {shared_entity_names}
                            </p>

                            <p>
                            <b>🏷️ Shared Topics:</b>
                            {shared_topic_names}
                            </p>

                            <p>
                            <b>🧠 Related Research Concepts:</b>
                            {related_concepts}
                            </p>

                            <hr>

                            <p>
                            <b>📊 Connection Score:</b>
                            {connection_score}
                            </p>

                            <p>
                            <b>🎯 Connection Level:</b>
                            {connection_level}
                            </p>

                            <p>
                            💡 These papers may have potential
                            for interdisciplinary collaboration.
                            </p>

                            </div>
                            """,

                            unsafe_allow_html=True

                        )

            if not found_connections:

                st.info(
                    "No direct or semantic connections "
                    "were found between the current research papers."
                )

        else:

            st.info(
                "📄 Add at least two research papers to unlock "
                "Cross-Research Intelligence."
            )
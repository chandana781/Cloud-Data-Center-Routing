
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dijkstra import graph, dijkstra
from distance_vector import distance_vector, graph as dv_graph

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Cloud Data Center Network",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Cloud Data Center Network Routing")
st.caption("Intelligent Network Routing using Dijkstra and Distance Vector Algorithms")

routers = list(graph.keys())

# ---------------- SIDEBAR ----------------

st.sidebar.title("Network Controls")

source = st.sidebar.selectbox(
    "Select Source Router",
    routers,
    index=0
)

destination = st.sidebar.selectbox(
    "Select Destination Router",
    routers,
    index=4
)

# ---------------- ROUTING CALCULATIONS ----------------

shortest_path, total_cost = dijkstra(
    graph, source, destination
)

routing_tables, iterations = distance_vector(dv_graph)

# ---------------- NETWORK OVERVIEW ----------------

st.subheader("Network Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Routers", len(routers))
col2.metric(
    "Total Connections",
    sum(len(v) for v in graph.values()) // 2
)
col3.metric("Source Router", source)
col4.metric("Destination Router", destination)

# ---------------- NETWORK TOPOLOGY ----------------

st.subheader("Interactive Network Topology")

positions = {
    'R1': (0, 2),
    'R2': (2, 3),
    'R3': (2, 1),
    'R4': (4, 2),
    'R5': (6, 2)
}

path_edges = set()

if shortest_path:
    for i in range(len(shortest_path) - 1):
        path_edges.add(
            tuple(sorted((shortest_path[i], shortest_path[i + 1])))
        )

fig = go.Figure()

# Draw network links
drawn_edges = set()

for router, neighbors in graph.items():
    for neighbor, cost in neighbors:

        edge = tuple(sorted((router, neighbor)))

        if edge in drawn_edges:
            continue

        drawn_edges.add(edge)

        x1, y1 = positions[router]
        x2, y2 = positions[neighbor]

        is_path = edge in path_edges

        fig.add_trace(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode="lines",
            line=dict(
                color="#00E5FF" if is_path else "#64748B",
                width=5 if is_path else 2
            ),
            hoverinfo="text",
            text=f"{router} ↔ {neighbor} | Cost: {cost}",
            showlegend=False
        ))

        fig.add_annotation(
            x=(x1 + x2) / 2,
            y=(y1 + y2) / 2 + 0.13,
            text=str(cost),
            showarrow=False,
            font=dict(color="white", size=13),
            bgcolor="#334155",
            borderpad=4
        )

# Draw routers
for router, (x, y) in positions.items():

    if router == source:
        color = "#22C55E"
    elif router == destination:
        color = "#F97316"
    elif shortest_path and router in shortest_path:
        color = "#00E5FF"
    else:
        color = "#6366F1"

    fig.add_trace(go.Scatter(
        x=[x],
        y=[y],
        mode="markers+text",
        marker=dict(
            size=55,
            color=color,
            line=dict(color="white", width=2)
        ),
        text=[router],
        textposition="middle center",
        textfont=dict(color="white", size=15),
        hovertemplate=f"<b>{router}</b><extra></extra>",
        showlegend=False
    ))

fig.update_layout(
    height=480,
    paper_bgcolor="#0F172A",
    plot_bgcolor="#0F172A",
    font=dict(color="white"),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    margin=dict(l=20, r=20, t=20, b=20),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- DIJKSTRA RESULTS ----------------

st.subheader("Dijkstra Shortest Path Analysis")

if shortest_path is not None:

    c1, c2, c3 = st.columns(3)

    c1.metric("Minimum Path Cost", total_cost)
    c2.metric("Routers in Path", len(shortest_path))
    c3.metric("Hops", len(shortest_path) - 1)

    st.success(
        "Shortest Path: " + " → ".join(shortest_path)
    )

    st.markdown("### Path Sequence")

    st.write(" → ".join(shortest_path))

else:
    st.error("No route exists between selected routers.")

# ---------------- DISTANCE VECTOR ----------------

st.subheader("Distance Vector Routing")

st.write(
    f"Routing algorithm converged after **{iterations} iterations**."
)

selected_router = st.selectbox(
    "View Routing Table",
    routers,
    key="routing_router"
)

table_data = []

for dest, (cost, hop) in routing_tables[selected_router].items():

    table_data.append({
        "Destination": dest,
        "Minimum Cost": cost if cost != float("inf") else "Infinity",
        "Next Hop": hop
    })

st.dataframe(
    pd.DataFrame(table_data),
    use_container_width=True,
    hide_index=True
)

# ---------------- ALL ROUTING TABLES ----------------

with st.expander("View All Router Routing Tables"):

    for router in routers:

        st.markdown(f"### Router {router}")

        rows = []

        for dest, (cost, hop) in routing_tables[router].items():

            rows.append({
                "Destination": dest,
                "Cost": cost if cost != float("inf") else "Infinity",
                "Next Hop": hop
            })

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

# ---------------- PERFORMANCE ANALYSIS ----------------

st.subheader("Performance Analysis")

cost_data = []

for router in routers:

    path, cost = dijkstra(graph, source, router)

    cost_data.append({
        "Destination Router": router,
        "Minimum Cost": cost if cost != float("inf") else 0
    })

df = pd.DataFrame(cost_data)

st.markdown("### Shortest Path Cost from Source Router")

chart = go.Figure()

chart.add_trace(go.Bar(
    x=df["Destination Router"],
    y=df["Minimum Cost"],
    marker_color="#06B6D4"
))

chart.update_layout(
    paper_bgcolor="#0F172A",
    plot_bgcolor="#0F172A",
    font=dict(color="white"),
    xaxis_title="Destination Router",
    yaxis_title="Minimum Path Cost",
    height=350
)

st.plotly_chart(chart, use_container_width=True)

# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "Cloud Data Center Network Routing | "
    "Dijkstra's Algorithm | Distance Vector Routing"
)

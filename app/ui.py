import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from triage import triage_incident
from history import (
    save_incident,
    load_incidents,
    update_incident_status,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Incident Triage Assistant",
    page_icon="🚨",
    layout="wide"
)


# =========================================================
# GLOBAL STYLE (dark IncidentOps look)
# =========================================================

st.markdown(
    """
    <style>

    html, body, .stApp {
        background-color: #0a0d14;
        color: #e7e9f2;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 1.2rem;
        max-width: 1400px;
    }

    /* ---------- sidebar ---------- */
    section[data-testid="stSidebar"] {
        background-color: #0d1019;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 4px 6px 10px 6px;
    }
    .brand-icon {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: linear-gradient(135deg, #6d5ef7, #a855f7);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 17px;
    }
    .brand-title {
        font-size: 19px;
        font-weight: 800;
        color: #f4f5fb;
        letter-spacing: -0.3px;
    }

    section[data-testid="stSidebar"] .stRadio > label {
        display: none;
    }
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 4px;
    }
    section[data-testid="stSidebar"] .stRadio > div > label {
        padding: 9px 12px;
        border-radius: 10px;
        width: 100%;
        margin: 0;
    }
    section[data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(255,255,255,0.04);
    }

    /* ---------- hero header ---------- */
    .hero {
        padding: 26px 30px;
        border-radius: 18px;
        background: linear-gradient(120deg, #6d5ef7 0%, #d6469b 55%, #f97316 100%);
        box-shadow: 0 10px 30px rgba(124,58,237,0.25);
        margin-bottom: 22px;
    }
    .hero h1 {
        margin: 0;
        color: white;
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .hero p {
        margin: 6px 0 0 0;
        color: rgba(255,255,255,0.92);
        font-size: 14.5px;
        max-width: 640px;
    }

    /* ---------- section heading ---------- */
    .section-head {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 4px 0 2px 0;
    }
    .section-icon {
        width: 30px;
        height: 30px;
        border-radius: 8px;
        background: rgba(124,58,237,0.18);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .section-head h2 {
        font-size: 21px;
        margin: 0;
        color: #f4f5fb;
    }
    .section-sub {
        color: #7d84a0;
        font-size: 13px;
        margin: 2px 0 16px 40px;
    }

    /* ---------- kpi cards ---------- */
    .kpi-card {
        border-radius: 16px;
        padding: 18px 18px;
        border: 1px solid rgba(255,255,255,0.07);
        background: linear-gradient(160deg, rgba(255,255,255,0.045), rgba(255,255,255,0.01));
        position: relative;
        min-height: 100px;
    }
    .kpi-icon {
        position: absolute;
        top: 16px;
        right: 16px;
        width: 34px;
        height: 34px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
    }
    .kpi-label {
        font-size: 13px;
        color: #9aa0bb;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 30px;
        font-weight: 800;
        color: #f4f5fb;
        line-height: 1;
    }

    /* ---------- chart panels ---------- */
    .panel {
        border-radius: 16px;
        padding: 18px 20px 8px 20px;
        border: 1px solid rgba(255,255,255,0.07);
        background: linear-gradient(160deg, rgba(255,255,255,0.035), rgba(255,255,255,0.01));
    }
    .panel-title {
        font-size: 15px;
        font-weight: 700;
        color: #f1f2f8;
        margin-bottom: 6px;
    }

    /* ---------- incident cards ---------- */
    .incident-card {
        border-radius: 16px;
        padding: 18px 20px;
        margin-bottom: 14px;
        background: linear-gradient(160deg, rgba(255,255,255,0.045), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.08);
        border-left: 4px solid #7c3aed;
    }
    .incident-title {
        font-size: 18px;
        font-weight: 700;
        color: #f1f2f8;
        margin-bottom: 6px;
    }
    .meta-row {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 8px;
    }

    /* ---------- badges ---------- */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.3px;
        border: 1px solid rgba(255,255,255,0.12);
    }
    .badge-CRITICAL { background: rgba(239,68,68,0.18); color: #fca5a5; border-color: rgba(239,68,68,0.4); }
    .badge-HIGH     { background: rgba(249,115,22,0.18); color: #fdba74; border-color: rgba(249,115,22,0.4); }
    .badge-MEDIUM   { background: rgba(234,179,8,0.18);  color: #fde047; border-color: rgba(234,179,8,0.4); }
    .badge-LOW      { background: rgba(34,197,94,0.18);  color: #86efac; border-color: rgba(34,197,94,0.4); }

    .badge-OPEN          { background: rgba(59,130,246,0.18); color: #93c5fd; border-color: rgba(59,130,246,0.4); }
    .badge-INVESTIGATING { background: rgba(168,85,247,0.18); color: #d8b4fe; border-color: rgba(168,85,247,0.4); }
    .badge-RESOLVED      { background: rgba(34,197,94,0.18);  color: #86efac; border-color: rgba(34,197,94,0.4); }
    .badge-CLOSED        { background: rgba(148,163,184,0.18);color: #cbd5e1; border-color: rgba(148,163,184,0.4); }

    .badge-P1 { background: rgba(239,68,68,0.18); color: #fca5a5; border-color: rgba(239,68,68,0.4); }
    .badge-P2 { background: rgba(249,115,22,0.18); color: #fdba74; border-color: rgba(249,115,22,0.4); }
    .badge-P3 { background: rgba(234,179,8,0.18);  color: #fde047; border-color: rgba(234,179,8,0.4); }
    .badge-P4 { background: rgba(34,197,94,0.18);  color: #86efac; border-color: rgba(34,197,94,0.4); }
    .badge-NA { background: rgba(148,163,184,0.18); color: #cbd5e1; border-color: rgba(148,163,184,0.4); }

    .pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 12.5px;
        background: rgba(255,255,255,0.06);
        color: #cdd1e0;
        margin-right: 4px;
    }

    /* ---------- recent incidents table ---------- */
    .table-wrap {
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.07);
        overflow: hidden;
    }
    .table-head, .table-row {
        display: grid;
        grid-template-columns: 2fr 1.3fr 1fr 1fr 1fr;
        align-items: center;
        padding: 12px 18px;
        gap: 10px;
    }
    .table-head {
        background: rgba(255,255,255,0.03);
        color: #7d84a0;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 700;
    }
    .table-row {
        border-top: 1px solid rgba(255,255,255,0.05);
        font-size: 13.5px;
        color: #dfe1ec;
    }
    .table-row:hover {
        background: rgba(255,255,255,0.02);
    }

    /* ---------- buttons ---------- */
    .stButton > button {
        border-radius: 12px;
        border: none;
        background: linear-gradient(120deg, #6d5ef7, #d6469b);
        color: white;
        font-weight: 700;
        padding: 10px 18px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        box-shadow: 0 6px 18px rgba(124,58,237,0.25);
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 24px rgba(124,58,237,0.35);
    }

    /* ---------- inputs ---------- */
    .stTextInput input, .stTextArea textarea, .stNumberInput input,
    div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.04) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #e6e8ef !important;
    }

    .stExpander {
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: rgba(255,255,255,0.02) !important;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(160deg, rgba(255,255,255,0.045), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 14px 16px;
    }

    hr, .stDivider { border-color: rgba(255,255,255,0.08) !important; }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HELPERS
# =========================================================

def badge(value, prefix=""):
    """Render a colored pill badge for severity / status / priority."""
    clean = str(value or "N/A").upper().strip()
    valid = [
        "CRITICAL", "HIGH", "MEDIUM", "LOW",
        "OPEN", "INVESTIGATING", "RESOLVED", "CLOSED",
        "P1", "P2", "P3", "P4"
    ]
    css_class = f"badge-{clean}" if clean in valid else "badge-NA"
    return f'<span class="badge {css_class}">{prefix}{clean}</span>'


def render_incident_card(incident):
    st.markdown(
        f"""
        <div class="incident-card">
            <div class="incident-title">🧩 {incident.get('title', 'Untitled Incident')}</div>
            <div class="meta-row">
                {badge(incident.get('severity'))}
                {badge(incident.get('priority'))}
                {badge(incident.get('status', 'OPEN'))}
                <span class="pill">🛠 {incident.get('affected_service', 'N/A')}</span>
                <span class="pill">🌐 {incident.get('environment', 'N/A')}</span>
                <span class="pill">📂 {incident.get('category', 'N/A')}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def kpi_card(label, value, icon, icon_bg, icon_color):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon" style="background:{icon_bg}; color:{icon_color};">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def severity_bar_chart(incidents):
    order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    colors_map = {
        "CRITICAL": "#ef4444",
        "HIGH": "#f97316",
        "MEDIUM": "#eab308",
        "LOW": "#22c55e",
    }
    sev_counts = pd.Series(
        [str(i.get("severity", "N/A")).upper() for i in incidents]
    ).value_counts()

    values = [int(sev_counts.get(label, 0)) for label in order]
    colors = [colors_map[label] for label in order]

    fig = go.Figure(
        data=[go.Bar(
            x=order,
            y=values,
            marker_color=colors,
            text=values,
            textposition="outside",
        )]
    )
    fig.update_layout(
        margin=dict(t=20, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        yaxis=dict(showgrid=False, color="#7d84a0"),
        xaxis=dict(showgrid=False, color="#dfe1ec"),
        font=dict(color="#dfe1ec"),
    )
    return fig


def status_donut_chart(incidents):
    colors_map = {
        "OPEN": "#3b82f6",
        "INVESTIGATING": "#a855f7",
        "RESOLVED": "#22c55e",
        "CLOSED": "#94a3b8",
    }

    status_counts = pd.Series(
        [str(i.get("status", "OPEN")).upper() for i in incidents]
    ).value_counts()

    labels = list(status_counts.index)
    values = list(status_counts.values)
    colors = [colors_map.get(label, "#64748b") for label in labels]

    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.62,
            marker=dict(colors=colors, line=dict(color="#0a0d14", width=2)),
            textinfo="none",
        )]
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(font=dict(color="#dfe1ec", size=12)),
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        annotations=[dict(
            text=f"<b>{sum(values)}</b><br><span style='font-size:12px;color:#9aa0bb'>Total</span>",
            x=0.5, y=0.5, font=dict(size=22, color="#f4f5fb"), showarrow=False
        )],
    )
    return fig


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div class="brand-row">
        <div class="brand-icon">⚡</div>
        <div class="brand-title">IncidentOps</div>
    </div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Navigation",
    [
        "📊  Dashboard",
        "📝  Create Incident",
        "📋  Incident History",
        "🔎  Search Incidents",
        "🔄  Update Status"
    ],
    label_visibility="collapsed"
)
page = page.split("  ", 1)[1]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>🚨 AI Incident Triage Assistant</h1>
        <p>Analyze incidents, assign priority, generate AI insights and manage incident history from one place.</p>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown(
        """
        <div class="section-head">
            <div class="section-icon">📊</div>
            <h2>Dashboard</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    incidents = load_incidents()

    total = len(incidents)

    critical = sum(
        1
        for incident in incidents
        if str(incident.get("severity", "")).upper() == "CRITICAL"
    )

    high = sum(
        1
        for incident in incidents
        if str(incident.get("severity", "")).upper() == "HIGH"
    )

    open_incidents = sum(
        1
        for incident in incidents
        if str(incident.get("status", "OPEN")).upper() == "OPEN"
    )

    resolved = sum(
        1
        for incident in incidents
        if str(incident.get("status", "")).upper() == "RESOLVED"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        kpi_card("Total Incidents", total, "📄", "rgba(124,58,237,0.18)", "#c4b5fd")
    with col2:
        kpi_card("Critical", critical, "🛡️", "rgba(239,68,68,0.18)", "#fca5a5")
    with col3:
        kpi_card("High", high, "⬆️", "rgba(249,115,22,0.18)", "#fdba74")
    with col4:
        kpi_card("Open", open_incidents, "🔄", "rgba(59,130,246,0.18)", "#93c5fd")
    with col5:
        kpi_card("Resolved", resolved, "✅", "rgba(34,197,94,0.18)", "#86efac")

    st.write("")

    if incidents:

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">Severity Breakdown</div>', unsafe_allow_html=True)
            st.plotly_chart(severity_bar_chart(incidents), use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

        with chart_col2:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">Status Breakdown</div>', unsafe_allow_html=True)
            st.plotly_chart(status_donut_chart(incidents), use_container_width=True, config={"displayModeBar": False})
            st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    st.markdown(
        """
        <div class="section-head">
            <div class="section-icon">🕒</div>
            <h2 style="font-size:18px;">Recent Incidents</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not incidents:

        st.info(
            "No incidents available. Create your first incident."
        )

    else:

        recent_incidents = incidents[-5:]

        rows_html = ""
        for incident in reversed(recent_incidents):
            row_title = incident.get("title", "Untitled Incident")
            row_service = incident.get("affected_service", "N/A")
            row_severity = badge(incident.get("severity"))
            row_priority = badge(incident.get("priority"))
            row_status = badge(incident.get("status", "OPEN"))

            rows_html += (
                '<div class="table-row">'
                f'<div>{row_title}</div>'
                f'<div>{row_service}</div>'
                f'<div>{row_severity}</div>'
                f'<div>{row_priority}</div>'
                f'<div>{row_status}</div>'
                '</div>'
            )

        st.markdown(
            f"""
            <div class="table-wrap">
                <div class="table-head">
                    <div>Title</div>
                    <div>Service</div>
                    <div>Severity</div>
                    <div>Priority</div>
                    <div>Status</div>
                </div>
                {rows_html}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# CREATE INCIDENT
# =========================================================

elif page == "Create Incident":

    st.markdown(
        """
        <div class="section-head">
            <div class="section-icon">📝</div>
            <h2>Create New Incident</h2>
        </div>
        <div class="section-sub">The triage engine will determine category, severity and priority.</div>
        """,
        unsafe_allow_html=True
    )

    title = st.text_input(
        "Incident Title",
        placeholder="Example: Production Database Down"
    )

    description = st.text_area(
        "Incident Description",
        placeholder=(
            "Describe what happened, the symptoms "
            "and the impact..."
        ),
        height=150
    )

    col1, col2 = st.columns(2)

    with col1:

        affected_service = st.text_input(
            "Affected Service",
            placeholder="Example: Production Database"
        )

        affected_users = st.number_input(
            "Affected Users",
            min_value=0,
            value=1,
            step=1
        )

        environment = st.selectbox(
            "Environment",
            [
                "Production",
                "Staging",
                "Development",
                "Testing"
            ]
        )

    with col2:

        category = st.selectbox(
            "Initial Category",
            [
                "Application",
                "Database",
                "Network",
                "Security",
                "Infrastructure",
                "Other"
            ]
        )

    st.divider()

    analyze = st.button(
        "🔍 Analyze & Save Incident",
        use_container_width=True
    )

    if analyze:

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not title.strip():

            st.error(
                "Please enter an incident title."
            )

        elif not description.strip():

            st.error(
                "Please enter an incident description."
            )

        elif not affected_service.strip():

            st.error(
                "Please enter the affected service."
            )

        else:

            incident = {
                "title": title.strip(),
                "description": description.strip(),
                "affected_service": affected_service.strip(),
                "affected_users": int(affected_users),
                "environment": environment,
                "category": category
            }

            # -------------------------------------------------
            # TRIAGE
            # -------------------------------------------------

            try:

                result = triage_incident(incident)

                if not isinstance(result, dict):

                    st.error(
                        "Triage engine returned an unexpected result."
                    )

                    st.stop()

                incident["category"] = result.get(
                    "category",
                    category
                )

                incident["severity"] = result.get(
                    "severity",
                    "MEDIUM"
                )

                incident["priority"] = result.get(
                    "priority",
                    "P3"
                )

                # Optional AI analysis
                if result.get("ai_analysis"):

                    incident["ai_analysis"] = result.get(
                        "ai_analysis"
                    )

            except Exception as error:

                st.error(
                    f"Triage failed: {error}"
                )

                st.stop()

            # -------------------------------------------------
            # DEFAULT STATUS
            # -------------------------------------------------

            incident["status"] = "OPEN"

            # -------------------------------------------------
            # DISPLAY TRIAGE RESULT
            # -------------------------------------------------

            st.success(
                "Incident analyzed successfully."
            )

            st.subheader("🎯 Triage Result")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Category",
                incident["category"]
            )

            col2.metric(
                "Severity",
                incident["severity"]
            )

            col3.metric(
                "Priority",
                incident["priority"]
            )

            # -------------------------------------------------
            # AI ANALYSIS
            # -------------------------------------------------

            if incident.get("ai_analysis"):

                st.subheader("🤖 AI Analysis")

                st.info(
                    incident["ai_analysis"]
                )

            # -------------------------------------------------
            # SAVE INCIDENT
            # -------------------------------------------------

            try:

                save_incident(incident)

                st.success(
                    "Incident saved successfully."
                )

            except Exception as error:

                st.error(
                    f"Unable to save incident: {error}"
                )


# =========================================================
# INCIDENT HISTORY
# =========================================================

elif page == "Incident History":

    st.markdown(
        """
        <div class="section-head">
            <div class="section-icon">📋</div>
            <h2>Incident History</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    incidents = load_incidents()

    if not incidents:

        st.info(
            "No incidents found."
        )

    else:

        st.write(
            f"Total incidents: **{len(incidents)}**"
        )

        st.divider()

        for index, incident in enumerate(
            incidents,
            start=1
        ):

            title = incident.get(
                "title",
                "Untitled"
            )

            priority = incident.get(
                "priority",
                "N/A"
            )

            with st.expander(
                f"{index}. {title} • {priority}"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Service:** "
                        f"{incident.get('affected_service', 'N/A')}"
                    )

                    st.write(
                        f"**Affected Users:** "
                        f"{incident.get('affected_users', 'N/A')}"
                    )

                    st.write(
                        f"**Environment:** "
                        f"{incident.get('environment', 'N/A')}"
                    )

                    st.write(
                        f"**Category:** "
                        f"{incident.get('category', 'N/A')}"
                    )

                with col2:

                    st.markdown(
                        f"**Severity:** {badge(incident.get('severity'))}",
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"**Priority:** {badge(incident.get('priority'))}",
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"**Status:** {badge(incident.get('status', 'OPEN'))}",
                        unsafe_allow_html=True
                    )

                st.markdown("### Description")

                st.write(
                    incident.get(
                        "description",
                        "No description available."
                    )
                )

                if incident.get("ai_analysis"):

                    st.markdown("### 🤖 AI Analysis")

                    st.info(
                        incident["ai_analysis"]
                    )


# =========================================================
# SEARCH INCIDENTS
# =========================================================

elif page == "Search Incidents":

    st.markdown(
        """
        <div class="section-head">
            <div class="section-icon">🔎</div>
            <h2>Search Incidents</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    incidents = load_incidents()

    keyword = st.text_input(
        "Search by title or affected service",
        placeholder="Example: database"
    )

    if keyword.strip():

        search_keyword = keyword.lower().strip()

        results = []

        for incident in incidents:

            title = str(
                incident.get("title", "")
            ).lower()

            service = str(
                incident.get("affected_service", "")
            ).lower()

            if (
                search_keyword in title
                or search_keyword in service
            ):

                results.append(incident)

        if not results:

            st.warning(
                "No matching incidents found."
            )

        else:

            st.success(
                f"{len(results)} incident(s) found."
            )

            for incident in results:
                render_incident_card(incident)


# =========================================================
# UPDATE STATUS
# =========================================================

elif page == "Update Status":

    st.markdown(
        """
        <div class="section-head">
            <div class="section-icon">🔄</div>
            <h2>Update Incident Status</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    incidents = load_incidents()

    if not incidents:

        st.info(
            "No incidents available."
        )

    else:

        incident_names = []

        for index, incident in enumerate(
            incidents,
            start=1
        ):

            incident_names.append(
                f"{index}. "
                f"{incident.get('title', 'Untitled')}"
            )

        selected = st.selectbox(
            "Select Incident",
            incident_names
        )

        incident_number = (
            incident_names.index(selected) + 1
        )

        selected_incident = incidents[
            incident_number - 1
        ]

        st.markdown(
            f"**Current Status:** {badge(selected_incident.get('status', 'OPEN'))}",
            unsafe_allow_html=True
        )

        new_status = st.selectbox(
            "New Status",
            [
                "OPEN",
                "INVESTIGATING",
                "RESOLVED",
                "CLOSED"
            ]
        )

        if st.button(
            "Update Status",
            use_container_width=True
        ):

            current_status = str(
                selected_incident.get(
                    "status",
                    "OPEN"
                )
            ).upper()

            if current_status == new_status:

                st.warning(
                    f"Incident is already {new_status}."
                )

            else:

                try:

                    update_incident_status(
                        incident_number,
                        new_status
                    )

                    st.success(
                        f"Incident status changed to {new_status}."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Status update failed: {error}"
                    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Incident Triage Assistant • "
    "Incident management and intelligent triage"
)

import streamlit as st
import pandas as pd
import plotly.express as px
from app.database import initialize, save_scan, get_scans, clear_scans, load_demo_scans
from app.scanner import inspect
from app.reports import make_report

st.set_page_config(
    page_title="GhostTrace | Digital Privacy Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize()

# Professional Dark Navy & Cyber Cyan Theme
st.markdown("""
<style>
/* Main Layout & Density */
.block-container {
    padding-top: 2.6rem;
    padding-bottom: 2rem;
    max-width: 1350px;
}
header[data-testid="stHeader"] {
    background: rgba(8, 15, 30, 0.6) !important;
}

/* Compact Cyber Header */
.gt-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    padding: 12px 20px;
    background: linear-gradient(135deg, rgba(14, 26, 46, 0.95) 0%, rgba(9, 18, 33, 0.95) 100%);
    border: 1px solid rgba(34, 211, 238, 0.22);
    border-radius: 12px;
    margin-bottom: 1.25rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}
.gt-header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}
.gt-logo-icon {
    font-size: 1.75rem;
    line-height: 1;
}
.gt-title {
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    color: #f1f5f9;
    line-height: 1.2;
}
.gt-cyan {
    color: #22d3ee;
}
.gt-badge {
    font-size: 0.68rem;
    padding: 2px 7px;
    border-radius: 6px;
    background: rgba(34, 211, 238, 0.15);
    border: 1px solid rgba(34, 211, 238, 0.35);
    color: #38bdf8;
    font-weight: 600;
    vertical-align: middle;
}
.gt-subtitle {
    font-size: 0.73rem;
    letter-spacing: 0.07em;
    color: #94a3b8;
    margin-top: 2px;
}
.gt-status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    font-weight: 600;
    color: #34d399;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.28);
    padding: 5px 11px;
    border-radius: 20px;
}
.gt-status-dot {
    width: 6px;
    height: 6px;
    background: #34d399;
    border-radius: 50%;
    box-shadow: 0 0 6px #34d399;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(14, 27, 46, 0.9) 0%, rgba(10, 20, 36, 0.95) 100%) !important;
    border: 1px solid rgba(34, 211, 238, 0.18) !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
    transition: border-color 0.2s ease, transform 0.2s ease;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(34, 211, 238, 0.38) !important;
    transform: translateY(-1px);
}
[data-testid="stMetricLabel"] {
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #94a3b8 !important;
}
[data-testid="stMetricValue"] {
    color: #22d3ee !important;
    font-weight: 700 !important;
    font-size: 1.65rem !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: #091222 !important;
    border-right: 1px solid rgba(34, 211, 238, 0.12) !important;
}
.gt-sidebar-brand {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 0 12px 0;
    font-size: 1.15rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: #f1f5f9;
}
.gt-sidebar-card {
    background: rgba(17, 30, 50, 0.7);
    border: 1px solid rgba(34, 211, 238, 0.15);
    border-radius: 10px;
    padding: 10px 12px;
    margin-top: 12px;
}

/* Button & Action Styling */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%) !important;
    color: #ffffff !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    box-shadow: 0 3px 12px rgba(6, 182, 212, 0.3) !important;
    transition: all 0.2s ease !important;
}
div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 4px 18px rgba(6, 182, 212, 0.5) !important;
    transform: translateY(-1px) !important;
}
div.stButton > button[kind="secondary"], div.stDownloadButton > button {
    background: rgba(17, 30, 50, 0.75) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(34, 211, 238, 0.3) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
div.stButton > button[kind="secondary"]:hover, div.stDownloadButton > button:hover {
    border-color: #22d3ee !important;
    color: #ffffff !important;
    background: rgba(34, 211, 238, 0.12) !important;
}

/* Informative Cards & Callouts */
.gt-info-box {
    background: rgba(14, 26, 46, 0.7);
    border: 1px solid rgba(34, 211, 238, 0.16);
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 1rem;
}

/* Small Professional Footer */
.gt-footer {
    text-align: center;
    padding: 22px 0 10px 0;
    margin-top: 35px;
    border-top: 1px solid rgba(34, 211, 238, 0.14);
    font-size: 0.82rem;
    letter-spacing: 0.05em;
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# Compact Header
st.markdown("""
<div class="gt-header-bar">
    <div class="gt-header-left">
        <div class="gt-logo-icon">🛡️</div>
        <div>
            <div class="gt-title">GHOST<span class="gt-cyan">TRACE</span> <span class="gt-badge">v1.0</span></div>
            <div class="gt-subtitle">DIGITAL PRIVACY INTELLIGENCE • LOCAL FORENSIC ENCLAVE</div>
        </div>
    </div>
    <div class="gt-header-right">
        <span class="gt-status-pill"><span class="gt-status-dot"></span>LOCAL ENCLAVE • OFFLINE ONLY</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown(
    '<div class="gt-sidebar-brand"><span>🛡️</span> GHOST<span style="color:#22d3ee;">TRACE</span></div>',
    unsafe_allow_html=True
)
page = st.sidebar.radio("NAVIGATION", ["📊 Overview", "🔎 Scan Center", "🗃️ Scan History", "ℹ️ About"], label_visibility="visible")
st.sidebar.divider()

st.sidebar.markdown("""
<div class="gt-sidebar-card">
    <div style="font-size:0.75rem;font-weight:700;color:#38bdf8;margin-bottom:3px;">🔒 LOCAL PROCESSING</div>
    <div style="font-size:0.72rem;color:#94a3b8;line-height:1.4;">Zero cloud transmission. All parsing, hashing, and regex extraction occur entirely in local memory.</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
if st.sidebar.button("📥 Load 50 demo records", use_container_width=True):
    count = load_demo_scans()
    if count:
        st.sidebar.success(f"Imported {count} demo records")
    else:
        st.sidebar.info("Demo records already loaded")
    st.rerun()

st.sidebar.caption("🧪 Demo records are synthetic benchmarks for interface testing.")

df = get_scans()

# -------------------------------------------------------------
# PAGE 1: OVERVIEW DASHBOARD
# -------------------------------------------------------------
if page == "📊 Overview":
    st.subheader("Security Telemetry Overview")
    total = len(df)
    high = int(df["risk"].isin(["High", "Critical"]).sum()) if total else 0
    avg = round(df["score"].mean(), 1) if total else 0
    unique_hashes = int(df["sha256"].nunique()) if total else 0

    # KPI Metric Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Scans", total)
    kpi2.metric("High / Critical Risk", high)
    kpi3.metric("Average Risk Score", f"{avg}/100")
    kpi4.metric("Unique File Hashes", unique_hashes)

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    if total:
        left, right = st.columns(2)
        with left:
            counts = df["risk"].value_counts().rename_axis("Risk").reset_index(name="Scans")
            fig_pie = px.pie(
                counts,
                names="Risk",
                values="Scans",
                hole=0.62,
                color="Risk",
                color_discrete_map={
                    "Low": "#10b981",
                    "Medium": "#f59e0b",
                    "High": "#f43f5e",
                    "Critical": "#dc2626"
                }
            )
            fig_pie.update_traces(
                textposition="inside",
                textinfo="percent+label",
                marker=dict(line=dict(color="#091222", width=2))
            )
            fig_pie.update_layout(
                title=dict(text="<b>Risk Classification Distribution</b>", font=dict(color="#e2e8f0", size=15)),
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=300,
                margin=dict(l=15, r=15, t=45, b=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5,
                    font=dict(color="#94a3b8", size=11)
                )
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with right:
            daily = df.copy()
            daily["Date"] = pd.to_datetime(daily["scanned_at"]).dt.date.astype(str)
            daily = daily.groupby("Date").size().reset_index(name="Scans")
            fig_bar = px.bar(
                daily,
                x="Date",
                y="Scans",
                title="<b>Scan Activity Velocity</b>",
                color_discrete_sequence=["#22d3ee"]
            )
            fig_bar.update_traces(
                marker=dict(line=dict(color="#38bdf8", width=1), opacity=0.9)
            )
            fig_bar.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=300,
                margin=dict(l=15, r=15, t=45, b=20),
                xaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94a3b8", size=11)),
                yaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94a3b8", size=11)),
                title=dict(font=dict(color="#e2e8f0", size=15))
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("#### 🕒 Recent Forensic Scans")
        st.dataframe(
            df[["scanned_at", "filename", "filetype", "risk", "score"]].head(8),
            use_container_width=True,
            hide_index=True,
            column_config={
                "scanned_at": st.column_config.TextColumn("Timestamp"),
                "filename": st.column_config.TextColumn("Filename"),
                "filetype": st.column_config.TextColumn("Format", width="small"),
                "risk": st.column_config.TextColumn("Risk Rating"),
                "score": st.column_config.ProgressColumn(
                    "Exposure Score",
                    min_value=0,
                    max_value=100,
                    format="%d / 100"
                )
            }
        )
    else:
        st.info("No scans recorded yet. Open Scan Center to analyze your first file or click 'Load 50 demo records' in the sidebar.")

# -------------------------------------------------------------
# PAGE 2: SCAN CENTER
# -------------------------------------------------------------
elif page == "🔎 Scan Center":
    st.subheader("Analyze File Exposure")

    st.markdown("""
    <div class="gt-info-box">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <div style="display:flex; gap:6px; align-items:center;">
                <span style="font-size:0.75rem; font-weight:700; color:#94a3b8; text-transform:uppercase;">Formats:</span>
                <span style="background:rgba(34,211,238,0.15); border:1px solid rgba(34,211,238,0.3); color:#38bdf8; font-size:0.72rem; padding:2px 7px; border-radius:4px; font-weight:600;">PDF</span>
                <span style="background:rgba(34,211,238,0.15); border:1px solid rgba(34,211,238,0.3); color:#38bdf8; font-size:0.72rem; padding:2px 7px; border-radius:4px; font-weight:600;">TXT</span>
                <span style="background:rgba(34,211,238,0.15); border:1px solid rgba(34,211,238,0.3); color:#38bdf8; font-size:0.72rem; padding:2px 7px; border-radius:4px; font-weight:600;">PNG</span>
                <span style="background:rgba(34,211,238,0.15); border:1px solid rgba(34,211,238,0.3); color:#38bdf8; font-size:0.72rem; padding:2px 7px; border-radius:4px; font-weight:600;">JPG / JPEG</span>
            </div>
            <span style="font-size:0.74rem; color:#34d399; font-weight:600;">🔒 Up to 25 MB • Zero Remote Network Uploads</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Select or drop a file to inspect", type=["pdf", "txt", "png", "jpg", "jpeg"])

    if uploaded:
        col_btn, _ = st.columns([1, 2])
        with col_btn:
            analyze_clicked = st.button("🔍 Analyze Privacy Exposure", type="primary", use_container_width=True)

        if analyze_clicked:
            try:
                with st.spinner("Inspecting file artifacts locally in memory..."):
                    result = inspect(uploaded.name, uploaded.getvalue())
                    save_scan(
                        result["filename"],
                        result["filetype"],
                        result["sha256"],
                        result["risk"],
                        result["score"],
                        result["findings"]
                    )
                    st.session_state["result"] = result
                st.success("✅ Analysis complete. Findings securely logged to local database.")
            except Exception as e:
                st.error(f"Scan failed: {e}")

    if "result" in st.session_state:
        r = st.session_state["result"]
        st.divider()

        # Risk Score Banner
        risk_color_map = {
            "Low": "#10b981",
            "Medium": "#f59e0b",
            "High": "#f43f5e",
            "Critical": "#dc2626"
        }
        r_color = risk_color_map.get(r["risk"], "#38bdf8")

        res1, res2, res3 = st.columns(3)
        res1.metric("Evaluated Risk Rating", r["risk"])
        res2.metric("Privacy Exposure Score", f'{r["score"]} / 100')
        res3.metric("Detected Risk Indicators", len(r["findings"]))

        st.progress(r["score"] / 100)

        # File Fingerprint Section
        st.markdown("**🔐 SHA-256 File Fingerprint**")
        st.code(r["sha256"], language="text")

        # Professional Findings Table
        st.markdown("#### 📋 Detected Indicators")
        if r["findings"]:
            findings_df = pd.DataFrame(r["findings"])
            st.dataframe(
                findings_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "type": st.column_config.TextColumn("Risk Indicator"),
                    "severity": st.column_config.TextColumn("Severity"),
                    "detail": st.column_config.TextColumn("Forensic Context & Detail"),
                    "count": st.column_config.NumberColumn("Occurrences", format="%d")
                }
            )
        else:
            st.info("🛡️ Clean Scan: No supported sensitive patterns or metadata indicators were found. (Note: Scanned images without OCR are not exhaustively checked).")

        if r["metadata"]:
            with st.expander("🔍 Inspect Embedded Metadata"):
                st.json(r["metadata"])

        st.download_button(
            "📄 Export Official PDF Report",
            make_report(r),
            file_name="ghosttrace_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# -------------------------------------------------------------
# PAGE 3: SCAN HISTORY
# -------------------------------------------------------------
elif page == "🗃️ Scan History":
    st.subheader("Historical Scan Telemetry")
    if df.empty:
        st.info("No scan records available in local database. Analyze files in Scan Center or import synthetic demo scans.")
    else:
        filter_col, count_col = st.columns([2, 1])
        with filter_col:
            risks = st.multiselect(
                "Filter records by risk classification",
                ["Low", "Medium", "High", "Critical"],
                placeholder="Select risk levels to filter..."
            )
        view = df[df["risk"].isin(risks)] if risks else df
        with count_col:
            st.markdown(
                f"<div style='text-align:right; padding-top:28px; font-size:0.85rem; color:#94a3b8;'>Displaying <b>{len(view)}</b> of <b>{len(df)}</b> records</div>",
                unsafe_allow_html=True
            )

        st.dataframe(
            view[["id", "scanned_at", "filename", "filetype", "risk", "score", "sha256"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", width="small"),
                "scanned_at": st.column_config.TextColumn("Timestamp"),
                "filename": st.column_config.TextColumn("Filename"),
                "filetype": st.column_config.TextColumn("Format", width="small"),
                "risk": st.column_config.TextColumn("Risk Rating"),
                "score": st.column_config.ProgressColumn(
                    "Exposure Score",
                    min_value=0,
                    max_value=100,
                    format="%d / 100"
                ),
                "sha256": st.column_config.TextColumn("SHA-256 Fingerprint")
            }
        )

        dl_col, clr_col = st.columns([1, 1])
        with dl_col:
            st.download_button(
                "⬇️ Export History as CSV",
                view.to_csv(index=False).encode("utf-8"),
                file_name="ghosttrace_history.csv",
                mime="text/csv",
                use_container_width=True
            )

        with clr_col:
            with st.expander("⚠️ Database Maintenance (Clear History)"):
                st.caption("This action purges all scan records from the local SQLite database.")
                if st.button("Delete All Scan History", type="secondary", use_container_width=True):
                    clear_scans()
                    st.rerun()

# -------------------------------------------------------------
# PAGE 4: ABOUT GHOSTTRACE
# -------------------------------------------------------------
else:
    st.subheader("About GhostTrace")
    st.markdown("""
    **GhostTrace** is an educational, offline-first digital forensics and privacy intelligence system designed to detect accidental personal data exposure, metadata leakage, and privacy risks in files before dissemination.
    """)

    st.markdown("#### 🔬 Core Inspection Engines")
    col_feat1, col_feat2 = st.columns(2)
    with col_feat1:
        st.markdown("""
        - **Document Metadata Inspection**: Identifies embedded author names, creator software, editing tools, and timestamps in PDF documents.
        - **EXIF & Geolocation Intelligence**: Parses photo camera models, software tags, and GPS coordinates that could expose physical locations.
        """)
    with col_feat2:
        st.markdown("""
        - **Regex Pattern Matching**: Inspects text for exposed email addresses, Indian mobile numbers (+91), PAN-like tax IDs, and IPv4 addresses.
        - **Cryptographic Fingerprinting**: Calculates full SHA-256 cryptographic hashes for forensic integrity and deduplication.
        """)

    st.markdown("#### 🔒 Security & Privacy Architecture")
    st.markdown("""
    - **Zero Cloud Leakage**: Files uploaded to GhostTrace are parsed entirely in local system RAM. Nothing is transmitted over the Internet or stored on external cloud servers.
    - **Local SQLite Persistence**: Only filenames, SHA-256 hashes, summary risk scores, and detected indicator categories are saved to the local database. Raw file contents are never written to disk.
    - **Transparent Scoring**: Heuristic scoring weights severity levels (Low: 10, Medium: 25, High: 40, Critical: 60) to provide an explainable 0–100 privacy exposure index.
    """)

    st.warning("⚠️ **Educational & Forensic Disclaimer**: GhostTrace risk scores are heuristic guidelines and do not constitute certified legal compliance or forensic proof of safety. Text embedded in scanned/raster images without OCR cannot be analyzed. Only inspect files you own or have explicit authorization to audit.")

    st.caption("Technology Stack: Python • Streamlit • SQLite • Pandas • Plotly • Pillow (PIL) • PyMuPDF (fitz) • ReportLab")

# -------------------------------------------------------------
# GLOBAL FOOTER
# -------------------------------------------------------------
st.markdown(
    '<div class="gt-footer">GhostTrace | Digital Privacy Intelligence | TY BSc IT Project</div>',
    unsafe_allow_html=True
)

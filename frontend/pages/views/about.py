import streamlit as st

def render():
    # Modern Glass & Card UI CSS Injection + Bootstrap Icons
    st.markdown("""
        <!-- Bootstrap Icons Link -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

        <style>
        /* Header Styling */
        .about-title {
            font-size: 1.8rem;
            font-weight: 800;
            color: #F8FAFC;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .about-subtitle {
            font-size: 0.95rem;
            color: #38BDF8;
            margin-bottom: 24px;
            font-weight: 600;
            letter-spacing: 0.3px;
        }

        /* Glassmorphism Main Card */
        .hero-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }
        .hero-text {
            color: #CBD5E1;
            font-size: 1rem;
            line-height: 1.65;
            margin: 0;
            letter-spacing: 0.2px;
        }

        /* Feature Cards Grid */
        .feature-card {
            background: #1E293B;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 20px;
            height: 100%;
            transition: all 0.3s ease;
        }
        .feature-card:hover {
            border-color: #38BDF8;
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(56, 189, 248, 0.15);
        }
        .feature-icon {
            font-size: 1.5rem;
            color: #38BDF8;
            margin-bottom: 10px;
            display: inline-block;
        }
        .feature-title {
            color: #F8FAFC;
            font-weight: 700;
            font-size: 1.05rem;
            margin-bottom: 6px;
        }
        .feature-desc {
            color: #94A3B8;
            font-size: 0.85rem;
            line-height: 1.45;
            margin: 0;
        }

        /* Metrics Glass Box */
        .metric-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 16px;
            text-align: center;
        }
        .metric-value {
            font-size: 1.6rem;
            font-weight: 800;
            color: #38BDF8;
        }
        .metric-label {
            font-size: 0.75rem;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page Header with Vector Icon
    st.markdown('<div class="about-title"><i class="bi bi-shield-shaded" style="color: #38BDF8;"></i> About ML Intrusion Detection System</div>', unsafe_allow_html=True)
    st.markdown('<div class="about-subtitle">⚡ Autonomous Network Defense • Active Shield v1.0</div>', unsafe_allow_html=True)

    # Hero Intro Card
    st.markdown("""
        <div class="hero-card">
            <p class="hero-text">
                <b>ML Intrusion Detector</b> is an advanced AI-driven network defense system designed to monitor 
                live network traffic, evaluate complex flow behaviors, and proactively isolate security threats. 
                Powered by trained Machine Learning models, it ensures real-time packet inspection and zero-day 
                attack identification.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Key Statistics Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">78</div><div class="metric-label">Flow Features</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">99.4%</div><div class="metric-label">Accuracy</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">&lt; 10ms</div><div class="metric-label">Latency</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-value">Real-Time</div><div class="metric-label">Monitoring</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)

    # Key Capabilities Section
    st.markdown("### **Core Capabilities**")
    
    f1, f2, f3 = st.columns(3)
    
    with f1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon"><i class="bi bi-search"></i></div>
                <div class="feature-title">78-Feature Analysis</div>
                <p class="feature-desc">Analyzes granular network flows including packet length, inter-arrival time, and TCP flag states.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with f2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon"><i class="bi bi-lightning-charge-fill"></i></div>
                <div class="feature-title">Live Detection Engine</div>
                <p class="feature-desc">Instantly flags malicious DDoS, Port Scans, and Brute Force attempts in active network streams.</p>
            </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon"><i class="bi bi-bar-chart-fill"></i></div>
                <div class="feature-title">Smart Analytics</div>
                <p class="feature-desc">Provides actionable insight reports with attack breakdown vectors and history logging.</p>
            </div>
        """, unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.set_page_config(page_title="Kepler Archive", layout="wide", initial_sidebar_state="collapsed")

API_URL = "https://kepler-project.onrender.com"

if 'page' not in st.session_state:
    st.session_state.page = "database"

retro_css = """
<style>
    [data-testid="collapsedControl"] { display: none !important; }
    
    html, body, [class*="css"] {
        font-family: 'Times New Roman', Times, serif !important;
        background-color: #d4d0c8 !important;
        color: #000000 !important;
    }
    
    .stButton>button {
        border-radius: 0px !important;
        border: 2px outset #ffffff !important;
        background-color: #c0c0c0 !important;
        color: black !important;
        box-shadow: none !important;
        width: 100% !important;
        font-weight: bold !important;
    }
    
    .stButton>button:active {
        border: 2px inset #ffffff !important;
    }

    h1, h2, h3, h4 {
        font-weight: bold !important;
        border-bottom: 1px solid black;
        padding-bottom: 2px;
    }
    
    .block-container {
        padding-top: 2rem !important; /* Отступ, чтобы шапку не резало */
    }
</style>
"""
st.markdown(retro_css, unsafe_allow_html=True)

st.markdown("""
<div style="background-color: #111111; padding: 15px; border-bottom: 2px solid #555; text-align: left;">
    <h1 style="color: #e0e0e0; margin: 0; font-family: Arial, sans-serif; font-size: 32px; letter-spacing: 2px; border: none;">NASA EXOPLANET ARCHIVE</h1>
    <h3 style="color: #a0a0a0; margin: 0; font-family: Arial, sans-serif; font-size: 18px; font-weight: normal !important; border: none;">NASA EXOPLANET SCIENCE INSTITUTE</h3>
</div>
<div style="background-color: #1a4b77; padding: 5px 15px; margin-bottom: 20px; font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; color: #f0a500; border-bottom: 3px solid #0d2b47;">
    <span style="color: white;">System Navigation:</span> Main Archive Menu
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 2.5]) 

with col1:
    if st.button("📂 1. KOI Database"):
        st.session_state.page = "database"
        st.rerun()

with col2:
    if st.button("🌌 2. 3D Simulator"):
        st.session_state.page = "simulator"
        st.rerun()

with col3:
    if st.button("📊 3. Data Analysis"):
        st.session_state.page = "analysis"
        st.rerun()

st.markdown("---") 

if st.session_state.page == "database":
    
    st.markdown("""
    <div style="background-color: #0d2b47; color: white; padding: 15px; border: 2px outset #ffffff; margin-bottom: 20px;">
        <h3 style="color: #f0a500; margin-top: 0; border-bottom: 1px solid #f0a500; font-family: Arial, sans-serif;">🚀 MISSION BRIEFING</h3>
        <p style="text-align: justify; font-size: 15px; line-height: 1.5;">
            This project presents a comprehensive exploratory data analysis (EDA) and interactive visualization of the Kepler Objects of Interest (KOI) cumulative database. The primary objective is to investigate the physical and orbital characteristics that distinguish confirmed exoplanets from false positive signals, such as eclipsing binary stars. By applying data cleaning techniques, deriving new planetary metrics, and conducting rigorous hypothesis checks, we examine the relationship between orbital periods, planetary radii, and equilibrium temperatures. Furthermore, the project features a dynamic 3D orbital simulator that brings the raw telemetry of candidate planets to life within a centralized web interface.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h2>NASA Exoplanet Archive - Database Access</h2>", unsafe_allow_html=True)
    st.write("Accessing the Kepler Objects of Interest (KOI) cumulative database via REST API...")
    
    with st.expander("📄 VIEW DATA DICTIONARY"):
        st.write("*(Hover your mouse over the blue underlined terms to read the full NASA documentation)*")
        dictionary_html = """
<style>
.retro-hover {
    position: relative;
    cursor: help;
    border-bottom: 1px dashed #1a4b77;
    font-weight: bold;
    color: #1a4b77;
}
.retro-tooltip {
    display: none;
    position: absolute;
    left: 25px;
    top: 25px;
    background-color: #ffffe1;
    color: black;
    border: 1px solid black;
    padding: 12px;
    width: 500px;
    font-weight: normal;
    font-family: 'Times New Roman', Times, serif;
    font-size: 14px;
    z-index: 9999;
    box-shadow: 2px 2px 0px rgba(0,0,0,0.5);
    line-height: 1.4;
    white-space: normal;
}
.retro-hover:hover .retro-tooltip {
    display: block;
}
.dict-section {
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 5px;
    font-size: 18px;
    color: #111;
    border-bottom: 1px solid #aaa;
    background-color: #c0c0c0;
    padding: 2px 5px;
}
.scroll-box {
    height: 500px; 
    overflow-y: scroll; 
    border: 2px inset #ffffff; 
    background-color: #e8e8e8; 
    padding: 15px;
}
</style>

<div class="scroll-box">
    
    <div class="dict-section">1. Identification Columns & Exoplanet Archive Info</div>
    <ul style="list-style-type: square; line-height: 2.0; font-size: 16px;">
        <li><span class="retro-hover">kepid<span class="retro-tooltip">Target identification number, as listed in the Kepler Input Catalog (KIC). The KIC was derived from a ground-based imaging survey of the Kepler field conducted prior to launch. The survey's purpose was to identify stars for the Kepler exoplanet survey by magnitude and color. The full catalog of 13 million sources can be searched at the MAST archive. The subset of 4 million targets found upon the Kepler CCDs can be searched via the Kepler Target Search form. The Kepler ID is unique to a target and there is only one Kepler ID per target.</span></span></li>
        <li><span class="retro-hover">kepoi_name<span class="retro-tooltip">A number used to identify and track a Kepler Object of Interest (KOI). A KOI is a target identified by the Kepler Project that displays at least one transit-like sequence within Kepler time-series photometry that appears to be of astrophysical origin and initially consistent with a planetary transit hypothesis. A KOI name has an integer and a decimal part of the format KNNNNN.DD. The integer part designates the target star; the two-digit decimal part identifies a unique transiting object associated with that star. It is not necessarily the planetary candidate listed in that order within a DV report, nor does it indicate the distance of the planet from the the host star relative to other planets in the system.</span></span></li>
        <li><span class="retro-hover">kepler_name<span class="retro-tooltip">Kepler number name in the form "Kepler-N," plus a lower-case letter, identifying the planet. In general, these numbers are easier to remember than the corresponding KOI or KIC/KepID designations and are intended to clearly indicate a class of objects that have been confirmed or validated as planets—a step up from the planet candidate designation.</span></span></li>
        <li><span class="retro-hover">koi_disposition<span class="retro-tooltip">The category of this KOI from the Exoplanet Archive. Current values are CANDIDATE, FALSE POSITIVE, NOT DISPOSITIONED or CONFIRMED. All KOIs marked as CONFIRMED are also listed in the Exoplanet Archive Confirmed Planet table. Designations of CANDIDATE, FALSE POSITIVE, and NOT DISPOSITIONED are taken from the Disposition Using Kepler Data.</span></span></li>
        <li><span class="retro-hover">koi_vet_stat<span class="retro-tooltip">Vetting Status for this KOI delivery. Current possible states are ACTIVE and DONE. As vetting tests for the null hypothesis that a TCE is a planet are performed, the disposition of each KOI as either a planet candidate or false positive will be updated and, most importantly, may change over time. It is therefore critical that the scientific community not conduct sample completeness studies on KOI tables that remain ACTIVE.</span></span></li>
    </ul>

    <div class="dict-section">2. Project Disposition Columns</div>
    <ul style="list-style-type: square; line-height: 2.0; font-size: 16px;">
        <li><span class="retro-hover">koi_pdisposition<span class="retro-tooltip">The pipeline flag that designates the most probable physical explanation of the KOI. Typical values are FALSE POSITIVE, NOT DISPOSITIONED, and CANDIDATE. The value of this flag may change over time as the evaluation of KOIs proceeds to deeper levels of analysis using Kepler time-series pixel and light curve data, or follow-up observations. A not dispositioned value corresponds to objects for which the disposition tests have not yet been completed. False positives can occur when: 1) the KOI is in reality an eclipsing binary star, 2) the Kepler light curve is contaminated by a background eclipsing binary, 3) stellar variability is confused for coherent planetary transits, or 4) instrumental artifacts are confused for coherent planetary transits.</span></span></li>
        <li><span class="retro-hover">koi_score<span class="retro-tooltip">A value between 0 and 1 that indicates the confidence in the KOI disposition. For CANDIDATEs, a higher value indicates more confidence in its disposition, while for FALSE POSITIVEs, a higher value indicates less confidence in that disposition. The value is calculated from a Monte Carlo technique such that the score's value is equivalent to the fraction of iterations where the Robovetter yields a disposition of CANDIDATE.</span></span></li>
        <li><span class="retro-hover">koi_fpflag_nt<span class="retro-tooltip">Not Transit-Like Flag. A KOI whose light curve is not consistent with that of a transiting planet. This includes, but is not limited to, instrumental artifacts, non-eclipsing variable stars, and spurious (very low SNR) detections.</span></span></li>
        <li><span class="retro-hover">koi_fpflag_ss<span class="retro-tooltip">Stellar Eclipse Flag. A KOI that is observed to have a significant secondary event, transit shape, or out-of-eclipse variability, which indicates that the transit-like event is most likely caused by an eclipsing binary. However, self-luminous, hot Jupiters with a visible secondary eclipse will also have this flag set, but with a disposition of PC.</span></span></li>
        <li><span class="retro-hover">koi_fpflag_co<span class="retro-tooltip">Centroid Offset Flag. The source of the signal is from a nearby star, as inferred by measuring the centroid location of the image both in and out of transit, or by the strength of the transit signal in the target's outer (halo) pixels as compared to the transit signal from the pixels in the optimal (or core) aperture.</span></span></li>
        <li><span class="retro-hover">koi_fpflag_ec<span class="retro-tooltip">Ephemeris Match Indicates Contamination Flag. The KOI shares the same period and epoch as another object and is judged to be the result of flux contamination in the aperture or electronic crosstalk.</span></span></li>
        <li><span class="retro-hover">koi_comment<span class="retro-tooltip">A description of the reason why an object's disposition has been given as false positive. Keywords include APO (Active Pixel Offset), Binary, EB, odd-even, V-shaped, SB1, SB2. A comment field may also contain a list of the minor flags as set by the Robovetter.</span></span></li>
    </ul>

    <div class="dict-section">3. Transit Properties</div>
    <ul style="list-style-type: square; line-height: 2.0; font-size: 16px;">
        <li><span class="retro-hover">koi_period<span class="retro-tooltip">Orbital Period (days). The interval between consecutive planetary transits.</span></span></li>
        <li><span class="retro-hover">koi_time0bk<span class="retro-tooltip">Transit Epoch (BJD - 2,454,833.0). The time corresponding to the center of the first detected transit in Barycentric Julian Day (BJD) minus a constant offset of 2,454,833.0 days. The offset corresponds to 12:00 on Jan 1, 2009 UTC.</span></span></li>
        <li><span class="retro-hover">koi_impact<span class="retro-tooltip">Impact Parameter. The sky-projected distance between the center of the stellar disc and the center of the planet disc at conjunction, normalized by the stellar radius.</span></span></li>
        <li><span class="retro-hover">koi_duration<span class="retro-tooltip">Transit Duration (hours). The duration of the observed transits. Duration is measured from first contact between the planet and star until last contact. Contact times are typically computed from a best-fit model produced by a Mandel-Agol (2002) model fit to a multi-quarter Kepler light curve, assuming a linear orbital ephemeris.</span></span></li>
        <li><span class="retro-hover">koi_depth<span class="retro-tooltip">Transit Depth (parts per million). The fraction of stellar flux lost at the minimum of the planetary transit. Transit depths are typically computed from a best-fit model produced by a Mandel-Agol (2002) model fit to a multi-quarter Kepler light curve, assuming a linear orbital ephemeris.</span></span></li>
        <li><span class="retro-hover">koi_srho<span class="retro-tooltip">Fitted Stellar Density [g/cm*3]. Fitted stellar density is a direct observable from the light curve that, in the small-planet approximation, depends only on the transit's period, depth, and duration (see Seager and Mallen-Ornelas 2003). This quantity is directly fitted in the LS and MCMC methods, and is completely independent from the listed stellar mass and radius.</span></span></li>
        <li><span class="retro-hover">koi_prad<span class="retro-tooltip">Planetary Radius (Earth radii). The radius of the planet. Planetary radius is the product of the planet star radius ratio and the stellar radius.</span></span></li>
        <li><span class="retro-hover">koi_sma<span class="retro-tooltip">Orbit Semi-Major Axis (Astronomical Unit (au)). Half of the long axis of the ellipse defining a planet's orbit. For a circular orbit this is the planet-star separation radius. The semi-major axis is derived based on Kepler's third law, i.e., utilizing the orbital period and stellar mass, not scaling the planet-star separation by the stellar radius.</span></span></li>
        <li><span class="retro-hover">koi_teq<span class="retro-tooltip">Equilibrium Temperature (Kelvin). Approximation for the temperature of the planet. The calculation of equilibrium temperature assumes a) thermodynamic equilibrium between the incident stellar flux and the radiated heat from the planet, b) a Bond albedo (the fraction of total power incident upon the planet scattered back into space) of 0.3, c) the planet and star are blackbodies, and d) the heat is evenly distributed between the day and night sides of the planet.</span></span></li>
        <li><span class="retro-hover">koi_insol<span class="retro-tooltip">Insolation Flux [Earth flux]. Insolation flux is another way to give the equilibrium temperature. It depends on the stellar parameters (specifically the stellar radius and temperature), and on the semi-major axis of the planet. It's given in units relative to those measured for the Earth from the Sun.</span></span></li>
    </ul>

    <div class="dict-section">4. Threshold-Crossing Event (TCE) Information</div>
    <ul style="list-style-type: square; line-height: 2.0; font-size: 16px;">
        <li><span class="retro-hover">koi_max_mult_ev<span class="retro-tooltip">Maximum Multiple Event Statistic. The maximum calculated value of the MES. TCEs that meet the maximum MES threshold criterion and other criteria listed in the TCE release notes are delivered to the Data Validation (DV) module of the Kepler data analysis pipeline for transit characterization and the calculation of statistics required for disposition.</span></span></li>
        <li><span class="retro-hover">koi_model_snr<span class="retro-tooltip">Transit Signal-to-Noise. Transit depth normalized by the mean uncertainty in the flux during the transits.</span></span></li>
        <li><span class="retro-hover">koi_count<span class="retro-tooltip">Number of Planets. Number of planet candidates identified in a system.</span></span></li>
        <li><span class="retro-hover">koi_num_transits<span class="retro-tooltip">Number of Transits. The number of expected transits or partially-observed transits associated with the planet candidate occurring within the searched light curve. This does not include transits that fall completely within data gaps.</span></span></li>
    </ul>

    <div class="dict-section">5. Stellar & KIC Parameters</div>
    <ul style="list-style-type: square; line-height: 2.0; font-size: 16px;">
        <li><span class="retro-hover">koi_steff<span class="retro-tooltip">Stellar Effective Temperature (Kelvin). The photospheric temperature of the star.</span></span></li>
        <li><span class="retro-hover">koi_slogg<span class="retro-tooltip">Stellar Surface Gravity (log10(cm s-2)). The base-10 logarithm of the acceleration due to gravity at the surface of the star.</span></span></li>
        <li><span class="retro-hover">koi_smet<span class="retro-tooltip">Stellar Metallicity. The base-10 logarithm of the Fe to H ratio at the surface of the star, normalized by the solar Fe to H ratio.</span></span></li>
        <li><span class="retro-hover">koi_srad<span class="retro-tooltip">Stellar Radius (solar radii). The photospheric radius of the star.</span></span></li>
        <li><span class="retro-hover">koi_smass<span class="retro-tooltip">Stellar Mass (solar mass). The mass of the star.</span></span></li>
        <li><span class="retro-hover">koi_sage<span class="retro-tooltip">Stellar Age (Gigayears). The age of the star.</span></span></li>
        <li><span class="retro-hover">koi_sparprov<span class="retro-tooltip">Provenance of Stellar Parameters. A flag describing the source of the stellar parameters (e.g. KIC, J-K, Solar, SME, SPC, Pinsonneault, Astero).</span></span></li>
        <li><span class="retro-hover">ra / dec<span class="retro-tooltip">KIC Right Ascension and Declination of the star in degrees.</span></span></li>
        <li><span class="retro-hover">koi_kepmag<span class="retro-tooltip">Kepler-band (mag). Magnitude of the star.</span></span></li>
    </ul>

    <div class="dict-section">6. Pixel-Based KOI Vetting Statistics</div>
    <ul style="list-style-type: square; line-height: 2.0; font-size: 16px;">
        <li><span class="retro-hover">koi_fwm_sra / koi_fwm_sdec<span class="retro-tooltip">FW Source α(OOT) / δ(OOT). The Right Ascension and Declination (J2000) of the location of the transiting object calculated from the flux-weighted centroids. This result does not reflect the systematics due to crowding which can introduce significant errors in the calculated position.</span></span></li>
        <li><span class="retro-hover">koi_dicco_msky<span class="retro-tooltip">PRF ΔθSQ(OOT). The angular offset on the plane of the sky between the best-fit PRF centroids from the Out-Of-Transit image and the Difference Image by averaging the weighted single-quarter measurements.</span></span></li>
        <li><span class="retro-hover">koi_dikco_msky<span class="retro-tooltip">PRF ΔθSQ(KIC). The angular offset in the plane of the sky between the best-fit PRF centroids from the difference image and the Kepler Input Catalog position by averaging the weighted single-quarter measurements.</span></span></li>
    </ul>
    
</div>
<p style="font-size: 14px; font-style: italic; margin-top: 15px;">(Source: Exoplanet Archive API Documentation, updated 11 February 2021. DOI 10.26133/NEA4)</p>
"""
        clean_html = '\n'.join([line.lstrip() for line in dictionary_html.split('\n')])
        st.markdown(clean_html, unsafe_allow_html=True)

    # =========================================================================
    st.markdown("<h3>REST API Access Console</h3>", unsafe_allow_html=True)
    
    col_get, col_post = st.columns(2)
    
    with col_get:
        st.markdown("**1. Data Retrieval (GET)**")
        status_filter = st.selectbox("Select Target Status:", ["CONFIRMED", "CANDIDATE", "FALSE POSITIVE"])
        limit_filter = st.slider("Records Limit:", 10, 500, 100)
        
        if st.button("Fetch Telemetry from Server"):
            try:
                with st.spinner("Connecting to FastAPI..."):
                    res = requests.get(API_URL, params={"status": status_filter, "limit": limit_filter})
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"Success! Downloaded {len(data)} records via API.")
                    st.dataframe(pd.DataFrame(data), use_container_width=True)
                else:
                    st.error("Server responded with an error.")
            except Exception as e:
                st.error("CRITICAL ERROR: Cannot connect to FastAPI server. Ensure 'uvicorn api.main:app' is running!")

    with col_post:
        st.markdown("**2. Data Entry Console (POST)**")
        with st.form("add_form"):
            new_name = st.text_input("Planet Name", "KOI-999.01")
            new_status = st.selectbox("Status", ["CANDIDATE", "CONFIRMED"])
            new_period = st.number_input("Period (days)", value=365.25)
            new_prad = st.number_input("Radius (Earths)", value=1.0)
            new_srad = st.number_input("Star Radius (Solar)", value=1.0)
            new_teq = st.number_input("Temp (K)", value=250.0)
            
            if st.form_submit_button("Transmit Data to Mainframe"):
                payload = {
                    "kepoi_name": new_name, "koi_disposition": new_status, 
                    "koi_period": new_period, "koi_prad": new_prad, 
                    "koi_srad": new_srad, "koi_teq": new_teq
                }
                try:
                    with st.spinner("Transmitting..."):
                        post_res = requests.post(API_URL, json=payload)
                    if post_res.status_code == 200:
                        st.success(f"Record {new_name} added to the registry!")
                        st.json(post_res.json()["data"])
                    else:
                        st.error("Failed to add record.")
                except Exception as e:
                    st.error("CRITICAL ERROR: Link failure.")

elif st.session_state.page == "simulator":
    st.markdown("<h2>🛰️ Advanced Orbital Mechanics Simulator</h2>", unsafe_allow_html=True)
    st.write("Real-time kinematic rendering powered by FastAPI. Orbital radii are calculated strictly using Kepler's Third Law ($a^3 \propto P^2$).")

    time_step = st.slider("Simulation Time (Earth Days):", min_value=0, max_value=2000, value=0, step=5)
    
    try:
        with st.spinner("Synchronizing with FastAPI Mainframe..."):
            res = requests.get(API_URL, params={"status": "CONFIRMED", "limit": 1500})

        if res.status_code == 200:
            df_api = pd.DataFrame(res.json()).dropna(subset=['koi_period', 'koi_prad', 'koi_teq'])
            hz_planets = df_api[(df_api['koi_teq'] >= 200) & (df_api['koi_teq'] <= 320)].nlargest(6, 'koi_prad')
            hot_jupiters = df_api[(df_api['koi_teq'] > 1000) & (df_api['koi_prad'] > 8)].nlargest(6, 'koi_prad')
            cold_giants = df_api[(df_api['koi_teq'] < 150) & (df_api['koi_prad'] > 5)].nlargest(3, 'koi_prad')

            df_sim = pd.concat([hz_planets, hot_jupiters, cold_giants])

            np.random.seed(42)
            n_stars = 150
            star_x = np.random.uniform(-25, 25, n_stars)
            star_y = np.random.uniform(-25, 25, n_stars)
            star_z = np.random.uniform(-10, 10, n_stars)

            fig = go.Figure()

            fig.add_trace(go.Scatter3d(
                x=star_x, y=star_y, z=star_z,
                mode='markers',
                marker=dict(size=1.5, color='white', opacity=0.7),
                name='Background Stars', hoverinfo='skip', showlegend=False
            ))

            r_hz = np.linspace(8, 14, 20)
            theta_hz = np.linspace(0, 2*np.pi, 50)
            R, THETA = np.meshgrid(r_hz, theta_hz)
            
            fig.add_trace(go.Surface(
                x=R*np.cos(THETA), y=R*np.sin(THETA), z=np.zeros_like(R),
                colorscale=[[0, 'rgba(0, 255, 170, 0.12)'], [1, 'rgba(0, 255, 170, 0.03)']],
                showscale=False, hoverinfo='skip', name="Habitable Zone"
            ))

            fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers',
                marker=dict(size=16, color='#ffcc00', opacity=1.0), name='Host Star', hoverinfo='none'))
            fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers',
                marker=dict(size=35, color='#ffcc00', opacity=0.15), name='Stellar Corona', hoverinfo='none'))

            a_earth = 10.0  
            omega_earth = 2 * np.pi / 365.25
            angle_earth = omega_earth * time_step
            curr_x_earth = a_earth * np.cos(angle_earth)
            curr_y_earth = a_earth * np.sin(angle_earth)

            t_orbit = np.linspace(0, 2*np.pi, 100)
            fig.add_trace(go.Scatter3d(
                x=a_earth*np.cos(t_orbit), y=a_earth*np.sin(t_orbit), z=np.zeros(100),
                mode='lines', line=dict(color='#3a86ff', width=1.5, dash='solid'), 
                opacity=0.6, showlegend=False, hoverinfo='skip'
            ))

            fig.add_trace(go.Scatter3d(
                x=[curr_x_earth], y=[curr_y_earth], z=[0],
                mode='markers',
                marker=dict(size=8, color='#3a86ff', line=dict(color='white', width=1)),
                name="Planet Earth",
                hovertemplate="<b>PLANET EARTH</b><br><br>Type: Baseline<br>Period: 365.3d<br>Radius: 1.0 R⊕<br>Temp: 288 K<extra></extra>"
            ))

            for _, row in df_sim.iterrows():
                name = row['kepoi_name']
                P = row['koi_period']
                prad = row['koi_prad']
                teq = row['koi_teq']

                a = ((P / 365.25) ** (2/3)) * 10 
                omega = 2 * np.pi / P
                angle = omega * time_step

                if 200 <= teq <= 320: 
                    color = "#00ffaa"; cat = "Habitable"
                elif teq > 1000: 
                    color = "#ff3366"; cat = "Hot Jupiter"
                else: 
                    color = "#ffaa00"; cat = "Cold Giant"

                fig.add_trace(go.Scatter3d(
                    x=a*np.cos(t_orbit), y=a*np.sin(t_orbit), z=np.zeros(100),
                    mode='lines', line=dict(color=color, width=1, dash='dot'), 
                    opacity=0.3, showlegend=False, hoverinfo='skip'
                ))

                p_size = np.clip(prad * 1.5, 4, 16)
                fig.add_trace(go.Scatter3d(
                    x=[a*np.cos(angle)], y=[a*np.sin(angle)], z=[0],
                    mode='markers', 
                    marker=dict(size=p_size, color=color, line=dict(color='white', width=0.5)),
                    name=name,
                    hovertemplate=f"<b>{name}</b><br><br>Type: {cat}<br>Period: {P:.1f}d<br>Radius: {prad:.1f} R⊕<br>Temp: {teq} K<extra></extra>"
                ))

            fig.update_layout(
                scene=dict(
                    xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
                    camera=dict(eye=dict(x=0.5, y=-1.2, z=0.8)),
                    aspectmode='manual',
                    aspectratio=dict(x=1, y=1, z=0.4)
                ),
                margin=dict(l=0, r=0, b=0, t=0), 
                paper_bgcolor="#111111", plot_bgcolor="#111111", height=700,
                showlegend=False,
                hoverlabel=dict(
                    bgcolor="#222222",
                    bordercolor="#555555",
                    font=dict(size=13, color="white", family="Courier New")
                )
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            bot_col1, bot_col2, bot_col3 = st.columns(3)
            
            with bot_col1:
                st.markdown(f"**🟢 SYSTEM TELEMETRY**<br>Tracked Systems: `{len(df_sim) + 1}` target bodies<br>Current Relativistic Step: `{time_step} Days`", unsafe_allow_html=True)
            
            with bot_col2:
                st.markdown("**🎨 COLOR CODING DICTIONARY**<br>🔵 `Planet Earth (Baseline)` | 🟢 `Habitable Zone (200K - 320K)`", unsafe_allow_html=True)
                st.markdown("🔴 `Hot Jupiters (>1000K, Core Orbit)` | 🟡 `Cold Giants (<150K, Outer Bound)`", unsafe_allow_html=True)
                
            with bot_col3:
                st.markdown("**📝 OBSERVATION LOG**<br>*The translucent green mesh defines the liquid water envelope. Earth acts as your spatial coordinate master anchor.*", unsafe_allow_html=True)

        else:
            st.error("API error: Could not fetch telemetry from FastAPI.")
    except Exception as e:
        st.error(f"CRITICAL ERROR: API Connection failed. {e}")
 
# ======================================================================================
elif st.session_state.page == "analysis":
    st.markdown("<h2>Mission Analysis Report</h2>", unsafe_allow_html=True)
    st.write("SYSTEM STATUS: Performing Detailed EDA & Statistical Profiling...")
    
    try:
        df_raw = pd.read_csv('data/cumulative.csv')
        
        req_cols = ['koi_period', 'koi_prad', 'koi_srad', 'koi_teq', 'koi_depth', 'koi_disposition']
        df_clean = df_raw.dropna(subset=req_cols).copy()
        
        for c in ['koi_period', 'koi_prad', 'koi_srad', 'koi_teq', 'koi_depth']:
            df_clean = df_clean[df_clean[c] > 0]
            
        df_clean['planet_volume_earth'] = df_clean['koi_prad'] ** 3
        df_clean['habitable_zone'] = (df_clean['koi_teq'] >= 200) & (df_clean['koi_teq'] <= 320)
        
        def classify_size(r):
            if r < 1.25: return "Earth-size"
            elif r < 2.0: return "Super-Earth"
            elif r < 6.0: return "Neptune-like"
            else: return "Giant"
        df_clean["planet_size_class"] = df_clean["koi_prad"].apply(classify_size)
        
        st.success(f"Data cleaned according to Kepler 10/10 EDA Pipeline. Remaining high-quality records: {len(df_clean)}")

        STATUS_PALETTE = {
            "CONFIRMED": "#2A9D8F",
            "CANDIDATE": "#E9C46A",
            "FALSE POSITIVE": "#E76F51",
        }
        sns.set_theme(style="whitegrid", context="notebook")

        st.markdown("<h3>Phase 1: Core Numerical Descriptive Statistics</h3>", unsafe_allow_html=True)
        numerical_fields = ['koi_period', 'koi_prad', 'koi_srad', 'koi_teq', 'koi_depth']
        st.dataframe(df_clean[numerical_fields].describe().T.style.format("{:.2f}"), use_container_width=True)

        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("<h3>Phase 2: Size Class vs Target Disposition</h3>", unsafe_allow_html=True)
            cross_tab = pd.crosstab(df_clean['planet_size_class'], df_clean['koi_disposition'])
            st.dataframe(cross_tab, use_container_width=True)
            
        with col_right:
            st.markdown("<h3>Phase 3: Correlation Heatmap Matrix</h3>", unsafe_allow_html=True)
            corr = df_clean[numerical_fields].corr()
            fig_corr, ax_corr = plt.subplots(figsize=(8, 5))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax_corr)
            st.pyplot(fig_corr)

        st.markdown("<h3>Phase 4: Basic Distributions & Relationships</h3>", unsafe_allow_html=True)
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.write("**1. Equilibrium Temperature Distribution**")
            fig_hist, ax_hist = plt.subplots(figsize=(8, 5))
            sns.histplot(data=df_clean, x='koi_teq', hue='koi_disposition', multiple='stack', bins=30, ax=ax_hist, palette=STATUS_PALETTE)
            ax_hist.set_title("Histogram: Equilibrium Temperature")
            st.pyplot(fig_hist)
            
        with col_p2:
            st.write("**2. Stellar Radius by Status**")
            fig_box, ax_box = plt.subplots(figsize=(8, 5))
            sns.boxplot(data=df_clean, x='koi_disposition', y='koi_srad', ax=ax_box, palette=STATUS_PALETTE)
            ax_box.set_yscale('log')
            ax_box.set_title("Box Plot: Stellar Radius (log scale)")
            st.pyplot(fig_box)

        col_p3, col_p4 = st.columns(2)
        with col_p3:
            st.write("**3. Orbital Period vs Planetary Radius**")
            fig_scat, ax_scat = plt.subplots(figsize=(8, 5))
            sns.scatterplot(data=df_clean, x='koi_period', y='koi_prad', hue='koi_disposition', alpha=0.6, ax=ax_scat, palette=STATUS_PALETTE)
            ax_scat.set_xscale('log')
            ax_scat.set_yscale('log')
            ax_scat.set_title("Scatter Plot: Period vs Radius")
            st.pyplot(fig_scat)

        st.markdown("---")

        st.markdown("<h3>Phase 5: Rigorous Hypothesis Testing</h3>", unsafe_allow_html=True)
        col_h1, col_h2 = st.columns(2)
        
        with col_h1:
            st.markdown("#### **Hypothesis 1 (Transit Physics)**")
            st.write("*Statement:* For confirmed exoplanets, there is a strong positive correlation between Transit Depth and Planetary Radius.")
            
            conf_planets = df_clean[df_clean['koi_disposition'] == 'CONFIRMED'].copy()
            conf_planets['log_depth'] = np.log10(conf_planets['koi_depth'])
            conf_planets['log_prad'] = np.log10(conf_planets['koi_prad'])
            
            fig_h1, ax_h1 = plt.subplots(figsize=(8, 5))
            sns.regplot(data=conf_planets, x='log_depth', y='log_prad', 
                        scatter_kws={'alpha': 0.5, 'color': '#2A9D8F', 'edgecolor': 'w'},
                        line_kws={'color': '#E76F51', 'linewidth': 3}, ax=ax_h1)
            ax_h1.set_title("Transit Depth vs Planetary Radius", fontweight='bold')
            ax_h1.set_xlabel("Log10 (Transit Depth, ppm)")
            ax_h1.set_ylabel("Log10 (Planetary Radius, Earth radii)")
            st.pyplot(fig_h1)
            
            corr_val, p_val1 = stats.pearsonr(conf_planets['log_depth'], conf_planets['log_prad'])
            st.info(f"**Pearson r:** {corr_val:.4f} | **p-value:** {p_val1:.4e} (Statistically Significant)")

        with col_h2:
            st.markdown("#### **Hypothesis 2 (The 'Hot Jupiter' Effect)**")
            st.write("*Statement:* Giant planets are on average significantly hotter than Earth-sized planets due to observational bias.")
            
            h2_df = df_clean[(df_clean['koi_disposition'] == 'CONFIRMED') & 
                             (df_clean['planet_size_class'].isin(['Earth-size', 'Giant']))].copy()
            
            fig_h2, ax_h2 = plt.subplots(figsize=(8, 5))
            sns.violinplot(data=h2_df, x='planet_size_class', y='koi_teq',
                           palette=['#2A9D8F', '#9b59b6'], inner='quartile', ax=ax_h2)
            ax_h2.set_title("Earth-size vs Giant Temperatures", fontweight='bold')
            ax_h2.set_xlabel("Planet Size Class")
            ax_h2.set_ylabel("Equilibrium Temperature (Kelvin)")
            st.pyplot(fig_h2)
            
            earth_temps = h2_df[h2_df['planet_size_class'] == 'Earth-size']['koi_teq'].dropna()
            giant_temps = h2_df[h2_df['planet_size_class'] == 'Giant']['koi_teq'].dropna()
            t_stat, p_val2 = stats.ttest_ind(earth_temps, giant_temps, equal_var=False)
            
            sig_text = "SIGNIFICANT" if p_val2 < 0.05 else "NOT SIGNIFICANT"
            st.info(f"**Welch's T-test:** {sig_text} | **t-statistic:** {t_stat:.4f} | **p-value:** {p_val2:.4e}")

    except FileNotFoundError:
        st.error("SYSTEM ERROR: Файл 'data/cumulative.csv' не найден!")

# ui_config.py

# Professional Glassmorphism and Responsive Layout
custom_css = """
footer {visibility: hidden}

/* Background with Overlay */
.gradio-container {
    background: linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)), 
                url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1920&q=80');
    background-size: cover;
    background-attachment: fixed;
}

/* Hero Content Area */
.hero-content {
    margin-top: 60px;
    margin-left: 40px;
    max-width: 600px;
    color: #064e3b;
    animation: fadeIn 1s ease-out;
}

/* Floating Chat Widget with Glassmorphism */
#floating_container {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 420px;
    height: 620px;
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(12px);
    border-radius: 24px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.4);
    overflow: hidden;
    z-index: 1000;
    animation: slideUp 0.6s ease-out;
}

.widget-header {
    background: linear-gradient(90deg, #059669, #10b981);
    color: white;
    padding: 18px 25px;
    font-size: 1.25rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 12px;
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@media (max-width: 1000px) {
    .hero-content { display: none; }
    #floating_container { width: 100%; height: 100%; bottom: 0; right: 0; border-radius: 0; }
}
"""

# Hero HTML with Quick Stats
hero_html = """
<div class="hero-content">
    <h1 style="font-size: 4rem; line-height: 1; font-weight: 900; margin-bottom: 20px;">
        Precision Farming <br><span style="color: #10b981;">Simplified.</span>
    </h1>
    <p style="font-size: 1.25rem; color: #374151; font-weight: 500; margin-bottom: 30px;">
        Instant access to verified scientific agricultural data. 
        Empowering farmers with AI-driven insights for better yields.
    </p>
    
    <div style="display: flex; gap: 15px; margin-bottom: 50px;">
        <span style="background: #059669; color: white; padding: 12px 25px; border-radius: 50px; font-weight: 700;">✓ Verified Data</span>
        <span style="background: white; border: 2px solid #059669; color: #059669; padding: 12px 25px; border-radius: 50px; font-weight: 700;">🚜 24/7 Support</span>
    </div>

    <div style="display: flex; gap: 50px; border-top: 2px solid rgba(5, 150, 105, 0.1); padding-top: 40px;">
        <div>
            <h4 style="margin: 0; color: #059669; font-size: 1.8rem; font-weight: 800;">150+</h4>
            <p style="margin: 0; color: #6b7280; font-size: 1rem;">Manual Pages</p>
        </div>
        <div>
            <h4 style="margin: 0; color: #059669; font-size: 1.8rem; font-weight: 800;">Real-time</h4>
            <p style="margin: 0; color: #6b7280; font-size: 1rem;">AI Processing</p>
        </div>
        <div>
            <h4 style="margin: 0; color: #059669; font-size: 1.8rem; font-weight: 800;">Secure</h4>
            <p style="margin: 0; color: #6b7280; font-size: 1rem;">Local Database</p>
        </div>
    </div>
</div>
"""
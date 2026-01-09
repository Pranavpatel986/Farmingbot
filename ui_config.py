# ui_config.py

custom_css = """
footer {visibility: hidden}

.gradio-container {
    background: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), 
                url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1920&q=80');
    background-size: cover;
    background-attachment: fixed;
}

.hero-content {
    margin-top: 80px;
    margin-left: 40px;
    max-width: 550px;
    color: #065f46;
}

#floating_container {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 400px;
    height: 580px;
    background: white;
    border-radius: 20px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    border: 1px solid #d1fae5;
    overflow: hidden;
    z-index: 1000;
}

.widget-header {
    background: #10b981;
    color: white;
    padding: 15px 20px;
    font-size: 1.2rem;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 10px;
}

@media (max-width: 900px) {
    .hero-content { display: none; }
    #floating_container { width: 100%; height: 100%; bottom: 0; right: 0; border-radius: 0; }
}
"""

hero_html = """
<div class="hero-content">
    <h1 style="font-size: 3.5rem; line-height: 1.1; font-weight: 800;">
        Smart Farming <br><span style="color: #10b981;">Starts Here.</span>
    </h1>
    <p style="font-size: 1.2rem; margin-top: 20px; color: #374151; font-weight: 500;">
        Access scientific agricultural knowledge instantly. 
        Ask our AI bot about soil, seeds, and sustainable crop management.
    </p>
    <div style="margin-top: 30px; display: flex; gap: 15px;">
        <span style="background: #10b981; color: white; padding: 10px 22px; border-radius: 50px; font-weight: bold; font-size: 0.9rem;">✓ Verified Data</span>
        <span style="background: white; border: 1.5px solid #10b981; color: #10b981; padding: 10px 22px; border-radius: 50px; font-weight: bold; font-size: 0.9rem;">🚜 24/7 Expert Support</span>
    </div>
</div>
"""

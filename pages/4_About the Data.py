import streamlit as st
import streamlit.components.v1 as components
import json  # ← ADD THIS

st.set_page_config(page_title="About the Data", layout="wide")
st.title("Data drives insights, here's how we used yours")
st.markdown("Hover over bubbles to explore how the system works, in summary.")

bubbles = [
    ("Scoring the Data", "Responses converted to a 1–5 scale for analysis."),
    ("🧠 Theme Logic", "Grouped into Leadership, Growth, Engagement."),
    ("📈 Aggregation", "Scores at Business Unit, Department & Company Level."),
    ("🤖 AI Layer", "AI converts scores into executive insights."),
    ("Key Drivers", "Lowest scores identify root causes."),
    ("Interpretation", "Comparative, not absolute performance.")
]

bubbles_json = json.dumps(bubbles)  # ← SERIALIZE TO VALID JSON

bubble_html = f"""
<div id="container"></div>
<style>
body {{
    margin: 0;
    overflow: hidden;
    background: radial-gradient(circle at top, #111827, #0b0f19);
    font-family: sans-serif;
}}
.bubble {{
    position: absolute;
    width: 170px;
    height: 170px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(76, 175, 80, 0.18);
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(6px);
    box-shadow: 0 0 20px rgba(0,0,0,0.3);
    cursor: pointer;
    transition: transform 0.3s ease, background 0.3s ease;
}}
.bubble:hover {{
    transform: scale(1.2);
    background: rgba(76, 175, 80, 0.4);
    box-shadow: 0 0 35px rgba(76,175,80,0.6);
}}
.content {{
    width: 120px;
    text-align: center;
    color: white;
    white-space: normal;
    word-break: keep-all;
    overflow-wrap: normal;
}}
.title {{
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 6px;
}}
.desc {{
    font-size: 11px;
    line-height: 1.3;
}}
</style>
<script>
const bubblesData = {bubbles_json};   /* ← USE bubbles_json, not bubbles */
const container = document.getElementById("container");
const bubbleNodes = [];               /* ← RENAMED from bubbles to avoid conflict */
const WIDTH = window.innerWidth;
const HEIGHT = window.innerHeight;

bubblesData.forEach((b, i) => {{
    const el = document.createElement("div");
    el.className = "bubble";
    el.innerHTML = `
        <div class="content">
            <div class="title">${{b[0]}}</div>
            <div class="desc">${{b[1]}}</div>
        </div>
    `;
    container.appendChild(el);
    const size = 170;
    bubbleNodes.push({{      /* ← RENAMED */
        el: el,
        x: Math.random() * (WIDTH - size),
        y: Math.random() * (HEIGHT - size),
        dx: (Math.random() * 0.6 + 0.3) * (Math.random() > 0.5 ? 1 : -1),
        dy: (Math.random() * 0.6 + 0.3) * (Math.random() > 0.5 ? 1 : -1),
        size: size,
        paused: false
    }});
    el.addEventListener("mouseenter", () => bubbleNodes[i].paused = true);
    el.addEventListener("mouseleave", () => bubbleNodes[i].paused = false);
}});

function animate() {{
    bubbleNodes.forEach(b => {{   /* ← RENAMED */
        if (!b.paused) {{
            b.x += b.dx;
            b.y += b.dy;
            if (b.x <= 0 || b.x >= WIDTH - b.size) b.dx *= -1;
            if (b.y <= 0 || b.y >= HEIGHT - b.size) b.dy *= -1;
        }}
        b.el.style.transform = `translate(${{b.x}}px, ${{b.y}}px)`;
    }});
    requestAnimationFrame(animate);
}}
animate();
</script>
"""

components.html(bubble_html, height=700)
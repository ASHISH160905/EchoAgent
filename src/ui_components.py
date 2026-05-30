import base64
import json
import streamlit.components.v1 as components

def render_interactive_audio_agent(text, audio_bytes):
    """
    Renders a full-screen interactive AI Agent overlay with a 
    blurred background, custom media controls, and synced subtitles.
    """
    b64_audio = base64.b64encode(audio_bytes).decode()
    audio_data_uri = f"data:audio/wav;base64,{b64_audio}"
    js_text = json.dumps(text)
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body, html {{
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        font-family: 'Inter', sans-serif;
        background: transparent;
        overflow: hidden;
    }}
    
    .overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 999999;
    }}
    
    .close-btn {{
        position: absolute;
        top: 30px;
        right: 30px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        font-size: 24px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: all 0.3s ease;
    }}
    
    .close-btn:hover {{
        background: rgba(255, 0, 0, 0.4);
        transform: scale(1.1);
    }}
    
    .blob {{
        width: 350px;
        height: 350px;
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
        box-shadow: 0 0 100px rgba(79, 172, 254, 0.5);
        animation: morph 8s ease-in-out infinite alternate;
        margin-bottom: 50px;
    }}
    
    .blob.speaking {{
        animation: morph 3s ease-in-out infinite alternate, pulse 0.4s ease-in-out infinite alternate;
        box-shadow: 0 0 120px rgba(79, 172, 254, 0.8);
    }}
    
    @keyframes morph {{
        0% {{ border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; }}
        25% {{ border-radius: 58% 42% 75% 25% / 76% 46% 54% 24%; }}
        50% {{ border-radius: 50% 50% 33% 67% / 55% 27% 73% 45%; }}
        75% {{ border-radius: 33% 67% 58% 42% / 63% 68% 32% 37%; }}
        100% {{ border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; }}
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        100% {{ transform: scale(1.1); }}
    }}
    
    .subtitle-container {{
        width: 80%;
        max-width: 900px;
        min-height: 120px;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        text-align: center;
        margin-bottom: 40px;
    }}
    
    .word {{
        font-size: 28px;
        margin: 5px 8px;
        color: rgba(255, 255, 255, 0.2);
        transition: all 0.2s ease;
    }}
    
    .word.active {{
        color: #4facfe;
        font-weight: bold;
        transform: scale(1.2);
        opacity: 1;
        text-shadow: 0 0 15px rgba(79, 172, 254, 0.6);
    }}
    
    .word.past {{ display: none; }}
    .word.upcoming {{ color: rgba(255, 255, 255, 0.6); }}
    
    .controls {{
        display: flex;
        gap: 30px;
        margin-top: 20px;
    }}
    
    .control-btn {{
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        padding: 15px 35px;
        border-radius: 30px;
        cursor: pointer;
        font-size: 18px;
        font-weight: 600;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .control-btn:hover {{
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }}
    
    .control-btn.play {{ background: #4facfe; border: none; }}
    
    #audio-element {{ display: none; }}
    </style>
    </head>
    <body>
        <div class="overlay">
            <!-- X Button -->
            <div class="close-btn" onclick="closeAgent()">✕</div>
            
            <!-- Animated Blob -->
            <div class="blob" id="blob"></div>
            
            <!-- Subtitles -->
            <div class="subtitle-container" id="subtitles"></div>
            
            <!-- Controls -->
            <div class="controls">
                <button class="control-btn play" id="playBtn" onclick="toggleAudio()">Play</button>
                <button class="control-btn" onclick="restartAudio()">Restart</button>
            </div>
            
            <audio id="audio-element" src="{audio_data_uri}"></audio>
        </div>

        <script>
            const fullText = {js_text};
            const words = fullText.split(/\\s+/);
            const container = document.getElementById('subtitles');
            const audio = document.getElementById('audio-element');
            const blob = document.getElementById('blob');
            const playBtn = document.getElementById('playBtn');
            
            // Render words
            words.forEach((w, i) => {{
                const span = document.createElement('span');
                span.className = 'word';
                span.id = 'word-' + i;
                span.innerText = w;
                container.appendChild(span);
            }});
            
            function toggleAudio() {{
                if (audio.paused) {{
                    audio.play();
                    playBtn.innerText = "Pause";
                    blob.classList.add('speaking');
                }} else {{
                    audio.pause();
                    playBtn.innerText = "Play";
                    blob.classList.remove('speaking');
                }}
            }}
            
            function restartAudio() {{
                audio.currentTime = 0;
                audio.play();
                playBtn.innerText = "Pause";
                blob.classList.add('speaking');
            }}
            
            function closeAgent() {{
                // Inform Streamlit to reset
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: 'close'
                }}, '*');
                
                // For immediate visual feedback
                document.body.style.display = 'none';
                
                // Try to find the Streamlit close button and click it if possible
                // (though postMessage is cleaner if handled)
            }}
            
            audio.onended = () => {{
                playBtn.innerText = "Play";
                blob.classList.remove('speaking');
            }};
            
            audio.ontimeupdate = () => {{
                if (audio.duration) {{
                    const progress = audio.currentTime / audio.duration;
                    const currentIndex = Math.floor(progress * words.length);
                    const windowSize = 25;
                    
                    for (let i = 0; i < words.length; i++) {{
                        const span = document.getElementById('word-' + i);
                        if (!span) continue;
                        
                        // Reset display first
                        span.style.display = 'inline-block';
                        
                        if (i < currentIndex) {{
                            span.className = 'word past';
                            span.style.display = 'none';
                        }} else if (i === currentIndex) {{
                            span.className = 'word active';
                        }} else if (i < currentIndex + windowSize) {{
                            span.className = 'word upcoming';
                        }} else {{
                            span.className = 'word';
                            span.style.display = 'none';
                        }}
                    }}
                }}
            }};
            
            // Attempt auto-play (browsers often block this, so playBtn is backup)
            window.onload = () => {{
                audio.play().catch(() => console.log("Autoplay blocked"));
            }};
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=1000, width=1500)

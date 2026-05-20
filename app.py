
import gradio as gr
from model import AdvancedAIHumanizer

humanizer = AdvancedAIHumanizer()


def estimate_ai_score(text):
    """Simple AI score estimation using perplexity and burstiness"""

    perplexity = humanizer.calculate_perplexity(text)
    burstiness = humanizer.calculate_burstiness(text)

    ai_score = 50

    if perplexity > 40:
        ai_score -= 25
    else:
        ai_score += 20

    if burstiness > 0.5:
        ai_score -= 25
    else:
        ai_score += 20

    ai_score = max(0, min(100, ai_score))

    if ai_score <= 20:
        status = "🟢 Very Human"
    elif ai_score <= 40:
        status = "🟡 Mostly Human"
    elif ai_score <= 60:
        status = "🟠 Mixed"
    else:
        status = "🔴 Likely AI"

    return f"""
AI Detection Score: {ai_score}%

Status: {status}

Perplexity: {perplexity:.1f}
Burstiness: {burstiness:.2f}
"""


def process_text_advanced(input_text, intensity):
    if not input_text or len(input_text.strip()) < 10:
        return "Please enter at least 10 characters of text.", "No analysis available.", "No AI score available."

    try:
        result = humanizer.humanize_text(input_text, intensity)
        analysis = humanizer.get_detailed_analysis(result)
        ai_score = estimate_ai_score(result)

        return result, analysis, ai_score

    except Exception as e:
        return f"Error: {str(e)}", "Processing failed.", "AI score failed."


with open("styles.css", "r") as f:
    custom_css = f.read()


with gr.Blocks(
    title="HumanizeAI",
    theme=gr.themes.Soft()
) as app:

    gr.HTML(f"""
    <style>
    {custom_css}
    </style>
    """)  

    gr.HTML("""
    <div class="page">

        <!-- NAVBAR -->
        <div class="navbar">

            <div class="logo-wrap">
                <div class="logo-icon"></div>
                <div class="logo-text">HumanizeAI</div>
            </div>

            <div class="nav-links">
                <span>Home</span>
                <span>Humanizer</span>
                <span>AI Detector</span>
                <span>Pricing</span>
                <span>Blog</span>
            </div>

            <div class="nav-actions">
                <button class="login-btn">Log in</button>
                <button class="start-btn">Get Started Free</button>
            </div>

        </div>

        <!-- HERO -->
        <div class="hero-section">

            <div class="hero-left">

                <div class="hero-badge">
                    #1 AI Humanizer & AI Detector
                </div>

                <h1>
                    Humanize AI Text.<br>
                    <span>Bypass AI Detection.</span>
                </h1>

                <p>
                    Make AI content sound natural, undetectable,
                    and 100% human instantly.
                </p>

                <div class="hero-buttons">
                    <button class="hero-btn primary">
                        Humanize Text
                    </button>

                    <button class="hero-btn secondary">
                        Check AI Score
                    </button>
                </div>

            </div>
    """)

    with gr.Row(elem_classes="main-grid"):

        # LEFT INPUT
        with gr.Column(scale=1, elem_classes="glass-card"):

            gr.HTML("""
            <div class="editor-title">
                Your AI Content
            </div>
            """)

            input_text = gr.Textbox(
                placeholder="Paste your AI generated text...",
                lines=18,
                elem_classes="modern-input",
                show_label=False
            )

            intensity = gr.Radio(
                choices=[
                    ("Light", "light"),
                    ("Standard", "standard"),
                    ("Heavy", "heavy")
                ],
                value="standard",
                label="Humanization Level",
                elem_classes="radio-modern"
            )

            btn = gr.Button(
                "✨ Humanize",
                elem_classes="humanize-btn"
            )

        # RIGHT OUTPUT
        with gr.Column(scale=1, elem_classes="glass-card"):

            gr.HTML("""
            <div class="editor-title">
                Humanized Output
            </div>
            """)

            output_text = gr.Textbox(
                lines=18,
                show_label=False,
                elem_classes="modern-output"
            )

            ai_score_box = gr.Textbox(
                label="AI Detection Score",
                lines=6,
                elem_classes="score-box"
            )

            analysis = gr.Textbox(
                label="Detection Analysis",
                lines=8,
                elem_classes="analysis-box"
            )

    gr.HTML("""

        </div>

        <!-- FEATURES -->

        <div class="feature-section">

            <div class="section-header">
                <span>FEATURES</span>
                <h2>Powerful Tools. Human Results.</h2>
            </div>

            <div class="feature-grid">

                <div class="feature-card">
                    <div class="feature-icon purple">✦</div>
                    <h3>Advanced Humanizer</h3>
                    <p>
                        Rewrite AI text naturally with human tone.
                    </p>
                </div>

                <div class="feature-card">
                    <div class="feature-icon green">🛡</div>
                    <h3>AI Score Checker</h3>
                    <p>
                        Real-time AI probability detection system.
                    </p>
                </div>

                <div class="feature-card">
                    <div class="feature-icon blue">⚡</div>
                    <h3>Bypass Detection</h3>
                    <p>
                        Optimized rewriting for AI detectors.
                    </p>
                </div>

            </div>

        </div>

    </div>
    """)

    btn.click(
        fn=process_text_advanced,
        inputs=[input_text, intensity],
        outputs=[output_text, analysis, ai_score_box]
    )

    input_text.submit(
        fn=process_text_advanced,
        inputs=[input_text, intensity],
        outputs=[output_text, analysis, ai_score_box]
    )


if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )
  

import streamlit as st
import requests
import fitz
import html
import platform


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Offline AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "theme" not in st.session_state:
    st.session_state.theme = "system"


# ============================================================
# NAVIGATION FUNCTIONS
# ============================================================

def go_home():
    st.session_state.page = "home"


def go_tutor():
    st.session_state.page = "tutor"


def go_quiz():
    st.session_state.page = "quiz"


def go_pdf():
    st.session_state.page = "pdf"


# ============================================================
# THEME FUNCTIONS
# ============================================================

def set_light():
    st.session_state.theme = "light"


def set_dark():
    st.session_state.theme = "dark"


def set_system():
    st.session_state.theme = "system"


# ============================================================
# DETERMINE THEME
# ============================================================

# Streamlit itself does not expose the user's OS theme directly
# to Python. "System" therefore uses the light design as the
# safe default when no browser theme detection is available.

if st.session_state.theme == "dark":

    bg_color = "#0f0b1a"
    card_color = "#1b1528"
    text_color = "#f5f3ff"
    secondary_text = "#b8aecb"
    border_color = "#33264d"
    input_color = "#211a30"

elif st.session_state.theme == "light":

    bg_color = "#faf9ff"
    card_color = "#ffffff"
    text_color = "#24164f"
    secondary_text = "#716b82"
    border_color = "#e7dfff"
    input_color = "#ffffff"

else:

    bg_color = "#faf9ff"
    card_color = "#ffffff"
    text_color = "#24164f"
    secondary_text = "#716b82"
    border_color = "#e7dfff"
    input_color = "#ffffff"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
<style>

.stApp {{
    background:
        radial-gradient(
            circle at 10% 10%,
            #eee7ff 0%,
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 90%,
            #e8ddff 0%,
            transparent 30%
        ),
        {bg_color};

    color: {text_color};
}}

.block-container {{
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}}


/* ============================================================
   TOP BAR
   ============================================================ */

.top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;

    margin-bottom: 15px;
}}

.app-mini-title {{
    font-size: 18px;
    font-weight: 800;
    color: {text_color};
}}


/* ============================================================
   HERO
   ============================================================ */

.hero {{
    background:
        linear-gradient(
            135deg,
            #4c1d95,
            #6d28d9,
            #8b5cf6
        );

    padding: 55px 30px;
    border-radius: 30px;

    text-align: center;
    color: white;

    box-shadow:
        0 20px 50px rgba(91, 33, 182, 0.28);

    margin-bottom: 40px;
}}

.hero-title {{
    font-size: 46px;
    font-weight: 800;
}}

.hero-subtitle {{
    font-size: 19px;
    margin-top: 12px;
    opacity: 0.92;
}}

.offline-badge {{
    display: inline-block;

    margin-top: 24px;
    padding: 10px 22px;

    border-radius: 50px;

    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.30);

    font-size: 14px;
    font-weight: 600;
}}


/* ============================================================
   WELCOME
   ============================================================ */

.welcome {{
    text-align: center;
    margin: 35px 0;
}}

.welcome-title {{
    font-size: 31px;
    font-weight: 800;
    color: {text_color};
}}

.welcome-text {{
    color: {secondary_text};
    font-size: 16px;
    margin-top: 8px;
}}


/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature-card {{
    background: {card_color};

    border-radius: 22px;

    padding: 28px;

    min-height: 205px;

    border: 1px solid {border_color};

    box-shadow:
        0 8px 25px rgba(50,30,100,0.07);
}}

.feature-icon {{
    font-size: 42px;
    margin-bottom: 12px;
}}

.feature-title {{
    font-size: 21px;
    font-weight: 750;
    color: {text_color};
    margin-bottom: 8px;
}}

.feature-text {{
    color: {secondary_text};
    font-size: 15px;
    line-height: 1.6;
}}


/* ============================================================
   SECTION
   ============================================================ */

.section-title {{
    font-size: 30px;
    font-weight: 800;
    color: {text_color};
    margin-top: 20px;
}}

.section-text {{
    color: {secondary_text};
    font-size: 16px;
    margin-bottom: 20px;
}}


/* ============================================================
   INPUT
   ============================================================ */

.stTextInput input {{
    border-radius: 14px;

    border: 1px solid {border_color};

    background: {input_color};

    color: {text_color};

    padding: 13px 15px;
}}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {{
    background: {card_color};
    border-radius: 18px;
    padding: 10px;
}}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {{
    width: 100%;

    border: none;

    border-radius: 14px;

    background:
        linear-gradient(
            135deg,
            #6d28d9,
            #8b5cf6
        );

    color: white;

    font-weight: 700;

    padding: 12px 20px;

    transition: all 0.25s ease;
}}

.stButton > button:hover {{
    transform: translateY(-3px);

    box-shadow:
        0 10px 25px rgba(109,40,217,0.30);
}}


/* ============================================================
   RESPONSE
   ============================================================ */

.response-card {{
    background: {card_color};

    padding: 26px;

    border-radius: 20px;

    border-left: 5px solid #7c3aed;

    box-shadow:
        0 8px 25px rgba(50,30,100,0.08);

    margin-top: 20px;

    color: {text_color};

    line-height: 1.7;
}}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {{
    text-align: center;

    margin-top: 55px;

    padding-top: 22px;

    color: {secondary_text};

    border-top: 1px solid {border_color};

    font-size: 14px;
}}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# OLLAMA
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


# ============================================================
# TOP SETTINGS BUTTON
# ============================================================

if st.session_state.page != "home":

    col_back, col_space, col_settings = st.columns(
        [2, 7, 2]
    )

    with col_back:

        st.button(
            "← Home",
            on_click=go_home,
            key="top_home"
        )

    with col_settings:

        settings_open = st.popover("⋮ Settings")

        with settings_open:

            st.markdown("### ⚙️ Settings")

            st.markdown("**🎨 Theme**")

            st.button(
                "☀️ Light",
                on_click=set_light,
                key="theme_light"
            )

            st.button(
                "🌙 Dark",
                on_click=set_dark,
                key="theme_dark"
            )

            st.button(
                "🖥️ System",
                on_click=set_system,
                key="theme_system"
            )

            st.caption(
                f"Current theme: {st.session_state.theme.title()}"
            )


else:

    col_title, col_space, col_settings = st.columns(
        [5, 4, 2]
    )

    with col_title:

        st.html("""
        <div class="app-mini-title">
            🎓 Offline AI Tutor
        </div>
        """)

    with col_settings:

        settings_open = st.popover("⋮ Settings")

        with settings_open:

            st.markdown("### ⚙️ Settings")

            st.markdown("**🎨 Theme**")

            st.button(
                "☀️ Light",
                on_click=set_light,
                key="home_theme_light"
            )

            st.button(
                "🌙 Dark",
                on_click=set_dark,
                key="home_theme_dark"
            )

            st.button(
                "🖥️ System",
                on_click=set_system,
                key="home_theme_system"
            )

            st.caption(
                f"Current theme: {st.session_state.theme.title()}"
            )


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    st.html("""
    <div class="hero">

        <div class="hero-title">
            🎓 Offline AI Tutor
        </div>

        <div class="hero-subtitle">
            Your Personal AI-Powered Study Companion
        </div>

        <div class="offline-badge">
            🟢 100% Local &nbsp; • &nbsp;
            🔒 Private &nbsp; • &nbsp;
            ⚡ Fast
        </div>

    </div>
    """)

    st.html("""
    <div class="welcome">

        <div class="welcome-title">
            Welcome, Student! 👋
        </div>

        <div class="welcome-text">
            Learn smarter with your private AI study assistant.
            Choose a learning mode below to get started.
        </div>

    </div>
    """)

    col1, col2, col3 = st.columns(3)


    # ========================================================
    # AI TUTOR CARD
    # ========================================================

    with col1:

        st.html("""
        <div class="feature-card">

            <div class="feature-icon">
                🤖
            </div>

            <div class="feature-title">
                Ask AI Tutor
            </div>

            <div class="feature-text">
                Ask questions and get instant
                explanations from your local AI tutor.
            </div>

        </div>
        """)

        st.button(
            "Start AI Tutor →",
            on_click=go_tutor,
            key="home_tutor"
        )


    # ========================================================
    # QUIZ CARD
    # ========================================================

    with col2:

        st.html("""
        <div class="feature-card">

            <div class="feature-icon">
                🧠
            </div>

            <div class="feature-title">
                Generate Quiz
            </div>

            <div class="feature-text">
                Create AI-generated multiple-choice
                questions to test your knowledge.
            </div>

        </div>
        """)

        st.button(
            "Create Quiz →",
            on_click=go_quiz,
            key="home_quiz"
        )


    # ========================================================
    # PDF CARD
    # ========================================================

    with col3:

        st.html("""
        <div class="feature-card">

            <div class="feature-icon">
                📚
            </div>

            <div class="feature-title">
                Ask from PDF
            </div>

            <div class="feature-text">
                Upload your study material and ask
                questions directly from your PDF.
            </div>

        </div>
        """)

        st.button(
            "Open PDF Tutor →",
            on_click=go_pdf,
            key="home_pdf"
        )


    st.html("""
    <div class="footer">

        🎓 Offline AI Tutor
        <br><br>

        Powered by Ollama + Llama 3.2
        <br>

        🔒 Your study data stays on your local system.

    </div>
    """)


# ============================================================
# AI TUTOR PAGE
# ============================================================

elif st.session_state.page == "tutor":

    st.html("""
    <div class="section-title">
        🤖 Ask AI Tutor
    </div>

    <div class="section-text">
        Your personal offline AI study assistant.
    </div>
    """)

    question = st.text_input(
        "Your question",
        placeholder="Example: Explain machine learning in simple words..."
    )

    if st.button(
        "✨ Ask AI",
        key="ask_ai"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            prompt = f"""
You are an educational AI tutor.

Explain the following question clearly
and in simple language for a student.

Question:
{question}
"""

            data = {
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }

            try:

                with st.spinner(
                    "🤖 AI Tutor is thinking..."
                ):

                    response = requests.post(
                        OLLAMA_URL,
                        json=data,
                        timeout=120
                    )

                    response.raise_for_status()

                    result = response.json()

                    answer = result.get(
                        "response",
                        "No response received."
                    )

                safe_answer = html.escape(
                    answer
                ).replace(
                    "\n",
                    "<br>"
                )

                st.html(f"""
                <div class="response-card">

                    <strong>
                        🤖 AI Tutor Response
                    </strong>

                    <br><br>

                    {safe_answer}

                </div>
                """)

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to Ollama. "
                    "Please make sure Ollama is running."
                )

            except Exception as e:

                st.error(
                    f"❌ Something went wrong: {e}"
                )


# ============================================================
# QUIZ PAGE
# ============================================================

elif st.session_state.page == "quiz":

    st.html("""
    <div class="section-title">
        🧠 Generate Quiz
    </div>

    <div class="section-text">
        Test your knowledge with an AI-generated quiz.
    </div>
    """)

    topic = st.text_input(
        "Enter a topic",
        placeholder="Example: Artificial Intelligence"
    )

    if st.button(
        "🧠 Generate Quiz",
        key="generate_quiz"
    ):

        if not topic.strip():

            st.warning(
                "Please enter a topic."
            )

        else:

            prompt = f"""
Create a quiz about {topic}.

Generate 5 multiple-choice questions.

Each question must have:

A. Option A
B. Option B
C. Option C
D. Option D

Clearly provide the correct answer
after each question.
"""

            data = {
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }

            try:

                with st.spinner(
                    "🧠 Creating your quiz..."
                ):

                    response = requests.post(
                        OLLAMA_URL,
                        json=data,
                        timeout=120
                    )

                    response.raise_for_status()

                    result = response.json()

                    answer = result.get(
                        "response",
                        "No quiz generated."
                    )

                safe_answer = html.escape(
                    answer
                ).replace(
                    "\n",
                    "<br>"
                )

                st.html(f"""
                <div class="response-card">

                    <strong>
                        🧠 Your Quiz
                    </strong>

                    <br><br>

                    {safe_answer}

                </div>
                """)

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to Ollama."
                )

            except Exception as e:

                st.error(
                    f"❌ Something went wrong: {e}"
                )


# ============================================================
# PDF PAGE
# ============================================================

elif st.session_state.page == "pdf":

    st.html("""
    <div class="section-title">
        📚 Ask from PDF
    </div>

    <div class="section-text">
        Upload your study material and ask questions from it.
    </div>
    """)

    uploaded_file = st.file_uploader(
        "Upload your study PDF",
        type=["pdf"]
    )

    if uploaded_file:

        try:

            document = fitz.open(
                stream=uploaded_file.getvalue(),
                filetype="pdf"
            )

            pdf_text = ""

            for page in document:

                pdf_text += page.get_text()

            document.close()

            pdf_text = pdf_text[:10000]

            if pdf_text.strip():

                st.success(
                    f"📄 {uploaded_file.name} uploaded successfully!"
                )

                question = st.text_input(
                    "Ask a question about the PDF",
                    placeholder="Example: What is the main topic of this document?"
                )

                if st.button(
                    "📖 Ask from PDF",
                    key="ask_pdf"
                ):

                    if not question.strip():

                        st.warning(
                            "Please enter a question."
                        )

                    else:

                        prompt = f"""
You are an educational AI tutor.

Answer the student's question using
ONLY the study material provided below.

If the answer is not present in the
study material, say:

"The answer is not available in
the uploaded PDF."

STUDY MATERIAL:

{pdf_text}

QUESTION:

{question}
"""

                        data = {
                            "model": MODEL,
                            "prompt": prompt,
                            "stream": False
                        }

                        try:

                            with st.spinner(
                                "📚 Reading your study material..."
                            ):

                                response = requests.post(
                                    OLLAMA_URL,
                                    json=data,
                                    timeout=120
                                )

                                response.raise_for_status()

                                result = response.json()

                                answer = result.get(
                                    "response",
                                    "No response received."
                                )

                            safe_answer = html.escape(
                                answer
                            ).replace(
                                "\n",
                                "<br>"
                            )

                            st.html(f"""
                            <div class="response-card">

                                <strong>
                                    📚 PDF Tutor Response
                                </strong>

                                <br><br>

                                {safe_answer}

                            </div>
                            """)

                        except requests.exceptions.ConnectionError:

                            st.error(
                                "❌ Cannot connect to Ollama."
                            )

                        except Exception as e:

                            st.error(
                                f"❌ Something went wrong: {e}"
                            )

            else:

                st.warning(
                    "⚠️ No readable text was found in this PDF."
                )

        except Exception as e:

            st.error(
                f"❌ Unable to read the PDF: {e}"
            )
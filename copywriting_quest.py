import time
import os
import json
import openai
import streamlit as st
from streamlit_lottie import st_lottie
from tenacity import retry, stop_after_attempt, wait_random_exponential

def main():
    set_page_config()
    custom_css()
    hide_elements()
    sidebar()
    title_and_description()
    input_section()

def set_page_config():
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
        page_icon="img/logo.png"
    )

def custom_css():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            [class="st-emotion-cache-7ym5gk ef3psqc12"] {
                display: inline-block;
                padding: 5px 20px;
                background-color: #4681f4;
                color: #FBFFFF;
                width: 300px;
                height: 35px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

def hide_elements():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

def sidebar():
    st.sidebar.image("img/alwrity.jpeg", use_column_width=True)
    st.sidebar.markdown("🧕 :red[Checkout Alwrity], complete **AI writer & Blogging solution**:[Alwrity](https://alwrity.netlify.app)")


def title_and_description():
    st.title("✍️ Alwrity - AI Generator for QUEST Copywriting Formula")
    with st.expander("What is **QUEST Copywriting Formula** & **How to Use**? 📝❗"):
        st.markdown('''
            ### What's QUEST Copywriting Formula, and How to use this AI generator 🗣️
            ---
            #### QUEST Copywriting Formula

            QUEST is an acronym for Question-Unpack-Emphasize-Solution-Transform. It's a copywriting framework that focuses on guiding the audience through different stages:

            1. **Question**: Presenting a thought-provoking question to engage the audience.
            2. **Unpack**: Unpacking the question by elaborating on its implications and relevance.
            3. **Emphasize**: Emphasizing the importance or significance of the topic.
            4. **Solution**: Presenting your product or service as the solution to the question.
            5. **Transform**: Describing the transformation or improvement your solution offers.

            The QUEST formula helps in creating engaging and persuasive copy that leads the audience to explore the solution.

            #### QUEST Copywriting Formula: Simple Example

            - **Question**: "Ever wondered how to boost your productivity?"
            - **Unpack**: "Let's delve into the strategies and tools that can help you achieve more in less time."
            - **Emphasize**: "Productivity is key to success in today's fast-paced world."
            - **Solution**: "Our productivity app provides a seamless solution to streamline your workflow."
            - **Transform**: "Experience a new level of efficiency and effectiveness with our app."

            ---
        ''')


def input_section():
    with st.expander("**PRO-TIP** - Easy Steps to Create Compelling QUEST Copy", expanded=True):
        col1, space, col2 = st.columns([5, 0.1, 5])
        with col1:
            brand_name = st.text_input('Enter Brand/Company Name',
                               help="Enter the name of your brand or company.")
            question = st.text_input('Present a Thought-Provoking Question to Engage Your Audience',
                             help="Pose a question that resonates with your audience.",
                             placeholder="Cities less polluted? future of remote work? Stress Free holidays ?")
            solution = st.text_input(f'Present Your Product or Service as the Solution for {brand_name}\'s Audience',
                             help="Introduce your product or service as the solution to the question.",
                             placeholder="Our new app reduces, Our team ensures comfort, App is fastest...")

        with col2:
            unpack = st.text_input(f'Elaborate on the Question by Unpacking its Implications',
                           help="Provide context and detail to the question.",
                           placeholder="Environmental impact, societal benefits, Safe travels, Better service...")
            emphasize = st.text_input(f'Emphasize the Importance or Significance of the Topic',
                              help="Highlight the relevance and impact of the topic.",
                              placeholder="Sustainability is crucial, Relaxed holidays, Faster services, Support...")

        if st.button('**Get QUEST Copy**'):
            if question.strip() and unpack.strip() and emphasize.strip() and solution.strip():
                with st.spinner("Generating QUEST Copy..."):
                    quest_copy = generate_quest_copy(brand_name, question, unpack, emphasize, solution)
                    if quest_copy:
                        st.subheader('**👩🔬👩🔬 Your QUEST Copy**')
                        st.markdown(quest_copy)
                    else:
                        st.error("💥 **Failed to generate QUEST copy. Please try again!**")
            else:
                st.error("All fields are required!")

    page_bottom()


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_quest_copy(brand_name, question, unpack, emphasize, solution):
    prompt = f"""As an expert copywriter, I need your help in creating a marketing campaign for {brand_name}. 
        Your task is to use the QUEST (Question-Unpack-Emphasize-Solution-Transform) formula to craft compelling copy.
        Here's the breakdown:
        - Question: {question}
        - Unpack: {unpack}
        - Emphasize: {emphasize}
        - Solution: {solution}
        Do not provide explanations, provide the final marketing copy.
    """
    return openai_chatgpt(prompt)


def page_bottom():
    """Display the bottom section of the web app."""
    data_oracle = import_json(r"lottie_files/brain_robot.json")
    st_lottie(data_oracle, width=600, key="oracle")

    st.markdown('''
    Copywrite using QUEST Copywriting Formula - powered by AI (OpenAI, Gemini Pro).

    Implemented by [Alwrity](https://alwrity.netlify.app).

    Learn more about [Google's Stance on AI generated content](https://alwrity.netlify.app/post/googles-guidelines-on-using-ai-generated-content-everything-you-need-to-know).
    ''')

    st.markdown("""
    ### Question:
    Have you ever wondered how to boost your productivity?

    ### Unpack:
    Let's delve into the strategies and tools that can help you achieve more in less time.

    ### Emphasize:
    Productivity is key to success in today's fast-paced world.

    ### Solution:
    Our productivity app provides a seamless solution to streamline your workflow.

    ### Transform:
    Experience a new level of efficiency and effectiveness with our app.
    """)


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", max_tokens=500, top_p=0.9, n=1):
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"An error occurred: {err}")


# Function to import JSON data
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url



if __name__ == "__main__":
    main()


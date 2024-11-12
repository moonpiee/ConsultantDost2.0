import streamlit as st
from layout import footer
st.set_page_config(
    page_title="Glossary",
    page_icon="https://cdn-icons-png.flaticon.com/128/1189/1189175.png",
)
st.title("Glossary of Model Settings")

# Model Section
st.header("Model")
st.markdown("""
The language model to use for generating output. The following models are available:

1. **Llama3–70b-8192**: Best overall model with high performance.
2. **Llama3–8b-8192**: A smaller variant of Llama3, optimized for efficiency.
3. **Mixtral-8x7b-32768**: Best for long contexts, capable of handling extensive inputs.
4. **Gemma2-9b-It**: An advanced model with improved capabilities.
5. **Gemma-7b-It**: A versatile model suitable for a variety of tasks.
6. **Llama-3.2-11b-Text-Preview**: A preview model for text generation tasks.
7. **Llama-3.1-70b-Versatile**: A highly versatile model for diverse applications.
""")
# Temperature Section
st.header("Temperature")
st.markdown("""
Controls the randomness of the response. This ranges from 0.0 to 1.0:
- **0.0**: Deterministic responses, less creative.
- **1.0**: Highly random and creative responses.
""")

st.markdown("That's all! You are ready to experiment!!")

footer()
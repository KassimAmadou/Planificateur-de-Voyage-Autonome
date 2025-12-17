import streamlit as st
from langchain_community.callbacks import StreamlitCallbackHandler
from agent_logic import get_agent
from utils import create_pdf, get_pdf_download_link
from prompts import get_travel_prompt
import re


st.set_page_config(page_title="Travel Planner", layout="wide")

# --- UTILITY FUNCTIONS ---
def extract_info(text, keyword):
    """
    Extracts specific information from text based on a keyword.
    
    Args:
        text (str): The full text to analyze.
        keyword (str): The keyword to identify the line.
    
    Returns:
        str: The extracted information after ':', or 'See details' if not found.
    """
    lines = text.split('\n')
    for line in lines:
        if keyword.lower() in line.lower() and ":" in line:
            return line.split(':', 1)[1].strip().replace('*', '')
    return "See details"

def parse_itinerary_days(text):
    """
    Parses the text to extract the days of the itinerary.
    
    Args:
        text (str): The text containing the itinerary.
    
    Returns:
        list: List of dictionaries with 'title', 'subtitle', 'content' for each day.
    """
    days = []
    pattern = r"(Jour \d+|Day \d+)(.*?)(?=Jour \d+|Day \d+|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    for match in matches:
        day_title = match[0].strip().replace(":", "")
        content = match[1].strip()
        if content.startswith(":"): content = content[1:].strip()
        
        lines = content.split('\n')
        subtitle = lines[0] if lines else ""
        details = "\n".join(lines[1:]) if len(lines) > 1 else ""
        
        if not details: details, subtitle = subtitle, "Daily schedule"
        days.append({"title": day_title, "subtitle": subtitle, "content": details})
    return days


with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=80)
    st.title("Generative AI Project")
    st.info("**Objective:** Autonomous agent (ReAct) planning trips from A to Z.")
    
    st.write("### Group Members")
    st.write("- **AMADOU Kassim**")
    st.write("- **AZEMAR Solene**")
    st.write("- **BELET Marine**")
    st.write("- **BENABDELJALIL Yanis**")
    st.divider()
    st.caption("ING 5 - 2025")

# --- MAIN INTERFACE ---
st.title("Autonomous Travel Planner")
st.markdown("Describe your trip, the AI handles flights, weather, car, and activities with interactive links.")
st.divider()


if "plan_result" not in st.session_state:
    st.session_state["plan_result"] = None
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

# Demo Button Function
def remplir_exemple():
    """
    Fills the text field with an example travel request.
    """
    st.session_state["input_text"] = (
        "I want to go to New York for Christmas (December 20 to 27) with my fiancée. "
        "Comfortable budget. We like museums, gastronomy, and seeing snow. "
        "Find me flights, a nice hotel, and romantic activities."
    )

with st.container():
    st.button("Fill with a test example", on_click=remplir_exemple, type="secondary")
    col1, col2 = st.columns([2, 1])
    with col1:
        
        user_input = st.text_area(
            "Your travel request:",
            value=st.session_state["input_text"],
            key="widget_input",
            placeholder="Ex: Bali in March, 2 adults, medium budget...",
            height=150
        )
        
        if user_input != st.session_state["input_text"]:
            st.session_state["input_text"] = user_input

    with col2:
        st.write(""); st.write("")
        plan_btn = st.button("Start planning", type="primary", use_container_width=True)
        reset_btn = st.button("Reset", use_container_width=True)

    if reset_btn:
        st.session_state["plan_result"] = None
        st.session_state["input_text"] = ""
        st.rerun()

# --- AI EXECUTION ---
if plan_btn and user_input:
    st.write("### Analysis and Search in progress...")
    st_callback = StreamlitCallbackHandler(st.container())
    
    try:
        agent_executor = get_agent()
        # Call to separate prompt
        prompt_enriched = get_travel_prompt(user_input)
        
        response = agent_executor.invoke(
            {"input": prompt_enriched},
            {"callbacks": [st_callback]}
        )
        st.session_state["plan_result"] = response["output"]
        st.rerun()
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

# --- RESULTS DISPLAY ---
if st.session_state["plan_result"]:
    result = st.session_state["plan_result"]
    st.divider()
    st.success("Trip planned successfully!")
    

    st.subheader("Trip Summary")
    c1, c2, c3 = st.columns(3)
    c1.info(f"**Destination**\n\n{extract_info(result, 'DESTINATION')}")
    c2.info(f"**Period**\n\n{extract_info(result, 'PERIOD')}")
    c3.info(f"**Budget**\n\n{extract_info(result, 'BUDGET')}")
    c4, c5 = st.columns(2)
    c4.info(f"**Style**\n\n{extract_info(result, 'STYLE')}")
    c5.warning(f"**Weather**\n\n{extract_info(result, 'WEATHER')}")


    col_prat, col_trans = st.columns(2)
    with col_prat:
        with st.expander("Practical Info (Visa, Luggage)", expanded=True):
            if "[PRACTICAL]" in result:
                content = result.split("[PRACTICAL]")[1].split("[TRANSPORT]")[0].strip()
                st.markdown(content)
    with col_trans:
        with st.expander("Transport & Car (Mandatory)", expanded=True):
            if "[TRANSPORT]" in result:
                content = result.split("[TRANSPORT]")[1].split("[ITINERARY]")[0].strip()
                st.markdown(content)


    st.subheader("Interactive Itinerary")
    days = parse_itinerary_days(result)
    if days:
        for day in days:
            with st.expander(f"**{day['title']}** : {day['subtitle']}", expanded=False):
                st.markdown(day['content'])
    else:
        st.warning("Raw display:")
        st.write(result)

 
    st.divider()
    col_pdf, _ = st.columns([1, 2])
    with col_pdf:
        pdf_path = create_pdf(result)
        st.markdown(get_pdf_download_link(pdf_path), unsafe_allow_html=True)
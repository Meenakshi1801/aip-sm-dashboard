import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import datetime

# -------------------------------
# Basic Settings
# -------------------------------

st.set_page_config(
    page_title="AIP-SM Dashboard",
    page_icon="🤖",
    layout="wide"
)

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyupggsoyQTDI_DI1hBduBOjjksaRaMJ5YM9T0bJtrB6fAjCp9I0JPJl-Qo4PBj1xtS/exec"

# Embedded Google Form URLs
INITIAL_READINESS_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeiN0A4MueCQCgWq_dzEeUrquULAX8dIoGanSOKpigzLIHtqg/viewform?embedded=true"
FINAL_READINESS_URL = "https://docs.google.com/forms/d/e/1FAIpQLScQhRPS0Ah4XQwgvWPwo1KdwTK0SJYnaJX59geplh-siym5SA/viewform?embedded=true"
FEEDBACK_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfztEhAKjtwR658RyBHA3v39l_CT3yAUsF5wbG2dsXCOlW0kQ/viewform?embedded=true"

# Direct Google Form Links
INITIAL_READINESS_DIRECT_URL = "https://forms.gle/ZBRPQx2NQLcWdLCx5"
FINAL_READINESS_DIRECT_URL = "https://forms.gle/UZzoX4ArPU3FsK2T6"
FEEDBACK_DIRECT_URL = "https://forms.gle/6ruZCbMsRB5fXX4y6"


# -------------------------------
# Helper Functions
# -------------------------------

def submit_to_google_sheet(sheet_name, row):
    payload = {
        "sheet_name": sheet_name,
        "row": row
    }

    try:
        response = requests.post(APPS_SCRIPT_URL, json=payload, timeout=10)

        if response.status_code == 200:
            try:
                result = response.json()
                status = result.get("status", "")
                message = result.get("message", "Submission processed.")

                if status == "success":
                    return True, message
                elif status == "duplicate":
                    return False, message
                else:
                    return False, message

            except Exception:
                return False, "Submission response could not be read properly."

        else:
            return False, f"Submission failed. Status code: {response.status_code}"

    except Exception as e:
        return False, f"Error: {e}"


def user_code_instruction():
    st.info(
        """
        **User Code Instruction**

        Please create your User Code using this format:

        **AIP + last five digits of your mobile number**

        Example: If your mobile number ends with **78456**, your User Code will be **AIP78456**.

        Please use the same User Code in the initial readiness check, all dashboard activities, final portfolio, 
        final readiness reflection, and feedback form.
        """
    )


def single_submission_instruction():
    st.warning(
        """
        **Submission Rule**

        Please submit each module only once. Multiple submissions using the same User Code in the same section are not allowed.
        """
    )


def common_user_fields():
    user_code = st.text_input("User Code")
    programme = st.selectbox("Programme", ["B.Ed.", "M.Ed.", "Other"])
    year = st.selectbox("Year", ["First Year", "Second Year", "Other"])
    subject = st.text_input("Teaching Subject")
    topic = st.text_input("Selected Topic")
    return user_code, programme, year, subject, topic


def module_form(sheet_name, prompt_label, ai_label, revised_label, reflection_label):
    user_code_instruction()
    single_submission_instruction()

    with st.form(key=sheet_name):
        user_code, programme, year, subject, topic = common_user_fields()

        prompt = st.text_area(prompt_label, height=180)
        ai_response = st.text_area(ai_label, height=220)
        revised_output = st.text_area(revised_label, height=220)
        reflection = st.text_area(reflection_label, height=160)

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not user_code or not subject or not topic:
                st.error("Please fill User Code, Subject, and Topic before submitting.")
            elif not prompt or not ai_response or not revised_output:
                st.error("Please fill Prompt, AI Response, and Revised Output before submitting.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                row = [
                    timestamp,
                    user_code.strip().upper(),
                    programme,
                    year,
                    subject,
                    topic,
                    prompt,
                    ai_response,
                    revised_output,
                    reflection
                ]

                success, message = submit_to_google_sheet(sheet_name, row)

                if success:
                    st.success("Your submission has been saved successfully.")
                else:
                    st.error(message)


def embed_form(url, height=1400):
    components.iframe(url, height=height, scrolling=True)


def form_with_backup_button(embed_url, direct_url, button_text, height=1600):
    st.info(
        """
        If the form does not open properly on your mobile device, please use the button below to open it directly.
        """
    )

    st.link_button(button_text, direct_url)

    st.markdown("---")

    embed_form(embed_url, height=height)

    st.markdown("---")

    st.info(
        """
        If the embedded form above is not visible due to browser/cookie restrictions, please use the direct button below.
        """
    )

    st.link_button(button_text, direct_url)


def developer_section():
    col1, col2 = st.columns([1, 4])

    with col1:
        try:
            st.image("profile.jpg", width=150)
        except Exception:
            st.warning("Profile photo not found. Please upload profile.jpg to GitHub repository.")

    with col2:
        st.markdown(
            """
            ### Conceptualized and Developed by  
            **Dr. Meenakshi Dwivedi**  
            Assistant Professor  
            Department of Education / School of Education  
            Mahatma Jyotiba Phule Rohilkhand University, Bareilly, Uttar Pradesh, India
            """
        )


# -------------------------------
# Sidebar Navigation
# -------------------------------

st.sidebar.title("AIP-SM Dashboard")

page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Initial Readiness Check",
        "Module 1: Objective Prompting",
        "Module 2: Activity Prompting",
        "Module 3: Assessment Prompting",
        "Module 4: Inclusive Prompting",
        "Module 5: Ethical Verification",
        "Final Portfolio",
        "Final Readiness Reflection",
        "Dashboard Feedback"
    ]
)


# -------------------------------
# Home Page
# -------------------------------

if page == "Home":
    st.title("AIP-SM Dashboard")
    st.subheader("AI Prompt Scaffolding Model for Pedagogical Design Readiness")

    developer_section()

    st.markdown("---")

    st.markdown(
        """
        ### Purpose of the Dashboard

        The **AIP-SM Dashboard** is a web-based learning and practice platform designed to support 
        pre-service teachers, teacher educators, and students in developing responsible AI-supported 
        pedagogical design skills.

        The dashboard may be used for:

        - academic training,
        - teacher-education workshops,
        - online learning activities,
        - AI-supported lesson design practice,
        - and research-based intervention studies.
        """
    )

    st.info(
        """
        This dashboard is intended for educational, training, and academic purposes. Users are encouraged 
        to verify AI-generated content and apply their own pedagogical judgment before using it in academic 
        or classroom contexts.
        """
    )

    st.markdown(
        """
        ### Dashboard Activities

        Through this dashboard, you will complete module-wise activities related to:

        - Objective prompting
        - Activity prompting
        - Assessment prompting
        - Inclusive prompting
        - Ethical verification and reflective revision

        You will first complete the initial readiness check, then complete five modules, submit your final portfolio, 
        complete the final readiness reflection, and finally submit the dashboard feedback form.
        """
    )

    user_code_instruction()

    st.warning(
        """
        Please complete the activities in sequence:

        **Initial Readiness Check → Module 1 → Module 2 → Module 3 → Module 4 → Module 5 → Final Portfolio → Final Readiness Reflection → Dashboard Feedback**
        """
    )


# -------------------------------
# Initial Readiness Check Page
# -------------------------------

elif page == "Initial Readiness Check":
    st.title("Initial Readiness Check")
    st.subheader("AI-Supported Teaching Readiness")

    user_code_instruction()

    st.write(
        """
        Before beginning the AIP-SM activities, please complete this short readiness check. It will help you reflect 
        on your present understanding of AI-supported pedagogical design, lesson planning, assessment preparation, 
        inclusive adaptation, and ethical verification of AI-generated educational content.
        """
    )

    st.info(
        """
        There is no right or wrong answer. Please respond honestly based on your present understanding and experience.
        """
    )

    form_with_backup_button(
        embed_url=INITIAL_READINESS_URL,
        direct_url=INITIAL_READINESS_DIRECT_URL,
        button_text="Open AI-Supported Teaching Readiness Form",
        height=1600
    )


# -------------------------------
# Module 1
# -------------------------------

elif page == "Module 1: Objective Prompting":
    st.title("Module 1: Context and Objective Prompting")

    st.write(
        """
        This module will help you write structured AI prompts for generating learning objectives. 
        A good prompt should clearly mention the class, subject, topic, learner level, duration, 
        and expected learning outcome.
        """
    )

    st.markdown("### Prompt Formula")
    st.code(
        "Act as a teacher educator. Prepare clear and measurable learning objectives for Class [Class] students "
        "in the subject [Subject] on the topic [Topic]. The objectives should be suitable for a [Duration]-minute lesson "
        "and should be aligned with Bloom’s Taxonomy. Consider the learner level as [Learner Level]."
    )

    st.markdown("### Example Prompt")
    st.code(
        "Act as a teacher educator. Prepare clear and measurable learning objectives for Class 8 students in Science "
        "on the topic Photosynthesis. The objectives should be suitable for a 40-minute lesson and should be aligned "
        "with Bloom’s Taxonomy. Consider the learner level as mixed ability."
    )

    module_form(
        sheet_name="Module1_Objectives",
        prompt_label="Your prompt for learning objectives",
        ai_label="AI-generated objectives",
        revised_label="Your revised objectives",
        reflection_label="Reflection/Reason for Revision"
    )


# -------------------------------
# Module 2
# -------------------------------

elif page == "Module 2: Activity Prompting":
    st.title("Module 2: Activity Prompting")

    st.write(
        """
        This module will help you write AI prompts for designing learner-centred teaching-learning activities. 
        A good activity prompt should focus on participation, collaboration, questioning, conceptual understanding, 
        and available classroom resources.
        """
    )

    st.markdown("### Prompt Formula")
    st.code(
        "Act as a teacher educator. Suggest learner-centred teaching-learning activities for Class [Class] students "
        "in the subject [Subject] on the topic [Topic]. The activities should encourage student participation, "
        "collaboration, questioning, and conceptual understanding. The activity should be suitable for [Duration] minutes "
        "and should use available resources such as [Resources]."
    )

    st.markdown("### Example Prompt")
    st.code(
        "Act as a teacher educator. Suggest learner-centred teaching-learning activities for Class 8 students in Science "
        "on the topic Photosynthesis. The activities should encourage student participation, collaboration, questioning, "
        "and conceptual understanding. The activity should be suitable for 20 minutes and should use available resources "
        "such as blackboard, textbook, and worksheet."
    )

    module_form(
        sheet_name="Module2_Activities",
        prompt_label="Your prompt for teaching-learning activity",
        ai_label="AI-generated activity",
        revised_label="Your revised activity",
        reflection_label="Reflection/Reason for Revision"
    )


# -------------------------------
# Module 3
# -------------------------------

elif page == "Module 3: Assessment Prompting":
    st.title("Module 3: Assessment Prompting")

    st.write(
        """
        This module will help you write AI prompts for preparing assessment questions and tasks. 
        A good assessment prompt should ask for questions that are aligned with learning objectives 
        and suitable for the class level.
        """
    )

    st.markdown("### Prompt Formula")
    st.code(
        "Act as a teacher educator. Prepare formative assessment tasks for Class [Class] students in the subject [Subject] "
        "on the topic [Topic]. Include multiple-choice questions, short-answer questions, and one application-based question. "
        "The questions should be aligned with the learning objectives and suitable for the learner level [Learner Level]. "
        "Also provide answer keys or assessment criteria."
    )

    st.markdown("### Example Prompt")
    st.code(
        "Act as a teacher educator. Prepare formative assessment tasks for Class 8 students in Science on the topic "
        "Photosynthesis. Include multiple-choice questions, short-answer questions, and one application-based question. "
        "The questions should be aligned with the learning objectives and suitable for mixed-ability learners. "
        "Also provide answer keys or assessment criteria."
    )

    module_form(
        sheet_name="Module3_Assessment",
        prompt_label="Your prompt for assessment tasks",
        ai_label="AI-generated assessment tasks",
        revised_label="Your revised assessment tasks",
        reflection_label="Reflection/Reason for Revision"
    )


# -------------------------------
# Module 4
# -------------------------------

elif page == "Module 4: Inclusive Prompting":
    st.title("Module 4: Inclusive Prompting")

    st.write(
        """
        This module will help you write AI prompts for adapting teaching-learning material for diverse learners. 
        Inclusive prompting helps pre-service teachers consider slow learners, advanced learners, language needs, 
        accessibility, and varied learning styles.
        """
    )

    st.markdown("### Prompt Formula")
    st.code(
        "Act as an inclusive education expert. Adapt the teaching-learning activity for Class [Class] students "
        "in the subject [Subject] on the topic [Topic]. Suggest modifications for slow learners, advanced learners, "
        "students with language difficulty, and students with limited learning resources. The adaptation should be practical "
        "and suitable for the classroom context."
    )

    st.markdown("### Example Prompt")
    st.code(
        "Act as an inclusive education expert. Adapt the teaching-learning activity for Class 8 students in Science "
        "on the topic Photosynthesis. Suggest modifications for slow learners, advanced learners, students with language "
        "difficulty, and students with limited learning resources. The adaptation should be practical and suitable for the classroom context."
    )

    module_form(
        sheet_name="Module4_Inclusion",
        prompt_label="Your prompt for inclusive adaptation",
        ai_label="AI-generated inclusive adaptation",
        revised_label="Your revised inclusive adaptation",
        reflection_label="Reflection/Reason for Revision"
    )


# -------------------------------
# Module 5
# -------------------------------

elif page == "Module 5: Ethical Verification":
    st.title("Module 5: Ethical Verification and Reflective Revision")

    st.write(
        """
        This module will help you verify AI-generated educational content before using it. 
        AI output should not be copied directly. It should be checked for accuracy, bias, learner suitability, 
        originality, and pedagogical appropriateness.
        """
    )

    st.markdown("### Prompt Formula")
    st.code(
        "Act as a teacher educator and reviewer. Review the following AI-generated teaching material for factual accuracy, "
        "bias, learner suitability, age-appropriateness, originality, and pedagogical alignment. Suggest corrections and improvements. "
        "The material is for Class [Class], subject [Subject], topic [Topic]."
    )

    st.markdown("### Example Prompt")
    st.code(
        "Act as a teacher educator and reviewer. Review the following AI-generated teaching material for factual accuracy, "
        "bias, learner suitability, age-appropriateness, originality, and pedagogical alignment. Suggest corrections and improvements. "
        "The material is for Class 8, subject Science, topic Photosynthesis."
    )

    module_form(
        sheet_name="Module5_Ethics",
        prompt_label="Your prompt for ethical verification",
        ai_label="AI-generated verification response",
        revised_label="Corrections/Revisions made by you",
        reflection_label="Reflection/Reason for Revision"
    )


# -------------------------------
# Final Portfolio Page
# -------------------------------

elif page == "Final Portfolio":
    st.title("Final Portfolio Submission")
    st.subheader("AI-Supported Pedagogical Design Output")

    user_code_instruction()
    single_submission_instruction()

    st.write(
        """
        You have completed all five AIP-SM modules. Now submit your final AI-supported pedagogical design portfolio. 
        Combine your revised learning objectives, teaching-learning activity, assessment tasks, inclusive adaptation plan, 
        ethical verification note, and final reflection.

        Please ensure that the final output reflects your own pedagogical judgment and is not copied directly from AI-generated content.
        """
    )

    with st.form(key="Final_Portfolio"):
        user_code, programme, year, subject, topic = common_user_fields()

        final_objectives = st.text_area("Final Learning Objectives", height=180)
        final_activity = st.text_area("Final Teaching-Learning Activity", height=220)
        final_assessment = st.text_area("Final Assessment Tasks", height=220)
        inclusion_plan = st.text_area("Inclusive Adaptation Plan", height=200)
        ethics_note = st.text_area("Ethical Verification Note", height=180)
        final_reflection = st.text_area("Final Reflection", height=200)

        submitted = st.form_submit_button("Submit Final Portfolio")

        if submitted:
            if not user_code or not subject or not topic:
                st.error("Please fill User Code, Subject, and Topic before submitting.")
            elif not final_objectives or not final_activity or not final_assessment:
                st.error("Please fill Final Learning Objectives, Final Teaching-Learning Activity, and Final Assessment Tasks before submitting.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                row = [
                    timestamp,
                    user_code.strip().upper(),
                    programme,
                    year,
                    subject,
                    topic,
                    final_objectives,
                    final_activity,
                    final_assessment,
                    inclusion_plan,
                    ethics_note,
                    final_reflection
                ]

                success, message = submit_to_google_sheet("Final_Portfolio", row)

                if success:
                    st.success("Your final portfolio has been saved successfully.")
                else:
                    st.error(message)


# -------------------------------
# Final Readiness Reflection Page
# -------------------------------

elif page == "Final Readiness Reflection":
    st.title("Final Readiness Reflection")
    st.subheader("AI-Supported Teaching Readiness")

    user_code_instruction()

    st.write(
        """
        After completing all AIP-SM modules and submitting your final portfolio, please complete this final readiness reflection. 
        It will help you reflect on your learning, confidence, and readiness in using AI for pedagogical design.
        """
    )

    st.info(
        """
        There is no right or wrong answer. Please respond based on your present understanding and experience after completing the dashboard activities.
        """
    )

    form_with_backup_button(
        embed_url=FINAL_READINESS_URL,
        direct_url=FINAL_READINESS_DIRECT_URL,
        button_text="Open Final Readiness Reflection Form",
        height=1600
    )


# -------------------------------
# Dashboard Feedback Page
# -------------------------------

elif page == "Dashboard Feedback":
    st.title("Dashboard Feedback")
    st.subheader("AIP-SM Dashboard Experience")

    user_code_instruction()

    st.write(
        """
        Please complete this feedback form after finishing the final readiness reflection. Your feedback will help improve 
        the AIP-SM Dashboard for educational, training, workshop, online learning, and academic purposes.
        """
    )

    st.info(
        """
        Please select the response that best represents your experience with the dashboard.
        """
    )

    form_with_backup_button(
        embed_url=FEEDBACK_URL,
        direct_url=FEEDBACK_DIRECT_URL,
        button_text="Open Dashboard Feedback Form",
        height=1400
    )
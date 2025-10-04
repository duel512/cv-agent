"""
System prompt template for the personal AI assistant.
This module generates a well-structured prompt that guides the LLM to represent you professionally.
"""

import json
from pathlib import Path


def load_personal_info():
    """Load personal information from JSON file."""
    data_path = Path(__file__).parent / "data" / "personal_info.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_experience(experience_list):
    """Format experience section for the prompt."""
    formatted = []
    for exp in experience_list:
        exp_text = f"""
**{exp['title']}** at {exp['company']} ({exp['duration']})
Location: {exp['location']}
{exp['description']}
Key Achievements:
"""
        for achievement in exp['achievements']:
            exp_text += f"  • {achievement}\n"
        formatted.append(exp_text.strip())
    return "\n\n".join(formatted)


def format_education(education_list):
    """Format education section for the prompt."""
    formatted = []
    for edu in education_list:
        edu_text = f"""
**{edu['degree']}** in {edu['field']}
{edu['institution']}, {edu['location']}
Graduated: {edu['graduation_date']}
GPA: {edu.get('gpa', 'N/A')}
"""
        if edu.get('honors'):
            edu_text += "Honors: " + ", ".join(edu['honors']) + "\n"
        if edu.get('relevant_coursework'):
            edu_text += "Relevant Coursework: " + ", ".join(edu['relevant_coursework']) + "\n"
        formatted.append(edu_text.strip())
    return "\n\n".join(formatted)


def format_projects(projects_list):
    """Format projects section for the prompt."""
    formatted = []
    for proj in projects_list:
        proj_text = f"""
**{proj['name']}**
{proj['description']}
Technologies: {', '.join(proj['technologies'])}
Highlights:
"""
        for highlight in proj['highlights']:
            proj_text += f"  • {highlight}\n"
        if proj.get('link'):
            proj_text += f"Link: {proj['link']}\n"
        formatted.append(proj_text.strip())
    return "\n\n".join(formatted)


def format_skills(skills_dict):
    """Format skills section for the prompt."""
    formatted = []
    for category, skills in skills_dict.items():
        category_name = category.replace('_', ' ').title()
        formatted.append(f"**{category_name}**: {', '.join(skills)}")
    return "\n".join(formatted)


def generate_system_prompt():
    """Generate the complete system prompt with all personal information."""
    info = load_personal_info()

    prompt = f"""You are an AI assistant representing {info['name']}, a {info['title']}.

Your primary role is to provide information about {info['name'].split()[0]}'s professional background, qualifications, skills, and experience to potential recruiters, hiring managers, or anyone interested in learning more about them.

# IMPORTANT GUIDELINES

1. **Professional Tone**: Always maintain a professional, friendly, and helpful demeanor. You are representing a real person seeking opportunities.

2. **First-Person Perspective**: Speak as if you ARE {info['name']}. Use "I" and "my" when referring to their experience and qualifications.
   - Example: "I have 3 years of experience in..." NOT "They have 3 years..."

3. **Accuracy**: Only provide information that is explicitly stated in the context below. If asked about something not covered, politely say you don't have that specific information but offer related information if available.

4. **Conciseness**: Provide comprehensive but concise answers. Avoid unnecessary elaboration unless specifically asked for more detail.

5. **Engagement**: Be conversational and engaging. Show enthusiasm about the work and opportunities.

6. **Redirection**: If asked inappropriate questions or questions unrelated to professional qualifications, politely redirect the conversation.

7. **Call to Action**: When appropriate, encourage the person to reach out directly via the contact information provided.

# CONTEXT - COMPLETE PROFESSIONAL PROFILE

## Personal Information
**Name**: {info['name']}
**Title**: {info['title']}
**Location**: {info['contact']['location']}

**Contact Information**:
- Email: {info['contact']['email']}
- Phone: {info['contact'].get('phone', 'Available upon request')}
- LinkedIn: {info['contact'].get('linkedin', 'N/A')}
- GitHub: {info['contact'].get('github', 'N/A')}

## Professional Summary
{info['summary']}

## Education
{format_education(info['education'])}

## Professional Experience
{format_experience(info['experience'])}

## Technical Skills
{format_skills(info['skills'])}

## Notable Projects
{format_projects(info['projects'])}
"""

    # Add optional sections if they exist and are not empty
    if info.get('publications') and len(info['publications']) > 0:
        pubs = []
        for pub in info['publications']:
            pub_text = f"• {pub['title']} - {pub['venue']} ({pub['date']})"
            if pub.get('link'):
                pub_text += f" [{pub['link']}]"
            pubs.append(pub_text)
        prompt += "\n## Publications\n" + "\n".join(pubs) + "\n"

    if info.get('certifications') and len(info['certifications']) > 0:
        certs = [f"• {cert['name']} - {cert['issuer']} ({cert['date']})"
                 for cert in info['certifications']]
        prompt += "\n## Certifications\n" + "\n".join(certs) + "\n"

    if info.get('languages') and len(info['languages']) > 0:
        langs = [f"• {lang['language']}: {lang['proficiency']}"
                 for lang in info['languages']]
        prompt += "\n## Languages\n" + "\n".join(langs) + "\n"

    if info.get('interests') and len(info['interests']) > 0:
        prompt += "\n## Professional Interests\n" + "\n".join([f"• {interest}" for interest in info['interests']]) + "\n"

    # Add additional context
    if info.get('additional_info'):
        add_info = info['additional_info']
        prompt += "\n## Additional Context\n"

        if add_info.get('career_goals'):
            prompt += f"**Career Goals**: {add_info['career_goals']}\n"

        if add_info.get('personality'):
            prompt += f"**Working Style**: {add_info['personality']}\n"

        if add_info.get('availability'):
            prompt += f"**Availability**: {add_info['availability']}\n"

        if add_info.get('work_authorization'):
            prompt += f"**Work Authorization**: {add_info['work_authorization']}\n"

        if add_info.get('fun_facts') and len(add_info['fun_facts']) > 0:
            prompt += "\n**Fun Facts** (use sparingly and only when appropriate):\n"
            prompt += "\n".join([f"• {fact}" for fact in add_info['fun_facts']]) + "\n"

    # Add conversation examples and final instructions
    prompt += """

# CONVERSATION EXAMPLES

**Example 1 - General Inquiry**:
User: "Tell me about your background"
Assistant: "I'm a {title} with a strong foundation in {key_areas}. I graduated from {university} with a degree in {field} and have {X} years of experience in {domain}. I'm particularly passionate about {interest_area} and have worked on projects involving {technologies}. Would you like to know more about any specific aspect of my experience?"

**Example 2 - Specific Technical Question**:
User: "What experience do you have with Python?"
Assistant: "I have extensive experience with Python - it's one of my primary programming languages. I've used it for {specific_use_cases from experience}. In my role at {company}, I {specific_achievement}. I'm also familiar with frameworks like {frameworks_from_skills}. Would you like to hear about a specific project where I used Python?"

**Example 3 - Availability**:
User: "When can you start?"
Assistant: "{availability_info}. I'm very interested in learning more about the opportunity. Would you like to discuss the role in more detail? Feel free to reach out to me directly at {email}."

**Example 4 - Unknown Information**:
User: "What's your experience with Kubernetes?"
Assistant: "I don't have specific information about my Kubernetes experience in my profile, but I do have experience with {related_technologies}. If this is important for the role you're considering, I'd be happy to discuss my related experience and learning ability in more detail. You can reach me at {email}."

**Example 5 - Inappropriate Question**:
User: "What's your age?"
Assistant: "I appreciate your interest, but I'd prefer to focus on my professional qualifications and how I can contribute to your team. Is there anything specific about my experience or skills you'd like to discuss?"

# FINAL INSTRUCTIONS

- Always be helpful and informative
- Show genuine interest in opportunities that align with the profile
- If someone seems like a good fit, encourage them to reach out directly
- Maintain professionalism at all times
- Be honest about limitations or gaps in the provided information
- Use the context above as your single source of truth
- Do not make up or infer information not provided in the context
- Keep responses focused and relevant to job recruitment context

Remember: Your goal is to provide a positive, professional first impression that encourages recruiters to reach out for a conversation.
"""

    return prompt


def get_welcome_message():
    """Generate a welcoming first message for the chat interface."""
    info = load_personal_info()

    message = f"""Hello! I'm an AI assistant representing **{info['name']}**, a {info['title']}.

I'm here to answer any questions you might have about my background, experience, skills, and qualifications. Feel free to ask me about:
- My professional experience and achievements
- Technical skills and expertise
- Education and projects
- Career goals and interests
- Availability and contact information

How can I help you today?"""

    return message


if __name__ == "__main__":
    # Test the prompt generation
    print("=" * 80)
    print("GENERATED SYSTEM PROMPT")
    print("=" * 80)
    print(generate_system_prompt())
    print("\n" + "=" * 80)
    print("WELCOME MESSAGE")
    print("=" * 80)
    print(get_welcome_message())

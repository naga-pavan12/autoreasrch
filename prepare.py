"""
Benchmark Hydrator for PM Discovery Accelerator.
Sets up sample data for the 4 core research types.
"""
import os
import json

def write_sample(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(content, f, indent=2)

def main():
    # 1. Customer Interviews
    write_sample("research_types/customer_interviews/benchmark/mock_interview_01.json", {
        "id": "CI_01",
        "input_text": "User: I spend 2 hours a day manually syncing Jira and Trello. It's so frustrating because the fields don't match, and I often miss critical updates.",
        "expected_pain_points": [
            {
                "description": "Manual syncing between Jira and Trello takes 2 hours daily.",
                "required_keywords": ["syncing", "jira", "trello", "2 hours"]
            }
        ]
    })

    # 2. Competitor Research
    write_sample("research_types/competitor_research/benchmark/mock_competitor_01.json", {
        "id": "CR_01",
        "input_text": "Review: FeatureX by CompetitorA is great, but their pricing is opaque and they lack a public API, which makes it hard for us to automate our reporting.",
        "expected_problems": [
            {
                "description": "CompetitorA lacks a public API for reporting automation.",
                "required_keywords": ["API", "reporting", "automate"]
            }
        ]
    })

    # 3. Support Tickets
    write_sample("research_types/support_tickets/benchmark/mock_tickets_01.json", {
        "id": "ST_01",
        "input_text": "Ticket 1: Logins failing on Chrome 120.\nTicket 2: Chrome 120 users reporting white screen of death.\nTicket 3: Authentication issues for browser v120.",
        "expected_themes": [
            {
                "description": "Critical authentication failure on Chrome 120.",
                "required_keywords": ["authentication", "Chrome 120", "failing"]
            }
        ]
    })

    # 4. Synthesis
    write_sample("research_types/synthesis/benchmark/mock_synthesis_01.json", {
        "id": "SYN_01",
        "input_text": "Analysis Summary:\n1. Users losing 2 hours on syncing (High Impact).\n2. Competitor gap in API (Medium Impact).\n3. Chrome 120 auth issues (Urgent).",
        "expected_opportunities": [
            {
                "description": "Build automated sync connector for Jira/Trello.",
                "required_keywords": ["sync", "connector", "Jira"]
            }
        ]
    })

    print("Successfully hydrated benchmark folders for 4 core research types.")

if __name__ == "__main__":
    main()

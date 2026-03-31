from __future__ import annotations

from typing import Any, Dict, List


def load_dataset() -> List[Dict[str, Any]]:
    """
    Dataset estático e determinístico com 21 exemplos.
    Mantém a ordem fixa para evitar flakiness nos testes.
    """
    dataset = [
        {
            "bug_id": "BUG-001",
            "description": "The login button does nothing when clicked on mobile devices.",
            "expected_output": "As a mobile user, I want the login button to trigger authentication so that I can access my account.",
        },
        {
            "bug_id": "BUG-002",
            "description": "The dashboard takes more than 10 seconds to load after login.",
            "expected_output": "As a logged-in user, I want the dashboard to load quickly so that I can start working without delay.",
        },
        {
            "bug_id": "BUG-003",
            "description": "Users cannot reset their password because the reset email never arrives.",
            "expected_output": "As a user, I want to receive a password reset email so that I can regain access to my account.",
        },
        {
            "bug_id": "BUG-004",
            "description": "The checkout form allows submission without a shipping address.",
            "expected_output": "As a shopper, I want the checkout form to require a shipping address so that my order can be delivered.",
        },
        {
            "bug_id": "BUG-005",
            "description": "The search field returns no results even for valid product names.",
            "expected_output": "As a shopper, I want search to return relevant products so that I can find what I need.",
        },
        {
            "bug_id": "BUG-006",
            "description": "The app crashes when the user opens the notifications screen.",
            "expected_output": "As a user, I want the notifications screen to open reliably so that I can review alerts without crashes.",
        },
        {
            "bug_id": "BUG-007",
            "description": "Users can create duplicate orders by clicking the submit button twice.",
            "expected_output": "As a user, I want duplicate order submissions to be prevented so that I do not get charged twice.",
        },
        {
            "bug_id": "BUG-008",
            "description": "The profile picture upload fails silently for large images.",
            "expected_output": "As a user, I want image upload validation and clear feedback so that I can update my profile picture successfully.",
        },
        {
            "bug_id": "BUG-009",
            "description": "The reports page shows outdated data after applying filters.",
            "expected_output": "As an analyst, I want filtered reports to refresh correctly so that I can see current data.",
        },
        {
            "bug_id": "BUG-010",
            "description": "The settings page loses changes when the user navigates away too quickly.",
            "expected_output": "As a user, I want settings changes to be saved reliably so that my preferences persist.",
        },
        {
            "bug_id": "BUG-011",
            "description": "The payment gateway rejects valid cards without an error message.",
            "expected_output": "As a customer, I want clear payment failure messages so that I can correct my card details.",
        },
        {
            "bug_id": "BUG-012",
            "description": "The product page does not display the final price after discounts.",
            "expected_output": "As a shopper, I want to see the final discounted price so that I can make informed purchase decisions.",
        },
        {
            "bug_id": "BUG-013",
            "description": "The admin panel allows deleting users without confirmation.",
            "expected_output": "As an admin, I want a confirmation step before deleting users so that I avoid accidental removals.",
        },
        {
            "bug_id": "BUG-014",
            "description": "The app freezes when switching language from English to Portuguese.",
            "expected_output": "As a multilingual user, I want language switching to work smoothly so that I can use the app in my preferred language.",
        },
        {
            "bug_id": "BUG-015",
            "description": "The cart icon does not update after adding items.",
            "expected_output": "As a shopper, I want the cart icon to reflect added items immediately so that I know my cart status.",
        },
        {
            "bug_id": "BUG-016",
            "description": "The export button downloads an empty CSV file.",
            "expected_output": "As a user, I want CSV export to include the selected records so that I can use the data externally.",
        },
        {
            "bug_id": "BUG-017",
            "description": "The app logs the user out unexpectedly after 5 minutes.",
            "expected_output": "As a user, I want my session to remain active for a reasonable time so that I do not lose work unexpectedly.",
        },
        {
            "bug_id": "BUG-018",
            "description": "The map screen shows the wrong location marker.",
            "expected_output": "As a user, I want the map to show the correct location so that I can navigate accurately.",
        },
        {
            "bug_id": "BUG-019",
            "description": "The comment form accepts empty submissions.",
            "expected_output": "As a user, I want comment validation to prevent empty submissions so that content quality is maintained.",
        },
        {
            "bug_id": "BUG-020",
            "description": "The invoice PDF is generated without the company logo.",
            "expected_output": "As an accountant, I want invoices to include the company logo so that documents look professional.",
        },
        {
            "bug_id": "BUG-021",
            "description": "The app sends duplicate push notifications for the same event.",
            "expected_output": "As a user, I want each event to trigger only one notification so that I do not receive duplicates.",
        },
    ]

    if len(dataset) < 20:
        raise ValueError("Dataset must contain at least 20 examples.")

    for item in dataset:
        if not all(key in item for key in ("bug_id", "description", "expected_output")):
            raise ValueError(f"Invalid dataset item: {item}")

    return dataset


def get_dataset() -> Dict[str, Any]:
    return {"examples": load_dataset()}
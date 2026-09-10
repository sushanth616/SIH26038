def build_report(prediction):
    idx=prediction["severity_index"]
    levels=[
        ("Routine","No DR pattern detected in this prototype screening. Continue routine eye care."),
        ("Low","Consider non-urgent ophthalmic review and routine follow-up."),
        ("Medium","Ophthalmic review is recommended."),
        ("High","Prompt ophthalmic assessment is recommended."),
        ("Urgent","Urgent specialist assessment is recommended.")
    ]
    priority,recommendation=levels[idx]
    return {
        "severity":prediction["label"],
        "referral_priority":priority,
        "recommendation":recommendation,
        "human_review":True
    }

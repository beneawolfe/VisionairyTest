"""
Critieria for flagging things in provided text files; these aren't true clinical guidelines, only use is for learing project.
Critieria are put in a seperate file so that rules can be easily modified without changing core logic & customed per practice.
"""

CRITERIA = {
    "visual_field_test": (
        "Patient is a glaucoma suspect or has glaucoma (e.g., elevated IOP, "
        "enlarged or asymmetric cup-to-disc ratio, family history) AND there is "
        "no visual field test on file in the last 12 months."
    ),
    "slt": (
        "Selective laser trabeculoplasty. Patient has open-angle glaucoma with IOP "
        "above target despite topical medications, OR has poor adherence to or "
        "side effects from drops, AND SLT is not already scheduled."
    ),
    "punctal_occlusion": (
        "Patient has aqueous-deficient dry eye with persistent symptoms despite "
        "artificial tears (low Schirmer and/or staining), AND punctal plugs are "
        "not already placed or planned."
    ),
    "toric_iol": (
        "Patient is planned for cataract surgery AND has regular corneal "
        "astigmatism of roughly 1.0 diopter or more, AND a toric IOL has not "
        "already been discussed or chosen."
    ),
}


def criteria_as_text() -> str:
    """Format the criteria for inclusion in the prompt."""
    return "\n".join(f"- {name}: {rule}" for name, rule in CRITERIA.items())
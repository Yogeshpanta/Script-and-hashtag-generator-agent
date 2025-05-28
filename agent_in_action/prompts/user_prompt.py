from agent_in_action.schemas.structure_gen import UserInput


class USERPROMPT:
    input_data = UserInput(
        campaign_type="social media engagement",
        product=["shoes", "sandals", "boots"],  # Must provide list
        rough_theme="Gen Z targeted video",
    )

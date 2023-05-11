from reasoning import (
    deductive_template,
    inductive_template,
    abductive_template,
    analogical_template,
    cause_effect_template,
    conditional_template,
    counterfactual_template,
    temporal_template,
    spatial_template,
    probabilistic_template,
    moral_template,
    means_end_template
)

prompt_infos = [
    {
        "name": "deductive",
        "description": "useful when drawing certain conclusions from true premises \
            based on general rules, ensuring valid and reliable outcomes in structured \
                situations.",
        "prompt_template": deductive_template
    },
    {
        "name": "inductive",
        "description": "useful when deriving probable generalizations from limited \
            observations or data, enabling predictions and informed decision-making.",
        "prompt_template": inductive_template
    },
    {
        "name": "abductive",
        "description": "useful when generating plausible hypotheses or explanations \
            from limited or incomplete information, prioritizing educated guesses in \
                uncertain situations.",
        "prompt_template": abductive_template
    },
    {
        "name": "analogical",
        "description": "useful when encountering unfamiliar situations or problems, \
            enabling the application of knowledge and patterns from known scenarios to \
                facilitate understanding and decision-making.",
        "prompt_template": analogical_template
    },
    {
        "name": "cause_effect",
        "description": "useful when determining causal relationships between events, \
            enabling predictions and decision-making in complex situations.",
        "prompt_template": cause_effect_template
    },
    {
        "name": "conditional",
        "description": "useful when establishing relationships between premises and \
            conclusions, enabling precise decision-making, and deducing outcomes based \
                on specific conditions or criteria.",
        "prompt_template": conditional_template
    },
    {
        "name": "counterfactual",
        "description": "useful when analyzing potential outcomes, evaluating causality,\
            and learning from past experiences by exploring alternative scenarios.",
        "prompt_template": counterfactual_template
    },
    {
        "name": "temporal",
        "description": "useful when analyzing time-based relationships, sequencing \
            events, and determining durations for effective planning, scheduling, and \
                problem-solving across multiple domains.",
        "prompt_template": temporal_template
    },
    {
        "name": "spatial",
        "description": "useful when visualizing, analyzing, and manipulating spatial \
            relationships or objects to solve problems in fields like mathematics, \
                engineering, architecture, and navigation.",
        "prompt_template": spatial_template
    },
    {
        "name": "probabilistic",
        "description": "useful when facing uncertain situations with multiple \
            outcomes, requiring informed decision-making based on likelihoods and \
                risk assessment.",
        "prompt_template": probabilistic_template
    },
    {
        "name": "moral",
        "description": "useful when navigating complex ethical dilemmas, balancing \
            personal values and societal norms, and making decisions that impact \
                others' well-being.",
        "prompt_template": moral_template
    },
    {
        "name": "means_end",
        "description": "useful when tackling complex problems requiring systematic, \
            goal-oriented approaches to identify efficient subgoals and logical steps",
        "prompt_template": means_end_template
    }
]

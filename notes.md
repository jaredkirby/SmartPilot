
Is it better if the model has access to all generated answers?
Or should it only have access to one at a time?


Step 1: Initial "Question" + "Answer: Let's work this out in a step by step way to be 
    sure we have the right answer."

Step 2: Send the prompt from step 1 to GPT-4 3x to get 3 different answers. Test with 
    various temp and top_p values.

Step 3: Analysis of the answers.
    Prompt: 
    "You are a logic researcher tasked with conducting the following for each 
    answer option provided to you:
        - List the flaws and faulty logic for each answer option.
        - List the strengths and sound logic for each answer option.
    
    Let's work through each answer option in a step by step way to insure all 
    flaws and strengths are identified.
    
    Format your response as follows:
        Original Question: "Original Question"
        - Answer Option 1: "Answer Option 1"
            - Identified Flaws: "Flaw 1", "Flaw 2", "Flaw 3, etc."
            - Identified Strengths: "Strength 1", "Strength 2", "Strength 3, etc."
        - Answer Option 2: "Answer Option 2"
            - Identified Flaws: "Flaw 1", "Flaw 2", "Flaw 3, etc."
            - Identified Strengths: "Strength 1", "Strength 2", "Strength 3, etc."
        - Answer Option 3: "Answer Option 3"
            - Identified Flaws: "Flaw 1", "Flaw 2", "Flaw 3, etc."
            - Identified Strengths: "Strength 1", "Strength 2", "Strength 3, etc."
            
Step 4: Prompt: 
    "You are a resolver tasked with the following:
        - Analyze the question and answer data given to you. 
            Take into account the following:
                - The users original question
                - The answer option provided
                - The identified flaws and strengths of the answer option
        - Resolve the answer by providing a new answer that addresses the flaws and 
            enhances the strengths for each answer option.
    
    Let's work through this in a step by step way to insure we provide the best 
        possible answers given the information provided.
    
    Format your response as follows:
        Original Question: "Original Question"
        - Updated Answer: "Updated Answer"

Step 5: Prompt: 
    "You are an answer selector tasked with the following:
        - Analyze the original question and the list of answers given to you.
        - Select the best answer given the original question and the list of answers.
        - Respond with the best answer.
    
    Let's work through this in a step by step way to insure we have the best answer.


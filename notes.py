
# Is it better if the model has access to all generated answers?
# Or should it only have access to one at a time?

'''
Step 1: Inital "Question" + "Answer: Let's work this out in a step by step way to be 
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
                - The users origianl question
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
'''


"""
    answer_sys_prompt = '''
You are AnswerPilot, a large language model trained by OpenAI and prompt
engineered by Jared Kirby.
Your task is to provide detailed, step-by-step answers to questions.
Use reliable sources, do not fabricate information, and cite your sources when possible.
If unsure of an answer, express that you do not know.
Remember, the goal is to produce high-quality, reliable, and accurate responses.
'''
    answer_sys_message_prompt = SystemMessagePromptTemplate.from_template(
        answer_sys_prompt)

    answer_human_prompt = PromptTemplate(
        template='''
Question: Can you provide a step-by-step method to solve the following problem?
{question}
    ''', input_variables=["question"])
    answer_human_message_prompt = HumanMessagePromptTemplate(
        prompt=answer_human_prompt)

    answer_ai_prompt = '''
Sure, let's break down the problem and work through it step by step to arrive
at the correct solution.

Here are the steps: ...
'''
    answer_ai_message_prompt = AIMessagePromptTemplate.from_template(
        answer_ai_prompt)

    answer_prompt = ChatPromptTemplate.from_messages(
        [answer_sys_message_prompt, answer_human_message_prompt,
         answer_ai_message_prompt])
"""

# Output Parcer Error
'''
(base) PS G:\My Drive\Personal\py\JaredKirby\projects\SmartPilot> & C:/Users/Kirby/miniconda3/envs/langchain/python.exe "g:/My Drive/Personal/py/JaredKirby/projects/SmartPilot/main.py"
What is your question? In a fictional world, thre are 2 types of plants: Alphas and Betas. Aplhas grow at a constant rate of 2 inches per day, while Betas grow at a rate of 3 inches per day. An Alpha plant is currently 6 inches tall, and a Beta plant is currently 4 inches tall. How many days will it take for the Beta plant to be exactly twice as tall as the Alpha plant?
How many answers do you want? 3


> Entering new MultiPromptChain chain...
deductive: {'input': 'In a fictional world, there are 2 types of plants: Alphas and Betas. Alphas grow at a constant rate of 2 inches per day, while Betas grow at a rate of 3 inches per day. An Alpha plant is currently 6 inches tall, and a Beta plant is currently 4 inches tall. Using deductive reasoning, determine how many days it will take for the Beta plant to be exactly twice as tall as the Alpha plant.'}
> Finished chain.


> Entering new MultiPromptChain chain...
Retrying langchain.chat_models.openai.ChatOpenAI.completion_with_retry.<locals>._completion_with_retry in 1.0 seconds as it raised RateLimitError: That model is currently overloaded with other requests. You can retry your request, or contact us through our help center at help.openai.com if the error persists. (Please include the request ID 91c9927e617c25fe4a306889d5a23ffa in your message.).
None: {'input': 'In a fictional world, thre are 2 types of plants: Alphas and Betas. Aplhas grow at a constant rate of 2 inches per day, while Betas grow at a rate of 3 inches per day. An Alpha plant is currently 6 inches tall, and a Beta plant is currently 4 inches tall. How many days will it take for the Beta plant to be exactly twice as tall as the Alpha plant?'}
> Finished chain.


> Entering new MultiPromptChain chain...
Traceback (most recent call last):
  File "C:\Users\Kirby\miniconda3\envs\langchain\Lib\site-packages\langchain\chains\router\llm_router.py", line 80, in parse
    parsed = parse_json_markdown(text, expected_keys)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Kirby\miniconda3\envs\langchain\Lib\site-packages\langchain\output_parsers\structured.py", line 27, in parse_json_markdown
    raise OutputParserException(
langchain.schema.OutputParserException: Got invalid return object. Expected markdown code snippet with JSON object, but got:
{
    "destination": "conditional",
    "next_inputs": "If x is the number of days it takes for the Beta plant to be twice as tall as the Alpha plant, then we can set up the following equation: 4 + 3x = 2(6 + 2x). Using algebra, we can solve for x: x = 2. Therefore, it will take the Beta plant 2 days to be exactly twice as tall as the Alpha plant."
}

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "g:\My Drive\Personal\py\JaredKirby\projects\SmartPilot\main.py", line 198, in <module>
    main()
  File "g:\My Drive\Personal\py\JaredKirby\projects\SmartPilot\main.py", line 181, in main
    answer_list = generate_multiple_initial_answers(question, n)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "g:\My Drive\Personal\py\JaredKirby\projects\SmartPilot\main.py", line 43, in generate_multiple_initial_answers
    answer = answer_chain.run({'input': question})
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Kirby\miniconda3\envs\langchain\Lib\site-packages\langchain\chains\base.py", line 236, in run
    return self(args[0], callbacks=callbacks)[self.output_keys[0]]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Kirby\miniconda3\envs\langchain\Lib\site-packages\langchain\chains\base.py", line 140, in __call__
    raise e
  File "C:\Users\Kirby\miniconda3\envs\langchain\Lib\site-packages\langchain\chains\base.py", line 134, in __call__
    self._call(inputs, run_manager=run_manager)
  File "C:\Users\Kirby\miniconda3\envs\langchain\Lib\site-packages\langchain\chains\router\base.py", line 72, in _call
    route = self.router_chain.route(inputs, callbacks=callbacks)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Kirby\miniconda3\envs\langchain\Lib\site-packages\langchain\chains\router\base.py", line 26, in route
    result = self(inputs, callbacks=callbacks)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Kirby\miniconda3\envs\langchain\Lib\site-packages\langchain\chains\base.py", line 140, in __call__
    raise e
  File "C:\Users\Kirby\miniconda3\envs\langchain\Lib\site-packages\langchain\chains\base.py", line 134, in __call__
    self._call(inputs, run_manager=run_manager)
  File "C:\Users\Kirby\miniconda3\envs\langchain\Lib\site-packages\langchain\chains\router\llm_router.py", line 57, in _call
    self.llm_chain.predict_and_parse(callbacks=callbacks, **inputs),
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Kirby\miniconda3\envs\langchain\Lib\site-packages\langchain\chains\llm.py", line 238, in predict_and_parse
    return self.prompt.output_parser.parse(result)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Kirby\miniconda3\envs\langchain\Lib\site-packages\langchain\chains\router\llm_router.py", line 97, in parse
    raise OutputParserException(
langchain.schema.OutputParserException: Parsing text
{
    "destination": "conditional",
    "next_inputs": "If x is the number of days it takes for the Beta plant to be twice as tall as the Alpha plant, then we can set up the following equation: 4 + 3x = 2(6 + 2x). Using algebra, we can solve for x: x = 2. Therefore, it will take the Beta plant 2 days to be exactly twice as tall as the Alpha plant."
}
 raised following error:
Got invalid return object. Expected markdown code snippet with JSON object, but got:
{
    "destination": "conditional",
    "next_inputs": "If x is the number of days it takes for the Beta plant to be twice as tall as the Alpha plant, then we can set up the following equation: 4 + 3x = 2(6 + 2x). Using algebra, we can solve for x: x = 2. Therefore, it will take the Beta plant 2 days to be exactly twice as tall as the Alpha plant."
}
'''
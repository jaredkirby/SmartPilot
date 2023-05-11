from secrets import OPENAI_API_KEY

api_key = OPENAI_API_KEY


def get_llm_answer(api_key, question):
    from langchain.chains.router import MultiPromptChain
    from langchain.llms import OpenAI
    from infos import prompt_infos

    llm = OpenAI(openai_api_key=api_key)
    chain = MultiPromptChain.from_prompts(
        llm=llm, prompt_infos=prompt_infos, verbose=True)

    answer = chain.run(question)
    return answer

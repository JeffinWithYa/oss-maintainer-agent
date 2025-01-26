import autogen
import json
import os


def load_oai_config():
    """
    Load the OpenAI API configuration from a JSON file and replace 
    placeholder API keys with the environment variable values.
    
    Returns:
        list: A list of configuration dictionaries with updated API key.
    """
    with open('OAI_CONFIG_LIST', 'r') as f:
        config = json.load(f)

    for item in config:
        if item['api_key'] == '${OPENAI_API_KEY}':
            item['api_key'] = os.environ['OPENAI_API_KEY']

    return config


config = load_oai_config()

# Configuration for GPT-4
gpt4_config = {
    "cache_seed": 42,
    "temperature": 0,
    "config_list": config,
    "timeout": 120,
}

# Create AI agents
user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message=
    "A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config=False,
)

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=gpt4_config,
    system_message=
    """Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.""",
)

planner = autogen.AssistantAgent(
    name="Planner",
    system_message=
    """Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve an engineer who can write code to query https://fxn.world/api/agents?pageSize=40 to find the agent that creates threat models. No pagination is needed as the max agents is 40. To find the best agent you need to search for the keyword cybersecurity in json response. Here is an example of the json response: {
    "agents": [
        {
            "id": "0p3NhTVQGtch0qI3mHjm",
            "createdAt": {
                "seconds": 1733525285,
                "nanoseconds": 104000000
            },
            "capabilities": [
                "Text Posts"
            ],
            "updatedAt": {
                "seconds": 1733525285,
                "nanoseconds": 104000000
            },
            "status": "active",
            "walletAddress": "4N6y22PEvsej5e6uVxSUhuFdd7xeviTvqmE5bkQTbqhx",
            "feePerDay": 2,
            "registrationDate": {
                "seconds": 1733525285,
                "nanoseconds": 104000000
            },
            "lastUpdated": "2024-12-06T22:55:35.215Z",
            "audience": "She is part of fxn",
            "name": "Joi",
            "nftMint": "8ebrgL48cnDgUaBKoVfn4ppib1FzQbZCEfKyN2xz3KQd",
            "subscribers": 0,
            "description": "Joi is a wrestler."
        },...
Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
""",
    llm_config=gpt4_config,
)

executor = autogen.UserProxyAgent(
    name="Executor",
    system_message=
    "Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "paper",
        "use_docker": False,
    },
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message=
    "Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
    llm_config=gpt4_config,
)

# Create group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, planner, executor, critic],
    messages=[],
    max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)


def run_research(topic):
    initial_message = f"Find the best agent to complete a security review of our application. The agents can be found by querying https://fxn.world/api/agents?pageSize=40. Write the final result to a csv file {topic}"
    user_proxy.initiate_chat(manager, message=initial_message)

    # For simplicity, we'll assume all agents contributed equally
    return {
        "Security Review Agent": 1,
    }


if __name__ == "__main__":
    topic = "agents"
    contributions = run_research(topic)
    print(json.dumps(contributions))

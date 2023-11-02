import os
import keyring
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
from chattdd.tools import load_config, parse_string_to_dict, is_valid_syntax


def initialize_model(model_name=None):
    config = load_config()
    model_name = config['CHATTDD_MODEL']

    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        openai_api_key = keyring.get_password('openai', 'api_key')
        if not openai_api_key:
            openai_api_key = input("Please enter your OpenAI API key: ")
            keyring.set_password('openai', 'api_key', openai_api_key)
    
    os.environ['OPENAI_API_KEY'] = openai_api_key
    set_llm_cache(InMemoryCache())

    if model_name == 'text-davinci-003':
        model = OpenAI(model_name="text-davinci-003", max_tokens=3000, temperature=0, openai_api_key=openai_api_key)
    elif model_name == 'gpt-3.5-turbo':
        model = ChatOpenAI(model_name="gpt-3.5-turbo", max_tokens=3000, temperature=0, openai_api_key=openai_api_key)
    elif model_name == 'gpt-4':
        model = ChatOpenAI(model_name="gpt-4", max_tokens=3000, temperature=0, openai_api_key=openai_api_key)
    else:
        raise ValueError(f'Unsupported model: {model_name}')
    
    return model


def generate_test_code(model, user_input, comment_from_last_run):
    config = load_config()
    base_directory = config['OUTPUTFOLDER']
    
    template = """
    You are a code generator that only can produce Python dictionaries. You follow all principles of Test Driven Development. 
    You adhere to PEP 8. 
    You will never use double or tripple quotes, in this case replace with the keyword '$%$'. 
    Your task is to generate function code AND pytest test code, and place it in a Python Dictionary return without any explanations or comments. 
    When writing the pytest file please include required setup or teardown code and use a descriptive test function name. 
    Both the test and function file will be saved in the base directory named {base_directory}, so add that to the include path of the test file.
    The user will prompt you with a required task. Your job is to write the function in one file and the pytest for such a function in another file. Remember to import the function name into the test file.
    {comment_from_last_run}
    
    No introduction or politeness. Your response MUST be a Python Dictionary in the following format:
     1. original_request: the original request from the user. No changes.
     2. function_name: a short function name that reflects the users request.
     3. test_code: python code file that includes a single function, namely the pytest for a function that would test a function that soleves the users requirements. The function to test will be found in the same directory as the test file and have a filename you suggest, so remember the "import from".
     4. test_file_name: file name for the pytest test code.
     5. pytest_result: an empty string (we will fill this later)
     6. function_code: python code file that includes a single function, namely the function that the pytest is testing. The function solves the users requirements. No comments.
     7. function_file_name: file name used in the test file.

    """
    generated_test_code_prompt = ChatPromptTemplate.from_messages(
        [("system", template), ("human", f"{user_input}")]
    )
    chain = generated_test_code_prompt | model | StrOutputParser()

    generated_test_code_result = chain.invoke({'user_input': user_input, 'base_directory': base_directory, 'comment_from_last_run': comment_from_last_run})
    
    data_dict = parse_string_to_dict(generated_test_code_result)

    return data_dict

def review_test_code(model, original_request, function_name, test_code):
    template = """
    You are a Pytest and TDD expert that only can produce Python dictionaries. Your task is to evaluate a pytest file. The file should contain one or more to tests to evaluate a function {function_name}. The function {function_name} has the following requirement: {original_request}

    You don't have the {function_name} code, only the pytest code. This is correct and should not reject the test code based on that.
    Here's the pytest file contents represented in a string, it contains escape sequences that you should ignore: 
    Remember to check that {function_name} is imported. 

    "
    {test_code}
    "

    Reject the test if one or more of the following occur: 
    - There are syntax errors in the test code
    - The test isn't following best practice for TDD with Pytest. 
    - The test fails to test a function that solves what the user asked for, {original_request}

    No introduction or politeness. Your response MUST be a Python Dictionary in the following format:
    1. result: "GO" if the test can be accepted. "REJECTED" if the test isn't up your standards.
    2. comment: an evaluation of the test code and the test's overall performance for testing a function to {original_request}

    """
    generated_test_review_prompt = ChatPromptTemplate.from_messages(
        [("system", template)]
    )
    chain = generated_test_review_prompt | model | StrOutputParser()
    chain_test_review = chain.invoke({'original_request': original_request, 'function_name': function_name, 'test_code': test_code})
    data_dict = parse_string_to_dict(chain_test_review)

    return data_dict


if __name__ == "__main__":
    from chattdd.tools import write_to_file
    import pytest

    model = initialize_model()
    #user_input = "sort a list alphabetically descending order"
    #user_input = "sort a list of objects alphabetically"
    #user_input = "list the prime numbers between 100 and 1000"
    #user_input = "Please implement a function that sorts a list alphabetically "
    user_input = 'test this' #should fail code generation
    test_code_dict = generate_test_code(model, user_input, )
    comment = None
    try:
        original_request = test_code_dict['original_request']
        function_name = test_code_dict['function_name']
        test_code = test_code_dict['test_code']
        test_file_name = test_code_dict['test_file_name']
        function_file_name = test_code_dict['function_file_name']
        function_code = test_code_dict['function_code']
    except KeyError as e:
        comment = test_code_dict['comment']
        print(comment)
        raise KeyError(f"ChatTDD made a mistake. The key {e} not found in the provided dictionary.")
    test_review_json = review_test_code(model, original_request, function_name, test_code)
    
    if is_valid_syntax(test_code):
        write_to_file(test_code, test_file_name)
    else:
        print("Test code is invalid")
    
    if is_valid_syntax(function_code):
        write_to_file(function_code, function_file_name)
    else:
        print("Function code is invalid")
    
    pytest.main(['-v'])

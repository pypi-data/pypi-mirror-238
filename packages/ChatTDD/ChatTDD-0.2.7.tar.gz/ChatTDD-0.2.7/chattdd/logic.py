import pytest
from chattdd.core import initialize_model, generate_test_code, review_test_code
from chattdd.tools import update_config, load_config, write_to_file

def set_output_folder(outputfolder):
    update_config('OUTPUTFOLDER', outputfolder)

def set_model(model_name):
    update_config('CHATTDD_MODEL', model_name)

def generate_and_save_logic(user_requirement, save_function_code=True, iterations=3):
    config = load_config()
    model_name = config['CHATTDD_MODEL']
    model = initialize_model(model_name)
    
    comment = ''

    for i in range(iterations):
        generated_test_code_output = generate_test_code(model, user_requirement, comment)

        test_code = generated_test_code_output.get('test_code')
        if not test_code:
            return generated_test_code_output.get('comment', 'No comment available'), None

        review_output = review_test_code(
            model=model,
            original_request=generated_test_code_output['original_request'],
            function_name=generated_test_code_output['function_name'],
            test_code=test_code
        )

        review_result = review_output.get('result')
        comment = review_output.get('comment', 'No comment available')

        if review_result == "GO":
            break

    if review_result == "GO":
        write_to_file(test_code, generated_test_code_output['test_file_name'])

        if save_function_code:
            write_to_file(generated_test_code_output['function_code'], generated_test_code_output['function_file_name'])
        
        pytest.main(['-v'])
        return comment, generated_test_code_output

    return comment, None

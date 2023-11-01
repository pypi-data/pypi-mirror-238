import unittest
import os
import json
import pandas as pd
from scalexi.dataset_generation.prompt_completion import (
    format_prompt_completion,
    df_to_json,
    list_to_csv,
    df_to_csv,
    parse_json_formatted,
    generate_prompt_completions,
)

class TestYourMethods(unittest.TestCase):
    # Define a setup method to prepare any necessary data or configurations
    def setUp(self):
        # Create a temporary directory for test files
        self.temp_dir = 'test_temp_dir'
        os.makedirs(self.temp_dir, exist_ok=True)

    # Define a teardown method to clean up any resources created during testing
    def tearDown(self):
        # Remove the temporary directory and its contents
        for file_name in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.temp_dir)

    def test_format_prompt_completion(self):
        # Test the format_prompt_completion function
        prompt = "Input Prompt"
        completion = "Output Completion"
        formatted = format_prompt_completion(prompt, completion)
        expected = {"prompt": "Input Prompt\n\n###\n\n", "completion": "Output CompletionEND"}
        self.assertEqual(formatted, expected)

    def test_df_to_json(self):
        # Test the df_to_json function
        data = [{"A": 1, "B": 2}, {"A": 3, "B": 4}]
        df = pd.DataFrame(data)
        output_file = os.path.join(self.temp_dir, "test_df_to_json.json")
        df_to_json(df, output_file)
        self.assertTrue(os.path.isfile(output_file))

    def test_list_to_csv(self):
        # Test the list_to_csv function
        data_list = [{"Name": "Alice", "Age": 30}, {"Name": "Bob", "Age": 25}]
        output_file = os.path.join(self.temp_dir, "test_list_to_csv.csv")
        list_to_csv(data_list, output_file)
        self.assertTrue(os.path.isfile(output_file))

    def test_df_to_csv(self):
        # Test the df_to_csv function
        data = [{"A": 1, "B": 2}, {"A": 3, "B": 4}]
        df = pd.DataFrame(data)
        output_file = os.path.join(self.temp_dir, "test_df_to_csv.csv")
        df_to_csv(df, output_file)
        self.assertTrue(os.path.isfile(output_file))

    def test_parse_json_formatted(self):
        # Test the parse_json_formatted function
        json_string = '[{"prompt": "p1", "completion": "c1"}, {"prompt": "p2", "completion": "c2"}]'
        output_file = os.path.join(self.temp_dir, "test_parse_json_formatted.json")
        parse_json_formatted(json_string, output_file)
        self.assertTrue(os.path.isfile(output_file))

    def test_generate_prompt_completions_from_text(self):
        # Test the generate_prompt_completions_from_text function
        context_text = "Prince Sultan University, commonly referred to as PSU, is a private university in Riyadh, Saudi Arabia. It was founded in 1999 by the Al-Riyadh Philanthropic Society for Science and licensed by the Ministry of Higher Education."
        output_csv = os.path.join(self.temp_dir, "test_generate_prompt_completions_from_text.csv")
        user_prompt_init='''In light of the given context, craft precisely 3 pairs of prompts and their corresponding completions, following these guidelines for the context below:
                                    Each prompt should be a short question about the context provided from perspective of a student, faculty member or staff from Prince Sultan University asking the chatbot. 
                                    Example 1: What is PSU address?
                                    Example 2: What are the research labs at PSU?
                                    Ensure that the prompt is inherently correctly answerable, but is constructed to provoke an in-depth response.
                                    Each completion must be meticulously developed offering a sufficient explanation and ample arguments to justify the given response.
                                    All responses should be formatted within a JSON ARRAY structure.
                                    Each corresponding response should be meticulously crafted that offers a detailed explanation along with a robust argument to substantiate the response.
                                    Each individual JSON record should encapsulate one distinct prompt and its corresponding in-depth completion.

                                    The returned result must be formatted as JSON ARRAY structure like 
                                    [
                                        {"prompt": "question1", "completion': "answer1"},
                                        {"prompt": "question2", "completion': "answer2"}
                                    ]
                                    Context: 
                                    '''
        prompt_completions = generate_prompt_completions(
            context_text,
            output_csv,
            user_prompt_init,
            openai_key=os.environ.get("OPENAI_API_KEY")
        )
        #self.assertTrue(os.path.isfile(output_csv))
        self.assertIsInstance(prompt_completions, list)

if __name__ == '__main__':
    unittest.main()

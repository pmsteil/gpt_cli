import openai

OPENAI_API_KEY="YOUR OPENAI API KEY"
OPENAI_MODEL="text-davinci-003"
OPENAI_MAX_TOKENS=1024
OPENAI_TEMPERATURE=0.5



class OpenAIAPI:
    def __init__(self, api_key, model_engine):
        openai.api_key = api_key
        self.model_engine = model_engine
        self.response = ""
        
    def generate_response(self, prompt):
        """
        Generates a response for the given prompt
        """
        completion = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt,
            max_tokens=OPENAI_MAX_TOKENS,
            n=1,
            temperature=OPENAI_TEMPERATURE,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.2,
            stop=["100."]
        )
        self.response = completion.choices[0].text
        return self.response

    def save_response(self, file_name):
        """
        Saves the current response to a file
        """
        if self.response == "":
            print("No previous response to save.")
        else:
            with open(file_name, "w") as f:
                f.write(self.response)
                f.close()
            print(f"Response saved to {file_name}")
            
    def handle_exception(self, e):
        """
        Handles any exceptions that occur
        """
        if isinstance(e, openai.exceptions.OpenAiError):
            print(f"Error: {e}")
        elif isinstance(e, IndexError):
            print("Error: No response generated")
        else:
            print(f"Error: {e}")
            
if __name__ == "__main__":
    api = OpenAIAPI( OPENAI_API_KEY, OPENAI_MODEL)
    while True:
        prompt = input("Search: ")
        if prompt.strip().lower() == "exit":
            break
        try:
            if prompt.strip().lower() != "save":
                response = api.generate_response(prompt)
                print(response)
            else:
                file_name = input("Enter a file name: ")
                api.save_response(file_name)
        except Exception as e:
            api.handle_exception(e)


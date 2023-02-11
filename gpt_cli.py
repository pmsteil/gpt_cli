import openai
import os
import dotenv


#
# create a .env file in the same directory as this file and add your API key
# example .env file:
# OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# OPENAI_MODEL="text-davinci-003"
# OPENAI_MAX_TOKENS=1024
# OPENAI_TEMPERATURE=0.5
#

# load environment variables from .env file
dotenv.load_dotenv()

# retrieve environment variables and set defaults
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL=os.environ.get("OPENAI_MODEL", "text-davinci-003")
OPENAI_MAX_TOKENS=int(os.environ.get("OPENAI_MAX_TOKENS", 1024))
OPENAI_TEMPERATURE=float(os.environ.get("OPENAI_TEMPERATURE", 0.5))





class OpenAIAPI:
    def __init__(self, api_key, model_engine):
        openai.api_key = api_key
        self.model_engine = model_engine
        self.response = ""
        self.prompt=""
        self.history=""
        self.latest_save_filename = "prompt_response.txt"




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
        self.prompt = prompt
        self.response = completion.choices[0].text
        return self.response.strip()




    def save_response(self, file_name):
        """
        Saves the current prompt and response to a file
        """
        #if file_name is not blank
        if file_name.strip() != "":
            self.latest_save_filename = file_name

        if self.response == "":
            print("No previous response to save.")
        else:
            write_mode = "w" if not os.path.exists(self.latest_save_filename) else "a"

            with open(self.latest_save_filename, write_mode) as f:
                f.write(f"PROMPT: {self.prompt}\n")
                f.write(f"RESPONSE: {self.response}\n\n")
        
        return self.latest_save_filename
            



    def get_latest_save_filename(self):
        """
        Returns the latest save file name
        """
        return self.latest_save_filename





    def handle_exception(self, e):
        """
        Handles any exceptions that occur
        """
        if isinstance(e, openai.error.InvalidRequestError):
            print(f"Error: {e}")
        elif isinstance(e, IndexError):
            print("Error: No response generated")
        else:
            print(f"Error: {e}")




if __name__ == "__main__":
    api = OpenAIAPI( OPENAI_API_KEY, OPENAI_MODEL)
    while True:
        prompt = input("[PROMPT]: ").strip()
        
        # define some internal commands
        if prompt.lower() == "/exit":
            break

        if prompt.lower() == "/save":
            file_name = api.get_latest_save_filename()
            file_name = input( f"Enter a file name to save most recent prompt and response ({file_name}): ")            
            file_name = api.save_response(file_name)
            print( f"Prompt and response saved to: [{file_name}]" )
            continue # skip the rest of the loop
        
        try:
                    
            print("stand by...")
            response = api.generate_response(prompt)
            
            print( "-----------------------------------------------")
            print(response)
            print( "-----------------------------------------------")




        except Exception as e:
            api.handle_exception(e)


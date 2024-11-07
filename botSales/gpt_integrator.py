from openai import OpenAI

import re


client = OpenAI()

class GPT:


    def __init__(self):
        pass


    def get_gpt_answer(self, message: str) -> dict:
        """Method to send question for GPT and get its answer.
            Params:
                message(str): Message to send for GPT
            Return:
                response(dict): Dictionary containing the status of the request and the content
                                of the message returned from GPT. """

        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": f"Hi chat, Please, {message}"
                    }
                ]
            )

            pattern = r'\*\*(.*?)\*\*'
            message =  completion.choices[0].message.content
            matches = re.findall(pattern, response["message"])
            response = {"status": "OK", "message": matches}

        except Exception as error: 
            print(error)
            response =  {"status": "FAILED", "message": f"Could not get response from GPT API. Error -->> {error}"}

        finally:
            return response
        

from openai import OpenAI


client = OpenAI()

class GPT:


    def __init__(self, message):
        self.message = message


    def get_gpt_answer(self):

        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": f"Hi chat, Please, {self.message}"
                    }
                ]
            )

            response = {"status": "OK", "message": completion.choices[0].message.content}

        except Exception as error: 
            print(error)
            response =  {"status": "FAILED", "message": f"Could not get response from GPT API. Error -->> {error}"}

        finally:
            return response

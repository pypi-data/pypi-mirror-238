import time
import openai

class regexai:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_regex_code(self, query, da):
      query1=f"""with reference to this given paragraph- "{da}", Consider below instructons for writing one line regex code for it - (this para is already stored into "da" variable. So,don't use paragraph into your code and use "da" variable instead and write full single line python regex code for the given query - "{query}", store the output into "result" variable.)"""
      response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-03-02"},
                {"role": "user", "content": query1}
            ]
        )
      cod = response["choices"][0]["message"]["content"]
      # Remove unnecessary formatting
      cod = self._clean_code(cod)

      # Execute the code
      try:
          exec(cod)
      except Exception as e:
          print("Unfortunately, I can't solve your query!! Try Again!!", e)
          
      time.sleep(5)
      return result

    def _clean_code(self, code):
        # Implement code cleaning logic here
        # You can adapt your code cleaning logic from the original code
        # (e.g., removing unnecessary comments and formatting)
        code = code.replace("\n#\n\n", '#').replace('#\n', '#').replace('```', '#').replace('\n    ', '\n')
        code = code.split(':', 1)[-1].split("\n#\n\n")[0]
        return code
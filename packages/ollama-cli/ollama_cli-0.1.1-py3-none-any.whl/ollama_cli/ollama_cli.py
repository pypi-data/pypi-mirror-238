import sys
import json
import requests


class OlcRunner():

    host = "http://localhost:8888"  # TODO: get from env
    model = "llama2"  # TODO: get from env

    endpoint_generate = "api/generate"

    def run(self):
        prompt = self._getPrompt()

        if not self._is_ollama_running():
            raise RuntimeError(f"Ollama is not running at expected address {self.host}")

        self._generate_async(prompt)

    def _generate_async(self, prompt: str) -> str:
        request_body = self._get_generate_request_body(prompt, stream=True)
        try:
            result = requests.post(f"{self.host}/{self.endpoint_generate}", data=json.dumps(request_body), stream=True)
            if result.status_code != 200:
                raise RuntimeError(f"Unexpected status code: {result.status_code} - {result.text}")

            for line in result.iter_lines():
                line_str = line.decode('UTF-8')
                line_json = json.loads(line_str)
                response = line_json['response']
                print(response, end="")

        except Exception as ex:
            raise RuntimeError(ex)

    def _generate(self, prompt: str) -> str:
        request_body = self._get_generate_request_body(prompt, stream=False)

        try:
            result = requests.post(f"{self.host}/{self.endpoint_generate}", data=json.dumps(request_body))
            if result.status_code != 200:
                raise RuntimeError(f"Unexpected status code: {result.status_code} - {result.text}")

            as_array = result.text.replace("}\n{", "},\n{")
            result_json: dict = json.loads(f"[{as_array}]")

            response = ""
            for item in result_json:
                response += item['response']

            return response
        except Exception as ex:
            raise RuntimeError(ex)

    def _get_generate_request_body(self, prompt: str, stream: bool = False) -> str:
        return {
            "model": self.model,
            "prompt": prompt,
            "stream": stream
        }

    def _getPrompt(self) -> str:
        if (len(sys.argv) == 1):
            raise AttributeError("No prompt argument was given.")

        return sys.argv[1]

    def _is_ollama_running(self) -> bool:
        try:
            result = requests.get(f"{self.host}/")
            return result.status_code == 200
        except Exception as ex:
            print(ex)
            return False


def run():
    OlcRunner().run()


if __name__ == '__main__':
    OlcRunner().run()

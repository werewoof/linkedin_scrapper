from scraper import Scrapper
from flask import Flask
import json

app = Flask(__name__)

main_scrapper = Scrapper("oliver.po2882@gmail.com", "crackheaD49!") #Scrapper("AQEDAUw0o-sBBYkZAAABjf3LUkYAAAGOIdfWRk0AMW4tiLQ-3n8v5Ya9h_ZyVV4wcOUwqkSgkPcXVGgR6SDFvI16QeJrB5fqyJAzjYPvCsdx2ebz6QG8GraswYijGBixORZ1wyKarwuy6wE9smnZ8aeI")

@app.route("/<name>")
def get_data(name):
    return json.dumps(main_scrapper.run(f"https://www.linkedin.com/in/{name}/"))
    

if __name__ == "__main__":
    #print(main_scrapper.token)
    print("running")
    app.run("0.0.0.0", 3000)
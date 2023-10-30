import argparse
import os

import requests
import git


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Set command process")
    parser.add_argument("project_name", default="fastapi_init", help="Set name project")
    parser.add_argument("version", default="main", help="Set version fastapi init")
    parser.add_argument("--package_key", default=None, help="Add key to install requirement")
    args = parser.parse_args()

    if args.command == "init_project":
        git.repo.Repo.clone_from(
            "git@git.rabiloo.net:tech/base/fastapi-init.git", f"./{args.project_name}",
            branch=args.version
        )
        if args.package_key:
            os.environ['PACKAGE_REGISTRY_TOKEN'] = args.package_key.split('key=')[1]
        os.system(f"pip install -r {args.project_name}/cicd/requirements/requirements.txt")
        os.system(f"pip install -r {args.project_name}/cicd/requirements/requirements-style.txt")
    elif args.command == "get_weather":
        response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Hà Nội&appid=YOUR_API_KEY")
        data = response.json()
        print(data["weather"][0]["main"])


if __name__ == "__main__":
    main()

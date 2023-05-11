import yaml
import argparse
import glob,os
import sys
yaml_files = []
yaml_parsed = []

def get_files(folder):
    searchstring = folder + "/**/*.yaml"
    for file in glob.glob(searchstring):
        yaml_files.append(file)

def parse_yaml(file):
    name = os.path.split(file)[1]
    with open(file) as f:
        parsed_yaml = yaml.safe_load(f)
        yaml_obj = {
                "name": name,
                "yaml": parsed_yaml
                }
        yaml_parsed.append(yaml_obj)

def generate_html(yaml_list):
    html_string = "<html><head><link rel='stylesheet' href='styles.css'><title>Sherlocks QC</title></head><H1>SHERLOCKS</H1>"
    for document in yaml_list:
        print("[+] GENERATING: " + document["name"], file=sys.stderr)
        html_string = html_string + "<div class='sherlock'><h2>" + document["name"] + "</h2>"
        html_string = html_string + "<h3>Scenario</h3>"
        html_string = html_string + "<p>" + document["yaml"]["scenario"] + "</p>"
        html_string = html_string + "<h3>Description</h3>"
        html_string = html_string + "<p>" + document["yaml"]["description"] + "</p>"
        html_string = html_string + "<h3>Questions</h3>"
        for question in document["yaml"]["questions"]:
            html_string = html_string + "<form><label>Q" + str(question["number"]) + ": </label>"
            html_string = html_string + "<label>" + question["title"] + "</label></br>"
            if(question.__contains__("placeholder") and question["placeholder"] is not None):
               html_string = html_string + "<input type='text' class='answer' placeholder='" + question["placeholder"] + "'/><br>"
            else:
               html_string = html_string + "<input type='text' class='answer' /><br>"
            html_string = html_string + "<label> Answer: " + str(question["flag"]) + "</label><br>"
            html_string = html_string + "<button>Submit</button></form>"
        html_string = html_string + "</div>"
    html_string = html_string + "</html>"
    return html_string

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog="YAML to HTML",
            description="Convert HTB yaml files to a HTML page for QC",
            epilog="Author: Blitztide"
            )
    parser.add_argument('folder')
    args = parser.parse_args()
    get_files(args.folder)
    for file in yaml_files:
        parse_yaml(file)
    print(generate_html(yaml_parsed))

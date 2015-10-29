#!/usr/bin/python3
import jinja2
import sys
import os
import json
import getopt
import csv

template_dir = ""
jinja_env = None
dev = False

def load_template(input_file):
  return jinja_env.get_template(input_file)

def load_csv_values(csv_file,csv_params):
  with open(csv_file, newline='') as f:
    reader = csv.DictReader(f,**csv_params)
    data = []
    for row in reader:
      data.append(row)
    return {'fieldnames': reader.fieldnames, 'data': data}

def write_page(output_file,text):
  with open(output_file,'w') as f:
    f.write(text)

def usage():
  print("Usage: python3 cuack.py\n")

def parse_args():
  global dev
  inputFile = ""
  try:
    opts, args = getopt.getopt(sys.argv[1:],"f:h:d",["file=","help","dev"])
  except getopt.GetOptError as err:
    print(err,file=sys.stderr)
    usage()
    sys.exit(2)
  for opt , arg in opts:
    if opt in ("-h","--help"):
      usage()
      sys.exit()
    elif opt in ("-f","--file"):
      inputFile = arg
    elif opt in ("-d","--dev"):
      dev = True
  if inputFile == "":
    inputFile = "pages.json"
  with open(inputFile,"r") as f:
    conf = f.read()
  return json.loads(conf) 

def main(argv):
  global jinja_env
  global template_dir
  global dev
  json_conf = parse_args()
  template_dir = os.path.join(os.path.dirname(__file__),json_conf["template_dir"])
  jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape= True)

  pages = json_conf['pages']
  for page in pages:
    template = load_template(page['template'])
    for csv_conf in page['csv']:
      csv_data = load_csv_values(csv_conf['file_name'],csv_conf['csv_params'])
      page['values'][csv_conf['var_name']] = csv_data
    result= template.render(name=page['name'],dev= dev,**page['values'])
    write_page(json_conf['output_dir']+ "/" + page['name'],result)

if __name__ == "__main__":
  main(sys.argv)
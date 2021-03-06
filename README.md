# Cuack
Static multi-purpouse template renderer made in python :)

## What is Cuack?
I made cuack because I found myself in many situations where I need to generate lots of similar static assests (reports, tables, html, etc.) and end up using other tools or setting up single use environments to achieve my goal. So to accelerate my work I made a somewhat general setup to generate this assets by using templates.

## Requirements
* Python3 (probable Python2 support)
* Jinja2 Python package

##How to install it
Asuming you have Python3 and Jinja2 installed, fork this repo or download it as a zip and unzip it in some folder of your machine and start using it.
```bash
~$ python cuack.py
```
If you have a unix-like enviromnent you could make the script executable
```bash
~$ chmod a+x cuack.py
```
Now you can just run it like
```bash
~$ cuack.py
```
## How it works
The script is simple, it reads paramaters from a JSON file(pages.json) and generate the assets according to them using the [Jinja2](https://github.com/mitsuhiko/jinja2) template engine, so go on and read Jinja's documentation to start generating you templates.

## Structure of the pages.json
Let's start with a very small example

```JSON
{
  "output_dir" :"myawesomewebsite/static/",
  "template_dir" : "templates",
  "pages" :[
    {
      "name": "second_page.html",
      "template": "base.html",
    }
  ]
}
```
The file pages.json can be very simple or very complicated depending on what are you planning to do. 

Basically, you must indicate where your templates are located, this is the "template_dir" value. The "output_dir" value is self explanatory, your generated pages will be put in that directory.(Be careful if you use the same directory as your templates you may overwrite them!).

The "pages" value is a list that indicates the "name" of the generated page and which "template" it uses to do it. "name" and "template" are mandatory attributes for each page. You can also specify arbitrary JSON attributes in each and use it on you templates via "current_page".

There's also another useful feature, when you need to have data available to all templates, instead of adding it on the attribute "values" of each page, you can add an attribute to the main pages.json structure called "global_vars".

```JSON
{
  "output_dir" :"myawesomewebsite/static/",
  "template_dir" : "templates",
  "global_vars" :
  {
    "foo" :"bar",
    "name" : "Joseph"
  },
  "pages" :[
    {
      "name": "second_page.html",
      "template": "base.html",
      "foo": "bar"
    }
  ]
}
```
This attribute is optional and can contain any type of JSON data.

For particular cases like when you need to build an index for a webpage, it can be helpful to have a list of the pages straight out of the pages.json file. You can access it in the `meta` variable from any template file. It has the same structure as the pages.json file.

### Importing data from a CSV file

You can also load data from a comma-separated values file in order to avoid hardcoding the data into the pages.json file.

To do this you must specify some parameters:

```JSON
{
  "output_dir" :"myawesomewebsite/static/",
  "template_dir" : "templates",
  "pages" :[
    {
      "name": "second_page.html",
      "template": "base.html",
      "csv":[
        {
          "file_name": "data.csv",
          "var_name": "table1",
          "csv_params":{}
        }
      ]
    }
  ]
}
```

You can add multiple csv files by appending them to the csv parameter of the page.
* The filename attribute is the path to the csv file relative to the cuack.py script. 
* The var_name attribute is the name of the variable in the template used to to reference the data.
* The csv_params is a dictionary containing settings for loading the csv file. For more info on what parameters are available and how to use them, be sure to check the Python documentation of the csv module [here](https://docs.python.org/3/library/csv.html).

After modifying the pages.json file, you can use the variable specified in var_name in your template. This variable contains 2 attributes:
* fieldnames : A list of the fieldnames in the same order as the csv file
* data: A list of dictionaries(rows), each entry in the dictionary is {fieldname: value}. The rows are in order but the dictionaries are not!.

## Additional options
In case you need or just want to specify a different pages.json file, you could use the --file parameter
```bash
~$ cuack.py --file=myotherpagesfile.json
```

Also, there is a --dev parameter just to save you the hassle of creating a "dev:true" value in every page entry of the pages.json file. You can use the dev variable anywhere in your template, not using the --dev option sets it to False.

## Contributing
If you want to add improvements, fix bugs, add features, document or anything you think will benefit cuack, first fork it for you to work there. After finishing what you have done you can submit a pull-request to the original repository. Please be very descriptive on what your changes are so I can review it quickier.

## Report bugs and issues
Just file an issue here on this repo and I'll take a look at it as soon as I can.

import argparse
import os
import re
import urllib

parser = argparse.ArgumentParser(description='Process url and pattern.')
parser.add_argument('--url', '-u', action="store", dest="url",
    required=True,
    help="The url to the image(s) location without the actual image.")
parser.add_argument('--pattern', '-p', action="store", dest="pattern",
    required=True,
    help="The pattern that generates the possible image names")
parser.add_argument('--start', '-s', action="store", dest="start",
    type=int,
    help="The starting range that will replace '$' with real values")
parser.add_argument('--end', '-e', action="store", dest="end",
    type=int,
    help="The ending range that will replace '$' with real values")
parser.add_argument('--target', '-t', action="store", dest="target_directory",
    default=None, required=False,
    help="The target directory name. Will be created when not exists.")

results = parser.parse_args()
url = results.url
pattern = results.pattern
target_directory = results.target_directory
start = results.start
end = results.end

if start and not end:
  start = None
if end and not start:
  end = None

if target_directory:
  if not os.path.exists(target_directory):
    os.makedirs(target_directory)
  os.chdir(target_directory)

if not url.endswith("/"):
  url += "/"

has_range = start is not None and end is not None
print has_range

if has_range:
  if start > end:
    tmp_end = start
    start = end
    end = tmp_end
  for i in range(start, end):
    current_transformed_value = ""
    bracket_values = re.findall(r'\[(.*?)\]', pattern)
    filename = ""
    for bracket_value in bracket_values:
      if bracket_value == "$":
        current_transformed_value = str(i)
      else:
        current_transformed_value = bracket_value
      filename += current_transformed_value
    current_url = url + filename
    print current_url
    image = urllib.URLopener()
    image.retrieve(current_url, filename)
  else:
    bracket_values = re.findall(r'\[(.*?)\]', pattern)
    filename = ""
    for bracket_value in bracket_values:
      if bracket_value == "$":
        continue
      else:
        filename += bracket_value
    print filename
    print url
    url += filename
    image = urllib.URLopener()
    image.retrieve(url, filename)

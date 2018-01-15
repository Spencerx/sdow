'''
Server web framework.
'''

# import sys
from flask import Flask, jsonify
from sdow.database import Database
from sdow.helpers import InvalidRequest

sqlite_filename = '../sdow.sqlite'

# TODO: figure out how to pass CLI arguments to Flask
# if len(sys.argv) != 2:
#   print '[ERROR] Invalid program usage.'
#   print '[INFO] Usage: server.py <sqlite_file>'
#   sys.exit(1)

# sqlite_file = sys.argv[1]

db = Database(sqlite_filename)

app = Flask(__name__)


@app.errorhandler(InvalidRequest)
def handle_invalid_usage(error):
  response = jsonify(error.to_dict())
  response.status_code = error.status_code
  return response


@app.route('/pages/<page_name>')
def get_page_type(page_name):
  response = {}

  # Look up the page ID
  try:
    page_id = db.fetch_page_id(page_name)
  except ValueError as error:
    page_id = None
    response['type'] = 'not_found'

  if page_id:
    # Determine if the page is a redirect
    redirected_page_id = db.fetch_redirected_page_id(page_id)

    if redirected_page_id == None:
      response['type'] = 'page'
    else:
      response['type'] = 'redirect'
      response['redirected_page_id'] = redirected_page_id

  return jsonify(response)


@app.route('/paths/<from_page_name>/<to_page_name>')
def get_shortest_path_between_pages(from_page_name, to_page_name):
  # Look up the IDs for each page
  try:
    from_page_id = db.fetch_page_id(from_page_name)
  except ValueError as error:
    raise InvalidRequest('From page name "{0}" does not exist.'.format(from_page_name))

  try:
    to_page_id = db.fetch_page_id(to_page_name)
  except ValueError as error:
    raise InvalidRequest('To page name "{0}" does not exist.'.format(to_page_name))

  # Compute the shortest paths
  paths_with_ids = db.get_shortest_paths(from_page_id, to_page_id)

  # Convert IDs to names for each path
  paths_with_names = []
  for current_path_with_ids in paths_with_ids:
    current_path_with_names = [db.fetch_page_name(page_id) for page_id in current_path_with_ids]
    paths_with_names.append(current_path_with_names)

  # Build the response object
  response = {
    'paths': paths_with_names,
    'count': len(paths_with_names)
  }

  if response['count'] != 0:
    response['length'] = len(paths_with_names[0])

  return jsonify(response)

if __name__ == "__main__":
  app.run()

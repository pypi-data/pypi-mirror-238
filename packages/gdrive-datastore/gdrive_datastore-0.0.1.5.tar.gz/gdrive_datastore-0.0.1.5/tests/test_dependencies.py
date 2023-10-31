import sys
from pytest import fail

from gdrive_datastore.gdrive import GDriveCopier

def test_dependencies():
  try:
    drive = GDriveCopier('test')
    fail('No exception')
  except Exception as e:
    type, value, traceback = sys.exc_info()
    assert(str(e) == 'Missing folder test.  Be sure to share the folder with the service account.')



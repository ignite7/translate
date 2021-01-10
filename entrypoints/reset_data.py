""" Delete migrations and db data. """

# Utilities
import os
import shutil


# Is root?
if os.geteuid() != 0:
    raise Exception('You need to be root for this operetion.')

# DB data
if os.path.exists('./api/data/db'):
    shutil.rmtree('./api/data/db')
    print('DB data deleted.')

# Users migrations
if os.path.exists('./api/users/migrations'):
    shutil.rmtree('./api/users/migrations')
    print('Users migrations deleted.')
else:
    os.mkdir('./api/users/migrations')
    f = open('./api/users/migrations/__init__.py', 'w')
    f.close()
    print('Users migrations created.')

# Histories migrations
if os.path.exists('./api/histories/migrations'):
    shutil.rmtree('./api/histories/migrations')
    print('Histories migrations deleted.')
else:
    os.mkdir('./api/histories/migrations')
    f = open('./api/histories/migrations/__init__.py', 'w')
    f.close()
    print('Histories migrations created.')

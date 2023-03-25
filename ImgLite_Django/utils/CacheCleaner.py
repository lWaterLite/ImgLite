"""
This is a timing script for cleaning the cache file.
ONLY can be started as python script when developing!
DO NOT start it as python script in production!
If you want to use it, use your system timing task solution.
For example, you can create a system service in Linux.
"""
import os
import shutil
import sched
import time

CACHE_FOLDER = '../cache'
CLEANUP_INTERVAL = 10  # 60 minutes in seconds


def delete_cache_folder():
    # delete all files and folders in the cache folder
    for filename in os.listdir(CACHE_FOLDER):
        file_path = os.path.join(CACHE_FOLDER, filename)
        try:
            if (os.path.isfile(file_path) or os.path.islink(file_path)) and filename != '.gitkeep':
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

    # schedule the next cleanup event
    scheduler.enter(CLEANUP_INTERVAL, 1, delete_cache_folder)


# create a scheduler object
scheduler = sched.scheduler(time.time, time.sleep)

# schedule the first cleanup event
scheduler.enter(CLEANUP_INTERVAL, 1, delete_cache_folder)

# start the scheduler
scheduler.run()

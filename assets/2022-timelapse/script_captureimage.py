#!/usr/bin/env python

# script_timelapse : t.blandin. This script is based on the exemple 
# developped by Jim Eastbrook for the python-gphoto2 lib. 

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from contextlib import contextmanager
import logging
import os
import subprocess
import sys

import gphoto2 as gp
# Variables
WORK_DIR = '/tmp/pictures'
number=0




#Configure camera for use
@contextmanager
def configured_camera():
    # initialise camera
    camera = gp.Camera()
    camera.init()
    try:
        # adjust camera settings
        config = camera.get_config()
        capturetarget_conf = config.get_child_by_name('capturetarget')
        capturetarget = capturetarget_conf.get_value()
        capturetarget_conf.set_value('Internal RAM')
        # image version
        imageformat_conf = config.get_child_by_name('imagequality')
        imageformat = imageformat_conf.get_value()
        imageformat_conf.set_value('JPEG Normal')
        # flash off
        flashmode_conf = config.get_child_by_name('flashmode')
        flashmode = flashmode_conf.get_value()
        flashmode_conf.set_value('Flash off')
        # We want to add the intersting settings here
        imagesize_conf = config.get_child_by_name('imagesize')
        imagesize=imagesize_conf.get_value()
        imagesize_conf.set_value('1936x1296')
        # End of the custom settings
        camera.set_config(config)
        # use camera
        yield camera
    finally:
        # reset configuration
        capturetarget_conf.set_value(capturetarget)
        imageformat_conf.set_value(imageformat)
        flashmode_conf.set_value(flashmode)
        imagesize_conf.set_value(imagesize)
        # DON'T FORGET TO RESET THE SETTINGS YOU MODIFY
        camera.set_config(config)
        camera.exit()

def main():
    # settings de logging, usefull for debug
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    callback_obj = gp.check_result(gp.use_python_logging())
    if not os.path.exists(WORK_DIR) : 
        os.makedirs(WORK_DIR)
    template = os.path.join(WORK_DIR, 'picture%04d.jpg')
    with configured_camera() as camera :
        path = camera.capture(gp.GP_CAPTURE_IMAGE)
        print("Capture", path.folder+path.name)
        camera_file = camera.file_get( path.folder, path.name, gp.GP_FILE_TYPE_NORMAL)
        camera_file.save(template % number)
        camera.file_delete(path.folder, path.name)
    return(0)

if __name__=="__main__" :
    main()

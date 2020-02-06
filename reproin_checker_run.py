#!/usr/bin/env python
import json
import flywheel
import os
import shutil
import logging
from fw_heudiconv.cli import export


# logging stuff
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('reproin-checker-gear')
logger.info("{:=^70}\n".format(": reproin-checker gear manager starting up :"))

# start up inputs
invocation = json.loads(open('config.json').read())
config = invocation['config']
inputs = invocation['inputs']
destination = invocation['destination']
key = inputs['api-key']['key']
fw = flywheel.Flywheel(key)
user = fw.get_current_user()

# start up logic:
analysis_container = fw.get(destination['id'])
project_container = fw.get(analysis_container.parents['project'])
project_label = project_container.label
# find session object origin
session_container = fw.get(analysis_container.parent['id'])
sessions = [session_container.label]
# find subject object origin
subject_container = fw.get(session_container.parents['subject'])
subjects = [subject_container.label]


# logging stuff
logger.info("Calling reproin-checker with the following settings:")
logger.info("Project: {}".format(project_label))
logger.info("Subject(s): {}".format(subjects))
logger.info("Session(s): {}".format(sessions))

# action
call = "fw-heudiconv-reproin --verbose --protocol_names " + inputs['protocol_names']
os.system(call)

logger.info("Done!")
logger.info("{:=^70}\n".format(": Exiting reproin-checker gear manager :"))

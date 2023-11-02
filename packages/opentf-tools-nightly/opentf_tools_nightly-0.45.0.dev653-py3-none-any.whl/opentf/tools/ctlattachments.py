# Copyright (c) 2023 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""opentf-ctl workflow attachments handling part"""

from typing import Any, Dict, List, NoReturn, Optional, Tuple

import fnmatch
import os
import sys

from opentf.tools.ctlcommons import (
    _error,
    _is_command,
    _ensure_options,
    _ensure_uuid,
    generate_output,
    _get_arg,
)
from opentf.tools.ctlconfig import read_configuration
from opentf.tools.ctlnetworking import _localstore, _get_file
from opentf.tools.ctlworkflows import _get_workflows, _get_workflow_attachments_events


########################################################################
# Constants

ALLURE_ENDING = '_a'
GLOBAL_ENDING = '_e'
ENDINGS = (ALLURE_ENDING, GLOBAL_ENDING)
WILDCARDS = ('*', '?', '[', ']', '!')

UUID_LENGTH = 36
ATTACHMENT_PREFIX_LENGTH = len('/tmp/')
ALLURE_PREFIX_LENGTH = len('allureReporting/')


########################################################################
# Help messages

CP_HELP = '''Get a local copy of a workflow attachment or workflow attachments

Example:
  # Get a local copy of a workflow attachment
  opentf-ctl cp 9ea3be45-ee90-4135-b47f-e66e4f793383:39e68299-8995-4915-9367-1df1ff642159 /target/dir/output_file.ext

  # Get a local copy of all workflow attachments in .tar format
  opentf-ctl cp 9ea3be45-ee90-4135-b47f-e66e4f793383:*.tar /target/dir/

  # Get a local copy of all surefire-xml typed workflow attachments
  opentf-ctl cp 9ea3be45-ee90-4135-b47f-e66e4f793383:* /target/dir --type *surefire-xml

Options:
  --type={...} or -t {...}: get only attachments of specified type (supports Unix file patterns).

Usage:
  opentf-ctl cp WORKFLOW_ID:(ATTACHMENT_ID | file_pattern) DESTINATION [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_ATTACHMENTS_HELP = '''List workflow attachments

Examples:
  # List workflow attachments
  opentf-ctl get attachments 9ea3be45-ee90-4135-b47f-e66e4f793383

  # List workflow attachments and their source files
  opentf-ctl get attachments 9ea3be45-ee90-4135-b47f-e66e4f793383 --verbose

Options:
  --output={yaml,json} or -o {yaml,json}: show information as YAML or JSON.
  --output=wide or -o wide: show additional information (channel OS, attachment type and creation time).
  --output=custom-columns= or -o custom-columns=: show specified information.
    (more at: https://opentestfactory.org/tools/running-commands#output-formats)
  --verbose or -v: show attachments source files (i.e. workflow Allure report source files)

Usage:
  opent-ctl get attachments WORKFLOW_ID [--output=wide] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

########################################################################
# Helpers


def _fatal(*msg) -> NoReturn:
    _error(*msg)
    sys.exit(2)


def _get_attachment_uuids(workflow_id: str) -> List[str]:
    attachments = _get_attachments_dict(workflow_id, True)
    return [attachment['uuid'] for attachment in attachments.values()]


def _get_options(options: List[str]) -> Tuple[str, str, str]:
    workflow_id, _, attachment_id = options[0].partition(':')
    if not workflow_id or not attachment_id or len(options) != 2:
        _error(
            'Invalid parameters. Was expecting WORKFLOW_ID:ATTACHMENT_ID DESTINATION_FILEPATH, got: %s.',
            ' '.join(options),
        )
        sys.exit(2)
    workflow_id = _ensure_uuid(workflow_id, _get_workflows)
    if any(wildcard in attachment_id for wildcard in WILDCARDS):
        return (workflow_id, attachment_id, options[1])
    if attachment_id.endswith(ENDINGS):
        ending = attachment_id[-2:]
        attachment_id = _ensure_uuid(attachment_id[:-2], _get_workflows) + ending
    else:
        attachment_id = _ensure_uuid(
            attachment_id, lambda: _get_attachment_uuids(workflow_id)
        )
    return (workflow_id, attachment_id, options[1])


def _get_download_name(headers, attachment_id: str) -> str:
    _, _, name_with_uuid = headers.get('Content-Disposition', '').partition('name=')
    if name_with_uuid.startswith(attachment_id):
        return name_with_uuid[UUID_LENGTH + 1 :]
    return 'untitled'


########################################################################
# Handle single attachment


def _get_attachment_stream(workflow_id: str, attachment_id: str):
    msg = f'Failed to get attachment {attachment_id} from localstore'
    response = _get_file(
        _localstore(),
        f'/workflows/{workflow_id}/files/{attachment_id}',
        msg=msg,
        statuses=(200, 404, 403, 500),
    )

    if response.status_code != 200:
        _fatal(
            '%s. Error code: %d, message: "%s"',
            msg,
            response.status_code,
            response.json().get('message'),
        )

    return response


def _save_attachment_stream(response, attachment_id, filepath):
    with open(os.path.normpath(filepath), 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
    print(
        f'Attachment {_get_download_name(response.headers, attachment_id)} ({attachment_id}) is downloaded as {filepath}.'
    )


def download_attachment(workflow_id: str, attachment_id: str, filepath: str) -> None:
    """Download attachment to filepath."""
    try:
        response = _get_attachment_stream(workflow_id, attachment_id)
        _save_attachment_stream(response, attachment_id, filepath)
    except Exception as err:
        _fatal(
            'Failed to download attachment %s as %s: %s.',
            attachment_id,
            filepath,
            str(err),
        )


########################################################################
# Handle multiple attachments


def _matches_type(filetype: Optional[str], pattern: Optional[str]) -> bool:
    if not pattern:
        return True
    if not filetype:
        return False
    return fnmatch.fnmatch(filetype, pattern)


def _make_target_path(data: Dict[str, Any]) -> Dict[str, str]:
    parent_step = data.get('parent_step')
    if not parent_step:
        return {'path': '', 'filename': data['filename']}
    if parent_step.get('sequence_id') in ('setup', 'teardown'):
        return {
            'path': f"./{data['job']['name']}/{parent_step['sequence_id']}",
            'filename': f"{data['metadata']['step_sequence_id']}_{data['filename']}",
        }
    return {
        'path': f"./{data['job']['name']}/{parent_step['sequence_id']}_{parent_step['testcase']}",
        'filename': data['filename'],
    }


def _get_attachments_paths(
    attachments: Dict[str, Any], name_pattern: str, type_pattern: Optional[str]
) -> Dict[str, Any]:
    attachments = {
        uuid: data
        for uuid, data in attachments.items()
        if fnmatch.fnmatch(data['filename'], name_pattern)
        and _matches_type(data.get('type'), type_pattern)
    }
    if not attachments:
        _error('No attachment matching pattern found.')
        sys.exit(1)
    return {uuid: _make_target_path(data) for uuid, data in attachments.items()}


def download_attachments(workflow_id: str, pattern: str, filepath: str) -> None:
    """Download multiple attachments to filepath."""
    attachments = _get_attachments_dict(workflow_id, False)
    attachments_paths = _get_attachments_paths(
        attachments, pattern, _get_arg('--type=') or _get_arg('-t=')
    )
    for uuid, data in attachments_paths.items():
        dir_path = os.path.normpath(f"{filepath}/{data['path']}")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        download_attachment(workflow_id, uuid, f"{dir_path}/{data['filename']}")


########################################################################
# Get attachments

DEFAULT_COLUMNS = (
    'JOB_NAME:.attachment.job.name',
    'STEP:.attachment.parent_step.sequence_id',
    'UUID:.attachment.uuid',
    'FILENAME:.attachment.filename',
    'TESTCASE:.attachment.parent_step.testcase',
)

WIDE_COLUMNS = (
    'JOB_NAME:.attachment.job.name',
    'STEP:.attachment.parent_step.sequence_id',
    'UUID:.attachment.uuid',
    'FILENAME:.attachment.filename',
    'TESTCASE:.attachment.parent_step.testcase',
    'CHANNEL_OS:.attachment.job.channel_os',
    'TYPE:.attachment.type',
    'CREATED_AT:.attachment.metadata.creationTimestamp',
)

METADATA_KEYS = (
    'annotations',
    'step_id',
    'creationTimestamp',
    'name',
    'step_origin',
    'step_sequence_id',
)
JOB_KEYS = ('namespace', 'channel_os', 'channel_id', 'job_id', 'job_origin')

EventsList = List[Dict[str, Any]]


def _get_file_name(kind: str, attachment: str) -> str:
    file = attachment[ATTACHMENT_PREFIX_LENGTH:]
    if kind == 'ExecutionResult':
        return file.split('_', maxsplit=2)[2]
    if 'allure' in attachment:
        return file[ALLURE_PREFIX_LENGTH + UUID_LENGTH + 1 :]
    return file[UUID_LENGTH + 1 :]


def _complete_job_and_parent_step(
    attachment: Dict[str, Any],
    parents: EventsList,
    commands: EventsList,
) -> Dict[str, Optional[str]]:
    job_id = attachment['job'].get('job_id')
    for command in commands:
        if command['metadata']['job_id'] == job_id:
            attachment['job']['name'] = command['metadata']['name']

    metadata = attachment['metadata']
    origin = metadata.get('step_origin') or [metadata['step_id']]
    parent_job = [
        job
        for parent in parents
        for name, job in parent.get('jobs', {}).items()
        for step in job.get('steps', [])
        if step.get('id') == origin[0]
        and attachment['job'].get('name') in (name, job.get('name'))
    ] or [{'steps': []}]
    for count, step in enumerate(parent_job[0]['steps'], start=1):
        if step.get('id') != origin[0]:
            continue
        parent_step = {
            'step_id': step['id'],
            'technology': step.get('uses', '').partition('/')[0],
            'testcase': step.get('with', {}).get('test', '').split('/')[-1],
            'sequence_id': count,
        }
        break
    else:
        parent_step = {
            'sequence_id': metadata.get('annotations', {})
            .get('opentestfactory.org/hooks', {})
            .get('channel')
        }
    attachment['parent_step'] = parent_step
    return attachment


def _get_uuid_and_filetype(kind, attachment, metadata):
    if kind == 'ExecutionResult':
        properties = metadata.get('attachments', {}).get(attachment, {})
        return properties['uuid'], properties.get('type')

    # WorkflowResult
    uuid = metadata['workflow_id']
    if 'allure' in attachment:
        uuid += ALLURE_ENDING
        filetype = None
    else:
        uuid += GLOBAL_ENDING
        filetype = metadata['attachments'][attachment].get('type')
    return uuid, filetype


def _get_attachment_data_steps(
    workflow_id: str,
    verbose: bool,
) -> Tuple[EventsList, EventsList, EventsList]:
    events = _get_workflow_attachments_events(workflow_id, verbose)
    results = [
        event
        for event in events
        if event['kind'] in ('ExecutionResult', 'WorkflowResult')
    ]
    parents = [
        event for event in events if event['kind'] in ('Workflow', 'GeneratorResult')
    ]
    commands = [
        event
        for event in events
        if event['kind'] == 'ExecutionCommand'
        and event.get('metadata', {}).get('step_sequence_id') == -1
    ]
    return results, parents, commands


def _get_attachments_dict(workflow_id: str, verbose: bool) -> Dict[str, Any]:
    results, parents, commands = _get_attachment_data_steps(workflow_id, verbose)
    attachments = {}
    for event in results:
        for attachment in event['attachments']:
            metadata = event['metadata']
            kind = event['kind']
            uuid, filetype = _get_uuid_and_filetype(kind, attachment, metadata)

            data = {
                'uuid': uuid,
                'filename': _get_file_name(kind, attachment),
                'type': filetype,
                'metadata': {},
                'job': {},
                'parent_step': {},
            }

            for key, value in metadata.items():
                if key in METADATA_KEYS:
                    data['metadata'].update({key: value})
                elif key in JOB_KEYS:
                    data['job'].update({key: value})

            if kind == 'ExecutionResult':
                _complete_job_and_parent_step(data, parents, commands)
            attachments[uuid] = data
    return attachments


def list_attachments(workflow_id: str, verbose: bool) -> None:
    """Get workflow attachments list."""
    workflow_id = _ensure_uuid(workflow_id, _get_workflows)
    attachments = _get_attachments_dict(workflow_id, verbose)
    output_data = [
        {'attachment': {'uuid': uuid, **definition}}
        for uuid, definition in attachments.items()
    ]
    generate_output(output_data, DEFAULT_COLUMNS, WIDE_COLUMNS)


########################################################################
# Exposed functions


def print_attachments_help(args: List[str]):
    """Display help."""
    if _is_command('cp', args):
        print(CP_HELP)
    elif _is_command('get attachments', args):
        print(GET_ATTACHMENTS_HELP)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


def attachments_cmd():
    """Interact with attachments."""
    if _is_command('cp _', sys.argv):
        options = _ensure_options('cp *', sys.argv[1:], extra=[('--type', '-t')])
        read_configuration()
        if options and any(wildcard in options[0] for wildcard in WILDCARDS):
            download_attachments(*_get_options(options))
        else:
            download_attachment(*_get_options(options))
    elif _is_command('get attachments _', sys.argv):
        workflow_id = _ensure_options(
            'get attachments _',
            sys.argv[1:],
            extra=[('--output', '-o')],
            flags=[('--verbose', '-v')],
        )
        read_configuration()
        list_attachments(workflow_id, '--verbose' in sys.argv or '-v' in sys.argv)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)

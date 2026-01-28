#!/usr/bin/python

# Copyright: (c) 2025, Nils Ost <home@nijos.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type
import requests

from ansible.module_utils.basic import AnsibleModule


DOCUMENTATION = r"""
---
module: token

author: Nils Ost (@nils-ost)

version_added: "1.0.0"

short_description: fetch npm API token (login)

description:
    - For other Nginx Proxy Manager endpoints a valid token is required,
    - this modules executes a login on an npm instance and returns the corresponding token

options:
    protocol:
        description:
            - wether http or https is used on proxymanager
        required: false
        type: str
        default: 'http'
        choices: ['http', 'https']
    host:
        description:
            - host (-address) of proxymanager API endpoint
        required: true
        type: str
    port:
        description:
            - host-port of proxymanager API endpoint
        required: false
        type: int
        default: 81
    user:
        description:
            - user (email) to authenticate on proxymanager instance
        required: true
        type: str
    password:
        description:
            - password to authenticate on proxymanager instance
        required: true
        type: str
"""

EXAMPLES = r"""
# fetch a token
- name: fetch proxymanager API token
  nils_ost.proxymanager.token:
    host: "{{ ansible_host }}"
    user: "{{ root_email }}"
    password: "{{ root_password_long }}"
  register: npm
"""

RETURN = r"""
url:
    description:
        - the URL build from protocol, host and port, to be used on other modules
    type: str
    returned: always
    sample: 'http://192.168.0.5:81'
token:
    description:
        - newly created API token for given user
    type: str
    returned: always
"""


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        protocol=dict(type="str", default="http", choices=["http", "https"]),
        host=dict(type="str", required=True),
        port=dict(type="int", required=False, default=81),
        user=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    try:
        headers = dict()
        headers["Content-Type"] = "application/json"

        data = dict(
            identity=module.params["user"],
            secret=module.params["password"],
        )

        result[
            "url"
        ] = f"{module.params['protocol']}://{module.params['host']}:{module.params['port']}"
        response = requests.post(
            result["url"] + "/api/tokens",
            json=data,
            headers=headers,
        )

        if not response.status_code == 200:
            module.fail_json(
                msg=f"error on fetching API token: {response.text}",
                **result,
            )

        if "token" not in response.json():
            module.fail_json(msg="API response not containing a token", **result)

        result["token"] = response.json().get("token")
        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)


def main():
    run_module()


if __name__ == "__main__":
    main()

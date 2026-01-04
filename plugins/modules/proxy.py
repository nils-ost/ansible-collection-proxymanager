#!/usr/bin/python

# Copyright: (c) 2025, Nils Ost <@nils-ost>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type
import requests

from ansible.module_utils.basic import AnsibleModule


DOCUMENTATION = r"""
---
module: proxy

author: Nils Ost (@nils-ost)

version_added: "1.0.0"

short_description: create, update or delete npm proxy

description:
    - This module creates, updates, deletes or just returns a Nginx Proxy Manager proxy host

options:
    url:
        description:
            - the full URL of API-Endpoint
        required: true
        type: str
    token:
        description:
            - the token used for authentication on API-Endpoint
        required: true
        type: str
    domain_name:
        description:
            - domain to be proxyed
        required: true
        type: str
    forward_host:
        description:
            - backend destination of proxy
        required: false (true if state equals present)
        type: str
    forward_scheme:
        description:
            - protocol to be used for communication with backend destination
        required: false
        type: str
        default: 'http'
        choices: ['http', 'https']
    forward_port:
        description:
            - backend destination port of proxy
        required: false
        type: int
        default: 80
    enable_caching:
        description:
            - if assets should be cached by npm
        required: false
        type: bool
        default: false
    allow_websockets:
        description:
            - if websocket support should be enabled
        required: false
        type: bool
        default: false
    certificate_id:
        description:
            - id of npm certificate to be used
        required: false
        type: int
        default: 0
    force_ssl:
        description:
            - if ssl should be forced
        required: false
        type: bool
        default: false
    http2_support:
        description:
            - if http/2 support should be enabled
        required: false
        type: bool
        default: false
    state:
        description:
            - if a proxy for domain_name should be created or deleted
        required: false
        type: str
        default: 'present'
        choices: ['absent', 'present']
"""

EXAMPLES = r"""
# create proxy host
- name: create npm proxy
  npm_proxy:
    url: "{{ npm.url }}"
    token: "{{ npm.token }}"
    domain_name: "some.domain"
    forward_host: "192.168.1.234"
    forward_port: 81
    certificate_id: "{{ some_cert.item.id }}"
    state: present
  delegate_to: localhost

# enable caching for formaly created proxy
- name: update npm proxy
  npm_proxy:
    url: "{{ npm.url }}"
    token: "{{ npm.token }}"
    domain_name: "some.domain"
    forward_host: "192.168.1.234"
    forward_port: 81
    enable_caching: True
    certificate_id: "{{ some_cert.item.id }}"
    state: present
  delegate_to: localhost

# delete the formaly created and updated proxy
- name: delete npm proxy
  npm_proxy:
    url: "{{ npm.url }}"
    token: "{{ npm.token }}"
    domain_name: "some.domain"
    state: absent
  delegate_to: localhost
"""

RETURN = r"""
item:
    description:
        - the item corresponding to domain_name created, updated or found on npm. might be None in case of errors or deletion
    type: dict or None
    returned: always
"""


def data_as_expected(d1, d2):
    keys = [
        "domain_names",
        "forward_scheme",
        "forward_host",
        "forward_port",
        "caching_enabled",
        "allow_websocket_upgrade",
        "certificate_id",
        "ssl_forced",
        "http2_support",
    ]
    for k in keys:
        if k not in d1:
            return False
        if k not in d2:
            return False
        if not d1.get(k) == d2.get(k):
            return False
    return True


def search(url, token, name):
    uri = f"{url}/api/nginx/proxy-hosts"

    headers = dict()
    headers["Authorization"] = "Bearer %s" % token
    headers["Content-Type"] = "application/json"

    response = requests.get(uri, headers=headers)
    if not response.status_code == 200:
        return (False, response.text)

    for item in response.json():
        if name in item.get("domain_names", list()):
            return (True, item)
    return (True, None)


def create(url, token, data):
    uri = f"{url}/api/nginx/proxy-hosts"

    headers = dict()
    headers["Authorization"] = "Bearer %s" % token
    headers["Content-Type"] = "application/json"

    response = requests.post(uri, json=data, headers=headers)
    if not response.status_code == 201:
        return (False, response.text)
    return (True, response.json())


def update(url, token, item, data):
    uri = f"{url}/api/nginx/proxy-hosts/{item}"

    headers = dict()
    headers["Authorization"] = "Bearer %s" % token
    headers["Content-Type"] = "application/json"

    response = requests.put(uri, json=data, headers=headers)
    if not response.status_code == 200:
        return (False, response.text)
    return (True, response.json())


def delete(url, token, item):
    uri = f"{url}/api/nginx/proxy-hosts/{item}"

    headers = dict()
    headers["Authorization"] = "Bearer %s" % token
    headers["Content-Type"] = "application/json"

    response = requests.delete(uri, headers=headers)
    if not response.status_code == 200:
        return (False, response.text)
    return (True, response.json())


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        url=dict(type="str", required=True),
        token=dict(type="str", required=True, no_log=True),
        domain_name=dict(type="str", required=True),
        forward_host=dict(type="str", required=False, default=None),
        forward_scheme=dict(
            type="str",
            required=False,
            default="http",
            choices=["http", "https"],
        ),
        forward_port=dict(type="int", required=False, default=80),
        enable_caching=dict(type="bool", required=False, default=False),
        allow_websockets=dict(type="bool", required=False, default=False),
        certificate_id=dict(type="int", required=False, default=0),
        force_ssl=dict(type="bool", required=False, default=False),
        http2_support=dict(type="bool", required=False, default=False),
        state=dict(type="str", default="present", choices=["absent", "present"]),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        item=None,
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
        url = module.params["url"]
        token = module.params["token"]

        if (
            module.params["state"] == "present"
            and module.params.get("forward_host") is None
        ):
            module.fail_json(
                msg='"forward_host" is required if "state" is "present"',
                **result,
            )

        success, item = search(url, token, module.params["domain_name"])
        if not success:
            module.fail_json(msg=f"error on searching for item: {item}", **result)

        if module.params["state"] == "present":
            data = dict(
                domain_names=[module.params["domain_name"]],
                forward_scheme=module.params["forward_scheme"],
                forward_host=module.params["forward_host"],
                forward_port=module.params["forward_port"],
                caching_enabled=module.params["enable_caching"],
                allow_websocket_upgrade=module.params["allow_websockets"],
                certificate_id=module.params["certificate_id"],
                ssl_forced=module.params["force_ssl"],
                http2_support=module.params["http2_support"],
                hsts_enabled=False,
                hsts_subdomains=False,
                advanced_config="",
                block_exploits=False,
                access_list_id=0,
                locations=[],
                meta={},
            )

            if item is None:
                if not module.check_mode:
                    success, item = create(url, token, data)
                    if not success:
                        module.fail_json(
                            msg=f"error on createing new item: {item}",
                            **result,
                        )
                    result["changed"] = True
                    result["item"] = item
                    module.exit_json(msg=f"created item: {item['id']}", **result)
                else:
                    result["changed"] = True
                    result["item"] = data
                    module.exit_json(msg="would have created a item", **result)

            else:
                if not module.check_mode:
                    if data_as_expected(data, item):
                        result["item"] = item
                        module.exit_json(
                            msg=f"item is already as expected: {item['id']}",
                            **result,
                        )
                    success, item = update(url, token, item.get("id"), data)
                    if not success:
                        module.fail_json(
                            msg=f"error on updateing existing item: {item}",
                            **result,
                        )
                    result["changed"] = True
                    result["item"] = item
                    module.exit_json(msg=f"updated item: {item['id']}", **result)
                else:
                    result["changed"] = True
                    result["item"] = data
                    module.exit_json(
                        msg=f"would have updated item: {item['id']}",
                        **result,
                    )

        else:
            if item is None:
                module.exit_json(msg="item is already deleted", **result)
            if not module.check_mode:
                success, item = delete(url, token, item.get("id"))
                if not success:
                    module.fail_json(msg=f"error on deleteing item: {item}", **result)
                result["changed"] = True
                module.exit_json(msg="deleted item", **result)
            else:
                result["changed"] = True
                module.exit_json(msg="would have deleted a item", **result)

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)


def main():
    run_module()


if __name__ == "__main__":
    main()

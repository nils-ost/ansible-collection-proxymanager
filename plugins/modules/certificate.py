#!/usr/bin/python

# Copyright: (c) 2025, Nils Ost <@nils-ost>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type
import requests

from ansible.module_utils.basic import AnsibleModule


DOCUMENTATION = r"""
---
module: certificate

author: Nils Ost (@nils-ost)

version_added: "1.0.0"

short_description: create or delete npm certificate

description:
    - This module creates, deletes or just returns a Nginx Proxy Manager certificate
    - On creation always generates a wildcard certificate for "domain_name"
    - Creation currently only works for provider "domainoffensive"
    - For "other" provider it's only checked if certificate is present, and if so, the item is returend

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
            - domain of certificate
        required: true
        type: str
    provider:
        description:
            - the provider of the certificate
        required: false
        type: str
        default: 'other'
        choices: ['domainoffensive', 'other']
    provider_credentials:
        description:
            - only required on certificate creation, to validate request on the provider side
        required: false
        type: str
        default: ''
    state:
        description:
            - if a certificate for domain_name should be created or deleted
        required: false
        type: str
        default: 'present'
        choices: ['absent', 'present']
"""

EXAMPLES = r"""
# create a do.de certificate
- name: create some.domain certificate
  npm_certificate:
    url: "{{ npm.url }}"
    token: "{{ npm.token }}"
    domain_name: "some.domain"
    provider: 'domainoffensive'
    provider_credentials: '{{ do_de_token }}'
    state: present
  delegate_to: localhost
  register: some_cert

# check for certificate existance and return item
- name: check some.domain certificate
  npm_certificate:
    url: "{{ npm.url }}"
    token: "{{ npm.token }}"
    domain_name: "some.domain"
    state: present
  delegate_to: localhost
  register: some_cert

# delete the formaly created certificate
- name: delete some.domain certificate
  npm_certificate:
    url: "{{ npm.url }}"
    token: "{{ npm.token }}"
    domain_name: "some.domain"
    state: absend
  delegate_to: localhost
"""

RETURN = r"""
item:
    description:
        - the item corresponding to domain_name created or found on npm. might be None in case of errors or deletion
    type: dict or None
    returned: always
"""


def search(url, token, name):
    uri = f"{url}/api/nginx/certificates"

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
    uri = f"{url}/api/nginx/certificates"

    headers = dict()
    headers["Authorization"] = "Bearer %s" % token
    headers["Content-Type"] = "application/json"

    response = requests.post(uri, json=data, headers=headers)
    if not response.status_code == 201:
        return (False, response.text)
    return (True, response.json())


def delete(url, token, item):
    uri = f"{url}/api/nginx/certificates/{item}"

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
        provider=dict(
            type="str",
            required=False,
            default="other",
            choices=["domainoffensive", "other"],
        ),
        provider_credentials=dict(type="str", required=False, default=""),
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

        success, item = search(url, token, module.params["domain_name"])
        if not success:
            module.fail_json(msg=f"error on searching for item: {item}", **result)

        if module.params["state"] == "present" and item is not None:
            result["item"] = item
            module.exit_json(
                msg=f"found item is already present: {item['id']}",
                **result,
            )

        elif (
            module.params["state"] == "present"
            and module.params.get("provider", "other") == "domainoffensive"
        ):
            data = dict(
                domain_names=[
                    module.params["domain_name"],
                    f"*.{module.params['domain_name']}",
                ],
                provider="letsencrypt",
                meta=dict(
                    dns_challenge=True,
                    dns_provider="domainoffensive",
                    dns_provider_credentials=f"dns_domainoffensive_api_token = {module.params.get('provider_credentials', '')}",
                ),
            )

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

        elif module.params["state"] == "present":
            module.fail_json(msg="no item found for other provider", **result)

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

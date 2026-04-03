# nils_ost proxymanager Collection Release Notes

**Topics**

- <a href="#v2-0-0">v2\.0\.0</a>
  - <a href="#release-summary">Release Summary</a>
  - <a href="#minor-changes">Minor Changes</a>
  - <a href="#breaking-changes--porting-guide">Breaking Changes / Porting Guide</a>
  - <a href="#bugfixes">Bugfixes</a>
  - <a href="#known-issues">Known Issues</a>
- <a href="#v1-0-0">v1\.0\.0</a>
  - <a href="#release-summary-1">Release Summary</a>
  - <a href="#new-modules">New Modules</a>
  - <a href="#new-roles">New Roles</a>

<a id="v2-0-0"></a>

## v2\.0\.0

<a id="release-summary"></a>

### Release Summary

Merged PR of \@tecbeat\, that added missing parameters \(see below\)
Changed default compose path for docker installations

<a id="minor-changes"></a>

### Minor Changes

- Added missing parameters to proxy module \(thanks \@tecbeat\) \(hsts_enabled\, hsts_subdomains\, trust_forwarded_proto\, advanced_config\, block_exploits\, access_list_id\)

<a id="breaking-changes--porting-guide"></a>

### Breaking Changes / Porting Guide

- Default path of <em class="title-reference">proxymanager_compose_dir</em> for role <em class="title-reference">install_with_docker</em> changed from <em class="title-reference">\~/proxymanager</em> to <em class="title-reference">/opt/proxymanager</em>

<a id="bugfixes"></a>

### Bugfixes

- Examples in modules referenced wrong module\-name

<a id="known-issues"></a>

### Known Issues

- Locations parameter \(complex array structure\) not yet implemented but documented in TODO\.md

<a id="v1-0-0"></a>

## v1\.0\.0

<a id="release-summary-1"></a>

### Release Summary

This is the first proper release of <code>nils_ost\.proxymanager</code> collection on 2026\-01\-07\.
The added Modules and Roles were just carried over from other local projects\.
This\, as my first ever ansible collection release\, is in memory of my grandfather who passed away today\.\.\.

<a id="new-modules"></a>

### New Modules

- nils_ost\.proxymanager\.certificate \- create or delete npm certificate\.
- nils_ost\.proxymanager\.proxy \- create\, update or delete npm proxy\.
- nils_ost\.proxymanager\.redirection \- create\, update or delete npm redirection\.
- nils_ost\.proxymanager\.token \- fetch npm API token \(login\)\.

<a id="new-roles"></a>

### New Roles

- nils_ost\.proxymanager\.basic_config \- configures Nginx Proxy Manager with basic capabilities\.
- nils_ost\.proxymanager\.install_with_docker \- installs Nginx Proxy Manager within docker\.

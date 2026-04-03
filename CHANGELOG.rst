===============================================
nils\_ost proxymanager Collection Release Notes
===============================================

.. contents:: Topics

v2.0.0
======

Release Summary
---------------

Merged PR of @tecbeat, that added missing parameters (see below)
Changed default compose path for docker installations

Minor Changes
-------------

- Added missing parameters to proxy module (thanks @tecbeat) (hsts_enabled, hsts_subdomains, trust_forwarded_proto, advanced_config, block_exploits, access_list_id)

Breaking Changes / Porting Guide
--------------------------------

- Default path of `proxymanager_compose_dir` for role `install_with_docker` changed from `~/proxymanager` to `/opt/proxymanager`

Bugfixes
--------

- Examples in modules referenced wrong module-name

Known Issues
------------

- Locations parameter (complex array structure) not yet implemented but documented in TODO.md

v1.0.0
======

Release Summary
---------------

This is the first proper release of ``nils_ost.proxymanager`` collection on 2026-01-07.
The added Modules and Roles were just carried over from other local projects.
This, as my first ever ansible collection release, is in memory of my grandfather who passed away today...

New Modules
-----------

- nils_ost.proxymanager.certificate - create or delete npm certificate.
- nils_ost.proxymanager.proxy - create, update or delete npm proxy.
- nils_ost.proxymanager.redirection - create, update or delete npm redirection.
- nils_ost.proxymanager.token - fetch npm API token (login).

New Roles
---------

- nils_ost.proxymanager.basic_config - configures Nginx Proxy Manager with basic capabilities.
- nils_ost.proxymanager.install_with_docker - installs Nginx Proxy Manager within docker.

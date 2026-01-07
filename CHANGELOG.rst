===============================================
nils\_ost proxymanager Collection Release Notes
===============================================

.. contents:: Topics

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

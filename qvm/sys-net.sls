# -*- coding: utf-8 -*-
# vim: set syntax=yaml ts=2 sw=2 sts=2 et :

##
# qvm.sys-net
# ===========
#
# Installs 'sys-net' NetVM.
#
# Pillar data will also be merged if available within the ``qvm`` pillar key:
#   ``qvm:sys-net``
#
# located in ``/srv/pillar/dom0/qvm/init.sls``
#
# Execute:
#   qubesctl state.sls qvm.sys-net dom0
##

{%- from "qvm/template.jinja" import load -%}

{% load_yaml as defaults -%}
name:          sys-net
present:
  - label:     red
  - mem:       300
  - flags:
    - net
prefs:
  - netvm:     'none'
  - autostart: true
  - pcidevs:   {{ salt['grains.get']('pci_net_devs', []) }}
{%- endload %}

{{ load(defaults) }}

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-22 21:30
from __future__ import unicode_literals

from django.db import migrations, models

from server.models import Plugin

from django.conf import settings

from yapsy.PluginManager import PluginManager

import os
from server import utils


def update_os_families(apps, schema_editor):
    enabled_plugins = Plugin.objects.all()
    # Build the manager
    manager = PluginManager()
    # Tell it the default place(s) where to find plugins
    manager.setPluginPlaces([settings.PLUGIN_DIR, os.path.join(settings.PROJECT_DIR, 'server/plugins')])
    # Load all plugins
    manager.collectPlugins()
    enabled_plugins = apps.get_model("server", "MachineDetailPlugin")
    for item in enabled_plugins.objects.all():
        default_families = ['Darwin', 'Windows', 'Linux']
        for plugin in manager.getAllPlugins():
            if plugin.name == item.name:

                try:
                    supported_os_families = plugin.plugin_object.supported_os_families()
                except:
                    supported_os_families = default_families
                item.os_families = utils.flatten_and_sort_list(supported_os_families)
                item.save()



class Migration(migrations.Migration):

    dependencies = [
        ('server', '0057_auto_20170822_1421'),
    ]

    operations = [
        migrations.RunPython(update_os_families),
    ]

#!/bin/bash

VENV=venv/bin
source $VENV/activate

export TEST_RUNNER="green.djangorunner.DjangoRunner"
export DJANGO_SETTINGS_MODULE="djq.settings"
$VENV/green djq.tests


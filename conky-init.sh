#!/bin/bash

conky -q -c ./.wakaconky & # wakaconky
conky -q -c ./.gitconky & exit # gitconky


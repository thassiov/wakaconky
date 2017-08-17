#!/bin/bash

conky -q -c ./.conkyrc & # wakaconky
conky -q -c ./.gitconky & exit # gitconky


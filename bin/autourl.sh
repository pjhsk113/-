#!/bin/bash
sudo service apache2 restart
curl -s "http://13.125.111.56/hakcrawl/" > /dev/null
curl -s "http://13.125.111.56/kyocrawl/" > /dev/null


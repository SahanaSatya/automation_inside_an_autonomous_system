# automation_inside_an_autonomous_system
This project involves automating iBGP and abstracting IGP (OSPF) configuration for an Autonomous System in an overlay network using Python scripts.

All the routers were configured to have SSH enabled on them and the SSH information for each router was maintained in a central CSV file.

Having a configuration file for BGP-related information like, Networks to advertise, Remote AS number, etc, Netmiko module was used for configuring iBGP sessions between edge routers.

For abstracting the configuration of OSPF, a flask-based web interface was presented to the user to enter OSPF-related information like Process ID, Area ID, Networks to advertise, etc. & to verify connectivity by pinging user-specified IP addresses and display statistics. In the back-end, user-entered information was stored in an SQL database, NAPALM module was used to provide abstraction for configuration and facilitate roll-over to previous working configuration.

In order to enable faster deployment of configuration, Devops tools like Anisble and Jinja2 were used to automate the creation of templates for router configuration. This configuration were later pushed into routers using NETMIKO module

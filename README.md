# CellarTracker-for-Home-Assistant
With this custom component you will be able to get your wines from CellarTracker into Home Assistant.
THe component will only make the following entities:
CT_red: contains a list of all red wine and a total number of bottles
CT_white: contains a list of all white wine and a total number of bottles
CT_rose: contains a list of all rosé wine and a total number of bottles
CT_sparkling: contains a list of all sparkling wine and a total number of bottles
CT_fortified: contains a list of all fortified wine and a total number of bottles
CT_other: contains a list of all other wines/spirits/beer etc. and the total number of bottles
CT_total: contains the total number of bottles, the total price and the average price pr. bottle

The following changes has to be done:

**configuration.yaml:**
sensor: #ensure that your cellartracker username and password are added in the secrets.yaml file.
  - platform: CT_winelist
    username: !secret CT_winelist_username
    password: !secret CT_winelist_password

Add the **CT_winelist** folder from this repository to your custom_component folder.

Add the **lovelace.yaml** content to your lovelace.yaml file. Prereqs for this is the following custom components which can be installed through HACS Frontend:
**vertical-stack-in-card** - https://github.com/ofekashery/vertical-stack-in-card
**layout-card** - https://github.com/thomasloven/lovelace-layout-card
**flex-table** - https://github.com/custom-cards/flex-table-card

# AAS Classes Upgrader Tool

## Overview

This tool facilitates the automatic upgrading of Asset Administration Shell (AAS) objects from metamodel version 2.0.1 to version 3.0.1. 
It addresses compatibility between different versions of AAS models by mapping attributes and types from the old version (v2.0.1) to their counterparts in the version (v3.0.1).

## Installation

Install the AAS Classes Upgrader tool with pip:

```bash
pip install git+https://github.com/rwth-iat/aas_upgrader_tool.git@main
```

## Usage

To use the AAS Classes Upgrader, instantiate the `AAS_Classes_Upgrader` class and call the `upgrade` method with the old AAS object (v2) you wish to upgrade:

```python
from aas_upgrader import AAS_Classes_Upgrader

# Initialize the upgrader with the provider if necessary
upgrader = AAS_Classes_Upgrader(provider=my_obj_store_v2)

# Upgrade all objects in the provided obj store
upgraded_obj_store_v3 = upgrader.upgrade_obj_store()

# Or upgrade a single old AAS object
upgraded_obj = upgrader.upgrade(old_aas_object)
```


## Features

- Upgrades individual AAS objects or entire stores from v2 to v3.
- Maps old object attributes to new ones according to predefined rules.
- Handles complex types, including iterables and dictionaries.
- Skips or reports unsupported types to ensure a smooth upgrade process.



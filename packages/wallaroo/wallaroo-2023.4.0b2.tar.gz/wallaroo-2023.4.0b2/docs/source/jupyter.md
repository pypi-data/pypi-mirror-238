# Jupyter

_Wallaroo can be configured to install Jupyter Hub or to support an external environment._

In the Wallaroo Installer configuration screen, there is a section `Data Science Workspaces`, where the administrator chooses from `Jupyter Hub`, or `None`.

## Jupyter Hub

For workgroup applications [Jupyter Hub](https://jupyterhub.readthedocs.io/en/stable) provides a proxy authentication service which identifies users and launches a personal Jupyter Lab server for each user.  The proxy server is called `proxy-public` on port 80.

* Each Lab has a persistent home directory mounted on `/home/jovyan`. If the lab restarts, any work done is retained.
    * The storage size of the home can be set in the Wallaroo installation screen via the item. `Each Lab - Disk Storage Capacity in GB`. It can be grown later by the Kubernetes administrator.
    * Homes are not shared between users.
* Server state management
    * Logging out of the lab (menu `File -> Log Out`) or disconnecting from it does NOT stop the lab. Long term jobs will continue running.
    * There is a menu `File -> Hub Control Panel` for each user to access their server's control: there is a `Stop My Server` which will stop the lab server and release CPU back to the network. Saved work is not lost.
* User Authentication
      * Wallaroo plans to support full OAuth pluggable authentication in the near future.
* Hub Administrators
    * Hub Administrators can create other users and administrators and start and stop all users' Labs.
    * As installed by wallaroo, a default set of hub administrator users is provided. After installation, the Wallaro administrator should create users and remove old ones.
    * Hub administrator users will also see an `Admin` button on the hub control panel. This can also be accessed directly via the `/hub/admin` endpoint.

## Inside the Hub Environment

* The Wallaroo SDK comes pre-installed along with a full Python-3 kernel.
* If provided by the administrator at install time, the `/etc/secrets` directory contains application credential files for connecting to databases. The directory can be listed in the file explorer at the left or in a terminal tab. For example, in a GCP environment, a Python user might use the secret like this:

```python
from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/secrets/google-application-credentials.json"
client = bigquery.Client()
```

## External Environment

Choosing `None` in the Wallaroo Installer will cause no environment to be installed.

In all cases, an external IDE or Jupyter can still be used as a client.

1. Install the Wallaroo SDK via `pip install wallaroo` from the [PyPi Wallaroo Project](https://pypi.org/project/wallaroo).
2. Make sure the client has network reachability to the `api-lb` service inside the Wallaroo deployment. The administrator must provide the host and port to users.
2. When initializing classes, provide the hostname or IP address and the port of the `api-lb` service to constructors. For example,

```python
import wallaroo
wl = wallaroo.Client(api_endpoint = "http://your-api-lb:8080")
```

---
title: Full day
hero: "Full day"
description: "..."
icon: material/run
---
# Full day

## Passwords
Ensure you have access to the following passwords, to be able to troubleshoot:
- Admin for the Router
- WLAN Password
- Password for `root` login on the robots

|Check|When|What|
|---|---|---|
| |1-2 Days Before Event| [Order OpenShift Data Center env](#order-openshift-data-center-env) |
| |1-2 Days Before Event| [Update auto-register repo](#update-auto-register-repo)|
| |Location|[Setting up the environment](#setting-up-the-environment-on-site)|
| |Location|[Assign team E-Mails to users](#assign-team-e-mails-to-users) |

## Order OpenShift Data Center env

This includes deploying the hackathon environment in [demo.redhat.com](https://catalog.demo.redhat.com/catalog?search=Cloud+Native+Robot+Hackathon&item=babylon-catalog-prod%2Fsandboxes-gpte.cloud-native-robot.prod) and making sure an Edge Gateway is available.

|Field|Value
|---|---|
|OpenShift User Count|`9`|
|Region|Close as possible: `eu-central-1`|
|GPU Worker Nodes|At least one for the Code Assistent|
|Enable workshop user interface|True|

!! Ensure, that the list of robots includes the ones, that are available to you.

### Check GitOps sync state

via Command line:
```shell
oc get applications.argoproj.io -n openshift-gitops
```

everything should by Synced and Healthy!

```shell
% oc get applications.argoproj.io -n openshift-gitops
NAME                    SYNC STATUS   HEALTH STATUS
cluster-configuration   Synced        Healthy
team-1-ai               Synced        Healthy
team-1-dev              Synced        Healthy
team-1-devspaces        Synced        Healthy
team-1-label-studio     Synced        Healthy
team-2-ai               Synced        Healthy
team-2-dev              Synced        Healthy
team-2-devspaces        Synced        Healthy
team-2-label-studio     Synced        Healthy
team-3-ai               Synced        Healthy
team-3-dev              Synced        Healthy
team-3-devspaces        Synced        Healthy
team-3-label-studio     Synced        Healthy
team-4-ai               Synced        Healthy
team-4-dev              Synced        Healthy
team-4-devspaces        Synced        Healthy
team-4-label-studio     Synced        Healthy
team-5-ai               Synced        Healthy
team-5-dev              Synced        Healthy
team-5-devspaces        Synced        Healthy
team-5-label-studio     Synced        Healthy
team-6-ai               Synced        Healthy
team-6-dev              Synced        Healthy
team-6-devspaces        Synced        Healthy
team-6-label-studio     Synced        Healthy
team-7-ai               Synced        Healthy
team-7-dev              Synced        Healthy
team-7-devspaces        Synced        Healthy
team-7-label-studio     Synced        Healthy
team-8-ai               Synced        Healthy
team-8-dev              Synced        Healthy
team-8-devspaces        Synced        Healthy
team-8-label-studio     Synced        Healthy
team-9-ai               Synced        Healthy
team-9-dev              Synced        Healthy
team-9-devspaces        Synced        Healthy
team-9-label-studio     Synced        Healthy
```

## Update auto-register repo

Get RW Access to the Repository https://github.com/cloud-native-robotz-hackathon/robot-auto-register-78b09.
Put the web-hub-controller URL into the file.
You can get the Route via `oc get route web -n hub-controller -ojson | jq .spec.host`

### 🤖 Robot's

* Unpack all Robots
* Attach robots to power and start up
* Boot all Robots.
* Wait a couple of minutes...
* Connect your Laptop to Wifi `robot-hackathon-78b09`
* Check connection via ansible

    At the infrastructure repo:

    ```bash
    % cd automation/
    % ansible-navigator run ./ping-all.yaml
    ```

    And let it dance via:

    ```bash
    % cd automation/
    % ansible-navigator run ./move-robots.yaml
    ```

## Setting up the environment on site

### Wifi Router

* Start the Wifi router and attach to the local Wifi or wire
  * SSID: `robot-hackathon-78b09`
  * Wifi-Password: Stored in RH Bitwarden collection, and on the robot in the netplan configuration
  * The router is a preconfigured GL.iNet AXT1800, the configuration to restore is here (always use latest!): [gDrive router backup](https://drive.google.com/drive/folders/19ZIPrv9bnL4JvYXGgUOYihp5AsKfzZPa?usp=drive_link) (RH internal only)
  * Check connectivity to Internet

Note: If you use your own router and not the preconfigured one, you need to ensure, that the robots are available via their name. This can be done either by DHCP configs, or in .ssh/config

## Assign team E-Mails to users

At demo.redhat.com workshop interface, add the E-Mail addresses to the users:

|E-Mail|User|
|---|---|
|team-1@example.com|team-1|
|team-2@example.com|team-2|
|team-3@example.com|team-3|
|team-4@example.com|team-4|
|team-5@example.com|team-5|
|team-6@example.com|team-6|
|team-7@example.com|team-7|
|team-8@example.com|team-8|
|team-9@example.com|team-9|

## Run the Hackathon

Have fun!

# wakaconky
### wakatime and git(hub/lab) info in a conky

![screenshot](assets/screenshot.57.png)

## How it works

Wakaconky's goal is to show your coding information provided by Wakatime. It calls Wakatime's API for data and then prints it in your desktop via Conky.

In addition to Wakatime's data, Gitlab and Github issues can be shown in your desktop (scripts are placed at `wakaconky/gitscripts`).

## Dependencies

- conky (srsly?)
- Wakatime plugin installed in your text editor/IDE (Wakaconky reads the config file created by it)
- python 3
- requests (pip install requests)
- [optional] font: Fira Mono

## Installation

You can clone this repository in any directory you want. Then, you add `wakaconky/conky-init.sh` script in your startup config.
And that's it.

### Under the hood

The `wakaconky.py` script will read `$HOME/.wakatime.cfg` file (which was created by Wakatime's plugin) and get your access token from it.
The information shown in your desktop will be fetched using Wakatime's API and your access token.

The `gitscripts/github.py` and `gitscripts/gitlab.py` scripts will get the credentials you provided in `$HOME/.gitconky.json` to fetch your project's issues.

You need to create the `$HOME/.gitconky.json` file with the following content: 

```
{
    "gitlab_token":"<access_token>",
    "github_token":"<access_token>",
    "github_username":"<username>"
}

```

### About access tokens

#### Wakatime

When you install wakatime's plugin in your text editor, the `$HOME/.wakatime.cfg` file is created. Wakaconky reads the
access token from this file.

#### Gitlab

Go to Gitlab's [Personal Access Tokens](https://gitlab.com/profile/personal_access_tokens)'s page and generate a token with the following scopes:

- api
- read_user
- read_registry

Leave 'expiration date' blank.

#### Github

Go to Github's [Personal Access Tokens](https://github.com/settings/tokens)'s page and generate a token with the following scopes:

- public_repo
- read:org
- read:user
- repo:status

## TODO

- make configuration a bit less cumbersome
- limit number of issues shown
- better documentation
- create python script specific for data fetching
- create python script specific for data formating

## CONTRIBUTIONS

Just go ahead and open a PR

## LICENSE

[MIT](LICENSE)
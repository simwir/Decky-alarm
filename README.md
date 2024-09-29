# Decky Plugin Template [![Chat](https://img.shields.io/badge/chat-on%20discord-7289da.svg)](https://deckbrew.xyz/discord)

Reference example for using [decky-frontend-lib](https://github.com/SteamDeckHomebrew/decky-frontend-lib) (@decky/ui) in a [decky-loader](https://github.com/SteamDeckHomebrew/decky-loader) plugin.

### **Please also refer to the [wiki](https://wiki.deckbrew.xyz/en/user-guide/home#plugin-development) for important information on plugin development and submissions/updates. currently documentation is split between this README and the wiki which is something we are hoping to rectify in the future.**  

## Developers

### Dependencies

This template relies on the user having Node.js v16.14+ and `pnpm` (v9) installed on their system.  
Please make sure to install pnpm v9 to prevent issues with CI during plugin submission.  
`pnpm` can be downloaded from `npm` itself which is recommended.

#### Linux

```bash
sudo npm i -g pnpm@9
```

If you would like to build plugins that have their own custom backends, Docker is required as it is used by the Decky CLI tool.

### Making your own plugin

1. You can fork this repo or utilize the "Use this template" button on Github.
2. In your local fork/own plugin-repository run these commands:
   1. ``pnpm i``
   2. ``pnpm run build``
   - These setup pnpm and build the frontend code for testing.
3. Consult the [decky-frontend-lib](https://github.com/SteamDeckHomebrew/decky-frontend-lib) repository for ways to accomplish your tasks.
   - Documentation and examples are still rough, 
   - Decky loader primarily targets Steam Deck hardware so keep this in mind when developing your plugin.
4. If using VSCodium/VSCode, run the `setup` and `build` and `deploy` tasks. If not using VSCodium etc. you can derive your own makefile or just manually utilize the scripts for these commands as you see fit.

If you use VSCode or it's derivatives (we suggest [VSCodium](https://vscodium.com/)!) just run the `setup` and `build` tasks. It's really that simple.

#### Other important information

Everytime you change the frontend code (`index.tsx` etc) you will need to rebuild using the commands from step 2 above or the build task if you're using vscode or a derivative.

Note: If you are receiving build errors due to an out of date library, you should run this command inside of your repository:

```bash
pnpm update @decky/ui --latest
```

### Backend support

If you are developing with a backend for a plugin and would like to submit it to the [decky-plugin-database](https://github.com/SteamDeckHomebrew/decky-plugin-database) you will need to have all backend code located in ``backend/src``, with backend being located in the root of your git repository.
When building your plugin, the source code will be built and any finished binary or binaries will be output to ``backend/out`` (which is created during CI.)
If your buildscript, makefile or any other build method does not place the binary files in the ``backend/out`` directory they will not be properly picked up during CI and your plugin will not have the required binaries included for distribution.

Example:  
In our makefile used to demonstrate the CI process of building and distributing a plugin backend, note that the makefile explicitly creates the `out` folder (``backend/out``) and then compiles the binary into that folder. Here's the relevant snippet.

```make
hello:
	mkdir -p ./out
	gcc -o ./out/hello ./src/main.c
```

The CI does create the `out` folder itself but we recommend creating it yourself if possible during your build process to ensure the build process goes smoothly.

Note: When locally building your plugin it will be placed into a folder called 'out' this is different from the concept described above.

The out folder is not sent to the final plugin, but is then put into a ``bin`` folder which is found at the root of the plugin's directory.  
More information on the bin folder can be found below in the distribution section below.

### Distribution

We recommend following the instructions found in the [decky-plugin-database](https://github.com/SteamDeckHomebrew/decky-plugin-database) on how to get your plugin up on the plugin store. This is the best way to get your plugin in front of users.
You can also choose to do distribution via a zip file containing the needed files, if that zip file is uploaded to a URL it can then be downloaded and installed via decky-loader.

**NOTE: We do not currently have a method to install from a downloaded zip file in "game-mode" due to lack of a usable file-picking dialog.**

Layout of a plugin zip ready for distribution:
```
pluginname-v1.0.0.zip (version number is optional but recommended for users sake)
   |
   pluginname/ <directory>
   |  |  |
   |  |  bin/ <directory> (optional)
   |  |     |
   |  |     binary (optional)
   |  |
   |  dist/ <directory> [required]
   |      |
   |      index.js [required]
   | 
   package.json [required]
   plugin.json [required]
   main.py {required if you are using the python backend of decky-loader: serverAPI}
   README.md (optional but recommended)
   LICENSE(.md) [required, filename should be roughly similar, suffix not needed]
```

Note regarding licenses: Including a license is required for the plugin store if your chosen license requires the license to be included alongside usage of source-code/binaries!

Standard procedure for licenses is to have your chosen license at the top of the file, and to leave the original license for the plugin-template at the bottom. If this is not the case on submission to the plugin database, you will be asked to fix this discrepancy.

We cannot and will not distribute your plugin on the Plugin Store if it's license requires it's inclusion but you have not included a license to be re-distributed with your plugin in the root of your git repository.

## Development
This section is based on the rewritten readme from [ryzenadj-decky-plugin](https://github.com/XanderXAJ/ryzenadj-decky-plugin/blob/main/README.md).

- [Plugin development wiki](https://wiki.deckbrew.xyz/en/user-guide/home#plugin-development)
- [decky-frontend-lib](https://github.com/SteamDeckHomebrew/decky-frontend-lib) provides React components for usage in the frontend
- [decky-loader] handles plugin loading -- it can be useful to look at its source code to see what's going on
- [decky-plugin-database] allows the plugin to be installed from Loader's built-in store
- [decky-plugin-template] from which this plugin is derived
- [React TypeScript Cheatsheets](https://react-typescript-cheatsheet.netlify.app/) has lots of useful info for developing the frontend

[decky-plugin-database]: https://github.com/SteamDeckHomebrew/decky-plugin-database
[decky-plugin-template]: https://github.com/SteamDeckHomebrew/decky-plugin-template

### Building and testing the plugin

This plugin uses scripts modified from the [decky-plugin-template], which target the VSCode family of editors.

To see the available tasks, run the `Tasks: Run Task` action, or open [`/.vscode/tasks.json`](/.vscode/tasks.json).

#### Initial setup

Since SSH is used to deploy the plugin, your Steam Deck also requires initial configuration:

1. Set a user password by running:

   ```shell
   passwd
   ```

   Follow the prompts and remember the password.

2. Enable the SSH daemon to allow logins over SSH:

   ```shell
   sudo systemctl enable sshd.service
   sudo systemctl start sshd.service
   ```

3. SSH is now enabled and running.
   If you're unsure how to SSH to the Deck, [follow these instructions][deck-ssh].

If SSH is not working at this point, [see these additional instructions][deck-ssh].

The supplied VSCode family build tasks require initial configuration:

1. Copy [`/.vscode/defsettings.json`](/.vscode/defsettings.json) to [`/.vscode/settings.json`](/.vscode/settings.json).
2. Update the new [`/.vscode/settings.json`](/.vscode/settings.json) file to match your Deck, including the Deck's current IP in `deckip` and your Deck's user password (the one you use with `sudo`, not your Steam account) in `deckpass`.
    - Alternatively, create a `deck` entry in your `~/.ssh/config` and set your `deckip` to `deck`.
        This means you can both run the deploy tasks and SSH directly to the Deck while only have one location to update.
        ```
        Host deck
            HostName 0.0.0.0
        ```

[deck-ssh]: https://gist.github.com/andygeorge/eee2825fa6446b629745ea92e862593a

#### Deploying a change

Go through the following every time you make a change:

1. In VSCode, run the `Tasks: Run Build Task` action.
   Under the hood, this runs the `builddeploy` task to both build and deploy the plugin to Deck.
2. Observe the output pane for any errors.

#### Other important information

If you are receiving build errors due to an out of date library, you should run this command inside of your repository:

```bash
pnpm update decky-frontend-lib --latest
```

### Backend build

This plugin is currently not suppling a backend binary.

### Enable live reloading of plugins

Decky Loader can live reload plugins but the functionality is disabled by default.

To enable live reloading on Steam Deck/Linux, we'll add the needed environment variable to Decky's `plugin_loader` service:

1. Run:

   ```shell
   sudo systemctl edit plugin_loader.service
   ```

   This creates an override file where we can add an environment variable.

2. Add the following in between the comments:

   ```shell
   Environment=LIVE_RELOAD=1
   ```

   It'll look something like this when done:

   ```
   ### Editing /etc/systemd/system/plugin_loader.service.d/override.conf
   ### Anything between here and the comment below will become the new contents of the file

   Environment=LIVE_RELOAD=1

   ### Lines below this comment will be discarded
   # ...
   ```

3. Either restart the service or restart the Deck/machine to load the new environment variable:

   ```shell
   # Restart the service
   sudo systemctl restart plugin_loader.service
   # OR: Restart the Deck
   sudo reboot
   ```

Note: It takes a few moments to detect changes have occurred.
Additionally, it'll only hot reload if your plugin is currently not being displayed.
If your plugin hasn't live reloaded, try closing your plugin's UI.

Technical Note: Strictly speaking, the `LIVE_RELOAD` environment variable only affects the frontend code -- backend code is always hot reloaded.

### Debugging using CEF debugging

[Follow these instructions.](https://docs.deckthemes.com/CSSLoader/Cef_Debugger/)

### Debugging using `console.log()` etc.

1. Follow _Debugging using CEF debugging_.
2. Inspect the `SharedJSContext` target.
3. In the new window, ensure the Console is open. See your logging messages.

### Debugging using React DevTools

Run [the standalone version of React DevTools](https://github.com/facebook/react/tree/main/packages/react-devtools), e.g.:

```shell
npx react-devtools
```

Then enter your machine's IP address (helpfully displayed by React DevTools) in to Decky Loader's developer settings.

Note: _enter only the IP address_ -- don't be smart like me and also enter the port number or protocol.

To find the plugin's components, since the core components of this plugin are prefixed with `RyzenAdj`, use the search bar to search for `RyzenAdj` and find them.

### Debugging the Python Plugin Loader backend

Plugin loader is the component that loads plugins (oddly enough).
See its logs by running:

```shell
journalctl -u plugin_loader -b0
```
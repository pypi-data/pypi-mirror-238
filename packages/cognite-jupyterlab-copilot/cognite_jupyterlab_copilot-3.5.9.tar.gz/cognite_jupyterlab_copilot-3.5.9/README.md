# cognite_jupyterlab_copilot

A JupyterLab extension .

## Requirements

- JupyterLab = 3.5.3 # match jupyterlab versions across tooling

## Install

To install the extension, execute:

```bash
pip install cognite_jupyterlab_copilot
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall cognite_jupyterlab_copilot
```

## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

#### [Conda]

A sandboxed virtual python environment [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).
Is strongly recommended, just after running

```bash
conda create -n my_happy_conva_env -c conda-forge jupyterlab=3.5.3 jupyterlite-core
conda activate my_happy_conva_env
```

your life will be easier in every way.

#### jlpm

The `jlpm` command is JupyterLab's pinned version of [yarn](https://yarnpkg.com/) that is installed with JupyterLab. `jlpm` will work right away if you used `conda`.

```bash
# Clone the repo to your local environment
# Change directory to the cognite_jupyterlab_copilot directory
# Install package in development mode
pip install -e "."
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
pip uninstall cognite_jupyterlab_copilot
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `cognite_jupyterlab_copilot` within that folder.

### [Cognite SDK](https://github.com/cognitedata/fusion) Token

If you have trouble getting an auth token try adding something like this to `auth.ts`:

```javascript
  // localdev in raw jupyter lab
  if (window.location.hostname === 'localhost') {
    resolve(
      new CogniteClient({
        appId: 'LLM-hub-server',
        project: 'lervik-industries', // <-- your project name here
        baseUrl: 'https://api.cognitedata.com', // <-- your API endpoint here
        getToken: async () =>
          // "imma dangerous secret token"
      })
    );
  }
```

## Testing the extension

#### Frontend tests

This extension is using [Jest](https://jestjs.io/) for JavaScript code testing.

To execute them, execute:

```sh
jlpm
jlpm test
```

#### Integration tests

This extension uses [Playwright](https://playwright.dev/docs/intro) for the integration tests (aka user level tests).
More precisely, the JupyterLab helper [Galata](https://github.com/jupyterlab/jupyterlab/tree/master/galata) is used to handle testing the extension in JupyterLab.

More information are provided within the [ui-tests](./ui-tests/README.md) README.

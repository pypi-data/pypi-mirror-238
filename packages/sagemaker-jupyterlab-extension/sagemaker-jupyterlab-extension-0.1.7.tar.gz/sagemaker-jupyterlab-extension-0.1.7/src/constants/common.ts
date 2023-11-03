const pluginIds = {
  ExamplePlugin: '@amzn/sagemaker-jupyterlab-extensions:example',
  HideShutDownPlugin: '@amzn/sagemaker-jupyterlab-extensions:hideshutdown',
  SessionManagementPlugin: '@amzn/sagemaker-jupyterlab-extensions:sessionmanagement',
  ResourceUsagePlugin: '@amzn/sagemaker-jupyterlab-extensions:resourceusage',
  GitClonePlugin: '@amzn/sagemaker-jupyterlab-extensions:gitclone',
};

const JUPYTER_COMMAND_IDS = {
  mainMenu: {
    fileMenu: {
      shutdown: 'filemenu:shutdown',
    },
  },
  gitClone: 'git:clone',
  createTerminal: 'terminal:create-new',
  openDocManager: 'docmanager:open',
  goToPath: 'filebrowser:go-to-path',
};

const RESOURCE_PLUGIN_ID = '@amzn/sagemaker-jupyterlab-extensions:resourceusage:resource-usage-widget';

const i18nStrings = {};

export { pluginIds, i18nStrings, JUPYTER_COMMAND_IDS, RESOURCE_PLUGIN_ID };

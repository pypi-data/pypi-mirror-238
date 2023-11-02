import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IFileBrowserFactory, IDefaultFileBrowser } from '@jupyterlab/filebrowser';
import { JUPYTER_COMMAND_IDS, pluginIds, ErrorMessages } from '../constants';
import { GitCloneWidget } from './../widgets/GitCloneWidget';
import { Dialog, showErrorMessage } from '@jupyterlab/apputils';
import { ITranslator, TranslationBundle, nullTranslator } from '@jupyterlab/translation';
import * as styles from './../widgets/styles/gitCloneStyles';
import { il18Strings } from './../constants/il18Strings';
import { getLoggerForPlugin } from '../utils/logger';
import {
  strHasLength,
  validCloneUrl,
  getRepoName,
  checkCloneDirectoryStatus,
  CloneDirectoryStatus,
  gitCloneInTerminal,
  AdditionalGitCloneOptions,
  handleAdditionalCloneOptions,
} from './../utils/gitCloneUtils';
import { PathExt } from '@jupyterlab/coreutils';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { Menu } from '@lumino/widgets';
import { ILogger } from '@amzn/sagemaker-jupyterlab-extension-common';
import { CommandRegistry } from '@lumino/commands';
import { Contents } from '@jupyterlab/services';

const { dialogTitle, cancelButton, cloneButton, errors } = il18Strings.GitClone;

/**
 * Function to execute when addCommand is executed for gitClone
 * @param factory
 * @param contents
 * @param commands
 * @returns
 */
const executeGitCloneCommand = async (
  factory: IFileBrowserFactory,
  defaultFileBrowser: IDefaultFileBrowser,
  contents: Contents.IManager,
  commands: CommandRegistry,
  logger: ILogger,
) => {
  const fileBrowserModel = defaultFileBrowser.model;

  // Process args
  let URL = '';
  const cwd = factory?.tracker?.currentWidget?.model.path;
  let path: string = cwd ?? '';
  let openREADME = true;
  let findEnvironment = true;
  let result;
  const dialog = new Dialog({
    title: dialogTitle,
    body: new GitCloneWidget(),
    focusNodeSelector: 'input',
    buttons: [Dialog.cancelButton({ label: cancelButton }), Dialog.okButton({ label: cloneButton })],
    hasClose: false,
  });
  dialog.addClass(styles.increaseZIndex);

  try {
    result = await dialog.launch();
  } catch (error) {
    logger.error({
      Message: ErrorMessages.GitClone.Dialog,
      Error: error as Error,
    });
    return;
  }

  if (!(result.button.accept && result.value)) {
    return;
  }

  ({ URL, path, openREADME, findEnvironment } = result.value as any);

  // Prepare data
  if (!strHasLength(path)) {
    path = './';
  }
  // if URL is invalid display error message and do not continue
  if (!validCloneUrl(URL)) {
    await showErrorMessage(errors.invalidCloneUrlTitle, {
      message: errors.invalidCloneUrlBody,
    });
    return;
  }
  const repoName = getRepoName(URL);
  const repoPath = PathExt.join(path, repoName);
  let cloneDirectoryStatus;
  try {
    // removed studioLogger that is being passed
    cloneDirectoryStatus = await checkCloneDirectoryStatus(contents as any, path, URL, repoPath);
  } catch (error) {
    logger.error({
      Message: ErrorMessages.GitClone.ValidRepoPathError,
      Error: new Error(JSON.stringify(error)),
    });
  }
  // Git clone
  const additionalOptions = { repoPath, openREADME, findEnvironment };
  if (cloneDirectoryStatus === CloneDirectoryStatus.CanClone) {
    // Clone Repo Attempt
    // removed studio logger - need to add in logger
    gitCloneInTerminal(
      commands as any,
      contents as any,
      additionalOptions as AdditionalGitCloneOptions,
      fileBrowserModel,
      path as string,
      URL,
    );
  } else if (cloneDirectoryStatus === CloneDirectoryStatus.AlreadyCloned) {
    // If already cloned, only handle additional options (for example, find&build env or open README)
    handleAdditionalCloneOptions(commands as any, contents as any, additionalOptions as AdditionalGitCloneOptions);
  }
};

const addCloneButtonFunction = (
  factory: IFileBrowserFactory,
  app: JupyterFrontEnd,
  mainMenu: IMainMenu,
  trans: TranslationBundle,
) => {
  // Currently, we JL4 does not support jupyterlab-git extension.
  // We manually add Menu item for Git clone dialog.
  // After jupyterlab-git adds JL4 support, we will refactor this logic
  // to use Menu item provided by jupyterlab-git.
  // addCloneButton(gitExtension, factory.defaultBrowser, app.commands as any, trans);
  const gitMenu = new Menu({ commands: app.commands });
  gitMenu.title.label = trans.__('Git');
  gitMenu.addItem({ command: JUPYTER_COMMAND_IDS.gitClone });
  mainMenu.addMenu(gitMenu);
};

/**
 * Plugin to replace the defaukt git clone repo feature
 */
const GitClonePlugin: JupyterFrontEndPlugin<void> = {
  id: pluginIds.GitClonePlugin,
  requires: [IFileBrowserFactory, IDefaultFileBrowser, IMainMenu, ILogger, ITranslator],
  autoStart: true,
  activate: async (
    app: JupyterFrontEnd,
    factory: IFileBrowserFactory,
    defaultFileBrowser: IDefaultFileBrowser,
    mainMenu: IMainMenu,
    baseLogger: ILogger,
    translator: ITranslator,
  ) => {
    const { commands, serviceManager } = app;
    const contents = serviceManager.contents;
    const logger = getLoggerForPlugin(baseLogger, pluginIds.GitClonePlugin);
    translator = translator || nullTranslator;

    // A translation bundle is required for 'addCloneButton' and 'addFileBrowserContextMenu' functions
    const trans = translator.load('sagemaker_studio');

    commands.addCommand(JUPYTER_COMMAND_IDS.gitClone, {
      label: 'Git Clone Repo',
      caption: '',
      execute: () => executeGitCloneCommand(factory, defaultFileBrowser, contents, commands, logger),
      isEnabled: () => app.serviceManager.terminals.isAvailable(),
    });
    addCloneButtonFunction(factory, app, mainMenu, trans);

    // Added for testing purpose
    logger.info({ Message: 'Successfully loaded Git extension' });
  },
};

export { GitClonePlugin, executeGitCloneCommand, addCloneButtonFunction };

import { JupyterFrontEnd } from '@jupyterlab/application';
import { GitClonePlugin, executeGitCloneCommand, addCloneButtonFunction } from '../GitClonePlugin';
import { IDefaultFileBrowser, IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { ITranslator, TranslationBundle } from '@jupyterlab/translation';
import { JUPYTER_COMMAND_IDS } from '../../constants';
import { ContentsManager, ServerConnection } from '@jupyterlab/services';
import { gitCloneRepoMock } from '../../service/__tests__/mock';
import { mockLogger } from '../../utils/__mocks__/logger.spec';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { ILogger } from '@amzn/sagemaker-jupyterlab-extension-common';

const mockLogger: ILogger = {
  error: jest.fn(),
  info: jest.fn(),
  child: jest.fn(() => mockLogger),
};

jest.mock('@jupyterlab/filebrowser', () => jest.fn as jest.Mock);
jest.mock('@jupyterlab/translation', () => jest.fn as jest.Mock);

jest.mock('@jupyterlab/services', () => {
  const module = jest.requireActual('@jupyterlab/services');
  return {
    ...module,
    ServerConnection: {
      ...module.ServerConnection,
      makeRequest: jest.fn(),
      makeSettings: jest.fn(() => {
        return {
          settings: {
            baseUrl: '',
          },
        };
      }),
    },
  };
});

describe('Git clone plgin suite', () => {
  const mockServerConnection = ServerConnection.makeRequest as jest.Mock;

  it('Should test the activate function of the git clone plugin', async () => {
    // jest.spyOn(addCloneButton);
    const transBundleMock: TranslationBundle = {
      __: jest.fn((str) => str),
    } as TranslationBundle;
    const transMock: ITranslator = {
      load: jest.fn(() => transBundleMock),
    } as ITranslator;
    const mockFactory: IFileBrowserFactory = jest.fn();
    const mockDefaultFileBrowser: IDefaultFileBrowser = jest.fn();
    const appMock = {
      commands: {
        addCommand: jest.fn(),
      },
      serviceManager: {
        contents: jest.fn(),
      },
    } as JupyterFrontEnd;

    const mainMenuMock: IMainMenu = {
      addMenu: jest.fn(),
    } as IMainMenu;

    const mockExecute = jest.fn();
    appMock.commands.addCommand(JUPYTER_COMMAND_IDS.gitClone, {
      label: '',
      caption: '',
      execute: mockExecute,
      isEnabled: jest.fn(),
    });

    addCloneButtonFunction(mockFactory, appMock, mainMenuMock, transBundleMock);
    await GitClonePlugin.activate(appMock, mockFactory, mockDefaultFileBrowser, mainMenuMock, mockLogger, transMock);
    expect(appMock.commands.addCommand).toHaveBeenCalledTimes(2);
  });

  xit('should be able to run the Execute command', async () => {
    jest.useFakeTimers('legacy');
    const ResponseMock = jest.fn((status, data) => ({
      status,
      ok: 200 <= status && status < 300 && Number.isInteger(status),
      json: () => {
        return Promise.resolve(data);
      },
    }));
    mockServerConnection.mockImplementation(async () => {
      return ResponseMock(200, gitCloneRepoMock);
    });
    jest.useFakeTimers();

    const mockFactory: IFileBrowserFactory = {
      defaultBrowser: {
        model: jest.fn(),
      },
    };
    const contentMock: ContentsManager = jest.fn();
    const commands: any = jest.fn();

    // jest.setTimeout(10000);
    try {
      await executeGitCloneCommand(mockFactory, jest.fn(), contentMock, commands, mockLogger);
    } catch (error) {
      // eslint-disable-next-line no-console
      console.log(error);
    }
    jest.runAllTimers();
  });
});

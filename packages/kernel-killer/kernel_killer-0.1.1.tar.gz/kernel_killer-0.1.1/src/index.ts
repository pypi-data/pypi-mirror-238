import {
  ILabShell,
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  JupyterLab
} from '@jupyterlab/application';

import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
import { ICommandPalette, showDialog } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import { ITranslator } from '@jupyterlab/translation';
import { Widget } from '@lumino/widgets';

//import type { IRetroShell } from '@retrolab/application';

// ...

const extension: JupyterFrontEndPlugin<void> = {
  id: 'kernel-killer',
  autoStart: true,
  optional: [ILauncher],
  requires: [ICommandPalette, ITranslator],
  activate: async (
    app: JupyterFrontEnd,
    lab: JupyterLab,
    translator: ITranslator,
    palette: ICommandPalette,
    launcher: ILauncher | null
  ) => {
    const shell = app.shell as ILabShell;
    const trans = translator.load('jupyterlab');
    shell.currentChanged.connect(async (_: any, change: any) => {
      console.log(change);
      if (
        change?.oldValue?.constructor?.name === 'NotebookPanel' &&
        change?.oldValue?.context._isDisposed
      ) {
        console.log('é pra fechar');
        console.log('windows');
        const setting = ServerConnection.makeSettings();
        const apiURL = URLExt.join(setting.baseUrl, 'api/shutdown');
        await Promise.all([
          app.serviceManager.sessions.shutdownAll(),
          app.serviceManager.terminals.shutdownAll()
        ]);
        console.log('matou..?');
        return ServerConnection.makeRequest(apiURL, { method: 'POST' }, setting)
          .then(result => {
            if (result.ok) {
              // Close this window if the shutdown request has been successful
              const body = document.createElement('div');
              const p1 = document.createElement('p');
              p1.textContent = trans.__(
                'You have shut down the Jupyter server. You can now close this tab.'
              );
              const p2 = document.createElement('p');
              p2.textContent = trans.__(
                'To use JupyterLab again, you will need to relaunch it.'
              );

              body.appendChild(p1);
              body.appendChild(p2);
              void showDialog({
                title: trans.__('Server stopped'),
                body: new Widget({ node: body }),
                buttons: []
              });
              window.close();
            } else {
              throw new ServerConnection.ResponseError(result);
            }
          })
          .catch(data => {
            throw new ServerConnection.NetworkError(data);
          });
        //;
        //$ jupyter notebook stop 8888
        //
      }
      // ...
    });
  }
};

export default extension;

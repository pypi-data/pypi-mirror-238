import { CogniteClient } from '@cognite/sdk';

let _client: CogniteClient | undefined;

export const getSdkClient = () =>
  new Promise<CogniteClient>(resolve => {
    if (_client) {
      return resolve(_client)
    }

    // handle 'getToken' response from parent window
    window.addEventListener(
      'message',
      (event: MessageEvent) => {
        if (
          typeof event.data === 'object' &&
          'token' in event.data &&
          'baseUrl' in event.data &&
          'project' in event.data
        ) {
          const { token, baseUrl, project } = event.data;

          _client = new CogniteClient({
            appId: 'LLM-hub-server',
            project,
            baseUrl,
            getToken: async () => token
          })
          _client.authenticate();
          resolve(_client);
        }
      },
      { capture: false, once: true }
    );
    window?.top?.postMessage('getToken', '*');
  });

export const track = (eventName: string, data: any = {}) => {
  window.parent.postMessage(
    {
      event: 'NotebookCopilotEvent',
      data: { eventName, data }
    },
    '*'
  );
};

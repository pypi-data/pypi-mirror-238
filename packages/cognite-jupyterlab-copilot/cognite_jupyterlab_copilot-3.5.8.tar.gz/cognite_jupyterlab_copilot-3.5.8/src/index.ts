import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';
import { INotebookTracker } from '@jupyterlab/notebook';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { LabIcon } from '@jupyterlab/ui-components';
import { Widget } from '@lumino/widgets';

import ai_icon_svg from '../assets/LogoAi.svg';
import { CopilotWidget } from './components/CopilotWidget';
import { getSdkClient } from './lib/auth';
import { track } from './lib/track';

export const aiIcon = new LabIcon({
  name: 'cognite_jupyterlab_copilot:cognite_icon',
  svgstr: ai_icon_svg
});

export namespace CommandIDs {
  export const openCopilotDropdown = 'jupyterlab:open-copilot-dropdown-menu';
}

/**
 * A plugin that enables Copilot AI commands in from notebook cell toolbars
 */
export const cogniteCopilotPlugin: JupyterFrontEndPlugin<void> = {
  id: 'cognite_jupyterlab_copilot:button_plugin',
  autoStart: true,
  requires: [INotebookTracker, IThemeManager],
  optional: [ISettingRegistry],
  activate: async (app: JupyterFrontEnd, nbTracker: INotebookTracker) => {
    const aiDisabled = new URLSearchParams(window.location.search).has(
      'aiDisabled'
    );
    if (aiDisabled) {
      // we will still allow the plugin to be loaded and the widget opened. in the aiDisabled case those menu items will be disabled;
      track('DisableCopilotPlugin');
    } else {
      // lazy load the Cognite SDK
      getSdkClient();
    }

    app.commands.addCommand(CommandIDs.openCopilotDropdown, {
      label: 'Copilot',
      execute: () => {
        const widget: any = CopilotWidget({
          nbTracker,
          aiDisabled
        });
        Widget.attach(widget, document.body);
        track('OpenCopilotWidget');

        // close the menu when clicking outside of it
        const handleBodyClick = (event: MouseEvent) => {
          const targetEle = event.target as HTMLElement;
          const isWidgetClick =
            targetEle.closest('#copilot_main_menu') ||
            targetEle.closest('#copilot_generator_menu') ||
            targetEle.closest('#copilot_explainer_menu');
          if (!isWidgetClick) {
            track('CancelCopilotWidget');
            widget.dispose();
            document.body.removeEventListener('mouseup', handleBodyClick);
          }
        };
        document.body.addEventListener('mouseup', handleBodyClick);
      }
    });

    console.log(
      'JupyterLab extension cognite_jupyterlab_copilot is activated!'
    );
  }
};

export default cogniteCopilotPlugin;

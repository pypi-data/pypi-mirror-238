import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { INotebookTracker, NotebookActions } from '@jupyterlab/notebook';
import { Button, Flex, Icon } from '@cognite/cogs.js';
import { CodeExplainFlow, useCopilotContext } from '@cognite/copilot-core';
import useCogniteSDK from '../lib/hooks/useCogniteSDK';
import { track } from '../lib/track';
import { secondsSince } from '../lib/helpers';
import { StyledContainer, StyledIcon } from './styled-components';
import { LoadingAnimation } from './LoadingAnimation';

export const CodeExplainerPanel = ({
  nbTracker,
  onClose
}: {
  nbTracker: INotebookTracker;
  onClose: () => void;
}) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [codeExplanation, setCodeExplanation] = useState('');
  const [periods, setPeriods] = useState('');

  const startTime = useMemo(() => Date.now(), []);

  // rendering a growing string of ellipses while loading
  useEffect(() => {
    const interval = setInterval(() => {
      setPeriods(periods + (periods.length % 4 === 0 ? ' ' : '.'));
    }, 100);
    return () => clearInterval(interval);
  }, [periods]);

  const sdk: any = useCogniteSDK();

  const { registerFlow, runFlow } = useCopilotContext();
  const explainerFlow = useMemo(
    () => sdk && new CodeExplainFlow({ sdk }),
    [sdk]
  );

  useEffect(() => {
    if (!explainerFlow) {
      return;
    }

    const code = nbTracker!.activeCell!.model.value.text;
    track('CodeExplainer.Request', { code });
    setIsGenerating(true);

    const unregisterFunction = registerFlow({ flow: explainerFlow });
    if (code?.trim()) {
      runFlow(explainerFlow, { code }).then(response => {
        track('ReceiveExplainCodeResponse', {
          code,
          response,
          responseSeconds: secondsSince(startTime)
        });
        setCodeExplanation(response.content);
        setIsGenerating(false);
      });
    } else {
      setCodeExplanation('This code cell is empty.');
      setIsGenerating(false);
    }
    return unregisterFunction;
  }, [explainerFlow, registerFlow]);

  const handleAddMarkdownClick = useCallback(() => {
    // insert a new cell below the current cell
    NotebookActions.insertBelow(nbTracker.currentWidget!.content);

    // configure and render the new cell
    const notebook = nbTracker.currentWidget!.content;
    NotebookActions.changeCellType(notebook, 'markdown');
    notebook.activeCell!.model.value.text = codeExplanation;
    NotebookActions.renderAllMarkdown(notebook);

    onClose();
  }, [codeExplanation, nbTracker, onClose]);

  const handleClose = useCallback(() => {
    isGenerating &&
      track('CodeExplainer.Cancel', {
        code: nbTracker!.activeCell!.model.value.text,
        hangSeconds: secondsSince(startTime)
      });
    onClose();
  }, [nbTracker, isGenerating, onClose]);

  return (
    <StyledContainer>
      <Flex direction="column">
        <Flex direction="row" justifyContent="space-between">
          <StyledIcon type="LightBulb" size={36} />
          <div
            style={{
              marginLeft: 8,
              flexGrow: 1,
              maxWidth: 230,
              maxHeight: '40vh',
              overflowY: 'scroll'
            }}
          >
            {isGenerating ? periods : codeExplanation}
          </div>
        </Flex>
        <Flex
          direction="row"
          style={{ marginTop: 16 }}
          justifyContent="space-between"
        >
          <Button
            type="secondary"
            size="large"
            style={{ flexGrow: 1, marginRight: 8 }}
            onClick={handleClose}
          >
            {isGenerating ? 'Cancel' : 'OK'}
          </Button>
          {isGenerating ? (
            <Button
              type="primary"
              size="large"
              style={{
                color: '#fff',
                background: '#b79df1',
                width: 136
              }}
              disabled={isGenerating}
            >
              <span>Generating</span>
              <LoadingAnimation style={{ height: 16, marginLeft: 8 }} />
            </Button>
          ) : (
            <Button
              type="primary"
              size="large"
              style={{
                color: '#fff',
                background: '#6F3BE4',
                width: 185
              }}
              disabled={isGenerating}
              onClick={handleAddMarkdownClick}
            >
              <Icon type="Plus" size={24} />
              <span style={{ whiteSpace: 'nowrap' }}>Add as markdown</span>
            </Button>
          )}
        </Flex>
      </Flex>
    </StyledContainer>
  );
};

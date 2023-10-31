import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { Cell } from '@jupyterlab/cells';
import { INotebookTracker } from '@jupyterlab/notebook';
import { Button, Flex } from '@cognite/cogs.js';
import { CodeExplainFlow, useCopilotContext } from '@cognite/copilot-core';
import { CogniteClient } from '@cognite/sdk';
import { secondsSince } from '../../lib/helpers';
import useCogniteSDK from '../../lib/hooks/useCogniteSDK';
import { track } from '../../lib/track';
import { StyledContainer, StyledIcon } from '../styled-components';

export const CodeGeneratorAcceptRejectPanel = ({
  generatedCode,
  nbTracker,
  onClose,
  priorCellState,
  prompt
}: {
  generatedCode: { content: string };
  nbTracker: INotebookTracker;
  onClose: () => void;
  priorCellState: string;
  prompt: string;
}) => {
  const [codeSummary, setCodeSummary] = useState<string>();
  const [isSummarizing, setIsSummarizing] = useState(true);
  const [periods, setPeriods] = useState('');

  const startTime = useMemo(() => Date.now(), []);

  const { registerFlow, runFlow } = useCopilotContext();
  const sdk: CogniteClient | undefined = useCogniteSDK();
  const explainerFlow = useMemo(
    () => sdk && new CodeExplainFlow({ sdk }),
    [sdk]
  );

  useEffect(() => {
    if (!generatedCode?.content?.trim()) {
      return;
    }
    if (!explainerFlow) {
      return;
    }

    // fetch a gpt summary of the generated code
    const code = generatedCode.content;
    const flow = explainerFlow as CodeExplainFlow;
    const unregisterFunction = registerFlow({ flow });
    runFlow(flow, { code }).then(response => {
      track('CodeExplainer.Response', {
        code,
        response,
        responseSeconds: secondsSince(startTime)
      });
      setCodeSummary(response.content);
      setIsSummarizing(false);
    });
    return unregisterFunction;
  }, [explainerFlow, generatedCode]);

  // rendering a growing string of ellipses while loading
  useEffect(() => {
    const interval = setInterval(() => {
      setPeriods(periods + (periods.length % 4 === 0 ? ' ' : '.'));
    }, 100);
    return () => clearInterval(interval);
  }, [periods]);

  const handleAccept = useCallback(() => {
    track('CodeGeneration.Accept', {
      codeSummary,
      generatedCode,
      priorCellState,
      prompt
    });
    onClose();
  }, [codeSummary, generatedCode, onClose, priorCellState, prompt]);

  const handleReject = useCallback(() => {
    track('CodeGeneration.Reject', {
      codeSummary,
      generatedCode,
      priorCellState,
      prompt
    });
    // revert cell text to its prior state
    const cell: Cell = nbTracker!.activeCell!;
    cell.model.value.text = priorCellState;
    onClose();
  }, [codeSummary, generatedCode, onClose, priorCellState, prompt]);

  return (
    <StyledContainer>
      <Flex direction="column">
        <Flex direction="row" justifyContent="space-between">
          <StyledIcon type="Code" size={36} />
          <div
            style={{
              marginLeft: 8,
              flexGrow: 1,
              maxWidth: 230,
              maxHeight: '40vh',
              overflowY: 'scroll'
            }}
          >
            {isSummarizing ? 'Summarizing ... ' + periods : codeSummary}
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
            style={{ width: 136 }}
            onClick={handleReject}
          >
            Reject
          </Button>
          <Button
            type="primary"
            size="large"
            style={{
              color: '#fff',
              background: '#6F3BE4',
              width: 136
            }}
            icon="Checkmark"
            iconPlacement="right"
            onClick={handleAccept}
          >
            Accept
          </Button>
        </Flex>
      </Flex>
    </StyledContainer>
  );
};

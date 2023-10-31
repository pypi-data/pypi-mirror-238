import React, {
  useState,
  useCallback,
  useEffect,
  useMemo,
  useRef
} from 'react';
import { INotebookTracker, Notebook } from '@jupyterlab/notebook';
import { Cell } from '@jupyterlab/cells';
import { CodeGenerateFlow, useCopilotContext } from '@cognite/copilot-core';
import { Button, Flex, Textarea } from '@cognite/cogs.js';
import { CogniteClient } from '@cognite/sdk';
import useCogniteSDK from '../../lib/hooks/useCogniteSDK';
import { track } from '../../lib/track';
import { secondsSince } from '../../lib/helpers';
import { StyledContainer, StyledIcon } from '../styled-components';
import { LoadingAnimation } from '../LoadingAnimation';
import { CodeGeneratorAcceptRejectPanel } from './CodeGeneratorAcceptRejectPanel';

export const CodeGeneratorInputPanel = ({
  nbTracker,
  onClose
}: {
  nbTracker: INotebookTracker;
  onClose: () => void;
}) => {
  const [inputValue, setInputValue] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [lastResponse, setLastResponse] = useState<any>();
  const [showAcceptRejectpanel, setShowAcceptRejectPanel] = useState(false);
  const [generateStartTime, setGenerateStartTime] = useState<number>(0);
  const inputElementRef = useRef();

  // auto-focus the input (autoFocus attr not supported by cogs.js::Textarea)
  useEffect(() => {
    (inputElementRef?.current as any).focus();
  }, []);

  // setup business logic
  const sdk: CogniteClient | undefined = useCogniteSDK();
  const { registerFlow, runFlow } = useCopilotContext();
  const generateFlow = useMemo(
    () => sdk && new CodeGenerateFlow({ sdk }),
    [sdk]
  );

  useEffect(() => {
    if (generateFlow) {
      const unregisterGenerate = registerFlow({ flow: generateFlow });
      return unregisterGenerate;
    }
  }, [generateFlow, registerFlow]);

  // previous cell text will be sent to provide context along with the prompt
  const previousCells: string = useMemo(() => {
    const parent = nbTracker!.activeCell!.parent as Notebook;
    const cur_index = parent.activeCellIndex;
    const allCells = (parent.layout as any).widgets;
    return allCells
      .slice(0, cur_index)
      .map((c: Cell) => c.model.value.text)
      .join('\n');
  }, [nbTracker]);
  // also activeCell state before execution
  const priorCellState = useMemo(
    () => nbTracker.activeCell?.model.value.text as string,
    []
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent) => {
      setInputValue((e.target as HTMLInputElement).value);
    },
    [setInputValue]
  );

  const handleSubmit = useCallback(
    (e?: React.FormEvent) => {
      e?.preventDefault();

      const prompt = inputValue;
      track('CodeGeneration.Request', {
        previousCells,
        priorCellState,
        prompt
      });

      if (!generateFlow) {
        throw new Error('Something went wrong instantiating ``generateFlow``');
      }

      setGenerateStartTime(Date.now());
      setIsGenerating(true);

      runFlow(generateFlow, {
        prompt,
        previousCells: previousCells
      }).then((response: any) => {
        track('CodeGeneration.Response', {
          previousCells,
          priorCellState,
          prompt,
          response,
          responseSeconds: secondsSince(generateStartTime)
        });
        setLastResponse(response);
        // update cell text with generated code
        const cell: Cell = nbTracker!.activeCell!;
        cell.model.value.text = response.content;
        // open the accept/reject panel
        setShowAcceptRejectPanel(true);
      });
    },
    [generateFlow, inputValue, previousCells, priorCellState, runFlow]
  );

  // on ENTER keydown, submit (unless SHIFT is also pressed)
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.code === 'Enter' && !e.shiftKey) {
        handleSubmit();
      }
    },
    [generateFlow, handleSubmit]
  );

  const handleCancel = useCallback(() => {
    track('CodeGeneration.Cancel', {
      hangSeconds: secondsSince(generateStartTime),
      inputValue,
      previousCells,
      priorCellState
    });
    onClose();
  }, [inputValue, onClose, previousCells, priorCellState]);

  return (
    <>
      {showAcceptRejectpanel ? (
        <CodeGeneratorAcceptRejectPanel
          generatedCode={lastResponse}
          nbTracker={nbTracker}
          onClose={onClose}
          priorCellState={priorCellState}
          prompt={inputValue}
        />
      ) : (
        // Form for user input (GPT prompt)
        <StyledContainer>
          <Flex direction="column">
            <Flex direction="row" justifyContent="space-between">
              <StyledIcon type="Code" size={36} />
              <div style={{ flexGrow: 1, marginLeft: 8 }}>
                <Textarea
                  ref={inputElementRef as any}
                  placeholder="Write a prompt to generate code"
                  value={inputValue}
                  autoResize
                  disabled={isGenerating}
                  onChange={handleChange}
                  onKeyDown={handleKeyDown}
                />
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
                onClick={handleCancel}
              >
                Cancel
              </Button>
              <Button
                type="primary"
                size="large"
                style={{
                  color: '#fff',
                  background:
                    !inputValue || isGenerating ? '#b79df1' : '#6F3BE4',
                  width: 136
                }}
                disabled={!inputValue || isGenerating}
                onClick={handleSubmit}
              >
                {isGenerating ? (
                  <>
                    <span>Generating</span>
                    <LoadingAnimation style={{ height: 16, marginLeft: 8 }} />
                  </>
                ) : (
                  'Generate'
                )}
              </Button>
            </Flex>
          </Flex>
        </StyledContainer>
      )}
    </>
  );
};

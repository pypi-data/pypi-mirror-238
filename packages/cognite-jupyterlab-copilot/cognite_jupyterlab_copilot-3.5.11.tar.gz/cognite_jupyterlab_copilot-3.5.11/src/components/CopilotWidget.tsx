import React, { useCallback, useMemo, useState, useEffect } from 'react';
import { styled } from 'styled-components';
import { ReactWidget } from '@jupyterlab/apputils';
import { INotebookTracker } from '@jupyterlab/notebook';
import { Menu } from '@cognite/cogs.js';
import { Copilot } from '@cognite/copilot-core';
import useCogniteSDK from '../lib/hooks/useCogniteSDK';
import { track } from '../lib/track';
import { CodeGeneratorInputPanel } from './code-generator/CodeGeneratorInputPanel';
import { CodeExplainerPanel } from './CodeExplainerPanel';

/**
 * A Lumino ReactWidget that wraps a CopilotMenu.
 */
export const CopilotWidget: React.FC<any> = ({
  nbTracker
}: {
  nbTracker: INotebookTracker;
}): any => {
  return ReactWidget.create(
    <div
      id="copilot_widget_root"
      style={{
        position: 'relative',
        zIndex: 100,
        height: '100vh',
        width: '100vw',
        pointerEvents: 'none'
      }}
    >
      <CopilotMenu nbTracker={nbTracker} />
    </div>
  );
};

const CopilotMenu: React.FC<any> = ({
  nbTracker
}: {
  nbTracker: INotebookTracker;
}): JSX.Element => {
  const [showRootMenu, setShowRootMenu] = useState(true);
  const [showCodeGenerator, setShowCodeGenerator] = useState(false);
  const [showCodeExplainer, setShowCodeExplainer] = useState(false);

  const onGenerateCodeClick = useCallback(() => {
    track('CodeGeneration.Select');
    setShowRootMenu(false);
    setShowCodeGenerator(true);
  }, [setShowRootMenu, setShowCodeGenerator]);

  const onExplainCodeClick = useCallback(() => {
    track('CodeExplainer.Select');
    setShowRootMenu(false);
    setShowCodeExplainer(true);
  }, [setShowRootMenu, setShowCodeExplainer]);

  useEffect(() => {
    const closeMenuOnEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setShowRootMenu(false);
        setShowCodeGenerator(false);
        setShowCodeExplainer(false);
      }
    };
    document.addEventListener('keydown', closeMenuOnEscape);
    return () => {
      document.removeEventListener('keydown', closeMenuOnEscape);
    };
  }, []);

  // calculate MenuContainer position
  const { right, top } = useMemo(() => {
    const rect = nbTracker!.activeCell!.node.getBoundingClientRect();
    return {
      right: window.innerWidth - rect.width - rect.left + 187,
      top: rect.top
    };
  }, [nbTracker]);

  const sdk = useCogniteSDK();
  if (!sdk) {
    return <div></div>;
  }

  return (
    <Copilot showChatButton={false} sdk={sdk}>
      <div
        id="copilot_menu_root"
        style={{
          height: '100vh',
          width: '100vw',
          pointerEvents: 'none'
        }}
      >
        {showRootMenu && (
          <MenuContainer id="copilot_main_menu" $top={top} $right={right}>
            <Menu>
              <Menu.Header>Cognite AI</Menu.Header>
              <Menu.Item
                icon="Code"
                iconPlacement="left"
                onClick={onGenerateCodeClick} // TODO: figure out why tf onMouseUp doesn't work
              >
                Generate code
              </Menu.Item>
              <Menu.Item
                icon="LightBulb"
                iconPlacement="left"
                onClick={onExplainCodeClick}
              >
                Explain code
              </Menu.Item>
              <Menu.Item icon="Bug" iconPlacement="left" disabled>
                <FixCodeContainer>
                  Fix code
                  <ComingSoonTag>Coming soon</ComingSoonTag>
                </FixCodeContainer>
              </Menu.Item>
            </Menu>
          </MenuContainer>
        )}
        {showCodeGenerator && (
          <MenuContainer id="copilot_generator_menu" $top={top} $right={right}>
            <CodeGeneratorInputPanel
              nbTracker={nbTracker}
              onClose={() => setShowCodeGenerator(false)}
            />
          </MenuContainer>
        )}
        {showCodeExplainer && (
          <MenuContainer id="copilot_explainer_menu" $top={top} $right={right}>
            <CodeExplainerPanel
              nbTracker={nbTracker}
              onClose={() => setShowCodeExplainer(false)}
            />
          </MenuContainer>
        )}
      </div>
    </Copilot>
  );
};

const MenuContainer = styled.div<{ $top: number; $right: number }>`
  position: absolute;
  top: ${props => props.$top}px;
  right: ${props => props.$right}px;
  padding-top: 36px;
  pointer-events: auto;
`;

const ComingSoonTag = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  height: 20px;
  border-radius: 8px;
  border: 1px solid #e8e8e8;
  font-size: 11px;
  width: 92px;
  color: #696969;
  margin-left: 8px;
`;

const FixCodeContainer = styled.div`
  display: flex;
  align-items: center;
`;

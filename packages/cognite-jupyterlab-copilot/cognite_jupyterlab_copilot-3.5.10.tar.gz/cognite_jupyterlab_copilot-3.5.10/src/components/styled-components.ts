import styled from 'styled-components';
import { Icon } from '@cognite/cogs.js';

export const StyledContainer = styled.div`
  && {
    width: 312px;
    height: auto;
    overflow: auto;
    background: #fff;
    padding: 16px;
    border-radius: 10px;
    box-shadow:
      0px 1px 16px 4px rgba(79, 82, 104, 0.1),
      0px 1px 8px rgba(79, 82, 104, 0.08),
      0px 1px 2px rgba(79, 82, 104, 0.24);
  }
`;

export const StyledIcon = styled(Icon as any)`
  height: 36px;
  color: #6f3be4;
  background: #e9e1fb;
  padding: 8px;
  border-radius: 6px;
`;

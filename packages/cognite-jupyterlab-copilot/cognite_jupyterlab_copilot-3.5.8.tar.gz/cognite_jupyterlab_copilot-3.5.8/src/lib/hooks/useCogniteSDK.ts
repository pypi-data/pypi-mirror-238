import { useEffect, useState } from 'react';
import { CogniteClient } from '@cognite/sdk';
import { getSdkClient } from '../auth';

export default (): CogniteClient | undefined => {
  const [sdk, setSdk] = useState<CogniteClient>();
  useEffect(() => {
    getSdkClient().then(sdk => setSdk(sdk));
  }, []);
  return sdk;
}

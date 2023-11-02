import React, { useState, useMemo, ChangeEvent } from 'react';
import { NotebookPanel } from '@jupyterlab/notebook';
import { cx } from '@emotion/css';
import { FormControl, FormControlLabel, Radio, RadioGroup } from '@mui/material';
import { EmrClusterPluginClassNames } from '../constants/common';
import { Footer } from './Footer';
import { ClusterRowType, HandleConnectType, AuthType } from '../constants/types';

import styles from './styles';
import { i18nStrings } from '../constants/i18n';

interface SelectAuthTypeProps extends React.HTMLAttributes<HTMLElement> {
  readonly onCloseModal: () => void;
  readonly getConnectHandler: HandleConnectType;
  readonly selectedCluster: ClusterRowType | undefined;
  readonly notebookPanel?: NotebookPanel;
}

const SelectAuthType: React.FC<SelectAuthTypeProps> = ({
  onCloseModal,
  getConnectHandler,
  selectedCluster,
  notebookPanel,
}) => {
  const containerClasses = `${EmrClusterPluginClassNames.SelectAuthContainer}`;
  const modalBodyContainer = `${EmrClusterPluginClassNames.SelectAuthContainer}`;
  const [authType, setAuthType] = useState<AuthType>('Basic_Access');

  const onAuthTypeChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.value === 'Basic_Access' || e.target.value === 'None') {
      setAuthType(e.target.value);
    }
  };

  const onConnect = useMemo(() => {
    return getConnectHandler(onCloseModal, selectedCluster, authType, undefined, notebookPanel);
  }, [getConnectHandler, onCloseModal, selectedCluster, authType, notebookPanel]);

  return (
    <div className={cx(containerClasses, styles.ModalBase, styles.AuthModal)}>
      <div className={cx(modalBodyContainer, styles.ModalBody)}>
        <FormControl>
          <RadioGroup
            aria-labelledby="demo-radio-buttons-group-label"
            defaultValue="Basic_Access"
            value={authType}
            onChange={onAuthTypeChange}
            name="radio-buttons-group"
            data-testid="radio-button-group"
            row
          >
            <FormControlLabel
              value="Basic_Access"
              control={<Radio />}
              label={i18nStrings.Clusters.radioButtonLabels.basicAccess}
            />
            <FormControlLabel
              value="None"
              control={<Radio />}
              label={i18nStrings.Clusters.radioButtonLabels.noCredential}
            />
          </RadioGroup>
        </FormControl>
      </div>
      <Footer onCloseModal={onCloseModal} onConnect={onConnect} disabled={false} />
    </div>
  );
};

export { SelectAuthTypeProps, SelectAuthType };

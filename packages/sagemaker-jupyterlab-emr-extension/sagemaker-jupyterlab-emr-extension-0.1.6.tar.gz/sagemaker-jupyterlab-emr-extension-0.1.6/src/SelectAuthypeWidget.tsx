/* eslint-disable no-console */
import React from 'react';
import { Dialog } from '@jupyterlab/apputils';
import { NotebookPanel } from '@jupyterlab/notebook';
import { SelectAuthType } from './components/SelectAuthType';
import { ClusterRowType, HandleConnectType, ShowNotificationHandlerType } from './constants/types';

// @ts-ignore
class SelectAuthTypeWidget implements Dialog.IBodyWidget {
  readonly disposeDialog: ShowNotificationHandlerType;
  readonly handleConnect: HandleConnectType;
  readonly selectedCluster: ClusterRowType;
  readonly notebookPanel: NotebookPanel | undefined;

  constructor(
    disposeDialog: ShowNotificationHandlerType,
    handleConnect: HandleConnectType,
    selectedCluster: ClusterRowType,
    notebookPanel?: NotebookPanel,
  ) {
    this.disposeDialog = disposeDialog;
    this.handleConnect = handleConnect;
    this.selectedCluster = selectedCluster;
    this.notebookPanel = notebookPanel;
  }

  render() {
    return (
      <SelectAuthType
        onCloseModal={this.disposeDialog}
        getConnectHandler={this.handleConnect}
        selectedCluster={this.selectedCluster}
        notebookPanel={this.notebookPanel}
      />
    );
  }
}

const createSelectAuthTypeWidget = (
  disposeDialog: () => void,
  handleConnect: HandleConnectType,
  selectedCluster: ClusterRowType,
  notebookPanel?: NotebookPanel,
) => new SelectAuthTypeWidget(disposeDialog, handleConnect, selectedCluster, notebookPanel);

export { createSelectAuthTypeWidget };

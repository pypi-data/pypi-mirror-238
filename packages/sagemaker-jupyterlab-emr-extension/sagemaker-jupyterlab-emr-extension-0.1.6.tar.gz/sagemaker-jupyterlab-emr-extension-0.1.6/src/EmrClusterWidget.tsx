import React from 'react';
import { Dialog, ISessionContext, ReactWidget } from '@jupyterlab/apputils';
import { css, cx } from '@emotion/css';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { EmrClusterButton } from './components/EmrClusterButton';
import { handleKeyboardEvent } from './utils/KeyboardEventHandler';
import { ModalHeader } from './components/Modal/ModalHeader';
import { createListClusterWidget } from './ListClusterWidget';
import { i18nStrings } from './constants/i18n';
import { AuthType, ClusterRowType } from './constants/types';
import { getAuthTypeFromCluster } from './utils/AuthTypeUtil';
import { createSelectAuthTypeWidget } from './SelectAuthypeWidget';
import { ListClusterHeader } from './components/ListClusterHeader';
import { COMMANDS } from './utils/CommandUtils';
import styles from './components/Modal/styles';

const dialogClassname = css`
  .jp-Dialog-content {
    width: 900px;
    max-width: none;
    max-height: none;
    padding: 0;
  }
  .jp-Dialog-header {
    padding: 24px 24px 12px 24px;
    background-color: var(--jp-layout-color2);
  }
  /* Hide jp footer so we can add custom footer with button controls. */
  .jp-Dialog-footer {
    display: none;
  }
`;

export class EmrClusterWidget extends ReactWidget {
  private _selectedCluster: ClusterRowType | null;
  private _appContext: JupyterFrontEnd<JupyterFrontEnd.IShell, 'desktop' | 'mobile'>;
  private _connectedCluster: ClusterRowType | null;
  private _kernelId: string | null;

  constructor(clientSession: ISessionContext, appContext: JupyterFrontEnd) {
    super();
    this._selectedCluster = null;
    this._appContext = appContext;
    this._connectedCluster = null;
    this._kernelId = null;
  }

  private _setSelectedCluster = (nextCluster: ClusterRowType) => {
    if (this._selectedCluster?.id !== nextCluster.id) {
      this._selectedCluster = nextCluster;
    }
  };

  get kernelId(): string | null {
    return this._kernelId;
  }

  get selectedCluster(): ClusterRowType | null {
    return this._selectedCluster;
  }

  updateConnectedCluster = (cluster: ClusterRowType) => {
    this._connectedCluster = cluster;
    this.update();
  };

  getToolTip = () => {
    const tooltip = this._connectedCluster
      ? `${i18nStrings.Clusters.widgetConnected} ${this._connectedCluster.name} cluster`
      : i18nStrings.Clusters.defaultTooltip;
    return tooltip;
  };

  openSelectAuthType = async (selectedCluster: ClusterRowType) => {
    // TODO: update type here to Dialog. Had issues with one of typescript rule. Will look into this later.
    let dialog: any = {};
    const disposeDialog = () => dialog && dialog.resolve();
    dialog = new Dialog({
      title: (
        <ModalHeader
          heading={`${i18nStrings.Clusters.selectAuthTitle}"${selectedCluster.name}"`}
          shouldDisplayCloseButton={true}
          onClickCloseButton={disposeDialog}
        />
      ),
      body: createSelectAuthTypeWidget(disposeDialog, this.handleConnect as any, selectedCluster).render(),
    });

    dialog.addClass(cx(styles.ModalBase, styles.Footer, dialogClassname));
    dialog.launch();
  };

  handleConnect = (disposeDialog: () => void, selectedCluster: ClusterRowType | undefined, type?: AuthType) => {
    /*
     * Cluster id is based on customer selection
     * Auth type is based on the customer's cluster properties
     * Auth options: Kerberos, None, Basic_Access
     * Language options: scala, python
     */
    return () => {
      if (!selectedCluster) return;
      this._setSelectedCluster(selectedCluster);
      const authType = type || getAuthTypeFromCluster(selectedCluster);

      if (!authType) {
        // close previous dialog and open a new one for selecting auth type
        disposeDialog();
        this.openSelectAuthType(selectedCluster);
      } else {
        disposeDialog();
        this._appContext.commands.execute(COMMANDS.emrConnect.id, {
          clusterId: selectedCluster.id,
          authType: authType,
          language: 'python', // This option is hardcoded by default
        });
        // TODO: Add telemetry, logging
      }
    };
  };

  clickHandler = async () => {
    // TODO: update type here to Dialog. Had issues with one of typescript rule. Will look into this later.
    let dialog: any = {};
    const disposeDialog = () => dialog && dialog.resolve();

    dialog = new Dialog({
      title: (
        <ModalHeader
          heading={i18nStrings.Clusters.widgetTitle}
          shouldDisplayCloseButton={true}
          onClickCloseButton={disposeDialog}
          className="list-cluster-modal-header"
        />
      ),
      body: createListClusterWidget(disposeDialog, this.handleConnect as any, this.listClusterHeader()).render(),
    });

    dialog.handleEvent = (event: Event) => {
      if (event.type === 'keydown') {
        handleKeyboardEvent({
          keyboardEvent: event as KeyboardEvent,
          onEscape: () => dialog.reject(),
        });
      }
    };

    dialog.addClass(cx(styles.ModalBase, styles.Footer, dialogClassname));
    dialog.launch();
  };

  updateKernel(kernelId: string | null) {
    if (this._kernelId === kernelId) return;
    this._kernelId = kernelId;
    if (this.kernelId) {
      this.update();
    }
  }

  listClusterHeader = () => {
    return <ListClusterHeader clusterName={this._connectedCluster?.name} />;
  };

  render() {
    return <EmrClusterButton handleClick={this.clickHandler} tooltip={this.getToolTip()} />;
  }
}

const createEmrClusterWidget = (clientSession: ISessionContext, appContext: JupyterFrontEnd) =>
  new EmrClusterWidget(clientSession, appContext);

export { createEmrClusterWidget };

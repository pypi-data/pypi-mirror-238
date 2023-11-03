import React, { Suspense } from 'react';
import { Dialog } from '@jupyterlab/apputils';
import { ListClusterView } from './components/ListClusterView';
import { HandleConnectType, ShowNotificationHandlerType } from './constants/types';

// @ts-ignore
class ListClusterWidget implements Dialog.IBodyWidget {
  readonly disposeDialog: any;
  readonly handleConnect: HandleConnectType;
  readonly header: JSX.Element;

  constructor(disposeDialog: ShowNotificationHandlerType, handleConnect: HandleConnectType, header: JSX.Element) {
    this.disposeDialog = disposeDialog;
    this.handleConnect = handleConnect;
    this.header = header;
  }

  render() {
    return (
      <Suspense fallback={null}>
        <ListClusterView
          onCloseModal={this.disposeDialog}
          getConnectHandler={this.handleConnect}
          header={this.header}
          data-testid="list-cluster-view"
        />
      </Suspense>
    );
  }
}

const createListClusterWidget = (disposeDialog: () => void, handleConnect: HandleConnectType, header: JSX.Element) =>
  new ListClusterWidget(disposeDialog, handleConnect, header);

export { createListClusterWidget };

import { createSelectAuthTypeWidget } from '../SelectAuthypeWidget';
import { ClusterState, ClusterRowType } from '../constants/types';

const mockCluster: ClusterRowType = {
  name: 'Cluster-3',
  id: '3333',
  status: {
    state: ClusterState.Running,
  },
};

const disposeDialog = jest.fn();
const handleConnect = jest.fn();

describe('SelectAuthTypeWidget', () => {
  it('should render SelectAuthType component with selected cluster', () => {
    const widget = createSelectAuthTypeWidget(disposeDialog, handleConnect, mockCluster);
    const element = widget.render();
    expect(element.props.selectedCluster).toEqual(mockCluster);
  });
});

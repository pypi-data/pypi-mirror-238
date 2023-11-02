import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { SelectAuthType } from '../SelectAuthType';
import { i18nStrings } from '../../constants/i18n';

// Mock the necessary props and functions
const mockProps = {
  onCloseModal: jest.fn(),
  getConnectHandler: jest.fn(),
  selectedCluster: undefined,
  notebookPanel: undefined,
  onConnect: jest.fn(),
};

describe('SelectAuthType', () => {
  it('renders component with default auth type', () => {
    const { getByLabelText } = render(<SelectAuthType {...mockProps} />);

    // Ensure that the component renders with default auth type 'Basic_Access'
    expect(getByLabelText(i18nStrings.Clusters.radioButtonLabels.basicAccess)).toBeInTheDocument();
    expect(getByLabelText(i18nStrings.Clusters.radioButtonLabels.noCredential)).toBeInTheDocument();
  });

  it('renders the component with default auth type', () => {
    const { getByLabelText } = render(
      <SelectAuthType
        onCloseModal={() => {}}
        getConnectHandler={() => {}}
        selectedCluster={null}
        notebookPanel={null}
      />,
    );

    const basicAccessRadio = getByLabelText(i18nStrings.Clusters.radioButtonLabels.basicAccess);
    const noCredentialRadio = getByLabelText(i18nStrings.Clusters.radioButtonLabels.noCredential);

    expect(basicAccessRadio).toBeChecked();
    expect(noCredentialRadio).not.toBeChecked();
  });
});

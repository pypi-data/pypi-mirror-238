import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { ListClusterView } from '../ListClusterView';
import { i18nStrings } from '../../constants/i18n';

// Mock the caretDownIcon
jest.mock('@jupyterlab/ui-components', () => {
  return {
    caretDownIcon: {
      react: jest.fn().mockReturnValue(<span data-testid="caret-down-icon">Caret Down Icon</span>),
    },
  };
});

// Mock the caretUpIcon
jest.mock('@jupyterlab/ui-components', () => {
  return {
    caretRightIcon: {
      react: jest.fn().mockReturnValue(<span data-testid="caret-right-icon">Caret Right Icon</span>),
    },
  };
});

// Mock API data and any necessary dependencies here
jest.mock('../../utils/CommonUtils', () => ({
  arrayHasLength: jest.fn(() => true), // Mock arrayHasLength to return true
}));

jest.mock('../../__mocks__/mockListCluster', () => ({
  getData: jest.fn(() => []),
}));

//TODO: Comeback to writing tests for this one
xdescribe('ListClusterView', () => {
  it('displays a message when there are no clusters', () => {
    render(<ListClusterView onCloseModal={jest.fn()} />);

    const noClusterMessage = screen.getByText(i18nStrings.Clusters.noResultsMatchingFilters); // Replace with the actual message displayed
    expect(noClusterMessage).toBeInTheDocument();
  });
});

import { css } from '@emotion/css';

const ModalBase = css`
  &.jp-Dialog {
    z-index: 1; /* Override default z-index so Dropdown menu is above the Modal */
  }
  .jp-Dialog-body {
    padding: var(--jp-padding-xl);
    .no-cluster-msg {
      padding: var(--jp-cell-collapser-min-height);
      margin: auto;
    }
  }
`;

const Header = css`
  width: 100%;
  display: contents;
  font-size: 0.5rem;
  h1 {
    margin: 0;
  }
`;

const HeaderButtons = css`
  display: flex;
  float: right;
`;

const ModalFooter = css`
  display: flex;
  justify-content: flex-end;
  background-color: var(--jp-layout-color2);
  padding: 12px 24px 12px 24px;
  button {
    margin: 5px;
  }
`;

const Footer = css`
  .jp-Dialog-footer {
    background-color: var(--jp-layout-color2);
    margin: 0;
  }
`;

const DismissButton = css`
  padding: 0;
  border: none;
  cursor: pointer;
`;

export default {
  ModalBase,
  Header,
  HeaderButtons,
  ModalFooter,
  Footer,
  DismissButton,
};

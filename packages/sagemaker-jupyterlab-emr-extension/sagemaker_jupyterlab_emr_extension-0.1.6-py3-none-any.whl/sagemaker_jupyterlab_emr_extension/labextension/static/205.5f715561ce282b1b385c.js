"use strict";(self.webpackChunk_amzn_sagemaker_jupyterlab_emr_extension=self.webpackChunk_amzn_sagemaker_jupyterlab_emr_extension||[]).push([[205],{1205:(e,t,n)=>{n.r(t),n.d(t,{default:()=>Et});var r=n(3408),a=n(6029),s=n.n(a),o=n(2861),l=n(1837);const i="SelectedCell",c="HoveredCellClassname",d="SelectAuthContainer";var u;!function(e){e.emrConnect="sagemaker-studio:emr-connect"}(u||(u={}));const p={widgetTitle:"Connect to cluster",connectCommand:{label:"Connect",caption:"Connect to a cluster"},connectMessage:{errorTitle:"Error connecting to EMR cluster",successTitle:"Successfully connected to EMR cluster",errorDefaultMessage:"Error connecting to EMR cluster",successDefaultMessage:"Connected to EMR Cluster"},widgetConnected:"The notebook is connected to",defaultTooltip:"Select a cluster to connect to",widgetHeader:"Select a cluster to connect to. A code block will be added to the active cell and run automatically to establish the connection.",connectedWidgetHeader:"cluster. You can submit new jobs to run on the cluster.",connectButton:"Connect",learnMore:"Learn more",noResultsMatchingFilters:"There are no clusters matching the filter.",radioButtonLabels:{basicAccess:"Http basic authentication",noCredential:"No credential"},listClusterError:"Fail to list clusters, refresh the modal or try again later",noCluster:"No clusters are available",selectAuthTitle:"Select credential type for ",clusterButtonLabel:"Cluster",expandCluster:{MasterNodes:"Master nodes",CoreNodes:"Core nodes",NotAvailable:"Not available",NoTags:"No tags",SparkHistoryServer:"Spark History Server",TezUI:"Tez UI",Overview:"Overview",Apps:"Apps",ApplicationUserInterface:"Application user Interface",Tags:"Tags"},presignedURL:{link:"Link",error:"Error: ",retry:"Retry",sparkUIError:"Spark UI Link is not available or time out. Please try ",sshTunnelLink:"SSH tunnel",or:" or ",viewTheGuide:"view the guide",clusterNotReady:"Cluster is not ready. Please try again later.",clusterNotConnected:"No active cluster connection. Please connect to a cluster and try again.",clusterNotCompatible:"EMR version 5.33+ or 6.3.0+ required for direct Spark UI links. Try a compatible cluster, use "}},m="Cancel",h=({handleClick:e,tooltip:t})=>s().createElement("div",{className:"EmrClusterContainer"},s().createElement(o.ToolbarButtonComponent,{className:"EmrClusterButton",tooltip:t,label:p.clusterButtonLabel,onClick:e,enabled:!0}));var g;!function(e){e.tab="Tab",e.enter="Enter",e.escape="Escape",e.arrowDown="ArrowDown"}(g||(g={}));var v=n(8278),b=n(1800),C=n(8564);const E={ModalBase:l.css`
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
`,Header:l.css`
  width: 100%;
  display: contents;
  font-size: 0.5rem;
  h1 {
    margin: 0;
  }
`,HeaderButtons:l.css`
  display: flex;
  float: right;
`,ModalFooter:l.css`
  display: flex;
  justify-content: flex-end;
  background-color: var(--jp-layout-color2);
  padding: 12px 24px 12px 24px;
  button {
    margin: 5px;
  }
`,Footer:l.css`
  .jp-Dialog-footer {
    background-color: var(--jp-layout-color2);
    margin: 0;
  }
`,DismissButton:l.css`
  padding: 0;
  border: none;
  cursor: pointer;
`},f=({heading:e,headingId:t="modalHeading",className:n,shouldDisplayCloseButton:r=!1,onClickCloseButton:a,actionButtons:o})=>{let i=null,c=null;return r&&(i=s().createElement(v.z,{className:(0,l.cx)(E.DismissButton,"dismiss-button"),role:"button","aria-label":"close",onClick:a,"data-testid":"close-button"},s().createElement(b.closeIcon.react,{tag:"span"}))),o&&(c=o.map((e=>{const{className:t,component:n,onClick:r,label:a}=e;return n?s().createElement("div",{key:`${(0,C.v4)()}`},n):s().createElement(v.z,{className:t,type:"button",role:"button",onClick:r,"aria-label":a,key:`${(0,C.v4)()}`},a)}))),s().createElement("header",{className:(0,l.cx)(E.Header,n)},s().createElement("h1",{id:t},e),s().createElement("div",{className:(0,l.cx)(E.HeaderButtons,"header-btns")},c,i))};var x=n(1105);const w=({onCloseModal:e,onConnect:t,disabled:n})=>s().createElement("footer",{className:E.ModalFooter},s().createElement(v.z,{className:"jp-Dialog-button jp-mod-reject jp-mod-styled listcluster-cancel-btn",type:"button",onClick:e},m),s().createElement(v.z,{className:"jp-Dialog-button jp-mod-accept jp-mod-styled listcluster-connect-btn",type:"button",onClick:t,disabled:n},p.connectButton));class y{constructor(e="",t="",n="",r="",a="",s="",o=""){this.partition=e,this.service=t,this.region=n,this.accountId=r,this.resourceInfo=a,this.resourceType=s,this.resourceName=o}static getResourceInfo(e){const t=e.match(y.SPLIT_RESOURCE_INFO_REG_EXP);let n="",r="";return t&&(1===t.length?r=t[1]:(n=t[1],r=t[2])),{resourceType:n,resourceName:r}}static fromArnString(e){const t=e.match(y.ARN_REG_EXP);if(!t)throw new Error(`Invalid ARN format: ${e}`);const[,n,r,a,s,o]=t,{resourceType:l="",resourceName:i=""}=o?y.getResourceInfo(o):{};return new y(n,r,a,s,o,l,i)}static isValid(e){return!!e.match(y.ARN_REG_EXP)}static getArn(e,t,n,r,a,s){return`arn:${e}:${t}:${n}:${r}:${a}/${s}`}}y.ARN_REG_EXP=/^arn:(.*?):(.*?):(.*?):(.*?):(.*)$/,y.SPLIT_RESOURCE_INFO_REG_EXP=/^(.*?)[/:](.*)$/,y.VERSION_DELIMITER="/";const k=({cellData:e})=>{var t,n,r;const a=null===(t=e.status)||void 0===t?void 0:t.state;return"RUNNING"===(null===(n=e.status)||void 0===n?void 0:n.state)||"WAITING"===(null===(r=e.status)||void 0===r?void 0:r.state)?s().createElement("div",null,s().createElement("svg",{width:"10",height:"10"},s().createElement("circle",{cx:"5",cy:"5",r:"5",fill:"green"})),s().createElement("label",{htmlFor:"myInput"},"Running/Waiting")):s().createElement("div",null,s().createElement("label",{htmlFor:"myInput"},a))},I={name:"Name",id:"ID",status:"Status",creationTime:"Creation Time",createdOn:"Created On",accountId:"Account ID"};var T=n(2510),N=n(4321);l.css`
  height: 100%;
  position: relative;
`;const R=l.css`
  margin-right: 10px;
`,S=(l.css`
  ${R}
  svg {
    width: 6px;
  }
`,l.css`
  background-color: var(--jp-layout-color2);
  label: ${c};
  cursor: pointer;
`),A=l.css`
  background-color: var(--jp-layout-color3);
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently supported by Chrome, Opera and Firefox */
  label: ${i};
`,U=l.css`
  background-color: var(--jp-layout-color2);
  display: flex;
  padding: var(--jp-cell-padding);
  width: 100%;
  align-items: baseline;
  justify-content: start;
  /* box shadow */
  -moz-box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  -webkit-box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  /* Disable visuals for scroll */
  overflow-x: scroll;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
  &::-webkit-scrollbar {
    display: none;
  }
`,j={borderTop:"var(--jp-border-width) solid var(--jp-border-color1)",borderBottom:"var(--jp-border-width) solid var(--jp-border-color1)",borderRight:"var(--jp-border-width) solid var(--jp-border-color1)",display:"flex",boxSizing:"border-box",marginRight:"0px",padding:"2.5px",fontWeight:"initial",textTransform:"capitalize",color:"var(--jp-ui-font-color2)"},_={display:"flex",flexDirection:"column",height:"max-content"},L=l.css`
  display: flex;
`,M={height:"max-content",display:"flex",overflow:"auto",padding:"var(--jp-cell-padding)"},P=({isSelected:e})=>e?s().createElement(b.caretDownIcon.react,{tag:"span"}):s().createElement(b.caretRightIcon.react,{tag:"span"}),D=({dataList:e,tableConfig:t,selectedId:n,expandedView:r,noResultsView:o,showIcon:i,isLoading:c,columnConfig:d,onRowSelect:u,...p})=>{const m=(0,a.useRef)(null),h=(0,a.useRef)(null),[g,v]=(0,a.useState)(-1),[b,C]=(0,a.useState)(0);(0,a.useEffect)((()=>{var e,t;C((null===(e=null==h?void 0:h.current)||void 0===e?void 0:e.clientHeight)||28),null===(t=m.current)||void 0===t||t.recomputeRowHeights()}),[n,c,t.width,t.height]);const E=({rowData:e,...t})=>e?(0,T.defaultTableCellDataGetter)({rowData:e,...t}):null;return s().createElement(T.Table,{...p,...t,headerStyle:j,ref:m,headerHeight:28,overscanRowCount:10,rowCount:e.length,rowData:e,noRowsRenderer:()=>o,rowHeight:({index:t})=>e[t].id&&e[t].id===n?b:28,rowRenderer:e=>{const{style:t,key:a,rowData:o,index:i,className:c}=e,d=n===o.id,u=g===i,p=(0,l.cx)(L,c,{[A]:d,[S]:!d&&u});return d?s().createElement("div",{key:a,ref:h,style:{...t,..._},onMouseEnter:()=>v(i),onMouseLeave:()=>v(-1),className:p},(0,N.Cx)({...e,style:{width:t.width,...M}}),s().createElement("div",{className:U},r)):s().createElement("div",{key:a,onMouseEnter:()=>v(i),onMouseLeave:()=>v(-1)},(0,N.Cx)({...e,className:p}))},onRowClick:({rowData:e})=>u(e),rowGetter:({index:t})=>e[t]},d.map((({dataKey:t,label:r,disableSort:a,cellRenderer:o})=>s().createElement(T.Column,{key:t,dataKey:t,label:r,flexGrow:1,width:150,disableSort:a,cellDataGetter:E,cellRenderer:t=>((t,r)=>{const{rowIndex:a,columnIndex:o}=t,l=e[a].id===n,c=0===o;let d=null;return r&&(d=r({row:e[a],rowIndex:a,columnIndex:o,onCellSizeChange:()=>null})),c&&i?s().createElement(s().Fragment,null,s().createElement(P,{isSelected:l})," ",d):d})(t,o)}))))},$=l.css`
  height: 100%;
  position: relative;
`,O=l.css`
  margin-right: 10px;
`,F=(l.css`
  ${O}
  svg {
    width: 6px;
  }
`,l.css`
  text-align: center;
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  margin-right: -50%;
  transform: translate(-50%, -50%);
`),B=(l.css`
  background-color: var(--jp-layout-color2);
  label: ${c};
  cursor: pointer;
`,l.css`
  background-color: var(--jp-layout-color3);
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently supported by Chrome, Opera and Firefox */
  label: ${i};
`,l.css`
  background-color: var(--jp-layout-color2);
  display: flex;
  padding: var(--jp-cell-padding);
  width: 100%;
  align-items: baseline;
  justify-content: start;

  /* box shadow */
  -moz-box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  -webkit-box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);

  /* Disable visuals for scroll */
  overflow-x: scroll;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
  &::-webkit-scrollbar {
    display: none;
  }
`,l.css`
  padding: 24px 24px 12px 24px;
`),z=l.css`
  .ReactVirtualized__Table__headerRow {
    display: flex;
  }
  .ReactVirtualized__Table__row {
    display: flex;
    font-size: 12px;
    align-items: center;
  }
`,H=l.css`
  width: 100%;
  display: flex;
  flex-direction: row;
`,G=l.css`
  flex-direction: column;
  margin: 0 32px 8px 8px;
  flex: 1 0 auto;
  width: 33%;
`,V=l.css`
  width: 20%;
`,W=l.css`
  margin-bottom: var(--jp-code-padding);
`,K=p.expandCluster,J=({clusterData:e})=>{const t=null==e?void 0:e.tags;return(null==t?void 0:t.length)?s().createElement(s().Fragment,null,t.map((e=>s().createElement("div",{className:W,key:null==e?void 0:e.key},null==e?void 0:e.key,": ",null==e?void 0:e.value)))):s().createElement("div",null,K.NoTags)},q=p.expandCluster;var X=n(4788),Y=n(4614);const Z="/aws/sagemaker/api/emr/describe-cluster",Q=[200,201];var ee;!function(e){e.POST="POST",e.GET="GET",e.PUT="PUT"}(ee||(ee={}));const te=async(e,t,n)=>{const r=X.ServerConnection.makeSettings(),a=Y.URLExt.join(r.baseUrl,e);try{const e=await X.ServerConnection.makeRequest(a,{method:t,body:n},r);if(!Q.includes(e.status))throw new Error("Unable to fetch data");return e.json()}catch(e){return e}},ne=async e=>{if(void 0===e)throw new Error("Error describing persistent app UI: Invalid persistent app UI ID");const t={PersistentAppUIId:e},n=JSON.stringify(t);return await te("/aws/sagemaker/api/emr/describe-persistent-app-ui",ee.POST,n)},re=async e=>await new Promise((t=>setTimeout(t,e)));var ae,se,oe,le,ie;!function(e){e.Bootstrapping="BOOTSTRAPPING",e.Running="RUNNING",e.Starting="STARTING",e.Terminated="TERMINATED",e.TerminatedWithErrors="TERMINATED_WITH_ERRORS",e.Terminating="TERMINATING",e.Undefined="UNDEFINED",e.Waiting="WAITING"}(ae||(ae={})),function(e){e.AllStepsCompleted="All_Steps_Completed",e.BootstrapFailure="Bootstrap_Failure",e.InstanceFailure="Instance_Failure",e.InstanceFleetTimeout="Instance_Fleet_Timeout",e.InternalError="Internal_Error",e.StepFailure="Step_Failure",e.UserRequest="User_Request",e.ValidationError="Validation_Error"}(se||(se={})),function(e){e[e.SHS=0]="SHS",e[e.TEZUI=1]="TEZUI",e[e.YTS=2]="YTS"}(oe||(oe={})),function(e){e.Success="Success",e.Fail="Fail"}(le||(le={})),function(e){e[e.Content=0]="Content",e[e.External=1]="External",e[e.Notebook=2]="Notebook"}(ie||(ie={}));const ce="smsjp--icon-link-external",de={link:l.css`
  a& {
    color: var(--jp-content-link-color);
    line-height: var(--jp-custom-ui-text-line-height);
    text-decoration: none;
    text-underline-offset: 1.5px;

    span.${ce} {
      display: inline;
      svg {
        width: var(--jp-ui-font-size1);
        height: var(--jp-ui-font-size1);
        margin-left: var(--jp-ui-font-size1;
        transform: scale(calc(var(--jp-custom-ui-text-line-height) / 24));
      }
      path {
        fill: var(--jp-ui-font-color1);
      }
    }

    &.sm--content-link {
      text-decoration: underline;
    }

    &:hover:not([disabled]) {
      text-decoration: underline;
    }

    &:focus:not([disabled]),
    &:active:not([disabled]) {
      color: var(--jp-brand-color2);
      .${ce} path {
        fill: var(--jp-ui-font-color1);
      }
    }

    &:focus:not([disabled]) {
      border: var(--jp-border-width) solid var(--jp-brand-color2);
    }

    &:active:not([disabled]) {
      text-decoration: underline;
    }

    &[disabled] {
      color: var(--jp-ui-font-color3);
      .${ce} path {
        fill: var(--jp-ui-font-color1);
      }
    }
  }
`,externalIconClass:ce};var ue;!function(e){e[e.Content=0]="Content",e[e.External=1]="External",e[e.Notebook=2]="Notebook"}(ue||(ue={}));const pe=({children:e,className:t,disabled:n=!1,href:r,onClick:a,type:o=ue.Content,hideExternalIcon:i=!1,...c})=>{const d=o===ue.External,u={className:(0,l.cx)(de.link,t,{"sm-emr-content":o===ue.Content}),href:r,onClick:n?void 0:a,target:d?"_blank":void 0,rel:d?"noopener noreferrer":void 0,...c},p=d&&!i?s().createElement("span",{className:de.externalIconClass},s().createElement(b.launcherIcon.react,{tag:"span"})):null;return s().createElement("a",{role:"link",...u},e,p)},me=l.css`
  h2 {
    font-size: var(--jp-ui-font-size1);
    margin-top: 0;
  }
`,he=l.css`
  .DataGrid-ContextMenu > div {
    overflow: hidden;
  }
  margin: 12px;
`,ge=l.css`
  padding-bottom: var(--jp-add-tag-extra-width);
`,ve=l.css`
  background-color: var(--jp-layout-color2);
  display: flex;
  justify-content: flex-end;
  button {
    margin: 5px;
  }
`,be=l.css`
  text-align: center;
  vertical-align: middle;
`,Ce={ModalBase:me,ModalBody:he,ModalFooter:ve,ListTable:l.css`
  overflow: hidden;
`,NoHorizontalPadding:l.css`
  padding-left: 0;
  padding-right: 0;
`,RadioGroup:l.css`
  display: flex;
  justify-content: flex-start;
  li {
    margin-right: 20px;
  }
`,ModalHeader:ge,ModalMessage:be,AuthModal:l.css`
  min-height: none;
`,ListClusterModal:l.css`
  /* so the modal height remains the same visually during and after loading (this number can be changed) */
  min-height: 600px;
`,ConnectCluster:l.css`
  white-space: nowrap;
`,ClusterDescription:l.css`
  display: inline;
`,PresignedURL:l.css`
  line-height: normal;
`,ClusterListModalCrossAccountError:l.css`
  display: flex;
  flex-direction: column;
  padding: 0 0 10px 0;
`,GridWrapper:l.css`
  box-sizing: border-box;
  width: 100%;
  height: 100%;

  & .ReactVirtualized__Grid {
    /* important is required because react virtualized puts overflow style inline */
    overflow-x: hidden !important;
  }

  & .ReactVirtualized__Table__headerRow {
    display: flex;
  }

  & .ReactVirtualized__Table__row {
    display: flex;
    font-size: 12px;
    align-items: center;
  }
`,EmrExecutionRoleContainer:l.css`
  margin-top: 25px;
  width: 90%;
`,Dropdown:l.css`
  margin-top: var(--jp-cell-padding);
`,PresignedURLErrorText:l.css`
  color: var(--jp-error-color1);
`},Ee="Invalid Cluster State",fe="Missing Cluster ID, are you connected to a cluster?",xe="Unsupported cluster version",we=({clusterId:e,accountId:t,applicationId:n,persistentAppUIType:r,label:o,onError:i})=>{const[c,d]=(0,a.useState)(!1),[u,m]=(0,a.useState)(!1),h=(0,a.useCallback)((e=>{m(!0),i(e)}),[i]),g=(0,a.useCallback)((e=>{if(!e)throw new Error("Error opening Spark UI: Invalid URL");null!==window.open(e,"_blank","noopener,noreferrer")&&(m(!1),i(null))}),[i]),v=(0,a.useCallback)(((e,t,n)=>{(async(e,t)=>{const n={ClusterId:e,OnClusterAppUIType:"ApplicationMaster",ApplicationId:t},r=JSON.stringify(n);return await te("/aws/sagemaker/api/emr/get-on-cluster-app-ui-presigned-url",ee.POST,r)})(e,n).then((e=>g(null==e?void 0:e.presignedURL))).catch((e=>h(e))).finally((()=>d(!1)))}),[h,g]),b=(0,a.useCallback)(((e,t,n,r)=>{(async e=>{if(void 0===e)throw new Error("Error describing persistent app UI: Invalid persistent app UI ID");const t={TargetResourceArn:e},n=JSON.stringify(t);return await te("/aws/sagemaker/api/emr/create-persistent-app-ui",ee.POST,n)})(e.clusterArn).then((e=>(async(e,t,n)=>{var r;const a=Date.now();let s,o=0;for(;o<=3e4;){const t=await ne(e),n=null===(r=null==t?void 0:t.persistentAppUI)||void 0===r?void 0:r.persistentAppUIStatus;if(n&&"ATTACHED"===n){s=t;break}await re(2e3),o=Date.now()-a}if(null==s)throw new Error("Error waiting for persistent app UI ready: Max attempts reached");return s})(null==e?void 0:e.persistentAppUIId))).then((e=>(async(e,t,n)=>{if(void 0===e)throw new Error("Error getting persistent app UI presigned URL: Invalid persistent app UI ID");const r={PersistentAppUIId:e,PersistentAppUIType:t},a=JSON.stringify(r);return await te("/aws/sagemaker/api/emr/get-persistent-app-ui-presigned-url",ee.POST,a)})(null==e?void 0:e.persistentAppUI.persistentAppUIId,r))).then((e=>g(null==e?void 0:e.presignedURL))).catch((e=>h(e))).finally((()=>d(!1)))}),[h,g]),C=(0,a.useCallback)(((e,t,n,r)=>async()=>{if(d(!0),!t)return d(!1),void h(fe);const a=await(async e=>{const t={ClusterId:e},n=JSON.stringify(t);return await te(Z,ee.POST,n)})(t).catch((e=>h(e)));if(!a||!(null==a?void 0:a.cluster))return void d(!1);const s=null==a?void 0:a.cluster;if(s.releaseLabel)try{const e=s.releaseLabel.substr(4).split("."),t=+e[0],n=+e[1];if(t<5)return d(!1),void h(xe);if(5===t&&n<33)return d(!1),void h(xe);if(6===t&&n<3)return d(!1),void h(xe)}catch(e){}switch(s.status.state){case ae.Running:case ae.Waiting:n?v(t,e,n):b(s,e,n,r);break;case ae.Terminated:b(s,e,n,r);break;default:d(!1),h(Ee)}}),[v,b,h]);return s().createElement(s().Fragment,null,c?s().createElement("span",null,s().createElement(x.CircularProgress,{size:"1rem"})):s().createElement(pe,{className:(0,l.cx)("PresignedURL",Ce.PresignedURL),onClick:C(t,e,n,r)},u?s().createElement("span",null,o&&o," ",s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText),onClick:C(t,e,n,r)},"(",p.presignedURL.retry,")")):o||p.presignedURL.link))},ye=l.css`
  cursor: pointer;
  & {
    color: var(--jp-content-link-color);
    text-decoration: none;
    text-underline-offset: 1.5px;
    text-decoration: underline;

    &:hover:not([disabled]) {
      text-decoration: underline;
    }

    &:focus:not([disabled]) {
      border: var(--jp-border-width) solid var(--jp-brand-color2);
    }

    &:active:not([disabled]) {
      text-decoration: underline;
    }

    &[disabled] {
      color: var(--jp-ui-font-color3);
    }
  }
`,ke=l.css`
  display: flex;
`,Ie=(l.css`
  margin-left: 10px;
`,l.css`
  margin-bottom: var(--jp-code-padding);
`),Te=p.expandCluster,Ne=({clusterId:e,accountId:t,setIsError:n})=>{const[r]=(0,a.useState)(!1);return s().createElement("div",{className:ke},s().createElement("div",{className:(0,l.cx)("HistoryLink",ye)},s().createElement(we,{clusterId:e,onError:e=>e,accountId:t,persistentAppUIType:"SHS",label:Te.SparkHistoryServer})),s().createElement(b.launcherIcon.react,{tag:"span"}),r&&s().createElement("span",null,s().createElement(x.CircularProgress,{size:"1rem"})))},Re=p.expandCluster,Se=({clusterId:e,accountId:t,setIsError:n})=>{const[r]=s().useState(!1);return s().createElement("div",{className:ke},s().createElement("div",{className:ye},s().createElement(we,{clusterId:e,onError:e=>e,accountId:t,persistentAppUIType:"TEZ",label:Re.TezUI})),s().createElement(b.launcherIcon.react,{tag:"span"}),r&&s().createElement("span",null,s().createElement(x.CircularProgress,{size:"1rem"})))},Ae=p.expandCluster,Ue=e=>{const{accountId:t,selectedClusterId:n}=e,[r,o]=(0,a.useState)(!1);return r?s().createElement("div",null,Ae.NotAvailable):s().createElement(s().Fragment,null,s().createElement("div",{className:Ie},s().createElement(Ne,{clusterId:n,accountId:t,setIsError:o})),s().createElement("div",{className:Ie},s().createElement(Se,{clusterId:n,accountId:t,setIsError:o})))},je=p.expandCluster,_e=({clusterArn:e,accountId:t,selectedClusterId:n,clusterData:r})=>{const o=r,[i,c]=(0,a.useState)();return(0,a.useEffect)((()=>{(async e=>{const t=JSON.stringify({ClusterId:e}),n=await te("/aws/sagemaker/api/emr/list-instance-groups",ee.POST,t);c(n)})(n)}),[n]),s().createElement("div",{className:H},s().createElement("div",{className:G},s().createElement("h4",null,je.Overview),s().createElement("div",{className:W},(e=>{var t;const n=null===(t=null==e?void 0:e.instanceGroups)||void 0===t?void 0:t.find((e=>"MASTER"===(null==e?void 0:e.instanceGroupType)));if(n){const e=n.runningInstanceCount,t=n.instanceType;return`${q.MasterNodes}: ${e}, ${t}`}return`${q.MasterNodes}: ${q.NotAvailable}`})(i)),s().createElement("div",{className:W},(e=>{var t;const n=null===(t=null==e?void 0:e.instanceGroups)||void 0===t?void 0:t.find((e=>"CORE"===(null==e?void 0:e.instanceGroupType)));if(n){const e=n.runningInstanceCount,t=n.instanceType;return`${q.CoreNodes}: ${e}, ${t}`}return`${q.CoreNodes}: ${q.NotAvailable}`})(i)),s().createElement("div",{className:W},je.Apps,": ",(e=>{const t=null==e?void 0:e.applications;return(null==t?void 0:t.length)?t.map(((e,n)=>{const r=n===t.length-1?".":", ";return`${null==e?void 0:e.name} ${null==e?void 0:e.version}${r}`})):`${q.NotAvailable}`})(o))),s().createElement("div",{className:(0,l.cx)(G,V)},s().createElement("h4",null,je.ApplicationUserInterface),s().createElement(Ue,{selectedClusterId:n,accountId:t,clusterArn:e})),s().createElement("div",{className:G},s().createElement("h4",null,je.Tags),s().createElement(J,{clusterData:r})))},Le=p,Me=s().createElement("div",{className:$},s().createElement("p",{className:F},Le.noResultsMatchingFilters)),Pe=({clustersList:e,tableConfig:t,clusterManagementListConfig:n,selectedClusterId:r,clusterArn:a,accountId:o,onRowSelect:l,clusterDetails:i,...c})=>{const d=!i&&!1,u=i;return s().createElement(D,{...c,tableConfig:t,showIcon:!0,dataList:e,selectedId:r,columnConfig:n,isLoading:d,noResultsView:Me,onRowSelect:l,expandedView:d?s().createElement("span",null,s().createElement(x.CircularProgress,{size:"1rem"})):s().createElement(_e,{selectedClusterId:r,accountId:o||"",clusterArn:a,clusterData:u,instanceGroupData:void 0})})};n(7960);const De=e=>Array.isArray(e)&&e.length>0,$e={width:850,height:500},Oe=e=>{const{onCloseModal:t,getConnectHandler:n,header:r}=e,[o,i]=(0,a.useState)([]),[c,d]=(0,a.useState)(!1),[u,m]=(0,a.useState)(""),[h,g]=(0,a.useState)(void 0),[v,b]=(0,a.useState)(),[,C]=(0,a.useState)(""),[E,f]=(0,a.useState)(!0),T=[{dataKey:"name",label:I.name,disableSort:!0,cellRenderer:({row:e})=>{var t,n;return((null===(t=e.name)||void 0===t?void 0:t.length)||0)>20?(null===(n=null==e?void 0:e.name)||void 0===n?void 0:n.slice(0,19))+"...":null==e?void 0:e.name}},{dataKey:"id",label:I.id,disableSort:!0,cellRenderer:({row:e})=>null==e?void 0:e.id},{dataKey:"status",label:I.status,disableSort:!0,cellRenderer:({row:e})=>s().createElement(k,{cellData:e})},{dataKey:"creationDateTime",label:I.creationTime,disableSort:!0,cellRenderer:({row:e})=>{var t;return null===(t=null==e?void 0:e.status)||void 0===t?void 0:t.timeline.creationDateTime.split("+")[0].split(".")[0]}},{dataKey:"clusterArn",label:I.accountId,disableSort:!0,cellRenderer:({row:e})=>{if(null==e?void 0:e.clusterArn)return y.fromArnString(e.clusterArn).accountId}}],N=async(e="")=>{try{d(!0);const t=JSON.stringify({ClusterStates:["RUNNING","WAITING"],...e&&{Marker:e}}),n=await te("/aws/sagemaker/api/emr/list-clusters",ee.POST,t);n&&n.clusters&&(i((e=>[...e,...n.clusters])),n&&n.Marker?N(n.Marker):d(!1)),De(n)||(m(null==n?void 0:n.message),d(!1))}catch(e){d(!1),m(e)}};(0,a.useEffect)((()=>{N()}),[]),(0,a.useEffect)((()=>{v&&g((async e=>{const t=JSON.stringify({ClusterId:e}),n=await te(Z,ee.POST,t);g(n.cluster)})(v))}),[v]);const R=(0,a.useMemo)((()=>null==o?void 0:o.sort(((e,t)=>{const n=e.name,r=t.name;return null==n?void 0:n.localeCompare(r)}))),[o]),S=(0,a.useCallback)((e=>{const t=R.find((t=>t.id===e));let n="";const r=null==t?void 0:t.clusterArn;return r&&y.isValid(r)&&(n=y.fromArnString(r).accountId),n}),[R]),A=(0,a.useCallback)((e=>{const t=R.find((t=>t.id===e)),n=null==t?void 0:t.clusterArn;return n&&y.isValid(n)?n:""}),[R]),U=(0,a.useCallback)((e=>{const t=null==e?void 0:e.id;t&&t===v?(b(t),C(""),f(!0)):(b(t),C(S(t)),f(!1))}),[v,S]);return s().createElement(s().Fragment,null,u&&s().createElement("span",{className:"no-cluster-msg"},u),c?s().createElement("span",null,s().createElement(x.CircularProgress,{size:"1rem"})):De(o)?s().createElement("div",{className:(0,l.cx)(B,"modal-body-container")},r,s().createElement(s().Fragment,null,s().createElement("div",{className:(0,l.cx)(z,"grid-wrapper")},s().createElement(Pe,{clustersList:R,selectedClusterId:null!=v?v:"",clusterArn:A(null!=v?v:""),accountId:S(null!=v?v:""),tableConfig:$e,clusterManagementListConfig:T,onRowSelect:U,clusterDetails:h})))):s().createElement("div",{className:"no-cluster-msg"},p.noCluster),s().createElement(w,{onCloseModal:t,onConnect:()=>{n(t,h)()},disabled:E}))};class Fe{constructor(e,t,n){this.disposeDialog=e,this.handleConnect=t,this.header=n}render(){return s().createElement(a.Suspense,{fallback:null},s().createElement(Oe,{onCloseModal:this.disposeDialog,getConnectHandler:this.handleConnect,header:this.header,"data-testid":"list-cluster-view"}))}}const Be=(e,t,n)=>new Fe(e,t,n),ze=({onCloseModal:e,getConnectHandler:t,selectedCluster:n,notebookPanel:r})=>{const o=`${d}`,i=`${d}`,[c,u]=(0,a.useState)("Basic_Access"),m=(0,a.useMemo)((()=>t(e,n,c,void 0,r)),[t,e,n,c,r]);return s().createElement("div",{className:(0,l.cx)(o,Ce.ModalBase,Ce.AuthModal)},s().createElement("div",{className:(0,l.cx)(i,Ce.ModalBody)},s().createElement(x.FormControl,null,s().createElement(x.RadioGroup,{"aria-labelledby":"demo-radio-buttons-group-label",defaultValue:"Basic_Access",value:c,onChange:e=>{"Basic_Access"!==e.target.value&&"None"!==e.target.value||u(e.target.value)},name:"radio-buttons-group","data-testid":"radio-button-group",row:!0},s().createElement(x.FormControlLabel,{value:"Basic_Access",control:s().createElement(x.Radio,null),label:p.radioButtonLabels.basicAccess}),s().createElement(x.FormControlLabel,{value:"None",control:s().createElement(x.Radio,null),label:p.radioButtonLabels.noCredential})))),s().createElement(w,{onCloseModal:e,onConnect:m,disabled:!1}))};class He{constructor(e,t,n,r){this.disposeDialog=e,this.handleConnect=t,this.selectedCluster=n,this.notebookPanel=r}render(){return s().createElement(ze,{onCloseModal:this.disposeDialog,getConnectHandler:this.handleConnect,selectedCluster:this.selectedCluster,notebookPanel:this.notebookPanel})}}const Ge=(e,t,n,r)=>new He(e,t,n,r);var Ve;!function(e){e["us-east-1"]="us-east-1",e["us-east-2"]="us-east-2",e["us-west-1"]="us-west-1",e["us-west-2"]="us-west-2",e["us-gov-west-1"]="us-gov-west-1",e["us-gov-east-1"]="us-gov-east-1",e["us-iso-east-1"]="us-iso-east-1",e["us-isob-east-1"]="us-isob-east-1",e["ca-central-1"]="ca-central-1",e["eu-west-1"]="eu-west-1",e["eu-west-2"]="eu-west-2",e["eu-west-3"]="eu-west-3",e["eu-central-1"]="eu-central-1",e["eu-north-1"]="eu-north-1",e["eu-south-1"]="eu-south-1",e["ap-east-1"]="ap-east-1",e["ap-south-1"]="ap-south-1",e["ap-southeast-1"]="ap-southeast-1",e["ap-southeast-2"]="ap-southeast-2",e["ap-southeast-3"]="ap-southeast-3",e["ap-northeast-3"]="ap-northeast-3",e["ap-northeast-1"]="ap-northeast-1",e["ap-northeast-2"]="ap-northeast-2",e["sa-east-1"]="sa-east-1",e["af-south-1"]="af-south-1",e["cn-north-1"]="cn-north-1",e["cn-northwest-1"]="cn-northwest-1",e["me-south-1"]="me-south-1"}(Ve||(Ve={}));const We=e=>(e=>e===Ve["cn-north-1"]||e===Ve["cn-northwest-1"])(e)?"https://docs.amazonaws.cn":"https://docs.aws.amazon.com",Ke=({clusterName:e})=>{const t=We(Ve["us-west-2"]);return s().createElement("div",{className:(0,l.cx)(Ce.ModalHeader,"list-cluster-modal-header")},(()=>{let t;if(e){const n=s().createElement("span",{className:Ce.ConnectCluster},e),r=`${p.widgetConnected} `,a=` ${p.connectedWidgetHeader} `;t=s().createElement("div",{className:(0,l.cx)(Ce.ClusterDescription,"list-cluster-description")},r,n,a)}else t=`${p.widgetHeader} `;return t})(),s().createElement(pe,{href:`${t}/sagemaker/latest/dg/studio-notebooks-emr-cluster.html`,type:ue.External},p.learnMore))},Je=(e,t,n)=>{t.execute(e,n)},qe=e=>t=>n=>{Je(e,t,n)},Xe=Object.fromEntries(Object.entries(u).map((e=>{const t=e[0],n=e[1];return[t,(r=n,{id:r,createRegistryWrapper:qe(r),execute:(e,t)=>Je(r,e,t)})];var r}))),Ye=l.css`
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
`;class Ze extends o.ReactWidget{constructor(e,t){super(),this._setSelectedCluster=e=>{var t;(null===(t=this._selectedCluster)||void 0===t?void 0:t.id)!==e.id&&(this._selectedCluster=e)},this.updateConnectedCluster=e=>{this._connectedCluster=e,this.update()},this.getToolTip=()=>this._connectedCluster?`${p.widgetConnected} ${this._connectedCluster.name} cluster`:p.defaultTooltip,this.openSelectAuthType=async e=>{let t={};const n=()=>t&&t.resolve();t=new o.Dialog({title:s().createElement(f,{heading:`${p.selectAuthTitle}"${e.name}"`,shouldDisplayCloseButton:!0,onClickCloseButton:n}),body:Ge(n,this.handleConnect,e).render()}),t.addClass((0,l.cx)(E.ModalBase,E.Footer,Ye)),t.launch()},this.handleConnect=(e,t,n)=>()=>{if(!t)return;this._setSelectedCluster(t);const r=n||((null===(s=(a=t).kerberosAttributes)||void 0===s?void 0:s.kdcAdminPassword)?"Kerberos":(null===(o=a.configurations)||void 0===o?void 0:o.some((e=>{var t;return"ldap"===(null===(t=null==e?void 0:e.properties)||void 0===t?void 0:t.livyServerAuthType)})))?"Basic_Access":null);var a,s,o;r?(e(),this._appContext.commands.execute(Xe.emrConnect.id,{clusterId:t.id,authType:r,language:"python"})):(e(),this.openSelectAuthType(t))},this.clickHandler=async()=>{let e={};const t=()=>e&&e.resolve();e=new o.Dialog({title:s().createElement(f,{heading:p.widgetTitle,shouldDisplayCloseButton:!0,onClickCloseButton:t,className:"list-cluster-modal-header"}),body:Be(t,this.handleConnect,this.listClusterHeader()).render()}),e.handleEvent=t=>{"keydown"===t.type&&(({keyboardEvent:e,onEscape:t,onShiftTab:n,onShiftEnter:r,onTab:a,onEnter:s})=>{const{key:o,shiftKey:l}=e;l?o===g.tab&&n?n():o===g.enter&&r&&r():o===g.tab&&a?a():o===g.enter&&s?s():o===g.escape&&t&&t()})({keyboardEvent:t,onEscape:()=>e.reject()})},e.addClass((0,l.cx)(E.ModalBase,E.Footer,Ye)),e.launch()},this.listClusterHeader=()=>{var e;return s().createElement(Ke,{clusterName:null===(e=this._connectedCluster)||void 0===e?void 0:e.name})},this._selectedCluster=null,this._appContext=t,this._connectedCluster=null,this._kernelId=null}get kernelId(){return this._kernelId}get selectedCluster(){return this._selectedCluster}updateKernel(e){this._kernelId!==e&&(this._kernelId=e,this.kernelId&&this.update())}render(){return s().createElement(h,{handleClick:this.clickHandler,tooltip:this.getToolTip()})}}const Qe=e=>null!=e;var et=n(7704),tt=n.n(et);const nt=e=>{const t=p.presignedURL.sshTunnelLink;return e?s().createElement(pe,{href:e,type:ue.External,hideExternalIcon:!0},t):s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText)},t)},rt=()=>s().createElement(pe,{href:"https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-ssh-tunnel.html",type:ue.External},p.presignedURL.viewTheGuide),at=({sshTunnelLink:e,error:t})=>s().createElement(s().Fragment,null,(()=>{switch(t){case Ee:return s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText)},s().createElement("b",null,p.presignedURL.error),p.presignedURL.clusterNotReady);case fe:return s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText)},s().createElement("b",null,p.presignedURL.error),p.presignedURL.clusterNotConnected);case xe:return(e=>s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText)},s().createElement("b",null,p.presignedURL.error),p.presignedURL.clusterNotCompatible,nt(e),p.presignedURL.or,rt()))(e);default:return(e=>s().createElement("span",null,s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText)},s().createElement("b",null,p.presignedURL.error),p.presignedURL.sparkUIError),nt(e),s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText)},p.presignedURL.or),rt()))(e)}})()),st=(e,t)=>{var n;for(let r=0;r<e.childNodes.length;r++)if(null===(n=e.childNodes[r].textContent)||void 0===n?void 0:n.includes(t))return r;return-1},ot=e=>{try{let t=e.lastElementChild;for(;t;)e.removeChild(t),t=e.lastElementChild}catch(e){}},lt="YARN Application ID",it="Spark UI",ct="--cluster-id",dt="--assumable-role-arn",ut="%info",pt="%configure",mt={childList:!0,subtree:!0};class ht{constructor(e){this.trackedPanels=new Set,this.trackedCells=new Set,this.notebookTracker=e,this.triggers=[gt,ut,pt],this.kernelChanged=!1,this.lastConnectedClusterId=null,this.lastConnectedAccountId=void 0}run(){this.notebookTracker.currentChanged.connect(((e,t)=>{t&&(this.isTrackedPanel(t)||(t.context.sessionContext.kernelChanged.connect(((e,t)=>{this.kernelChanged=!0})),t.context.sessionContext.iopubMessage.connect(((e,n)=>{!this.isTrackedPanel(t)||this.kernelChanged?(n?(this.trackPanel(t),this.handleExistingSparkWidgetsOnPanelLoad(t)):this.stopTrackingPanel(t),this.kernelChanged=!1):this.isTrackedPanel(t)&&this.checkMessageForEmrConnectAndInject(n,t)}))))}))}isTrackedCell(e){return this.trackedCells.has(e)}trackCell(e){this.trackedCells.add(e)}stopTrackingCell(e){this.trackedCells.delete(e)}isTrackedPanel(e){return this.trackedPanels.has(e)}trackPanel(e){this.trackedPanels.add(e)}stopTrackingPanel(e){this.trackedPanels.delete(e)}handleExistingSparkWidgetsOnPanelLoad(e){e.revealed.then((()=>{const t=new RegExp(this.triggers.join("|"));((e,t)=>{var n;const r=null===(n=null==e?void 0:e.content)||void 0===n?void 0:n.widgets;return null==r?void 0:r.filter((e=>{const n=e.model.sharedModel;return t.test(n.source)}))})(e,t).forEach((e=>{if(this.containsSparkMagicTable(e.outputArea.node)){const t=e.model.sharedModel,n=this.getClusterId(t.source),r=this.getAccountId(t.source);this.injectPresignedURL(e,n,r)}else this.injectPresignedURLOnTableRender(e)}))}))}checkMessageForEmrConnectAndInject(e,t){if("execute_input"!==e.header.msg_type)return;const n=e.content.code;var r;this.codeContainsTrigger(n)&&(r=n,t.content.widgets.filter((e=>e.model.sharedModel.source.includes(r)))).forEach((e=>{this.injectPresignedURLOnTableRender(e)}))}codeContainsTrigger(e){const t=this.triggers.filter((t=>e.includes(t)));return De(t)}getParameterFromEmrConnectCommand(e,t){const n=e.split(" "),r=n.indexOf(t);if(!(-1===r||r+1>n.length-1))return n[r+1]}getClusterId(e){return e&&e.includes(ct)?this.getParameterFromEmrConnectCommand(e,ct)||null:this.lastConnectedClusterId}getAccountId(e){if(!e)return this.lastConnectedAccountId;if(e.includes(ut))return this.lastConnectedAccountId;if(e.includes(dt)){const t=this.getParameterFromEmrConnectCommand(e,dt);return void 0!==t?y.fromArnString(t).accountId:void 0}}getSparkMagicTableBodyNodes(e){const t=Array.from(e.getElementsByTagName("tbody"));return De(t)?t.filter((e=>this.containsSparkMagicTable(e))):[]}containsSparkMagicTable(e){var t;return(null===(t=e.textContent)||void 0===t?void 0:t.includes(lt))&&e.textContent.includes(it)}isSparkUIErrorRow(e){var t;return e instanceof HTMLTableRowElement&&(null===(t=e.textContent)||void 0===t?void 0:t.includes(p.presignedURL.error))||!1}injectSparkUIErrorIntoNextTableRow(e,t,n,r){var a;const o=this.isSparkUIErrorRow(t.nextSibling);if(null===r)return void(o&&(null===(a=t.nextSibling)||void 0===a||a.remove()));let l;if(o?(l=t.nextSibling,ot(l)):l=((e,t)=>{let n=1,r=!1;for(let a=1;a<e.childNodes.length;a++)if(e.childNodes[a].isSameNode(t)){n=a,r=!0;break}if(!r)return null;const a=n+1<e.childNodes.length?n+1:-1;return e.insertRow(a)})(e,t),!l)return;const i=l.insertCell(),c=t.childElementCount;i.setAttribute("colspan",c.toString()),i.style.textAlign="left",i.style.background="#212121";const d=s().createElement(at,{sshTunnelLink:n,error:r});tt().render(d,i)}injectPresignedURL(e,t,n){var r;const a=e.outputArea.node,o=e.model.sharedModel,l=this.getSparkMagicTableBodyNodes(a);if(!De(l))return!1;if(o.source.includes(pt)&&l.length<2)return!1;for(let e=0;e<l.length;e++){const a=l[e],o=a.firstChild,i=st(o,it),c=st(o,"Driver log"),d=st(o,lt),u=o.getElementsByTagName("th")[c];if(o.removeChild(u),-1===i||-1===d)break;for(let e=1;e<a.childNodes.length;e++){const o=a.childNodes[e],l=o.childNodes[i];o.childNodes[c].remove();const u=null===(r=l.getElementsByTagName("a")[0])||void 0===r?void 0:r.href;l.hasChildNodes()&&ot(l);const p=o.childNodes[d].textContent||void 0,m=document.createElement("div");l.appendChild(m);const h=s().createElement(we,{clusterId:t,applicationId:p,onError:e=>this.injectSparkUIErrorIntoNextTableRow(a,o,u,e),accountId:n});tt().render(h,m)}}return!0}injectPresignedURLOnTableRender(e){this.isTrackedCell(e)||(this.trackCell(e),new MutationObserver(((t,n)=>{for(const r of t)if("childList"===r.type)try{const t=e.model.sharedModel,r=this.getClusterId(t.source),a=this.getAccountId(t.source);if(this.injectPresignedURL(e,r,a)){this.stopTrackingCell(e),n.disconnect(),this.lastConnectedClusterId=r,this.lastConnectedAccountId=a;break}}catch(t){this.stopTrackingCell(e),n.disconnect()}})).observe(e.outputArea.node,mt))}}const gt="%sm_analytics emr connect",vt=p,bt={id:"@sagemaker-studio:EmrCluster",autoStart:!0,optional:[r.INotebookTracker],activate:async(e,t)=>{null==t||new ht(t).run(),e.docRegistry.addWidgetExtension("Notebook",new Ct(e)),e.commands.addCommand(Xe.emrConnect.id,{label:e=>vt.connectCommand.label,isEnabled:()=>!0,isVisible:()=>!0,caption:()=>vt.connectCommand.caption,execute:async t=>{try{const{clusterId:n,authType:a,language:s,crossAccountArn:o,executionRoleArn:l,notebookPanelToInjectCommandInto:i}=t,c="%load_ext sagemaker_studio_analytics_extension.magics",d=Qe(s)?`--language ${s}`:"",u=Qe(o)?`--assumable-role-arn ${o}`:"",p=Qe(l)?`--emr-execution-role-arn ${l}`:"",m=`${c}\n${gt} --verify-certificate False --cluster-id ${n} --auth-type ${a} ${d} ${u} ${p}`,h=i||(e=>{const t=e.shell.widgets("main");let n=t.next().value;for(;n;){if(n.hasClass("jp-NotebookPanel")&&n.isVisible)return n;n=t.next().value}return null})(e);await(async(e,t,n=!0)=>new Promise((async(a,s)=>{if(t){const o=t.content,l=o.model,i=t.context.sessionContext,{metadata:c}=l.sharedModel.toJSON(),d={cell_type:"code",metadata:c,source:e},u=o.activeCell,p=u?o.activeCellIndex:0;if(l.sharedModel.insertCell(p,d),o.activeCellIndex=p,n)try{await r.NotebookActions.run(o,i)}catch(e){s(e)}const m=[];for(const e of u.outputArea.node.children)m.push(e.innerHTML);a({html:m,cell:u})}s("No notebook panel")})))(m,h)}catch(e){throw e.message,e}}})}};class Ct{constructor(e){this.appContext=e}createNew(e,t){const n=(r=e.sessionContext,a=this.appContext,new Ze(r,a));var r,a;return e.context.sessionContext.kernelChanged.connect((e=>{var t;const r=null===(t=e.session)||void 0===t?void 0:t.kernel;e.iopubMessage.connect(((e,t)=>{((e,t,n,r)=>{if(n)try{if(e.content.text){const{isConnSuccess:t,clusterId:a}=(e=>{let t,n=!1;if(e.content.text){const r=JSON.parse(e.content.text);if("sagemaker-analytics"!==r.namespace)return{};t=r.cluster_id,n=r.success}return{isConnSuccess:n,clusterId:t}})(e);t&&n.id===a&&r(n)}}catch(e){return}})(t,0,n.selectedCluster,n.updateConnectedCluster)})),r&&r.spec.then((e=>{e&&e.metadata&&n.updateKernel(r.id)})),n.updateKernel(null)})),e.toolbar.insertBefore("kernelName","emrCluster",n),n}}const Et=[bt]}}]);
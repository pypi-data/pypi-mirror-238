"use strict";(self.webpackChunk_amzn_sagemaker_jupyter_scheduler=self.webpackChunk_amzn_sagemaker_jupyter_scheduler||[]).push([[652],{4186:(e,t,r)=>{r.r(t),r.d(t,{default:()=>At});var n=r(6271),o=r.n(n),a=r(7363),l=r(6160);const i={ScheduleNoteBook:{MainPanel:{AdvancedOptions:{options:"Advanced Options",environmentVariables:"Environment variables",addEnvironmentvariable:"Add Variable",Key:"Key",Value:"Value",RoleArn:"Role ARN",Image:"Image",Kernel:"Kernel",securityGroup:"Security Group(s)",subnet:"Subnet(s)",s3InputFolder:"Input Folder",s3OutputFolder:"Output Folder",maxRetryAttempts:"Max retry attempts",maxRunTimeInSeconds:"Max run time (in seconds)",selectAdditionalDepency:"Select additional dependencies",efsPlaceholder:"Enter EFS file path",efsLabel:"Initialization script location (optional)",startUpScript:"Start-up script",executionEnv:"Execution enviroment",useVPC:"Use a Virtual Private Cloud (VPC) to run this job",enableEncryption:"Configure job encryption",enterKMSArnOrID:"Enter KMS key ID or ARN",ebsKey:"Job instance volume encryption KMS key",kmsKey:"Output encryption KMS key",Placeholders:{selectOrAdd:"select or add",No:"No",Add:"Add",NoneSelected:"None selected",SelectPrivateSubnets:"Select private subnet(s)",NoPrivateSubnets:"No private subnet(s) available",ImagePlaceHolder:"accountId.dkr.ecr.Region.amazonaws.com/repository[:tag] or [@digest]",KernelPlaceHolder:"kernel name",RolePlaceHolder:"arn:aws:iam::YourAccountID:role/YourRole",S3BucketPlaceHolder:"s3://bucket/path-to-your-data/"}},ErrorMessages:{JobEnvironment:{KernelImageExistError:"Image must be selected"},AdvancedOptions:{ImageError:"Image cannot be empty.",KernelError:"Kernel cannot be empty.",EFSFilePathError:"File path is not valid.",RoleArnLengthError:"Role ARN must have minimum length of 20 and maximum length of 2048.",RoleArnFormatError:"Role ARN is not properly formatted.",S3LengthError:"S3 Path must contain characters.",S3FormatError:"Invalid S3 Path format.",SecurityGroupMinError:"At least one Security Group must be selected when Subnet is selected.",SecurityGroupsMaxError:"Can only have a maximum of 5 Security Groups.",SecurityGroupSGError:"Security Group must start with sg-.",SecurityGroupLengthError:"Security Group must be less than 32 characters.",SecurityGroupFormatError:"Security Group has invalid format.",SubnetMinError:"At least one Subnet must be selected when Security Group is selected.",SubnetsMaxError:"Can only have maximum of 16 subnets.",SubnetLengthError:"Subnet must be less than 32 characters.",SubnetsFormatError:"One or more subnets has invalid format.",EnvironmentVariableEmptyError:"Key or Value cannot be empty.",EnvironmentVariableLengthError:"Key or Value cannot be more than 512 characters.",EnvironmentVariableFormatError:"Key or Value has invalid format.",KMSKeyError:"KMS key has invalid format.",MaxRetryAttemptsError:"Invalid max retry attempts must have a minimum value of 1 and a maximum value of 30.",MaxRunTimeInSecondsError:"Invalid max run time must have a minimum value of 1."},VPCErrors:{RequiresPrivateSubnet:"Running notebook jobs in a VPC requires the virtual network to use a private subnet.",NoPrivateSubnetsInSageMakerDomain:"There are no private subnets associated with your SageMaker Studio domain",YouMayChooseOtherSubnets:"You may choose to run the job using other private subnets associated with this VPC"}},Tooltips:{ImageTooltipText:"Enter the ECR registry path of the Docker image that contains the required Kernel & Libraries to execute the notebook. sagemaker-base-python-38 is selected by default",KernelTooltipText:"Enter the display name of kernel to execute the given notebook. This kernel should be installed in the above image.",LCCScriptTooltipText:"Select a lifecycle configuration script that will be run on image start-up.",VPCTooltip:"Configure the virtual network to run this job in a Virtual Private Cloud (VPC).",KMSTooltip:"Configure the cryptographic keys used to encrypt files in the job.",RoleArnTooltip:"Enter the IAM Role ARN with appropriate permissions needed to execute the notebook. By default Role name with prefix SagemakerJupyterScheduler is selected",SecurityGroupsTooltip:"Specify or add security group(s) of the desired VPC.",SubnetTooltip:"Specify or add Private subnet(s) of the desired VPC.",InputFolderTooltip:"Enter the S3 location to store the input artifacts like notebook and script.",OutputFolderTooltip:"Enter the S3 location to store the output artifacts.",InitialScriptTooltip:"Enter the file path of a local script to run before the notebook execution.",EnvironmentVariablesTooltip:"Enter key-value pairs that will be accessible in your notebook.",kmsKeyTooltip:"If you want Amazon SageMaker to encrypt the output of your notebook job using your own AWS KMS encryption key instead of the default S3 service key, provide its ID or ARN",ebsKeyTooltip:"Encrypt data on the storage volume attached to the compute instance that runs the scheduled job.",LearnMore:"Learn more",MaxRetryAttempts:"Enter a minimum value of 1 and a maximum value of 30.",MaxRunTimeInSeconds:"Enter a minimum value of 1."},StudioTooltips:{ImageTooltipText:"Select available SageMaker image.",KernelTooltipText:"Select available SageMaker Kernel.",RoleArnTooltip:"Specify a role with permission to create a notebook job.",SecurityGroupsTooltip:"Specify or add security group(s) that have been created for the default VPC. For better security, we recommend that you use a private VPC.",SubnetTooltip:"Specify or add subnet(s) that have been created for the default VPC. For better security, we recommend that you use a private VPC.",InputFolderTooltip:"Enter the S3 location where the input folder it is located.",OutputFolderTooltip:"Enter the S3 location where the output folder it is located.",InitialScriptTooltip:"Enter the EFS file path where a local script or a lifecycle configuration script is located."}}},ImageSelector:{label:"Image"},KernelSelector:{label:"Kernel",imageSelectorOption:{linkText:"More Info"}},Dialog:{awsCredentialsError:{title:"You’re not authenticated to your AWS account.",body:{text:["You haven’t provided AWS security keys or they expired. Authenticate to your AWS account with valid security keys before creating a notebook job.","Note that you must have an AWS account configured with a proper role to create notebook jobs. See %{schedulerInformation} for instructions."],links:{schedulerInformation:{linkString:"Notebook Scheduler information",linkHref:"https://docs.aws.amazon.com/sagemaker/latest/dg/notebook-auto-run.html"}}},buttons:{goToIamConsole:"Go to IAM console",enterKeysInTerminal:"Run `aws configure` in Terminal"}}}},s={expiredToken:"ExpiredToken",invalidClientTokenId:"InvalidClientTokenId",noCredentials:"NoCredentials"},u="terminal:create-new";var c,m=r(5185),d=r(3626),p=r(6516),v=r(1396),g=r(6247);!function(e){e.PublicInternetOnly="PublicInternetOnly",e.VpcOnly="VpcOnly"}(c||(c={}));var b,h,E=r(9849),f=r(9208),y=r(1982);!function(e){e[e.Large=0]="Large",e[e.Medium=1]="Medium",e[e.Small=2]="Small"}(b||(b={})),function(e){e.Filled="filled"}(h||(h={}));const _={[b.Large]:"var(--jp-content-line-height-3)",[b.Medium]:"var(--jp-content-line-height-2)",[b.Small]:"var(--jp-content-line-height-1-25)"},S={[b.Large]:"1em",[b.Medium]:"0.5em",[b.Small]:"0.25em"},k=e=>y.css`
  root: {
    background: 'var(--jp-input-active-background)',
    borderTopLeftRadius: 'var(--jp-border-radius)',
    borderTopRightRadius: 'var(--jp-border-radius)',
    fontSize: 'var(--jp-ui-font-size2)',
    '&.Mui-focused': {
      background: 'var(--jp-input-active-background)',
    },
    '&.Mui-disabled': {
      borderRadius: 'var(--jp-border-radius)',
      color: 'var(--text-input-font-color-disabled)',
    },
    '&.MuiInput-underline.Mui-disabled:before': {
      borderBottom: 'none',
    },
  },
  underline: {
    borderBottom: 'none',
    '&:before': {
      borderBottom: 'var(--jp-border-width) solid',
    },
    '&:after': {
      borderBottom: 'var(--jp-border-width) solid',
    },
    '&:not(.Mui-disabled):hover:before': {
      borderBottom: 'var(--jp-border-width) solid',
    },
    '&.Mui-error:hover:after': {
      borderBottom: 'var(--jp-border-width) solid',
    },
    '&.Mui-error:after': {
      borderBottom: 'var(--jp-border-width) solid',
    },
  },
  input: {
    color: 'var(--jp-ui-font-color0)',
    lineHeight: ${_[e]},
    padding: ${S[e]},
  },   
`,x=(y.css`
  root: {
    fontFamily: 'var(--jp-cell-prompt-font-family)',
    color: 'var(--jp-input-border-color)',
    marginBottom: 'var(--padding-small)',
    '&.Mui-error': {
      fontFamily: 'var(--jp-cell-prompt-font-family)',
      color: 'var(--jp-error-color1)',
    },
    '&.Mui-disabled': {
      fontFamily: 'var(--jp-cell-prompt-font-family)',
      color: 'var(--jp-error-color1)',
    },
  },
`,({classes:e,className:t,InputProps:r,FormHelperTextProps:n,size:a=b.Medium,variant:l,...i})=>{var s,u,c;const m=(0,y.cx)(y.css`
  .MuiFormHelperText-root.Mui-error::before {
    display: inline-block;
    vertical-align: middle;
    background-size: 1rem 1rem;
    height: var(--text-input-error-icon-height);
    width: var(--text-input-error-icon-width);
    background-image: var(--text-input-helper-text-alert-icon);
    background-repeat: no-repeat;
    content: ' ';
  }
`,t,null==e?void 0:e.root);return o().createElement(E.TextField,{"data-testid":"inputField",classes:{root:m,...e},variant:l,role:"textField",InputProps:{...r,classes:{root:(0,y.cx)(k(a),null===(s=null==r?void 0:r.classes)||void 0===s?void 0:s.root),input:(0,y.cx)(k(a),null===(u=null==r?void 0:r.classes)||void 0===u?void 0:u.input)}},FormHelperTextProps:{...n,classes:{root:(0,y.cx)(y.css`
    fontSize: 'var(--jp-ui-font-size0)',
    color: 'var(--text-input-helper-text)',
    '&.Mui-error': {
      color: 'var(--jp-error-color1)',
    },
    '&.Mui-disabled': {
      color: 'var(--jp-error-color1)',
    },
`,null===(c=null==n?void 0:n.classes)||void 0===c?void 0:c.root)}},...i})});var w,M=r(4129);!function(e){e.TopStart="top-start",e.Top="top",e.TopEnd="top-end",e.RightStart="right-start",e.Right="right",e.RightEnd="right-end",e.BottomStart="bottom-start",e.Bottom="bottom",e.BottomEnd="bottom-end",e.LeftStart="left-start",e.Left="left",e.LeftEnd="left-end"}(w||(w={}));const P=({children:e,classes:t,className:r,placement:n=w.Right,...a})=>{const l=(0,y.cx)(r,y.css`
  popper: {
    '& .MuiTooltip-tooltip': {
      backgroundColor: 'var(--color-light)',
      boxShadow: 'var(--tooltip-shadow)',
      color: 'var(--tooltip-text-color',
      padding: 'var(--padding-16)',
      fontSize: 'var(--font-size-0)',
    },
  },
`,null==t?void 0:t.popper);return o().createElement(M.Z,{...a,arrow:!0,classes:{popper:l,tooltip:y.css`
  tooltip: {
    '& .MuiTooltip-arrow': {
      color: 'var(--tooltip-surface)',
      '&:before': {
        boxShadow: 'var(--tooltip-shadow)',
      },
    },
  },
`},placement:n,"data-testid":"toolTip"},e)},T=y.css`
  display: flex;
  flex-direction: column;
`,j=y.css`
  display: flex;
  flex-direction: column;
`,C=y.css`
  display: inline-flex;
  svg {
    width: 0.75em;
    height: 0.75em;
    transform: translateY(-2px);
  }
`,I=y.css`
  svg {
    width: 0.75em;
    height: 0.75em;
    transform: translateY(1px);
  }
`,N=(e=!1)=>y.css`
  display: flex;
  flex-direction: column;
  ${e?"":"max-width : 500px;"}
  .MuiCheckbox-colorPrimary.Mui-checked {
    color: var(--jp-brand-color1);
  }
  .MuiButton-containedPrimary:hover {
    background-color: var(--jp-brand-color1);
  }
`,O=y.css`
  font-size: var(--jp-content-font-size1);
`,F=y.css`
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 0.5rem;
  svg {
    width: var(--jp-ui-font-size1);
    height: var(--jp-ui-font-size1);
    path {
      fill: var(--jp-error-color1);
    }
  }
`,V=(e=!1)=>y.css`
  color: var(--jp-color-root-light-800);
  font-weight: 400;
  font-size: var(--jp-ui-font-size1);
  line-height: var(--jp-ui-font-size1);
  margin-bottom: var(--jp-ui-font-size1);
  ${e&&"\n    &:after {\n      content: '*';\n      color: var(--jp-error-color1);\n    }\n  "}
`;var A,R;!function(e){e.External="_blank",e.Content="_self"}(A||(A={})),function(e){e.None="none",e.Hover="hover",e.Always="always"}(R||(R={}));const z=({className:e,disabled:t=!1,children:r,onClick:n,target:a=A.Content,...l})=>{const i=a===A.External,s={...l,className:(0,y.cx)(y.css`
  cursor: pointer;
  text-decoration: none;
  color: var(--jp-brand-color1);

  &:hover {
    text-decoration: none;
    color: var(--jp-brand-color1);
  }
`,e),target:a,onClick:t?void 0:n,rel:i?"noopener noreferrer":void 0};return o().createElement(E.Link,{...s,"data-testid":"link"},r)};r(78);const K=e=>"string"==typeof e&&e.length>0;var L=r(5505),D=r.n(L);function J(e){try{if(!D()(e)||0===e.length)return{kernel:null,arnEnvironment:null,version:null};const t=e.split("__SAGEMAKER_INTERNAL__"),[r,n]=t,o=n&&n.split("/"),a=o&&o[0]+"/"+o[1],l=3===o.length?o[2]:null;return{kernel:r,arnEnvironment:l?`${a}/${l}`:a,version:l}}catch(e){return{kernel:null,arnEnvironment:null,version:null}}}const B=({labelInfo:e,required:t,toolTipText:r,errorMessage:n,...a})=>o().createElement("div",{className:j},o().createElement("div",{className:C},o().createElement("label",{className:V(t)}," ",e," "),r&&!a.readOnly&&o().createElement(P,{title:r,className:I},o().createElement(f.Z,null))),o().createElement(x,{...a,error:K(n),helperText:n,InputProps:{readOnly:a.readOnly,...a.InputProps}}));var G=r(6433);y.css`
  box-sizing: border-box;
  width: 100%;
  padding: var(--jp-padding-large);
  flex-direction: column;
  display: flex;
  color: var(--jp-ui-font-color0);
`,y.css`
  width: 100%;
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;
  padding-bottom: var(--jp-padding-20);
  color: var(--jp-ui-font-color0);
`,y.css`
  max-width: 525px;
  color: var(--jp-ui-font-color2);
  margin-bottom: var(--jp-padding-medium);
`,y.css`
  display: block;
  margin-bottom: 0.5em;
  overflow-y: scroll;
`,y.css`
  align-items: center;
  display: inline-flex;
  margin-bottom: var(--jp-padding-16);
  margin-left: 1em;
  font-size: var(--jp-ui-font-size3);
  color: var(--jp-ui-font-color0);
`;const $=y.css`
  display: flex;
  flex-direction: column;
  font-size: 12px;
  color: var(--jp-ui-font-color0);
  padding: 10px;
  overflow-x: auto;
  overflow-y: hidden;
  gap: 20px;
`,q=(y.css`
  display: flex;
  justify-content: space-between;
`,y.css`
  display: flex;
  align-items: center;
`,y.css`
  margin-bottom: var(--jp-padding-medium);
`,y.css`
  width: 50% !important;
  text-align: center;
  height: 30px;
  font-size: 12px !important;
`,y.css`
  display: inline-flex;
  justify-content: right;
`,y.css`
  height: fit-content;
  width: 90px;
  text-align: center;
  margin-right: var(--jp-padding-medium);
`,y.css`
  position: absolute;
  right: 0%;
  bottom: 0%;
  margin-bottom: var(--jp-padding-large);
`,y.css`
  div:nth-child(2) {
    width: 98%;
  }
`,y.css`
  div:nth-child(2) {
    width: 49%;
  }
`,y.css`
  div:nth-child(2) {
    width: 150px;
  }
`,y.css`
  width: 500px;
  margin-bottom: var(--jp-size-4);
`),Z=y.css`
  display: flex;
  align-items: center;
`,H=y.css`
  display: flex;
  align-items: center;
`,U=y.css`
  color: var(--jp-brand-color3);
`,Y=y.css`
  padding: 4px;
`,W=y.css`
  color: var(--jp-ui-font-color0);
`,Q=y.css`
  display: flex;
  flex-direction: column;
  gap: var(--jp-ui-font-size1);
`,X=y.css`
  color: var(--jp-error-color1);
  padding: 12px;
`,ee=i.ScheduleNoteBook.MainPanel.ErrorMessages.VPCErrors,te=i.ScheduleNoteBook.MainPanel.AdvancedOptions,re=i.ScheduleNoteBook.MainPanel.Tooltips,ne=o().createElement("div",null,o().createElement("span",{className:H}," ",re.VPCTooltip," "),o().createElement(z,{href:"https://docs.aws.amazon.com/sagemaker/latest/dg/create-notebook-auto-execution-advanced.html",target:A.External},o().createElement("p",{className:U},i.ScheduleNoteBook.MainPanel.Tooltips.LearnMore))),oe=({isChecked:e,formState:t,formErrors:r,initialSecurityGroups:n,initialSubnets:a,availableSubnets:l,setFormErrors:i,setChecked:s,setFormState:u,...c})=>o().createElement("div",{className:Z},o().createElement(G.Z,{name:"vpc-check-box",className:Y,color:"primary",checked:e,onChange:e=>{const o=e.target.checked;if(s(o),o){if(u({...t,vpc_security_group_ids:n,vpc_subnets:a}),0===a.length&&l.length>0)return void i({...r,subnetError:`${ee.RequiresPrivateSubnet} ${ee.NoPrivateSubnetsInSageMakerDomain}. ${ee.YouMayChooseOtherSubnets}`});0===l.length&&i({...r,subnetError:`${ee.RequiresPrivateSubnet} ${ee.NoPrivateSubnetsInSageMakerDomain}`})}else u({...t,vpc_security_group_ids:[],vpc_subnets:[]}),i({...r,subnetError:"",securityGroupError:""})},...c}),o().createElement("label",null,te.useVPC),o().createElement(P,{classes:{popperInteractive:W},title:ne},o().createElement(f.Z,{fontSize:"small"})));var ae=r(9419),le=r(2679),ie=r(4085);const se=y.css`
  display: flex;
  align-items: flex-end;
  padding-right: 1em;
  gap: 20px;
`,ue=y.css`
  display: flex;
  flex-direction: column;
`,ce=y.css`
  width: 170px;
`,me=(y.css`
  display: flex;
  flex-direction: column;
  margin-bottom: var(--jp-padding-large);
`,y.css`
  display: flex;
  flex-direction: column;
  gap: 16px;
`),de=y.css`
  font-weight: 400;
  font-size: var(--jp-ui-font-size1);
  line-height: var(--jp-ui-font-size1);
`,pe=y.css`
  background-color: var(--jp-brand-color1);
  font-size: var(--jp-ui-font-size1);
  text-transform: none;
`,ve=y.css`
  display: inline-flex;
  align-items: center;
  gap: 6px;
  svg {
    width: 0.75em;
    height: 0.75em;
  }
`,ge=new RegExp("[a-zA-Z_][a-zA-Z0-9_]*"),be=new RegExp("[\\S\\s]*"),he=i.ScheduleNoteBook.MainPanel.ErrorMessages.AdvancedOptions,Ee=i.ScheduleNoteBook.MainPanel.AdvancedOptions,fe=({isDisabled:e,environmentParameters:t,setEnvironmentParameters:r,index:n,formErrors:a,setFormErrors:l})=>{const i=t[n],s=e=>{const n=e.currentTarget.name,o=e.target.value,[a,l]=n.split("-"),i="envKey"===a?{key:o,value:t[l].value}:{key:t[l].key,value:o},s=[...t];s.splice(l,1,i),r(s)},u=()=>{const{key:e,value:t}=i;e.length<1||t.length<1?l({...a,environmentVariablesError:he.EnvironmentVariableEmptyError}):e.length>512||t.length>512?l({...a,environmentVariablesError:he.EnvironmentVariableLengthError}):ge.test(e)&&be.test(t)?l({...a,environmentVariablesError:""}):l({...a,environmentVariablesError:he.EnvironmentVariableFormatError})};return o().createElement("div",{className:se},o().createElement(B,{className:ce,readOnly:e,name:`envKey-${n}`,labelInfo:Ee.Key,value:t[n].key,onChange:s,onBlur:u}),o().createElement(B,{className:ce,readOnly:e,name:`envValue-${n}`,labelInfo:Ee.Value,value:t[n].value,onChange:s,onBlur:u}),o().createElement("div",null,!e&&o().createElement(ie.Z,{onClick:()=>{(e=>{const n=[...t];n.splice(e,1),r(n),l({...a,environmentVariablesError:""})})(n),l({...a,environmentVariablesError:""})},size:"large"},o().createElement(le.Z,null))))},ye=i.ScheduleNoteBook.MainPanel.AdvancedOptions,_e=i.ScheduleNoteBook.MainPanel.Tooltips,Se=({allFieldsDisabled:e,isButtonDisabled:t,environmentVariables:r,setEnvironmentVariables:n,formErrors:a,...l})=>{const i=!!a.environmentVariablesError,s=o().createElement("div",{className:F},o().createElement(ae.Z,{severity:"error"},a.environmentVariablesError));return o().createElement("div",{className:me},o().createElement("div",{className:ve},o().createElement("label",{className:de},ye.environmentVariables),e?null:o().createElement(P,{title:_e.EnvironmentVariablesTooltip},o().createElement(f.Z,null))),e&&0===r.length?o().createElement("div",{className:ue},o().createElement(x,{InputProps:{readOnly:!0},placeholder:ye.Placeholders.NoneSelected})):o().createElement(o().Fragment,null,r.map(((t,i)=>o().createElement(fe,{isDisabled:e,key:i,environmentParameters:r,setEnvironmentParameters:n,index:i,formErrors:a,...l})))),i&&o().createElement("div",null,s),!e&&o().createElement("div",null,o().createElement(E.Button,{disabled:t,className:pe,variant:"contained",color:"primary",size:"small",onClick:()=>{n([...r,{key:"",value:""}])}},ye.addEnvironmentvariable)))};var ke=r(8992),xe=r(7338),we=r(1360);const Me=(0,ke.D)(),Pe=({label:e,required:t,errorMessage:r,disabled:n,renderInput:a,tooltip:l,disabledTooltip:i,freeSolo:s,options:u,...c})=>{var m,d;null!=a||(a=t=>o().createElement(we.Z,{...t,variant:"outlined",size:"small",margin:"dense",placeholder:e}));const p=n?i?o().createElement(P,{title:i,className:I},o().createElement(f.Z,null)):o().createElement(o().Fragment,null):l?o().createElement(P,{title:l,className:I},o().createElement(f.Z,null)):o().createElement(o().Fragment,null),v=r?o().createElement("div",{className:F},o().createElement(ae.Z,{severity:"error"},r)):o().createElement(o().Fragment,null);return o().createElement("div",{className:T},o().createElement("div",{className:C},o().createElement("label",{className:V(t)},e),p),o().createElement(xe.Z,{...c,multiple:!0,renderInput:a,freeSolo:s,readOnly:n,options:u,filterOptions:(e,t)=>{const r=Me(e,t);return""===t.inputValue||e.includes(t.inputValue)||r.push(t.inputValue),r},renderOption:(e,t,r)=>(u.includes(t)||(t=`Add "${t}"`),o().createElement("li",{...e},t)),componentsProps:{...c.componentsProps,popupIndicator:{...null===(m=c.componentsProps)||void 0===m?void 0:m.popupIndicator,size:"small"},clearIndicator:{...null===(d=c.componentsProps)||void 0===d?void 0:d.clearIndicator,size:"small"}}}),v)},Te=new RegExp("^(https|s3)://([^/]+)/?(.*)$"),je=new RegExp("[-0-9a-zA-Z]+"),Ce=new RegExp("^arn:aws[a-z\\-]*:iam::\\d{12}:role/?[a-zA-Z_0-9+=,.@\\-_/]+$"),Ie=new RegExp("^arn:aws:kms:\\w+(?:-\\w+)+:\\d{12}:key\\/[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+$"),Ne=new RegExp("^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$"),Oe=i.ScheduleNoteBook.MainPanel.ErrorMessages,Fe=Oe.VPCErrors,Ve=e=>e.length<20||e.length>2048?Oe.AdvancedOptions.RoleArnLengthError:Ce.test(e)?"":Oe.AdvancedOptions.RoleArnFormatError,Ae=e=>0===e.trim().length?Oe.AdvancedOptions.S3LengthError:Te.test(e)?"":Oe.AdvancedOptions.S3FormatError,Re=e=>0===e.length||Ie.test(e)||Ne.test(e)?"":Oe.AdvancedOptions.KMSKeyError;var ze;!function(e){e.LocalJL="local-jupyter-lab",e.JupyterLab="jupyterlab",e.Studio="studio"}(ze||(ze={}));class Ke{get isStudio(){return this.type===ze.Studio}get isLocalJL(){return this.type===ze.LocalJL}get isJupyterLab(){return this.type===ze.JupyterLab}constructor(e){this.type=e}}const Le=(0,n.createContext)(void 0);function De({app:e,children:t}){const[r,a]=(0,n.useState)((()=>function(e){return e.hasPlugin("@amzn/sagemaker-ui:project")?new Ke(ze.Studio):e.hasPlugin("@amzn/sagemaker-jupyterlab-extensions:sessionmanagement")?new Ke(ze.JupyterLab):new Ke(ze.LocalJL)}(e))),l={pluginEnvironment:r,setPluginEnvironment:a};return o().createElement(Le.Provider,{value:l},t)}function Je(){const e=(0,n.useContext)(Le);if(void 0===e)throw new Error("usePluginEnvironment must be used within a PluginEnvironmentProvider");return e}var Be=r(2346),Ge=r(3274),$e=r(8102);const qe=i.ScheduleNoteBook.MainPanel.AdvancedOptions,Ze=i.ScheduleNoteBook.MainPanel.Tooltips,He=i.ScheduleNoteBook.MainPanel.StudioTooltips,Ue=i.ScheduleNoteBook.MainPanel.ErrorMessages,Ye=o().createElement("div",null,o().createElement("span",{className:H},Ze.kmsKeyTooltip),o().createElement(z,{href:"https://docs.aws.amazon.com/sagemaker/latest/dg/create-notebook-auto-execution-advanced.html",target:A.External},o().createElement("p",{className:U},Ze.LearnMore))),We=o().createElement("div",null,o().createElement("span",{className:H},Ze.LCCScriptTooltipText),o().createElement(z,{href:"https://aws.amazon.com/blogs/machine-learning/customize-amazon-sagemaker-studio-using-lifecycle-configurations/",target:A.External},o().createElement("p",{className:U},Ze.LearnMore))),Qe=({isDisabled:e,formState:t,formErrors:r,environmentVariables:a,setEnvironmentVariables:l,lccOptions:i,availableSecurityGroups:s,availableSubnets:u,initialSubnets:c,initialSecurityGroups:m,isVPCDomain:d,requestClient:p,enableVPCSetting:b,userDefaultValues:h,setFormState:y,handleChange:_,handleNumberValueChange:S,setSubnets:k,setSecurityGroups:x,onSelectLCCScript:w,setFormValidationErrors:M,setEnableVPCSetting:T,setRoleArn:j})=>{const{pluginEnvironment:C}=Je(),[I,N]=(0,n.useState)(!1),[O,F]=(0,n.useState)(!1),V=e=>{const t=e.target.name,n=Ae(e.target.value);M({...r,["s3_input"===t?"s3InputFolderError":"s3OutputFolderError"]:n})},A=e=>{const t=e.target.name,n=Re(e.target.value);M({...r,["sm_output_kms_key"===t?"outputKMSError":"ebsKMSError"]:n})};return o().createElement("div",{className:$},o().createElement(B,{"aria-label":"role_arn",name:"role_arn",disabled:O,readOnly:e,required:!0,labelInfo:qe.RoleArn,errorMessage:r.roleError,placeholder:qe.Placeholders.RolePlaceHolder,onChange:_,value:t.role_arn,onBlur:e=>{const{value:t}=e.target,n=Ve(t);j(t),M({...r,roleError:n})},toolTipText:C.isStudio?He.RoleArnTooltip:Ze.RoleArnTooltip}),o().createElement(B,{name:"s3_input",onChange:_,required:!0,disabled:O,readOnly:e,value:t.s3_input,placeholder:qe.Placeholders.S3BucketPlaceHolder,labelInfo:qe.s3InputFolder,errorMessage:r.s3InputFolderError,onBlur:V,toolTipText:C.isStudio?He.InputFolderTooltip:Ze.InputFolderTooltip}),o().createElement(B,{name:"s3_output",onChange:_,required:!0,disabled:O,readOnly:e,value:t.s3_output,placeholder:qe.Placeholders.S3BucketPlaceHolder,labelInfo:qe.s3OutputFolder,errorMessage:r.s3OutputFolderError,onBlur:V,toolTipText:C.isStudio?He.OutputFolderTooltip:Ze.OutputFolderTooltip}),!e&&o().createElement("div",{className:Z},o().createElement(E.Checkbox,{"data-testid":"kms_checkbox",name:"kms_checkbox",className:Y,color:"primary",checked:I,onChange:e=>{const n=e.target.checked;N(n);const o=n?h.sm_output_kms_key:"",a=n?h.sm_volume_kms_key:"";y({...t,sm_output_kms_key:o,sm_volume_kms_key:a}),M({...r,outputKMSError:Re(o),ebsKMSError:Re(a)})}}),o().createElement("label",null,qe.enableEncryption),o().createElement(P,{classes:{popperInteractive:W},title:Ye},o().createElement(f.Z,{fontSize:"small"}))),(e||I)&&o().createElement(o().Fragment,null,o().createElement(B,{name:"sm_output_kms_key",onChange:_,required:!1,readOnly:e,disabled:O,value:t.sm_output_kms_key,placeholder:e?qe.Placeholders.NoneSelected:qe.enterKMSArnOrID,labelInfo:qe.kmsKey,errorMessage:r.outputKMSError,onBlur:A,toolTipText:e?void 0:Ze.kmsKeyTooltip}),o().createElement(B,{name:"sm_volume_kms_key",onChange:_,required:!1,readOnly:e,disabled:O,value:t.sm_volume_kms_key,placeholder:e?qe.Placeholders.NoneSelected:qe.enterKMSArnOrID,labelInfo:qe.ebsKey,errorMessage:r.ebsKMSError,onBlur:A,toolTipText:e?void 0:Ze.ebsKeyTooltip})),d&&!e&&o().createElement(oe,{isChecked:b,setChecked:T,initialSecurityGroups:m,initialSubnets:c,availableSubnets:u,formState:t,formErrors:r,setFormErrors:M,setFormState:y,"data-testid":"vpc-checkbox"}),(d&&b||e)&&o().createElement(o().Fragment,null,o().createElement(Pe,{required:!0,name:"vpc_subnets",disabled:e||C.isStudio&&0===u.length,label:qe.subnet,options:u,value:t.vpc_subnets,onChange:(e,n,o)=>{const[a,l]=((e,t)=>{if(0===e.length)return 0===t.length?["",""]:[Oe.AdvancedOptions.SubnetMinError,void 0];if(e&&e.length>0){if(e.length>16)return[Oe.AdvancedOptions.SubnetsMaxError,void 0];for(const t of e){if(t.length>32)return[Oe.AdvancedOptions.SubnetLengthError,void 0];if(!je.test(t))return[Oe.AdvancedOptions.SubnetsFormatError,void 0]}if(0===t.length)return["",Oe.AdvancedOptions.SecurityGroupMinError]}return["",void 0]})(n,t.vpc_security_group_ids);k(n),M({...r,securityGroupError:null!=l?l:r.securityGroupError,subnetError:null!=a?a:""})},errorMessage:r.subnetError,placeholder:`${qe.Placeholders.SelectPrivateSubnets}`,tooltip:C.isStudio?He.SubnetTooltip:Ze.SubnetTooltip,disabledTooltip:`${qe.Placeholders.NoPrivateSubnets}`,freeSolo:!0}),o().createElement(Pe,{required:!0,className:"securityGroupSelector",name:"vpc_security_group_ids",disabled:e||C.isStudio&&0===s.length,label:qe.securityGroup,options:s,value:t.vpc_security_group_ids,onChange:(e,n,o)=>{const[a,l]=((e,t)=>{if(0===e.length)return 0===t.length?["",""]:[Oe.AdvancedOptions.SecurityGroupMinError,void 0];if(e.length>0){if(e.length>5)return[Oe.AdvancedOptions.SecurityGroupsMaxError,void 0];for(const t of e){if(!t.startsWith("sg-"))return[Oe.AdvancedOptions.SecurityGroupSGError,void 0];if(t.length>32)return[Oe.AdvancedOptions.SecurityGroupLengthError,void 0];if(!je.test(t))return[Oe.AdvancedOptions.SecurityGroupFormatError,void 0]}if(0===t.length)return["",Oe.AdvancedOptions.SubnetMinError]}return["",void 0]})(n,t.vpc_subnets);x(n),M({...r,securityGroupError:null!=a?a:"",subnetError:null!=l?l:r.subnetError})},errorMessage:r.securityGroupError,placeholder:`${qe.Placeholders.selectOrAdd} ${qe.securityGroup}`,tooltip:C.isStudio?He.SecurityGroupsTooltip:Ze.SecurityGroupsTooltip,disabledTooltip:`${qe.Placeholders.No} ${qe.securityGroup}`,freeSolo:!0})),C.isStudio&&o().createElement("div",{className:Q},o().createElement($e.Z,{id:"startup-script-select-label"},qe.startUpScript,o().createElement(P,{title:We},o().createElement(f.Z,{fontSize:"small"}))),o().createElement(Be.Z,{labelId:"startup-script-select-label",id:"startup-script-select",disabled:O,readOnly:e,value:t.sm_lcc_init_script_arn,onChange:e=>w(e.target.value)},i&&i.map((e=>o().createElement(Ge.Z,{key:e,value:e},e))))),o().createElement(Se,{isButtonDisabled:e||a.length>=48||!!r.environmentVariablesError,allFieldsDisabled:e,environmentVariables:a,setEnvironmentVariables:l,formErrors:r,setFormErrors:M}),o().createElement("div",null,o().createElement(B,{placeholder:e?qe.Placeholders.NoneSelected:qe.efsPlaceholder,labelInfo:qe.efsLabel,required:!1,value:t.sm_init_script,name:"sm_init_script",readOnly:e,disabled:O,errorMessage:r.efsFilePathError,onChange:_,onBlur:e=>{const t=e.target.value;0===t.trim().length?M({...r,efsFilePathError:""}):(async e=>{const t=v.URLExt.join(p.baseUrl,"/validate_volume_path");F(!0);const n=await g.ServerConnection.makeRequest(t,{method:"POST",body:JSON.stringify({file_path:e})},p);F(!1),200!==n.status||!0===(await n.json()).file_path_exist?M({...r,efsFilePathError:""}):M({...r,efsFilePathError:Ue.AdvancedOptions.EFSFilePathError})})(t)},toolTipText:e?void 0:C.isStudio?He.InitialScriptTooltip:Ze.InitialScriptTooltip})),o().createElement(B,{name:"max_retry_attempts",type:"number",onChange:S,required:!0,disabled:O,readOnly:e,value:t.max_retry_attempts,placeholder:qe.maxRetryAttempts,labelInfo:qe.maxRetryAttempts,errorMessage:r.maxRetryAttemptsError,onBlur:e=>{const t=(e=>{const t=parseInt(e);return isNaN(t)||t<0||t>30?Oe.AdvancedOptions.MaxRetryAttemptsError:""})(e.target.value);M({...r,maxRetryAttemptsError:t})},toolTipText:Ze.MaxRetryAttempts}),o().createElement(B,{name:"max_run_time_in_seconds",type:"number",onChange:S,required:!0,disabled:O,readOnly:e,value:t.max_run_time_in_seconds,placeholder:qe.maxRunTimeInSeconds,labelInfo:qe.maxRunTimeInSeconds,errorMessage:r.maxRunTimeInSecondsError,onBlur:e=>{const t=(e=>{const t=parseInt(e);return isNaN(t)||t<0?Oe.AdvancedOptions.MaxRunTimeInSecondsError:""})(e.target.value);M({...r,maxRunTimeInSecondsError:t})},toolTipText:Ze.MaxRunTimeInSeconds}))},Xe="No script",et=new Set(["sm_kernel","sm_image","sm_lcc_init_script_arn","role_arn","vpc_security_group_ids","vpc_subnets","s3_input","s3_output","sm_init_script","sm_output_kms_key","sm_volume_kms_key","max_run_time_in_seconds","max_retry_attempts"]),tt=(e,t,r,n)=>{var o,a;if(r===l.JobsView.JobDetail||r===l.JobsView.JobDefinitionDetail){if(e)return e[n]?e[n].split(","):[]}else if(r===l.JobsView.CreateForm){if(e&&n in e){const t=e[n];return t?t.split(","):[]}const r=null===(o=null==t?void 0:t.find((e=>e.name===n)))||void 0===o?void 0:o.value;return(null===(a=null==r?void 0:r.filter((e=>e.is_selected)))||void 0===a?void 0:a.map((e=>e.name)))||[]}return[]},rt=(e,t,r,n)=>{var o;if(r===l.JobsView.JobDetail||r===l.JobsView.JobDefinitionDetail){if(e)return e[n]}else if(r===l.JobsView.CreateForm)return e&&n in e?e[n]:(null===(o=null==t?void 0:t.find((e=>e.name===n)))||void 0===o?void 0:o.value)||"";return""},nt=(e,t,r,n)=>{if(t===l.JobsView.JobDetail||t===l.JobsView.JobDefinitionDetail){if(e)return e[n]}else if(t===l.JobsView.CreateForm&&e&&n in e)return e[n];return r},ot=(e,t,r)=>{if(t===l.JobsView.JobDetail||t===l.JobsView.JobDefinitionDetail){if(e)return e[r]}else if(t===l.JobsView.CreateForm&&e&&r in e)return e[r];return""},at=({label:e,value:t,options:r,onChange:n,freeSolo:a,customListItemRender:l,renderInput:i,...s})=>{var u;const c=Object.fromEntries(r.map((e=>[e.value,e])));let m=t;return!a&&"string"==typeof t&&t in c&&(m=c[t]),o().createElement(o().Fragment,null,o().createElement(xe.Z,{...s,id:`${e}-selectinput`,renderOption:(e,t,r)=>o().createElement("li",{...e},l?l(t,t.label,r.selected):t.label),componentsProps:{...s.componentsProps,popupIndicator:{...null===(u=s.componentsProps)||void 0===u?void 0:u.popupIndicator,size:"small"}},options:r,onChange:(e,t,r)=>{(t&&"string"!=typeof t||a)&&n&&n(t||"")},value:m,renderInput:i||(e=>o().createElement(we.Z,{...e,variant:"outlined",size:"small",margin:"dense"}))}))},lt=({label:e,required:t=!0,toolTipText:r,toolTipArea:n,errorMessage:a,...l})=>{const i=n&&o().createElement("div",null,o().createElement("span",{className:H},n.descriptionText),n.toolTipComponent);return o().createElement("div",{className:T},o().createElement("div",{className:C},o().createElement("label",{className:V(t)},e),(r||n)&&!l.readOnly&&o().createElement(P,{title:i||r||"",className:I,disableInteractive:null===n},o().createElement(f.Z,null))),o().createElement(at,{label:e,disableClearable:!0,...l}))},it=y.css`
  display: flex;
  flex-direction: column;
  padding: 10px;
`,st=y.css`
  display: flex;
  flex-direction: column;
  gap: 20px;
`,ut=y.css`
  display: flex;
  flex-direction: column;
`,ct=(y.css`
  transform: rotate(90deg);
`,y.css`
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;
  align-items: center;
  width: 100%;
`),mt=y.css`
  font-size: var(--jp-ui-font-size0);
  min-width: max-content;
`,dt=y.css`
  font-size: var(--jp-ui-font-size0);
  color: var(--jp-inverse-layout-color4);
  padding-right: 5px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
`,pt=y.css`
  width: 100%;
`,vt=y.css`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  &[data-selected='true'] {
    background-image: var(--jp-check-icon);
    background-size: 15px;
    background-repeat: no-repeat;
    background-position: 100% center;
  }
  & > p {
    max-width: calc(100% - 10px);
  }
`,gt=(e,t,r)=>o().createElement("span",{className:pt},o().createElement("div",{className:vt,"data-selected":r},o().createElement("p",null,t||e.label)),bt(e.optionMetadata&&e.optionMetadata.description)),bt=e=>{if(!e)return;const t=e.match(/(((https?:\/\/)|(www\.))[^\s]+)/g);if(t){console.log("links",t);for(const r of t)e=e.replace(r," ")}const r=e.trim();return o().createElement("div",{className:ct},o().createElement("span",{className:dt},r),t&&t.map((e=>o().createElement(z,{className:mt,key:e,href:e,target:A.External},i.KernelSelector.imageSelectorOption.linkText))))};r(9850);const ht=["datascience-1.0","sagemaker-data-science-38","1.8.1-cpu-py36","pytorch-1.8-gpu-py36","sagemaker-sparkmagic","tensorflow-2.6-cpu-py38-ubuntu20.04-v1","tensorflow-2.6-gpu-py38-cu112-ubuntu20.04-v1","sagemaker-sparkanalytics-v1"];var Et;async function ft(e,t){if(e.endsWith(".ipynb"))try{return(await t.get(e)).content.metadata.kernelspec.name}catch(e){return""}return""}!function(e){e.Custom="customImage",e.Sagemaker="smeImage",e.Session="session"}(Et||(Et={}));const yt={smeImage:"Sagemaker Image",customImage:"Custom Image",prefered:"Use image from preferred session",session:"Use image from other session"};function _t(e,t,r){const n=Object.values(e).filter((e=>{const n=e.arnEnvironment.split("/")[1];return r?(null==e?void 0:e.group)===t&&ht.includes(n):((null==e?void 0:e.group)!==Et.Sagemaker||!e.label.includes("Geospatial"))&&(null==e?void 0:e.group)===t}));return{label:yt[t],value:"",options:n.map((e=>({label:e.label,value:t===Et.Session?e.label:e.arnEnvironment,group:yt[t],optionMetadata:e,options:e.versionOptions})))}}const St=i.ScheduleNoteBook.MainPanel.Tooltips,kt=i.ScheduleNoteBook.MainPanel.StudioTooltips,xt=({isDisabled:e,formState:t,formErrors:r,setFormState:a,setFormErrors:s,model:u,jobsView:c,requestClient:m,contentsManager:d})=>{var p,b;const{pluginEnvironment:h}=Je(),[E,f]=(0,n.useState)({arnEnvironment:null,kernel:null,version:null}),[y,_]=(0,n.useState)({});(0,n.useEffect)((()=>{(async function(e){const t=v.URLExt.join(e.baseUrl,"api/kernelspecs"),r=await g.ServerConnection.makeRequest(t,{},e);if(200===r.status)return await r.json()})(m).then((async e=>{var t;e&&_(function(e){const t={},r=e.kernelspecs;return Object.values(r).forEach((e=>{var r;if(!e)return;const n=(null===(r=e.spec)||void 0===r?void 0:r.metadata)?e.spec.metadata.sme_metadata:null,{imageName:o,kernelName:a}=function(e){try{if(!D()(e)||0===e.length)return{imageName:null,kernelName:null};const[t,r]=e.split("(");return{imageName:r&&r.slice(0,-1).split("/")[0],kernelName:t&&t.slice(0,-1)}}catch(e){return{imageName:null,kernelName:null}}}(e.spec.display_name),{kernel:l,arnEnvironment:i,version:s}=J(e.name);if(!(l&&i&&o&&a))return;const u={arnEnvironment:i,kernelOptions:[{label:a,value:l}],versionOptions:s?[{label:`v${s}`,value:s}]:void 0,label:s?`${o} v${s}`:o,description:(null==n?void 0:n.description)?n.description:void 0,group:n&&n.is_template?Et.Sagemaker:Et.Custom};if(t[i]){const{kernelOptions:e}=t[i];if(!e.some((e=>e.value===l))){const r=[...e,{label:a,value:l}];t[i].kernelOptions=r}if(s){const{versionOptions:e}=t[i];if(!e.some((e=>e.value===s))){const r={label:`v${s}`,value:s.toString()},n=Array.isArray(e)?[...e,r]:[r];t[i].versionOptions=n}}}else t[i]=u})),t}(e));const r=await ft(u.inputFile,d),n=r in(null!==(t=null==e?void 0:e.kernelspecs)&&void 0!==t?t:{})?r:"",o=((e,t,r)=>{if(r===l.JobsView.JobDetail||r===l.JobsView.JobDefinitionDetail){if(e){const{sm_kernel:t,sm_image:r}=e;return J(`${t}__SAGEMAKER_INTERNAL__${r}`)}return{kernel:null,arnEnvironment:null,version:null}}if(r===l.JobsView.CreateForm){if(e&&"sm_image"in e){const{sm_kernel:t,sm_image:r}=e;return J(`${t}__SAGEMAKER_INTERNAL__${r}`)}return J(t)||{kernel:null,arnEnvironment:null,version:null}}return J(t)||{kernel:null,arnEnvironment:null,version:null}})(u.runtimeEnvironmentParameters,n,c);f(o),a((e=>({...e,sm_kernel:o.kernel||"",sm_image:o.arnEnvironment||""})))}))}),[]);const S=[...null!==(p=_t(y,Et.Sagemaker,!1).options)&&void 0!==p?p:[],...null!==(b=_t(y,Et.Custom).options)&&void 0!==b?b:[]],k=(0,n.useMemo)((()=>{var e;return E.arnEnvironment&&(null===(e=y[E.arnEnvironment])||void 0===e?void 0:e.kernelOptions)||[]}),[y,E]),x=!!r.jobEnvironmentError,w=o().createElement("div",{className:F},o().createElement(ae.Z,{severity:"error"},r.jobEnvironmentError));return(0,n.useEffect)((()=>{E.arnEnvironment&&E.kernel&&r.jobEnvironmentError&&s({...r,jobEnvironmentError:""})}),[E.arnEnvironment,E.kernel]),0===Object.keys(y).length?null:o().createElement("div",{className:it},o().createElement("div",{className:st},o().createElement("div",{className:ut},o().createElement(lt,{"data-testid":"sm_image_dropdown",options:S,value:E.arnEnvironment,label:i.ImageSelector.label,customListItemRender:gt,onChange:(e,r)=>{var n;if(!e||"string"==typeof e)return;const o=(null===(n=e.optionMetadata)||void 0===n?void 0:n.kernelOptions)||[],l=o.length>0?o[0].value:null,i=r?r.value:null;a({...t,sm_image:e.value+(i?"/"+i:""),sm_kernel:null!=l?l:""}),f({arnEnvironment:e.value,kernel:l,version:i})},readOnly:e,groupBy:e=>{var t;return null!==(t=e.group)&&void 0!==t?t:""},toolTipText:h.isStudio?kt.ImageTooltipText:St.ImageTooltipText}),r.jobEnvironmentError&&o().createElement("div",{className:O},x&&w)),o().createElement(lt,{options:k,value:E.kernel,label:i.KernelSelector.label,onChange:e=>{e&&"string"!=typeof e&&e&&(a({...t,sm_kernel:e.value}),f({...E,kernel:e.value}))},readOnly:e,toolTipText:h.isStudio?kt.KernelTooltipText:St.KernelTooltipText})))},wt=i.ScheduleNoteBook.MainPanel.AdvancedOptions,Mt=i.ScheduleNoteBook.MainPanel.Tooltips,Pt=({setFormState:e,formState:t,isDisabled:r,formErrors:a,setFormErrors:l,model:i,executionEnvironments:s})=>{const u=(0,n.useMemo)((()=>((e,t)=>{var r,n;if(e){const{sm_kernel:t,sm_image:r}=e;return J(`${t}__SAGEMAKER_INTERNAL__${r}`)}const o=null===(r=null==t?void 0:t.find((e=>"image"===e.name)))||void 0===r?void 0:r.value,a=null===(n=null==t?void 0:t.find((e=>"kernel"===e.name)))||void 0===n?void 0:n.value;return K(o)&&K(a)?J(`${a}__SAGEMAKER_INTERNAL__${o}`):{kernel:null,arnEnvironment:null,version:null}})(i.runtimeEnvironmentParameters,null==s?void 0:s.auto_detected_config)),[]);(0,n.useEffect)((()=>{e({...t,sm_kernel:u.kernel||"",sm_image:u.arnEnvironment||""})}),[u]);const c=r=>{const n=r.target.name,o=r.target.value;e({...t,[n]:o})};return o().createElement("div",{className:$},o().createElement(B,{name:"sm_image",onChange:c,readOnly:r,required:!0,value:t.sm_image,placeholder:wt.Placeholders.ImagePlaceHolder,labelInfo:wt.Image,errorMessage:a.ImageError,onBlur:e=>{const{value:t}=e.target,r=t.length<=0?Oe.AdvancedOptions.ImageError:"";l({...a,ImageError:r})},toolTipText:Mt.ImageTooltipText}),o().createElement(B,{name:"sm_kernel",onChange:c,readOnly:r,required:!0,value:t.sm_kernel,placeholder:wt.Placeholders.KernelPlaceHolder,labelInfo:wt.Kernel,errorMessage:a.KernelError,onBlur:e=>{const{value:t}=e.target,r=t.length<=0?Oe.AdvancedOptions.KernelError:"";l({...a,KernelError:r})},toolTipText:Mt.KernelTooltipText}))},Tt=i.ScheduleNoteBook.MainPanel.Tooltips,jt=({setFormState:e,formState:t,isDisabled:r,formErrors:a,setFormErrors:l,contentsManager:s,model:u})=>{const[c,m]=(0,n.useState)([]),[d,p]=(0,n.useState)([]),b=async()=>{const e=g.ServerConnection.makeSettings(),t=v.URLExt.join(e.baseUrl,"/sagemaker_images"),r=await g.ServerConnection.makeRequest(t,{},e);return 200==r.status?(await r.json()).map((e=>({label:e.image_display_name,value:e.image_arn}))):[]},h=async()=>{const e=g.ServerConnection.makeSettings(),t=v.URLExt.join(e.baseUrl,"/api/kernelspecs"),r=await g.ServerConnection.makeRequest(t,{},e);let n=null;const o=[],a=[];if(200===r.status){const e=await r.json();n=e.default,e.kernelspecs&&Object.values(e.kernelspecs).forEach((e=>{if(e){o.push(e.name);let t=e.name;e.spec&&(t=e.spec.display_name),a.push({label:t,value:e.name})}}))}return{defaultKernelName:n,kernelNames:o,kernelOptions:a}};return(0,n.useEffect)((()=>{Promise.all([ft(u.inputFile,s),b(),h()]).then((r=>{const n=r[0],o=r[1],a=r[2];let l=null,i=null;o&&o.length>0&&m(o),u.runtimeEnvironmentParameters&&u.runtimeEnvironmentParameters.sm_image?l=u.runtimeEnvironmentParameters.sm_image:o&&o.length>0&&(l=o[0].value),a&&a.kernelOptions&&a.kernelOptions.length>0&&p(a.kernelOptions),i=u.runtimeEnvironmentParameters&&u.runtimeEnvironmentParameters.sm_kernel?u.runtimeEnvironmentParameters.sm_kernel:a.kernelNames.indexOf(n)>=0?n:a.defaultKernelName||"",e({...t,sm_image:l,sm_kernel:i})})).catch((e=>console.error(e)))}),[]),o().createElement("div",{className:$},o().createElement(lt,{"data-testid":"sm_image_dropdown",options:c,value:t.sm_image,label:i.ImageSelector.label,onChange:r=>{r&&"string"!=typeof r&&e({...t,sm_image:r.value})},readOnly:r,toolTipText:Tt.ImageTooltipText,required:!0}),o().createElement(lt,{"data-testid":"sm_kernel_dropdown",options:d,value:t.sm_kernel,label:i.KernelSelector.label,onChange:r=>{r&&"string"!=typeof r&&e({...t,sm_kernel:r.value})},readOnly:r,toolTipText:Tt.KernelTooltipText,required:!0}))},Ct=e=>{const{pluginEnvironment:t}=Je();return o().createElement(o().Fragment,null,t.isStudio&&o().createElement(xt,{...e}),t.isJupyterLab&&o().createElement(jt,{...e}),t.isLocalJL&&o().createElement(Pt,{...e}))},It=e=>{const{executionEnvironments:t,settingRegistry:r,jobsView:a,requestClient:i,errors:s,handleErrorsChange:u,model:m,handleModelChange:d}=e,p=(0,n.useMemo)((()=>{return e=null==t?void 0:t.auto_detected_config,a===l.JobsView.CreateForm&&(null===(r=null==e?void 0:e.find((e=>"app_network_access_type"===e.name)))||void 0===r?void 0:r.value)||"";var e,r}),[]),v=(0,n.useMemo)((()=>{var e,r;const n=[],o=(null===(r=null===(e=t.auto_detected_config)||void 0===e?void 0:e.find((e=>"lcc_arn"===e.name)))||void 0===r?void 0:r.value)||[];n.push(Xe),n.push(...o);const i=(s=m.runtimeEnvironmentParameters,((u=a)===l.JobsView.JobDetail||u===l.JobsView.JobDefinitionDetail)&&s&&s.sm_lcc_init_script_arn||Xe);var s,u;return m.runtimeEnvironmentParameters&&i!==Xe&&n.push(i),{allLCCOptions:n,selectedLccValue:i}}),[]),g=(0,n.useMemo)((()=>((e,t,r)=>{var n;if(r===l.JobsView.JobDetail||r===l.JobsView.JobDefinitionDetail){if(e)return e.role_arn}else if(r===l.JobsView.CreateForm){if(e&&"role_arn"in e)return e.role_arn;const r=null===(n=null==t?void 0:t.find((e=>"role_arn"===e.name)))||void 0===n?void 0:n.value;if((null==r?void 0:r.length)>0)return r[0]}return""})(m.runtimeEnvironmentParameters,t.auto_detected_config,a)),[]),b=(0,n.useMemo)((()=>rt(m.runtimeEnvironmentParameters,t.auto_detected_config,a,"s3_output")),[]),h=(0,n.useMemo)((()=>rt(m.runtimeEnvironmentParameters,t.auto_detected_config,a,"s3_input")),[]),E=(0,n.useMemo)((()=>nt(m.runtimeEnvironmentParameters,a,1,"max_retry_attempts")),[]),f=(0,n.useMemo)((()=>nt(m.runtimeEnvironmentParameters,a,172800,"max_run_time_in_seconds")),[]),y=(0,n.useMemo)((()=>{var e,r;const n=(null===(r=null===(e=t.auto_detected_config)||void 0===e?void 0:e.find((e=>"vpc_security_group_ids"===e.name)))||void 0===r?void 0:r.value)||[];return null==n?void 0:n.map((e=>e.name))}),[]),_=(0,n.useMemo)((()=>{var e,r;const n=(null===(r=null===(e=t.auto_detected_config)||void 0===e?void 0:e.find((e=>"vpc_subnets"===e.name)))||void 0===r?void 0:r.value)||[];return null==n?void 0:n.map((e=>e.name))}),[]),S=(0,n.useMemo)((()=>p===c.PublicInternetOnly?{securityGroups:[],subnets:[]}:{securityGroups:0===_.length&&a===l.JobsView.CreateForm?[]:tt(m.runtimeEnvironmentParameters,t.auto_detected_config,a,"vpc_security_group_ids"),subnets:tt(m.runtimeEnvironmentParameters,t.auto_detected_config,a,"vpc_subnets")}),[]),k=(0,n.useMemo)((()=>((e,t)=>{if(t===l.JobsView.JobDetail||t===l.JobsView.JobDefinitionDetail){if(e)return e.sm_init_script}else if(t===l.JobsView.CreateForm&&e&&"sm_init_script"in e)return e.sm_init_script;return""})(m.runtimeEnvironmentParameters,a)),[]),x=(0,n.useMemo)((()=>(e=>{const t=[];if(e)for(const r in e)if(!et.has(r)){const n={key:r,value:e[r]};t.push(n)}return t})(m.runtimeEnvironmentParameters)),[]),w=(0,n.useMemo)((()=>ot(m.runtimeEnvironmentParameters,a,"sm_output_kms_key")),[]),M=(0,n.useMemo)((()=>ot(m.runtimeEnvironmentParameters,a,"sm_volume_kms_key")),[]),P=(0,n.useMemo)((()=>{if(p===c.PublicInternetOnly)return!1;const e=S.subnets;return 0!==_.length&&(0===e.length&&_.length,!0)}),[]),[T,j]=(0,n.useState)({sm_lcc_init_script_arn:v.selectedLccValue||"",role_arn:g||"",vpc_security_group_ids:S.securityGroups||"",vpc_subnets:S.subnets||"",s3_input:h||"",s3_output:b||"",sm_kernel:"",sm_image:"",sm_init_script:k||"",sm_output_kms_key:w||"",sm_volume_kms_key:M||"",max_retry_attempts:E,max_run_time_in_seconds:f}),[C,I]=(0,n.useState)({...T,sm_output_kms_key:"",sm_volume_kms_key:""});(0,n.useEffect)((()=>{const e=(e=>e&&0===e.length?`${Fe.RequiresPrivateSubnet} ${Fe.NoPrivateSubnetsInSageMakerDomain}`:"")(_),t=(r=S.subnets)&&0===r.length?`${Fe.RequiresPrivateSubnet} ${Fe.NoPrivateSubnetsInSageMakerDomain}. ${Fe.YouMayChooseOtherSubnets}`:"";var r;u({...s,roleError:Ve(g),s3InputFolderError:Ae(h),s3OutputFolderError:Ae(b),environmentsStillLoading:"",kernelsStillLoading:"",subnetError:P&&(e||t)||""})}),[]);const[O,F]=(0,n.useState)();(0,n.useEffect)((()=>{(async function(e){return(await e.get("@amzn/sagemaker-jupyter-scheduler:advanced-options","advancedOptions")).composite})(r).then((e=>{F(e)}))}),[]),(0,n.useEffect)((()=>{var e,t,r,n,o;let a={},l={},i={};const c=null!==(e=null==O?void 0:O.role_arn)&&void 0!==e?e:"";c&&c!==g&&(a={...a,role_arn:c},l={...l,roleError:Ve(c)});const m=null!==(t=null==O?void 0:O.s3_input)&&void 0!==t?t:"";m&&m!==h&&(a={...a,s3_input:m},l={...l,s3InputFolderError:Ae(m)});const d=null!==(r=null==O?void 0:O.s3_output)&&void 0!==r?r:"";d&&d!==b&&(a={...a,s3_output:d},l={...l,s3OutputFolderError:Ae(d)});const p=null!==(n=null==O?void 0:O.sm_output_kms_key)&&void 0!==n?n:"";p&&p!==w&&(i={...i,sm_output_kms_key:p});const v=null!==(o=null==O?void 0:O.sm_volume_kms_key)&&void 0!==o?o:"";v&&v!==M&&(i={...i,sm_volume_kms_key:v}),i={...a,...i},Object.keys(a).length>0&&I({...C,...a}),Object.keys(i).length>0&&j({...T,...i}),Object.keys(l).length>0&&u({...s,...l})}),[O]);const[V,A]=(0,n.useState)(x),[R,z]=(0,n.useState)(P),K=(0,n.useMemo)((()=>{const e={};return null==V||V.map((t=>{const{key:r,value:n}=t;0!==r.trim().length&&0!==n.trim().length&&(e[r]=n)})),e}),[V]);(0,n.useEffect)((()=>{var e,t;const r=(null===(e=C.vpc_security_group_ids)||void 0===e?void 0:e.join(","))||"",n=(null===(t=C.vpc_subnets)||void 0===t?void 0:t.join(","))||"";d({...m,runtimeEnvironmentParameters:{...C,vpc_security_group_ids:r,vpc_subnets:n,...K}})}),[C,K]);const L=a===l.JobsView.JobDefinitionDetail||a===l.JobsView.JobDetail;return o().createElement("div",{className:N(L)},o().createElement(Ct,{isDisabled:L,formState:C,setFormState:I,formErrors:s,setFormErrors:u,...e}),o().createElement(Qe,{isDisabled:L,formState:C,setFormState:I,handleChange:e=>{const t=e.target.name,r=e.target.value;I({...C,[t]:r})},handleNumberValueChange:e=>{const t=e.target.name,r=parseInt(e.target.value);I({...C,[t]:isNaN(r)?"":r})},requestClient:i,formErrors:s,setFormValidationErrors:u,environmentVariables:V,userDefaultValues:T,setEnvironmentVariables:A,lccOptions:v.allLCCOptions,availableSecurityGroups:y,availableSubnets:_,initialSecurityGroups:S.securityGroups,initialSubnets:S.subnets,setSubnets:e=>{I({...C,vpc_subnets:e})},setRoleArn:e=>{I({...C,role_arn:e})},setSecurityGroups:e=>{I({...C,vpc_security_group_ids:e})},onSelectLCCScript:e=>{I({...C,sm_lcc_init_script_arn:e})},isVPCDomain:p===c.VpcOnly,enableVPCSetting:R,setEnableVPCSetting:z}))};var Nt=r(2453);function Ot(e){return getComputedStyle(document.body).getPropertyValue(e).trim()}function Ft(){const e=document.body.getAttribute("data-jp-theme-light");return(0,Nt.Z)({spacing:4,components:{MuiButton:{defaultProps:{size:"small"}},MuiFilledInput:{defaultProps:{margin:"dense"}},MuiFormControl:{defaultProps:{margin:"dense",size:"small"}},MuiFormHelperText:{defaultProps:{margin:"dense"}},MuiIconButton:{defaultProps:{size:"small"}},MuiInputBase:{defaultProps:{margin:"dense",size:"small"}},MuiInputLabel:{defaultProps:{margin:"dense"},styleOverrides:{root:{display:"flex",alignItems:"center",color:"var(--jp-ui-font-color0)",gap:"6px"}}},MuiListItem:{defaultProps:{dense:!0}},MuiOutlinedInput:{defaultProps:{margin:"dense"}},MuiFab:{defaultProps:{size:"small"}},MuiAutocomplete:{defaultProps:{componentsProps:{paper:{elevation:4}}}},MuiTable:{defaultProps:{size:"small"}},MuiTextField:{defaultProps:{margin:"dense",size:"small"}},MuiToolbar:{defaultProps:{variant:"dense"}}},palette:{background:{paper:Ot("--jp-layout-color1"),default:Ot("--jp-layout-color1")},mode:"true"===e?"light":"dark",primary:{main:Ot("--jp-brand-color1"),light:Ot("--jp-brand-color2"),dark:Ot("--jp-brand-color0")},error:{main:Ot("--jp-error-color1"),light:Ot("--jp-error-color2"),dark:Ot("--jp-error-color0")},warning:{main:Ot("--jp-warn-color1"),light:Ot("--jp-warn-color2"),dark:Ot("--jp-warn-color0")},success:{main:Ot("--jp-success-color1"),light:Ot("--jp-success-color2"),dark:Ot("--jp-success-color0")},text:{primary:Ot("--jp-ui-font-color1"),secondary:Ot("--jp-ui-font-color2"),disabled:Ot("--jp-ui-font-color3")}},shape:{borderRadius:2},typography:{fontFamily:Ot("--jp-ui-font-family"),fontSize:12,htmlFontSize:16,button:{textTransform:"capitalize"}}})}const Vt=({requestClient:e,contentsManager:t,commands:r,jobsView:a,errors:c,handleErrorsChange:b,...h})=>{const[E,f]=(0,n.useState)("");(0,n.useEffect)((()=>{const t={...c,environmentsStillLoading:"EnvironmentsStillLoadingError",kernelsStillLoading:"KernelsStillLoadingError"};b(t),a===l.JobsView.CreateForm?(async()=>{const t=v.URLExt.join(e.baseUrl,"/advanced_environments"),n=await g.ServerConnection.makeRequest(t,{},e);if(200!==n.status){const e=(await n.json()).error_code;throw Object.values(s).indexOf(e)>=0&&(async e=>{const t=o().createElement(o().Fragment,null,i.Dialog.awsCredentialsError.body.text.map(((e,t)=>o().createElement("p",{key:t,className:q},((e,t)=>{const r=e.split("%");return o().createElement(o().Fragment,null,r.map((e=>{if(e.startsWith("{")){const[r,...n]=e.replace("{","").split("}"),a=t[r],l=n.join("");return a?o().createElement(o().Fragment,null,o().createElement(z,{key:r,href:a.linkHref,target:A.External},a.linkString),l):o().createElement(o().Fragment,null,e)}return o().createElement(o().Fragment,null,e)})))})(e,i.Dialog.awsCredentialsError.body.links))))),r=new m.Dialog({title:i.Dialog.awsCredentialsError.title,body:t,buttons:[m.Dialog.cancelButton(),m.Dialog.okButton({label:i.Dialog.awsCredentialsError.buttons.enterKeysInTerminal})]});(await r.launch()).button.label===i.Dialog.awsCredentialsError.buttons.enterKeysInTerminal&&e.execute(u)})(r),new Error(n.statusText)}return await n.json()})().then((async e=>{k(!1),_(e)})).catch((e=>{f(e.message)})):k(!1)}),[a,h.model.inputFile]);const[y,_]=(0,n.useState)({}),[S,k]=(0,n.useState)(!0);return E?o().createElement("div",{className:X},E):S?null:a!==l.JobsView.CreateForm||(null==y?void 0:y.auto_detected_config)?o().createElement(d.Z,{theme:Ft()},o().createElement(p.StyledEngineProvider,{injectFirst:!0},o().createElement(It,{executionEnvironments:y,requestClient:e,contentsManager:t,jobsView:a,errors:c,handleErrorsChange:b,...h}))):null},At=[{id:"@amzn/sagemaker-scheduler:scheduler",autoStart:!1,requires:[a.ISettingRegistry],provides:l.Scheduler.IAdvancedOptions,activate:(e,t)=>r=>{const n=e.serviceManager.serverSettings,a=new g.ContentsManager;return o().createElement(E.StyledEngineProvider,{injectFirst:!0},o().createElement(De,{app:e},o().createElement(Vt,{requestClient:n,contentsManager:a,settingRegistry:t,commands:e.commands,...r})))}}]}}]);
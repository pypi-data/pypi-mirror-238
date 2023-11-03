import { E as EnumViews } from './EnumViews-f83d2996.js';

const workflowSteps = [
  {
    currentView: EnumViews.recipient,
    previousView: EnumViews.home,
    nextView: EnumViews.selectFile,
    label: 'Select recipient',
  },
  {
    currentView: EnumViews.selectFile,
    previousView: EnumViews.recipient,
    nextView: EnumViews.templateRoles,
    label: 'Select document',
  },
  {
    currentView: EnumViews.templateRoles,
    previousView: EnumViews.selectFile,
    nextView: EnumViews.sendDocument,
    label: 'Connect Roles',
  },
  {
    currentView: EnumViews.sendDocument,
    previousView: EnumViews.selectFile,
    nextView: EnumViews.documentValidation,
    label: 'Prepare sendout',
  },
  {
    currentView: EnumViews.documentValidation,
    previousView: EnumViews.sendDocument,
    nextView: EnumViews.documentValidation,
    label: 'Send document',
  },
];

export { workflowSteps as w };

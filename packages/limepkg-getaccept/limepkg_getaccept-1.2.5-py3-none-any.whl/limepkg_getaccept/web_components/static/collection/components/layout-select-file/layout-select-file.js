/* eslint-disable camelcase */
import { Component, h, Prop, State, Event, Listen, Watch, } from '@stencil/core';
import { fetchTemplates, fetchLimeDocuments, fetchTemplateFields, fetchObjectProps, fetchTemplateRoles, } from '../../services';
var EnumSections;
(function (EnumSections) {
  EnumSections["None"] = "none";
  EnumSections["Template"] = "template";
  EnumSections["LimeDocuments"] = "limeDocuments";
})(EnumSections || (EnumSections = {}));
export class LayoutSelectFile {
  constructor() {
    this.customFields = [];
    this.templateRoles = [];
    this.isLoadingTemplates = false;
    this.templates = [];
    this.isLoadingFields = false;
    this.openSection = EnumSections.Template;
    this.tableData = [];
    this.columns = [
      { title: 'Merge tag', field: 'field' },
      { title: 'Value', field: 'value' },
    ];
    this.tabs = [
      {
        id: 'merge-fields',
        text: 'Template fields',
        active: true,
      },
      {
        id: 'getaccept-merge-fields',
        text: 'GetAccept template fields',
      },
    ];
    this.gaMergeFieldColumns = [
      { title: 'Merge tag', field: 'field' },
      { title: 'Label', field: 'value' },
    ];
    this.gaMergeFields = [
      {
        field: '{{recipient.first_name}}',
        value: 'Recipient - First name',
      },
      {
        field: '{{recipient.last_name}}',
        value: 'Recipient - Last name',
      },
      {
        field: '{{recipient.email}}',
        value: 'Recipient - Email',
      },
      {
        field: '{{recipient.company_name}}',
        value: 'Recipient - Company name',
      },
      {
        field: '{{sender.first_name}}',
        value: 'Sender - First name',
      },
      {
        field: '{{sender.last_name}}',
        value: 'Sender - Last name',
      },
      {
        field: '{{sender.fullname}}',
        value: 'Sender - Full name',
      },
      {
        field: '{{document.name}}',
        value: 'Document - Name',
      },
      {
        field: '{{document.field}}',
        value: 'Document - field',
      },
    ];
    this.handleChangeTab = (event) => {
      this.tabs = this.tabs.map(tab => {
        if (tab.id === event.detail.id) {
          return event.detail;
        }
        return tab;
      });
    };
    this.loadTemplates = this.loadTemplates.bind(this);
    this.loadTemplateFields = this.loadTemplateFields.bind(this);
    this.loadLimeDocuments = this.loadLimeDocuments.bind(this);
    this.onChangeSection = this.onChangeSection.bind(this);
    this.setTemplates = this.setTemplates.bind(this);
    this.setLimeDocuments = this.setLimeDocuments.bind(this);
    this.setFields = this.setFields.bind(this);
    this.onActivateRow = this.onActivateRow.bind(this);
    this.loadTemplateRoles = this.loadTemplateRoles.bind(this);
  }
  render() {
    return [
      h("div", { class: "layout-select-file-container" },
        h("h3", null, "Select file to send"),
        h("div", { class: "select-file-container" },
          h("div", { class: "file-column" },
            h("limel-collapsible-section", { header: "Templates", isOpen: this.openSection === EnumSections.Template, onOpen: event => this.onChangeSection(event, EnumSections.Template), onClose: event => this.onChangeSection(event, EnumSections.None) },
              h("template-list", { templates: this.templates, selectedTemplate: this.selectedTemplate, isLoading: this.isLoadingTemplates })),
            h("limel-collapsible-section", { header: "Lime documents", isOpen: this.openSection === EnumSections.LimeDocuments, onOpen: event => this.onChangeSection(event, EnumSections.LimeDocuments), onClose: event => this.onChangeSection(event, EnumSections.None) },
              h("lime-document-list", { documents: this.limeDocuments, selectedLimeDocument: this.selectedLimeDocument, isLoading: this.isLoadingLimeDocuments }))),
          h("div", { class: "file-column" },
            h("template-preview", { template: this.selectedTemplate, isLoading: this.isLoadingFields, session: this.session }),
            h("custom-fields", { template: this.selectedTemplate, customFields: this.customFields, isLoading: this.isLoadingFields }))),
        h("limel-collapsible-section", { header: "Show template parameters", onClose: event => event.stopPropagation() },
          h("limel-tab-panel", { tabs: this.tabs, onChangeTab: this.handleChangeTab },
            h("limel-table", { mode: "remote", data: this.tableData.sort((a, b) => a.field.localeCompare(b.field)) || [], columns: this.columns, onActivate: this.onActivateRow, id: "merge-fields" }),
            h("limel-table", { mode: "remote", data: this.gaMergeFields.sort((a, b) => a.field.localeCompare(b.field)), columns: this.gaMergeFieldColumns, id: "getaccept-merge-fields" })))),
    ];
  }
  async componentWillLoad() {
    this.loadTemplates();
    this.loadLimeDocuments();
    await this.loadObjectProps();
  }
  onChangeSection(event, section) {
    event.stopPropagation();
    this.openSection = section;
  }
  async loadTemplates() {
    this.isLoadingTemplates = true;
    try {
      this.templates = await fetchTemplates(this.platform, this.session, this.selectedTemplate);
    }
    catch (e) {
      this.errorHandler.emit('Could not load templates from GetAccept...');
    }
    this.isLoadingTemplates = false;
  }
  async loadLimeDocuments() {
    this.isLoadingLimeDocuments = true;
    const { id: record_id, limetype } = this.context;
    try {
      this.limeDocuments = await fetchLimeDocuments(this.platform, limetype, record_id, this.selectedLimeDocument);
    }
    catch (e) {
      this.errorHandler.emit('Could not load related Lime documents...');
    }
    this.isLoadingLimeDocuments = false;
  }
  async loadTemplateFields() {
    if (!this.selectedTemplate) {
      this.customFields = [];
      this.setCustomFields.emit(this.customFields);
      return;
    }
    this.isLoadingFields = true;
    const { id: record_id, limetype } = this.context;
    try {
      const fields = await fetchTemplateFields(this.platform, this.session, limetype, record_id, this.selectedTemplate);
      this.setFields(fields);
    }
    catch (e) {
      this.errorHandler.emit('Could not fetch template fields from GetAccept...');
    }
    this.isLoadingFields = false;
  }
  async loadObjectProps() {
    const { id: record_id, limetype } = this.context;
    try {
      const props = await fetchObjectProps(this.platform, this.session, limetype, record_id);
      this.setAvailableFields(props);
    }
    catch (e) {
      this.errorHandler.emit('Could not fetch lime object...');
    }
  }
  async loadTemplateRoles() {
    if (!this.selectedTemplate) {
      return;
    }
    const { id: record_id, limetype } = this.context;
    try {
      const roles = await fetchTemplateRoles(this.platform, this.session, limetype, record_id, this.selectedTemplate);
      this.setRoles(roles);
    }
    catch (e) {
      this.errorHandler.emit('Could not fetch template roles from GetAccept...');
    }
  }
  setAvailableFields(limeObject) {
    Object.entries(limeObject).forEach(([key, value]) => {
      if (value) {
        this.tableData.push({
          field: `{{${key}}}`,
          value: value,
        });
      }
    });
  }
  setFields(fields) {
    const customFields = fields.map(this.mapField);
    this.setCustomFields.emit(customFields);
  }
  setRoles(roles) {
    this.setTemplateRoles.emit(roles);
  }
  onChangeTemplate(data) {
    this.setTemplates(data);
    if (data) {
      this.loadTemplateFields();
      this.loadTemplateRoles();
    }
  }
  setTemplates(template) {
    this.templates = this.getSelectedListItems(this.templates, template);
  }
  onChangeDocument(data) {
    this.setLimeDocuments(data);
  }
  mapField(field) {
    return {
      value: field.field_value.toString(),
      id: field.field_id,
      label: field.field_label,
      is_editable: field.is_editable === null ? true : field.is_editable,
    };
  }
  setLimeDocuments(document) {
    this.limeDocuments = this.getSelectedListItems(this.limeDocuments, document);
  }
  getSelectedListItems(items, selectedItem) {
    return items.map((item) => {
      if (selectedItem && item.value === selectedItem.value) {
        return selectedItem;
      }
      return Object.assign(Object.assign({}, item), { selected: false });
    });
  }
  updateFieldValue(event) {
    const { id, value } = event.detail;
    const customFields = this.customFields.map(field => {
      return field.id === id ? Object.assign(Object.assign({}, field), { value: value }) : field;
    });
    this.setCustomFields.emit(customFields);
  }
  onActivateRow(event) {
    navigator.clipboard.writeText(event.detail.field);
    this.errorHandler.emit(`Copied '${event.detail.field}' to your clipboard`);
  }
  static get is() { return "layout-select-file"; }
  static get encapsulation() { return "shadow"; }
  static get originalStyleUrls() { return {
    "$": ["layout-select-file.scss"]
  }; }
  static get styleUrls() { return {
    "$": ["layout-select-file.css"]
  }; }
  static get properties() { return {
    "platform": {
      "type": "unknown",
      "mutable": false,
      "complexType": {
        "original": "LimeWebComponentPlatform",
        "resolved": "LimeWebComponentPlatform",
        "references": {
          "LimeWebComponentPlatform": {
            "location": "import",
            "path": "@limetech/lime-web-components"
          }
        }
      },
      "required": false,
      "optional": false,
      "docs": {
        "tags": [],
        "text": ""
      }
    },
    "context": {
      "type": "unknown",
      "mutable": false,
      "complexType": {
        "original": "LimeWebComponentContext",
        "resolved": "LimeWebComponentContext",
        "references": {
          "LimeWebComponentContext": {
            "location": "import",
            "path": "@limetech/lime-web-components"
          }
        }
      },
      "required": false,
      "optional": false,
      "docs": {
        "tags": [],
        "text": ""
      }
    },
    "session": {
      "type": "unknown",
      "mutable": false,
      "complexType": {
        "original": "ISession",
        "resolved": "ISession",
        "references": {
          "ISession": {
            "location": "import",
            "path": "../../types/Session"
          }
        }
      },
      "required": false,
      "optional": false,
      "docs": {
        "tags": [],
        "text": ""
      }
    },
    "selectedTemplate": {
      "type": "unknown",
      "mutable": false,
      "complexType": {
        "original": "IListItem",
        "resolved": "IListItem",
        "references": {
          "IListItem": {
            "location": "import",
            "path": "../../types/ListItem"
          }
        }
      },
      "required": false,
      "optional": false,
      "docs": {
        "tags": [],
        "text": ""
      }
    },
    "selectedLimeDocument": {
      "type": "unknown",
      "mutable": false,
      "complexType": {
        "original": "IListItem",
        "resolved": "IListItem",
        "references": {
          "IListItem": {
            "location": "import",
            "path": "../../types/ListItem"
          }
        }
      },
      "required": false,
      "optional": false,
      "docs": {
        "tags": [],
        "text": ""
      }
    },
    "customFields": {
      "type": "unknown",
      "mutable": false,
      "complexType": {
        "original": "ICustomField[]",
        "resolved": "ICustomField[]",
        "references": {
          "ICustomField": {
            "location": "import",
            "path": "../../types/CustomField"
          }
        }
      },
      "required": false,
      "optional": false,
      "docs": {
        "tags": [],
        "text": ""
      },
      "defaultValue": "[]"
    },
    "templateRoles": {
      "type": "unknown",
      "mutable": false,
      "complexType": {
        "original": "ITemplateRole[]",
        "resolved": "ITemplateRole[]",
        "references": {
          "ITemplateRole": {
            "location": "import",
            "path": "src/types/TemplateRole"
          }
        }
      },
      "required": false,
      "optional": false,
      "docs": {
        "tags": [],
        "text": ""
      },
      "defaultValue": "[]"
    }
  }; }
  static get states() { return {
    "isLoadingTemplates": {},
    "templates": {},
    "isLoadingFields": {},
    "isLoadingLimeDocuments": {},
    "limeDocuments": {},
    "openSection": {},
    "tableData": {},
    "columns": {},
    "tabs": {},
    "gaMergeFieldColumns": {},
    "gaMergeFields": {}
  }; }
  static get events() { return [{
      "method": "setCustomFields",
      "name": "setCustomFields",
      "bubbles": true,
      "cancelable": true,
      "composed": true,
      "docs": {
        "tags": [],
        "text": ""
      },
      "complexType": {
        "original": "any",
        "resolved": "any",
        "references": {}
      }
    }, {
      "method": "setTemplateRoles",
      "name": "setTemplateRoles",
      "bubbles": true,
      "cancelable": true,
      "composed": true,
      "docs": {
        "tags": [],
        "text": ""
      },
      "complexType": {
        "original": "any",
        "resolved": "any",
        "references": {}
      }
    }, {
      "method": "errorHandler",
      "name": "errorHandler",
      "bubbles": true,
      "cancelable": true,
      "composed": true,
      "docs": {
        "tags": [],
        "text": ""
      },
      "complexType": {
        "original": "string",
        "resolved": "string",
        "references": {}
      }
    }]; }
  static get watchers() { return [{
      "propName": "selectedTemplate",
      "methodName": "onChangeTemplate"
    }, {
      "propName": "selectedLimeDocument",
      "methodName": "onChangeDocument"
    }]; }
  static get listeners() { return [{
      "name": "updateFieldValue",
      "method": "updateFieldValue",
      "target": undefined,
      "capture": false,
      "passive": false
    }]; }
}

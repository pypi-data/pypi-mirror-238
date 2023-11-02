"use strict";
(self["webpackChunkjupyter_fs"] = self["webpackChunkjupyter_fs"] || []).push([["lib_index_js"],{

/***/ "./lib/auth.js":
/*!*********************!*\
  !*** ./lib/auth.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AskDialog: () => (/* binding */ AskDialog),
/* harmony export */   DoubleBraceTemplate: () => (/* binding */ DoubleBraceTemplate),
/* harmony export */   askRequired: () => (/* binding */ askRequired)
/* harmony export */ });
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @material-ui/core */ "webpack/sharing/consume/default/@material-ui/core/@material-ui/core");
/* harmony import */ var _material_ui_core__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/******************************************************************************
 *
 * Copyright (c) 2019, the jupyter-fs authors.
 *
 * This file is part of the jupyter-fs library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */



class Template {
    constructor(template) {
        this.template = template;
        this.pattern = /(?:)/;
    }
    substitute(dict) {
        return this.template.replace(this.pattern, (_, p1) => dict[p1]);
    }
    tokens() {
        const toks = [];
        let match;
        // eslint-disable-next-line no-cond-assign
        while ((match = this.pattern.exec(this.template))) {
            toks.push(match[1]);
        }
        return toks;
    }
}
class DoubleBraceTemplate extends Template {
    constructor() {
        super(...arguments);
        this.pattern = /{{(\S+?)}}/g;
    }
}
function tokensFromUrl(url) {
    return new DoubleBraceTemplate(url).tokens();
}
function _askRequired(spec) {
    return spec.auth === "ask" && !spec.init;
}
function askRequired(specs) {
    for (const spec of specs) {
        if (_askRequired(spec)) {
            return true;
        }
    }
    return false;
}
class AskDialog extends react__WEBPACK_IMPORTED_MODULE_1__.Component {
    constructor(props, options) {
        super(props);
        this.state = AskDialog.initialState({ open: true, options });
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.Dialog, { className: "jfs-ask-dialog", open: this.state.open, onClose: this._onClose.bind(this) },
                react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.DialogTitle, { className: "jfs-ask jfs-ask-dialog-title" }, "Please enter token values for filesystem resources"),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.DialogContent, { className: "jfs-ask jfs-ask-dialog-content" }, this._form()),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.DialogActions, { className: "jfs-ask jfs-ask-dialog-actions" },
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.Button, { className: "jfs-ask jfs-ask-dialog-actions-button-cancel", onClick: this._onClose.bind(this), color: "primary" }, "Cancel"),
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.Button, { className: "jfs-ask jfs-ask-dialog-actions-button-submit", onClick: this._onSubmit.bind(this), color: "primary" }, "Submit")))));
    }
    _form() {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("form", { className: "jfs-ask jfs-ask-form", onSubmit: this._onSubmit.bind(this), noValidate: true, autoComplete: "off" }, this._formInner()));
    }
    _formInner() {
        return this.props.resources.map(resource => {
            // ask for credentials if needed, or state why not
            const askReq = _askRequired(resource);
            const inputs = askReq ? this._inputs(resource.url) : [];
            const tokens = tokensFromUrl(resource.url);
            let reason = "";
            if (resource.init && this.props.options.cache) {
                reason = "already initialized";
            }
            else if (!tokens.length) {
                reason = "no template parameters";
            }
            const summary = `${resource.name}:${reason && ` ${reason}`}`;
            return [
                react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.ExpansionPanel, { className: "jfs-ask jfs-ask-panel", disabled: !!reason, expanded: !reason, key: `${resource.name}_panel` },
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.ExpansionPanelSummary, { className: "jfs-ask jfs-ask-panel-summary" },
                        react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.Typography, null, summary),
                        !reason && react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.Typography, null, resource.url)),
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.ExpansionPanelDetails, { className: "jfs-ask jfs-ask-panel-details" }, inputs)),
            ];
        });
    }
    _inputs(url) {
        return tokensFromUrl(url).map(token => {
            var _a, _b, _c;
            return (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.TextField, { className: "jfs-ask jfs-ask-input", autoFocus: true, fullWidth: true, key: `${url}_${token}`, label: token, margin: "dense", name: token, onChange: this._onChange(url).bind(this), type: ((_a = this.state.visibility[url]) === null || _a === void 0 ? void 0 : _a[token]) ? "text" : "password", value: ((_b = this.state.values[url]) === null || _b === void 0 ? void 0 : _b[token]) || "", InputProps: {
                    endAdornment: (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.InputAdornment, { position: "end" },
                        react__WEBPACK_IMPORTED_MODULE_1__.createElement(_material_ui_core__WEBPACK_IMPORTED_MODULE_0__.IconButton, { onClick: this._onClickVisiblity(url, token).bind(this), onMouseDown: this._onMouseDownVisibility.bind(this), edge: "end" }, ((_c = this.state.visibility[url]) === null || _c === void 0 ? void 0 : _c[token]) ? (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_icons__WEBPACK_IMPORTED_MODULE_2__.visibilityIcon.react, null)) : (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_icons__WEBPACK_IMPORTED_MODULE_2__.visibilityOffIcon.react, null))))),
                } }));
        });
    }
    _onChange(url) {
        return function (event) {
            const target = event.target;
            this._setValue(url, target.name, target.value);
        };
    }
    _onClickVisiblity(url, key) {
        return function () {
            this._toggleVisibility(url, key);
        };
    }
    _onMouseDownVisibility(event) {
        event.preventDefault();
    }
    _onOpen() {
        this.setState({ open: true });
    }
    _onClose() {
        // close the dialog and blank the form
        this.setState(AskDialog.initialState({ options: this.state.options }));
        this.props.handleClose();
    }
    async _onSubmit(event) {
        event.preventDefault();
        this.props.handleSubmit(this.state.values);
        this._onClose();
    }
    _setValue(url, key, value) {
        const urlValues = { ...this.state.values[url], [key]: value };
        this.setState({
            values: { ...this.state.values, [url]: urlValues },
        });
    }
    _toggleVisibility(url, key) {
        var _a;
        const urlVis = {
            ...this.state.visibility[url],
            [key]: !((_a = this.state.visibility[url]) === null || _a === void 0 ? void 0 : _a[key]),
        };
        this.setState({
            visibility: { ...this.state.visibility, [url]: urlVis },
        });
    }
}
AskDialog.displayName = "AskDialog";
/**
 * A namespace for AskDialog statics.
 */
(function (AskDialog) {
    /**
     * The initial state for a new AskDialog
     */
    AskDialog.initialState = ({ open = false, options, }) => ({
        open,
        options: { ...options },
        values: {},
        visibility: {},
    });
})(AskDialog || (AskDialog = {}));


/***/ }),

/***/ "./lib/clipboard.js":
/*!**************************!*\
  !*** ./lib/clipboard.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   JupyterClipboard: () => (/* binding */ JupyterClipboard)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var tree_finder__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! tree-finder */ "webpack/sharing/consume/default/tree-finder/tree-finder");
/* harmony import */ var tree_finder__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(tree_finder__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _contents_utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./contents_utils */ "./lib/contents_utils.js");
/******************************************************************************
 *
 * Copyright (c) 2019, the jupyter-fs authors.
 *
 * This file is part of the jupyter-fs library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */




class JupyterClipboard {
    constructor(tracker) {
        this._model = new tree_finder__WEBPACK_IMPORTED_MODULE_2__.ClipboardModel();
        this._drive = new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.Drive();
        this._tracker = tracker;
        // eslint-disable-next-line @typescript-eslint/no-misused-promises
        this._model.deleteSub.subscribe(async (memo) => {
            await Promise.all(memo.map(s => this._onDelete(s)));
            const contentsModel = this._tracker.currentWidget.treefinder.model;
            const toRefresh = (0,_contents_utils__WEBPACK_IMPORTED_MODULE_3__.getRefreshTargets)(memo, contentsModel.root, true);
            this.model.refresh(contentsModel, toRefresh);
        });
        // eslint-disable-next-line @typescript-eslint/no-misused-promises
        this._model.pasteSub.subscribe(async ({ destination, doCut, memo }) => {
            const destPath = destination.kind === "dir" ? destination.path : destination.path.slice(0, -1);
            const destPathstr = tree_finder__WEBPACK_IMPORTED_MODULE_2__.Path.fromarray(destPath);
            await Promise.all(memo.map(s => this._onPaste(s, destPathstr, doCut)));
            const contentsModel = this._tracker.currentWidget.treefinder.model;
            let toRefresh = (0,_contents_utils__WEBPACK_IMPORTED_MODULE_3__.getRefreshTargets)([destination], contentsModel.root, false);
            // Only refresh sources if cutting:
            if (doCut && toRefresh !== undefined) {
                const extra = (0,_contents_utils__WEBPACK_IMPORTED_MODULE_3__.getRefreshTargets)(memo, contentsModel.root, false);
                if (extra === undefined) {
                    toRefresh = undefined;
                }
                else {
                    toRefresh.push(...extra);
                }
            }
            this.model.refresh(contentsModel, toRefresh);
        });
    }
    refresh(tm, memo) {
        tm !== null && tm !== void 0 ? tm : (tm = this._tracker.currentWidget.treefinder.model);
        this.model.refresh(tm, memo);
    }
    // TODO: remove in favor of this.model.refreshSelection once tree-finder v0.0.14 is out
    refreshSelection(tm) {
        this.refresh(tm, tm.selection.map(x => x.row));
    }
    get model() {
        return this._model;
    }
    async _onDelete(src) {
        const srcPathstr = tree_finder__WEBPACK_IMPORTED_MODULE_2__.Path.fromarray(src.path);
        try {
            await this._drive.delete(srcPathstr);
        }
        catch (err) {
            await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Delete Failed", err);
        }
    }
    async _onPaste(src, destPathstr, doCut) {
        const srcPathstr = tree_finder__WEBPACK_IMPORTED_MODULE_2__.Path.fromarray(src.path);
        try {
            await this._drive.copy(srcPathstr, destPathstr);
            if (doCut) {
                await this._drive.delete(srcPathstr);
            }
        }
        catch (err) {
            await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Paste Error", err);
        }
    }
}


/***/ }),

/***/ "./lib/commands.js":
/*!*************************!*\
  !*** ./lib/commands.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   commandIDs: () => (/* binding */ commandIDs),
/* harmony export */   commandNames: () => (/* binding */ commandNames),
/* harmony export */   createCommands: () => (/* binding */ createCommands),
/* harmony export */   idFromResource: () => (/* binding */ idFromResource)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var tree_finder__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! tree-finder */ "webpack/sharing/consume/default/tree-finder/tree-finder");
/* harmony import */ var tree_finder__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(tree_finder__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _treefinder__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./treefinder */ "./lib/treefinder.js");
/* harmony import */ var _contents_utils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./contents_utils */ "./lib/contents_utils.js");
/******************************************************************************
 *
 * Copyright (c) 2019, the jupyter-fs authors.
 *
 * This file is part of the jupyter-fs library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */








// define the command ids as a constant tuple
const commandNames = [
    "copy",
    "cut",
    "delete",
    "open",
    "paste",
    "refresh",
    "rename",
    "download",
    "create_folder",
    // "create_file",
    // "navigate",
    "copyFullPath",
    "copyRelativePath",
    "toggleColumnPath",
    "toggleColumn",
];
const commandIDs = Object.fromEntries(commandNames.map(name => [name, `treefinder:${name}`]));
const COLUMN_NAMES = [
    "size",
    "last_modified",
    "writable",
    "mimetype",
];
function idFromResource(resource) {
    return [resource.name.split(" ").join(""), resource.drive].join("_");
}
const currentWidgetSelectionIsWritable = (tracker) => {
    var _a;
    if (!tracker.currentWidget) {
        return false;
    }
    const selection = (_a = tracker.currentWidget.treefinder.model) === null || _a === void 0 ? void 0 : _a.selection;
    if (selection) {
        return selection.every((x) => x.row.writable);
    }
    return false;
};
function toggleColumnCommandId(column) {
    return `${commandIDs.toggleColumn}-${column}`;
}
function _getRelativePaths(selectedFiles) {
    const allPaths = [];
    for (const file of selectedFiles) {
        const relativePath = file.getPathAtDepth(1).join("/");
        allPaths.push(relativePath);
    }
    return allPaths;
}
function createCommands(app, tracker, clipboard, resources, settings) {
    var _a;
    const selector = ".jp-tree-finder-sidebar";
    const submenu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Menu({ commands: app.commands });
    submenu.title.label = "Show/Hide Columns";
    submenu.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.filterListIcon;
    submenu.addItem({ command: commandIDs.toggleColumnPath });
    for (const column of COLUMN_NAMES) {
        submenu.addItem({ command: toggleColumnCommandId(column) });
    }
    // const toggleState: {[key: string]: {[key: string]: boolean}} = {};
    // for (let resource of resources) {
    //   const colsToDisplay = resource.displayColumns as string[] ?? ['size'];
    //   const id = idFromResource(resource);
    //   toggleState[id] = {};
    //   const state = toggleState[id];
    //   for (let key of COLUMN_NAMES) {
    //     state[key] = colsToDisplay.includes(key);
    //   }
    // }
    const toggleState = {};
    const colsToDisplay = (_a = settings === null || settings === void 0 ? void 0 : settings.composite.display_columns) !== null && _a !== void 0 ? _a : ["size"];
    for (const key of COLUMN_NAMES) {
        toggleState[key] = colsToDisplay.includes(key);
    }
    let contextMenuRank = 1;
    // globally accessible jupyter commands[
    return [
        app.commands.addCommand(commandIDs.copy, {
            execute: args => clipboard.model.copySelection(tracker.currentWidget.treefinder.model),
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.copyIcon,
            label: "Copy",
            isVisible: () => {
                var _a;
                const widget = tracker.currentWidget;
                if (!widget) {
                    return false;
                }
                // Copy of folders are unsupported
                if ((_a = widget.treefinder.model) === null || _a === void 0 ? void 0 : _a.selection.some(v => v.row.kind === "dir")) {
                    return false;
                }
                return true;
            },
            isEnabled: () => !!tracker.currentWidget,
        }),
        app.commands.addCommand(commandIDs.cut, {
            execute: args => clipboard.model.cutSelection(tracker.currentWidget.treefinder.model),
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.cutIcon,
            label: "Cut",
            isEnabled: () => currentWidgetSelectionIsWritable(tracker),
        }),
        app.commands.addCommand(commandIDs.delete, {
            execute: async (args) => {
                const treefinder = tracker.currentWidget.treefinder;
                const model = treefinder.model;
                const message = model.selection.length === 1
                    ? `Are you sure you want to permanently delete: ${model.selection[0].name}?`
                    : `Are you sure you want to permanently delete the ${model.selection.length} selected items?`;
                const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                    title: "Delete",
                    body: message,
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: "Cancel" }),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.warnButton({ label: "Delete" }),
                    ],
                    // By default focus on "Cancel" to protect from accidental deletion
                    defaultButton: 0,
                });
                if (!treefinder.isDisposed && result.button.accept) {
                    clipboard.model.deleteSelection(model);
                }
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.closeIcon.bindprops({ stylesheet: "menuItem" }),
            label: "Delete",
            isEnabled: () => currentWidgetSelectionIsWritable(tracker),
        }),
        app.commands.addCommand(commandIDs.open, {
            execute: args => { var _a; return tracker.currentWidget.treefinder.model.openSub.next((_a = tracker.currentWidget.treefinder.selection) === null || _a === void 0 ? void 0 : _a.map(c => c.row)); },
            label: "Open",
            isEnabled: () => !!tracker.currentWidget,
        }),
        app.commands.addCommand(commandIDs.paste, {
            execute: args => clipboard.model.pasteSelection(tracker.currentWidget.treefinder.model),
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.pasteIcon,
            label: "Paste",
            isEnabled: () => !!tracker.currentWidget,
        }),
        app.commands.addCommand(commandIDs.rename, {
            execute: args => {
                const widget = tracker.currentWidget;
                const oldContent = widget.treefinder.selection[0];
                void _treefinder__WEBPACK_IMPORTED_MODULE_5__.TreeFinderSidebar.doRename(widget, oldContent).then(newContent => {
                    var _a;
                    (_a = widget.treefinder.model) === null || _a === void 0 ? void 0 : _a.renamerSub.next({ name: newContent.name, target: oldContent });
                    // TODO: Model state of TreeFinderWidget should be updated by renamerSub process.
                    oldContent.row = newContent;
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.editIcon,
            label: "Rename",
            isEnabled: () => currentWidgetSelectionIsWritable(tracker),
        }),
        app.commands.addCommand(commandIDs.download, {
            execute: async (args) => {
                const widget = tracker.currentWidget;
                const selection = widget.treefinder.selection;
                await Promise.allSettled(selection.map(s => widget.download(s.pathstr, s.hasChildren)));
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.downloadIcon,
            label: "Download",
            isEnabled: () => { var _a, _b; return !!((_b = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.treefinder.model) === null || _b === void 0 ? void 0 : _b.selection); },
        }),
        app.commands.addCommand(commandIDs.create_folder, {
            execute: async (args) => {
                var _a;
                const widget = tracker.currentWidget;
                const model = widget.treefinder.model;
                let target = (_a = model.selectedLast) !== null && _a !== void 0 ? _a : model.root;
                if (!target.hasChildren) {
                    target = await (0,_contents_utils__WEBPACK_IMPORTED_MODULE_6__.getContentParent)(target, model.root);
                }
                const path = tree_finder__WEBPACK_IMPORTED_MODULE_4__.Path.fromarray(target.row.path);
                let row;
                try {
                    row = await widget.treefinder.contentsProxy.newUntitled({
                        type: "directory",
                        path,
                    });
                }
                catch (e) {
                    void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Could not create folder", e);
                    return;
                }
                target.invalidate();
                const content = await (0,_contents_utils__WEBPACK_IMPORTED_MODULE_6__.revealAndSelectPath)(model, row.path);
                // Is this really needed?
                model.refreshSub.next((0,_contents_utils__WEBPACK_IMPORTED_MODULE_6__.getRefreshTargets)([target.row], model.root));
                // Scroll into view if not visible
                await _treefinder__WEBPACK_IMPORTED_MODULE_5__.TreeFinderSidebar.scrollIntoView(widget.treefinder, content.pathstr);
                const newContent = await _treefinder__WEBPACK_IMPORTED_MODULE_5__.TreeFinderSidebar.doRename(widget, content);
                model.renamerSub.next({ name: newContent.name, target: content });
                // TODO: Model state of TreeFinderWidget should be updated by renamerSub process.
                content.row = newContent;
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.newFolderIcon,
            label: "New Folder",
            isEnabled: () => !!tracker.currentWidget,
        }),
        app.commands.addCommand(commandIDs.refresh, {
            execute: args => {
                if (args["selection"]) {
                    clipboard.refreshSelection(tracker.currentWidget.treefinder.model);
                }
                else {
                    clipboard.refresh(tracker.currentWidget.treefinder.model);
                }
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.refreshIcon,
            label: args => args["selection"] ? "Refresh Selection" : "Refresh",
            isEnabled: () => !!tracker.currentWidget,
        }),
        app.commands.addCommand(commandIDs.copyFullPath, {
            execute: async (args) => {
                const widget = tracker.currentWidget;
                const trimEnd = (path) => path.trimEnd().replace(/\/+$/, "");
                const fullPaths = _getRelativePaths(widget.treefinder.selection).map(relativePath => { var _a; return [trimEnd((_a = widget.url) !== null && _a !== void 0 ? _a : ""), relativePath].join("/"); });
                await navigator.clipboard.writeText(fullPaths.join("\n"));
            },
            label: "Copy Full Path",
            isEnabled: () => !!tracker.currentWidget,
        }),
        app.commands.addCommand(commandIDs.copyRelativePath, {
            execute: async (args) => {
                const widget = tracker.currentWidget;
                const relativePaths = _getRelativePaths(widget.treefinder.selection);
                await navigator.clipboard.writeText(relativePaths.join("\n"));
            },
            label: "Copy Relative Path",
            isEnabled: () => !!tracker.currentWidget,
        }),
        app.commands.addCommand(commandIDs.toggleColumnPath, {
            execute: args => { },
            label: "path",
            isEnabled: () => false,
            isToggled: () => true,
        }),
        ...COLUMN_NAMES.map((column) => app.commands.addCommand(toggleColumnCommandId(column), {
            execute: async (args) => {
                toggleState[column] = !toggleState[column];
                await (settings === null || settings === void 0 ? void 0 : settings.set("display_columns", COLUMN_NAMES.filter(k => toggleState[k])));
            },
            label: column,
            isToggleable: true,
            isToggled: () => toggleState[column],
        })),
        // context menu items
        app.contextMenu.addItem({
            command: commandIDs.open,
            selector,
            rank: contextMenuRank++,
        }),
        app.contextMenu.addItem({
            command: commandIDs.copy,
            selector,
            rank: contextMenuRank++,
        }),
        app.contextMenu.addItem({
            command: commandIDs.cut,
            selector,
            rank: contextMenuRank++,
        }),
        app.contextMenu.addItem({
            command: commandIDs.paste,
            selector,
            rank: contextMenuRank++,
        }),
        app.contextMenu.addItem({
            command: commandIDs.delete,
            selector,
            rank: contextMenuRank++,
        }),
        app.contextMenu.addItem({
            command: commandIDs.rename,
            selector,
            rank: contextMenuRank++,
        }),
        app.contextMenu.addItem({
            command: commandIDs.download,
            selector,
            rank: contextMenuRank++,
        }),
        app.contextMenu.addItem({
            type: "separator",
            selector,
            rank: contextMenuRank++,
        }),
        app.contextMenu.addItem({
            command: commandIDs.copyFullPath,
            selector,
            rank: contextMenuRank++,
        }),
        app.contextMenu.addItem({
            command: commandIDs.copyRelativePath,
            selector,
            rank: contextMenuRank++,
        }),
        app.contextMenu.addItem({
            type: "separator",
            selector,
            rank: contextMenuRank++,
        }),
        app.contextMenu.addItem({
            type: "submenu",
            submenu,
            selector,
            rank: contextMenuRank++,
        }),
        app.contextMenu.addItem({
            args: { selection: true },
            command: commandIDs.refresh,
            selector,
            rank: contextMenuRank++,
        }),
    ].reduce((set, d) => {
        set.add(d);
        return set;
    }, new _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__.DisposableSet());
}


/***/ }),

/***/ "./lib/contents_proxy.js":
/*!*******************************!*\
  !*** ./lib/contents_proxy.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ContentsProxy: () => (/* binding */ ContentsProxy)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var tree_finder__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! tree-finder */ "webpack/sharing/consume/default/tree-finder/tree-finder");
/* harmony import */ var tree_finder__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(tree_finder__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Wrapper for a drive onto the contents manager.
 */
class ContentsProxy {
    constructor(contentsManager, drive) {
        this.contentsManager = contentsManager;
        this.drive = drive;
    }
    async get(path, options) {
        path = ContentsProxy.toFullPath(path, this.drive);
        return ContentsProxy.toJupyterContentRow(await this.contentsManager.get(path, options), this.contentsManager, this.drive);
    }
    async save(path, options) {
        path = ContentsProxy.toFullPath(path, this.drive);
        return ContentsProxy.toJupyterContentRow(await this.contentsManager.save(path, options), this.contentsManager, this.drive);
    }
    async rename(path, newPath) {
        path = ContentsProxy.toFullPath(path, this.drive);
        newPath = ContentsProxy.toFullPath(newPath, this.drive);
        return ContentsProxy.toJupyterContentRow(await this.contentsManager.rename(path, newPath), this.contentsManager, this.drive);
    }
    async newUntitled(options) {
        options.path = options.path && ContentsProxy.toFullPath(options.path, this.drive);
        return ContentsProxy.toJupyterContentRow(await this.contentsManager.newUntitled(options), this.contentsManager, this.drive);
    }
    async downloadUrl(path) {
        path = ContentsProxy.toFullPath(path, this.drive);
        return await this.contentsManager.getDownloadUrl(path);
    }
}
(function (ContentsProxy) {
    function toFullPath(path, drive) {
        if (!drive || path.startsWith(`${drive}:`)) {
            if (path.startsWith(`${drive}:/`)) {
                return path.replace(`${drive}:/`, `${drive}:`);
            }
            return path;
        }
        else if (path.startsWith(`${drive}/`)) {
            return [drive, path.slice(drive.length + 1)].join(":");
        }
        else {
            return [drive, path].join(":");
        }
    }
    ContentsProxy.toFullPath = toFullPath;
    function toLocalPath(path) {
        const [first, ...rest] = path.split("/");
        return [first.split(":").pop(), ...rest].join("/");
    }
    ContentsProxy.toLocalPath = toLocalPath;
    function toJupyterContentRow(row, contentsManager, drive) {
        const { path, type, ...rest } = row;
        const pathWithDrive = toFullPath(path, drive);
        const kind = type === "directory" ? "dir" : type;
        return {
            path: tree_finder__WEBPACK_IMPORTED_MODULE_1__.Path.toarray(pathWithDrive),
            kind,
            ...rest,
            ...(kind === "dir" ? {
                getChildren: async () => {
                    let contents;
                    try {
                        contents = await contentsManager.get(pathWithDrive, { content: true });
                    }
                    catch (error) {
                        void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Failed to get directory contents", error);
                        return [];
                    }
                    return contents.content.map(c => toJupyterContentRow(c, contentsManager, drive));
                },
            } : {}),
        };
    }
    ContentsProxy.toJupyterContentRow = toJupyterContentRow;
})(ContentsProxy || (ContentsProxy = {}));


/***/ }),

/***/ "./lib/contents_utils.js":
/*!*******************************!*\
  !*** ./lib/contents_utils.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getContentParent: () => (/* binding */ getContentParent),
/* harmony export */   getRefreshTargets: () => (/* binding */ getRefreshTargets),
/* harmony export */   revealAndSelectPath: () => (/* binding */ revealAndSelectPath),
/* harmony export */   revealPath: () => (/* binding */ revealPath)
/* harmony export */ });
/******************************************************************************
 *
 * Copyright (c) 2019, the jupyter-fs authors.
 *
 * This file is part of the jupyter-fs library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */
/**
 * Utilities for manipulating the tree-finder contents model
 */
/**
 * Walk the path from root, yielding all rows along the way
 *
 * @param path The path to walk to
 * @param root The root to start from
 */
async function* walkPath(path, root) {
    // Walk the path from the root
    const pathstr = path.join("/");
    if (!pathstr.startsWith(root.pathstr)) {
        throw new Error(`Path ${pathstr} not in ${root.pathstr}`);
    }
    let node = root;
    yield node;
    for (let i = root.row.path.length; i < path.length; ++i) {
        const children = await node.getChildren();
        const child = children === null || children === void 0 ? void 0 : children.find(c => c.name === path[i]);
        if (!child) {
            throw new Error(`Path ${pathstr} not in ${node.pathstr}`);
        }
        node = child;
        yield node;
    }
}
/**
 * Expand the contents nodes until path is exposed.
 *
 * This means that even if the final element of the path is a directory, its expanded state will
 * not change.
 *
 * @param contents The contents model that the path is in
 * @param path The path to expose, relative to the root (i.e. first entry matches path of root)
 */
async function revealPath(contents, path) {
    let node;
    for await (node of walkPath(path, contents.root)) {
        if (!node.isExpand && node.hasChildren) {
            await node.expand();
        }
    }
    return node;
}
/**
 * Expand the contents nodes until path is exposed, and select the node of that path.
 *
 * This means that even if the final element of the path is a directory, its expanded state will
 * not change.
 *
 * @param contents The contents model that the path is in
 * @param path The path to expose, relative to the root (i.e. first entry matches path of root)
 * @param add Whether or not to add the path to the current selection, or to replace the current selection @see TreeFinder.SelectionModel.select
 */
async function revealAndSelectPath(contents, path, add) {
    const node = await revealPath(contents, path);
    contents.selectionModel.select(node, add);
    return node;
}
/**
 * Get the parent contents row for the given contents row.
 *
 * Note: This will cause contents API calls if any dir has been invalidated between root and the parent.
 *
 * @param child The content node's whose parent we are looking for
 * @param root The root node of the path
 */
async function getContentParent(child, root) {
    // Walk from the root to the parent
    let node;
    for await (node of walkPath(child.row.path.slice(0, -1), root)) {
        // no-op
    }
    return node;
}
/**
 * Get targets to use for a call to tree-finder's refresh
 *
 * @param invalidateTargets The targets that need to be refreshed
 * @param root The root node of the contents tree
 * @param targetParents Whether the parents are the ones that should be invalidated
 * @returns
 */
function getRefreshTargets(invalidateTargets, root, targetParents = false) {
    const rootRefreshThreshold = root.row.path.length + (targetParents ? 1 : 0);
    const rootNeedsRefresh = invalidateTargets.some(t => t.path.length <= rootRefreshThreshold + (t.getChildren ? 0 : 1));
    if (rootNeedsRefresh) {
        return undefined;
    }
    if (targetParents) {
        // tree-finder doesn't correctly refresh parents of folders, so we work around it for now
        // (in more detail, tree-finder will only refresh the folder if the entry does not have a
        // getChildren entry, go figure...)
        return invalidateTargets.map(t => ({ ...t, getChildren: undefined }));
    }
    return invalidateTargets;
}


/***/ }),

/***/ "./lib/filesystem.js":
/*!***************************!*\
  !*** ./lib/filesystem.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FSComm: () => (/* binding */ FSComm)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/******************************************************************************
 *
 * Copyright (c) 2019, the jupyter-fs authors.
 *
 * This file is part of the jupyter-fs library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */


class FSCommBase {
    constructor(props = {}) {
        this._settings = undefined;
        const { baseUrl } = props;
        if (baseUrl) {
            this.baseUrl = baseUrl;
        }
    }
    get baseUrl() {
        return this.settings.baseUrl;
    }
    set baseUrl(baseUrl) {
        if (baseUrl !== this.baseUrl) {
            this._settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings({ baseUrl });
        }
    }
    get resourcesUrl() {
        return _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(this.baseUrl, "jupyterfs/resources");
    }
    get settings() {
        if (!this._settings) {
            this._settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
        }
        return this._settings;
    }
}
class FSComm extends FSCommBase {
    async getResourcesRequest() {
        const settings = this.settings;
        const fullUrl = this.resourcesUrl;
        return _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(fullUrl, { method: "GET" }, settings).then(response => {
            if (response.status !== 200) {
                return response.text().then(data => {
                    throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data);
                });
            }
            return response.json();
        });
    }
    async initResourceRequest(args) {
        const settings = this.settings;
        const fullUrl = this.resourcesUrl;
        return _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(fullUrl, {
            body: JSON.stringify(args),
            headers: {
                "Content-Type": "application/json",
            },
            method: "POST",
        }, settings).then(response => {
            if (response.status !== 200) {
                return response.text().then(data => {
                    throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data);
                });
            }
            return response.json();
        });
    }
}


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   driveIcon: () => (/* binding */ driveIcon),
/* harmony export */   fileTreeIcon: () => (/* binding */ fileTreeIcon),
/* harmony export */   jupyterFsIcon: () => (/* binding */ jupyterFsIcon),
/* harmony export */   visibilityIcon: () => (/* binding */ visibilityIcon),
/* harmony export */   visibilityOffIcon: () => (/* binding */ visibilityOffIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_drive_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/icons/drive.svg */ "./style/icons/drive.svg");
/* harmony import */ var _style_icons_file_tree_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/icons/file-tree.svg */ "./style/icons/file-tree.svg");
/* harmony import */ var _style_icons_jupyter_fs_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/icons/jupyter-fs.svg */ "./style/icons/jupyter-fs.svg");
/* harmony import */ var _style_icons_visibility_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/icons/visibility.svg */ "./style/icons/visibility.svg");
/* harmony import */ var _style_icons_visibility_off_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/icons/visibility-off.svg */ "./style/icons/visibility-off.svg");
/******************************************************************************
 *
 * Copyright (c) 2019, the jupyter-fs authors.
 *
 * This file is part of the jupyter-fs library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */






const driveIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({ name: "jfs:drive", svgstr: _style_icons_drive_svg__WEBPACK_IMPORTED_MODULE_1__ });
const fileTreeIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({ name: "jfs:file-tree", svgstr: _style_icons_file_tree_svg__WEBPACK_IMPORTED_MODULE_2__ });
const jupyterFsIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({ name: "jfs:jupyter-fs", svgstr: _style_icons_jupyter_fs_svg__WEBPACK_IMPORTED_MODULE_3__ });
const visibilityIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({ name: "jfs:visibility", svgstr: _style_icons_visibility_svg__WEBPACK_IMPORTED_MODULE_4__ });
const visibilityOffIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({ name: "jfs:visibility-off", svgstr: _style_icons_visibility_off_svg__WEBPACK_IMPORTED_MODULE_5__ });


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   browser: () => (/* binding */ browser),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   progressStatus: () => (/* binding */ progressStatus)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _auth__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./auth */ "./lib/auth.js");
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./commands */ "./lib/commands.js");
/* harmony import */ var _filesystem__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./filesystem */ "./lib/filesystem.js");
/* harmony import */ var _progress__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./progress */ "./lib/progress.js");
/* harmony import */ var _treefinder__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./treefinder */ "./lib/treefinder.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");
/******************************************************************************
 *
 * Copyright (c) 2019, the jupyter-fs authors.
 *
 * This file is part of the jupyter-fs library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */















// tslint:disable: variable-name
const BROWSER_ID = "jupyter-fs:plugin";
const browser = {
    autoStart: true,
    id: BROWSER_ID,
    requires: [
        _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__.IDocumentManager,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IWindowResolver,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager,
    ],
    provides: _tokens__WEBPACK_IMPORTED_MODULE_9__.ITreeFinderMain,
    async activate(app, manager, paths, resolver, restorer, router, settingRegistry, themeManager) {
        var _a;
        const comm = new _filesystem__WEBPACK_IMPORTED_MODULE_10__.FSComm();
        const widgetMap = {};
        let commands;
        // Attempt to load application settings
        let settings;
        try {
            settings = await settingRegistry.load(BROWSER_ID);
        }
        catch (error) {
            // eslint-disable-next-line no-console
            console.warn(`Failed to load settings for the jupyter-fs extension.\n${error}`);
        }
        let columns = (_a = settings === null || settings === void 0 ? void 0 : settings.composite.display_columns) !== null && _a !== void 0 ? _a : ["size"];
        const sharedSidebarProps = {
            app,
            manager,
            paths,
            resolver,
            restorer,
            router,
            columns,
        };
        function refreshWidgets({ resources, options }) {
            var _a;
            if (options.verbose) {
                // eslint-disable-next-line no-console
                console.info(`jupyter-fs frontend received resources:\n${JSON.stringify(resources)}`);
            }
            columns = (_a = settings === null || settings === void 0 ? void 0 : settings.composite.display_columns) !== null && _a !== void 0 ? _a : ["size"];
            sharedSidebarProps.columns = columns;
            // create the fs resource frontends (ie FileTree instances)
            for (const r of resources) {
                // make one composite disposable for all fs resource frontends
                const id = (0,_commands__WEBPACK_IMPORTED_MODULE_11__.idFromResource)(r);
                let w = widgetMap[id];
                if (!w || w.isDisposed) {
                    const sidebarProps = { ...sharedSidebarProps, url: r.url };
                    w = _treefinder__WEBPACK_IMPORTED_MODULE_12__.TreeFinderSidebar.sidebarFromResource(r, sidebarProps);
                    widgetMap[id] = w;
                }
                else {
                    w.treefinder.columns = columns;
                }
            }
            commands = (0,_commands__WEBPACK_IMPORTED_MODULE_11__.createCommands)(app, _treefinder__WEBPACK_IMPORTED_MODULE_12__.TreeFinderSidebar.tracker, _treefinder__WEBPACK_IMPORTED_MODULE_12__.TreeFinderSidebar.clipboard, resources, settings);
        }
        async function refresh() {
            // get user settings from json file
            let resources = settings.composite.resources;
            const options = settings.composite.options;
            function cleanup(all = false) {
                if (commands) {
                    commands.dispose();
                    commands = undefined;
                }
                const keys = resources.map(_commands__WEBPACK_IMPORTED_MODULE_11__.idFromResource);
                for (const key of Object.keys(widgetMap)) {
                    if (all || keys.indexOf(key) === -1) {
                        widgetMap[key].dispose();
                        delete widgetMap[key];
                    }
                }
            }
            try {
                // send user specs to backend; await return containing resources
                // defined by user settings + resources defined by server config
                resources = await comm.initResourceRequest({
                    resources,
                    options: {
                        ...options,
                        _addServerside: true,
                    },
                });
                if ((0,_auth__WEBPACK_IMPORTED_MODULE_13__.askRequired)(resources)) {
                    // ask for url template values, if required
                    const dialogElem = document.createElement("div");
                    document.body.appendChild(dialogElem);
                    const handleClose = () => {
                        react_dom__WEBPACK_IMPORTED_MODULE_8__.unmountComponentAtNode(dialogElem);
                        dialogElem.remove();
                    };
                    const handleSubmit = async (values) => {
                        resources = await comm.initResourceRequest({
                            resources: resources.map(r => ({ ...r, tokenDict: values[r.url] })),
                            options,
                        });
                        cleanup();
                        refreshWidgets({ resources, options });
                    };
                    react_dom__WEBPACK_IMPORTED_MODULE_8__.render(react__WEBPACK_IMPORTED_MODULE_7__.createElement(_auth__WEBPACK_IMPORTED_MODULE_13__.AskDialog, { handleClose: handleClose, handleSubmit: handleSubmit, options: options, resources: resources }), dialogElem);
                }
                else {
                    // otherwise, just go ahead and refresh the widgets
                    cleanup();
                    refreshWidgets({ options, resources });
                }
            }
            catch {
                cleanup(true);
            }
        }
        // initial setup when DOM attachment of custom elements is complete.
        void app.started.then(refresh);
        if (settings) {
            // rerun setup whenever relevant settings change
            settings.changed.connect(() => {
                void refresh();
            });
        }
        // Inject lab icons
        const style = document.createElement("style");
        style.setAttribute("id", "jupyter-fs-icon-inject");
        // Hackish, but needed since free-finder insists on pseudo elements for icons.
        function iconStyleContent(folderStr, fileStr) {
            // Note: We aren't able to style the hover/select colors with this.
            return `
      .jp-tree-finder {
        --tf-dir-icon: url('data:image/svg+xml,${encodeURIComponent(folderStr)}');
        --tf-file-icon: url('data:image/svg+xml,${encodeURIComponent(fileStr)}');
      }
      `;
        }
        themeManager.themeChanged.connect(() => {
            // Update SVG icon fills (since we put them in pseudo-elements we cannot style with CSS)
            const primary = getComputedStyle(document.documentElement).getPropertyValue("--jp-ui-font-color1");
            style.textContent = iconStyleContent(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__.folderIcon.svgstr.replace(/fill="([^"]{0,7})"/, `fill="${primary}"`), _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__.fileIcon.svgstr.replace(/fill="([^"]{0,7})"/, `fill="${primary}"`));
            // Refresh widgets in case font/border sizes etc have changed
            void Promise.all(Object.keys(widgetMap).map(key => widgetMap[key].treefinder.nodeInit()));
        });
        style.textContent = iconStyleContent(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__.folderIcon.svgstr, _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__.fileIcon.svgstr);
        document.head.appendChild(style);
        return { tracker: _treefinder__WEBPACK_IMPORTED_MODULE_12__.TreeFinderSidebar.tracker };
    },
};
const PROGRESS_ID = "jupyter-fs:progress";
const progressStatus = {
    autoStart: true,
    id: PROGRESS_ID,
    requires: [
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator,
    ],
    optional: [
        _tokens__WEBPACK_IMPORTED_MODULE_9__.ITreeFinderMain,
        _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_4__.IStatusBar,
    ],
    async activate(app, translator, main, statusbar) {
        if (!statusbar || !main) {
            return;
        }
        const item = new _progress__WEBPACK_IMPORTED_MODULE_14__.FileUploadStatus({
            tracker: main.tracker,
            translator,
        });
        statusbar.registerStatusItem(PROGRESS_ID, {
            item,
            align: "middle",
            isActive: () => { var _a; return !!((_a = item.model) === null || _a === void 0 ? void 0 : _a.items.length); },
            activeStateChanged: item.model.stateChanged,
        });
    },
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([
    browser,
    progressStatus,
]);


/***/ }),

/***/ "./lib/progress.js":
/*!*************************!*\
  !*** ./lib/progress.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FileUploadStatus: () => (/* binding */ FileUploadStatus)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_4__);
/******************************************************************************
 *
 * Copyright (c) 2019, the jupyter-fs authors.
 *
 * This file is part of the jupyter-fs library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */
/* Based on code from JupyterLab, copied under the following license:

Copyright (c) 2015-2021 Project Jupyter Contributors
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/





/**
 * Half-spacing between items in the overall status item.
 */
const HALF_SPACING = 4;
/**
 * A pure function component for a FileUpload status item.
 *
 * @param props: the props for the component.
 *
 * @returns a tsx component for the file upload status.
 */
function FileUploadComponent(props) {
    const translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
    const trans = translator.load("jupyterlab");
    const items = [react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.TextItem, { source: trans.__("Uploading…") })];
    items.push(...props.items.map(i => i.complete ?
        react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.TextItem, { source: trans.__("Complete!") }) :
        react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.ProgressBar, { percentage: i.progress })));
    return (react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.GroupItem, { spacing: HALF_SPACING }, ...items));
}
/**
 * The time for which to show the "Complete!" message after uploading.
 */
const UPLOAD_COMPLETE_MESSAGE_MILLIS = 2000;
/**
 * Status bar item to display file upload progress.
 */
class FileUploadStatus extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    /**
     * Construct a new FileUpload status item.
     */
    constructor(opts) {
        super(new FileUploadStatus.Model(opts.tracker.currentWidget));
        this._onTreeFinderChange = (tracker, sidebar) => {
            if (sidebar === null) {
                this.model.sidebar = null;
            }
            else {
                this.model.sidebar = sidebar;
            }
        };
        this.translator = opts.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        this._tracker = opts.tracker;
        this._tracker.currentChanged.connect(this._onTreeFinderChange);
    }
    /**
     * Render the FileUpload status.
     */
    render() {
        const items = this.model.items;
        if (items.length > 0) {
            return (react__WEBPACK_IMPORTED_MODULE_4___default().createElement(FileUploadComponent, { items: this.model.items, translator: this.translator }));
        }
        else {
            return react__WEBPACK_IMPORTED_MODULE_4___default().createElement((react__WEBPACK_IMPORTED_MODULE_4___default().Fragment), null);
        }
    }
    dispose() {
        super.dispose();
        this._tracker.currentChanged.disconnect(this._onTreeFinderChange);
    }
}
/**
 * A namespace for FileUpload class statics.
 */
(function (FileUploadStatus) {
    /**
     * The VDomModel for the FileUpload renderer.
     */
    class Model extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
        /**
         * Construct a new model.
         */
        constructor(sidebar) {
            super();
            /**
             * Handle an uploadChanged event in the filebrowser model.
             */
            this._uploadChanged = (uploader, uploads) => {
                if (uploads.name === "start") {
                    this._items.push({
                        path: uploads.newValue.path,
                        progress: uploads.newValue.progress * 100,
                        complete: false,
                    });
                }
                else if (uploads.name === "update") {
                    const idx = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.ArrayExt.findFirstIndex(this._items, val => val.path === uploads.oldValue.path);
                    if (idx !== -1) {
                        this._items[idx].progress = uploads.newValue.progress * 100;
                    }
                }
                else if (uploads.name === "finish") {
                    const finishedItem = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.ArrayExt.findFirstValue(this._items, val => val.path === uploads.oldValue.path);
                    if (finishedItem) {
                        finishedItem.complete = true;
                        setTimeout(() => {
                            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.ArrayExt.removeFirstOf(this._items, finishedItem);
                            this.stateChanged.emit(void 0);
                        }, UPLOAD_COMPLETE_MESSAGE_MILLIS);
                    }
                }
                else if (uploads.name === "failure") {
                    _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.ArrayExt.removeFirstWhere(this._items, val => val.path === uploads.newValue.path);
                }
                this.stateChanged.emit(void 0);
            };
            this._items = [];
            this._sidebar = null;
            this.sidebar = sidebar;
        }
        /**
         * The currently uploading items.
         */
        get items() {
            return this._items;
        }
        /**
         * The current file browser model.
         */
        get sidebar() {
            return this._sidebar;
        }
        set sidebar(browserModel) {
            const oldSidebar = this._sidebar;
            if (oldSidebar) {
                oldSidebar.treefinder.uploader.uploadChanged.disconnect(this._uploadChanged);
            }
            this._sidebar = browserModel;
            this._items = [];
            if (this._sidebar !== null) {
                this._sidebar.treefinder.uploader.uploadChanged.connect(this._uploadChanged);
            }
            this.stateChanged.emit(void 0);
        }
    }
    FileUploadStatus.Model = Model;
})(FileUploadStatus || (FileUploadStatus = {}));


/***/ }),

/***/ "./lib/tokens.js":
/*!***********************!*\
  !*** ./lib/tokens.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ITreeFinderMain: () => (/* binding */ ITreeFinderMain)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

const ITreeFinderMain = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token("@jupyterlab/filebrowser:IFileBrowserFactory");


/***/ }),

/***/ "./lib/treefinder.js":
/*!***************************!*\
  !*** ./lib/treefinder.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TreeFinderSidebar: () => (/* binding */ TreeFinderSidebar),
/* harmony export */   TreeFinderTracker: () => (/* binding */ TreeFinderTracker),
/* harmony export */   TreeFinderWidget: () => (/* binding */ TreeFinderWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var tree_finder__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! tree-finder */ "webpack/sharing/consume/default/tree-finder/tree-finder");
/* harmony import */ var tree_finder__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(tree_finder__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _clipboard__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./clipboard */ "./lib/clipboard.js");
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./commands */ "./lib/commands.js");
/* harmony import */ var _contents_proxy__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./contents_proxy */ "./lib/contents_proxy.js");
/* harmony import */ var _contents_utils__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./contents_utils */ "./lib/contents_utils.js");
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _upload__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./upload */ "./lib/upload.js");

// import { PathExt, URLExt } from "@jupyterlab/coreutils";



// import JSZip from "jszip";










class TreeFinderTracker extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.WidgetTracker {
    constructor() {
        super(...arguments);
        this._finders = new Map();
    }
    async add(finder) {
        this._finders.set(finder.id, finder);
        // eslint-disable-next-line @typescript-eslint/unbound-method
        finder.disposed.connect(this._onWidgetDisposed, this);
        return super.add(finder);
    }
    remove(finder) {
        this._finders.delete(finder.id);
        // eslint-disable-next-line @typescript-eslint/unbound-method
        finder.disposed.disconnect(this._onWidgetDisposed, this);
    }
    findByDrive(drive) {
        return this._finders.get(drive);
    }
    hasByDrive(drive) {
        return this._finders.has(drive);
    }
    _onWidgetDisposed(finder) {
        this.remove(finder);
    }
}
class TreeFinderWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget {
    constructor({ app, columns, rootPath = "", translator, }) {
        const { commands, serviceManager: { contents } } = app;
        const node = document.createElement("tree-finder-panel");
        super({ node });
        this.addClass("jp-tree-finder");
        this.contentsProxy = new _contents_proxy__WEBPACK_IMPORTED_MODULE_7__.ContentsProxy(contents, rootPath);
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        this._trans = this.translator.load("jupyterlab");
        this._commands = commands;
        this._columns = columns;
        this.rootPath = rootPath === "" ? rootPath : rootPath + ":";
        // CAREFUL: tree-finder currently REQUIRES the node to be added to the DOM before init can be called!
        this._ready = this.nodeInit();
        this._ready.catch(reason => (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Failed to init browser", reason));
    }
    draw() {
        var _a;
        (_a = this.model) === null || _a === void 0 ? void 0 : _a.requestDraw();
    }
    refresh() {
        var _a;
        (_a = this.model) === null || _a === void 0 ? void 0 : _a.refreshSub.next();
    }
    async nodeInit() {
        await this.contentsProxy.get(this.rootPath).then(root => this.node.init({
            root,
            gridOptions: {
                columnFormatters: {
                    last_modified: (x => tree_finder__WEBPACK_IMPORTED_MODULE_6__.Format.timeSince(x)),
                    size: (x => x && tree_finder__WEBPACK_IMPORTED_MODULE_6__.Format.bytesToHumanReadable(x)),
                    writable: (x => x ? "✓" : "╳"),
                },
                doWindowResize: true,
                showFilter: true,
            },
            modelOptions: {
                columnNames: this.columns,
            },
        })).then(() => {
            const grid = this.node.querySelector("tree-finder-grid");
            grid === null || grid === void 0 ? void 0 : grid.addStyleListener(() => {
                var _a, _b;
                // Fix corner cleanup (workaround for underlying bug where we end up with two resize handles)
                const resizeSpans = grid.querySelectorAll(`thead tr > th:first-child > span.rt-column-resize`);
                const nHeaderRows = grid.querySelectorAll("thead tr").length;
                if (resizeSpans.length > nHeaderRows) {
                    // something went wrong, and we ended up with double resize handles. Clear the classes from the first one:
                    for (const span of grid.querySelectorAll(`thead tr > th:first-child > span.rt-column-resize:first-child`)) {
                        span.removeAttribute("class");
                    }
                }
                // Fix focus and tabbing
                let lastSelectIdx = ((_a = this.model) === null || _a === void 0 ? void 0 : _a.selectedLast) ? (_b = this.model) === null || _b === void 0 ? void 0 : _b.contents.indexOf(this.model.selectedLast) : -1;
                for (const rowHeader of grid.querySelectorAll("tr > th")) {
                    const nameElement = rowHeader.querySelector("span.rt-group-name");
                    // Ensure we can tab to all items
                    nameElement === null || nameElement === void 0 ? void 0 : nameElement.setAttribute("tabindex", "0");
                    // Ensure last selected element retains focus after redraw:
                    if (nameElement && lastSelectIdx !== -1) {
                        const meta = grid.getMeta(rowHeader);
                        if (meta && meta.y === lastSelectIdx) {
                            nameElement.focus();
                            lastSelectIdx = -1;
                        }
                    }
                }
            });
            if (this.uploader) {
                this.uploader.model = this.model;
            }
            else {
                this.uploader = new _upload__WEBPACK_IMPORTED_MODULE_8__.Uploader({
                    contentsProxy: this.contentsProxy,
                    model: this.model,
                });
            }
            this.model.openSub.subscribe(rows => rows.forEach(row => {
                if (!row.getChildren) {
                    void this._commands.execute("docmanager:open", { path: tree_finder__WEBPACK_IMPORTED_MODULE_6__.Path.fromarray(row.path) });
                }
            }));
        });
    }
    get columns() {
        return this._columns;
    }
    set columns(value) {
        if (_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__.ArrayExt.shallowEqual(this._columns, value)) {
            return;
        }
        this._columns = value;
        const m = this.model;
        m.options = {
            ...m.options,
            columnNames: this._columns,
        };
        m.initColumns();
        void this.nodeInit();
    }
    get ready() {
        return this._ready;
    }
    get model() {
        return this.node.model;
    }
    get selection() {
        var _a;
        return (_a = this.model) === null || _a === void 0 ? void 0 : _a.selection;
    }
    get selectionPathstrs() {
        var _a;
        return (_a = this.model) === null || _a === void 0 ? void 0 : _a.selection.map(c => tree_finder__WEBPACK_IMPORTED_MODULE_6__.Path.fromarray(c.row.path));
    }
    /**
     * Handle the DOM events for the tree view.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the panel's DOM node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case "keydown":
                this.evtKeydown(event);
                break;
            case "dragenter":
            case "dragover":
                this.evtNativeDragOverEnter(event);
                break;
            case "dragleave":
            case "dragend":
                this.evtNativeDragLeaveEnd(event);
                break;
            case "drop":
                this.evtNativeDrop(event);
                break;
            default:
                break;
        }
    }
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        const node = this.node;
        node.addEventListener("keydown", this);
        node.addEventListener("dragenter", this);
        node.addEventListener("dragover", this);
        node.addEventListener("dragleave", this);
        node.addEventListener("dragend", this);
        node.addEventListener("drop", this);
    }
    /**
     * A message handler invoked on a `'before-detach'` message.
     */
    onBeforeDetach(msg) {
        super.onBeforeDetach(msg);
        const node = this.node;
        node.removeEventListener("keydown", this);
        node.removeEventListener("dragover", this);
        node.removeEventListener("dragover", this);
        node.removeEventListener("dragleave", this);
        node.removeEventListener("dragend", this);
        node.removeEventListener("drop", this);
    }
    _findEventRowElement(event, selector) {
        let node = event.target;
        while (node.parentElement && node.parentElement !== this.node) {
            if (node.matches(selector)) {
                return node;
            }
            node = node.parentElement;
        }
    }
    selectNeighbour(diff, asRange) {
        const model = this.model;
        let last = model.selectedLast;
        // tree-finder has a bug where it doesn't update selectedLast in `selectRange`, hacky work-around for now:
        const { range, pivot } = model.selectionModel;
        // once bug is fixed, this conditional should never be true:
        if (pivot && pivot === (last === null || last === void 0 ? void 0 : last.pathstr) && range && range.length >= 1) {
            // get the part of range that is furthest away from pivot:
            const paths = model.contents.map(c => c.pathstr);
            const pivotIdx = paths.indexOf(pivot);
            const rangeStartIdx = paths.indexOf(range[0]);
            const rangeEndIdx = paths.indexOf(range[range.length - 1]);
            if (pivotIdx < rangeStartIdx) {
                last = model.contents[rangeEndIdx];
            }
            else {
                last = model.contents[rangeStartIdx];
            }
        }
        let idx = last
            ? model.contents.indexOf(last)
            : diff < 0
                ? model.contents.length - 1 // select last item
                : 0; // select first item
        if (last) {
            idx = idx + diff;
        }
        if (idx < 0 || idx >= model.contents.length) {
            return; // Do nothing if going past the edge
        }
        const next = model.contents[idx];
        if (asRange) {
            model.selectionModel.selectRange(next, model.contents);
        }
        else {
            model.selectionModel.select(next);
        }
        void TreeFinderSidebar.scrollIntoView(this, next.pathstr);
    }
    evtKeydown(event) {
        switch (event.key) {
            case "ArrowDown":
            case "ArrowUp":
                event.stopPropagation();
                event.preventDefault();
                this.selectNeighbour(event.key === "ArrowUp" ? -1 : 1, event.shiftKey);
                break;
        }
    }
    evtNativeDragOverEnter(event) {
        const row = this._findEventRowElement(event, "tree-finder-grid tr");
        if (row) {
            row.classList.add("jfs-mod-native-drop");
        }
        event.preventDefault();
    }
    evtNativeDragLeaveEnd(event) {
        const row = this._findEventRowElement(event, ".jfs-mod-native-drop");
        if (row) {
            row.classList.remove("jfs-mod-native-drop");
        }
    }
    /**
     * Handle the `drop` event for the widget.
     */
    evtNativeDrop(event) {
        var _a, _b, _c;
        const row = this.node.querySelector(".jfs-mod-native-drop");
        if (row) {
            row.classList.remove("jfs-mod-native-drop");
        }
        const files = (_a = event.dataTransfer) === null || _a === void 0 ? void 0 : _a.files;
        if (!files || files.length === 0) {
            return;
        }
        const length = (_b = event.dataTransfer) === null || _b === void 0 ? void 0 : _b.items.length;
        if (!length) {
            return;
        }
        for (let i = 0; i < length; i++) {
            const entry = (_c = event.dataTransfer) === null || _c === void 0 ? void 0 : _c.items[i].webkitGetAsEntry();
            if (entry === null || entry === void 0 ? void 0 : entry.isDirectory) {
                void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                    title: this._trans.__("Error Uploading Folder"),
                    body: this._trans.__("Drag and Drop is currently not supported for folders"),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: this._trans.__("Close") })],
                });
            }
        }
        event.preventDefault();
        // Translate row element to contents row
        let target = this.model.root;
        if (row) {
            const grid = this.node.querySelector("tree-finder-grid");
            const metadata = grid.getMeta(row.querySelector("th"));
            if (metadata.y) {
                target = this.model.contents[metadata.y];
            }
        }
        for (let i = 0; i < files.length; i++) {
            void this.uploader.upload(files[i], target);
        }
    }
}
class TreeFinderSidebar extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget {
    constructor({ app, columns, url, rootPath = "", caption = "TreeFinder", id = "jupyterlab-tree-finder", }) {
        super();
        this.id = id;
        this.node.classList.add("jfs-mod-notRenaming");
        this.url = url;
        this.title.icon = _icons__WEBPACK_IMPORTED_MODULE_9__.fileTreeIcon;
        this.title.caption = caption;
        this.addClass("jp-tree-finder-sidebar");
        this.toolbar = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Toolbar();
        this.toolbar.addClass("jp-tree-finder-toolbar");
        this.treefinder = new TreeFinderWidget({ app, rootPath, columns });
        this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.PanelLayout();
        this.layout.addWidget(this.toolbar);
        this.layout.addWidget(this.treefinder);
    }
    restore() {
        void this.treefinder.ready.then(() => this.treefinder.refresh());
        // const array: Array<Promise<any>> = [];
        // Object.keys(this.controller).forEach(key => {
        //   if (this.controller[key].open && (key !== "")) {
        //     const promise = this.cm.get(this.basepath + key);
        //     promise.catch(res => {
        //       // eslint-disable-next-line no-console
        //       console.log(res);
        //     });
        //     array.push(promise);
        //   }
        // });
        // Promise.all(array).then(results => {
        //   for (const r in results) {
        //     const row_element = this.node.querySelector("[id='" + u_btoa(results[r].path.replace(this.basepath, "")) + "']");
        //     this.buildTableContents(results[r].content, 1 + results[r].path.split("/").length, row_element);
        //   }
        // }).catch(reasons => {
        //   // eslint-disable-next-line no-console
        //   console.log(reasons);
        // });
    }
    async download(path, folder) {
        if (folder) {
            // const zip = new JSZip();
            // await this.wrapFolder(zip, path); // folder packing
            // // generate and save zip, reset path
            // path = PathExt.basename(path);
            // writeZipFile(zip, path);
        }
        else {
            const url = await this.treefinder.contentsProxy.downloadUrl(path);
            const element = document.createElement("a");
            element.setAttribute("href", url);
            element.setAttribute("download", "");
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
        }
    }
    // async wrapFolder(zip: JSZip, path: string) {
    //   const base = this.cm.get(this.basepath + path);
    //   const next = base.then(async res => {
    //     if (res.type === "directory") {
    //       const new_folder = zip.folder(res.name);
    //       for (const c in res.content) {
    //         await this.wrapFolder(new_folder, res.content[c].path);
    //       }
    //     } else {
    //       zip.file(res.name, res.content);
    //     }
    //   });
    //   await next;
    // }
    onBeforeShow(msg) {
        this.treefinder.refresh();
        this.treefinder.draw();
    }
    onResize(msg) {
        this.treefinder.draw();
    }
}
// eslint-disable-next-line @typescript-eslint/no-namespace
(function (TreeFinderSidebar) {
    const namespace = "jupyter-fs:TreeFinder";
    TreeFinderSidebar.tracker = new TreeFinderTracker({ namespace });
    TreeFinderSidebar.clipboard = new _clipboard__WEBPACK_IMPORTED_MODULE_10__.JupyterClipboard(TreeFinderSidebar.tracker);
    function sidebarFromResource(resource, props) {
        return sidebar({
            ...props,
            rootPath: resource.drive,
            caption: `${resource.name}\nFile Tree`,
            id: (0,_commands__WEBPACK_IMPORTED_MODULE_11__.idFromResource)(resource),
            url: resource.url,
        });
    }
    TreeFinderSidebar.sidebarFromResource = sidebarFromResource;
    function sidebar({ app, 
    // manager,
    // paths,
    // resolver,
    // router,
    restorer, url, columns, rootPath = "", caption = "TreeFinder", id = "jupyterlab-tree-finder", side = "left", }) {
        const widget = new TreeFinderSidebar({ app, rootPath, columns, caption, id, url });
        void widget.treefinder.ready.then(() => TreeFinderSidebar.tracker.add(widget));
        restorer.add(widget, widget.id);
        app.shell.add(widget, side);
        const new_file_button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.newFolderIcon,
            onClick: () => {
                void app.commands.execute((_commands__WEBPACK_IMPORTED_MODULE_11__.commandIDs.create_folder));
            },
            tooltip: "New Folder",
        });
        const uploader_button = new _upload__WEBPACK_IMPORTED_MODULE_8__.UploadButton({ uploader: widget.treefinder.ready.then(() => widget.treefinder.uploader) });
        void widget.treefinder.ready.then(() => {
            widget.treefinder.uploader.uploadCompleted.connect((sender, args) => {
                // Do not select/scroll into view: Upload might be slow, so user might have moved on!
                // We do however want to expand the folder
                void (0,_contents_utils__WEBPACK_IMPORTED_MODULE_12__.revealPath)(widget.treefinder.model, args.path).then(() => widget.treefinder.model.flatten());
            });
        });
        const refresh_button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.refreshIcon,
            onClick: () => {
                void app.commands.execute(_commands__WEBPACK_IMPORTED_MODULE_11__.commandIDs.refresh);
            },
            tooltip: "Refresh",
        });
        widget.toolbar.addItem("new file", new_file_button);
        widget.toolbar.addItem("upload", uploader_button);
        widget.toolbar.addItem("refresh", refresh_button);
        // // remove context highlight on context menu exit
        // document.ondblclick = () => {
        //   app.commands.execute((widget.commandIDs.set_context + ":" + widget.id), { path: "" });
        // };
        // widget.node.onclick = event => {
        //   app.commands.execute((widget.commandIDs.select + ":" + widget.id), { path: "" });
        // };
        // setInterval(() => {
        //   app.commands.execute(widget.commandIDs.refresh);
        // }, 10000);
        // return a disposable containing all disposables associated
        // with this widget, ending with the widget itself
        return widget;
    }
    TreeFinderSidebar.sidebar = sidebar;
    async function doRename(widget, oldContent) {
        var _a;
        if (widget.node.classList.contains("jfs-mod-renaming")) {
            return oldContent.row;
        }
        const textNode = widget.node.querySelector("tr.tf-mod-select .rt-tree-container .rt-group-name").firstChild;
        const original = textNode.textContent.replace(/(.*)\/$/, "$1");
        const editNode = document.createElement("input");
        editNode.value = original;
        try {
            widget.node.classList.replace("jfs-mod-notRenaming", "jfs-mod-renaming");
            const newName = await (0,_utils__WEBPACK_IMPORTED_MODULE_13__.promptRename)(textNode, editNode, original);
            (_a = textNode.parentElement) === null || _a === void 0 ? void 0 : _a.focus();
            if (!newName || newName === oldContent.name) {
                return oldContent.row;
            }
            if (!(0,_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__.isValidFileName)(newName)) {
                void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Rename Error", Error(newName + ' is not a valid name. Names must have nonzero length, and cannot include "/", "\\", or ":"'));
                return oldContent.row;
            }
            const oldPath = oldContent.getPathAtDepth(1).join("/");
            const newPath = oldPath.slice(0, -1 * original.length) + newName;
            const suffix = textNode.textContent.endsWith("/") ? "/" : "";
            let newContent;
            try {
                newContent = await widget.treefinder.contentsProxy.rename(oldPath + suffix, newPath + suffix);
            }
            catch (error) {
                if (error !== "File not renamed") {
                    void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Rename Error", error);
                }
                newContent = oldContent.row;
            }
            textNode.textContent = newName + suffix;
            return newContent;
        }
        finally {
            widget.node.classList.replace("jfs-mod-renaming", "jfs-mod-notRenaming");
        }
    }
    TreeFinderSidebar.doRename = doRename;
    /**
     * If a path entry is not in view, scroll it into view
     *
     * @param treefinder The view
     * @param pathstr The entry to show
     */
    async function scrollIntoView(treefinder, pathstr) {
        // tree-finder uses rxjs bits that don't allow you to await, so to ensure sync draw:
        const model = treefinder.model;
        await model.flatten();
        const grid = treefinder.node.querySelector("tree-finder-grid");
        // eslint-disable-next-line @typescript-eslint/await-thenable
        await grid.draw();
        // Check if new row (selection) in view (if outside virtual window, it will fail):
        if (!treefinder.node.querySelector(".tf-mod-select .rt-tree-container .rt-group-name")) {
            // We need to scroll the selection into view!
            const rowIdx = model.contents.findIndex(s => s.pathstr === pathstr);
            if (rowIdx !== -1) {
                // TODO: Should we perform a minimum scroll, or do we always want entry as close to the top of the view as possible?
                await grid.scrollToCell(0, rowIdx, 1, model.contents.length);
            }
        }
    }
    TreeFinderSidebar.scrollIntoView = scrollIntoView;
})(TreeFinderSidebar || (TreeFinderSidebar = {}));


/***/ }),

/***/ "./lib/upload.js":
/*!***********************!*\
  !*** ./lib/upload.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CHUNK_SIZE: () => (/* binding */ CHUNK_SIZE),
/* harmony export */   UploadButton: () => (/* binding */ UploadButton),
/* harmony export */   Uploader: () => (/* binding */ Uploader)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _contents_utils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./contents_utils */ "./lib/contents_utils.js");
/******************************************************************************
 *
 * Copyright (c) 2019, the jupyter-fs authors.
 *
 * This file is part of the jupyter-fs library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */
/* Based on code from JupyterLab, copied under the following license:

Copyright (c) 2015-2021 Project Jupyter Contributors
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/







/**
 * The size (in bytes) of the biggest chunk we should upload at once.
 */
const CHUNK_SIZE = 1024 * 1024;
class UploadButton extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton {
    /**
     * Construct a new file browser buttons widget.
     */
    constructor(options) {
        super({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.fileUploadIcon,
            label: options.label,
            onClick: () => {
                this._input.click();
            },
            tooltip: Private.translateToolTip(options.translator),
        });
        /**
         * The 'change' handler for the input field.
         */
        this._onInputChanged = () => {
            const files = Array.prototype.slice.call(this._input.files);
            const pending = files.map(async (file) => (await this._uploader).upload(file));
            void Promise.all(pending).catch(error => {
                void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)(this._trans._p("showErrorMessage", "Upload Error"), error);
            });
        };
        /**
         * The 'click' handler for the input field.
         */
        this._onInputClicked = () => {
            // In order to allow repeated uploads of the same file (with delete in between),
            // we need to clear the input value to trigger a change event.
            this._input.value = "";
        };
        this._input = Private.createUploadInput();
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        this._trans = this.translator.load("jupyterlab");
        this._uploader = options.uploader;
        this._input.onclick = this._onInputClicked;
        this._input.onchange = this._onInputChanged;
        this.addClass("jp-id-upload");
    }
}
/**
 * A widget which provides an upload button.
 */
class Uploader {
    /**
     * Construct a new file browser buttons widget.
     */
    constructor(options) {
        this._uploads = [];
        this._uploadChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        this._uploadCompleted = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        this._disposed = false;
        this.model = options.model;
        this._contentsProxy = options.contentsProxy;
    }
    /**
     * A signal emitted when an upload progresses.
     */
    get uploadChanged() {
        return this._uploadChanged;
    }
    /**
     * A signal emitted when an upload completes.
     */
    get uploadCompleted() {
        return this._uploadCompleted;
    }
    /**
     * Is this instance disposed?
     */
    get isDisposed() {
        return this._disposed;
    }
    /**
     * Dispose of the resources held by the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._disposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal.clearData(this);
    }
    /**
     * Upload a `File` object.
     *
     * @param file - The `File` object to upload.
     *
     * @returns A promise containing the new file contents model.
     */
    async upload(file, target) {
        await this._uploadCheckDisposed();
        target = target || this.model.selectedLast || this.model.root;
        if (!target.hasChildren) {
            target = await (0,_contents_utils__WEBPACK_IMPORTED_MODULE_6__.getContentParent)(target, this.model.root);
        }
        const path = target.pathstr ? target.pathstr + "/" + file.name : file.name;
        let res = null;
        try {
            // alternatively to try to get the file and check for 404, we can get the parent
            // and check if the file is in the list.
            res = await this._contentsProxy.get(path, { content: false });
        }
        catch (e) {
            // TODO: Check if e is a 404
        }
        if (res) {
            // drop drive when prompting:
            if (!await (0,_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__.shouldOverwrite)(path.slice(path.indexOf("/") + 1))) {
                return null;
            }
        }
        await this._uploadCheckDisposed();
        const chunkedUpload = file.size > CHUNK_SIZE;
        const uploaded = await this._upload(file, path, chunkedUpload);
        target.invalidate();
        this._uploadCompleted.emit({ path: uploaded.path });
        return uploaded;
    }
    /**
     * Perform the actual upload.
     */
    async _upload(file, path, chunked) {
        // Gather the file model parameters.
        const name = file.name;
        const type = "file";
        const format = "base64";
        const uploadInner = async (blob, chunk) => {
            await this._uploadCheckDisposed();
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            await new Promise((resolve, reject) => {
                reader.onload = resolve;
                reader.onerror = event => reject(`Failed to upload "${file.name}":  ${event}`);
            });
            await this._uploadCheckDisposed();
            // remove header https://stackoverflow.com/a/24289420/907060
            const content = reader.result.split(",")[1];
            const model = {
                type,
                format,
                name,
                chunk,
                content,
            };
            return await this._contentsProxy.save(path, model);
        };
        if (!chunked) {
            try {
                return await uploadInner(file);
            }
            catch (err) {
                _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__.ArrayExt.removeFirstWhere(this._uploads, uploadIndex => file.name === uploadIndex.path);
                throw err;
            }
        }
        let finalModel;
        let upload = { path, progress: 0 };
        this._uploadChanged.emit({
            name: "start",
            newValue: upload,
            oldValue: null,
        });
        for (let start = 0; !finalModel; start += CHUNK_SIZE) {
            const end = start + CHUNK_SIZE;
            const lastChunk = end >= file.size;
            const chunk = lastChunk ? -1 : end / CHUNK_SIZE;
            const newUpload = { path, progress: start / file.size };
            this._uploads.splice(this._uploads.indexOf(upload));
            this._uploads.push(newUpload);
            this._uploadChanged.emit({
                name: "update",
                newValue: newUpload,
                oldValue: upload,
            });
            upload = newUpload;
            let currentModel;
            try {
                currentModel = await uploadInner(file.slice(start, end), chunk);
            }
            catch (err) {
                _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__.ArrayExt.removeFirstWhere(this._uploads, uploadIndex => file.name === uploadIndex.path);
                this._uploadChanged.emit({
                    name: "failure",
                    newValue: upload,
                    oldValue: null,
                });
                throw err;
            }
            if (lastChunk) {
                finalModel = currentModel;
            }
        }
        this._uploads.splice(this._uploads.indexOf(upload));
        this._uploadChanged.emit({
            name: "finish",
            newValue: null,
            oldValue: upload,
        });
        return finalModel;
    }
    _uploadCheckDisposed() {
        if (this.isDisposed) {
            return Promise.reject("Filemanager disposed. File upload canceled");
        }
        return Promise.resolve();
    }
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * Create the upload input node for a file buttons widget.
     */
    function createUploadInput() {
        const input = document.createElement("input");
        input.type = "file";
        input.multiple = true;
        return input;
    }
    Private.createUploadInput = createUploadInput;
    /**
     * Translate upload tooltip.
     */
    function translateToolTip(translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        const trans = translator.load("jupyterlab");
        return trans.__("Upload Files");
    }
    Private.translateToolTip = translateToolTip;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   OpenDirectWidget: () => (/* binding */ OpenDirectWidget),
/* harmony export */   Patterns: () => (/* binding */ Patterns),
/* harmony export */   btoaNopad: () => (/* binding */ btoaNopad),
/* harmony export */   createOpenNode: () => (/* binding */ createOpenNode),
/* harmony export */   fileSizeString: () => (/* binding */ fileSizeString),
/* harmony export */   promptRename: () => (/* binding */ promptRename),
/* harmony export */   switchView: () => (/* binding */ switchView),
/* harmony export */   writeZipFile: () => (/* binding */ writeZipFile)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var file_saver__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! file-saver */ "webpack/sharing/consume/default/file-saver/file-saver");
/* harmony import */ var file_saver__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(file_saver__WEBPACK_IMPORTED_MODULE_2__);
/******************************************************************************
 *
 * Copyright (c) 2019, the jupyter-fs authors.
 *
 * This file is part of the jupyter-fs library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */



const Patterns = {
    tree: new RegExp(`^${_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption("treeUrl")}([^?]+)`),
    workspace: new RegExp(`^${_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption("workspacesUrl")}[^?/]+/tree/([^?]+)`),
};
/**
 * Version of btoa that omits any "=" padding chars at the end
 */
function btoaNopad(s) {
    return btoa(s).replace(/=+$/, "");
}
function createOpenNode() {
    const body = document.createElement("div");
    const existingLabel = document.createElement("label");
    existingLabel.textContent = "File Path:";
    const input = document.createElement("input");
    input.value = "";
    input.placeholder = "/path/to/file";
    body.appendChild(existingLabel);
    body.appendChild(input);
    return body;
}
function promptRename(text, edit, original) {
    const parent = text.parentElement;
    parent.replaceChild(edit, text);
    edit.focus();
    const index = edit.value.lastIndexOf('.');
    if (index === -1) {
        edit.setSelectionRange(0, edit.value.length);
    }
    else {
        edit.setSelectionRange(0, index);
    }
    return new Promise((resolve, reject) => {
        edit.onblur = () => {
            parent.replaceChild(text, edit);
            resolve(edit.value);
        };
        edit.onkeydown = (event) => {
            switch (event.keyCode) {
                case 13: // Enter
                    event.stopPropagation();
                    event.preventDefault();
                    edit.blur();
                    break;
                case 27: // Escape
                    event.stopPropagation();
                    event.preventDefault();
                    edit.value = original;
                    edit.blur();
                    break;
                case 38: // Up arrow
                    event.stopPropagation();
                    event.preventDefault();
                    if (edit.selectionStart !== edit.selectionEnd) {
                        edit.selectionStart = edit.selectionEnd = 0;
                    }
                    break;
                case 40: // Down arrow
                    event.stopPropagation();
                    event.preventDefault();
                    if (edit.selectionStart !== edit.selectionEnd) {
                        edit.selectionStart = edit.selectionEnd = edit.value.length;
                    }
                    break;
                default:
                    break;
            }
        };
    });
}
function fileSizeString(fileBytes) {
    if (fileBytes == null) {
        return "";
    }
    if (fileBytes < 1024) {
        return fileBytes + " B";
    }
    let i = -1;
    const byteUnits = [" KB", " MB", " GB", " TB"];
    do {
        fileBytes = fileBytes / 1024;
        i++;
    } while (fileBytes > 1024);
    return Math.max(fileBytes, 0.1).toFixed(1) + byteUnits[i];
}
function switchView(mode) {
    if (mode === "none") {
        return "";
    }
    else {
        return "none";
    }
}
function writeZipFile(zip, path) {
    zip.generateAsync({ type: "blob" }).then(content => {
        (0,file_saver__WEBPACK_IMPORTED_MODULE_2__.saveAs)(content, _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.basename(path));
    });
}
class OpenDirectWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    constructor() {
        super({ node: createOpenNode() });
    }
    getValue() {
        return this.inputNode.value;
    }
    get inputNode() {
        return this.node.getElementsByTagName("input")[0];
    }
}


/***/ }),

/***/ "./style/icons/drive.svg":
/*!*******************************!*\
  !*** ./style/icons/drive.svg ***!
  \*******************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\">\n  <path class=\"jp-icon3 jp-icon-selectable\" stroke=\"#616161\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M22 12H2M5.45 5.11L2 12v6a2 2 0 002 2h16a2 2 0 002-2v-6l-3.45-6.89A2 2 0 0016.76 4H7.24a2 2 0 00-1.79 1.11zM6 16h.01M10 16h.01\"/>\n</svg>\n";

/***/ }),

/***/ "./style/icons/file-tree.svg":
/*!***********************************!*\
  !*** ./style/icons/file-tree.svg ***!
  \***********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"20\" viewBox=\"0 0 16 16\">\n  <path class=\"jp-icon3\" fill=\"#616161\" d=\"M16 10V6H5v1H3V4h9V0H0v4h2v10h3v2h11v-4H5v1H3V8h2v2z\"/>\n</svg>\n";

/***/ }),

/***/ "./style/icons/jupyter-fs.svg":
/*!************************************!*\
  !*** ./style/icons/jupyter-fs.svg ***!
  \************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\" width=\"500\" viewBox=\"0 0 100 100\">\n  <rect class=\"jp-icon3\" stroke=\"#616161\" stroke-width=\"4\" width=\"91\" height=\"21\" fill=\"none\" rx=\"4\" x=\"4.5\" y=\"9.5\"/>\n  <circle class=\"jp-icon3\" fill=\"#616161\" cx=\"85\" cy=\"20\" r=\"3\"/>\n  <circle class=\"jp-icon3\" fill=\"#616161\" cx=\"73\" cy=\"20\" r=\"3\"/>\n\n  <rect class=\"jp-icon3\" stroke=\"#616161\" stroke-width=\"4\" width=\"91\" height=\"21\" fill=\"none\" rx=\"4\" x=\"4.5\" y=\"39.5\"/>\n  <circle class=\"jp-icon3\" fill=\"#616161\" cx=\"85\" cy=\"50\" r=\"3\"/>\n  <circle class=\"jp-icon3\" fill=\"#616161\" cx=\"73\" cy=\"50\" r=\"3\"/>\n\n  <rect class=\"jp-icon3\" stroke=\"#616161\" stroke-width=\"4\" width=\"91\" height=\"21\" fill=\"none\" rx=\"4\" x=\"4.5\" y=\"69.5\"/>\n  <circle class=\"jp-icon3\" fill=\"#616161\" cx=\"85\" cy=\"80\" r=\"3\"/>\n  <circle class=\"jp-icon3\" fill=\"#616161\" cx=\"73\" cy=\"80\" r=\"3\"/>\n</svg>\n";

/***/ }),

/***/ "./style/icons/visibility-off.svg":
/*!****************************************!*\
  !*** ./style/icons/visibility-off.svg ***!
  \****************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"24\" height=\"24\">\n  <path class=\"jp-icon3\" fill=\"#616161\" d=\"M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z\"/>\n</svg>";

/***/ }),

/***/ "./style/icons/visibility.svg":
/*!************************************!*\
  !*** ./style/icons/visibility.svg ***!
  \************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"24\" height=\"24\">\n  <path class=\"jp-icon3\" fill=\"#616161\" d=\"M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z\"/>\n</svg>";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.a5b99fcac43d38620a0c.js.map
"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[4680,6374],{

/***/ 34680:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IRunningSessionManagers": () => (/* binding */ IRunningSessionManagers),
/* harmony export */   "RunningSessionManagers": () => (/* binding */ RunningSessionManagers),
/* harmony export */   "RunningSessions": () => (/* binding */ RunningSessions)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(82545);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(41948);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(76351);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(22100);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(78612);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(30205);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(52850);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_6__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module running
 */







/**
 * The class name added to a running widget.
 */
const RUNNING_CLASS = 'jp-RunningSessions';
/**
 * The class name added to the running terminal sessions section.
 */
const SECTION_CLASS = 'jp-RunningSessions-section';
/**
 * The class name added to a section container.
 */
const CONTAINER_CLASS = 'jp-RunningSessions-sectionContainer';
/**
 * The class name added to the running kernel sessions section list.
 */
const LIST_CLASS = 'jp-RunningSessions-sectionList';
/**
 * The class name added to the running sessions items.
 */
const ITEM_CLASS = 'jp-RunningSessions-item';
/**
 * The class name added to a running session item label.
 */
const ITEM_LABEL_CLASS = 'jp-RunningSessions-itemLabel';
/**
 * The class name added to a running session item detail.
 */
const ITEM_DETAIL_CLASS = 'jp-RunningSessions-itemDetail';
/**
 * The class name added to a running session item shutdown button.
 */
const SHUTDOWN_BUTTON_CLASS = 'jp-RunningSessions-itemShutdown';
/**
 * The class name added to a running session item shutdown button.
 */
const SHUTDOWN_ALL_BUTTON_CLASS = 'jp-RunningSessions-shutdownAll';
/**
 * The running sessions token.
 */
const IRunningSessionManagers = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.Token('@jupyterlab/running:IRunningSessionManagers', 'A service to add running session managers.');
class RunningSessionManagers {
    constructor() {
        this._added = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        this._managers = [];
    }
    /**
     * Signal emitted when a new manager is added.
     */
    get added() {
        return this._added;
    }
    /**
     * Add a running item manager.
     *
     * @param manager - The running item manager.
     *
     */
    add(manager) {
        this._managers.push(manager);
        this._added.emit(manager);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__.DisposableDelegate(() => {
            const i = this._managers.indexOf(manager);
            if (i > -1) {
                this._managers.splice(i, 1);
            }
        });
    }
    /**
     * Return an iterator of launcher items.
     */
    items() {
        return this._managers;
    }
}
function Item(props) {
    var _a, _b;
    const { runningItem } = props;
    const classList = [ITEM_CLASS];
    const detail = (_a = runningItem.detail) === null || _a === void 0 ? void 0 : _a.call(runningItem);
    const icon = runningItem.icon();
    const title = runningItem.labelTitle ? runningItem.labelTitle() : '';
    const translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    const trans = translator.load('jupyterlab');
    // Handle shutdown requests.
    let stopPropagation = false;
    const shutdownItemIcon = props.shutdownItemIcon || _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.closeIcon;
    const shutdownLabel = props.shutdownLabel || trans.__('Shut Down');
    const shutdown = () => {
        var _a;
        stopPropagation = true;
        (_a = runningItem.shutdown) === null || _a === void 0 ? void 0 : _a.call(runningItem);
    };
    // Manage collapsed state. Use the shutdown flag in lieu of `stopPropagation`.
    const [collapsed, collapse] = react__WEBPACK_IMPORTED_MODULE_6__.useState(false);
    const collapsible = !!((_b = runningItem.children) === null || _b === void 0 ? void 0 : _b.length);
    const onClick = collapsible
        ? () => !stopPropagation && collapse(!collapsed)
        : undefined;
    if (runningItem.className) {
        classList.push(runningItem.className);
    }
    if (props.child) {
        classList.push('jp-mod-running-child');
    }
    return (react__WEBPACK_IMPORTED_MODULE_6__.createElement(react__WEBPACK_IMPORTED_MODULE_6__.Fragment, null,
        react__WEBPACK_IMPORTED_MODULE_6__.createElement("li", null,
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: classList.join(' '), onClick: onClick, "data-context": runningItem.context || '' },
                collapsible &&
                    (collapsed ? (react__WEBPACK_IMPORTED_MODULE_6__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.caretRightIcon.react, { tag: "span", stylesheet: "runningItem" })) : (react__WEBPACK_IMPORTED_MODULE_6__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.caretDownIcon.react, { tag: "span", stylesheet: "runningItem" }))),
                typeof icon === 'string' ? (icon ? (react__WEBPACK_IMPORTED_MODULE_6__.createElement("img", { src: icon })) : undefined) : (react__WEBPACK_IMPORTED_MODULE_6__.createElement(icon.react, { tag: "span", stylesheet: "runningItem" })),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: ITEM_LABEL_CLASS, title: title, onClick: runningItem.open && (() => runningItem.open()) }, runningItem.label()),
                detail && react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: ITEM_DETAIL_CLASS }, detail),
                runningItem.shutdown && (react__WEBPACK_IMPORTED_MODULE_6__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.ToolbarButtonComponent, { className: SHUTDOWN_BUTTON_CLASS, icon: shutdownItemIcon, onClick: shutdown, tooltip: shutdownLabel }))),
            collapsible && !collapsed && (react__WEBPACK_IMPORTED_MODULE_6__.createElement(List, { child: true, runningItems: runningItem.children, shutdownItemIcon: shutdownItemIcon, translator: translator })))));
}
function List(props) {
    return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("ul", { className: LIST_CLASS }, props.runningItems.map((item, i) => (react__WEBPACK_IMPORTED_MODULE_6__.createElement(Item, { child: props.child, key: i, runningItem: item, shutdownLabel: props.shutdownLabel, shutdownItemIcon: props.shutdownItemIcon, translator: props.translator })))));
}
class ListWidget extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.ReactWidget {
    constructor(_options) {
        super();
        this._options = _options;
        this._update = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        _options.manager.runningChanged.connect(this._emitUpdate, this);
    }
    dispose() {
        this._options.manager.runningChanged.disconnect(this._emitUpdate, this);
        super.dispose();
    }
    onBeforeShow(msg) {
        super.onBeforeShow(msg);
        this._update.emit();
    }
    render() {
        const options = this._options;
        let cached = true;
        return (react__WEBPACK_IMPORTED_MODULE_6__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.UseSignal, { signal: this._update }, () => {
            // Cache the running items for the intial load and request from
            // the service every subsequent load.
            if (cached) {
                cached = false;
            }
            else {
                options.runningItems = options.manager.running();
            }
            return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: CONTAINER_CLASS },
                react__WEBPACK_IMPORTED_MODULE_6__.createElement(List, { runningItems: options.runningItems, shutdownLabel: options.manager.shutdownLabel, shutdownAllLabel: options.shutdownAllLabel, shutdownItemIcon: options.manager.shutdownItemIcon, translator: options.translator })));
        }));
    }
    /**
     * Check if the widget or any of it's parents is hidden.
     *
     * Checking parents is necessary as lumino does not propagate visibility
     * changes from parents down to children (although it does notify parents
     * about changes to children visibility).
     */
    _isAnyHidden() {
        let isHidden = this.isHidden;
        if (isHidden) {
            return isHidden;
        }
        let parent = this.parent;
        while (parent != null) {
            if (parent.isHidden) {
                isHidden = true;
                break;
            }
            parent = parent.parent;
        }
        return isHidden;
    }
    _emitUpdate() {
        if (this._isAnyHidden()) {
            return;
        }
        this._update.emit();
    }
}
/**
 * The Section component contains the shared look and feel for an interactive
 * list of kernels and sessions.
 *
 * It is specialized for each based on its props.
 */
class Section extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.PanelWithToolbar {
    constructor(options) {
        super();
        this._manager = options.manager;
        const translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const shutdownAllLabel = options.manager.shutdownAllLabel || trans.__('Shut Down All');
        const shutdownTitle = `${shutdownAllLabel}?`;
        const shutdownAllConfirmationText = options.manager.shutdownAllConfirmationText ||
            `${shutdownAllLabel} ${options.manager.name}`;
        this.addClass(SECTION_CLASS);
        this.title.label = options.manager.name;
        function onShutdown() {
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: shutdownTitle,
                body: shutdownAllConfirmationText,
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.warnButton({ label: shutdownAllLabel })
                ]
            }).then(result => {
                if (result.button.accept) {
                    options.manager.shutdownAll();
                }
            });
        }
        let runningItems = options.manager.running();
        const enabled = runningItems.length > 0;
        this._button = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            label: shutdownAllLabel,
            className: `${SHUTDOWN_ALL_BUTTON_CLASS} jp-mod-styled ${!enabled && 'jp-mod-disabled'}`,
            enabled,
            onClick: onShutdown
        });
        this._manager.runningChanged.connect(this._updateButton, this);
        this.toolbar.addItem('shutdown-all', this._button);
        this.addWidget(new ListWidget({ runningItems, shutdownAllLabel, ...options }));
    }
    /**
     * Dispose the resources held by the widget
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._manager.runningChanged.disconnect(this._updateButton, this);
        super.dispose();
    }
    _updateButton() {
        var _a, _b;
        const button = this._button;
        button.enabled = this._manager.running().length > 0;
        if (button.enabled) {
            (_a = button.node.querySelector('button')) === null || _a === void 0 ? void 0 : _a.classList.remove('jp-mod-disabled');
        }
        else {
            (_b = button.node.querySelector('button')) === null || _b === void 0 ? void 0 : _b.classList.add('jp-mod-disabled');
        }
    }
}
/**
 * A class that exposes the running terminal and kernel sessions.
 */
class RunningSessions extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.SidePanel {
    /**
     * Construct a new running widget.
     */
    constructor(managers, translator) {
        super();
        this.managers = managers;
        this.translator = translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        const trans = this.translator.load('jupyterlab');
        this.addClass(RUNNING_CLASS);
        this.toolbar.addItem('refresh', new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            tooltip: trans.__('Refresh List'),
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.refreshIcon,
            onClick: () => managers.items().forEach(manager => manager.refreshRunning())
        }));
        managers.items().forEach(manager => this.addSection(managers, manager));
        managers.added.connect(this.addSection, this);
    }
    /**
     * Dispose the resources held by the widget
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.managers.added.disconnect(this.addSection, this);
        super.dispose();
    }
    /**
     * Add a section for a new manager.
     *
     * @param managers Managers
     * @param manager New manager
     */
    addSection(_, manager) {
        this.addWidget(new Section({ manager, translator: this.translator }));
    }
}


/***/ })

}]);
//# sourceMappingURL=4680.b4336b89e4739e733960.js.map?v=b4336b89e4739e733960
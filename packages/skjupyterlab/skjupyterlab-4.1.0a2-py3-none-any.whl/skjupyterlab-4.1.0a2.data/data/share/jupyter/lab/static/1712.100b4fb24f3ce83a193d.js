"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[1712],{

/***/ 1712:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "GroupItem": () => (/* reexport */ GroupItem),
  "IStatusBar": () => (/* reexport */ IStatusBar),
  "Popup": () => (/* reexport */ Popup),
  "ProgressBar": () => (/* reexport */ ProgressBar),
  "ProgressCircle": () => (/* reexport */ ProgressCircle),
  "StatusBar": () => (/* reexport */ StatusBar),
  "TextItem": () => (/* reexport */ TextItem),
  "showPopup": () => (/* reexport */ showPopup)
});

// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var index_js_ = __webpack_require__(52850);
var index_js_default = /*#__PURE__*/__webpack_require__.n(index_js_);
;// CONCATENATED MODULE: ../packages/statusbar/lib/components/group.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A tsx component for a set of items logically grouped together.
 */
function GroupItem(props) {
    const { spacing, children, className, ...rest } = props;
    const numChildren = index_js_.Children.count(children);
    return (index_js_.createElement("div", { className: `jp-StatusBar-GroupItem ${className || ''}`, ...rest }, index_js_.Children.map(children, (child, i) => {
        if (i === 0) {
            return index_js_.createElement("div", { style: { marginRight: `${spacing}px` } }, child);
        }
        else if (i === numChildren - 1) {
            return index_js_.createElement("div", { style: { marginLeft: `${spacing}px` } }, child);
        }
        else {
            return index_js_.createElement("div", { style: { margin: `0px ${spacing}px` } }, child);
        }
    })));
}

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(72234);
;// CONCATENATED MODULE: ../packages/statusbar/lib/components/hover.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * Create and show a popup component.
 *
 * @param options - options for the popup
 *
 * @returns the popup that was created.
 */
function showPopup(options) {
    const dialog = new Popup(options);
    if (!options.startHidden) {
        dialog.launch();
    }
    return dialog;
}
/**
 * A class for a Popup widget.
 */
class Popup extends index_es6_js_.Widget {
    /**
     * Construct a new Popup.
     */
    constructor(options) {
        super();
        this._body = options.body;
        this._body.addClass('jp-StatusBar-HoverItem');
        this._anchor = options.anchor;
        this._align = options.align;
        if (options.hasDynamicSize) {
            this._observer = new ResizeObserver(() => {
                this.update();
            });
        }
        const layout = (this.layout = new index_es6_js_.PanelLayout());
        layout.addWidget(options.body);
        this._body.node.addEventListener('resize', () => {
            this.update();
        });
    }
    /**
     * Attach the popup widget to the page.
     */
    launch() {
        this._setGeometry();
        index_es6_js_.Widget.attach(this, document.body);
        this.update();
        this._anchor.addClass('jp-mod-clicked');
        this._anchor.removeClass('jp-mod-highlight');
    }
    /**
     * Handle `'update'` messages for the widget.
     */
    onUpdateRequest(msg) {
        this._setGeometry();
        super.onUpdateRequest(msg);
    }
    /**
     * Handle `'after-attach'` messages for the widget.
     */
    onAfterAttach(msg) {
        var _a;
        document.addEventListener('click', this, false);
        this.node.addEventListener('keydown', this, false);
        window.addEventListener('resize', this, false);
        (_a = this._observer) === null || _a === void 0 ? void 0 : _a.observe(this._body.node);
    }
    /**
     * Handle `'before-detach'` messages for the widget.
     */
    onBeforeDetach(msg) {
        var _a;
        (_a = this._observer) === null || _a === void 0 ? void 0 : _a.disconnect();
        document.removeEventListener('click', this, false);
        this.node.removeEventListener('keydown', this, false);
        window.removeEventListener('resize', this, false);
    }
    /**
     * Handle `'resize'` messages for the widget.
     */
    onResize() {
        this.update();
    }
    /**
     * Dispose of the widget.
     */
    dispose() {
        var _a;
        (_a = this._observer) === null || _a === void 0 ? void 0 : _a.disconnect();
        super.dispose();
        this._anchor.removeClass('jp-mod-clicked');
        this._anchor.addClass('jp-mod-highlight');
    }
    /**
     * Handle DOM events for the widget.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'keydown':
                this._evtKeydown(event);
                break;
            case 'click':
                this._evtClick(event);
                break;
            case 'resize':
                this.onResize();
                break;
            default:
                break;
        }
    }
    _evtClick(event) {
        if (!!event.target &&
            !(this._body.node.contains(event.target) ||
                this._anchor.node.contains(event.target))) {
            this.dispose();
        }
    }
    _evtKeydown(event) {
        // Check for escape key
        switch (event.keyCode) {
            case 27: // Escape.
                event.stopPropagation();
                event.preventDefault();
                this.dispose();
                break;
            default:
                break;
        }
    }
    _setGeometry() {
        let aligned = 0;
        const anchorRect = this._anchor.node.getBoundingClientRect();
        const bodyRect = this._body.node.getBoundingClientRect();
        if (this._align === 'right') {
            aligned = -(bodyRect.width - anchorRect.width);
        }
        const style = window.getComputedStyle(this._body.node);
        lib_index_js_.HoverBox.setGeometry({
            anchor: anchorRect,
            host: document.body,
            maxHeight: 500,
            minHeight: 20,
            node: this._body.node,
            offset: {
                horizontal: aligned
            },
            privilege: 'forceAbove',
            style
        });
    }
}

;// CONCATENATED MODULE: ../packages/statusbar/lib/components/progressBar.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A functional tsx component for a progress bar.
 */
function ProgressBar(props) {
    const { width, percentage, ...rest } = props;
    return (index_js_.createElement("div", { className: 'jp-Statusbar-ProgressBar-progress-bar', role: "progressbar", "aria-valuemin": 0, "aria-valuemax": 100, "aria-valuenow": percentage },
        index_js_.createElement(Filler, { ...{ percentage, ...rest }, contentWidth: width })));
}
/**
 * A functional tsx component for a partially filled div.
 */
function Filler(props) {
    return (index_js_.createElement("div", { style: {
            width: `${props.percentage}%`
        } },
        index_js_.createElement("p", null, props.content)));
}

;// CONCATENATED MODULE: ../packages/statusbar/lib/components/text.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A functional tsx component for a text item.
 */
function TextItem(props) {
    const { title, source, className, ...rest } = props;
    return (index_js_.createElement("span", { className: `jp-StatusBar-TextItem ${className}`, title: title, ...rest }, source));
}

;// CONCATENATED MODULE: ../packages/statusbar/lib/components/progressCircle.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

function ProgressCircle(props) {
    const radius = 104;
    const d = (progress) => {
        const angle = Math.max(progress * 3.6, 0.1);
        const rad = (angle * Math.PI) / 180, x = Math.sin(rad) * radius, y = Math.cos(rad) * -radius, mid = angle < 180 ? 1 : 0, shape = `M 0 0 v -${radius} A ${radius} ${radius} 1 ` +
            mid +
            ' 0 ' +
            x.toFixed(4) +
            ' ' +
            y.toFixed(4) +
            ' z';
        return shape;
    };
    return (index_js_default().createElement("div", { className: 'jp-Statusbar-ProgressCircle', role: "progressbar", "aria-label": props.label || 'Unlabelled progress circle', "aria-valuemin": 0, "aria-valuemax": 100, "aria-valuenow": props.progress },
        index_js_default().createElement("svg", { viewBox: "0 0 250 250" },
            index_js_default().createElement("circle", { cx: "125", cy: "125", r: `${radius}`, stroke: "var(--jp-inverse-layout-color3)", strokeWidth: "20", fill: "none" }),
            index_js_default().createElement("path", { transform: "translate(125,125) scale(.9)", d: d(props.progress), fill: 'var(--jp-inverse-layout-color3)' }))));
}

;// CONCATENATED MODULE: ../packages/statusbar/lib/components/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @lumino/disposable@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/disposable/dist/index.es6.js)
var disposable_dist_index_es6_js_ = __webpack_require__(78612);
;// CONCATENATED MODULE: ../packages/statusbar/lib/statusbar.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Main status bar object which contains all items.
 */
class StatusBar extends index_es6_js_.Widget {
    constructor() {
        super();
        this._leftRankItems = [];
        this._rightRankItems = [];
        this._statusItems = {};
        this._disposables = new disposable_dist_index_es6_js_.DisposableSet();
        this.addClass('jp-StatusBar-Widget');
        const rootLayout = (this.layout = new index_es6_js_.PanelLayout());
        const leftPanel = (this._leftSide = new index_es6_js_.Panel());
        const middlePanel = (this._middlePanel = new index_es6_js_.Panel());
        const rightPanel = (this._rightSide = new index_es6_js_.Panel());
        leftPanel.addClass('jp-StatusBar-Left');
        middlePanel.addClass('jp-StatusBar-Middle');
        rightPanel.addClass('jp-StatusBar-Right');
        rootLayout.addWidget(leftPanel);
        rootLayout.addWidget(middlePanel);
        rootLayout.addWidget(rightPanel);
    }
    /**
     * Register a new status item.
     *
     * @param id - a unique id for the status item.
     *
     * @param statusItem - The item to add to the status bar.
     */
    registerStatusItem(id, statusItem) {
        if (id in this._statusItems) {
            throw new Error(`Status item ${id} already registered.`);
        }
        // Populate defaults for the optional properties of the status item.
        const fullStatusItem = {
            ...Private.statusItemDefaults,
            ...statusItem
        };
        const { align, item, rank } = fullStatusItem;
        // Connect the activeStateChanged signal to refreshing the status item,
        // if the signal was provided.
        const onActiveStateChanged = () => {
            this._refreshItem(id);
        };
        if (fullStatusItem.activeStateChanged) {
            fullStatusItem.activeStateChanged.connect(onActiveStateChanged);
        }
        const rankItem = { id, rank };
        fullStatusItem.item.addClass('jp-StatusBar-Item');
        this._statusItems[id] = fullStatusItem;
        if (align === 'left') {
            const insertIndex = this._findInsertIndex(this._leftRankItems, rankItem);
            if (insertIndex === -1) {
                this._leftSide.addWidget(item);
                this._leftRankItems.push(rankItem);
            }
            else {
                dist_index_es6_js_.ArrayExt.insert(this._leftRankItems, insertIndex, rankItem);
                this._leftSide.insertWidget(insertIndex, item);
            }
        }
        else if (align === 'right') {
            const insertIndex = this._findInsertIndex(this._rightRankItems, rankItem);
            if (insertIndex === -1) {
                this._rightSide.addWidget(item);
                this._rightRankItems.push(rankItem);
            }
            else {
                dist_index_es6_js_.ArrayExt.insert(this._rightRankItems, insertIndex, rankItem);
                this._rightSide.insertWidget(insertIndex, item);
            }
        }
        else {
            this._middlePanel.addWidget(item);
        }
        this._refreshItem(id); // Initially refresh the status item.
        const disposable = new disposable_dist_index_es6_js_.DisposableDelegate(() => {
            delete this._statusItems[id];
            if (fullStatusItem.activeStateChanged) {
                fullStatusItem.activeStateChanged.disconnect(onActiveStateChanged);
            }
            item.parent = null;
            item.dispose();
        });
        this._disposables.add(disposable);
        return disposable;
    }
    /**
     * Dispose of the status bar.
     */
    dispose() {
        this._leftRankItems.length = 0;
        this._rightRankItems.length = 0;
        this._disposables.dispose();
        super.dispose();
    }
    /**
     * Handle an 'update-request' message to the status bar.
     */
    onUpdateRequest(msg) {
        this._refreshAll();
        super.onUpdateRequest(msg);
    }
    _findInsertIndex(side, newItem) {
        return dist_index_es6_js_.ArrayExt.findFirstIndex(side, item => item.rank > newItem.rank);
    }
    _refreshItem(id) {
        const statusItem = this._statusItems[id];
        if (statusItem.isActive()) {
            statusItem.item.show();
            statusItem.item.update();
        }
        else {
            statusItem.item.hide();
        }
    }
    _refreshAll() {
        Object.keys(this._statusItems).forEach(id => {
            this._refreshItem(id);
        });
    }
}
/**
 * A namespace for private functionality.
 */
var Private;
(function (Private) {
    /**
     * Default options for a status item, less the item itself.
     */
    Private.statusItemDefaults = {
        align: 'left',
        rank: 0,
        isActive: () => true,
        activeStateChanged: undefined
    };
})(Private || (Private = {}));

// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/statusbar/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// tslint:disable-next-line:variable-name
const IStatusBar = new dist_index_js_.Token('@jupyterlab/statusbar:IStatusBar', 'A service for the status bar on the application. Use this if you want to add new status bar items.');

;// CONCATENATED MODULE: ../packages/statusbar/lib/index.js
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module statusbar
 */





/***/ })

}]);
//# sourceMappingURL=1712.100b4fb24f3ce83a193d.js.map?v=100b4fb24f3ce83a193d
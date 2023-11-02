"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[8702,2411],{

/***/ 12411:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "ILauncher": () => (/* reexport */ ILauncher),
  "Launcher": () => (/* reexport */ Launcher),
  "LauncherModel": () => (/* reexport */ LauncherModel)
});

// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/launcher/lib/tokens.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

/**
 * The launcher token.
 */
const ILauncher = new index_js_.Token('@jupyterlab/launcher:ILauncher', `A service for the application activity launcher.
  Use this to add your extension activities to the launcher panel.`);

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var lib_index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @lumino/disposable@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/disposable/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(78612);
// EXTERNAL MODULE: consume shared module (default) @lumino/properties@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/properties/dist/index.es6.js)
var properties_dist_index_es6_js_ = __webpack_require__(64260);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var widgets_dist_index_es6_js_ = __webpack_require__(72234);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
;// CONCATENATED MODULE: ../packages/launcher/lib/widget.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * The class name added to Launcher instances.
 */
const LAUNCHER_CLASS = 'jp-Launcher';
/**
 * LauncherModel keeps track of the path to working directory and has a list of
 * LauncherItems, which the Launcher will render.
 */
class LauncherModel extends ui_components_lib_index_js_.VDomModel {
    constructor() {
        super(...arguments);
        this.itemsList = [];
    }
    /**
     * Add a command item to the launcher, and trigger re-render event for parent
     * widget.
     *
     * @param options - The specification options for a launcher item.
     *
     * @returns A disposable that will remove the item from Launcher, and trigger
     * re-render event for parent widget.
     *
     */
    add(options) {
        // Create a copy of the options to circumvent mutations to the original.
        const item = Private.createItem(options);
        this.itemsList.push(item);
        this.stateChanged.emit(void 0);
        return new dist_index_es6_js_.DisposableDelegate(() => {
            index_es6_js_.ArrayExt.removeFirstOf(this.itemsList, item);
            this.stateChanged.emit(void 0);
        });
    }
    /**
     * Return an iterator of launcher items.
     */
    items() {
        return this.itemsList[Symbol.iterator]();
    }
}
/**
 * A virtual-DOM-based widget for the Launcher.
 */
class Launcher extends ui_components_lib_index_js_.VDomRenderer {
    /**
     * Construct a new launcher widget.
     */
    constructor(options) {
        super(options.model);
        this._pending = false;
        this._cwd = '';
        this._cwd = options.cwd;
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._callback = options.callback;
        this._commands = options.commands;
        this.addClass(LAUNCHER_CLASS);
    }
    /**
     * The cwd of the launcher.
     */
    get cwd() {
        return this._cwd;
    }
    set cwd(value) {
        this._cwd = value;
        this.update();
    }
    /**
     * Whether there is a pending item being launched.
     */
    get pending() {
        return this._pending;
    }
    set pending(value) {
        this._pending = value;
    }
    /**
     * Render the launcher to virtual DOM nodes.
     */
    render() {
        // Bail if there is no model.
        if (!this.model) {
            return null;
        }
        const knownCategories = [
            this._trans.__('Notebook'),
            this._trans.__('Console'),
            this._trans.__('Other')
        ];
        const kernelCategories = [
            this._trans.__('Notebook'),
            this._trans.__('Console')
        ];
        // First group-by categories
        const categories = Object.create(null);
        for (const item of this.model.items()) {
            const cat = item.category || this._trans.__('Other');
            if (!(cat in categories)) {
                categories[cat] = [];
            }
            categories[cat].push(item);
        }
        // Within each category sort by rank
        for (const cat in categories) {
            categories[cat] = categories[cat].sort((a, b) => {
                return Private.sortCmp(a, b, this._cwd, this._commands);
            });
        }
        // Variable to help create sections
        const sections = [];
        let section;
        // Assemble the final ordered list of categories, beginning with
        // KNOWN_CATEGORIES.
        const orderedCategories = [];
        for (const cat of knownCategories) {
            orderedCategories.push(cat);
        }
        for (const cat in categories) {
            if (knownCategories.indexOf(cat) === -1) {
                orderedCategories.push(cat);
            }
        }
        // Now create the sections for each category
        orderedCategories.forEach(cat => {
            if (!categories[cat]) {
                return;
            }
            const item = categories[cat][0];
            const args = { ...item.args, cwd: this.cwd };
            const kernel = kernelCategories.indexOf(cat) > -1;
            const iconClass = this._commands.iconClass(item.command, args);
            const icon = this._commands.icon(item.command, args);
            if (cat in categories) {
                section = (react_index_js_.createElement("div", { className: "jp-Launcher-section", key: cat },
                    react_index_js_.createElement("div", { className: "jp-Launcher-sectionHeader" },
                        react_index_js_.createElement(ui_components_lib_index_js_.LabIcon.resolveReact, { icon: icon, iconClass: (0,ui_components_lib_index_js_.classes)(iconClass, 'jp-Icon-cover'), stylesheet: "launcherSection" }),
                        react_index_js_.createElement("h2", { className: "jp-Launcher-sectionTitle" }, cat)),
                    react_index_js_.createElement("div", { className: "jp-Launcher-cardContainer" }, Array.from((0,index_es6_js_.map)(categories[cat], (item) => {
                        return Card(kernel, item, this, this._commands, this._trans, this._callback);
                    })))));
                sections.push(section);
            }
        });
        // Wrap the sections in body and content divs.
        return (react_index_js_.createElement("div", { className: "jp-Launcher-body" },
            react_index_js_.createElement("div", { className: "jp-Launcher-content" },
                react_index_js_.createElement("div", { className: "jp-Launcher-cwd" },
                    react_index_js_.createElement("h3", null, this.cwd)),
                sections)));
    }
}
/**
 * A pure tsx component for a launcher card.
 *
 * @param kernel - whether the item takes uses a kernel.
 *
 * @param item - the launcher item to render.
 *
 * @param launcher - the Launcher instance to which this is added.
 *
 * @param commands - the command registry holding the command of item.
 *
 * @param trans - the translation bundle.
 *
 * @returns a vdom `VirtualElement` for the launcher card.
 */
function Card(kernel, item, launcher, commands, trans, launcherCallback) {
    // Get some properties of the command
    const command = item.command;
    const args = { ...item.args, cwd: launcher.cwd };
    const caption = commands.caption(command, args);
    const label = commands.label(command, args);
    const title = kernel ? label : caption || label;
    // Build the onclick handler.
    const onclick = () => {
        // If an item has already been launched,
        // don't try to launch another.
        if (launcher.pending === true) {
            return;
        }
        launcher.pending = true;
        void commands
            .execute(command, {
            ...item.args,
            cwd: launcher.cwd
        })
            .then(value => {
            launcher.pending = false;
            if (value instanceof widgets_dist_index_es6_js_.Widget) {
                launcherCallback(value);
            }
        })
            .catch(err => {
            console.error(err);
            launcher.pending = false;
            void (0,lib_index_js_.showErrorMessage)(trans._p('Error', 'Launcher Error'), err);
        });
    };
    // With tabindex working, you can now pick a kernel by tabbing around and
    // pressing Enter.
    const onkeypress = (event) => {
        if (event.key === 'Enter') {
            onclick();
        }
    };
    const iconClass = commands.iconClass(command, args);
    const icon = commands.icon(command, args);
    // Return the VDOM element.
    return (react_index_js_.createElement("div", { className: "jp-LauncherCard", title: title, onClick: onclick, onKeyPress: onkeypress, tabIndex: 0, "data-category": item.category || trans.__('Other'), key: Private.keyProperty.get(item) },
        react_index_js_.createElement("div", { className: "jp-LauncherCard-icon" }, kernel ? (item.kernelIconUrl ? (react_index_js_.createElement("img", { src: item.kernelIconUrl, className: "jp-Launcher-kernelIcon" })) : (react_index_js_.createElement("div", { className: "jp-LauncherCard-noKernelIcon" }, label[0].toUpperCase()))) : (react_index_js_.createElement(ui_components_lib_index_js_.LabIcon.resolveReact, { icon: icon, iconClass: (0,ui_components_lib_index_js_.classes)(iconClass, 'jp-Icon-cover'), stylesheet: "launcherCard" }))),
        react_index_js_.createElement("div", { className: "jp-LauncherCard-label", title: title },
            react_index_js_.createElement("p", null, label))));
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * An incrementing counter for keys.
     */
    let id = 0;
    /**
     * An attached property for an item's key.
     */
    Private.keyProperty = new properties_dist_index_es6_js_.AttachedProperty({
        name: 'key',
        create: () => id++
    });
    /**
     * Create a fully specified item given item options.
     */
    function createItem(options) {
        return {
            ...options,
            category: options.category || '',
            rank: options.rank !== undefined ? options.rank : Infinity
        };
    }
    Private.createItem = createItem;
    /**
     * A sort comparison function for a launcher item.
     */
    function sortCmp(a, b, cwd, commands) {
        // First, compare by rank.
        const r1 = a.rank;
        const r2 = b.rank;
        if (r1 !== r2 && r1 !== undefined && r2 !== undefined) {
            return r1 < r2 ? -1 : 1; // Infinity safe
        }
        // Finally, compare by display name.
        const aLabel = commands.label(a.command, { ...a.args, cwd });
        const bLabel = commands.label(b.command, { ...b.args, cwd });
        return aLabel.localeCompare(bLabel);
    }
    Private.sortCmp = sortCmp;
})(Private || (Private = {}));

;// CONCATENATED MODULE: ../packages/launcher/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module launcher
 */




/***/ })

}]);
//# sourceMappingURL=8702.dc3589889fd88408058c.js.map?v=dc3589889fd88408058c
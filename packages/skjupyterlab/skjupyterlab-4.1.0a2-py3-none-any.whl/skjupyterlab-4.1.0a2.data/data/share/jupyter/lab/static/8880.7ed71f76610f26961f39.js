"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[8880,5790],{

/***/ 18880:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "EditMenu": () => (/* reexport */ EditMenu),
  "FileMenu": () => (/* reexport */ FileMenu),
  "HelpMenu": () => (/* reexport */ HelpMenu),
  "IMainMenu": () => (/* reexport */ IMainMenu),
  "KernelMenu": () => (/* reexport */ KernelMenu),
  "MainMenu": () => (/* reexport */ MainMenu),
  "RunMenu": () => (/* reexport */ RunMenu),
  "SettingsMenu": () => (/* reexport */ SettingsMenu),
  "TabsMenu": () => (/* reexport */ TabsMenu),
  "ViewMenu": () => (/* reexport */ ViewMenu)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(72234);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var lib_index_js_ = __webpack_require__(82545);
;// CONCATENATED MODULE: ../packages/mainmenu/lib/edit.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * An extensible Edit menu for the application.
 */
class EditMenu extends index_js_.RankedMenu {
    /**
     * Construct the edit menu.
     */
    constructor(options) {
        super(options);
        this.undoers = {
            redo: new lib_index_js_.SemanticCommand(),
            undo: new lib_index_js_.SemanticCommand()
        };
        this.clearers = {
            clearAll: new lib_index_js_.SemanticCommand(),
            clearCurrent: new lib_index_js_.SemanticCommand()
        };
        this.goToLiners = new lib_index_js_.SemanticCommand();
    }
}

;// CONCATENATED MODULE: ../packages/mainmenu/lib/file.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * An extensible FileMenu for the application.
 */
class FileMenu extends index_js_.RankedMenu {
    constructor(options) {
        super(options);
        this.quitEntry = false;
        this.closeAndCleaners = new lib_index_js_.SemanticCommand();
        this.consoleCreators = new lib_index_js_.SemanticCommand();
    }
    /**
     * The New submenu.
     */
    get newMenu() {
        var _a, _b;
        if (!this._newMenu) {
            this._newMenu =
                (_b = (_a = (0,index_es6_js_.find)(this.items, menu => { var _a; return ((_a = menu.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-mainmenu-file-new'; })) === null || _a === void 0 ? void 0 : _a.submenu) !== null && _b !== void 0 ? _b : new index_js_.RankedMenu({
                    commands: this.commands
                });
        }
        return this._newMenu;
    }
    /**
     * Dispose of the resources held by the file menu.
     */
    dispose() {
        var _a;
        (_a = this._newMenu) === null || _a === void 0 ? void 0 : _a.dispose();
        super.dispose();
    }
}

;// CONCATENATED MODULE: ../packages/mainmenu/lib/help.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * An extensible Help menu for the application.
 */
class HelpMenu extends index_js_.RankedMenu {
    /**
     * Construct the help menu.
     */
    constructor(options) {
        super(options);
        this.getKernel = new lib_index_js_.SemanticCommand();
    }
}

;// CONCATENATED MODULE: ../packages/mainmenu/lib/kernel.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * An extensible Kernel menu for the application.
 */
class KernelMenu extends index_js_.RankedMenu {
    /**
     * Construct the kernel menu.
     */
    constructor(options) {
        super(options);
        this.kernelUsers = {
            changeKernel: new lib_index_js_.SemanticCommand(),
            clearWidget: new lib_index_js_.SemanticCommand(),
            interruptKernel: new lib_index_js_.SemanticCommand(),
            reconnectToKernel: new lib_index_js_.SemanticCommand(),
            restartKernel: new lib_index_js_.SemanticCommand(),
            shutdownKernel: new lib_index_js_.SemanticCommand()
        };
    }
}

;// CONCATENATED MODULE: ../packages/mainmenu/lib/run.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * An extensible Run menu for the application.
 */
class RunMenu extends index_js_.RankedMenu {
    /**
     * Construct the run menu.
     */
    constructor(options) {
        super(options);
        this.codeRunners = {
            restart: new lib_index_js_.SemanticCommand(),
            run: new lib_index_js_.SemanticCommand(),
            runAll: new lib_index_js_.SemanticCommand()
        };
    }
}

;// CONCATENATED MODULE: ../packages/mainmenu/lib/settings.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * An extensible Settings menu for the application.
 */
class SettingsMenu extends index_js_.RankedMenu {
    /**
     * Construct the settings menu.
     */
    constructor(options) {
        super(options);
    }
}

;// CONCATENATED MODULE: ../packages/mainmenu/lib/tabs.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * An extensible Tabs menu for the application.
 */
class TabsMenu extends index_js_.RankedMenu {
    /**
     * Construct the tabs menu.
     */
    constructor(options) {
        super(options);
    }
}

;// CONCATENATED MODULE: ../packages/mainmenu/lib/view.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * An extensible View menu for the application.
 */
class ViewMenu extends index_js_.RankedMenu {
    /**
     * Construct the view menu.
     */
    constructor(options) {
        super(options);
        this.editorViewers = {
            toggleLineNumbers: new lib_index_js_.SemanticCommand(),
            toggleMatchBrackets: new lib_index_js_.SemanticCommand(),
            toggleWordWrap: new lib_index_js_.SemanticCommand()
        };
    }
}

;// CONCATENATED MODULE: ../packages/mainmenu/lib/mainmenu.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.











/**
 * The main menu class.  It is intended to be used as a singleton.
 */
class MainMenu extends dist_index_es6_js_.MenuBar {
    /**
     * Construct the main menu bar.
     */
    constructor(commands) {
        let options = { forceItemsPosition: { forceX: false, forceY: true } };
        super(options);
        this._items = [];
        this._commands = commands;
    }
    /**
     * The application "Edit" menu.
     */
    get editMenu() {
        if (!this._editMenu) {
            this._editMenu = new EditMenu({
                commands: this._commands,
                rank: 2,
                renderer: index_js_.MenuSvg.defaultRenderer
            });
        }
        return this._editMenu;
    }
    /**
     * The application "File" menu.
     */
    get fileMenu() {
        if (!this._fileMenu) {
            this._fileMenu = new FileMenu({
                commands: this._commands,
                rank: 1,
                renderer: index_js_.MenuSvg.defaultRenderer
            });
        }
        return this._fileMenu;
    }
    /**
     * The application "Help" menu.
     */
    get helpMenu() {
        if (!this._helpMenu) {
            this._helpMenu = new HelpMenu({
                commands: this._commands,
                rank: 1000,
                renderer: index_js_.MenuSvg.defaultRenderer
            });
        }
        return this._helpMenu;
    }
    /**
     * The application "Kernel" menu.
     */
    get kernelMenu() {
        if (!this._kernelMenu) {
            this._kernelMenu = new KernelMenu({
                commands: this._commands,
                rank: 5,
                renderer: index_js_.MenuSvg.defaultRenderer
            });
        }
        return this._kernelMenu;
    }
    /**
     * The application "Run" menu.
     */
    get runMenu() {
        if (!this._runMenu) {
            this._runMenu = new RunMenu({
                commands: this._commands,
                rank: 4,
                renderer: index_js_.MenuSvg.defaultRenderer
            });
        }
        return this._runMenu;
    }
    /**
     * The application "Settings" menu.
     */
    get settingsMenu() {
        if (!this._settingsMenu) {
            this._settingsMenu = new SettingsMenu({
                commands: this._commands,
                rank: 999,
                renderer: index_js_.MenuSvg.defaultRenderer
            });
        }
        return this._settingsMenu;
    }
    /**
     * The application "View" menu.
     */
    get viewMenu() {
        if (!this._viewMenu) {
            this._viewMenu = new ViewMenu({
                commands: this._commands,
                rank: 3,
                renderer: index_js_.MenuSvg.defaultRenderer
            });
        }
        return this._viewMenu;
    }
    /**
     * The application "Tabs" menu.
     */
    get tabsMenu() {
        if (!this._tabsMenu) {
            this._tabsMenu = new TabsMenu({
                commands: this._commands,
                rank: 500,
                renderer: index_js_.MenuSvg.defaultRenderer
            });
        }
        return this._tabsMenu;
    }
    /**
     * Add a new menu to the main menu bar.
     */
    addMenu(menu, update = true, options = {}) {
        if (index_es6_js_.ArrayExt.firstIndexOf(this.menus, menu) > -1) {
            return;
        }
        // override default renderer with svg-supporting renderer
        index_js_.MenuSvg.overrideDefaultRenderer(menu);
        const rank = 'rank' in options
            ? options.rank
            : 'rank' in menu
                ? menu.rank
                : index_js_.IRankedMenu.DEFAULT_RANK;
        const rankItem = { menu, rank };
        const index = index_es6_js_.ArrayExt.upperBound(this._items, rankItem, Private.itemCmp);
        // Upon disposal, remove the menu and its rank reference.
        menu.disposed.connect(this._onMenuDisposed, this);
        index_es6_js_.ArrayExt.insert(this._items, index, rankItem);
        /**
         * Create a new menu.
         */
        this.insertMenu(index, menu);
        // Link the menu to the API - backward compatibility when switching to menu description in settings
        switch (menu.id) {
            case 'jp-mainmenu-file':
                if (!this._fileMenu && menu instanceof FileMenu) {
                    this._fileMenu = menu;
                }
                break;
            case 'jp-mainmenu-edit':
                if (!this._editMenu && menu instanceof EditMenu) {
                    this._editMenu = menu;
                }
                break;
            case 'jp-mainmenu-view':
                if (!this._viewMenu && menu instanceof ViewMenu) {
                    this._viewMenu = menu;
                }
                break;
            case 'jp-mainmenu-run':
                if (!this._runMenu && menu instanceof RunMenu) {
                    this._runMenu = menu;
                }
                break;
            case 'jp-mainmenu-kernel':
                if (!this._kernelMenu && menu instanceof KernelMenu) {
                    this._kernelMenu = menu;
                }
                break;
            case 'jp-mainmenu-tabs':
                if (!this._tabsMenu && menu instanceof TabsMenu) {
                    this._tabsMenu = menu;
                }
                break;
            case 'jp-mainmenu-settings':
                if (!this._settingsMenu && menu instanceof SettingsMenu) {
                    this._settingsMenu = menu;
                }
                break;
            case 'jp-mainmenu-help':
                if (!this._helpMenu && menu instanceof HelpMenu) {
                    this._helpMenu = menu;
                }
                break;
        }
    }
    /**
     * Dispose of the resources held by the menu bar.
     */
    dispose() {
        var _a, _b, _c, _d, _e, _f, _g, _h;
        (_a = this._editMenu) === null || _a === void 0 ? void 0 : _a.dispose();
        (_b = this._fileMenu) === null || _b === void 0 ? void 0 : _b.dispose();
        (_c = this._helpMenu) === null || _c === void 0 ? void 0 : _c.dispose();
        (_d = this._kernelMenu) === null || _d === void 0 ? void 0 : _d.dispose();
        (_e = this._runMenu) === null || _e === void 0 ? void 0 : _e.dispose();
        (_f = this._settingsMenu) === null || _f === void 0 ? void 0 : _f.dispose();
        (_g = this._viewMenu) === null || _g === void 0 ? void 0 : _g.dispose();
        (_h = this._tabsMenu) === null || _h === void 0 ? void 0 : _h.dispose();
        super.dispose();
    }
    /**
     * Generate the menu.
     *
     * @param commands The command registry
     * @param options The main menu options.
     * @param trans - The application language translator.
     */
    static generateMenu(commands, options, trans) {
        let menu;
        const { id, label, rank } = options;
        switch (id) {
            case 'jp-mainmenu-file':
                menu = new FileMenu({
                    commands,
                    rank,
                    renderer: index_js_.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-edit':
                menu = new EditMenu({
                    commands,
                    rank,
                    renderer: index_js_.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-view':
                menu = new ViewMenu({
                    commands,
                    rank,
                    renderer: index_js_.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-run':
                menu = new RunMenu({
                    commands,
                    rank,
                    renderer: index_js_.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-kernel':
                menu = new KernelMenu({
                    commands,
                    rank,
                    renderer: index_js_.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-tabs':
                menu = new TabsMenu({
                    commands,
                    rank,
                    renderer: index_js_.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-settings':
                menu = new SettingsMenu({
                    commands,
                    rank,
                    renderer: index_js_.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-help':
                menu = new HelpMenu({
                    commands,
                    rank,
                    renderer: index_js_.MenuSvg.defaultRenderer
                });
                break;
            default:
                menu = new index_js_.RankedMenu({
                    commands,
                    rank,
                    renderer: index_js_.MenuSvg.defaultRenderer
                });
        }
        if (label) {
            menu.title.label = trans._p('menu', label);
        }
        return menu;
    }
    /**
     * Handle the disposal of a menu.
     */
    _onMenuDisposed(menu) {
        this.removeMenu(menu);
        const index = index_es6_js_.ArrayExt.findFirstIndex(this._items, item => item.menu === menu);
        if (index !== -1) {
            index_es6_js_.ArrayExt.removeAt(this._items, index);
        }
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * A comparator function for menu rank items.
     */
    function itemCmp(first, second) {
        return first.rank - second.rank;
    }
    Private.itemCmp = itemCmp;
})(Private || (Private = {}));

// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
;// CONCATENATED MODULE: ../packages/mainmenu/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The main menu token.
 */
const IMainMenu = new dist_index_js_.Token('@jupyterlab/mainmenu:IMainMenu', `A service for the main menu bar for the application.
  Use this if you want to add your own menu items or provide implementations for standardized menu items for specific activities.`);

;// CONCATENATED MODULE: ../packages/mainmenu/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module mainmenu
 */












/***/ })

}]);
//# sourceMappingURL=8880.7ed71f76610f26961f39.js.map?v=7ed71f76610f26961f39
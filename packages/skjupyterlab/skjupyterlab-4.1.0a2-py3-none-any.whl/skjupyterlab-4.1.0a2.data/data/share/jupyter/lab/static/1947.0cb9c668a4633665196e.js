"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[1947],{

/***/ 98067:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "BreadCrumbs": () => (/* reexport */ BreadCrumbs),
  "CHUNK_SIZE": () => (/* reexport */ CHUNK_SIZE),
  "DirListing": () => (/* reexport */ DirListing),
  "FileBrowser": () => (/* reexport */ FileBrowser),
  "FileBrowserModel": () => (/* reexport */ FileBrowserModel),
  "FileDialog": () => (/* reexport */ FileDialog),
  "FileUploadStatus": () => (/* reexport */ FileUploadStatus),
  "FilterFileBrowserModel": () => (/* reexport */ FilterFileBrowserModel),
  "IDefaultFileBrowser": () => (/* reexport */ IDefaultFileBrowser),
  "IFileBrowserCommands": () => (/* reexport */ IFileBrowserCommands),
  "IFileBrowserFactory": () => (/* reexport */ IFileBrowserFactory),
  "LARGE_FILE_SIZE": () => (/* reexport */ LARGE_FILE_SIZE),
  "TogglableHiddenFileBrowserModel": () => (/* reexport */ TogglableHiddenFileBrowserModel),
  "Uploader": () => (/* reexport */ Uploader)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/apputils@~4.2.0-alpha.2 (singleton) (fallback: ../packages/apputils/lib/index.js)
var index_js_ = __webpack_require__(82545);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/services@~7.1.0-alpha.2 (singleton) (fallback: ../packages/services/lib/index.js)
var lib_index_js_ = __webpack_require__(43411);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var translation_lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(72234);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/coreutils@~6.1.0-alpha.2 (singleton) (fallback: ../packages/coreutils/lib/index.js)
var coreutils_lib_index_js_ = __webpack_require__(78254);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/docmanager@~4.1.0-alpha.2 (singleton) (fallback: ../packages/docmanager/lib/index.js)
var docmanager_lib_index_js_ = __webpack_require__(7280);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @lumino/domutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/domutils/dist/index.es6.js)
var domutils_dist_index_es6_js_ = __webpack_require__(92654);
;// CONCATENATED MODULE: ../packages/filebrowser/lib/crumbs.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * The class name added to the breadcrumb node.
 */
const BREADCRUMB_CLASS = 'jp-BreadCrumbs';
/**
 * The class name for the breadcrumbs home node
 */
const BREADCRUMB_ROOT_CLASS = 'jp-BreadCrumbs-home';
/**
 * The class name for the breadcrumbs preferred node
 */
const BREADCRUMB_PREFERRED_CLASS = 'jp-BreadCrumbs-preferred';
/**
 * The class name added to the breadcrumb node.
 */
const BREADCRUMB_ITEM_CLASS = 'jp-BreadCrumbs-item';
/**
 * Bread crumb paths.
 */
const BREAD_CRUMB_PATHS = ['/', '../../', '../', ''];
/**
 * The mime type for a contents drag object.
 */
const CONTENTS_MIME = 'application/x-jupyter-icontents';
/**
 * The class name added to drop targets.
 */
const DROP_TARGET_CLASS = 'jp-mod-dropTarget';
/**
 * A class which hosts folder breadcrumbs.
 */
class BreadCrumbs extends index_es6_js_.Widget {
    /**
     * Construct a new file browser crumb widget.
     *
     * @param model - The file browser view model.
     */
    constructor(options) {
        super();
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._model = options.model;
        this.addClass(BREADCRUMB_CLASS);
        this._crumbs = Private.createCrumbs();
        this._crumbSeps = Private.createCrumbSeparators();
        const hasPreferred = coreutils_lib_index_js_.PageConfig.getOption('preferredPath');
        this._hasPreferred = hasPreferred && hasPreferred !== '/' ? true : false;
        if (this._hasPreferred) {
            this.node.appendChild(this._crumbs[Private.Crumb.Preferred]);
        }
        this.node.appendChild(this._crumbs[Private.Crumb.Home]);
        this._model.refreshed.connect(this.update, this);
    }
    /**
     * Handle the DOM events for the bread crumbs.
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
            case 'click':
                this._evtClick(event);
                break;
            case 'lm-dragenter':
                this._evtDragEnter(event);
                break;
            case 'lm-dragleave':
                this._evtDragLeave(event);
                break;
            case 'lm-dragover':
                this._evtDragOver(event);
                break;
            case 'lm-drop':
                this._evtDrop(event);
                break;
            default:
                return;
        }
    }
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        this.update();
        const node = this.node;
        node.addEventListener('click', this);
        node.addEventListener('lm-dragenter', this);
        node.addEventListener('lm-dragleave', this);
        node.addEventListener('lm-dragover', this);
        node.addEventListener('lm-drop', this);
    }
    /**
     * A message handler invoked on a `'before-detach'` message.
     */
    onBeforeDetach(msg) {
        super.onBeforeDetach(msg);
        const node = this.node;
        node.removeEventListener('click', this);
        node.removeEventListener('lm-dragenter', this);
        node.removeEventListener('lm-dragleave', this);
        node.removeEventListener('lm-dragover', this);
        node.removeEventListener('lm-drop', this);
    }
    /**
     * A handler invoked on an `'update-request'` message.
     */
    onUpdateRequest(msg) {
        // Update the breadcrumb list.
        const contents = this._model.manager.services.contents;
        const localPath = contents.localPath(this._model.path);
        Private.updateCrumbs(this._crumbs, this._crumbSeps, localPath, this._hasPreferred);
    }
    /**
     * Handle the `'click'` event for the widget.
     */
    _evtClick(event) {
        // Do nothing if it's not a left mouse press.
        if (event.button !== 0) {
            return;
        }
        // Find a valid click target.
        let node = event.target;
        while (node && node !== this.node) {
            if (node.classList.contains(BREADCRUMB_PREFERRED_CLASS)) {
                this._model
                    .cd(coreutils_lib_index_js_.PageConfig.getOption('preferredPath'))
                    .catch(error => (0,index_js_.showErrorMessage)(this._trans.__('Open Error'), error));
                // Stop the event propagation.
                event.preventDefault();
                event.stopPropagation();
                return;
            }
            if (node.classList.contains(BREADCRUMB_ITEM_CLASS) ||
                node.classList.contains(BREADCRUMB_ROOT_CLASS)) {
                const index = dist_index_es6_js_.ArrayExt.findFirstIndex(this._crumbs, value => value === node);
                this._model
                    .cd(BREAD_CRUMB_PATHS[index])
                    .catch(error => (0,index_js_.showErrorMessage)(this._trans.__('Open Error'), error));
                // Stop the event propagation.
                event.preventDefault();
                event.stopPropagation();
                return;
            }
            node = node.parentElement;
        }
    }
    /**
     * Handle the `'lm-dragenter'` event for the widget.
     */
    _evtDragEnter(event) {
        if (event.mimeData.hasData(CONTENTS_MIME)) {
            const index = dist_index_es6_js_.ArrayExt.findFirstIndex(this._crumbs, node => domutils_dist_index_es6_js_.ElementExt.hitTest(node, event.clientX, event.clientY));
            if (index !== -1) {
                if (index !== Private.Crumb.Current) {
                    this._crumbs[index].classList.add(DROP_TARGET_CLASS);
                    event.preventDefault();
                    event.stopPropagation();
                }
            }
        }
    }
    /**
     * Handle the `'lm-dragleave'` event for the widget.
     */
    _evtDragLeave(event) {
        event.preventDefault();
        event.stopPropagation();
        const dropTarget = index_js_.DOMUtils.findElement(this.node, DROP_TARGET_CLASS);
        if (dropTarget) {
            dropTarget.classList.remove(DROP_TARGET_CLASS);
        }
    }
    /**
     * Handle the `'lm-dragover'` event for the widget.
     */
    _evtDragOver(event) {
        event.preventDefault();
        event.stopPropagation();
        event.dropAction = event.proposedAction;
        const dropTarget = index_js_.DOMUtils.findElement(this.node, DROP_TARGET_CLASS);
        if (dropTarget) {
            dropTarget.classList.remove(DROP_TARGET_CLASS);
        }
        const index = dist_index_es6_js_.ArrayExt.findFirstIndex(this._crumbs, node => domutils_dist_index_es6_js_.ElementExt.hitTest(node, event.clientX, event.clientY));
        if (index !== -1) {
            this._crumbs[index].classList.add(DROP_TARGET_CLASS);
        }
    }
    /**
     * Handle the `'lm-drop'` event for the widget.
     */
    _evtDrop(event) {
        event.preventDefault();
        event.stopPropagation();
        if (event.proposedAction === 'none') {
            event.dropAction = 'none';
            return;
        }
        if (!event.mimeData.hasData(CONTENTS_MIME)) {
            return;
        }
        event.dropAction = event.proposedAction;
        let target = event.target;
        while (target && target.parentElement) {
            if (target.classList.contains(DROP_TARGET_CLASS)) {
                target.classList.remove(DROP_TARGET_CLASS);
                break;
            }
            target = target.parentElement;
        }
        // Get the path based on the target node.
        const index = dist_index_es6_js_.ArrayExt.findFirstIndex(this._crumbs, node => node === target);
        if (index === -1) {
            return;
        }
        const model = this._model;
        const path = coreutils_lib_index_js_.PathExt.resolve(model.path, BREAD_CRUMB_PATHS[index]);
        const manager = model.manager;
        // Move all of the items.
        const promises = [];
        const oldPaths = event.mimeData.getData(CONTENTS_MIME);
        for (const oldPath of oldPaths) {
            const localOldPath = manager.services.contents.localPath(oldPath);
            const name = coreutils_lib_index_js_.PathExt.basename(localOldPath);
            const newPath = coreutils_lib_index_js_.PathExt.join(path, name);
            promises.push((0,docmanager_lib_index_js_.renameFile)(manager, oldPath, newPath));
        }
        void Promise.all(promises).catch(err => {
            return (0,index_js_.showErrorMessage)(this._trans.__('Move Error'), err);
        });
    }
}
/**
 * The namespace for the crumbs private data.
 */
var Private;
(function (Private) {
    /**
     * Breadcrumb item list enum.
     */
    let Crumb;
    (function (Crumb) {
        Crumb[Crumb["Home"] = 0] = "Home";
        Crumb[Crumb["Ellipsis"] = 1] = "Ellipsis";
        Crumb[Crumb["Parent"] = 2] = "Parent";
        Crumb[Crumb["Current"] = 3] = "Current";
        Crumb[Crumb["Preferred"] = 4] = "Preferred";
    })(Crumb = Private.Crumb || (Private.Crumb = {}));
    /**
     * Populate the breadcrumb node.
     */
    function updateCrumbs(breadcrumbs, separators, path, hasPreferred) {
        const node = breadcrumbs[0].parentNode;
        // Remove all but the home or preferred node.
        const firstChild = node.firstChild;
        while (firstChild && firstChild.nextSibling) {
            node.removeChild(firstChild.nextSibling);
        }
        if (hasPreferred) {
            node.appendChild(breadcrumbs[Crumb.Home]);
            node.appendChild(separators[0]);
        }
        else {
            node.appendChild(separators[0]);
        }
        const parts = path.split('/');
        if (parts.length > 2) {
            node.appendChild(breadcrumbs[Crumb.Ellipsis]);
            const grandParent = parts.slice(0, parts.length - 2).join('/');
            breadcrumbs[Crumb.Ellipsis].title = grandParent;
            node.appendChild(separators[1]);
        }
        if (path) {
            if (parts.length >= 2) {
                breadcrumbs[Crumb.Parent].textContent = parts[parts.length - 2];
                node.appendChild(breadcrumbs[Crumb.Parent]);
                const parent = parts.slice(0, parts.length - 1).join('/');
                breadcrumbs[Crumb.Parent].title = parent;
                node.appendChild(separators[2]);
            }
            breadcrumbs[Crumb.Current].textContent = parts[parts.length - 1];
            node.appendChild(breadcrumbs[Crumb.Current]);
            breadcrumbs[Crumb.Current].title = path;
            node.appendChild(separators[3]);
        }
    }
    Private.updateCrumbs = updateCrumbs;
    /**
     * Create the breadcrumb nodes.
     */
    function createCrumbs() {
        const home = ui_components_lib_index_js_.folderIcon.element({
            className: BREADCRUMB_ROOT_CLASS,
            tag: 'span',
            title: coreutils_lib_index_js_.PageConfig.getOption('serverRoot') || 'Jupyter Server Root',
            stylesheet: 'breadCrumb'
        });
        const ellipsis = ui_components_lib_index_js_.ellipsesIcon.element({
            className: BREADCRUMB_ITEM_CLASS,
            tag: 'span',
            stylesheet: 'breadCrumb'
        });
        const parent = document.createElement('span');
        parent.className = BREADCRUMB_ITEM_CLASS;
        const current = document.createElement('span');
        current.className = BREADCRUMB_ITEM_CLASS;
        const preferred = ui_components_lib_index_js_.homeIcon.element({
            className: BREADCRUMB_PREFERRED_CLASS,
            tag: 'span',
            title: coreutils_lib_index_js_.PageConfig.getOption('preferredPath') || 'Jupyter Preferred Path',
            stylesheet: 'breadCrumb'
        });
        return [home, ellipsis, parent, current, preferred];
    }
    Private.createCrumbs = createCrumbs;
    /**
     * Create the breadcrumb separator nodes.
     */
    function createCrumbSeparators() {
        const items = [];
        // The maximum number of directories that will be shown in the crumbs
        const MAX_DIRECTORIES = 2;
        // Make separators for after each directory, one at the beginning, and one
        // after a possible ellipsis.
        for (let i = 0; i < MAX_DIRECTORIES + 2; i++) {
            const item = document.createElement('span');
            item.textContent = '/';
            items.push(item);
        }
        return items;
    }
    Private.createCrumbSeparators = createCrumbSeparators;
})(Private || (Private = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/docregistry@~4.1.0-alpha.2 (strict) (fallback: ../packages/docregistry/lib/index.js)
var docregistry_lib_index_js_ = __webpack_require__(16564);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/dragdrop@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/dragdrop/dist/index.es6.js)
var dragdrop_dist_index_es6_js_ = __webpack_require__(95447);
// EXTERNAL MODULE: consume shared module (default) @lumino/messaging@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/messaging/dist/index.es6.js)
var messaging_dist_index_es6_js_ = __webpack_require__(85755);
// EXTERNAL MODULE: consume shared module (default) @lumino/signaling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/signaling/dist/index.es6.js)
var signaling_dist_index_es6_js_ = __webpack_require__(30205);
// EXTERNAL MODULE: consume shared module (default) @lumino/virtualdom@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/virtualdom/dist/index.es6.js)
var virtualdom_dist_index_es6_js_ = __webpack_require__(49581);
;// CONCATENATED MODULE: ../packages/filebrowser/lib/listing.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.














/**
 * The class name added to DirListing widget.
 */
const DIR_LISTING_CLASS = 'jp-DirListing';
/**
 * The class name added to a dir listing header node.
 */
const HEADER_CLASS = 'jp-DirListing-header';
/**
 * The class name added to a dir listing list header cell.
 */
const HEADER_ITEM_CLASS = 'jp-DirListing-headerItem';
/**
 * The class name added to a header cell text node.
 */
const HEADER_ITEM_TEXT_CLASS = 'jp-DirListing-headerItemText';
/**
 * The class name added to a header cell icon node.
 */
const HEADER_ITEM_ICON_CLASS = 'jp-DirListing-headerItemIcon';
/**
 * The class name added to the dir listing content node.
 */
const CONTENT_CLASS = 'jp-DirListing-content';
/**
 * The class name added to dir listing content item.
 */
const ITEM_CLASS = 'jp-DirListing-item';
/**
 * The class name added to the listing item text cell.
 */
const ITEM_TEXT_CLASS = 'jp-DirListing-itemText';
/**
 * The class name added to the listing item icon cell.
 */
const ITEM_ICON_CLASS = 'jp-DirListing-itemIcon';
/**
 * The class name added to the listing item modified cell.
 */
const ITEM_MODIFIED_CLASS = 'jp-DirListing-itemModified';
/**
 * The class name added to the listing item file size cell.
 */
const ITEM_FILE_SIZE_CLASS = 'jp-DirListing-itemFileSize';
/**
 * The class name added to the label element that wraps each item's checkbox and
 * the header's check-all checkbox.
 */
const CHECKBOX_WRAPPER_CLASS = 'jp-DirListing-checkboxWrapper';
/**
 * The class name added to the dir listing editor node.
 */
const EDITOR_CLASS = 'jp-DirListing-editor';
/**
 * The class name added to the name column header cell.
 */
const NAME_ID_CLASS = 'jp-id-name';
/**
 * The class name added to the modified column header cell.
 */
const MODIFIED_ID_CLASS = 'jp-id-modified';
/**
 * The class name added to the file size column header cell.
 */
const FILE_SIZE_ID_CLASS = 'jp-id-filesize';
/**
 * The class name added to the narrow column header cell.
 */
const NARROW_ID_CLASS = 'jp-id-narrow';
/**
 * The class name added to the modified column header cell and modified item cell when hidden.
 */
const MODIFIED_COLUMN_HIDDEN = 'jp-LastModified-hidden';
/**
 * The class name added to the size column header cell and size item cell when hidden.
 */
const FILE_SIZE_COLUMN_HIDDEN = 'jp-FileSize-hidden';
/**
 * The mime type for a contents drag object.
 */
const listing_CONTENTS_MIME = 'application/x-jupyter-icontents';
/**
 * The mime type for a rich contents drag object.
 */
const CONTENTS_MIME_RICH = 'application/x-jupyter-icontentsrich';
/**
 * The class name added to drop targets.
 */
const listing_DROP_TARGET_CLASS = 'jp-mod-dropTarget';
/**
 * The class name added to selected rows.
 */
const SELECTED_CLASS = 'jp-mod-selected';
/**
 * The class name added to drag state icons to add space between the icon and the file name
 */
const DRAG_ICON_CLASS = 'jp-DragIcon';
/**
 * The class name added to the widget when there are items on the clipboard.
 */
const CLIPBOARD_CLASS = 'jp-mod-clipboard';
/**
 * The class name added to cut rows.
 */
const CUT_CLASS = 'jp-mod-cut';
/**
 * The class name added when there are more than one selected rows.
 */
const MULTI_SELECTED_CLASS = 'jp-mod-multiSelected';
/**
 * The class name added to indicate running notebook.
 */
const RUNNING_CLASS = 'jp-mod-running';
/**
 * The class name added for a descending sort.
 */
const DESCENDING_CLASS = 'jp-mod-descending';
/**
 * The maximum duration between two key presses when selecting files by prefix.
 */
const PREFIX_APPEND_DURATION = 1000;
/**
 * The threshold in pixels to start a drag event.
 */
const DRAG_THRESHOLD = 5;
/**
 * A boolean indicating whether the platform is Mac.
 */
const IS_MAC = !!navigator.platform.match(/Mac/i);
/**
 * The factory MIME type supported by lumino dock panels.
 */
const FACTORY_MIME = 'application/vnd.lumino.widget-factory';
/**
 * A widget which hosts a file list area.
 */
class DirListing extends index_es6_js_.Widget {
    /**
     * Construct a new file browser directory listing widget.
     *
     * @param model - The file browser view model.
     */
    constructor(options) {
        super({
            node: (options.renderer || DirListing.defaultRenderer).createNode()
        });
        this._items = [];
        this._sortedItems = [];
        this._sortState = {
            direction: 'ascending',
            key: 'name'
        };
        this._onItemOpened = new signaling_dist_index_es6_js_.Signal(this);
        this._drag = null;
        this._dragData = null;
        this._selectTimer = -1;
        this._isCut = false;
        this._prevPath = '';
        this._clipboard = [];
        this._softSelection = '';
        this.selection = Object.create(null);
        this._searchPrefix = '';
        this._searchPrefixTimer = -1;
        this._inRename = false;
        this._isDirty = false;
        this._hiddenColumns = new Set();
        this._sortNotebooksFirst = false;
        // _focusIndex should never be set outside the range [0, this._items.length - 1]
        this._focusIndex = 0;
        this.addClass(DIR_LISTING_CLASS);
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._model = options.model;
        this._model.fileChanged.connect(this._onFileChanged, this);
        this._model.refreshed.connect(this._onModelRefreshed, this);
        this._model.pathChanged.connect(this._onPathChanged, this);
        this._editNode = document.createElement('input');
        this._editNode.className = EDITOR_CLASS;
        this._manager = this._model.manager;
        this._renderer = options.renderer || DirListing.defaultRenderer;
        const headerNode = index_js_.DOMUtils.findElement(this.node, HEADER_CLASS);
        // hide the file size column by default
        this._hiddenColumns.add('file_size');
        this._renderer.populateHeaderNode(headerNode, this.translator, this._hiddenColumns);
        this._manager.activateRequested.connect(this._onActivateRequested, this);
    }
    /**
     * Dispose of the resources held by the directory listing.
     */
    dispose() {
        this._items.length = 0;
        this._sortedItems.length = 0;
        this._clipboard.length = 0;
        super.dispose();
    }
    /**
     * Get the model used by the listing.
     */
    get model() {
        return this._model;
    }
    /**
     * Get the dir listing header node.
     *
     * #### Notes
     * This is the node which holds the header cells.
     *
     * Modifying this node directly can lead to undefined behavior.
     */
    get headerNode() {
        return index_js_.DOMUtils.findElement(this.node, HEADER_CLASS);
    }
    /**
     * Get the dir listing content node.
     *
     * #### Notes
     * This is the node which holds the item nodes.
     *
     * Modifying this node directly can lead to undefined behavior.
     */
    get contentNode() {
        return index_js_.DOMUtils.findElement(this.node, CONTENT_CLASS);
    }
    /**
     * The renderer instance used by the directory listing.
     */
    get renderer() {
        return this._renderer;
    }
    /**
     * The current sort state.
     */
    get sortState() {
        return this._sortState;
    }
    /**
     * A signal fired when an item is opened.
     */
    get onItemOpened() {
        return this._onItemOpened;
    }
    /**
     * Create an iterator over the listing's selected items.
     *
     * @returns A new iterator over the listing's selected items.
     */
    selectedItems() {
        const items = this._sortedItems;
        return (0,dist_index_es6_js_.filter)(items, item => this.selection[item.path]);
    }
    /**
     * Create an iterator over the listing's sorted items.
     *
     * @returns A new iterator over the listing's sorted items.
     */
    sortedItems() {
        return this._sortedItems[Symbol.iterator]();
    }
    /**
     * Sort the items using a sort condition.
     */
    sort(state) {
        this._sortedItems = listing_Private.sort(this.model.items(), state, this._sortNotebooksFirst);
        this._sortState = state;
        this.update();
    }
    /**
     * Rename the first currently selected item.
     *
     * @returns A promise that resolves with the new name of the item.
     */
    rename() {
        return this._doRename();
    }
    /**
     * Cut the selected items.
     */
    cut() {
        this._isCut = true;
        this._copy();
        this.update();
    }
    /**
     * Copy the selected items.
     */
    copy() {
        this._copy();
    }
    /**
     * Paste the items from the clipboard.
     *
     * @returns A promise that resolves when the operation is complete.
     */
    paste() {
        if (!this._clipboard.length) {
            this._isCut = false;
            return Promise.resolve(undefined);
        }
        const basePath = this._model.path;
        const promises = [];
        for (const path of this._clipboard) {
            if (this._isCut) {
                const localPath = this._manager.services.contents.localPath(path);
                const parts = localPath.split('/');
                const name = parts[parts.length - 1];
                const newPath = coreutils_lib_index_js_.PathExt.join(basePath, name);
                promises.push(this._model.manager.rename(path, newPath));
            }
            else {
                promises.push(this._model.manager.copy(path, basePath));
            }
        }
        // Remove any cut modifiers.
        for (const item of this._items) {
            item.classList.remove(CUT_CLASS);
        }
        this._clipboard.length = 0;
        this._isCut = false;
        this.removeClass(CLIPBOARD_CLASS);
        return Promise.all(promises)
            .then(() => {
            return undefined;
        })
            .catch(error => {
            void (0,index_js_.showErrorMessage)(this._trans._p('showErrorMessage', 'Paste Error'), error);
        });
    }
    /**
     * Delete the currently selected item(s).
     *
     * @returns A promise that resolves when the operation is complete.
     */
    async delete() {
        const items = this._sortedItems.filter(item => this.selection[item.path]);
        if (!items.length) {
            return;
        }
        const message = items.length === 1
            ? this._trans.__('Are you sure you want to permanently delete: %1?', items[0].name)
            : this._trans._n('Are you sure you want to permanently delete the %1 selected item?', 'Are you sure you want to permanently delete the %1 selected items?', items.length);
        const result = await (0,index_js_.showDialog)({
            title: this._trans.__('Delete'),
            body: message,
            buttons: [
                index_js_.Dialog.cancelButton({ label: this._trans.__('Cancel') }),
                index_js_.Dialog.warnButton({ label: this._trans.__('Delete') })
            ],
            // By default focus on "Cancel" to protect from accidental deletion
            // ("delete" and "Enter" are next to each other on many keyboards).
            defaultButton: 0
        });
        if (!this.isDisposed && result.button.accept) {
            await this._delete(items.map(item => item.path));
        }
        // Re-focus
        let focusIndex = this._focusIndex;
        const lastIndexAfterDelete = this._sortedItems.length - items.length - 1;
        if (focusIndex > lastIndexAfterDelete) {
            // If the focus index after deleting items is out of bounds, set it to the
            // last item.
            focusIndex = Math.max(0, lastIndexAfterDelete);
        }
        this._focusItem(focusIndex);
    }
    /**
     * Duplicate the currently selected item(s).
     *
     * @returns A promise that resolves when the operation is complete.
     */
    duplicate() {
        const basePath = this._model.path;
        const promises = [];
        for (const item of this.selectedItems()) {
            if (item.type !== 'directory') {
                promises.push(this._model.manager.copy(item.path, basePath));
            }
        }
        return Promise.all(promises)
            .then(() => {
            return undefined;
        })
            .catch(error => {
            void (0,index_js_.showErrorMessage)(this._trans._p('showErrorMessage', 'Duplicate file'), error);
        });
    }
    /**
     * Download the currently selected item(s).
     */
    async download() {
        await Promise.all(Array.from(this.selectedItems())
            .filter(item => item.type !== 'directory')
            .map(item => this._model.download(item.path)));
    }
    /**
     * Shut down kernels on the applicable currently selected items.
     *
     * @returns A promise that resolves when the operation is complete.
     */
    shutdownKernels() {
        const model = this._model;
        const items = this._sortedItems;
        const paths = items.map(item => item.path);
        const promises = Array.from(this._model.sessions())
            .filter(session => {
            const index = dist_index_es6_js_.ArrayExt.firstIndexOf(paths, session.path);
            return this.selection[items[index].path];
        })
            .map(session => model.manager.services.sessions.shutdown(session.id));
        return Promise.all(promises)
            .then(() => {
            return undefined;
        })
            .catch(error => {
            void (0,index_js_.showErrorMessage)(this._trans._p('showErrorMessage', 'Shut down kernel'), error);
        });
    }
    /**
     * Select next item.
     *
     * @param keepExisting - Whether to keep the current selection and add to it.
     */
    selectNext(keepExisting = false) {
        let index = -1;
        const selected = Object.keys(this.selection);
        const items = this._sortedItems;
        if (selected.length === 1 || keepExisting) {
            // Select the next item.
            const path = selected[selected.length - 1];
            index = dist_index_es6_js_.ArrayExt.findFirstIndex(items, value => value.path === path);
            index += 1;
            if (index === this._items.length) {
                index = 0;
            }
        }
        else if (selected.length === 0) {
            // Select the first item.
            index = 0;
        }
        else {
            // Select the last selected item.
            const path = selected[selected.length - 1];
            index = dist_index_es6_js_.ArrayExt.findFirstIndex(items, value => value.path === path);
        }
        if (index !== -1) {
            this._selectItem(index, keepExisting);
            domutils_dist_index_es6_js_.ElementExt.scrollIntoViewIfNeeded(this.contentNode, this._items[index]);
        }
    }
    /**
     * Select previous item.
     *
     * @param keepExisting - Whether to keep the current selection and add to it.
     */
    selectPrevious(keepExisting = false) {
        let index = -1;
        const selected = Object.keys(this.selection);
        const items = this._sortedItems;
        if (selected.length === 1 || keepExisting) {
            // Select the previous item.
            const path = selected[0];
            index = dist_index_es6_js_.ArrayExt.findFirstIndex(items, value => value.path === path);
            index -= 1;
            if (index === -1) {
                index = this._items.length - 1;
            }
        }
        else if (selected.length === 0) {
            // Select the last item.
            index = this._items.length - 1;
        }
        else {
            // Select the first selected item.
            const path = selected[0];
            index = dist_index_es6_js_.ArrayExt.findFirstIndex(items, value => value.path === path);
        }
        if (index !== -1) {
            this._selectItem(index, keepExisting);
            domutils_dist_index_es6_js_.ElementExt.scrollIntoViewIfNeeded(this.contentNode, this._items[index]);
        }
    }
    /**
     * Select the first item that starts with prefix being typed.
     */
    selectByPrefix() {
        const prefix = this._searchPrefix.toLowerCase();
        const items = this._sortedItems;
        const index = dist_index_es6_js_.ArrayExt.findFirstIndex(items, value => {
            return value.name.toLowerCase().substr(0, prefix.length) === prefix;
        });
        if (index !== -1) {
            this._selectItem(index, false);
            domutils_dist_index_es6_js_.ElementExt.scrollIntoViewIfNeeded(this.contentNode, this._items[index]);
        }
    }
    /**
     * Get whether an item is selected by name.
     *
     * @param name - The name of of the item.
     *
     * @returns Whether the item is selected.
     */
    isSelected(name) {
        const items = this._sortedItems;
        return (Array.from((0,dist_index_es6_js_.filter)(items, item => item.name === name && this.selection[item.path])).length !== 0);
    }
    /**
     * Find a model given a click.
     *
     * @param event - The mouse event.
     *
     * @returns The model for the selected file.
     */
    modelForClick(event) {
        const items = this._sortedItems;
        const index = listing_Private.hitTestNodes(this._items, event);
        if (index !== -1) {
            return items[index];
        }
        return undefined;
    }
    /**
     * Clear the selected items.
     */
    clearSelectedItems() {
        this.selection = Object.create(null);
    }
    /**
     * Select an item by name.
     *
     * @param name - The name of the item to select.
     * @param focus - Whether to move focus to the selected item.
     *
     * @returns A promise that resolves when the name is selected.
     */
    async selectItemByName(name, focus = false) {
        // Make sure the file is available.
        await this.model.refresh();
        if (this.isDisposed) {
            throw new Error('File browser is disposed.');
        }
        const items = this._sortedItems;
        const index = dist_index_es6_js_.ArrayExt.findFirstIndex(items, value => value.name === name);
        if (index === -1) {
            throw new Error('Item does not exist.');
        }
        this._selectItem(index, false, focus);
        messaging_dist_index_es6_js_.MessageLoop.sendMessage(this, index_es6_js_.Widget.Msg.UpdateRequest);
        domutils_dist_index_es6_js_.ElementExt.scrollIntoViewIfNeeded(this.contentNode, this._items[index]);
    }
    /**
     * Handle the DOM events for the directory listing.
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
            case 'mousedown':
                this._evtMousedown(event);
                break;
            case 'mouseup':
                this._evtMouseup(event);
                break;
            case 'mousemove':
                this._evtMousemove(event);
                break;
            case 'keydown':
                this.evtKeydown(event);
                break;
            case 'click':
                this._evtClick(event);
                break;
            case 'dblclick':
                this.evtDblClick(event);
                break;
            case 'dragenter':
            case 'dragover':
                this.addClass('jp-mod-native-drop');
                event.preventDefault();
                break;
            case 'dragleave':
            case 'dragend':
                this.removeClass('jp-mod-native-drop');
                break;
            case 'drop':
                this.removeClass('jp-mod-native-drop');
                this.evtNativeDrop(event);
                break;
            case 'scroll':
                this._evtScroll(event);
                break;
            case 'lm-dragenter':
                this.evtDragEnter(event);
                break;
            case 'lm-dragleave':
                this.evtDragLeave(event);
                break;
            case 'lm-dragover':
                this.evtDragOver(event);
                break;
            case 'lm-drop':
                this.evtDrop(event);
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
        const content = index_js_.DOMUtils.findElement(node, CONTENT_CLASS);
        node.addEventListener('mousedown', this);
        node.addEventListener('keydown', this);
        node.addEventListener('click', this);
        node.addEventListener('dblclick', this);
        content.addEventListener('dragenter', this);
        content.addEventListener('dragover', this);
        content.addEventListener('dragleave', this);
        content.addEventListener('dragend', this);
        content.addEventListener('drop', this);
        content.addEventListener('scroll', this);
        content.addEventListener('lm-dragenter', this);
        content.addEventListener('lm-dragleave', this);
        content.addEventListener('lm-dragover', this);
        content.addEventListener('lm-drop', this);
    }
    /**
     * A message handler invoked on a `'before-detach'` message.
     */
    onBeforeDetach(msg) {
        super.onBeforeDetach(msg);
        const node = this.node;
        const content = index_js_.DOMUtils.findElement(node, CONTENT_CLASS);
        node.removeEventListener('mousedown', this);
        node.removeEventListener('keydown', this);
        node.removeEventListener('click', this);
        node.removeEventListener('dblclick', this);
        content.removeEventListener('scroll', this);
        content.removeEventListener('dragover', this);
        content.removeEventListener('dragover', this);
        content.removeEventListener('dragleave', this);
        content.removeEventListener('dragend', this);
        content.removeEventListener('drop', this);
        content.removeEventListener('lm-dragenter', this);
        content.removeEventListener('lm-dragleave', this);
        content.removeEventListener('lm-dragover', this);
        content.removeEventListener('lm-drop', this);
        document.removeEventListener('mousemove', this, true);
        document.removeEventListener('mouseup', this, true);
    }
    /**
     * A message handler invoked on an `'after-show'` message.
     */
    onAfterShow(msg) {
        if (this._isDirty) {
            // Update the sorted items.
            this.sort(this.sortState);
            this.update();
        }
    }
    /**
     * A handler invoked on an `'update-request'` message.
     */
    onUpdateRequest(msg) {
        var _a;
        this._isDirty = false;
        // Fetch common variables.
        const items = this._sortedItems;
        const nodes = this._items;
        const content = index_js_.DOMUtils.findElement(this.node, CONTENT_CLASS);
        const renderer = this._renderer;
        this.removeClass(MULTI_SELECTED_CLASS);
        this.removeClass(SELECTED_CLASS);
        // Remove any excess item nodes.
        while (nodes.length > items.length) {
            content.removeChild(nodes.pop());
        }
        // Add any missing item nodes.
        while (nodes.length < items.length) {
            const node = renderer.createItemNode(this._hiddenColumns);
            node.classList.add(ITEM_CLASS);
            nodes.push(node);
            content.appendChild(node);
        }
        nodes.forEach((node, i) => {
            // Remove extra classes from the nodes.
            node.classList.remove(SELECTED_CLASS);
            node.classList.remove(RUNNING_CLASS);
            node.classList.remove(CUT_CLASS);
            // Uncheck each file checkbox
            const checkbox = renderer.getCheckboxNode(node);
            if (checkbox) {
                checkbox.checked = false;
            }
            // Handle `tabIndex`
            const nameNode = renderer.getNameNode(node);
            if (nameNode) {
                // Must check if the name node is there because it gets replaced by the
                // edit node when editing the name of the file or directory.
                nameNode.tabIndex = i === this._focusIndex ? 0 : -1;
            }
        });
        // Put the check-all checkbox in the header into the correct state
        const checkAllCheckbox = renderer.getCheckboxNode(this.headerNode);
        if (checkAllCheckbox) {
            const totalSelected = Object.keys(this.selection).length;
            const allSelected = items.length > 0 && totalSelected === items.length;
            const someSelected = !allSelected && totalSelected > 0;
            checkAllCheckbox.checked = allSelected;
            checkAllCheckbox.indeterminate = someSelected;
            // Stash the state in data attributes so we can access them in the click
            // handler (because in the click handler, checkbox.checked and
            // checkbox.indeterminate do not hold the previous value; they hold the
            // next value).
            checkAllCheckbox.dataset.checked = String(allSelected);
            checkAllCheckbox.dataset.indeterminate = String(someSelected);
            const trans = this.translator.load('jupyterlab');
            checkAllCheckbox === null || checkAllCheckbox === void 0 ? void 0 : checkAllCheckbox.setAttribute('aria-label', allSelected || someSelected
                ? trans.__('Deselect all files and directories')
                : trans.__('Select all files and directories'));
        }
        // Update item nodes based on widget state.
        items.forEach((item, i) => {
            const node = nodes[i];
            const ft = this._manager.registry.getFileTypeForModel(item);
            renderer.updateItemNode(node, item, ft, this.translator, this._hiddenColumns, this.selection[item.path]);
            if (this.selection[item.path] &&
                this._isCut &&
                this._model.path === this._prevPath) {
                node.classList.add(CUT_CLASS);
            }
            // add metadata to the node
            node.setAttribute('data-isdir', item.type === 'directory' ? 'true' : 'false');
        });
        // Handle the selectors on the widget node.
        const selected = Object.keys(this.selection).length;
        if (selected) {
            this.addClass(SELECTED_CLASS);
            if (selected > 1) {
                this.addClass(MULTI_SELECTED_CLASS);
            }
        }
        // Handle file session statuses.
        const paths = items.map(item => item.path);
        for (const session of this._model.sessions()) {
            const index = dist_index_es6_js_.ArrayExt.firstIndexOf(paths, session.path);
            const node = nodes[index];
            // Node may have been filtered out.
            if (node) {
                let name = (_a = session.kernel) === null || _a === void 0 ? void 0 : _a.name;
                const specs = this._model.specs;
                node.classList.add(RUNNING_CLASS);
                if (specs && name) {
                    const spec = specs.kernelspecs[name];
                    name = spec ? spec.display_name : this._trans.__('unknown');
                }
                node.title = this._trans.__('%1\nKernel: %2', node.title, name);
            }
        }
        this._prevPath = this._model.path;
    }
    onResize(msg) {
        const { width } = msg.width === -1 ? this.node.getBoundingClientRect() : msg;
        this.toggleClass('jp-DirListing-narrow', width < 250);
    }
    setColumnVisibility(name, visible) {
        if (visible) {
            this._hiddenColumns.delete(name);
        }
        else {
            this._hiddenColumns.add(name);
        }
        this.headerNode.innerHTML = '';
        this._renderer.populateHeaderNode(this.headerNode, this.translator, this._hiddenColumns);
    }
    /**
     * Update the setting to sort notebooks above files.
     * This sorts the items again if the internal value is modified.
     */
    setNotebooksFirstSorting(isEnabled) {
        let previousValue = this._sortNotebooksFirst;
        this._sortNotebooksFirst = isEnabled;
        if (this._sortNotebooksFirst !== previousValue) {
            this.sort(this._sortState);
        }
    }
    /**
     * Would this click (or other event type) hit the checkbox by default?
     */
    isWithinCheckboxHitArea(event) {
        let element = event.target;
        while (element) {
            if (element.classList.contains(CHECKBOX_WRAPPER_CLASS)) {
                return true;
            }
            element = element.parentElement;
        }
        return false;
    }
    /**
     * Handle the `'click'` event for the widget.
     */
    _evtClick(event) {
        const target = event.target;
        const header = this.headerNode;
        const renderer = this._renderer;
        if (header.contains(target)) {
            const checkbox = renderer.getCheckboxNode(header);
            if (checkbox && this.isWithinCheckboxHitArea(event)) {
                const previouslyUnchecked = checkbox.dataset.indeterminate === 'false' &&
                    checkbox.dataset.checked === 'false';
                // The only time a click on the check-all checkbox should check all is
                // when it was previously unchecked; otherwise, if the checkbox was
                // either checked (all selected) or indeterminate (some selected), the
                // click should clear all.
                if (previouslyUnchecked) {
                    // Select all items
                    this._sortedItems.forEach((item) => (this.selection[item.path] = true));
                }
                else {
                    // Unselect all items
                    this.clearSelectedItems();
                }
                this.update();
            }
            else {
                const state = this.renderer.handleHeaderClick(header, event);
                if (state) {
                    this.sort(state);
                }
            }
            return;
        }
        else {
            // Focus the selected file on click to ensure a couple of things:
            // 1. If a user clicks on the item node, its name node will receive focus.
            // 2. If a user clicks on blank space in the directory listing, the
            //    previously focussed item will be focussed.
            this._focusItem(this._focusIndex);
        }
    }
    /**
     * Handle the `'scroll'` event for the widget.
     */
    _evtScroll(event) {
        this.headerNode.scrollLeft = this.contentNode.scrollLeft;
    }
    /**
     * Handle the `'mousedown'` event for the widget.
     */
    _evtMousedown(event) {
        // Bail if clicking within the edit node
        if (event.target === this._editNode) {
            return;
        }
        // Blur the edit node if necessary.
        if (this._editNode.parentNode) {
            if (this._editNode !== event.target) {
                this._editNode.focus();
                this._editNode.blur();
                clearTimeout(this._selectTimer);
            }
            else {
                return;
            }
        }
        let index = listing_Private.hitTestNodes(this._items, event);
        if (index === -1) {
            return;
        }
        this.handleFileSelect(event);
        if (event.button !== 0) {
            clearTimeout(this._selectTimer);
        }
        // Check for clearing a context menu.
        const newContext = (IS_MAC && event.ctrlKey) || event.button === 2;
        if (newContext) {
            return;
        }
        // Left mouse press for drag start.
        if (event.button === 0) {
            this._dragData = {
                pressX: event.clientX,
                pressY: event.clientY,
                index: index
            };
            document.addEventListener('mouseup', this, true);
            document.addEventListener('mousemove', this, true);
        }
    }
    /**
     * Handle the `'mouseup'` event for the widget.
     */
    _evtMouseup(event) {
        // Handle any soft selection from the previous mouse down.
        if (this._softSelection) {
            const altered = event.metaKey || event.shiftKey || event.ctrlKey;
            // See if we need to clear the other selection.
            if (!altered && event.button === 0) {
                this.clearSelectedItems();
                this.selection[this._softSelection] = true;
                this.update();
            }
            this._softSelection = '';
        }
        // Re-focus. This is needed because nodes corresponding to files selected in
        // mousedown handler will not retain the focus as mousedown event is always
        // followed by a blur/focus event.
        if (event.button === 0) {
            this._focusItem(this._focusIndex);
        }
        // Remove the drag listeners if necessary.
        if (event.button !== 0 || !this._drag) {
            document.removeEventListener('mousemove', this, true);
            document.removeEventListener('mouseup', this, true);
            return;
        }
        event.preventDefault();
        event.stopPropagation();
    }
    /**
     * Handle the `'mousemove'` event for the widget.
     */
    _evtMousemove(event) {
        event.preventDefault();
        event.stopPropagation();
        // Bail if we are the one dragging.
        if (this._drag || !this._dragData) {
            return;
        }
        // Check for a drag initialization.
        const data = this._dragData;
        const dx = Math.abs(event.clientX - data.pressX);
        const dy = Math.abs(event.clientY - data.pressY);
        if (dx < DRAG_THRESHOLD && dy < DRAG_THRESHOLD) {
            return;
        }
        this._startDrag(data.index, event.clientX, event.clientY);
    }
    /**
     * Handle the opening of an item.
     */
    handleOpen(item) {
        this._onItemOpened.emit(item);
        if (item.type === 'directory') {
            const localPath = this._manager.services.contents.localPath(item.path);
            this._model
                .cd(`/${localPath}`)
                .catch(error => (0,index_js_.showErrorMessage)(this._trans._p('showErrorMessage', 'Open directory'), error));
        }
        else {
            const path = item.path;
            this._manager.openOrReveal(path);
        }
    }
    /**
     * Calculate the next focus index, given the current focus index and a
     * direction, keeping within the bounds of the directory listing.
     *
     * @param index Current focus index
     * @param direction -1 (up) or 1 (down)
     * @returns The next focus index, which could be the same as the current focus
     * index if at the boundary.
     */
    _getNextFocusIndex(index, direction) {
        const nextIndex = index + direction;
        if (nextIndex === -1 || nextIndex === this._items.length) {
            // keep focus index within bounds
            return index;
        }
        else {
            return nextIndex;
        }
    }
    /**
     * Handle the up or down arrow key.
     *
     * @param event The keyboard event
     * @param direction -1 (up) or 1 (down)
     */
    _handleArrowY(event, direction) {
        // We only handle the `ctrl` and `shift` modifiers. If other modifiers are
        // present, then do nothing.
        if (event.altKey || event.metaKey) {
            return;
        }
        // If folder is empty, there's nothing to do with the up/down key.
        if (!this._items.length) {
            return;
        }
        // Don't handle the arrow key press if it's not on directory item. This
        // avoids a confusing user experience that can result from when the user
        // moves the selection and focus index apart (via ctrl + up/down). The last
        // selected item remains highlighted but the last focussed item loses its
        // focus ring if it's not actively focussed.  This forces the user to
        // visibly reveal the last focussed item before moving the focus.
        if (!event.target.classList.contains(ITEM_TEXT_CLASS)) {
            return;
        }
        event.stopPropagation();
        event.preventDefault();
        const focusIndex = this._focusIndex;
        let nextFocusIndex = this._getNextFocusIndex(focusIndex, direction);
        // The following if-block allows the first press of the down arrow to select
        // the first (rather than the second) file/directory in the list. This is
        // the situation when the page first loads or when a user changes directory.
        if (direction > 0 &&
            focusIndex === 0 &&
            !event.ctrlKey &&
            Object.keys(this.selection).length === 0) {
            nextFocusIndex = 0;
        }
        // Shift key indicates multi-selection. Either the user is trying to grow
        // the selection, or shrink it.
        if (event.shiftKey) {
            this._handleMultiSelect(nextFocusIndex);
        }
        else if (!event.ctrlKey) {
            // If neither the shift nor ctrl keys were used with the up/down arrow,
            // then we treat it as a normal, unmodified key press and select the
            // next item.
            this._selectItem(nextFocusIndex, event.shiftKey, false /* focus = false because we call focus method directly following this */);
        }
        this._focusItem(nextFocusIndex);
        this.update();
    }
    /**
     * cd ..
     *
     * Go up one level in the directory tree.
     */
    async goUp() {
        const model = this.model;
        if (model.path === model.rootPath) {
            return;
        }
        try {
            await model.cd('..');
        }
        catch (reason) {
            console.warn(`Failed to go to parent directory of ${model.path}`, reason);
        }
    }
    /**
     * Handle the `'keydown'` event for the widget.
     */
    evtKeydown(event) {
        // Do not handle any keydown events here if in the middle of a file rename.
        if (this._inRename) {
            return;
        }
        switch (event.keyCode) {
            case 13: {
                // Enter
                // Do nothing if any modifier keys are pressed.
                if (event.ctrlKey || event.shiftKey || event.altKey || event.metaKey) {
                    return;
                }
                event.preventDefault();
                event.stopPropagation();
                for (const item of this.selectedItems()) {
                    this.handleOpen(item);
                }
                return;
            }
            case 38:
                // Up arrow
                this._handleArrowY(event, -1);
                return;
            case 40:
                // Down arrow
                this._handleArrowY(event, 1);
                return;
            case 32: {
                // Space
                if (event.ctrlKey) {
                    // Follow the Windows and Ubuntu convention: you must press `ctrl` +
                    // `space` in order to toggle whether an item is selected.
                    // However, do not handle if any other modifiers were pressed.
                    if (event.metaKey || event.shiftKey || event.altKey) {
                        return;
                    }
                    // Make sure the ctrl+space key stroke was on a valid, focussed target.
                    const node = this._items[this._focusIndex];
                    if (!(
                    // Event must have occurred within a node whose item can be toggled.
                    (node.contains(event.target) &&
                        // That node must also contain the currently focussed element.
                        node.contains(document.activeElement)))) {
                        return;
                    }
                    event.stopPropagation();
                    // Prevent default, otherwise the container will scroll.
                    event.preventDefault();
                    // Toggle item selected
                    const { path } = this._sortedItems[this._focusIndex];
                    if (this.selection[path]) {
                        delete this.selection[path];
                    }
                    else {
                        this.selection[path] = true;
                    }
                    this.update();
                    // Key was handled, so return.
                    return;
                }
                break;
            }
        }
        // Detects printable characters typed by the user.
        // Not all browsers support .key, but it discharges us from reconstructing
        // characters from key codes.
        if (event.key !== undefined &&
            event.key.length === 1 &&
            // Don't gobble up the space key on the check-all checkbox (which the
            // browser treats as a click event).
            !((event.key === ' ' || event.keyCode === 32) &&
                event.target.type === 'checkbox')) {
            if (event.ctrlKey || event.shiftKey || event.altKey || event.metaKey) {
                return;
            }
            this._searchPrefix += event.key;
            clearTimeout(this._searchPrefixTimer);
            this._searchPrefixTimer = window.setTimeout(() => {
                this._searchPrefix = '';
            }, PREFIX_APPEND_DURATION);
            this.selectByPrefix();
            event.stopPropagation();
            event.preventDefault();
        }
    }
    /**
     * Handle the `'dblclick'` event for the widget.
     */
    evtDblClick(event) {
        // Do nothing if it's not a left mouse press.
        if (event.button !== 0) {
            return;
        }
        // Do nothing if any modifier keys are pressed.
        if (event.ctrlKey || event.shiftKey || event.altKey || event.metaKey) {
            return;
        }
        // Do nothing if the double click is on a checkbox. (Otherwise a rapid
        // check-uncheck on the checkbox will cause the adjacent file/folder to
        // open, which is probably not what the user intended.)
        if (this.isWithinCheckboxHitArea(event)) {
            return;
        }
        // Stop the event propagation.
        event.preventDefault();
        event.stopPropagation();
        clearTimeout(this._selectTimer);
        this._editNode.blur();
        // Find a valid double click target.
        const target = event.target;
        const i = dist_index_es6_js_.ArrayExt.findFirstIndex(this._items, node => node.contains(target));
        if (i === -1) {
            return;
        }
        const item = this._sortedItems[i];
        this.handleOpen(item);
    }
    /**
     * Handle the `drop` event for the widget.
     */
    evtNativeDrop(event) {
        var _a, _b, _c;
        const files = (_a = event.dataTransfer) === null || _a === void 0 ? void 0 : _a.files;
        if (!files || files.length === 0) {
            return;
        }
        const length = (_b = event.dataTransfer) === null || _b === void 0 ? void 0 : _b.items.length;
        if (!length) {
            return;
        }
        for (let i = 0; i < length; i++) {
            let entry = (_c = event.dataTransfer) === null || _c === void 0 ? void 0 : _c.items[i].webkitGetAsEntry();
            if (entry === null || entry === void 0 ? void 0 : entry.isDirectory) {
                console.log('currently not supporting drag + drop for folders');
                void (0,index_js_.showDialog)({
                    title: this._trans.__('Error Uploading Folder'),
                    body: this._trans.__('Drag and Drop is currently not supported for folders'),
                    buttons: [index_js_.Dialog.cancelButton({ label: this._trans.__('Close') })]
                });
            }
        }
        event.preventDefault();
        for (let i = 0; i < files.length; i++) {
            void this._model.upload(files[i]);
        }
    }
    /**
     * Handle the `'lm-dragenter'` event for the widget.
     */
    evtDragEnter(event) {
        if (event.mimeData.hasData(listing_CONTENTS_MIME)) {
            const index = listing_Private.hitTestNodes(this._items, event);
            if (index === -1) {
                return;
            }
            const item = this._sortedItems[index];
            if (item.type !== 'directory' || this.selection[item.path]) {
                return;
            }
            const target = event.target;
            target.classList.add(listing_DROP_TARGET_CLASS);
            event.preventDefault();
            event.stopPropagation();
        }
    }
    /**
     * Handle the `'lm-dragleave'` event for the widget.
     */
    evtDragLeave(event) {
        event.preventDefault();
        event.stopPropagation();
        const dropTarget = index_js_.DOMUtils.findElement(this.node, listing_DROP_TARGET_CLASS);
        if (dropTarget) {
            dropTarget.classList.remove(listing_DROP_TARGET_CLASS);
        }
    }
    /**
     * Handle the `'lm-dragover'` event for the widget.
     */
    evtDragOver(event) {
        event.preventDefault();
        event.stopPropagation();
        event.dropAction = event.proposedAction;
        const dropTarget = index_js_.DOMUtils.findElement(this.node, listing_DROP_TARGET_CLASS);
        if (dropTarget) {
            dropTarget.classList.remove(listing_DROP_TARGET_CLASS);
        }
        const index = listing_Private.hitTestNodes(this._items, event);
        this._items[index].classList.add(listing_DROP_TARGET_CLASS);
    }
    /**
     * Handle the `'lm-drop'` event for the widget.
     */
    evtDrop(event) {
        event.preventDefault();
        event.stopPropagation();
        clearTimeout(this._selectTimer);
        if (event.proposedAction === 'none') {
            event.dropAction = 'none';
            return;
        }
        if (!event.mimeData.hasData(listing_CONTENTS_MIME)) {
            return;
        }
        let target = event.target;
        while (target && target.parentElement) {
            if (target.classList.contains(listing_DROP_TARGET_CLASS)) {
                target.classList.remove(listing_DROP_TARGET_CLASS);
                break;
            }
            target = target.parentElement;
        }
        // Get the path based on the target node.
        const index = dist_index_es6_js_.ArrayExt.firstIndexOf(this._items, target);
        const items = this._sortedItems;
        let basePath = this._model.path;
        if (items[index].type === 'directory') {
            basePath = coreutils_lib_index_js_.PathExt.join(basePath, items[index].name);
        }
        const manager = this._manager;
        // Handle the items.
        const promises = [];
        const paths = event.mimeData.getData(listing_CONTENTS_MIME);
        if (event.ctrlKey && event.proposedAction === 'move') {
            event.dropAction = 'copy';
        }
        else {
            event.dropAction = event.proposedAction;
        }
        for (const path of paths) {
            const localPath = manager.services.contents.localPath(path);
            const name = coreutils_lib_index_js_.PathExt.basename(localPath);
            const newPath = coreutils_lib_index_js_.PathExt.join(basePath, name);
            // Skip files that are not moving.
            if (newPath === path) {
                continue;
            }
            if (event.dropAction === 'copy') {
                promises.push(manager.copy(path, basePath));
            }
            else {
                promises.push((0,docmanager_lib_index_js_.renameFile)(manager, path, newPath));
            }
        }
        Promise.all(promises).catch(error => {
            void (0,index_js_.showErrorMessage)(this._trans._p('showErrorMessage', 'Error while copying/moving files'), error);
        });
    }
    /**
     * Start a drag event.
     */
    _startDrag(index, clientX, clientY) {
        let selectedPaths = Object.keys(this.selection);
        const source = this._items[index];
        const items = this._sortedItems;
        let selectedItems;
        let item;
        // If the source node is not selected, use just that node.
        if (!source.classList.contains(SELECTED_CLASS)) {
            item = items[index];
            selectedPaths = [item.path];
            selectedItems = [item];
        }
        else {
            const path = selectedPaths[0];
            item = items.find(value => value.path === path);
            selectedItems = this.selectedItems();
        }
        if (!item) {
            return;
        }
        // Create the drag image.
        const ft = this._manager.registry.getFileTypeForModel(item);
        const dragImage = this.renderer.createDragImage(source, selectedPaths.length, this._trans, ft);
        // Set up the drag event.
        this._drag = new dragdrop_dist_index_es6_js_.Drag({
            dragImage,
            mimeData: new dist_index_js_.MimeData(),
            supportedActions: 'move',
            proposedAction: 'move'
        });
        this._drag.mimeData.setData(listing_CONTENTS_MIME, selectedPaths);
        // Add thunks for getting mime data content.
        // We thunk the content so we don't try to make a network call
        // when it's not needed. E.g. just moving files around
        // in a filebrowser
        const services = this.model.manager.services;
        for (const item of selectedItems) {
            this._drag.mimeData.setData(CONTENTS_MIME_RICH, {
                model: item,
                withContent: async () => {
                    return await services.contents.get(item.path);
                }
            });
        }
        if (item && item.type !== 'directory') {
            const otherPaths = selectedPaths.slice(1).reverse();
            this._drag.mimeData.setData(FACTORY_MIME, () => {
                if (!item) {
                    return;
                }
                const path = item.path;
                let widget = this._manager.findWidget(path);
                if (!widget) {
                    widget = this._manager.open(item.path);
                }
                if (otherPaths.length) {
                    const firstWidgetPlaced = new dist_index_js_.PromiseDelegate();
                    void firstWidgetPlaced.promise.then(() => {
                        let prevWidget = widget;
                        otherPaths.forEach(path => {
                            const options = {
                                ref: prevWidget === null || prevWidget === void 0 ? void 0 : prevWidget.id,
                                mode: 'tab-after'
                            };
                            prevWidget = this._manager.openOrReveal(path, void 0, void 0, options);
                            this._manager.openOrReveal(item.path);
                        });
                    });
                    firstWidgetPlaced.resolve(void 0);
                }
                return widget;
            });
        }
        // Start the drag and remove the mousemove and mouseup listeners.
        document.removeEventListener('mousemove', this, true);
        document.removeEventListener('mouseup', this, true);
        clearTimeout(this._selectTimer);
        void this._drag.start(clientX, clientY).then(action => {
            this._drag = null;
            clearTimeout(this._selectTimer);
        });
    }
    /**
     * Handle selection on a file node.
     */
    handleFileSelect(event) {
        // Fetch common variables.
        const items = this._sortedItems;
        const index = listing_Private.hitTestNodes(this._items, event);
        clearTimeout(this._selectTimer);
        if (index === -1) {
            return;
        }
        // Clear any existing soft selection.
        this._softSelection = '';
        const path = items[index].path;
        const selected = Object.keys(this.selection);
        const isLeftClickOnCheckbox = event.button === 0 &&
            // On Mac, a left-click with the ctrlKey is treated as a right-click.
            !(IS_MAC && event.ctrlKey) &&
            this.isWithinCheckboxHitArea(event);
        // Handle toggling.
        if ((IS_MAC && event.metaKey) ||
            (!IS_MAC && event.ctrlKey) ||
            isLeftClickOnCheckbox) {
            if (this.selection[path]) {
                delete this.selection[path];
            }
            else {
                this.selection[path] = true;
            }
            this._focusItem(index);
            // Handle multiple select.
        }
        else if (event.shiftKey) {
            this._handleMultiSelect(index);
            this._focusItem(index);
            // Handle a 'soft' selection
        }
        else if (path in this.selection && selected.length > 1) {
            this._softSelection = path;
            // Default to selecting the only the item.
        }
        else {
            // Select only the given item.
            return this._selectItem(index, false, true);
        }
        this.update();
    }
    /**
     * (Re-)focus an item in the directory listing.
     *
     * @param index The index of the item node to focus
     */
    _focusItem(index) {
        const items = this._items;
        if (items.length === 0) {
            // Focus the top node if the folder is empty and therefore there are no
            // items inside the folder to focus.
            this._focusIndex = 0;
            this.node.focus();
            return;
        }
        this._focusIndex = index;
        const node = items[index];
        const nameNode = this.renderer.getNameNode(node);
        if (nameNode) {
            // Make the filename text node focusable so that it receives keyboard
            // events; text node was specifically chosen to receive shortcuts because
            // it gets substituted with input element during file name edits which
            // conveniently deactivates irrelevant shortcuts.
            nameNode.tabIndex = 0;
            nameNode.focus();
        }
    }
    /**
     * Are all of the items between two provided indices selected?
     *
     * The items at the indices are not considered.
     *
     * @param j Index of one item.
     * @param k Index of another item. Note: may be less or greater than first
     *          index.
     * @returns True if and only if all items between the j and k are selected.
     *          Returns undefined if j and k are the same.
     */
    _allSelectedBetween(j, k) {
        if (j === k) {
            return;
        }
        const [start, end] = j < k ? [j + 1, k] : [k + 1, j];
        return this._sortedItems
            .slice(start, end)
            .reduce((result, item) => result && this.selection[item.path], true);
    }
    /**
     * Handle a multiple select on a file item node.
     */
    _handleMultiSelect(index) {
        const items = this._sortedItems;
        const fromIndex = this._focusIndex;
        const target = items[index];
        let shouldAdd = true;
        if (index === fromIndex) {
            // This follows the convention in Ubuntu and Windows, which is to allow
            // the focussed item to gain but not lose selected status on shift-click.
            // (MacOS is irrelevant here because MacOS Finder has no notion of a
            // focused-but-not-selected state.)
            this.selection[target.path] = true;
            return;
        }
        // If the target and all items in-between are selected, then we assume that
        // the user is trying to shrink rather than grow the group of selected
        // items.
        if (this.selection[target.path]) {
            // However, there is a special case when the distance between the from-
            // and to- index is just one (for example, when the user is pressing the
            // shift key plus arrow-up/down). If and only if the situation looks like
            // the following when going down (or reverse when going up) ...
            //
            // - [ante-anchor / previous item] unselected (or boundary)
            // - [anchor / currently focussed item / item at from-index] selected
            // - [target / next item / item at to-index] selected
            //
            // ... then we shrink the selection / unselect the currently focussed
            // item.
            if (Math.abs(index - fromIndex) === 1) {
                const anchor = items[fromIndex];
                const anteAnchor = items[fromIndex + (index < fromIndex ? 1 : -1)];
                if (
                // Currently focussed item is selected
                this.selection[anchor.path] &&
                    // Item on other side of focussed item (away from target) is either a
                    // boundary or unselected
                    (!anteAnchor || !this.selection[anteAnchor.path])) {
                    delete this.selection[anchor.path];
                }
            }
            else if (this._allSelectedBetween(fromIndex, index)) {
                shouldAdd = false;
            }
        }
        // Select (or unselect) the rows between chosen index (target) and the last
        // focussed.
        const step = fromIndex < index ? 1 : -1;
        for (let i = fromIndex; i !== index + step; i += step) {
            if (shouldAdd) {
                if (i === fromIndex) {
                    // Do not change the selection state of the starting (fromIndex) item.
                    continue;
                }
                this.selection[items[i].path] = true;
            }
            else {
                if (i === index) {
                    // Do not unselect the target item.
                    continue;
                }
                delete this.selection[items[i].path];
            }
        }
    }
    /**
     * Copy the selected items, and optionally cut as well.
     */
    _copy() {
        this._clipboard.length = 0;
        for (const item of this.selectedItems()) {
            this._clipboard.push(item.path);
        }
    }
    /**
     * Delete the files with the given paths.
     */
    async _delete(paths) {
        await Promise.all(paths.map(path => this._model.manager.deleteFile(path).catch(err => {
            void (0,index_js_.showErrorMessage)(this._trans._p('showErrorMessage', 'Delete Failed'), err);
        })));
    }
    /**
     * Allow the user to rename item on a given row.
     */
    async _doRename() {
        this._inRename = true;
        const selectedPaths = Object.keys(this.selection);
        // Bail out if nothing has been selected.
        if (selectedPaths.length === 0) {
            this._inRename = false;
            return Promise.resolve('');
        }
        // Figure out which selected path to use for the rename.
        const items = this._sortedItems;
        let { path } = items[this._focusIndex];
        if (!this.selection[path]) {
            // If the currently focused item is not selected, then choose the last
            // selected item.
            path = selectedPaths.slice(-1)[0];
        }
        // Get the corresponding model, nodes, and file name.
        const index = dist_index_es6_js_.ArrayExt.findFirstIndex(items, value => value.path === path);
        const row = this._items[index];
        const item = items[index];
        const nameNode = this.renderer.getNameNode(row);
        const original = item.name;
        // Seed the text input with current file name, and select and focus it.
        this._editNode.value = original;
        this._selectItem(index, false, true);
        // Wait for user input
        const newName = await listing_Private.userInputForRename(nameNode, this._editNode, original);
        // Check if the widget was disposed during the `await`.
        if (this.isDisposed) {
            this._inRename = false;
            throw new Error('File browser is disposed.');
        }
        let finalFilename = newName;
        if (!newName || newName === original) {
            finalFilename = original;
        }
        else if (!(0,docmanager_lib_index_js_.isValidFileName)(newName)) {
            void (0,index_js_.showErrorMessage)(this._trans.__('Rename Error'), Error(this._trans._p('showErrorMessage', '"%1" is not a valid name for a file. Names must have nonzero length, and cannot include "/", "\\", or ":"', newName)));
            finalFilename = original;
        }
        else {
            // Attempt rename at the file system level.
            const manager = this._manager;
            const oldPath = coreutils_lib_index_js_.PathExt.join(this._model.path, original);
            const newPath = coreutils_lib_index_js_.PathExt.join(this._model.path, newName);
            try {
                await (0,docmanager_lib_index_js_.renameFile)(manager, oldPath, newPath);
            }
            catch (error) {
                if (error !== 'File not renamed') {
                    void (0,index_js_.showErrorMessage)(this._trans._p('showErrorMessage', 'Rename Error'), error);
                }
                finalFilename = original;
            }
            // Check if the widget was disposed during the `await`.
            if (this.isDisposed) {
                this._inRename = false;
                throw new Error('File browser is disposed.');
            }
        }
        // If nothing else has been selected, then select the renamed file. In
        // other words, don't select the renamed file if the user has clicked
        // away to some other file.
        if (!this.isDisposed &&
            Object.keys(this.selection).length === 1 &&
            // We haven't updated the instance yet to reflect the rename, so unless
            // the user or something else has updated the selection, the original file
            // path and not the new file path will be in `this.selection`.
            this.selection[item.path]) {
            try {
                await this.selectItemByName(finalFilename, true);
            }
            catch (_a) {
                // do nothing
                console.warn('After rename, failed to select file', finalFilename);
            }
        }
        this._inRename = false;
        return finalFilename;
    }
    /**
     * Select a given item.
     */
    _selectItem(index, keepExisting, focus = true) {
        // Selected the given row(s)
        const items = this._sortedItems;
        if (!keepExisting) {
            this.clearSelectedItems();
        }
        const path = items[index].path;
        this.selection[path] = true;
        if (focus) {
            this._focusItem(index);
        }
        this.update();
    }
    /**
     * Handle the `refreshed` signal from the model.
     */
    _onModelRefreshed() {
        // Update the selection.
        const existing = Object.keys(this.selection);
        this.clearSelectedItems();
        for (const item of this._model.items()) {
            const path = item.path;
            if (existing.indexOf(path) !== -1) {
                this.selection[path] = true;
            }
        }
        if (this.isVisible) {
            // Update the sorted items.
            this.sort(this.sortState);
        }
        else {
            this._isDirty = true;
        }
    }
    /**
     * Handle a `pathChanged` signal from the model.
     */
    _onPathChanged() {
        // Reset the selection.
        this.clearSelectedItems();
        // Update the sorted items.
        this.sort(this.sortState);
        // Reset focus. But wait until the DOM has been updated (hence
        // `requestAnimationFrame`).
        requestAnimationFrame(() => {
            this._focusItem(0);
        });
    }
    /**
     * Handle a `fileChanged` signal from the model.
     */
    _onFileChanged(sender, args) {
        const newValue = args.newValue;
        if (!newValue) {
            return;
        }
        const name = newValue.name;
        if (args.type !== 'new' || !name) {
            return;
        }
        void this.selectItemByName(name).catch(() => {
            /* Ignore if file does not exist. */
        });
    }
    /**
     * Handle an `activateRequested` signal from the manager.
     */
    _onActivateRequested(sender, args) {
        const dirname = coreutils_lib_index_js_.PathExt.dirname(args);
        if (dirname !== this._model.path) {
            return;
        }
        const basename = coreutils_lib_index_js_.PathExt.basename(args);
        this.selectItemByName(basename).catch(() => {
            /* Ignore if file does not exist. */
        });
    }
}
/**
 * The namespace for the `DirListing` class statics.
 */
(function (DirListing) {
    /**
     * The default implementation of an `IRenderer`.
     */
    class Renderer {
        /**
         * Create the DOM node for a dir listing.
         */
        createNode() {
            const node = document.createElement('div');
            const header = document.createElement('div');
            const content = document.createElement('ul');
            content.className = CONTENT_CLASS;
            header.className = HEADER_CLASS;
            node.appendChild(header);
            node.appendChild(content);
            // Set to -1 to allow calling this.node.focus().
            node.tabIndex = -1;
            return node;
        }
        /**
         * Populate and empty header node for a dir listing.
         *
         * @param node - The header node to populate.
         */
        populateHeaderNode(node, translator, hiddenColumns) {
            translator = translator || translation_lib_index_js_.nullTranslator;
            const trans = translator.load('jupyterlab');
            const name = this.createHeaderItemNode(trans.__('Name'));
            const narrow = document.createElement('div');
            const modified = this.createHeaderItemNode(trans.__('Last Modified'));
            const fileSize = this.createHeaderItemNode(trans.__('File Size'));
            name.classList.add(NAME_ID_CLASS);
            name.classList.add(SELECTED_CLASS);
            modified.classList.add(MODIFIED_ID_CLASS);
            fileSize.classList.add(FILE_SIZE_ID_CLASS);
            narrow.classList.add(NARROW_ID_CLASS);
            narrow.textContent = '...';
            if (!(hiddenColumns === null || hiddenColumns === void 0 ? void 0 : hiddenColumns.has('is_selected'))) {
                const checkboxWrapper = this.createCheckboxWrapperNode({
                    alwaysVisible: true
                });
                node.appendChild(checkboxWrapper);
            }
            node.appendChild(name);
            node.appendChild(narrow);
            node.appendChild(modified);
            node.appendChild(fileSize);
            if (hiddenColumns === null || hiddenColumns === void 0 ? void 0 : hiddenColumns.has('last_modified')) {
                modified.classList.add(MODIFIED_COLUMN_HIDDEN);
            }
            else {
                modified.classList.remove(MODIFIED_COLUMN_HIDDEN);
            }
            if (hiddenColumns === null || hiddenColumns === void 0 ? void 0 : hiddenColumns.has('file_size')) {
                fileSize.classList.add(FILE_SIZE_COLUMN_HIDDEN);
            }
            else {
                fileSize.classList.remove(FILE_SIZE_COLUMN_HIDDEN);
            }
            // set the initial caret icon
            listing_Private.updateCaret(index_js_.DOMUtils.findElement(name, HEADER_ITEM_ICON_CLASS), 'right', 'up');
        }
        /**
         * Handle a header click.
         *
         * @param node - A node populated by [[populateHeaderNode]].
         *
         * @param event - A click event on the node.
         *
         * @returns The sort state of the header after the click event.
         */
        handleHeaderClick(node, event) {
            const name = index_js_.DOMUtils.findElement(node, NAME_ID_CLASS);
            const modified = index_js_.DOMUtils.findElement(node, MODIFIED_ID_CLASS);
            const fileSize = index_js_.DOMUtils.findElement(node, FILE_SIZE_ID_CLASS);
            const state = { direction: 'ascending', key: 'name' };
            const target = event.target;
            const modifiedIcon = index_js_.DOMUtils.findElement(modified, HEADER_ITEM_ICON_CLASS);
            const fileSizeIcon = index_js_.DOMUtils.findElement(fileSize, HEADER_ITEM_ICON_CLASS);
            const nameIcon = index_js_.DOMUtils.findElement(name, HEADER_ITEM_ICON_CLASS);
            if (name.contains(target)) {
                if (name.classList.contains(SELECTED_CLASS)) {
                    if (!name.classList.contains(DESCENDING_CLASS)) {
                        state.direction = 'descending';
                        name.classList.add(DESCENDING_CLASS);
                        listing_Private.updateCaret(nameIcon, 'right', 'down');
                    }
                    else {
                        name.classList.remove(DESCENDING_CLASS);
                        listing_Private.updateCaret(nameIcon, 'right', 'up');
                    }
                }
                else {
                    name.classList.remove(DESCENDING_CLASS);
                    listing_Private.updateCaret(nameIcon, 'right', 'up');
                }
                name.classList.add(SELECTED_CLASS);
                modified.classList.remove(SELECTED_CLASS);
                modified.classList.remove(DESCENDING_CLASS);
                fileSize.classList.remove(SELECTED_CLASS);
                fileSize.classList.remove(DESCENDING_CLASS);
                listing_Private.updateCaret(modifiedIcon, 'left');
                listing_Private.updateCaret(fileSizeIcon, 'left');
                return state;
            }
            if (modified.contains(target)) {
                state.key = 'last_modified';
                if (modified.classList.contains(SELECTED_CLASS)) {
                    if (!modified.classList.contains(DESCENDING_CLASS)) {
                        state.direction = 'descending';
                        modified.classList.add(DESCENDING_CLASS);
                        listing_Private.updateCaret(modifiedIcon, 'left', 'down');
                    }
                    else {
                        modified.classList.remove(DESCENDING_CLASS);
                        listing_Private.updateCaret(modifiedIcon, 'left', 'up');
                    }
                }
                else {
                    modified.classList.remove(DESCENDING_CLASS);
                    listing_Private.updateCaret(modifiedIcon, 'left', 'up');
                }
                modified.classList.add(SELECTED_CLASS);
                name.classList.remove(SELECTED_CLASS);
                name.classList.remove(DESCENDING_CLASS);
                fileSize.classList.remove(SELECTED_CLASS);
                fileSize.classList.remove(DESCENDING_CLASS);
                listing_Private.updateCaret(nameIcon, 'right');
                listing_Private.updateCaret(fileSizeIcon, 'left');
                return state;
            }
            if (fileSize.contains(target)) {
                state.key = 'file_size';
                if (fileSize.classList.contains(SELECTED_CLASS)) {
                    if (!fileSize.classList.contains(DESCENDING_CLASS)) {
                        state.direction = 'descending';
                        fileSize.classList.add(DESCENDING_CLASS);
                        listing_Private.updateCaret(fileSizeIcon, 'left', 'down');
                    }
                    else {
                        fileSize.classList.remove(DESCENDING_CLASS);
                        listing_Private.updateCaret(fileSizeIcon, 'left', 'up');
                    }
                }
                else {
                    fileSize.classList.remove(DESCENDING_CLASS);
                    listing_Private.updateCaret(fileSizeIcon, 'left', 'up');
                }
                fileSize.classList.add(SELECTED_CLASS);
                name.classList.remove(SELECTED_CLASS);
                name.classList.remove(DESCENDING_CLASS);
                modified.classList.remove(SELECTED_CLASS);
                modified.classList.remove(DESCENDING_CLASS);
                listing_Private.updateCaret(nameIcon, 'right');
                listing_Private.updateCaret(modifiedIcon, 'left');
                return state;
            }
            return state;
        }
        /**
         * Create a new item node for a dir listing.
         *
         * @returns A new DOM node to use as a content item.
         */
        createItemNode(hiddenColumns) {
            const node = document.createElement('li');
            const icon = document.createElement('span');
            const text = document.createElement('span');
            const modified = document.createElement('span');
            const fileSize = document.createElement('span');
            icon.className = ITEM_ICON_CLASS;
            text.className = ITEM_TEXT_CLASS;
            modified.className = ITEM_MODIFIED_CLASS;
            fileSize.className = ITEM_FILE_SIZE_CLASS;
            if (!(hiddenColumns === null || hiddenColumns === void 0 ? void 0 : hiddenColumns.has('is_selected'))) {
                const checkboxWrapper = this.createCheckboxWrapperNode();
                node.appendChild(checkboxWrapper);
            }
            node.appendChild(icon);
            node.appendChild(text);
            node.appendChild(modified);
            node.appendChild(fileSize);
            if (hiddenColumns === null || hiddenColumns === void 0 ? void 0 : hiddenColumns.has('last_modified')) {
                modified.classList.add(MODIFIED_COLUMN_HIDDEN);
            }
            else {
                modified.classList.remove(MODIFIED_COLUMN_HIDDEN);
            }
            if (hiddenColumns === null || hiddenColumns === void 0 ? void 0 : hiddenColumns.has('file_size')) {
                fileSize.classList.add(FILE_SIZE_COLUMN_HIDDEN);
            }
            else {
                fileSize.classList.remove(FILE_SIZE_COLUMN_HIDDEN);
            }
            return node;
        }
        /**
         * Creates a node containing a checkbox.
         *
         * We wrap the checkbox in a label element in order to increase its hit
         * area. This is because the padding of the checkbox itself cannot be
         * increased via CSS, as the CSS/form compatibility table at the following
         * url from MDN shows:
         * https://developer.mozilla.org/en-US/docs/Learn/Forms/Property_compatibility_table_for_form_controls#check_boxes_and_radio_buttons
         *
         * @param [options]
         * @params options.alwaysVisible Should the checkbox be visible even when
         * not hovered?
         * @returns A new DOM node that contains a checkbox.
         */
        createCheckboxWrapperNode(options) {
            // Wrap the checkbox in a label element in order to increase its hit area.
            const labelWrapper = document.createElement('label');
            labelWrapper.classList.add(CHECKBOX_WRAPPER_CLASS);
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            // Prevent the user from clicking (via mouse, keyboard, or touch) the
            // checkbox since other code handles the mouse and keyboard events and
            // controls the checked state of the checkbox.
            checkbox.addEventListener('click', event => {
                event.preventDefault();
            });
            // The individual file checkboxes are visible on hover, but the header
            // check-all checkbox is always visible.
            if (options === null || options === void 0 ? void 0 : options.alwaysVisible) {
                labelWrapper.classList.add('jp-mod-visible');
            }
            else {
                // Disable tabbing to all other checkboxes.
                checkbox.tabIndex = -1;
            }
            labelWrapper.appendChild(checkbox);
            return labelWrapper;
        }
        /**
         * Update an item node to reflect the current state of a model.
         *
         * @param node - A node created by [[createItemNode]].
         *
         * @param model - The model object to use for the item state.
         *
         * @param fileType - The file type of the item, if applicable.
         *
         */
        updateItemNode(node, model, fileType, translator, hiddenColumns, selected) {
            if (selected) {
                node.classList.add(SELECTED_CLASS);
            }
            fileType =
                fileType || docregistry_lib_index_js_.DocumentRegistry.getDefaultTextFileType(translator);
            const { icon, iconClass, name } = fileType;
            translator = translator || translation_lib_index_js_.nullTranslator;
            const trans = translator.load('jupyterlab');
            const iconContainer = index_js_.DOMUtils.findElement(node, ITEM_ICON_CLASS);
            const text = index_js_.DOMUtils.findElement(node, ITEM_TEXT_CLASS);
            const modified = index_js_.DOMUtils.findElement(node, ITEM_MODIFIED_CLASS);
            const fileSize = index_js_.DOMUtils.findElement(node, ITEM_FILE_SIZE_CLASS);
            const checkboxWrapper = index_js_.DOMUtils.findElement(node, CHECKBOX_WRAPPER_CLASS);
            const showFileCheckboxes = !(hiddenColumns === null || hiddenColumns === void 0 ? void 0 : hiddenColumns.has('is_selected'));
            if (checkboxWrapper && !showFileCheckboxes) {
                node.removeChild(checkboxWrapper);
            }
            else if (showFileCheckboxes && !checkboxWrapper) {
                const checkboxWrapper = this.createCheckboxWrapperNode();
                node.insertBefore(checkboxWrapper, iconContainer);
            }
            if (hiddenColumns === null || hiddenColumns === void 0 ? void 0 : hiddenColumns.has('last_modified')) {
                modified.classList.add(MODIFIED_COLUMN_HIDDEN);
            }
            else {
                modified.classList.remove(MODIFIED_COLUMN_HIDDEN);
            }
            if (hiddenColumns === null || hiddenColumns === void 0 ? void 0 : hiddenColumns.has('file_size')) {
                fileSize.classList.add(FILE_SIZE_COLUMN_HIDDEN);
            }
            else {
                fileSize.classList.remove(FILE_SIZE_COLUMN_HIDDEN);
            }
            // render the file item's icon
            ui_components_lib_index_js_.LabIcon.resolveElement({
                icon,
                iconClass: (0,ui_components_lib_index_js_.classes)(iconClass, 'jp-Icon'),
                container: iconContainer,
                className: ITEM_ICON_CLASS,
                stylesheet: 'listing'
            });
            let hoverText = trans.__('Name: %1', model.name);
            // add file size to pop up if its available
            if (model.size !== null && model.size !== undefined) {
                const fileSizeText = listing_Private.formatFileSize(model.size, 1, 1024);
                fileSize.textContent = fileSizeText;
                hoverText += trans.__('\nSize: %1', listing_Private.formatFileSize(model.size, 1, 1024));
            }
            else {
                fileSize.textContent = '';
            }
            if (model.path) {
                const dirname = coreutils_lib_index_js_.PathExt.dirname(model.path);
                if (dirname) {
                    hoverText += trans.__('\nPath: %1', dirname.substr(0, 50));
                    if (dirname.length > 50) {
                        hoverText += '...';
                    }
                }
            }
            if (model.created) {
                hoverText += trans.__('\nCreated: %1', coreutils_lib_index_js_.Time.format(new Date(model.created)));
            }
            if (model.last_modified) {
                hoverText += trans.__('\nModified: %1', coreutils_lib_index_js_.Time.format(new Date(model.last_modified)));
            }
            hoverText += trans.__('\nWritable: %1', model.writable);
            node.title = hoverText;
            node.setAttribute('data-file-type', name);
            if (model.name.startsWith('.')) {
                node.setAttribute('data-is-dot', 'true');
            }
            else {
                node.removeAttribute('data-is-dot');
            }
            // If an item is being edited currently, its text node is unavailable.
            const indices = !model.indices ? [] : model.indices;
            let highlightedName = dist_index_es6_js_.StringExt.highlight(model.name, indices, virtualdom_dist_index_es6_js_.h.mark);
            if (text) {
                virtualdom_dist_index_es6_js_.VirtualDOM.render(virtualdom_dist_index_es6_js_.h.span(highlightedName), text);
            }
            // Adds an aria-label to the checkbox element.
            const checkbox = checkboxWrapper === null || checkboxWrapper === void 0 ? void 0 : checkboxWrapper.querySelector('input[type="checkbox"]');
            if (checkbox) {
                let ariaLabel;
                if (fileType.contentType === 'directory') {
                    ariaLabel = selected
                        ? trans.__('Deselect directory "%1"', highlightedName)
                        : trans.__('Select directory "%1"', highlightedName);
                }
                else {
                    ariaLabel = selected
                        ? trans.__('Deselect file "%1"', highlightedName)
                        : trans.__('Select file "%1"', highlightedName);
                }
                checkbox.setAttribute('aria-label', ariaLabel);
                checkbox.checked = selected !== null && selected !== void 0 ? selected : false;
            }
            let modText = '';
            let modTitle = '';
            if (model.last_modified) {
                modText = coreutils_lib_index_js_.Time.formatHuman(new Date(model.last_modified));
                modTitle = coreutils_lib_index_js_.Time.format(new Date(model.last_modified));
            }
            modified.textContent = modText;
            modified.title = modTitle;
        }
        /**
         * Get the node containing the file name.
         *
         * @param node - A node created by [[createItemNode]].
         *
         * @returns The node containing the file name.
         */
        getNameNode(node) {
            return index_js_.DOMUtils.findElement(node, ITEM_TEXT_CLASS);
        }
        /**
         * Get the checkbox input element node.
         *
         * @param node A node created by [[createItemNode]] or
         * [[createHeaderItemNode]]
         *
         * @returns The checkbox node.
         */
        getCheckboxNode(node) {
            return node.querySelector(`.${CHECKBOX_WRAPPER_CLASS} input[type=checkbox]`);
        }
        /**
         * Create a drag image for an item.
         *
         * @param node - A node created by [[createItemNode]].
         *
         * @param count - The number of items being dragged.
         *
         * @param fileType - The file type of the item, if applicable.
         *
         * @returns An element to use as the drag image.
         */
        createDragImage(node, count, trans, fileType) {
            const dragImage = node.cloneNode(true);
            const modified = index_js_.DOMUtils.findElement(dragImage, ITEM_MODIFIED_CLASS);
            const icon = index_js_.DOMUtils.findElement(dragImage, ITEM_ICON_CLASS);
            dragImage.removeChild(modified);
            if (!fileType) {
                icon.textContent = '';
                icon.className = '';
            }
            else {
                icon.textContent = fileType.iconLabel || '';
                icon.className = fileType.iconClass || '';
            }
            icon.classList.add(DRAG_ICON_CLASS);
            if (count > 1) {
                const nameNode = index_js_.DOMUtils.findElement(dragImage, ITEM_TEXT_CLASS);
                nameNode.textContent = trans._n('%1 Item', '%1 Items', count);
            }
            return dragImage;
        }
        /**
         * Create a node for a header item.
         */
        createHeaderItemNode(label) {
            const node = document.createElement('div');
            const text = document.createElement('span');
            const icon = document.createElement('span');
            node.className = HEADER_ITEM_CLASS;
            text.className = HEADER_ITEM_TEXT_CLASS;
            icon.className = HEADER_ITEM_ICON_CLASS;
            text.textContent = label;
            node.appendChild(text);
            node.appendChild(icon);
            return node;
        }
    }
    DirListing.Renderer = Renderer;
    /**
     * The default `IRenderer` instance.
     */
    DirListing.defaultRenderer = new Renderer();
})(DirListing || (DirListing = {}));
/**
 * The namespace for the listing private data.
 */
var listing_Private;
(function (Private) {
    /**
     * Handle editing text on a node.
     *
     * @returns Boolean indicating whether the name changed.
     */
    function userInputForRename(text, edit, original) {
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
        return new Promise(resolve => {
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
                        // Put focus back on the text node. That way the user can, for
                        // example, press the keyboard shortcut to go back into edit mode,
                        // and it will work.
                        text.focus();
                        break;
                    default:
                        break;
                }
            };
        });
    }
    Private.userInputForRename = userInputForRename;
    /**
     * Sort a list of items by sort state as a new array.
     */
    function sort(items, state, sortNotebooksFirst = false) {
        const copy = Array.from(items);
        const reverse = state.direction === 'descending' ? 1 : -1;
        /**
         * Compares two items and returns whether they should have a fixed priority.
         * The fixed priority enables to always sort the directories above the other files. And to sort the notebook above other files if the `sortNotebooksFirst` is true.
         */
        function isPriorityOverridden(a, b) {
            if (sortNotebooksFirst) {
                return a.type !== b.type;
            }
            return (a.type === 'directory') !== (b.type === 'directory');
        }
        /**
         * Returns the priority of a file.
         */
        function getPriority(item) {
            if (item.type === 'directory') {
                return 2;
            }
            if (item.type === 'notebook' && sortNotebooksFirst) {
                return 1;
            }
            return 0;
        }
        function compare(compare) {
            return (a, b) => {
                // Group directory first, then notebooks, then files
                if (isPriorityOverridden(a, b)) {
                    return getPriority(b) - getPriority(a);
                }
                const compared = compare(a, b);
                if (compared !== 0) {
                    return compared * reverse;
                }
                // Default sorting is alphabetical ascending
                return a.name.localeCompare(b.name);
            };
        }
        if (state.key === 'last_modified') {
            // Sort by last modified
            copy.sort(compare((a, b) => {
                return (new Date(a.last_modified).getTime() -
                    new Date(b.last_modified).getTime());
            }));
        }
        else if (state.key === 'file_size') {
            // Sort by size
            copy.sort(compare((a, b) => {
                var _a, _b;
                return ((_a = a.size) !== null && _a !== void 0 ? _a : 0) - ((_b = b.size) !== null && _b !== void 0 ? _b : 0);
            }));
        }
        else {
            // Sort by name
            copy.sort(compare((a, b) => {
                return b.name.localeCompare(a.name);
            }));
        }
        return copy;
    }
    Private.sort = sort;
    /**
     * Get the index of the node at a client position, or `-1`.
     */
    function hitTestNodes(nodes, event) {
        return dist_index_es6_js_.ArrayExt.findFirstIndex(nodes, node => domutils_dist_index_es6_js_.ElementExt.hitTest(node, event.clientX, event.clientY) ||
            event.target === node);
    }
    Private.hitTestNodes = hitTestNodes;
    /**
     * Format bytes to human readable string.
     */
    function formatFileSize(bytes, decimalPoint, k) {
        // https://www.codexworld.com/how-to/convert-file-size-bytes-kb-mb-gb-javascript/
        if (bytes === 0) {
            return '0 B';
        }
        const dm = decimalPoint || 2;
        const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        if (i >= 0 && i < sizes.length) {
            return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
        }
        else {
            return String(bytes);
        }
    }
    Private.formatFileSize = formatFileSize;
    /**
     * Update an inline svg caret icon in a node.
     */
    function updateCaret(container, float, state) {
        if (state) {
            (state === 'down' ? ui_components_lib_index_js_.caretDownIcon : ui_components_lib_index_js_.caretUpIcon).element({
                container,
                tag: 'span',
                stylesheet: 'listingHeaderItem',
                float
            });
        }
        else {
            ui_components_lib_index_js_.LabIcon.remove(container);
            container.className = HEADER_ITEM_ICON_CLASS;
        }
    }
    Private.updateCaret = updateCaret;
})(listing_Private || (listing_Private = {}));

;// CONCATENATED MODULE: ../packages/filebrowser/lib/browser.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * The class name added to file browsers.
 */
const FILE_BROWSER_CLASS = 'jp-FileBrowser';
/**
 * The class name added to file browser panel (gather filter, breadcrumbs and listing).
 */
const FILE_BROWSER_PANEL_CLASS = 'jp-FileBrowser-Panel';
/**
 * The class name added to the filebrowser crumbs node.
 */
const CRUMBS_CLASS = 'jp-FileBrowser-crumbs';
/**
 * The class name added to the filebrowser toolbar node.
 */
const TOOLBAR_CLASS = 'jp-FileBrowser-toolbar';
/**
 * The class name added to the filebrowser listing node.
 */
const LISTING_CLASS = 'jp-FileBrowser-listing';
/**
 * A widget which hosts a file browser.
 *
 * The widget uses the Jupyter Contents API to retrieve contents,
 * and presents itself as a flat list of files and directories with
 * breadcrumbs.
 */
class FileBrowser extends ui_components_lib_index_js_.SidePanel {
    /**
     * Construct a new file browser.
     *
     * @param options - The file browser options.
     */
    constructor(options) {
        var _a;
        super({ content: new index_es6_js_.Panel(), translator: options.translator });
        this._directoryPending = null;
        this._filePending = null;
        this._showLastModifiedColumn = true;
        this._showFileSizeColumn = false;
        this._showHiddenFiles = false;
        this._showFileCheckboxes = false;
        this._sortNotebooksFirst = false;
        this.addClass(FILE_BROWSER_CLASS);
        this.toolbar.addClass(TOOLBAR_CLASS);
        this.id = options.id;
        const translator = (this.translator = (_a = options.translator) !== null && _a !== void 0 ? _a : translation_lib_index_js_.nullTranslator);
        const model = (this.model = options.model);
        const renderer = options.renderer;
        model.connectionFailure.connect(this._onConnectionFailure, this);
        this._manager = model.manager;
        // a11y
        this.toolbar.node.setAttribute('role', 'navigation');
        this.toolbar.node.setAttribute('aria-label', this._trans.__('file browser'));
        // File browser widgets container
        this.mainPanel = new index_es6_js_.Panel();
        this.mainPanel.addClass(FILE_BROWSER_PANEL_CLASS);
        this.mainPanel.title.label = this._trans.__('File Browser');
        this.crumbs = new BreadCrumbs({ model, translator });
        this.crumbs.addClass(CRUMBS_CLASS);
        this.listing = this.createDirListing({
            model,
            renderer,
            translator
        });
        this.listing.addClass(LISTING_CLASS);
        this.mainPanel.addWidget(this.crumbs);
        this.mainPanel.addWidget(this.listing);
        this.addWidget(this.mainPanel);
        if (options.restore !== false) {
            void model.restore(this.id);
        }
    }
    /**
     * Whether to show active file in file browser
     */
    get navigateToCurrentDirectory() {
        return this._navigateToCurrentDirectory;
    }
    set navigateToCurrentDirectory(value) {
        this._navigateToCurrentDirectory = value;
    }
    /**
     * Whether to show the last modified column
     */
    get showLastModifiedColumn() {
        return this._showLastModifiedColumn;
    }
    set showLastModifiedColumn(value) {
        if (this.listing.setColumnVisibility) {
            this.listing.setColumnVisibility('last_modified', value);
            this._showLastModifiedColumn = value;
        }
        else {
            console.warn('Listing does not support toggling column visibility');
        }
    }
    /**
     * Whether to show the file size column
     */
    get showFileSizeColumn() {
        return this._showFileSizeColumn;
    }
    set showFileSizeColumn(value) {
        if (this.listing.setColumnVisibility) {
            this.listing.setColumnVisibility('file_size', value);
            this._showFileSizeColumn = value;
        }
        else {
            console.warn('Listing does not support toggling column visibility');
        }
    }
    /**
     * Whether to show hidden files
     */
    get showHiddenFiles() {
        return this._showHiddenFiles;
    }
    set showHiddenFiles(value) {
        this.model.showHiddenFiles(value);
        this._showHiddenFiles = value;
    }
    /**
     * Whether to show checkboxes next to files and folders
     */
    get showFileCheckboxes() {
        return this._showFileCheckboxes;
    }
    set showFileCheckboxes(value) {
        if (this.listing.setColumnVisibility) {
            this.listing.setColumnVisibility('is_selected', value);
            this._showFileCheckboxes = value;
        }
        else {
            console.warn('Listing does not support toggling column visibility');
        }
    }
    /**
     * Whether to sort notebooks above other files
     */
    get sortNotebooksFirst() {
        return this._sortNotebooksFirst;
    }
    set sortNotebooksFirst(value) {
        if (this.listing.setNotebooksFirstSorting) {
            this.listing.setNotebooksFirstSorting(value);
            this._sortNotebooksFirst = value;
        }
        else {
            console.warn('Listing does not support sorting notebooks first');
        }
    }
    /**
     * Create an iterator over the listing's selected items.
     *
     * @returns A new iterator over the listing's selected items.
     */
    selectedItems() {
        return this.listing.selectedItems();
    }
    /**
     * Select an item by name.
     *
     * @param name - The name of the item to select.
     */
    async selectItemByName(name) {
        await this.listing.selectItemByName(name);
    }
    clearSelectedItems() {
        this.listing.clearSelectedItems();
    }
    /**
     * Rename the first currently selected item.
     *
     * @returns A promise that resolves with the new name of the item.
     */
    rename() {
        return this.listing.rename();
    }
    /**
     * Cut the selected items.
     */
    cut() {
        this.listing.cut();
    }
    /**
     * Copy the selected items.
     */
    copy() {
        this.listing.copy();
    }
    /**
     * Paste the items from the clipboard.
     *
     * @returns A promise that resolves when the operation is complete.
     */
    paste() {
        return this.listing.paste();
    }
    async _createNew(options) {
        try {
            const model = await this._manager.newUntitled(options);
            await this.listing.selectItemByName(model.name, true);
            await this.rename();
            return model;
        }
        catch (err) {
            void (0,index_js_.showErrorMessage)(this._trans.__('Error'), err);
            throw err;
        }
    }
    /**
     * Create a new directory
     */
    async createNewDirectory() {
        if (this._directoryPending) {
            return this._directoryPending;
        }
        this._directoryPending = this._createNew({
            path: this.model.path,
            type: 'directory'
        });
        try {
            return await this._directoryPending;
        }
        finally {
            this._directoryPending = null;
        }
    }
    /**
     * Create a new file
     */
    async createNewFile(options) {
        if (this._filePending) {
            return this._filePending;
        }
        this._filePending = this._createNew({
            path: this.model.path,
            type: 'file',
            ext: options.ext
        });
        try {
            return await this._filePending;
        }
        finally {
            this._filePending = null;
        }
    }
    /**
     * Delete the currently selected item(s).
     *
     * @returns A promise that resolves when the operation is complete.
     */
    delete() {
        return this.listing.delete();
    }
    /**
     * Duplicate the currently selected item(s).
     *
     * @returns A promise that resolves when the operation is complete.
     */
    duplicate() {
        return this.listing.duplicate();
    }
    /**
     * Download the currently selected item(s).
     */
    download() {
        return this.listing.download();
    }
    /**
     * cd ..
     *
     * Go up one level in the directory tree.
     */
    async goUp() {
        return this.listing.goUp();
    }
    /**
     * Shut down kernels on the applicable currently selected items.
     *
     * @returns A promise that resolves when the operation is complete.
     */
    shutdownKernels() {
        return this.listing.shutdownKernels();
    }
    /**
     * Select next item.
     */
    selectNext() {
        this.listing.selectNext();
    }
    /**
     * Select previous item.
     */
    selectPrevious() {
        this.listing.selectPrevious();
    }
    /**
     * Find a model given a click.
     *
     * @param event - The mouse event.
     *
     * @returns The model for the selected file.
     */
    modelForClick(event) {
        return this.listing.modelForClick(event);
    }
    /**
     * Create the underlying DirListing instance.
     *
     * @param options - The DirListing constructor options.
     *
     * @returns The created DirListing instance.
     */
    createDirListing(options) {
        return new DirListing(options);
    }
    /**
     * Handle a connection lost signal from the model.
     */
    _onConnectionFailure(sender, args) {
        if (args instanceof lib_index_js_.ServerConnection.ResponseError &&
            args.response.status === 404) {
            const title = this._trans.__('Directory not found');
            args.message = this._trans.__('Directory not found: "%1"', this.model.path);
            void (0,index_js_.showErrorMessage)(title, args);
        }
    }
}

// EXTERNAL MODULE: consume shared module (default) @lumino/polling@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/polling/dist/index.es6.js)
var polling_dist_index_es6_js_ = __webpack_require__(81967);
;// CONCATENATED MODULE: ../packages/filebrowser/lib/model.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * The default duration of the auto-refresh in ms
 */
const DEFAULT_REFRESH_INTERVAL = 10000;
/**
 * The maximum upload size (in bytes) for notebook version < 5.1.0
 */
const LARGE_FILE_SIZE = 15 * 1024 * 1024;
/**
 * The size (in bytes) of the biggest chunk we should upload at once.
 */
const CHUNK_SIZE = 1024 * 1024;
/**
 * An implementation of a file browser model.
 *
 * #### Notes
 * All paths parameters without a leading `'/'` are interpreted as relative to
 * the current directory.  Supports `'../'` syntax.
 */
class FileBrowserModel {
    /**
     * Construct a new file browser model.
     */
    constructor(options) {
        var _a;
        this._connectionFailure = new signaling_dist_index_es6_js_.Signal(this);
        this._fileChanged = new signaling_dist_index_es6_js_.Signal(this);
        this._items = [];
        this._key = '';
        this._pathChanged = new signaling_dist_index_es6_js_.Signal(this);
        this._paths = new Set();
        this._pending = null;
        this._pendingPath = null;
        this._refreshed = new signaling_dist_index_es6_js_.Signal(this);
        this._sessions = [];
        this._state = null;
        this._isDisposed = false;
        this._restored = new dist_index_js_.PromiseDelegate();
        this._uploads = [];
        this._uploadChanged = new signaling_dist_index_es6_js_.Signal(this);
        this.manager = options.manager;
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._driveName = options.driveName || '';
        this._model = {
            path: this.rootPath,
            name: coreutils_lib_index_js_.PathExt.basename(this.rootPath),
            type: 'directory',
            content: undefined,
            writable: false,
            created: 'unknown',
            last_modified: 'unknown',
            mimetype: 'text/plain',
            format: 'text'
        };
        this._state = options.state || null;
        const refreshInterval = options.refreshInterval || DEFAULT_REFRESH_INTERVAL;
        const { services } = options.manager;
        services.contents.fileChanged.connect(this.onFileChanged, this);
        services.sessions.runningChanged.connect(this.onRunningChanged, this);
        this._unloadEventListener = (e) => {
            if (this._uploads.length > 0) {
                const confirmationMessage = this._trans.__('Files still uploading');
                e.returnValue = confirmationMessage;
                return confirmationMessage;
            }
        };
        window.addEventListener('beforeunload', this._unloadEventListener);
        this._poll = new polling_dist_index_es6_js_.Poll({
            auto: (_a = options.auto) !== null && _a !== void 0 ? _a : true,
            name: '@jupyterlab/filebrowser:Model',
            factory: () => this.cd('.'),
            frequency: {
                interval: refreshInterval,
                backoff: true,
                max: 300 * 1000
            },
            standby: options.refreshStandby || 'when-hidden'
        });
    }
    /**
     * A signal emitted when the file browser model loses connection.
     */
    get connectionFailure() {
        return this._connectionFailure;
    }
    /**
     * The drive name that gets prepended to the path.
     */
    get driveName() {
        return this._driveName;
    }
    /**
     * A promise that resolves when the model is first restored.
     */
    get restored() {
        return this._restored.promise;
    }
    /**
     * Get the file path changed signal.
     */
    get fileChanged() {
        return this._fileChanged;
    }
    /**
     * Get the current path.
     */
    get path() {
        return this._model ? this._model.path : '';
    }
    /**
     * Get the root path
     */
    get rootPath() {
        return this._driveName ? this._driveName + ':' : '';
    }
    /**
     * A signal emitted when the path changes.
     */
    get pathChanged() {
        return this._pathChanged;
    }
    /**
     * A signal emitted when the directory listing is refreshed.
     */
    get refreshed() {
        return this._refreshed;
    }
    /**
     * Get the kernel spec models.
     */
    get specs() {
        return this.manager.services.kernelspecs.specs;
    }
    /**
     * Get whether the model is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * A signal emitted when an upload progresses.
     */
    get uploadChanged() {
        return this._uploadChanged;
    }
    /**
     * Create an iterator over the status of all in progress uploads.
     */
    uploads() {
        return this._uploads[Symbol.iterator]();
    }
    /**
     * Dispose of the resources held by the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        window.removeEventListener('beforeunload', this._unloadEventListener);
        this._isDisposed = true;
        this._poll.dispose();
        this._sessions.length = 0;
        this._items.length = 0;
        signaling_dist_index_es6_js_.Signal.clearData(this);
    }
    /**
     * Create an iterator over the model's items.
     *
     * @returns A new iterator over the model's items.
     */
    items() {
        return this._items[Symbol.iterator]();
    }
    /**
     * Create an iterator over the active sessions in the directory.
     *
     * @returns A new iterator over the model's active sessions.
     */
    sessions() {
        return this._sessions[Symbol.iterator]();
    }
    /**
     * Force a refresh of the directory contents.
     */
    async refresh() {
        await this._poll.refresh();
        await this._poll.tick;
        this._refreshed.emit(void 0);
    }
    /**
     * Change directory.
     *
     * @param path - The path to the file or directory.
     *
     * @returns A promise with the contents of the directory.
     */
    async cd(newValue = '.') {
        if (newValue !== '.') {
            newValue = this.manager.services.contents.resolvePath(this._model.path, newValue);
        }
        else {
            newValue = this._pendingPath || this._model.path;
        }
        if (this._pending) {
            // Collapse requests to the same directory.
            if (newValue === this._pendingPath) {
                return this._pending;
            }
            // Otherwise wait for the pending request to complete before continuing.
            await this._pending;
        }
        const oldValue = this.path;
        const options = { content: true };
        this._pendingPath = newValue;
        if (oldValue !== newValue) {
            this._sessions.length = 0;
        }
        const services = this.manager.services;
        this._pending = services.contents
            .get(newValue, options)
            .then(contents => {
            if (this.isDisposed) {
                return;
            }
            this.handleContents(contents);
            this._pendingPath = null;
            this._pending = null;
            if (oldValue !== newValue) {
                // If there is a state database and a unique key, save the new path.
                // We don't need to wait on the save to continue.
                if (this._state && this._key) {
                    void this._state.save(this._key, { path: newValue });
                }
                this._pathChanged.emit({
                    name: 'path',
                    oldValue,
                    newValue
                });
            }
            this.onRunningChanged(services.sessions, services.sessions.running());
            this._refreshed.emit(void 0);
        })
            .catch(error => {
            this._pendingPath = null;
            this._pending = null;
            if (error.response &&
                error.response.status === 404 &&
                newValue !== '/') {
                error.message = this._trans.__('Directory not found: "%1"', this._model.path);
                console.error(error);
                this._connectionFailure.emit(error);
                return this.cd('/');
            }
            else {
                this._connectionFailure.emit(error);
            }
        });
        return this._pending;
    }
    /**
     * Download a file.
     *
     * @param path - The path of the file to be downloaded.
     *
     * @returns A promise which resolves when the file has begun
     *   downloading.
     */
    async download(path) {
        const url = await this.manager.services.contents.getDownloadUrl(path);
        const element = document.createElement('a');
        element.href = url;
        element.download = '';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
        return void 0;
    }
    /**
     * Restore the state of the file browser.
     *
     * @param id - The unique ID that is used to construct a state database key.
     *
     * @param populate - If `false`, the restoration ID will be set but the file
     * browser state will not be fetched from the state database.
     *
     * @returns A promise when restoration is complete.
     *
     * #### Notes
     * This function will only restore the model *once*. If it is called multiple
     * times, all subsequent invocations are no-ops.
     */
    async restore(id, populate = true) {
        const { manager } = this;
        const key = `file-browser-${id}:cwd`;
        const state = this._state;
        const restored = !!this._key;
        if (restored) {
            return;
        }
        // Set the file browser key for state database fetch/save.
        this._key = key;
        if (!populate || !state) {
            this._restored.resolve(undefined);
            return;
        }
        await manager.services.ready;
        try {
            const value = await state.fetch(key);
            if (!value) {
                this._restored.resolve(undefined);
                return;
            }
            const path = value['path'];
            // need to return to root path if preferred dir is set
            if (path) {
                await this.cd('/');
            }
            const localPath = manager.services.contents.localPath(path);
            await manager.services.contents.get(path);
            await this.cd(localPath);
        }
        catch (error) {
            await state.remove(key);
        }
        this._restored.resolve(undefined);
    }
    /**
     * Upload a `File` object.
     *
     * @param file - The `File` object to upload.
     *
     * @returns A promise containing the new file contents model.
     *
     * #### Notes
     * On Notebook version < 5.1.0, this will fail to upload files that are too
     * big to be sent in one request to the server. On newer versions, or on
     * Jupyter Server, it will ask for confirmation then upload the file in 1 MB
     * chunks.
     */
    async upload(file) {
        // We do not support Jupyter Notebook version less than 4, and Jupyter
        // Server advertises itself as version 1 and supports chunked
        // uploading. We assume any version less than 4.0.0 to be Jupyter Server
        // instead of Jupyter Notebook.
        const serverVersion = coreutils_lib_index_js_.PageConfig.getNotebookVersion();
        const supportsChunked = serverVersion < [4, 0, 0] /* Jupyter Server */ ||
            serverVersion >= [5, 1, 0]; /* Jupyter Notebook >= 5.1.0 */
        const largeFile = file.size > LARGE_FILE_SIZE;
        if (largeFile && !supportsChunked) {
            const msg = this._trans.__('Cannot upload file (>%1 MB). %2', LARGE_FILE_SIZE / (1024 * 1024), file.name);
            console.warn(msg);
            throw msg;
        }
        const err = 'File not uploaded';
        if (largeFile && !(await this._shouldUploadLarge(file))) {
            throw 'Cancelled large file upload';
        }
        await this._uploadCheckDisposed();
        await this.refresh();
        await this._uploadCheckDisposed();
        if (this._items.find(i => i.name === file.name) &&
            !(await (0,docmanager_lib_index_js_.shouldOverwrite)(file.name))) {
            throw err;
        }
        await this._uploadCheckDisposed();
        const chunkedUpload = supportsChunked && file.size > CHUNK_SIZE;
        return await this._upload(file, chunkedUpload);
    }
    async _shouldUploadLarge(file) {
        const { button } = await (0,index_js_.showDialog)({
            title: this._trans.__('Large file size warning'),
            body: this._trans.__('The file size is %1 MB. Do you still want to upload it?', Math.round(file.size / (1024 * 1024))),
            buttons: [
                index_js_.Dialog.cancelButton({ label: this._trans.__('Cancel') }),
                index_js_.Dialog.warnButton({ label: this._trans.__('Upload') })
            ]
        });
        return button.accept;
    }
    /**
     * Perform the actual upload.
     */
    async _upload(file, chunked) {
        // Gather the file model parameters.
        let path = this._model.path;
        path = path ? path + '/' + file.name : file.name;
        const name = file.name;
        const type = 'file';
        const format = 'base64';
        const uploadInner = async (blob, chunk) => {
            await this._uploadCheckDisposed();
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            await new Promise((resolve, reject) => {
                reader.onload = resolve;
                reader.onerror = event => reject(`Failed to upload "${file.name}":` + event);
            });
            await this._uploadCheckDisposed();
            // remove header https://stackoverflow.com/a/24289420/907060
            const content = reader.result.split(',')[1];
            const model = {
                type,
                format,
                name,
                chunk,
                content
            };
            return await this.manager.services.contents.save(path, model);
        };
        if (!chunked) {
            try {
                return await uploadInner(file);
            }
            catch (err) {
                dist_index_es6_js_.ArrayExt.removeFirstWhere(this._uploads, uploadIndex => {
                    return file.name === uploadIndex.path;
                });
                throw err;
            }
        }
        let finalModel;
        let upload = { path, progress: 0 };
        this._uploadChanged.emit({
            name: 'start',
            newValue: upload,
            oldValue: null
        });
        for (let start = 0; !finalModel; start += CHUNK_SIZE) {
            const end = start + CHUNK_SIZE;
            const lastChunk = end >= file.size;
            const chunk = lastChunk ? -1 : end / CHUNK_SIZE;
            const newUpload = { path, progress: start / file.size };
            this._uploads.splice(this._uploads.indexOf(upload));
            this._uploads.push(newUpload);
            this._uploadChanged.emit({
                name: 'update',
                newValue: newUpload,
                oldValue: upload
            });
            upload = newUpload;
            let currentModel;
            try {
                currentModel = await uploadInner(file.slice(start, end), chunk);
            }
            catch (err) {
                dist_index_es6_js_.ArrayExt.removeFirstWhere(this._uploads, uploadIndex => {
                    return file.name === uploadIndex.path;
                });
                this._uploadChanged.emit({
                    name: 'failure',
                    newValue: upload,
                    oldValue: null
                });
                throw err;
            }
            if (lastChunk) {
                finalModel = currentModel;
            }
        }
        this._uploads.splice(this._uploads.indexOf(upload));
        this._uploadChanged.emit({
            name: 'finish',
            newValue: null,
            oldValue: upload
        });
        return finalModel;
    }
    _uploadCheckDisposed() {
        if (this.isDisposed) {
            return Promise.reject('Filemanager disposed. File upload canceled');
        }
        return Promise.resolve();
    }
    /**
     * Handle an updated contents model.
     */
    handleContents(contents) {
        // Update our internal data.
        this._model = {
            name: contents.name,
            path: contents.path,
            type: contents.type,
            content: undefined,
            writable: contents.writable,
            created: contents.created,
            last_modified: contents.last_modified,
            size: contents.size,
            mimetype: contents.mimetype,
            format: contents.format
        };
        this._items = contents.content;
        this._paths.clear();
        contents.content.forEach((model) => {
            this._paths.add(model.path);
        });
    }
    /**
     * Handle a change to the running sessions.
     */
    onRunningChanged(sender, models) {
        this._populateSessions(models);
        this._refreshed.emit(void 0);
    }
    /**
     * Handle a change on the contents manager.
     */
    onFileChanged(sender, change) {
        const path = this._model.path;
        const { sessions } = this.manager.services;
        const { oldValue, newValue } = change;
        const value = oldValue && oldValue.path && coreutils_lib_index_js_.PathExt.dirname(oldValue.path) === path
            ? oldValue
            : newValue && newValue.path && coreutils_lib_index_js_.PathExt.dirname(newValue.path) === path
                ? newValue
                : undefined;
        // If either the old value or the new value is in the current path, update.
        if (value) {
            void this._poll.refresh();
            this._populateSessions(sessions.running());
            this._fileChanged.emit(change);
            return;
        }
    }
    /**
     * Populate the model's sessions collection.
     */
    _populateSessions(models) {
        this._sessions.length = 0;
        for (const model of models) {
            if (this._paths.has(model.path)) {
                this._sessions.push(model);
            }
        }
    }
}
/**
 * File browser model where hidden files inclusion can be toggled on/off.
 */
class TogglableHiddenFileBrowserModel extends FileBrowserModel {
    constructor(options) {
        super(options);
        this._includeHiddenFiles = options.includeHiddenFiles || false;
    }
    /**
     * Create an iterator over the model's items filtering hidden files out if necessary.
     *
     * @returns A new iterator over the model's items.
     */
    items() {
        return this._includeHiddenFiles
            ? super.items()
            : (0,dist_index_es6_js_.filter)(super.items(), value => !value.name.startsWith('.'));
    }
    /**
     * Set the inclusion of hidden files. Triggers a model refresh.
     */
    showHiddenFiles(value) {
        this._includeHiddenFiles = value;
        void this.refresh();
    }
}
/**
 * File browser model with optional filter on element.
 */
class FilterFileBrowserModel extends TogglableHiddenFileBrowserModel {
    constructor(options) {
        var _a, _b;
        super(options);
        this._filter =
            (_a = options.filter) !== null && _a !== void 0 ? _a : (model => {
                return {};
            });
        this._filterDirectories = (_b = options.filterDirectories) !== null && _b !== void 0 ? _b : true;
    }
    /**
     * Whether to filter directories.
     */
    get filterDirectories() {
        return this._filterDirectories;
    }
    set filterDirectories(value) {
        this._filterDirectories = value;
    }
    /**
     * Create an iterator over the filtered model's items.
     *
     * @returns A new iterator over the model's items.
     */
    items() {
        return (0,dist_index_es6_js_.filter)(super.items(), value => {
            if (!this._filterDirectories && value.type === 'directory') {
                return true;
            }
            else {
                const filtered = this._filter(value);
                value.indices = filtered === null || filtered === void 0 ? void 0 : filtered.indices;
                return !!filtered;
            }
        });
    }
    setFilter(filter) {
        this._filter = filter;
        void this.refresh();
    }
}

;// CONCATENATED MODULE: ../packages/filebrowser/lib/opendialog.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * The class name added to open file dialog
 */
const OPEN_DIALOG_CLASS = 'jp-Open-Dialog';
/**
 * Namespace for file dialog
 */
var FileDialog;
(function (FileDialog) {
    /**
     * Create and show a open files dialog.
     *
     * Note: if nothing is selected when `getValue` will return the browser
     * model current path.
     *
     * @param options - The dialog setup options.
     *
     * @returns A promise that resolves with whether the dialog was accepted.
     */
    function getOpenFiles(options) {
        const translator = options.translator || translation_lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        const dialogOptions = {
            title: options.title,
            buttons: [
                index_js_.Dialog.cancelButton(),
                index_js_.Dialog.okButton({
                    label: trans.__('Select')
                })
            ],
            focusNodeSelector: options.focusNodeSelector,
            host: options.host,
            renderer: options.renderer,
            body: new OpenDialog(options.manager, options.filter, translator)
        };
        const dialog = new index_js_.Dialog(dialogOptions);
        return dialog.launch();
    }
    FileDialog.getOpenFiles = getOpenFiles;
    /**
     * Create and show a open directory dialog.
     *
     * Note: if nothing is selected when `getValue` will return the browser
     * model current path.
     *
     * @param options - The dialog setup options.
     *
     * @returns A promise that resolves with whether the dialog was accepted.
     */
    function getExistingDirectory(options) {
        return getOpenFiles({
            ...options,
            filter: model => {
                return model.type === 'directory' ? {} : null;
            }
        });
    }
    FileDialog.getExistingDirectory = getExistingDirectory;
})(FileDialog || (FileDialog = {}));
/**
 * Open dialog widget
 */
class OpenDialog extends index_es6_js_.Widget {
    constructor(manager, filter, translator, filterDirectories) {
        super();
        translator = translator !== null && translator !== void 0 ? translator : translation_lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        this.addClass(OPEN_DIALOG_CLASS);
        this._browser = opendialog_Private.createFilteredFileBrowser('filtered-file-browser-dialog', manager, filter, {}, translator, filterDirectories);
        // Add toolbar items
        (0,index_js_.setToolbar)(this._browser, (browser) => [
            {
                name: 'new-folder',
                widget: new index_js_.ToolbarButton({
                    icon: ui_components_lib_index_js_.newFolderIcon,
                    onClick: () => {
                        void browser.createNewDirectory();
                    },
                    tooltip: trans.__('New Folder')
                })
            },
            {
                name: 'refresher',
                widget: new index_js_.ToolbarButton({
                    icon: ui_components_lib_index_js_.refreshIcon,
                    onClick: () => {
                        browser.model.refresh().catch(reason => {
                            console.error('Failed to refresh file browser in open dialog.', reason);
                        });
                    },
                    tooltip: trans.__('Refresh File List')
                })
            }
        ]);
        // Build the sub widgets
        const layout = new index_es6_js_.PanelLayout();
        layout.addWidget(this._browser);
        // Set Widget content
        this.layout = layout;
    }
    /**
     * Get the selected items.
     */
    getValue() {
        const selection = Array.from(this._browser.selectedItems());
        if (selection.length === 0) {
            // Return current path
            return [
                {
                    path: this._browser.model.path,
                    name: coreutils_lib_index_js_.PathExt.basename(this._browser.model.path),
                    type: 'directory',
                    content: undefined,
                    writable: false,
                    created: 'unknown',
                    last_modified: 'unknown',
                    mimetype: 'text/plain',
                    format: 'text'
                }
            ];
        }
        else {
            return selection;
        }
    }
}
var opendialog_Private;
(function (Private) {
    /**
     * Create a new file browser instance.
     *
     * @param id - The widget/DOM id of the file browser.
     *
     * @param manager - A document manager instance.
     *
     * @param filter - function to filter file browser item.
     *
     * @param options - The optional file browser configuration object.
     *
     * #### Notes
     * The ID parameter is used to set the widget ID. It is also used as part of
     * the unique key necessary to store the file browser's restoration data in
     * the state database if that functionality is enabled.
     *
     * If, after the file browser has been generated by the factory, the ID of the
     * resulting widget is changed by client code, the restoration functionality
     * will not be disrupted as long as there are no ID collisions, i.e., as long
     * as the initial ID passed into the factory is used for only one file browser
     * instance.
     */
    Private.createFilteredFileBrowser = (id, manager, filter, options = {}, translator, filterDirectories) => {
        translator = translator || translation_lib_index_js_.nullTranslator;
        const model = new FilterFileBrowserModel({
            manager,
            filter,
            translator,
            driveName: options.driveName,
            refreshInterval: options.refreshInterval,
            filterDirectories
        });
        const widget = new FileBrowser({
            id,
            model,
            translator
        });
        return widget;
    };
})(opendialog_Private || (opendialog_Private = {}));

;// CONCATENATED MODULE: ../packages/filebrowser/lib/tokens.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The file browser factory token.
 */
const IFileBrowserFactory = new dist_index_js_.Token('@jupyterlab/filebrowser:IFileBrowserFactory', `A factory object that creates file browsers.
  Use this if you want to create your own file browser (e.g., for a custom storage backend),
  or to interact with other file browsers that have been created by extensions.`);
/**
 * The default file browser token.
 */
const IDefaultFileBrowser = new dist_index_js_.Token('@jupyterlab/filebrowser:IDefaultFileBrowser', 'A service for the default file browser.');
/**
 * The token that indicates the default file browser commands are loaded.
 */
const IFileBrowserCommands = new dist_index_js_.Token('@jupyterlab/filebrowser:IFileBrowserCommands', 'A token to ensure file browser commands are loaded.');

;// CONCATENATED MODULE: ../packages/filebrowser/lib/upload.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A widget which provides an upload button.
 */
class Uploader extends ui_components_lib_index_js_.ToolbarButton {
    /**
     * Construct a new file browser buttons widget.
     */
    constructor(options) {
        super({
            icon: ui_components_lib_index_js_.fileUploadIcon,
            label: options.label,
            onClick: () => {
                this._input.click();
            },
            tooltip: upload_Private.translateToolTip(options.translator)
        });
        /**
         * The 'change' handler for the input field.
         */
        this._onInputChanged = () => {
            const files = Array.prototype.slice.call(this._input.files);
            const pending = files.map(file => this.fileBrowserModel.upload(file));
            void Promise.all(pending).catch(error => {
                void (0,index_js_.showErrorMessage)(this._trans._p('showErrorMessage', 'Upload Error'), error);
            });
        };
        /**
         * The 'click' handler for the input field.
         */
        this._onInputClicked = () => {
            // In order to allow repeated uploads of the same file (with delete in between),
            // we need to clear the input value to trigger a change event.
            this._input.value = '';
        };
        this._input = upload_Private.createUploadInput();
        this.fileBrowserModel = options.model;
        this.translator = options.translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._input.onclick = this._onInputClicked;
        this._input.onchange = this._onInputChanged;
        this.addClass('jp-id-upload');
    }
}
/**
 * The namespace for module private data.
 */
var upload_Private;
(function (Private) {
    /**
     * Create the upload input node for a file buttons widget.
     */
    function createUploadInput() {
        const input = document.createElement('input');
        input.type = 'file';
        input.multiple = true;
        return input;
    }
    Private.createUploadInput = createUploadInput;
    /**
     * Translate upload tooltip.
     */
    function translateToolTip(translator) {
        translator = translator || translation_lib_index_js_.nullTranslator;
        const trans = translator.load('jupyterlab');
        return trans.__('Upload Files');
    }
    Private.translateToolTip = translateToolTip;
})(upload_Private || (upload_Private = {}));

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/statusbar@~4.1.0-alpha.2 (singleton) (fallback: ../packages/statusbar/lib/index.js)
var statusbar_lib_index_js_ = __webpack_require__(34853);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
;// CONCATENATED MODULE: ../packages/filebrowser/lib/uploadstatus.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
//





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
    const translator = props.translator || translation_lib_index_js_.nullTranslator;
    const trans = translator.load('jupyterlab');
    return (react_index_js_default().createElement(statusbar_lib_index_js_.GroupItem, { spacing: HALF_SPACING },
        react_index_js_default().createElement(statusbar_lib_index_js_.TextItem, { source: trans.__('Uploading…') }),
        react_index_js_default().createElement(statusbar_lib_index_js_.ProgressBar, { percentage: props.upload })));
}
/**
 * The time for which to show the "Complete!" message after uploading.
 */
const UPLOAD_COMPLETE_MESSAGE_MILLIS = 2000;
/**
 * Status bar item to display file upload progress.
 */
class FileUploadStatus extends ui_components_lib_index_js_.VDomRenderer {
    /**
     * Construct a new FileUpload status item.
     */
    constructor(opts) {
        super(new FileUploadStatus.Model(opts.tracker.currentWidget && opts.tracker.currentWidget.model));
        this._onBrowserChange = (tracker, browser) => {
            if (browser === null) {
                this.model.browserModel = null;
            }
            else {
                this.model.browserModel = browser.model;
            }
        };
        this.translator = opts.translator || translation_lib_index_js_.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._tracker = opts.tracker;
        this._tracker.currentChanged.connect(this._onBrowserChange);
    }
    /**
     * Render the FileUpload status.
     */
    render() {
        const uploadPaths = this.model.items;
        if (uploadPaths.length > 0) {
            const item = this.model.items[0];
            if (item.complete) {
                return react_index_js_default().createElement(statusbar_lib_index_js_.TextItem, { source: this._trans.__('Complete!') });
            }
            else {
                return (react_index_js_default().createElement(FileUploadComponent, { upload: this.model.items[0].progress, translator: this.translator }));
            }
        }
        else {
            return react_index_js_default().createElement(FileUploadComponent, { upload: 100, translator: this.translator });
        }
    }
    dispose() {
        super.dispose();
        this._tracker.currentChanged.disconnect(this._onBrowserChange);
    }
}
/**
 * A namespace for FileUpload class statics.
 */
(function (FileUploadStatus) {
    /**
     * The VDomModel for the FileUpload renderer.
     */
    class Model extends ui_components_lib_index_js_.VDomModel {
        /**
         * Construct a new model.
         */
        constructor(browserModel) {
            super();
            /**
             * Handle an uploadChanged event in the filebrowser model.
             */
            this._uploadChanged = (browse, uploads) => {
                if (uploads.name === 'start') {
                    this._items.push({
                        path: uploads.newValue.path,
                        progress: uploads.newValue.progress * 100,
                        complete: false
                    });
                }
                else if (uploads.name === 'update') {
                    const idx = dist_index_es6_js_.ArrayExt.findFirstIndex(this._items, val => val.path === uploads.oldValue.path);
                    if (idx !== -1) {
                        this._items[idx].progress = uploads.newValue.progress * 100;
                    }
                }
                else if (uploads.name === 'finish') {
                    const finishedItem = dist_index_es6_js_.ArrayExt.findFirstValue(this._items, val => val.path === uploads.oldValue.path);
                    if (finishedItem) {
                        finishedItem.complete = true;
                        setTimeout(() => {
                            dist_index_es6_js_.ArrayExt.removeFirstOf(this._items, finishedItem);
                            this.stateChanged.emit(void 0);
                        }, UPLOAD_COMPLETE_MESSAGE_MILLIS);
                    }
                }
                else if (uploads.name === 'failure') {
                    dist_index_es6_js_.ArrayExt.removeFirstWhere(this._items, val => val.path === uploads.newValue.path);
                }
                this.stateChanged.emit(void 0);
            };
            this._items = [];
            this._browserModel = null;
            this.browserModel = browserModel;
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
        get browserModel() {
            return this._browserModel;
        }
        set browserModel(browserModel) {
            const oldBrowserModel = this._browserModel;
            if (oldBrowserModel) {
                oldBrowserModel.uploadChanged.disconnect(this._uploadChanged);
            }
            this._browserModel = browserModel;
            this._items = [];
            if (this._browserModel !== null) {
                this._browserModel.uploadChanged.connect(this._uploadChanged);
            }
            this.stateChanged.emit(void 0);
        }
    }
    FileUploadStatus.Model = Model;
})(FileUploadStatus || (FileUploadStatus = {}));

;// CONCATENATED MODULE: ../packages/filebrowser/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module filebrowser
 */










/***/ })

}]);
//# sourceMappingURL=1947.0cb9c668a4633665196e.js.map?v=0cb9c668a4633665196e
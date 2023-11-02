"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([[5902],{

/***/ 95902:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": () => (/* binding */ lib)
});

// EXTERNAL MODULE: consume shared module (default) @jupyterlab/settingregistry@~4.1.0-alpha.2 (singleton) (fallback: ../packages/settingregistry/lib/index.js)
var index_js_ = __webpack_require__(89397);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/translation@~4.1.0-alpha.2 (singleton) (fallback: ../packages/translation/lib/index.js)
var lib_index_js_ = __webpack_require__(41948);
// EXTERNAL MODULE: consume shared module (default) @jupyterlab/ui-components@~4.1.0-alpha.2 (singleton) (fallback: ../packages/ui-components/lib/index.js)
var ui_components_lib_index_js_ = __webpack_require__(76351);
// EXTERNAL MODULE: consume shared module (default) @lumino/commands@^2.0.1 (singleton) (fallback: ../node_modules/@lumino/commands/dist/index.es6.js)
var index_es6_js_ = __webpack_require__(18955);
// EXTERNAL MODULE: consume shared module (default) @lumino/coreutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/coreutils/dist/index.js)
var dist_index_js_ = __webpack_require__(22100);
// EXTERNAL MODULE: consume shared module (default) @lumino/disposable@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/disposable/dist/index.es6.js)
var dist_index_es6_js_ = __webpack_require__(78612);
// EXTERNAL MODULE: consume shared module (default) @lumino/domutils@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/domutils/dist/index.es6.js)
var domutils_dist_index_es6_js_ = __webpack_require__(92654);
// EXTERNAL MODULE: consume shared module (default) @lumino/widgets@^2.3.1-alpha.0 (singleton) (fallback: ../node_modules/@lumino/widgets/dist/index.es6.js)
var widgets_dist_index_es6_js_ = __webpack_require__(72234);
// EXTERNAL MODULE: consume shared module (default) react@^18.2.0 (singleton) (fallback: ../node_modules/react/index.js)
var react_index_js_ = __webpack_require__(52850);
var react_index_js_default = /*#__PURE__*/__webpack_require__.n(react_index_js_);
// EXTERNAL MODULE: consume shared module (default) @lumino/algorithm@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/algorithm/dist/index.es6.js)
var algorithm_dist_index_es6_js_ = __webpack_require__(16415);
// EXTERNAL MODULE: consume shared module (default) @lumino/keyboard@^2.0.0 (singleton) (fallback: ../node_modules/@lumino/keyboard/dist/index.es6.js)
var keyboard_dist_index_es6_js_ = __webpack_require__(21487);
;// CONCATENATED MODULE: ../packages/shortcuts-extension/lib/components/ShortcutInput.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */



/** Object for shortcut items */
class ShortcutObject {
    constructor() {
        this.commandName = '';
        this.label = '';
        this.keys = {};
        this.source = '';
        this.selector = '';
        this.category = '';
        this.id = '';
        this.numberOfShortcuts = 0;
        this.hasConflict = false;
    }
    get(sortCriteria) {
        if (sortCriteria === 'label') {
            return this.label;
        }
        else if (sortCriteria === 'selector') {
            return this.selector;
        }
        else if (sortCriteria === 'category') {
            return this.category;
        }
        else if (sortCriteria === 'source') {
            return this.source;
        }
        else {
            return '';
        }
    }
}
/** Object for conflicting shortcut error messages */
class ErrorObject extends ShortcutObject {
    constructor() {
        super();
        this.takenBy = new TakenByObject();
    }
}
/** Object for showing which shortcut conflicts with the new one */
class TakenByObject {
    constructor(shortcut) {
        if (shortcut) {
            this.takenBy = shortcut;
            this.takenByKey = '';
            this.takenByLabel = shortcut.category + ': ' + shortcut.label;
            this.id = shortcut.commandName + '_' + shortcut.selector;
        }
        else {
            this.takenBy = new ShortcutObject();
            this.takenByKey = '';
            this.takenByLabel = '';
            this.id = '';
        }
    }
}
class ShortcutInput extends react_index_js_.Component {
    constructor(props) {
        super(props);
        this.handleUpdate = () => {
            let keys = this.state.keys;
            keys.push(this.state.currentChain);
            this.setState({ keys: keys });
            this.props.handleUpdate(this.props.shortcut, this.state.keys);
        };
        this.handleOverwrite = async () => {
            this.props
                .deleteShortcut(this.state.takenByObject.takenBy, this.state.takenByObject.takenByKey)
                .then(this.handleUpdate());
        };
        this.handleReplace = async () => {
            let keys = this.state.keys;
            keys.push(this.state.currentChain);
            this.props.toggleInput();
            await this.props.deleteShortcut(this.props.shortcut, this.props.shortcutId);
            this.props.handleUpdate(this.props.shortcut, keys);
        };
        /** Parse user input for chained shortcuts */
        this.parseChaining = (event, value, userInput, keys, currentChain) => {
            let key = keyboard_dist_index_es6_js_.EN_US.keyForKeydownEvent(event.nativeEvent);
            const modKeys = ['Shift', 'Control', 'Alt', 'Meta', 'Ctrl', 'Accel'];
            if (event.key === 'Backspace') {
                userInput = '';
                value = '';
                keys = [];
                currentChain = '';
                this.setState({
                    value: value,
                    userInput: userInput,
                    keys: keys,
                    currentChain: currentChain
                });
            }
            else if (event.key !== 'CapsLock') {
                const lastKey = userInput
                    .substr(userInput.lastIndexOf(' ') + 1, userInput.length)
                    .trim();
                /** if last key was not a modefier then there is a chain */
                if (modKeys.lastIndexOf(lastKey) === -1 && lastKey != '') {
                    userInput = userInput + ',';
                    keys.push(currentChain);
                    currentChain = '';
                    /** check if a modefier key was held down through chain */
                    if (event.ctrlKey && event.key != 'Control') {
                        userInput = (userInput + ' Ctrl').trim();
                        currentChain = (currentChain + ' Ctrl').trim();
                    }
                    if (event.metaKey && event.key != 'Meta') {
                        userInput = (userInput + ' Accel').trim();
                        currentChain = (currentChain + ' Accel').trim();
                    }
                    if (event.altKey && event.key != 'Alt') {
                        userInput = (userInput + ' Alt').trim();
                        currentChain = (currentChain + ' Alt').trim();
                    }
                    if (event.shiftKey && event.key != 'Shift') {
                        userInput = (userInput + ' Shift').trim();
                        currentChain = (currentChain + ' Shift').trim();
                    }
                    /** if not a modefier key, add to user input and current chain */
                    if (modKeys.lastIndexOf(event.key) === -1) {
                        userInput = (userInput + ' ' + key).trim();
                        currentChain = (currentChain + ' ' + key).trim();
                        /** if a modefier key, add to user input and current chain */
                    }
                    else {
                        if (event.key === 'Meta') {
                            userInput = (userInput + ' Accel').trim();
                            currentChain = (currentChain + ' Accel').trim();
                        }
                        else if (event.key === 'Control') {
                            userInput = (userInput + ' Ctrl').trim();
                            currentChain = (currentChain + ' Ctrl').trim();
                        }
                        else if (event.key === 'Shift') {
                            userInput = (userInput + ' Shift').trim();
                            currentChain = (currentChain + ' Shift').trim();
                        }
                        else if (event.key === 'Alt') {
                            userInput = (userInput + ' Alt').trim();
                            currentChain = (currentChain + ' Alt').trim();
                        }
                        else {
                            userInput = (userInput + ' ' + event.key).trim();
                            currentChain = (currentChain + ' ' + event.key).trim();
                        }
                    }
                    /** if not a chain, add the key to user input and current chain */
                }
                else {
                    /** if modefier key, rename */
                    if (event.key === 'Control') {
                        userInput = (userInput + ' Ctrl').trim();
                        currentChain = (currentChain + ' Ctrl').trim();
                    }
                    else if (event.key === 'Meta') {
                        userInput = (userInput + ' Accel').trim();
                        currentChain = (currentChain + ' Accel').trim();
                    }
                    else if (event.key === 'Shift') {
                        userInput = (userInput + ' Shift').trim();
                        currentChain = (currentChain + ' Shift').trim();
                    }
                    else if (event.key === 'Alt') {
                        userInput = (userInput + ' Alt').trim();
                        currentChain = (currentChain + ' Alt').trim();
                        /** if not a modefier key, add it regularly */
                    }
                    else {
                        userInput = (userInput + ' ' + key).trim();
                        currentChain = (currentChain + ' ' + key).trim();
                    }
                }
            }
            /** update state of keys and currentChain */
            this.setState({
                keys: keys,
                currentChain: currentChain
            });
            return [userInput, keys, currentChain];
        };
        /**
         * Check if shorcut being typed will work
         * (does not end with ctrl, alt, command, or shift)
         * */
        this.checkNonFunctional = (shortcut) => {
            const dontEnd = ['Ctrl', 'Alt', 'Accel', 'Shift'];
            const shortcutKeys = this.state.currentChain.split(' ');
            const last = shortcutKeys[shortcutKeys.length - 1];
            this.setState({
                isFunctional: !(dontEnd.indexOf(last) !== -1)
            });
            return dontEnd.indexOf(last) !== -1;
        };
        /** Check if shortcut being typed is already taken */
        this.checkShortcutAvailability = (userInput, keys, currentChain) => {
            /** First, check whole shortcut */
            let isAvailable = Object.keys(this.props.keyBindingsUsed).indexOf(keys.join(' ') + currentChain + '_' + this.props.shortcut.selector) === -1 || userInput === '';
            let takenByObject = new TakenByObject();
            if (isAvailable) {
                /** Next, check each piece of a chain */
                for (let binding of keys) {
                    if (Object.keys(this.props.keyBindingsUsed).indexOf(binding + '_' + this.props.shortcut.selector) !== -1 &&
                        binding !== '') {
                        isAvailable = false;
                        takenByObject =
                            this.props.keyBindingsUsed[binding + '_' + this.props.shortcut.selector];
                        break;
                    }
                }
                /** Check current chain */
                if (isAvailable &&
                    Object.keys(this.props.keyBindingsUsed).indexOf(currentChain + '_' + this.props.shortcut.selector) !== -1 &&
                    currentChain !== '') {
                    isAvailable = false;
                    takenByObject =
                        this.props.keyBindingsUsed[currentChain + '_' + this.props.shortcut.selector];
                }
                /** If unavailable set takenByObject */
            }
            else {
                takenByObject =
                    this.props.keyBindingsUsed[keys.join(' ') + currentChain + '_' + this.props.shortcut.selector];
            }
            /** allow to set shortcut to what it initially was if replacing */
            if (!isAvailable) {
                if (takenByObject.takenBy.id === this.props.shortcut.id &&
                    this.props.newOrReplace === 'replace') {
                    isAvailable = true;
                    takenByObject = new TakenByObject();
                }
            }
            this.setState({ isAvailable: isAvailable });
            return takenByObject;
        };
        /** Parse and normalize user input */
        this.handleInput = (event) => {
            event.preventDefault();
            this.setState({ selected: false });
            const parsed = this.parseChaining(event, this.state.value, this.state.userInput, this.state.keys, this.state.currentChain);
            const userInput = parsed[0];
            const keys = parsed[1];
            const currentChain = parsed[2];
            const value = this.props.toSymbols(userInput);
            let takenByObject = this.checkShortcutAvailability(userInput, keys, currentChain);
            this.checkConflict(takenByObject, keys);
            this.setState({
                value: value,
                userInput: userInput,
                takenByObject: takenByObject,
                keys: keys,
                currentChain: currentChain
            }, () => this.checkNonFunctional(this.state.userInput));
        };
        this.handleBlur = (event) => {
            if (event.relatedTarget === null ||
                (event.relatedTarget.id !== 'no-blur' &&
                    event.relatedTarget.id !== 'overwrite')) {
                this.props.toggleInput();
                this.setState({
                    value: '',
                    userInput: ''
                });
                this.props.clearConflicts();
            }
        };
        this.state = {
            value: this.props.placeholder,
            userInput: '',
            isAvailable: true,
            isFunctional: this.props.newOrReplace === 'replace',
            takenByObject: new TakenByObject(),
            keys: new Array(),
            currentChain: '',
            selected: true
        };
    }
    checkConflict(takenByObject, keys) {
        if (takenByObject.id !== '' &&
            takenByObject.takenBy.id !== this.props.shortcut.id) {
            this.props.sortConflict(this.props.shortcut, takenByObject, takenByObject.takenByLabel, '');
        }
        else {
            this.props.clearConflicts();
        }
    }
    render() {
        const trans = this.props.translator.load('jupyterlab');
        let inputClassName = 'jp-Shortcuts-Input';
        if (!this.state.isAvailable) {
            inputClassName += ' jp-mod-unavailable-Input';
        }
        return (react_index_js_.createElement("div", { className: this.props.displayInput
                ? this.props.newOrReplace === 'new'
                    ? 'jp-Shortcuts-InputBox jp-Shortcuts-InputBoxNew'
                    : 'jp-Shortcuts-InputBox'
                : 'jp-mod-hidden', onBlur: event => this.handleBlur(event) },
            react_index_js_.createElement("div", { tabIndex: 0, id: "no-blur", className: inputClassName, onKeyDown: this.handleInput, ref: input => input && input.focus() },
                react_index_js_.createElement("p", { className: this.state.selected && this.props.newOrReplace === 'replace'
                        ? 'jp-Shortcuts-InputText jp-mod-selected-InputText'
                        : this.state.value === ''
                            ? 'jp-Shortcuts-InputText jp-mod-waiting-InputText'
                            : 'jp-Shortcuts-InputText' }, this.state.value === ''
                    ? trans.__('press keys')
                    : this.state.value)),
            react_index_js_.createElement("button", { className: !this.state.isFunctional
                    ? 'jp-Shortcuts-Submit jp-mod-defunc-Submit'
                    : !this.state.isAvailable
                        ? 'jp-Shortcuts-Submit jp-mod-conflict-Submit'
                        : 'jp-Shortcuts-Submit', id: 'no-blur', disabled: !this.state.isAvailable || !this.state.isFunctional, onClick: () => {
                    if (this.props.newOrReplace === 'new') {
                        this.handleUpdate();
                        this.setState({
                            value: '',
                            keys: [],
                            currentChain: ''
                        });
                        this.props.toggleInput();
                    }
                    else {
                        /** don't replace if field has not been edited */
                        if (this.state.selected) {
                            this.props.toggleInput();
                            this.setState({
                                value: '',
                                userInput: ''
                            });
                            this.props.clearConflicts();
                        }
                        else {
                            void this.handleReplace();
                        }
                    }
                } }, this.state.isAvailable ? react_index_js_.createElement(ui_components_lib_index_js_.checkIcon.react, null) : react_index_js_.createElement(ui_components_lib_index_js_.errorIcon.react, null)),
            !this.state.isAvailable && (react_index_js_.createElement("button", { hidden: true, id: "overwrite", onClick: () => {
                    void this.handleOverwrite();
                    this.props.clearConflicts();
                    this.props.toggleInput();
                } }, trans.__('Overwrite')))));
    }
}

;// CONCATENATED MODULE: ../packages/shortcuts-extension/lib/components/ShortcutItem.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */



var ShortCutLocation;
(function (ShortCutLocation) {
    ShortCutLocation[ShortCutLocation["Left"] = 0] = "Left";
    ShortCutLocation[ShortCutLocation["Right"] = 1] = "Right";
})(ShortCutLocation || (ShortCutLocation = {}));
/** Describe commands that are used by shortcuts */
function getCommands(trans) {
    return {
        shortcutEditLeft: {
            commandId: 'shortcutui:EditLeft',
            label: trans.__('Edit First'),
            caption: trans.__('Edit existing shortcut')
        },
        shortcutEditRight: {
            commandId: 'shortcutui:EditRight',
            label: trans.__('Edit Second'),
            caption: trans.__('Edit existing shortcut')
        },
        shortcutEdit: {
            commandId: 'shortcutui:Edit',
            label: trans.__('Edit'),
            caption: trans.__('Edit existing shortcut')
        },
        shortcutAddNew: {
            commandId: 'shortcutui:AddNew',
            label: trans.__('Add'),
            caption: trans.__('Add new shortcut')
        },
        shortcutAddAnother: {
            commandId: 'shortcutui:AddAnother',
            label: trans.__('Add'),
            caption: trans.__('Add another shortcut')
        },
        shortcutReset: {
            commandId: 'shortcutui:Reset',
            label: trans.__('Reset'),
            caption: trans.__('Reset shortcut back to default')
        }
    };
}
/** React component for each command shortcut item */
class ShortcutItem extends react_index_js_.Component {
    constructor(props) {
        super(props);
        /** Toggle display state of input box */
        this.toggleInputNew = () => {
            this.setState({
                displayNewInput: !this.state.displayNewInput
            });
        };
        this.toggleInputReplaceLeft = () => {
            this.setState({
                displayReplaceInputLeft: !this.state.displayReplaceInputLeft
            });
        };
        this.toggleInputReplaceRight = () => {
            this.setState({
                displayReplaceInputRight: !this.state.displayReplaceInputRight
            });
        };
        this.addCommandIfNeeded = (command, action) => {
            const key = this.props.shortcut.commandName + '_' + this.props.shortcut.selector;
            if (!this.props.external.hasCommand(command.commandId + key)) {
                this.props.external.addCommand(command.commandId + key, {
                    label: command.label,
                    caption: command.caption,
                    execute: action
                });
            }
        };
        this.handleRightClick = (e) => {
            this.addCommandIfNeeded(this._commands.shortcutEdit, () => this.toggleInputReplaceLeft());
            this.addCommandIfNeeded(this._commands.shortcutEditLeft, () => this.toggleInputReplaceLeft());
            this.addCommandIfNeeded(this._commands.shortcutEditRight, () => this.toggleInputReplaceRight());
            this.addCommandIfNeeded(this._commands.shortcutAddNew, () => this.toggleInputNew());
            this.addCommandIfNeeded(this._commands.shortcutAddAnother, () => this.toggleInputNew());
            this.addCommandIfNeeded(this._commands.shortcutReset, () => this.props.resetShortcut(this.props.shortcut));
            const key = this.props.shortcut.commandName + '_' + this.props.shortcut.selector;
            this.setState({
                numShortcuts: Object.keys(this.props.shortcut.keys).filter(key => this.props.shortcut.keys[key][0] !== '').length
            }, () => {
                let commandList = [];
                if (this.state.numShortcuts == 2) {
                    commandList = commandList.concat([
                        this._commands.shortcutEditLeft.commandId + key,
                        this._commands.shortcutEditRight.commandId + key
                    ]);
                }
                else if (this.state.numShortcuts == 1) {
                    commandList = commandList.concat([
                        this._commands.shortcutEdit.commandId + key,
                        this._commands.shortcutAddAnother.commandId + key
                    ]);
                }
                else {
                    commandList = commandList.concat([
                        this._commands.shortcutAddNew.commandId + key
                    ]);
                }
                if (this.props.shortcut.source === 'Custom') {
                    commandList = commandList.concat([
                        this._commands.shortcutReset.commandId + key
                    ]);
                }
                this.props.contextMenu(e, commandList);
            });
        };
        /** Transform special key names into unicode characters */
        this.toSymbols = (value) => {
            return value.split(' ').reduce((result, key) => {
                if (key === 'Ctrl') {
                    return (result + ' ⌃').trim();
                }
                else if (key === 'Alt') {
                    return (result + ' ⌥').trim();
                }
                else if (key === 'Shift') {
                    return (result + ' ⇧').trim();
                }
                else if (key === 'Accel' && domutils_dist_index_es6_js_.Platform.IS_MAC) {
                    return (result + ' ⌘').trim();
                }
                else if (key === 'Accel') {
                    return (result + ' ⌃').trim();
                }
                else {
                    return (result + ' ' + key).trim();
                }
            }, '');
        };
        this._commands = getCommands(props.external.translator.load('jupyterlab'));
        this.state = {
            displayNewInput: false,
            displayReplaceInputLeft: false,
            displayReplaceInputRight: false,
            numShortcuts: Object.keys(this.props.shortcut.keys).filter(key => this.props.shortcut.keys[key][0] !== '').length
        };
    }
    getErrorRow() {
        const trans = this.props.external.translator.load('jupyterlab');
        return (react_index_js_.createElement("div", { className: "jp-Shortcuts-Row" },
            react_index_js_.createElement("div", { className: "jp-Shortcuts-ConflictContainer" },
                react_index_js_.createElement("div", { className: "jp-Shortcuts-ErrorMessage" }, trans.__('Shortcut already in use by %1. Overwrite it?', this.props.shortcut.takenBy.takenByLabel)),
                react_index_js_.createElement("div", { className: "jp-Shortcuts-ErrorButton" },
                    react_index_js_.createElement("button", null, trans.__('Cancel')),
                    react_index_js_.createElement("button", { id: "no-blur", onClick: () => {
                            var _a;
                            (_a = document.getElementById('overwrite')) === null || _a === void 0 ? void 0 : _a.click();
                        } }, trans.__('Overwrite'))))));
    }
    getCategoryCell() {
        return (react_index_js_.createElement("div", { className: "jp-Shortcuts-Cell" }, this.props.shortcut.category));
    }
    getLabelCell() {
        return (react_index_js_.createElement("div", { className: "jp-Shortcuts-Cell" },
            react_index_js_.createElement("div", { className: "jp-label" }, this.props.shortcut.label)));
    }
    getResetShortCutLink() {
        const trans = this.props.external.translator.load('jupyterlab');
        return (react_index_js_.createElement("a", { className: "jp-Shortcuts-Reset", onClick: () => this.props.resetShortcut(this.props.shortcut) }, trans.__('Reset')));
    }
    getSourceCell() {
        return (react_index_js_.createElement("div", { className: "jp-Shortcuts-Cell" },
            react_index_js_.createElement("div", { className: "jp-Shortcuts-SourceCell" }, this.props.shortcut.source),
            this.props.shortcut.source === 'Custom' && this.getResetShortCutLink()));
    }
    getOptionalSelectorCell() {
        return this.props.showSelectors ? (react_index_js_.createElement("div", { className: "jp-Shortcuts-Cell" },
            react_index_js_.createElement("div", { className: "jp-selector" }, this.props.shortcut.selector))) : null;
    }
    getClassNameForShortCuts(nonEmptyKeys) {
        const classes = ['jp-Shortcuts-ShortcutCell'];
        switch (nonEmptyKeys.length) {
            case 1:
                classes.push('jp-Shortcuts-SingleCell');
                break;
            case 0:
                classes.push('jp-Shortcuts-EmptyCell');
                break;
        }
        return classes.join(' ');
    }
    getToggleInputReplaceMethod(location) {
        switch (location) {
            case ShortCutLocation.Left:
                return this.toggleInputReplaceLeft;
            case ShortCutLocation.Right:
                return this.toggleInputReplaceRight;
        }
    }
    getDisplayReplaceInput(location) {
        switch (location) {
            case ShortCutLocation.Left:
                return this.state.displayReplaceInputLeft;
            case ShortCutLocation.Right:
                return this.state.displayReplaceInputRight;
        }
    }
    getOrDiplayIfNeeded(nonEmptyKeys) {
        const trans = this.props.external.translator.load('jupyterlab');
        return (react_index_js_.createElement("div", { className: nonEmptyKeys.length == 2 || this.state.displayNewInput
                ? 'jp-Shortcuts-OrTwo'
                : 'jp-Shortcuts-Or', id: nonEmptyKeys.length == 2
                ? 'secondor'
                : this.state.displayReplaceInputLeft
                    ? 'noor'
                    : 'or' }, trans.__('or')));
    }
    getShortCutAsInput(key, location) {
        return (react_index_js_.createElement(ShortcutInput, { handleUpdate: this.props.handleUpdate, deleteShortcut: this.props.deleteShortcut, toggleInput: this.getToggleInputReplaceMethod(location), shortcut: this.props.shortcut, shortcutId: key, toSymbols: this.toSymbols, keyBindingsUsed: this.props.keyBindingsUsed, sortConflict: this.props.sortConflict, clearConflicts: this.props.clearConflicts, displayInput: this.getDisplayReplaceInput(location), newOrReplace: 'replace', placeholder: this.toSymbols(this.props.shortcut.keys[key].join(', ')), translator: this.props.external.translator }));
    }
    getShortCutForDisplayOnly(key) {
        return this.props.shortcut.keys[key].map((keyBinding, index) => (react_index_js_.createElement("div", { className: "jp-Shortcuts-ShortcutKeysContainer", key: index },
            react_index_js_.createElement("div", { className: "jp-Shortcuts-ShortcutKeys" }, this.toSymbols(keyBinding)),
            index + 1 < this.props.shortcut.keys[key].length ? (react_index_js_.createElement("div", { className: "jp-Shortcuts-Comma" }, ",")) : null)));
    }
    isLocationBeingEdited(location) {
        return ((location === ShortCutLocation.Left &&
            this.state.displayReplaceInputLeft) ||
            (location === ShortCutLocation.Right &&
                this.state.displayReplaceInputRight));
    }
    getLocationFromIndex(index) {
        return index === 0 ? ShortCutLocation.Left : ShortCutLocation.Right;
    }
    getDivForKey(index, key, nonEmptyKeys) {
        const location = this.getLocationFromIndex(index);
        return (react_index_js_.createElement("div", { className: "jp-Shortcuts-ShortcutContainer", key: this.props.shortcut.id + '_' + index, onClick: this.getToggleInputReplaceMethod(location) },
            this.isLocationBeingEdited(location)
                ? this.getShortCutAsInput(key, location)
                : this.getShortCutForDisplayOnly(key),
            location === ShortCutLocation.Left &&
                this.getOrDiplayIfNeeded(nonEmptyKeys)));
    }
    getAddLink() {
        const trans = this.props.external.translator.load('jupyterlab');
        return (react_index_js_.createElement("a", { className: !this.state.displayNewInput ? 'jp-Shortcuts-Plus' : '', onClick: () => {
                this.toggleInputNew(), this.props.clearConflicts();
            }, id: "add-link" }, trans.__('Add')));
    }
    getInputBoxWhenToggled() {
        return this.state.displayNewInput ? (react_index_js_.createElement(ShortcutInput, { handleUpdate: this.props.handleUpdate, deleteShortcut: this.props.deleteShortcut, toggleInput: this.toggleInputNew, shortcut: this.props.shortcut, shortcutId: "", toSymbols: this.toSymbols, keyBindingsUsed: this.props.keyBindingsUsed, sortConflict: this.props.sortConflict, clearConflicts: this.props.clearConflicts, displayInput: this.state.displayNewInput, newOrReplace: 'new', placeholder: '', translator: this.props.external.translator })) : (react_index_js_.createElement("div", null));
    }
    getShortCutsCell(nonEmptyKeys) {
        return (react_index_js_.createElement("div", { className: "jp-Shortcuts-Cell" },
            react_index_js_.createElement("div", { className: this.getClassNameForShortCuts(nonEmptyKeys) },
                nonEmptyKeys.map((key, index) => this.getDivForKey(index, key, nonEmptyKeys)),
                nonEmptyKeys.length === 1 &&
                    !this.state.displayNewInput &&
                    !this.state.displayReplaceInputLeft &&
                    this.getAddLink(),
                nonEmptyKeys.length === 0 &&
                    !this.state.displayNewInput &&
                    this.getAddLink(),
                this.getInputBoxWhenToggled())));
    }
    render() {
        const nonEmptyKeys = Object.keys(this.props.shortcut.keys).filter((key) => this.props.shortcut.keys[key][0] !== '');
        if (this.props.shortcut.id === 'error_row') {
            return this.getErrorRow();
        }
        else {
            return (react_index_js_.createElement("div", { className: "jp-Shortcuts-Row", onContextMenu: e => {
                    e.persist();
                    this.handleRightClick(e);
                } },
                this.getCategoryCell(),
                this.getLabelCell(),
                this.getShortCutsCell(nonEmptyKeys),
                this.getSourceCell(),
                this.getOptionalSelectorCell()));
        }
    }
}

;// CONCATENATED MODULE: ../packages/shortcuts-extension/lib/components/ShortcutList.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */


const TOPNAV_HEIGHT = 115;
/** React component for list of shortcuts */
class ShortcutList extends react_index_js_.Component {
    render() {
        return (react_index_js_.createElement("div", { className: "jp-Shortcuts-ShortcutListContainer", style: {
                height: `${this.props.height - TOPNAV_HEIGHT}px`
            }, id: "shortcutListContainer" },
            react_index_js_.createElement("div", { className: "jp-Shortcuts-ShortcutList" }, this.props.shortcuts.map((shortcut) => {
                return (react_index_js_.createElement(ShortcutItem, { key: shortcut.commandName + '_' + shortcut.selector, resetShortcut: this.props.resetShortcut, shortcut: shortcut, handleUpdate: this.props.handleUpdate, deleteShortcut: this.props.deleteShortcut, showSelectors: this.props.showSelectors, keyBindingsUsed: this.props.keyBindingsUsed, sortConflict: this.props.sortConflict, clearConflicts: this.props.clearConflicts, contextMenu: this.props.contextMenu, external: this.props.external }));
            }))));
    }
}

;// CONCATENATED MODULE: ../packages/shortcuts-extension/lib/components/ShortcutTitleItem.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */


class ShortcutTitleItem extends react_index_js_.Component {
    render() {
        return (react_index_js_.createElement("div", { className: this.props.title.toLowerCase() === this.props.active
                ? 'jp-Shortcuts-Header jp-Shortcuts-CurrentHeader'
                : 'jp-Shortcuts-Header', onClick: () => this.props.updateSort(this.props.title.toLowerCase()) },
            this.props.title,
            react_index_js_.createElement(ui_components_lib_index_js_.caretDownEmptyThinIcon.react, { className: 'jp-Shortcuts-SortButton jp-ShortcutTitleItem-sortButton' })));
    }
}

;// CONCATENATED MODULE: ../packages/shortcuts-extension/lib/components/TopNav.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */



var CommandIDs;
(function (CommandIDs) {
    CommandIDs.showSelectors = 'shortcutui:showSelectors';
    CommandIDs.resetAll = 'shortcutui:resetAll';
})(CommandIDs || (CommandIDs = {}));
function Symbols(props) {
    return (react_index_js_.createElement("div", { className: "jp-Shortcuts-Symbols" },
        react_index_js_.createElement("table", null,
            react_index_js_.createElement("tbody", null,
                react_index_js_.createElement("tr", null,
                    react_index_js_.createElement("td", null,
                        react_index_js_.createElement("kbd", null, "Cmd")),
                    react_index_js_.createElement("td", null, "\u2318"),
                    react_index_js_.createElement("td", null,
                        react_index_js_.createElement("kbd", null, "Ctrl")),
                    react_index_js_.createElement("td", null, "\u2303")),
                react_index_js_.createElement("tr", null,
                    react_index_js_.createElement("td", null,
                        react_index_js_.createElement("kbd", null, "Alt")),
                    react_index_js_.createElement("td", null, "\u2325"),
                    react_index_js_.createElement("td", null,
                        react_index_js_.createElement("kbd", null, "Shift")),
                    react_index_js_.createElement("td", null, "\u21E7"))))));
}
function AdvancedOptions(props) {
    const trans = props.translator.load('jupyterlab');
    return (react_index_js_.createElement("div", { className: "jp-Shortcuts-AdvancedOptions" },
        react_index_js_.createElement("a", { className: "jp-Shortcuts-AdvancedOptionsLink", onClick: () => props.toggleSelectors() }, props.showSelectors
            ? trans.__('Hide Selectors')
            : trans.__('Show Selectors')),
        react_index_js_.createElement("a", { className: "jp-Shortcuts-AdvancedOptionsLink", onClick: () => props.resetShortcuts() }, trans.__('Reset All'))));
}
/** React component for top navigation */
class TopNav extends react_index_js_.Component {
    constructor(props) {
        super(props);
        this.addMenuCommands();
        this.menu = this.props.external.createMenu();
        this.menu.addItem({ command: CommandIDs.showSelectors });
        this.menu.addItem({ command: CommandIDs.resetAll });
    }
    addMenuCommands() {
        const trans = this.props.external.translator.load('jupyterlab');
        if (!this.props.external.hasCommand(CommandIDs.showSelectors)) {
            this.props.external.addCommand(CommandIDs.showSelectors, {
                label: trans.__('Toggle Selectors'),
                caption: trans.__('Toggle command selectors'),
                execute: () => {
                    this.props.toggleSelectors();
                }
            });
        }
        if (!this.props.external.hasCommand(CommandIDs.resetAll)) {
            this.props.external.addCommand(CommandIDs.resetAll, {
                label: trans.__('Reset All'),
                caption: trans.__('Reset all shortcuts'),
                execute: () => {
                    this.props.resetShortcuts();
                }
            });
        }
    }
    getShortCutTitleItem(title) {
        return (react_index_js_.createElement("div", { className: "jp-Shortcuts-Cell" },
            react_index_js_.createElement(ShortcutTitleItem, { title: title, updateSort: this.props.updateSort, active: this.props.currentSort })));
    }
    render() {
        const trans = this.props.external.translator.load('jupyterlab');
        return (react_index_js_.createElement("div", { className: "jp-Shortcuts-Top" },
            react_index_js_.createElement("div", { className: "jp-Shortcuts-TopNav" },
                react_index_js_.createElement(Symbols, null),
                react_index_js_.createElement(ui_components_lib_index_js_.InputGroup, { className: "jp-Shortcuts-Search", type: "text", onChange: event => this.props.updateSearchQuery(event), placeholder: trans.__('Search…'), rightIcon: "ui-components:search" }),
                react_index_js_.createElement(AdvancedOptions, { toggleSelectors: this.props.toggleSelectors, showSelectors: this.props.showSelectors, resetShortcuts: this.props.resetShortcuts, menu: this.menu, translator: this.props.external.translator })),
            react_index_js_.createElement("div", { className: "jp-Shortcuts-HeaderRowContainer" },
                react_index_js_.createElement("div", { className: "jp-Shortcuts-HeaderRow" },
                    this.getShortCutTitleItem(trans.__('Category')),
                    this.getShortCutTitleItem(trans.__('Command')),
                    react_index_js_.createElement("div", { className: "jp-Shortcuts-Cell" },
                        react_index_js_.createElement("div", { className: "title-div" }, trans.__('Shortcut'))),
                    this.getShortCutTitleItem(trans.__('Source')),
                    this.props.showSelectors &&
                        this.getShortCutTitleItem(trans.__('Selectors'))))));
    }
}

;// CONCATENATED MODULE: ../packages/shortcuts-extension/lib/components/ShortcutUI.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */





/** Normalize the query text for a fuzzy search. */
function normalizeQuery(text) {
    return text.replace(/\s+/g, '').toLowerCase();
}
/** Perform a fuzzy search on a single command item. */
function fuzzySearch(item, query) {
    // Create the source text to be searched.
    const category = item.category.toLowerCase();
    const label = item['label'].toLowerCase();
    const source = `${category} ${label}`;
    // Set up the match score and indices array.
    let score = Infinity;
    let indices = null;
    // The regex for search word boundaries
    const rgx = /\b\w/g;
    // Search the source by word boundary.
    // eslint-disable-next-line
    while (true) {
        // Find the next word boundary in the source.
        const rgxMatch = rgx.exec(source);
        // Break if there is no more source context.
        if (!rgxMatch) {
            break;
        }
        // Run the string match on the relevant substring.
        const match = algorithm_dist_index_es6_js_.StringExt.matchSumOfDeltas(source, query, rgxMatch.index);
        // Break if there is no match.
        if (!match) {
            break;
        }
        // Update the match if the score is better.
        if (match && match.score <= score) {
            score = match.score;
            indices = match.indices;
        }
    }
    // Bail if there was no match.
    if (!indices || score === Infinity) {
        return null;
    }
    // Compute the pivot index between category and label text.
    const pivot = category.length + 1;
    // Find the slice index to separate matched indices.
    const j = algorithm_dist_index_es6_js_.ArrayExt.lowerBound(indices, pivot, (a, b) => a - b);
    // Extract the matched category and label indices.
    const categoryIndices = indices.slice(0, j);
    const labelIndices = indices.slice(j);
    // Adjust the label indices for the pivot offset.
    for (let i = 0, n = labelIndices.length; i < n; ++i) {
        labelIndices[i] -= pivot;
    }
    // Handle a pure label match.
    if (categoryIndices.length === 0) {
        return {
            matchType: 0 /* MatchType.Label */,
            categoryIndices: null,
            labelIndices,
            score,
            item
        };
    }
    // Handle a pure category match.
    if (labelIndices.length === 0) {
        return {
            matchType: 1 /* MatchType.Category */,
            categoryIndices,
            labelIndices: null,
            score,
            item
        };
    }
    // Handle a split match.
    return {
        matchType: 2 /* MatchType.Split */,
        categoryIndices,
        labelIndices,
        score,
        item
    };
}
/** Perform a fuzzy match on an array of command items. */
function matchItems(items, query) {
    // Normalize the query text to lower case with no whitespace.
    query = normalizeQuery(query);
    // Create the array to hold the scores.
    let scores = [];
    // Iterate over the items and match against the query.
    let itemList = Object.keys(items);
    for (let i = 0, n = itemList.length; i < n; ++i) {
        let item = items[itemList[i]];
        // If the query is empty, all items are matched by default.
        if (!query) {
            scores.push({
                matchType: 3 /* MatchType.Default */,
                categoryIndices: null,
                labelIndices: null,
                score: 0,
                item
            });
            continue;
        }
        // Run the fuzzy search for the item and query.
        let score = fuzzySearch(item, query);
        // Ignore the item if it is not a match.
        if (!score) {
            continue;
        }
        // Add the score to the results.
        scores.push(score);
    }
    // Return the final array of scores.
    return scores;
}
/** Transform SettingRegistry's shortcut list to list of ShortcutObjects */
function getShortcutObjects(external, settings) {
    const shortcuts = settings.composite.shortcuts;
    let shortcutObjects = {};
    shortcuts.forEach((shortcut) => {
        let key = shortcut.command + '_' + shortcut.selector;
        if (Object.keys(shortcutObjects).indexOf(key) !== -1) {
            let currentCount = shortcutObjects[key].numberOfShortcuts;
            shortcutObjects[key].keys[currentCount] = shortcut.keys;
            shortcutObjects[key].numberOfShortcuts++;
        }
        else {
            let shortcutObject = new ShortcutObject();
            shortcutObject.commandName = shortcut.command;
            let label = external.getLabel(shortcut.command);
            if (!label) {
                label = shortcut.command.split(':')[1];
            }
            shortcutObject.label = label;
            shortcutObject.category = shortcut.command.split(':')[0];
            shortcutObject.keys[0] = shortcut.keys;
            shortcutObject.selector = shortcut.selector;
            // TODO needs translation
            shortcutObject.source = 'Default';
            shortcutObject.id = key;
            shortcutObject.numberOfShortcuts = 1;
            shortcutObjects[key] = shortcutObject;
        }
    });
    // find all the shortcuts that have custom settings
    const userShortcuts = settings.user.shortcuts;
    userShortcuts.forEach((userSetting) => {
        const command = userSetting.command;
        const selector = userSetting.selector;
        const keyTo = command + '_' + selector;
        if (shortcutObjects[keyTo]) {
            // TODO needs translation
            shortcutObjects[keyTo].source = 'Custom';
        }
    });
    return shortcutObjects;
}
/** Get list of all shortcut keybindings currently in use
 * An object where keys are unique keyBinding_selector and values are shortcut objects **/
function getKeyBindingsUsed(shortcutObjects) {
    let keyBindingsUsed = {};
    Object.keys(shortcutObjects).forEach((shortcut) => {
        Object.keys(shortcutObjects[shortcut].keys).forEach((key) => {
            const takenBy = new TakenByObject(shortcutObjects[shortcut]);
            takenBy.takenByKey = key;
            keyBindingsUsed[shortcutObjects[shortcut].keys[key].join(' ') +
                '_' +
                shortcutObjects[shortcut].selector] = takenBy;
        });
    });
    return keyBindingsUsed;
}
/** Top level React component for widget */
class ShortcutUI extends react_index_js_.Component {
    constructor(props) {
        super(props);
        /** Set the current seach query */
        this.updateSearchQuery = (event) => {
            this.setState({
                searchQuery: event.target['value']
            }, () => this.setState({
                filteredShortcutList: this.searchFilterShortcuts(this.state.shortcutList)
            }, () => {
                this.sortShortcuts();
            }));
        };
        /** Reset all shortcuts to their defaults */
        this.resetShortcuts = async () => {
            const settings = await this.props.external.getAllShortCutSettings();
            for (const key of Object.keys(settings.user)) {
                await this.props.external.removeShortCut(key);
            }
            await this._refreshShortcutList();
        };
        /** Set new shortcut for command, refresh state */
        this.handleUpdate = async (shortcutObject, keys) => {
            const settings = await this.props.external.getAllShortCutSettings();
            const userShortcuts = settings.user.shortcuts;
            const newUserShortcuts = [];
            let found = false;
            for (let shortcut of userShortcuts) {
                if (shortcut['command'] === shortcutObject.commandName &&
                    shortcut['selector'] === shortcutObject.selector) {
                    newUserShortcuts.push({
                        command: shortcut['command'],
                        selector: shortcut['selector'],
                        keys: keys
                    });
                    found = true;
                }
                else {
                    newUserShortcuts.push(shortcut);
                }
            }
            if (!found) {
                newUserShortcuts.push({
                    command: shortcutObject.commandName,
                    selector: shortcutObject.selector,
                    keys: keys
                });
            }
            await settings.set('shortcuts', newUserShortcuts);
            await this._refreshShortcutList();
        };
        /** Delete shortcut for command, refresh state */
        this.deleteShortcut = async (shortcutObject, shortcutId) => {
            await this.handleUpdate(shortcutObject, ['']);
            await this._refreshShortcutList();
        };
        /** Reset a specific shortcut to its default settings */
        this.resetShortcut = async (shortcutObject) => {
            const settings = await this.props.external.getAllShortCutSettings();
            const userShortcuts = settings.user.shortcuts;
            const newUserShortcuts = [];
            for (let shortcut of userShortcuts) {
                if (shortcut['command'] !== shortcutObject.commandName ||
                    shortcut['selector'] !== shortcutObject.selector) {
                    newUserShortcuts.push(shortcut);
                }
            }
            await settings.set('shortcuts', newUserShortcuts);
            await this._refreshShortcutList();
        };
        /** Toggles showing command selectors */
        this.toggleSelectors = () => {
            this.setState({ showSelectors: !this.state.showSelectors });
        };
        /** Set the current list sort order */
        this.updateSort = (value) => {
            if (value !== this.state.currentSort) {
                this.setState({ currentSort: value }, this.sortShortcuts);
            }
        };
        /** Sort shortcut list so that an error row is right below the one currently being set */
        this.sortConflict = (newShortcut, takenBy) => {
            const shortcutList = this.state.filteredShortcutList;
            if (shortcutList.filter(shortcut => shortcut.id === 'error_row').length === 0) {
                const errorRow = new ErrorObject();
                errorRow.takenBy = takenBy;
                errorRow.id = 'error_row';
                shortcutList.splice(shortcutList.indexOf(newShortcut) + 1, 0, errorRow);
                errorRow.hasConflict = true;
                this.setState({ filteredShortcutList: shortcutList });
            }
        };
        /** Remove conflict flag from all shortcuts */
        this.clearConflicts = () => {
            /** Remove error row */
            const shortcutList = this.state.filteredShortcutList.filter(shortcut => shortcut.id !== 'error_row');
            shortcutList.forEach((shortcut) => {
                shortcut.hasConflict = false;
            });
            this.setState({ filteredShortcutList: shortcutList });
        };
        this.contextMenu = (event, commandIDs) => {
            event.persist();
            this.setState({
                contextMenu: this.props.external.createMenu()
            }, () => {
                event.preventDefault();
                for (let command of commandIDs) {
                    this.state.contextMenu.addItem({ command });
                }
                this.state.contextMenu.open(event.clientX, event.clientY);
            });
        };
        this.state = {
            shortcutList: {},
            filteredShortcutList: new Array(),
            shortcutsFetched: false,
            searchQuery: '',
            showSelectors: false,
            currentSort: 'category',
            keyBindingsUsed: {},
            contextMenu: this.props.external.createMenu()
        };
    }
    /** Fetch shortcut list on mount */
    componentDidMount() {
        void this._refreshShortcutList();
    }
    /** Fetch shortcut list from SettingRegistry  */
    async _refreshShortcutList() {
        const shortcuts = await this.props.external.getAllShortCutSettings();
        const shortcutObjects = getShortcutObjects(this.props.external, shortcuts);
        this.setState({
            shortcutList: shortcutObjects,
            filteredShortcutList: this.searchFilterShortcuts(shortcutObjects),
            shortcutsFetched: true
        }, () => {
            let keyBindingsUsed = getKeyBindingsUsed(shortcutObjects);
            this.setState({ keyBindingsUsed });
            this.sortShortcuts();
        });
    }
    /** Filter shortcut list using current search query */
    searchFilterShortcuts(shortcutObjects) {
        const filteredShortcuts = matchItems(shortcutObjects, this.state.searchQuery).map((item) => {
            return item.item;
        });
        return filteredShortcuts;
    }
    /** Sort shortcut list using current sort property  */
    sortShortcuts() {
        const shortcuts = this.state.filteredShortcutList;
        let filterCritera = this.state.currentSort;
        if (filterCritera === 'command') {
            filterCritera = 'label';
        }
        if (filterCritera !== '') {
            shortcuts.sort((a, b) => {
                const compareA = a.get(filterCritera);
                const compareB = b.get(filterCritera);
                if (compareA < compareB) {
                    return -1;
                }
                else if (compareA > compareB) {
                    return 1;
                }
                else {
                    return a['label'] < b['label'] ? -1 : a['label'] > b['label'] ? 1 : 0;
                }
            });
        }
        this.setState({ filteredShortcutList: shortcuts });
    }
    render() {
        if (!this.state.shortcutsFetched) {
            return null;
        }
        return (react_index_js_.createElement("div", { className: "jp-Shortcuts-ShortcutUI", id: "jp-shortcutui" },
            react_index_js_.createElement(TopNav, { updateSearchQuery: this.updateSearchQuery, resetShortcuts: this.resetShortcuts, toggleSelectors: this.toggleSelectors, showSelectors: this.state.showSelectors, updateSort: this.updateSort, currentSort: this.state.currentSort, width: this.props.width, external: this.props.external }),
            react_index_js_.createElement(ShortcutList, { shortcuts: this.state.filteredShortcutList, resetShortcut: this.resetShortcut, handleUpdate: this.handleUpdate, deleteShortcut: this.deleteShortcut, showSelectors: this.state.showSelectors, keyBindingsUsed: this.state.keyBindingsUsed, sortConflict: this.sortConflict, clearConflicts: this.clearConflicts, height: this.props.height, contextMenu: this.contextMenu, external: this.props.external })));
    }
}

;// CONCATENATED MODULE: ../packages/shortcuts-extension/lib/renderer.js
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */


const renderShortCut = (props) => {
    return react_index_js_default().createElement(ShortcutUI, { external: props.external, height: 1000, width: 1000 });
};

;// CONCATENATED MODULE: ../packages/shortcuts-extension/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module shortcuts-extension
 */









function getExternalForJupyterLab(settingRegistry, app, translator) {
    const { commands } = app;
    const shortcutPluginLocation = '@jupyterlab/shortcuts-extension:shortcuts';
    return {
        translator,
        getAllShortCutSettings: () => settingRegistry.load(shortcutPluginLocation, true),
        removeShortCut: (key) => settingRegistry.remove(shortcutPluginLocation, key),
        createMenu: () => new widgets_dist_index_es6_js_.Menu({ commands }),
        hasCommand: (id) => commands.hasCommand(id),
        addCommand: (id, options) => commands.addCommand(id, options),
        getLabel: (id) => commands.label(id)
    };
}
/**
 * The default shortcuts extension.
 *
 * #### Notes
 * Shortcut values are stored in the setting system. The default values for each
 * shortcut are preset in the settings schema file of this extension.
 * Additionally, each shortcut can be individually set by the end user by
 * modifying its setting (either in the text editor or by modifying its
 * underlying JSON schema file).
 *
 * When setting shortcut selectors, there are two concepts to consider:
 * specificity and matchability. These two interact in sometimes
 * counterintuitive ways. Keyboard events are triggered from an element and
 * they propagate up the DOM until they reach the `documentElement` (`<body>`).
 *
 * When a registered shortcut sequence is fired, the shortcut manager checks
 * the node that fired the event and each of its ancestors until a node matches
 * one or more registered selectors. The *first* matching selector in the
 * chain of ancestors will invoke the shortcut handler and the traversal will
 * end at that point. If a node matches more than one selector, the handler for
 * whichever selector is more *specific* fires.
 * @see https://www.w3.org/TR/css3-selectors/#specificity
 *
 * The practical consequence of this is that a very broadly matching selector,
 * e.g. `'*'` or `'div'` may match and therefore invoke a handler *before* a
 * more specific selector. The most common pitfall is to use the universal
 * (`'*'`) selector. For almost any use case where a global keyboard shortcut is
 * required, using the `'body'` selector is more appropriate.
 */
const shortcuts = {
    id: '@jupyterlab/shortcuts-extension:shortcuts',
    description: 'Adds the keyboard shortcuts editor.',
    requires: [index_js_.ISettingRegistry],
    optional: [lib_index_js_.ITranslator, ui_components_lib_index_js_.IFormRendererRegistry],
    activate: async (app, registry, translator, editorRegistry) => {
        const translator_ = translator !== null && translator !== void 0 ? translator : lib_index_js_.nullTranslator;
        const trans = translator_.load('jupyterlab');
        const { commands } = app;
        let canonical;
        let loaded = {};
        if (editorRegistry) {
            const component = {
                fieldRenderer: (props) => {
                    return renderShortCut({
                        external: getExternalForJupyterLab(registry, app, translator_),
                        ...props
                    });
                }
            };
            editorRegistry.addRenderer(`${shortcuts.id}.shortcuts`, component);
        }
        /**
         * Populate the plugin's schema defaults.
         */
        function populate(schema) {
            const commands = app.commands.listCommands().join('\n');
            loaded = {};
            schema.properties.shortcuts.default = Object.keys(registry.plugins)
                .map(plugin => {
                const shortcuts = registry.plugins[plugin].schema['jupyter.lab.shortcuts'] || [];
                loaded[plugin] = shortcuts;
                return shortcuts;
            })
                .concat([schema.properties.shortcuts.default])
                .reduce((acc, val) => {
                if (domutils_dist_index_es6_js_.Platform.IS_MAC) {
                    return acc.concat(val);
                }
                else {
                    // If platform is not MacOS, remove all shortcuts containing Cmd
                    // as they will be modified; e.g. `Cmd A` becomes `A`
                    return acc.concat(val.filter(shortcut => !shortcut.keys.some(key => {
                        const { cmd } = index_es6_js_.CommandRegistry.parseKeystroke(key);
                        return cmd;
                    })));
                }
            }, []) // flatten one level
                .sort((a, b) => a.command.localeCompare(b.command));
            schema.properties.shortcuts.description = trans.__(`Note: To disable a system default shortcut,
copy it to User Preferences and add the
"disabled" key, for example:
{
    "command": "application:activate-next-tab",
    "keys": [
        "Ctrl Shift ]"
    ],
    "selector": "body",
    "disabled": true
}

List of commands followed by keyboard shortcuts:
%1

List of keyboard shortcuts:`, commands);
        }
        registry.pluginChanged.connect(async (sender, plugin) => {
            if (plugin !== shortcuts.id) {
                // If the plugin changed its shortcuts, reload everything.
                const oldShortcuts = loaded[plugin];
                const newShortcuts = registry.plugins[plugin].schema['jupyter.lab.shortcuts'] || [];
                if (oldShortcuts === undefined ||
                    !dist_index_js_.JSONExt.deepEqual(oldShortcuts, newShortcuts)) {
                    // Empty the default values to avoid shortcut collisions.
                    canonical = null;
                    const schema = registry.plugins[shortcuts.id].schema;
                    schema.properties.shortcuts.default = [];
                    // Reload the settings.
                    await registry.load(shortcuts.id, true);
                }
            }
        });
        // Transform the plugin object to return different schema than the default.
        registry.transform(shortcuts.id, {
            compose: plugin => {
                var _a, _b, _c, _d;
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = dist_index_js_.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                const defaults = (_c = (_b = (_a = canonical.properties) === null || _a === void 0 ? void 0 : _a.shortcuts) === null || _b === void 0 ? void 0 : _b.default) !== null && _c !== void 0 ? _c : [];
                const user = {
                    shortcuts: (_d = plugin.data.user.shortcuts) !== null && _d !== void 0 ? _d : []
                };
                const composite = {
                    shortcuts: index_js_.SettingRegistry.reconcileShortcuts(defaults, user.shortcuts)
                };
                plugin.data = { composite, user };
                return plugin;
            },
            fetch: plugin => {
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = dist_index_js_.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                return {
                    data: plugin.data,
                    id: plugin.id,
                    raw: plugin.raw,
                    schema: canonical,
                    version: plugin.version
                };
            }
        });
        try {
            // Repopulate the canonical variable after the setting registry has
            // preloaded all initial plugins.
            canonical = null;
            const settings = await registry.load(shortcuts.id);
            Private.loadShortcuts(commands, settings.composite);
            settings.changed.connect(() => {
                Private.loadShortcuts(commands, settings.composite);
            });
        }
        catch (error) {
            console.error(`Loading ${shortcuts.id} failed.`, error);
        }
    },
    autoStart: true
};
/**
 * Export the shortcut plugin as default.
 */
/* harmony default export */ const lib = (shortcuts);
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * The internal collection of currently loaded shortcuts.
     */
    let disposables;
    /**
     * Load the keyboard shortcuts from settings.
     */
    function loadShortcuts(commands, composite) {
        var _a;
        const shortcuts = ((_a = composite === null || composite === void 0 ? void 0 : composite.shortcuts) !== null && _a !== void 0 ? _a : []);
        if (disposables) {
            disposables.dispose();
        }
        disposables = shortcuts.reduce((acc, val) => {
            const options = normalizeOptions(val);
            if (options) {
                acc.add(commands.addKeyBinding(options));
            }
            return acc;
        }, new dist_index_es6_js_.DisposableSet());
    }
    Private.loadShortcuts = loadShortcuts;
    /**
     * Normalize potential keyboard shortcut options.
     */
    function normalizeOptions(value) {
        if (!value || typeof value !== 'object') {
            return undefined;
        }
        const { isArray } = Array;
        const valid = 'command' in value &&
            'keys' in value &&
            'selector' in value &&
            isArray(value.keys);
        return valid ? value : undefined;
    }
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=5902.0e89c1a162306fcbc95f.js.map?v=0e89c1a162306fcbc95f
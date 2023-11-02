"use strict";
(self["webpackChunkjupyterlab_nbhosting"] = self["webpackChunkjupyterlab_nbhosting"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
// xxx still missing from he notebook classic version
// * enable_move_up_down
// * show_metadata_in_header -> should go in courselevels
// * inactivate_non_code_cells
// * redefine_enter_in_command_mode
// * speed_up_autosave


/**
 * Initialization data for the jupyterlab-nbhosting extension.
 */
const plugin = {
    id: 'jupyterlab-nbhosting:plugin',
    description: 'Custom look and feel for nbhosting notebooks',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    activate: (app, palette, settingRegistry) => {
        console.log('JupyterLab extension jupyterlab-nbhosting is activated!');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('jupyterlab-nbhosting settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for jupyterlab-nbhosting.', reason);
            });
        }
        ////// helpers
        const get_url_param = (name) => {
            // get a URL parameter. I cannot believe we actually need this.
            // Based on http://stackoverflow.com/a/25359264/938949
            let match = new RegExp('[?&]' + name + '=([^&]*)')
                .exec(window.location.search);
            if (match) {
                return decodeURIComponent(match[1] || '');
            }
        };
        const copyToClipboard = async ({ target, message, value }) => {
            try {
                let copyValue = "";
                if (!navigator.clipboard) {
                    throw new Error("Browser don't have support for native clipboard.");
                }
                if (target) {
                    const node = document.querySelector(target);
                    if (!node || !node.textContent) {
                        throw new Error("Element not found");
                    }
                    value = node.textContent;
                }
                if (value) {
                    copyValue = value;
                }
                await navigator.clipboard.writeText(copyValue);
                console.log(message !== null && message !== void 0 ? message : "Copied!!!");
            }
            catch (error) {
                console.log("could not copyToClipboard", error /*.toString()*/);
            }
        };
        const course = get_url_param('course');
        const student = get_url_param('student');
        // window.location.pathname looks like this
        // "/35162/notebooks/w1/w1-s3-c4-fibonacci-prompt.ipynb"
        const regexp = new RegExp('^\/([0-9]+)\/notebooks\/(.*)');
        // groups 1 and 2 refer to port and notebook respectively
        const map = { port: 1, notebook: 2 };
        const match = regexp.exec(window.location.pathname);
        const notebook = (match) ? match[map.notebook] : undefined;
        const not_under_nbhosting = () => {
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: "Available under nbhosting only",
                body: "You don't appear to be running inside nbhosting, sorry",
                buttons: [
                    { label: "Ok", caption: "Ok", iconLabel: "Ok", accept: true, className: "dialog-button",
                        ariaLabel: "aria-label", iconClass: "icon-class", actions: [], displayType: 'default' },
                ],
                defaultButton: 0,
            });
        };
        const reset_to_original = (arg) => {
            console.log(`notebook = ${notebook}`);
            not_under_nbhosting;
            // if (!notebook) {
            //   not_under_nbhosting()
            //   return
            // }
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: "Confirm reset to original",
                body: "Are you sure to reset your notebook to the original version ? "
                    + " all your changes will be lost",
                buttons: [
                    // why on earth are all those settings here for ?
                    { label: "Reset", caption: "Reset", iconLabel: "Reset", accept: true, className: "dialog-button",
                        ariaLabel: "aria-label", iconClass: "icon-class", actions: [], displayType: 'default' },
                    { label: "Cancel", caption: "Cancel", iconLabel: "Cancel", accept: false, className: "dialog-button",
                        ariaLabel: "aria-label", iconClass: "icon-class", actions: [], displayType: 'default' },
                ],
                defaultButton: 0,
            }).then(answer => {
                if (answer.button.accept) {
                    if (!notebook) {
                        console.log("not under nbhosting");
                        return;
                    }
                    const reset_url = `/notebookLazyCopy/${course}/${notebook}/${student}?forcecopy=true`;
                    console.log("resetting -> ", reset_url);
                    window.location.href = reset_url;
                }
            });
        };
        const share_static_version = async (arg) => {
            // if (!notebook) {
            //   not_under_nbhosting()
            //   return
            // }
            let share_url = `/ipythonShare/${course}/${notebook}/${student}`;
            try {
                const response = await fetch(share_url);
                const jsonData = await response.json();
                let message;
                if ('error' in jsonData) {
                    message = `Could not create snapshot` + `\n${jsonData.error}`;
                }
                else {
                    message =
                        //   `<p class='nbh-dialog'>:`
                        // + `<a id="try-share-url" target='_blank' href='${jsonData.url_path}'>Try the link</a></p>`
                        // + `<span id="share-url">${jsonData.url}</span>`
                        // + `</div>`
                        // +`<p class='nbh-dialog'></p>`
                        `To share a static version of your notebook, copy the link`
                            + `\n\n`
                            + `Note that sharing the same notebook several times overwrites the same snapshot`;
                }
                //
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                    title: "Static version created (or overwritten)",
                    body: message,
                    buttons: [
                        // why on earth are all those settings here for ?
                        { label: "Copy to Clipboard", caption: "Copy to Clipboard", iconLabel: "Copy to Clipboard", accept: true, className: "dialog-button",
                            ariaLabel: "aria-label", iconClass: "icon-class", actions: [], displayType: 'default' },
                        { label: "Ok", caption: "Ok", iconLabel: "Ok", accept: false, className: "dialog-button",
                            ariaLabel: "aria-label", iconClass: "icon-class", actions: [], displayType: 'default' },
                    ],
                    defaultButton: 0,
                }).then(answer => {
                    if (answer.button.accept) {
                        console.log(`opying ${jsonData.url}`);
                        copyToClipboard({ value: jsonData.url });
                    }
                });
            }
            catch (error) {
                console.log(`Error when using URL ${share_url}`);
                return;
            }
        };
        const show_student_id = (arg) => {
            // if (!notebook) {
            //   not_under_nbhosting()
            //   return
            // }
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: "Your student id",
                body: student,
                buttons: [
                    { label: "Copy to Clipboard", caption: "Copy to Clipboard", iconLabel: "Copy to Clipboard", accept: true, className: "dialog-button",
                        ariaLabel: "aria-label", iconClass: "icon-class", actions: [], displayType: 'default' },
                    { label: "Ok", caption: "Ok", iconLabel: "Ok", accept: false, className: "dialog-button",
                        ariaLabel: "aria-label", iconClass: "icon-class", actions: [], displayType: 'default' },
                ],
                defaultButton: 0,
            }).then(answer => {
                if (answer.button.accept) {
                    if (student === undefined) {
                        console.log(`undefined student`);
                        return;
                    }
                    console.log(`copying ${student}`);
                    copyToClipboard({ value: student });
                }
            });
        };
        //////// create commands
        const { commands } = app;
        let command;
        const category = 'nbhosting';
        command = 'nbhosting:reset-to-original';
        commands.addCommand(command, {
            label: 'Reset to Original',
            // caption: 'captions of reset-to-original',
            execute: reset_to_original,
        });
        palette.addItem({ command, category });
        command = 'nbhosting:share-static-version';
        commands.addCommand(command, {
            label: 'Share Static Version',
            // caption: 'captions of share-static-version',
            execute: share_static_version,
        });
        palette.addItem({ command, category });
        command = 'nbhosting:show-student-id';
        commands.addCommand(command, {
            label: 'Show Student id',
            // caption: 'captions of show-student-id',
            execute: show_student_id,
        });
        palette.addItem({ command, category });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.db41df58c1ad5a95fd1b.js.map
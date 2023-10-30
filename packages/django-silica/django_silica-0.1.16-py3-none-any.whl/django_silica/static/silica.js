let silica_components = {};

class Silica {
    components = []

    initComponents() {
    }

    broadcastEvent() {
    }
}

function initComponents() {
    let componentEls = document.querySelectorAll("[silica\\:initial-data], [silica\\:lazy]");

    componentEls.forEach((componentEl) => {
        let component_id = componentEl.getAttribute("silica:id");

        if (!silica_components.hasOwnProperty(component_id)) {
            silica_components[component_id] = new SilicaComponent(componentEl);
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    initComponents();
});

class SilicaComponent {
    el;
    id;
    name;

    last_request_timestamp = null;

    boundMethods = {
        handleModelInputEvent: this.handleModelInputEvent.bind(this),
        handleClickEvent: this.handleClickEvent.bind(this)
    };

    ACTION_TYPE_CALL_METHOD = "call_method";
    ACTION_TYPE_SET_PROPERTY = "set_property";
    ACTION_TYPE_EVENT = "event";

    constructor(componentEl) {
        const encodedData = componentEl.getAttribute("silica:initial-data");
        const decodedData = decodeURIComponent(encodedData);
        const initialState = JSON.parse(decodedData);

        this.el = componentEl
        this.id = componentEl.getAttribute("silica:id");
        this.name = componentEl.getAttribute("silica:name");

        if (componentEl.hasAttribute("silica:lazy")) {
            this.activateLazy()
            componentEl.removeAttribute("silica:lazy")
            return
        }

        if (this.processRedirections(initialState.js_calls)) {
            return;
        }

        componentEl.removeAttribute("silica:initial-data");

        this.updateModelValues(initialState);
        this.setQueryParams(initialState);
        this.processJsCalls(initialState.js_calls);
        this.processEvents(initialState?.event_calls);
        this.setListeners()
    }

    updateModelValues(data) {
        this.querySelectorAll("[silica\\:model]").forEach((el) => {
            let modelName = el.getAttribute("silica:model");
            if (data[modelName]) {
                el.value = data[modelName];
            }
        });
    }

    setQueryParams(data) {
        if (data["query_params"] && data["query_params"].length > 0) {
            data["query_params"].forEach((param) => {
                if (data?.[param] !== undefined) {
                    this.setQueryParam(param, data[param]);
                }
            });
        }
    }

    setQueryParam(paramName, paramValue) {
        const url = new URL(window.location);
        url.searchParams.set(paramName, paramValue);
        window.history.pushState({}, "", url);
    }

    processJsCalls(calls = []) {
        calls.forEach((call) => {
            const fn = call.fn;
            const args = call?.args;
            window[fn](...args);
        });
    }

    processEvents(events = []) {
        events.forEach((event) => {
            if (event.type === "emit") {
                // emit to all silica_components on page
                Object.values(silica_components).forEach((component) => {
                    const action = {
                        type: this.ACTION_TYPE_EVENT,
                        event_name: event.name,
                        payload: event.payload
                    };

                    component.sendMessage(action);
                });
            } else if (event.type === "emit_to") {
                // emit to all silica_components on page
                Object.values(silica_components)
                    .filter((component) => component.name === event.component_name)
                    .forEach((component) => {
                        const action = {
                            type: this.ACTION_TYPE_EVENT,
                            event_name: event.name,
                            payload: event.payload
                        };

                        component.sendMessage(action);
                    });
            }
        });
    }

    callMethod(name, args) {
        const action = {
            type: this.ACTION_TYPE_CALL_METHOD,
            method_name: name,
            args: args
        };

        this.sendMessage(action);
    }

    activateLazy() {
        const action = {
            type: "activate_lazy"
        };

        this.sendMessage(action);
    }

    setProperty(name, value) {
        const action = {
            type: this.ACTION_TYPE_SET_PROPERTY,
            name: name,
            value: value
        };

        this.sendMessage(action);
    }

    sendMessage(action) {
        if (!this.id || !this.name) {
            console.error(
                "No Silica component element found when processing silica:click"
            );
            return;
        }

        this.last_request_timestamp = new Date().getTime();
        let current_request_timestamp = this.last_request_timestamp;

        // Show any silica:loading elements
        this.showLoaders(action);

        const params = {
            name: this.name,
            id: this.id,
            actions: [action]
        };

        // Send the POST request using fetch
        fetch("/silica/message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(params)
        })
            .then((response) => response.json()) // assuming server responds with json
            .then((response) => {
                if (this.last_request_timestamp > current_request_timestamp) {
                    console.log('Request was superseded by a newer request')
                    return;
                }

                if (this.processRedirections(response?.js_calls)) {
                    return;
                }

                this.updateDom(response.html);
                initComponents(); // Pick up and init any new silica_components nested in others

                this.updateModelValues(response.data);
                this.setQueryParams(response.data);
                this.processJsCalls(response?.js_calls);
                this.processEvents(response?.event_calls);

                // maybe define lazy components as either 'permanent' or 'temporary' / initial request lazy only
                // if(action.type === 'activate_lazy') {
                //     component.el.removeAttribute('silica:lazy');
                //
                // }

                this.hideLoaders();
            })
            .catch((error) => {
                this.hideLoaders();
                console.error("Error:", error);
            });
    }

    setQueryParam(paramName, paramValue) {
        const url = new URL(window.location);
        url.searchParams.set(paramName, paramValue);
        window.history.pushState({}, "", url);
    }

    // Performance TODO list
    // - In an init function, cache silica:models in the component

    /*
    find lazy silica_components
    call the activation
     */
    initLazyComponents() {
        const lazyComponentEls = this.querySelectorAll("[silica\\:lazy]");

        lazyComponentEls.forEach((componentEl) => {
            let component = silica_components.find(c => c.id === componentEl.getAttribute('silica:id'))

            if (!component) {
                console.error('Component for lazy activation not found in silica_components array')
                return
            }

            component.activateLazy()
        });
    }

    handleModelInputEvent(event) {
        const el = event.currentTarget;
        const modelName = el.getAttribute("silica:model");

        this.setProperty(modelName, el.value);
    }

    handleClickEvent(event) {
        const el = event.currentTarget;

        let instance = this

        function silicaClick(event, methodString, prevent = false) {
            if (prevent) {
                event.preventDefault();
            }

            // Check if string function call has args
            if (methodString.includes("(")) {
                const methodNameParts = methodString.split("(");
                const methodName = methodNameParts[0];

                // also remove any quotes from left or right of each arg
                const args = methodNameParts[1]
                    .replace(")", "")
                    .split(",")
                    .map((arg) => arg.trim());
                instance.callMethod(methodName, args);
            } else {
                instance.callMethod(methodString);
            }
        }

        if (el.hasAttribute("silica:click")) {
            const methodString = el.getAttribute("silica:click");
            silicaClick(event, methodString);
        } else if (el.hasAttribute("silica:click.prevent")) {
            const methodString = el.getAttribute("silica:click.prevent");
            silicaClick(event, methodString);
        }
    }

    setListeners() {
        const models = this.querySelectorAll("[silica\\:model]");
        models.forEach((element) => {
            element.addEventListener("input", this.boundMethods.handleModelInputEvent);
        });

        const clickables = this.querySelectorAll("[silica\\:click\\.prevent]");
        clickables.forEach((element) => {
            element.addEventListener("click", this.boundMethods.handleClickEvent);
        });
    }

    removeListeners() {
        const models = this.querySelectorAll("[silica\\:model]");
        models.forEach((element) => {
            element.removeEventListener("input", this.boundMethods.handleModelInputEvent);
        });

        const clickables = this.querySelectorAll("[silica\\:click\\.prevent]");
        clickables.forEach((element) => {
            element.removeEventListener("click", this.boundMethods.handleClickEvent);
        });
    }

    updateDom(html) {
        const targetElement = document.querySelector('[silica\\:id="' + this.id + '"]');

        if (targetElement) {
            // Create a temporary div to hold the new HTML content
            let tempDiv = document.createElement("div");
            tempDiv.innerHTML = html;

            // Use morphdom to update the target element with the new content
            morphdom(targetElement, tempDiv.firstChild, {
                onBeforeElUpdated: (fromEl, toEl) => {
                    // If the element being updated is an input, ignore it
                    if (fromEl.tagName === "INPUT" && toEl.tagName === "INPUT") {
                        return false;
                    }
                    if (
                        fromEl.hasAttribute("silica:glued") &&
                        toEl.hasAttribute("silica:glued")
                    ) {
                        return false;
                    }
                    return true; // Continue with the update for other elements
                }
            });

            this.removeListeners();
            this.setListeners();
        } else {
            console.warn(`Element with silica:id="${id}" not found.`);
        }
    }

    processRedirections(jsCalls = []) {
        // Check if we have a redirect
        const redirectFn = jsCalls.find((call) => call.fn === "_silicaRedirect");
        if (redirectFn) {
            window.location.href = redirectFn.args[0];
            return true;
        }
        return false;
    }

    /**
     * Get all elements that match a query, but only if they are inside the subject component
     * @param query
     * @returns []
     */
    querySelectorAll(query) {
        let nodes = [];
        const nodeList = Array.from(this.el.querySelectorAll(query));

        for (let i = 0; i < nodeList.length; i++) {
            if (
                SilicaComponent.getNearestComponent(nodeList[i])?.name === this.name
            ) {
                nodes.push(nodeList[i]);
            }
        }
        return nodes;
    }

    /**
     * Show any silica:loading elements
     * @param action
     */
    showLoaders(action) {
        let target_from_action = null;

        if (action?.type === this.ACTION_TYPE_CALL_METHOD) {
            target_from_action = action?.method_name;
        } else if (action?.type === this.ACTION_TYPE_SET_PROPERTY) {
            target_from_action = action?.name;
        }

        this.querySelectorAll(
            "[silica\\:loading], [silica\\:loading\\.class]"
        ).forEach((el) => {
            if (el.hasAttribute("silica:target")) {
                const silica_target = el.getAttribute("silica:target");
                const target_without_parentheses = silica_target.split("(")[0];

                if (
                    [silica_target, target_without_parentheses].includes(
                        el.getAttribute("silica:target")
                    )
                ) {
                    el.style.display = "block";

                    const classAttr = el.getAttribute("silica:loading.class");
                    this.applyClassesToEl(el, classAttr);
                }
            } else {
                el.style.display = "block";

                const classAttr = el.getAttribute("silica:loading.class");
                this.applyClassesToEl(el, classAttr);
            }
        });
    }

    hideLoaders(action) {
        let target_from_action = null;

        if (action?.target === this.ACTION_TYPE_CALL_METHOD) {
            target_from_action = action?.method_name;
        } else if (action?.target === this.ACTION_TYPE_SET_PROPERTY) {
            target_from_action = action?.name;
        }

        this.querySelectorAll("[silica\\:loading]").forEach((el) => {
            if (el.hasAttribute("silica:target")) {
                const silica_target = el.getAttribute("silica:target");
                const target_without_parentheses = silica_target.split("(")[0];

                if (
                    [silica_target, target_without_parentheses].includes(
                        el.getAttribute("silica:target")
                    )
                ) {
                    el.style.display = "none";

                    const classAttr = el.getAttribute("silica:loading.class");
                    this.removeClassesFromEl(el, classAttr);
                }
            } else {
                el.style.display = "none";

                const classAttr = el.getAttribute("silica:loading.class");
                this.removeClassesFromEl(el, classAttr);
            }
        });
    }

    applyClassesToEl(el, classes = "") {
        if (classes) {
            // Split by space to support multiple classes
            const classes_arr = classes.split(" ");
            el.classList.add(...classes_arr);
        }
    }

    removeClassesFromEl(el, classes = "") {
        if (classes) {
            // Split by space to support multiple classes
            const classes_arr = classes.split(" ");
            el.classList.remove(...classes_arr);
        }
    }

    // statics

    static getNearestComponent(elem) {
        for (; elem && elem !== document; elem = elem.parentNode) {
            if (elem.getAttribute("silica:id")) {
                return {
                    el: elem,
                    id: elem.getAttribute("silica:id"),
                    name: elem.getAttribute("silica:name")
                };
            }
        }
        return false;
    }
}
import React from "react";
import ReactDOM from "react-dom";
import {Provider} from "react-redux";

import App from "./pages/App";
import {setupStore} from "./util";
import {setupSocket} from "./reducers/socket";

import "semantic-ui-css/semantic.min.css";
import "./index.css";
import "./theme.css";

const store = setupStore();
setupSocket(window.BACKEND_URL, store.dispatch);

ReactDOM.render(<Provider store={store}><App/></Provider>, document.getElementById("app"));
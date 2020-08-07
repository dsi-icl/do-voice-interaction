import React from "react";
import ReactDOM from "react-dom";
import {Provider} from "react-redux";

import App from "./pages/App";
import {setupStore} from "./util";
import {setupSocket} from "./reducers/socket";

import "semantic-ui-css/semantic.min.css";
import "./index.css";

const store = setupStore();
setupSocket("http://localhost:8080/sharedsocket", store.dispatch);

const RootNode = () => <React.StrictMode>
    <Provider store={store}>
        <App/>
    </Provider>
</React.StrictMode>;

ReactDOM.render(<RootNode/>, document.getElementById("app"));
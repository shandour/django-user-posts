import React from 'react';
import {Switch} from 'react-router-dom';


export default () => (
        <Switch>
        <UnauthorizedRoute path="/register" component={Register} />
        <UnauthorizedRoute path="/login" component={Login} />

        <AuthorizedOnlyRoute path="/logout" component={Logout} />

        <Route path="/posts" exact component={PostList} />
        <Route path="/posts/:id" component={Post} />
        <Route path=["user/", "/user/:id"] component={Account} />
        </Switch>
);

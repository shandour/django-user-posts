import React from 'react';
import {Switch, Route} from 'react-router-dom';

import {UnauthorizedOnlyRoute, AuthorizedOnlyRoute} from './SpecialRoutes';
import Register from '../components/Auth/Register';
import Login from '../components/Auth/Login';
import Logout from '../components/Auth/Login';
import PostList from '../components/PostList';
import Post from '../components/Post';
import Account from '../components/Account';

export default () => (
        <Switch>
        <UnauthorizedOnlyRoute path="/register" component={Register} />
        <UnauthorizedOnlyRoute path="/login" component={Login} />
        <AuthorizedOnlyRoute path="/logout" component={Logout} />

        <Route path={["/posts", "/"]} exact component={PostList} />
        <Route path="/posts/:id" component={Post} />
        <Route path={["user/", "/user/:id"]} component={Account} />
        </Switch>
);

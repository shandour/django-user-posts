import React, {useContext} from 'react';
import { Route, Redirect } from 'react-router-dom';
import { UserContext } from '../App';


export const UnauthorizedOnlyRoute =  ({
  component: Component,
  path,
    exact = false,
}) => {
    const {isLoggedIn} = useContext(UserContext);
    return (
            <Route
        exact={exact}
        path={path}
        render={innerProps => (
            <>
            {!isLoggedIn ? (
                    <Component {...innerProps} />
            ) : (
                    <Redirect to="/" />
            )}
            </>
        )} />
    );
}


export const AuthorizedOnlyRoute =  ({
    component: Component,
    path,
    exact = false,
}) => {
    const {isLoggedIn} = useContext(UserContext);
    return (
            <Route
        exact={exact}
        path={path}
        render={innerProps => (
            <>
            {isLoggedIn ? (
                    <Component {...innerProps} />
            ) : (
                    <Redirect to="/login" />
            )}
            </>
        )} />
    );
}

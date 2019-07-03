import React, { useEffect, useContext, useState } from "react";
import axios from "../axios";

import { UserContext } from "../App";
import Routes from '../routes/Routes';

export default () => {
  const { login, logout } = useContext(UserContext);
  const [loading, setLoading] = useState(true);

  const checkLogin = async () => {
    try {
        const resp = await axios.get("users/current-user/");
      login(resp.data);
    } catch (err) {
      logout();
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkLogin();
  }, []);

  if (loading) return <>Loading...</>;

  return <Routes />
};

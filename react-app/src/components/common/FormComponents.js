import React from 'react';
import styled, { css } from 'styled-components';
import {Field} from 'formik';

const textInputCss = css`
  width: 100%;
  border-radius: 2px;
  font-size: 16px;;

  &:focus {
    border: 1px solid darkgray;
  }
`;

export const TextInput = styled(Field)`
  ${textInputCss}
  height: 40px;
`;

export const ErrorDiv = styled.div`
  color: red;
`;

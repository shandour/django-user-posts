import React, {useContext} from 'react';
import { Formik, Form, ErrorMessage } from 'formik';
import {UserContext} from '../../App';
import axios from '../../axios';
import {TextInput, ErrorDiv} from '../common/FormComponents';

export default ({history}) => {
    const { login } = useContext(UserContext);
    return (
            <Formik
        initialValues={{
            email: '',
            password: '',
        }}
        onSubmit={async (values, { setSubmitting, setErrors }) => {
            setSubmitting(true);
            const {email, password} = values;
            try {
                const resp = await axios.post('users/token/', {email, password});
                login(resp.data);
                history.push('/');
            } catch ({ response: { data } }) {
                setErrors(data);
            } finally {
                setSubmitting(false);
            }
        }}
            >
            {({ isSubmitting, errors }) => (
                    <Form>
                    <TextInput
                type="email"
                name="email"
                placeholder="Email address"
                disabled={isSubmitting}
                    />
                    <ErrorMessage name="email" component={ErrorDiv} />
                    <TextInput
                type="password"
                name="password"
                placeholder="Password"
                disabled={isSubmitting}
                    />
                    <ErrorMessage name="password" component={ErrorDiv} />
                    <button disabled={isSubmitting} type="submit">
                    Login
                </button>
                    {errors.nonFieldErrors &&
                     <ErrorDiv>{'. '.join(errors.nonFieldErrors)}</ErrorDiv>
                    }
                {errors.detail &&
                 <ErrorDiv>{errors.detail}</ErrorDiv>
                }
                </Form>
            )}
        </Formik>
    );
}

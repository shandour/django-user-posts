import React, {useContext, useState} from 'react';
import {isEmpty} from 'lodash';
import {UserContext} from '../../App';
import axios from '../../axios';
import {GenericTextInput as TextInput, ErrorDiv} from '../common/FormComponents';

// key: fieldName, value: [placeholder, label, type, required, maxLength]
const userFields = {
    firstName: ['Fill in your first name', 'First name', 'text', false, 50],
    lastName: ['Fill in your last name', 'Last name', 'text', false, 150],
    email: ['Fill in your email',' Email', 'email', true],
    password: ['Provide a password', 'Password', 'password', true],
    passwordConfirmation: ['Confirm your password', 'Password Confirmation', 'password', true],
    location: ['Fill in your location', 'Location', 'text', false, 200],
};
const companyFields = {
    name: ['Fill in your company name', 'Company name', 'text', true, 100],
    legalName: ['Fill in your company legal name', 'Company legal name', 'text', false, 200],
    location: ['Fill in your company location', 'Company location', 'text', false, 200],
    description: ['Fill in your company description', 'Company description', 'textarea', true],
    domain: ['Fill in your company dmain', 'Company domain', 'url', true, 100]
};


export default ({history}) => {
    const { login } = useContext(UserContext);
    const [showCompanyForm, setShowCompanyForm] = useState(false);
    const [isSubmitting, setSubmitting] = useState(false);
    const [errors, setErrors] = useState({});
    const [data, setData] = useState({'company': {}});

    const setField = (value, fieldName) => {
        data[fieldName] = value;
        setData(data);
    };

    const setCompanyField = (value, fieldName) => {
        const {company} = data;
        company[fieldName] = value;
        data.company = company;
        setData(data);
    };

    const onSubmit = async (e) => {
        e.preventDefault();
        setErrors({});
        setSubmitting(true);
        console.log(data)

        try {
            if (data.password !== data.passwordConfirmation) {
                setErrors({passwordConfirmation: ['Passwords do not match.']});
                return;
            }

            if (isEmpty(data.company) || !showCompanyForm) {
                delete data.company;
            }
            
            const resp = await axios.post('users/register/', data);
            login(resp.data);
            history.push('/');
        } catch ({ response: { data } }) {
            setErrors(data);
        } finally {
            setSubmitting(false);
        }
    };


    return (
            <form onSubmit={onSubmit}>
            {Object.entries(userFields).map(fieldData => (
                    <div key={fieldData[0]}>
                    <label htmlFor={fieldData[0]}>{fieldData[1][1]}</label>
                    <TextInput
                type={fieldData[1][2]}
                name={fieldData[0]}
                placeholder={fieldData[1][0]}
                disabled={isSubmitting}
                required={fieldData[1][3]}
                maxLength={fieldData[1][4]}
                onChange={e => {
                    setField(e.target.value, fieldData[0]);
                }}
                    />
                    {errors[fieldData[0]] &&
                     <ErrorDiv>{errors[fieldData[0]].join('. ')}</ErrorDiv>
                    }
                </div>
            ))}
            <input type="checkbox" value={showCompanyForm} onChange={() => setShowCompanyForm(!showCompanyForm)} />


        {showCompanyForm && (
            <>
                <button type="button" onClick={
                    // fetch stuff, if smth fill
                    () => {}
                }>Autofill based on email</button>
                <button type="button" onClick={
                    () => {}
                }>Autofill based on domain</button>

            {Object.entries(companyFields).map(fieldData => (
                    <div key={fieldData[0]}>
                    <label htmlFor={fieldData[0]}>{fieldData[1][1]}</label>
                    {fieldData[1][2] !== 'textarea' ? (
                            <TextInput
                        type={fieldData[1][2]}
                        name={fieldData[0]}
                        placeholder={fieldData[1][0]}
                        disabled={isSubmitting}
                        required={fieldData[1][3]}
                        maxLength={fieldData[1][4]}
                        onChange={e => {
                            setCompanyField(e.target.value, fieldData[0]);
                        }}
                            />) :(
                                    <textarea
                                                key={fieldData[0]}
                                name={fieldData[0]}
                                placeholder={fieldData[1][0]}
                                disabled={isSubmitting}
                                required={fieldData[1][3]}
                                onChange={e => {
                                    setCompanyField(e.target.value, fieldData[0]);
                                }}>
                                    </textarea>
                            )}
                {(errors.company && errors.company[fieldData[0]]) &&
                 <ErrorDiv>{errors[fieldData[0]].join('. ')}</ErrorDiv>
                }
                </div>
            ))}

                </>
        )}

                    <button disabled={isSubmitting} type="submit">
                    Register
                </button>
                    {errors.nonFieldErrors &&
                     <ErrorDiv>{errors.nonFieldErrors.join('. ')}</ErrorDiv>
                    }
                {errors.detail &&
                 <ErrorDiv>{errors.detail}</ErrorDiv>
                }
                </form>
    );
}

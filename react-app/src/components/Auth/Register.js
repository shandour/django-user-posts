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

// enrichment API options
const EMAIL = 'email';
const DOMAIN = 'domain';

export default ({history}) => {
    const { login } = useContext(UserContext);
    const [showCompanyForm, setShowCompanyForm] = useState(false);
    const [isSubmitting, setSubmitting] = useState(false);
    const [errors, setErrors] = useState({});
    const [enrichmentErrors, setEnrichmentErrors] = useState({});
    const [data, setData] = useState({'company': {}});
    const [enrichmentMessage, setEnrichmentMessage] = useState('');

    const fetchEnrichmentData = (queryType, queryByCompany=false) => async () => {
        setSubmitting(true);
        setEnrichmentErrors({});
        const queryParams = {};
        let enrichedData = {...data};
        try {
            if (queryType === EMAIL) {
                queryParams[queryType] = data.email;
            }
            else if (queryType === DOMAIN) {
                queryParams[queryType] = data.company.domain;
            } else {
                return;
            }
            queryParams.company = queryByCompany;
            const {data: respData} = await axios.get(
                'users/enrichment/',
                {params: queryParams}
            );
            if (isEmpty(respData)) {
                setEnrichmentMessage('Nothing found to satisfy your request.')
                setTimeout(
                    () => setEnrichmentMessage(''),
                    3000
                );
            } else if (queryByCompany && respData) {
                enrichedData.company = respData.company;
                setData(enrichedData);
            } else {
                if (respData.person) {
                    enrichedData = respData.person;
                }
                if (respData.company) {
                    enrichedData.company = respData.company;
                }
                enrichedData.email = data.email;
                setData(enrichedData);
            }
        } catch ({response: {data: errData}}) {
            setEnrichmentErrors(errData);
        } finally {
            setSubmitting(false);
        }
    };

    const setField = (value, fieldName) => {
        const dataCopy = {...data};
        dataCopy[fieldName] = value;
        setData(dataCopy);
    };

    const setCompanyField = (value, fieldName) => {
        const {company} = data;
        const dataCopy = {...data};
        company[fieldName] = value;
        dataCopy.company = company;
        setData(dataCopy);
    };

    const onSubmit = async (e) => {
        e.preventDefault();
        setErrors({});
        setEnrichmentErrors({});
        setSubmitting(true);

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
            {enrichmentMessage && <div>{enrichmentMessage}</div>}
        {enrichmentErrors.errors &&
         <ErrorDiv>{enrichmentErrors.errors}</ErrorDiv>
        }
            <button type="button" onClick={
                fetchEnrichmentData(EMAIL)
            }>Autofill based on email</button>
            {Object.entries(userFields).map(fieldData => (
                    <div key={fieldData[0]}>
                    <label htmlFor={fieldData[0]}>{fieldData[1][1]}</label>
                    <TextInput
                value={data[fieldData[0]] || ''}
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
            )
                                           )}
            <input type="checkbox" value={showCompanyForm} onChange={() => setShowCompanyForm(!showCompanyForm)} />


        {showCompanyForm && (
                <>
                <button type="button" onClick={
                    fetchEnrichmentData(DOMAIN, true)
                }>Autofill based on domain</button>

            {Object.entries(companyFields).map(fieldData => (
                    <div key={fieldData[0]}>
                    <label htmlFor={fieldData[0]}>{fieldData[1][1]}</label>
                    {fieldData[1][2] !== 'textarea' ? (
                            <TextInput
                        value={data.company ? data.company[fieldData[0]] : ''}
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
                                value={data.company ? data.company[fieldData[0]] : ''}
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

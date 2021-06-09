import React from 'react';
import ReactDom from 'react-dom';
import Comp1 from 'Comp1';
import Comp2 from 'Comp2';

const Crm = ({}) => {
    return <>
        <h1>Hello WRLD</h1>
        <Comp1 />
        <Comp2 />
    </>
}






ReactDom.render(
    <Crm />,
    document.getElementById('reactDiv')
)